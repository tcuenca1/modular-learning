"""Almacén de documentos de texto donde los repositorios guardan su JSON.

Los repositorios serializan igual que siempre y solo delegan dónde vive cada documento:

- `AlmacenArchivos`: archivos bajo la carpeta de datos (ML_DATA_DIR). Es el modo local.
- `AlmacenPostgres`: una tabla `documentos` en Postgres (DATABASE_URL). Es el modo en la nube,
  donde el disco del servidor no persiste entre reinicios.

Las claves son rutas relativas con `/`, las mismas que en disco: `schedules/X_cronograma.json`,
`config/materias.txt`, `repaso/tarjetas.json`…
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from functools import lru_cache
from pathlib import Path
from typing import Any

from modular_learning import settings

TABLA = "documentos"

# Un candado reentrante por documento, compartido por todas las instancias del proceso
_CANDADOS: dict[str, threading.RLock] = {}
_GUARDA_CANDADOS = threading.Lock()
_REINTENTOS_REEMPLAZO = 8


class AlmacenDocumentos(ABC):
    """Documentos de texto identificados por una clave con forma de ruta relativa."""

    @abstractmethod
    def leer(self, clave: str) -> str | None:
        """Contenido del documento, o None si no existe."""

    @abstractmethod
    def escribir(self, clave: str, contenido: str) -> None:
        """Crea o reemplaza el documento."""

    @abstractmethod
    def listar(self, prefijo: str = "") -> list[str]:
        """Claves que empiezan por `prefijo`, ordenadas."""

    @abstractmethod
    def eliminar(self, clave: str) -> bool:
        """Borra el documento; retorna False si no existía."""

    def _identidad_candado(self, clave: str) -> str:
        """Texto que identifica el documento aunque haya varias instancias del almacén."""
        return f"{id(self)}:{clave}"

    def bloquear(self, clave: str) -> AbstractContextManager[Any]:
        """
        Candado del documento para serializar un ciclo leer-modificar-escribir dentro del
        proceso. Es reentrante: un método que ya lo tiene puede llamar a otro que lo pida.
        """
        identidad = self._identidad_candado(clave)
        with _GUARDA_CANDADOS:
            return _CANDADOS.setdefault(identidad, threading.RLock())


class AlmacenArchivos(AlmacenDocumentos):
    """Documentos como archivos bajo `raiz` (por defecto, la carpeta de datos actual)."""

    def __init__(self, raiz: str | Path | None = None):
        self._raiz = Path(raiz) if raiz is not None else None

    @property
    def raiz(self) -> Path:
        # Se resuelve en cada uso para respetar cambios de ML_DATA_DIR (tests, CLI)
        return self._raiz if self._raiz is not None else settings.ruta_data()

    def _ruta(self, clave: str) -> str:
        return os.path.join(self.raiz, *clave.split("/"))

    def _identidad_candado(self, clave: str) -> str:
        return os.path.normcase(os.path.abspath(self._ruta(clave)))

    def leer(self, clave: str) -> str | None:
        ruta = self._ruta(clave)
        if not os.path.exists(ruta):
            return None
        try:
            with open(ruta, encoding="utf-8") as f:
                return f.read()
        except OSError:
            return None

    def escribir(self, clave: str, contenido: str) -> None:
        ruta = self._ruta(clave)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        # Nombre temporal único: dos escrituras a la vez no se pisan el archivo intermedio
        temporal = f"{ruta}.{uuid.uuid4().hex}.tmp"
        try:
            with open(temporal, "w", encoding="utf-8") as f:
                f.write(contenido)
            for intento in range(_REINTENTOS_REEMPLAZO):
                try:
                    os.replace(temporal, ruta)
                    return
                except PermissionError:  # Windows: otro proceso tiene el destino abierto
                    if intento == _REINTENTOS_REEMPLAZO - 1:
                        raise
                    time.sleep(0.02 * (intento + 1))
        finally:
            if os.path.exists(temporal):
                os.remove(temporal)

    def listar(self, prefijo: str = "") -> list[str]:
        carpeta, _, inicio_nombre = prefijo.rpartition("/")
        base = os.path.join(self.raiz, *carpeta.split("/")) if carpeta else str(self.raiz)
        if not os.path.isdir(base):
            return []
        return sorted(
            f"{carpeta}/{nombre}" if carpeta else nombre
            for nombre in os.listdir(base)
            if nombre.startswith(inicio_nombre)
            and not nombre.endswith(".tmp")
            and os.path.isfile(os.path.join(base, nombre))
        )

    def eliminar(self, clave: str) -> bool:
        ruta = self._ruta(clave)
        if not os.path.isfile(ruta):
            return False
        os.remove(ruta)
        return True


class AlmacenPostgres(AlmacenDocumentos):
    """
    Documentos en la tabla `documentos` de Postgres, con un pool de conexiones y una instantánea
    en memoria de toda la tabla.

    Cada consulta a la base remota (Neon) cuesta un viaje de red, así que se carga la tabla
    entera en una sola consulta y las lecturas y listados se sirven de memoria. Las escrituras
    actualizan la base y la instantánea. La instantánea caduca a los `segundos_cache`
    (ML_CACHE_SEGUNDOS, 30 por defecto) para ver cambios hechos por otro proceso, como el script
    `deploy/subir_datos.py`. Pensado para un único proceso del servidor y pocos datos.
    """

    def __init__(self, url: str, pool: Any | None = None, segundos_cache: float | None = None):
        if pool is None:
            from psycopg_pool import ConnectionPool

            # check_connection descarta conexiones que el servidor cerró (Neon suspende la base
            # de datos tras unos minutos sin uso)
            pool = ConnectionPool(
                url,
                min_size=1,
                max_size=4,
                check=ConnectionPool.check_connection,
                open=True,
            )
        self._pool = pool
        self._segundos_cache = (
            segundos_cache
            if segundos_cache is not None
            else float(os.getenv("ML_CACHE_SEGUNDOS", "30"))
        )
        self._instantanea: dict[str, str] | None = None
        self._cargada_en = 0.0
        self._candado_carga = threading.Lock()
        with self._pool.connection() as conn:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS {TABLA} ("
                "clave text PRIMARY KEY, "
                "contenido text NOT NULL, "
                "actualizado timestamptz NOT NULL DEFAULT now())"
            )

    def _vigente(self) -> dict[str, str]:
        """Instantánea de la tabla; se vuelve a cargar (una consulta) si no existe o caducó."""
        instantanea = self._instantanea
        if instantanea is not None and time.monotonic() - self._cargada_en < self._segundos_cache:
            return instantanea
        with self._candado_carga:
            instantanea = self._instantanea
            if instantanea is None or time.monotonic() - self._cargada_en >= self._segundos_cache:
                with self._pool.connection() as conn:
                    filas = conn.execute(f"SELECT clave, contenido FROM {TABLA}").fetchall()
                instantanea = {clave: contenido for clave, contenido in filas}
                self._instantanea = instantanea
                self._cargada_en = time.monotonic()
            return instantanea

    def precalentar(self) -> None:
        """Carga la instantánea (y de paso despierta la base de datos) antes de la primera petición."""
        self._vigente()

    def leer(self, clave: str) -> str | None:
        return self._vigente().get(clave)

    def escribir(self, clave: str, contenido: str) -> None:
        with self._pool.connection() as conn:
            conn.execute(
                f"INSERT INTO {TABLA} (clave, contenido) VALUES (%s, %s) "
                "ON CONFLICT (clave) DO UPDATE "
                "SET contenido = EXCLUDED.contenido, actualizado = now()",
                (clave, contenido),
            )
        self._vigente()[clave] = contenido

    def listar(self, prefijo: str = "") -> list[str]:
        return sorted(c for c in self._vigente() if c.startswith(prefijo))

    def eliminar(self, clave: str) -> bool:
        with self._pool.connection() as conn:
            cursor = conn.execute(f"DELETE FROM {TABLA} WHERE clave = %s", (clave,))
        self._vigente().pop(clave, None)
        return cursor.rowcount > 0

    def vaciar_cache(self) -> None:
        """Invalida la instantánea: la próxima lectura vuelve a consultar la base."""
        self._instantanea = None


@lru_cache(maxsize=4)
def _almacen_postgres(url: str) -> AlmacenPostgres:
    return AlmacenPostgres(url)


def almacen_global() -> AlmacenDocumentos:
    """Postgres si hay DATABASE_URL (despliegue en la nube); si no, archivos en ML_DATA_DIR."""
    url = os.getenv("DATABASE_URL", "").strip()
    return _almacen_postgres(url) if url else AlmacenArchivos()


def almacen_por_defecto() -> AlmacenDocumentos:
    """El almacén de los repositorios de datos (hoy el global; luego el de la cuenta activa)."""
    return almacen_global()


def almacen_en(ruta: str | None) -> tuple[AlmacenDocumentos, str] | None:
    """Para los repositorios que aceptan una ruta de archivo explícita (tests y CLI)."""
    if not ruta:
        return None
    return AlmacenArchivos(os.path.dirname(ruta)), os.path.basename(ruta)


class DocumentoJson:
    """Un documento JSON del almacén: el que usa por defecto o el de una ruta explícita."""

    def __init__(
        self,
        clave: str,
        ruta_archivo: str | None = None,
        almacen: AlmacenDocumentos | None = None,
    ):
        explicito = almacen_en(ruta_archivo)
        self._almacen, self.clave = explicito if explicito else (almacen, clave)

    @property
    def almacen(self) -> AlmacenDocumentos:
        return self._almacen or almacen_por_defecto()

    def bloqueo(self) -> AbstractContextManager[Any]:
        """Candado del documento para un ciclo leer-modificar-escribir (reentrante)."""
        return self.almacen.bloquear(self.clave)

    def leer(self, defecto: Any) -> Any:
        texto = self.almacen.leer(self.clave)
        if texto is None:
            return defecto
        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            return defecto

    def escribir(self, datos: Any, sangria: int = 2) -> None:
        self.almacen.escribir(self.clave, json.dumps(datos, indent=sangria, ensure_ascii=False))


__all__ = [
    "AlmacenArchivos",
    "AlmacenDocumentos",
    "AlmacenPostgres",
    "DocumentoJson",
    "almacen_en",
    "almacen_global",
    "almacen_por_defecto",
]
