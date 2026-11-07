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
from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import Any

from modular_learning import settings

TABLA = "documentos"


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
        temporal = f"{ruta}.tmp"
        with open(temporal, "w", encoding="utf-8") as f:
            f.write(contenido)
        os.replace(temporal, ruta)

    def listar(self, prefijo: str = "") -> list[str]:
        carpeta, _, inicio_nombre = prefijo.rpartition("/")
        base = os.path.join(self.raiz, *carpeta.split("/")) if carpeta else str(self.raiz)
        if not os.path.isdir(base):
            return []
        return sorted(
            f"{carpeta}/{nombre}" if carpeta else nombre
            for nombre in os.listdir(base)
            if nombre.startswith(inicio_nombre) and os.path.isfile(os.path.join(base, nombre))
        )

    def eliminar(self, clave: str) -> bool:
        ruta = self._ruta(clave)
        if not os.path.isfile(ruta):
            return False
        os.remove(ruta)
        return True


class AlmacenPostgres(AlmacenDocumentos):
    """Documentos en la tabla `documentos` de Postgres, con un pool de conexiones y caché en memoria."""

    def __init__(self, url: str, pool: Any | None = None):
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
        self._cache: dict[str, str | None] = {}
        with self._pool.connection() as conn:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS {TABLA} ("
                "clave text PRIMARY KEY, "
                "contenido text NOT NULL, "
                "actualizado timestamptz NOT NULL DEFAULT now())"
            )

    def leer(self, clave: str) -> str | None:
        if clave in self._cache:
            return self._cache[clave]
        with self._pool.connection() as conn:
            fila = conn.execute(
                f"SELECT contenido FROM {TABLA} WHERE clave = %s", (clave,)
            ).fetchone()
        contenido = fila[0] if fila else None
        self._cache[clave] = contenido
        return contenido

    def escribir(self, clave: str, contenido: str) -> None:
        self._cache[clave] = contenido
        with self._pool.connection() as conn:
            conn.execute(
                f"INSERT INTO {TABLA} (clave, contenido) VALUES (%s, %s) "
                "ON CONFLICT (clave) DO UPDATE "
                "SET contenido = EXCLUDED.contenido, actualizado = now()",
                (clave, contenido),
            )

    def listar(self, prefijo: str = "") -> list[str]:
        # left() en lugar de LIKE: los "_" de los nombres no deben actuar como comodines
        with self._pool.connection() as conn:
            filas = conn.execute(
                f"SELECT clave, contenido FROM {TABLA} WHERE left(clave, %s) = %s ORDER BY clave",
                (len(prefijo), prefijo),
            ).fetchall()
        for clave_doc, contenido_doc in filas:
            self._cache[clave_doc] = contenido_doc
        return [f[0] for f in filas]

    def eliminar(self, clave: str) -> bool:
        self._cache.pop(clave, None)
        with self._pool.connection() as conn:
            cursor = conn.execute(f"DELETE FROM {TABLA} WHERE clave = %s", (clave,))
        return cursor.rowcount > 0

    def vaciar_cache(self) -> None:
        """Invalida la caché local en memoria."""
        self._cache.clear()


@lru_cache(maxsize=4)
def _almacen_postgres(url: str) -> AlmacenPostgres:
    return AlmacenPostgres(url)


def almacen_por_defecto() -> AlmacenDocumentos:
    """Postgres si hay DATABASE_URL (despliegue en la nube); si no, archivos en ML_DATA_DIR."""
    url = os.getenv("DATABASE_URL", "").strip()
    return _almacen_postgres(url) if url else AlmacenArchivos()


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
    "almacen_por_defecto",
]
