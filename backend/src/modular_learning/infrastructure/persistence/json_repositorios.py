"""Implementaciones en JSON de los puertos de persistencia y repositorios."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, ClassVar

from modular_learning.core.domain.cronograma import asignar_ids, buscar_clase, es_completada
from modular_learning.core.domain.materias import Materia, slug_materia
from modular_learning.core.domain.proyectos import Proyecto
from modular_learning.core.ports.plugin_practico import PluginConfigRepoPort
from modular_learning.core.ports.proyectos import ProyectosRepo
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)
from modular_learning.infrastructure.persistence.almacen import (
    AlmacenArchivos,
    AlmacenDocumentos,
    DocumentoJson,
    almacen_por_defecto,
)

SUFIJO_CRONOGRAMA = "_cronograma.json"


class JsonMateriaRepo(MateriaRepo):
    """Catálogo de asignaturas en config/materias.json como [{slug, nombre}]."""

    MATERIAS_INICIALES: ClassVar[list[str]] = [
        "Seguridad de la Informacion",
        "Ingenieria de Software II",
        "Programacion Web",
        "Internet de las Cosas",
        "Tecnologias de Conmutacion I",
    ]

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("config/materias.json", ruta_archivo, almacen)

    def _escribir(self, materias: list[Materia]) -> None:
        self._documento.escribir([m.a_dict() for m in materias], sangria=4)

    def listar(self) -> list[Materia]:
        datos = self._documento.leer(None)
        if datos is None:
            # Migración automática desde config/materias.txt si existe
            texto_legado = self._documento.almacen.leer("config/materias.txt")
            if texto_legado:
                lineas = [l.strip() for l in texto_legado.splitlines() if l.strip()]
                materias = [Materia.desde_nombre(n) for n in lineas if n]
            else:
                materias = [Materia.desde_nombre(n) for n in self.MATERIAS_INICIALES]
            self._escribir(materias)
            return materias
        materias: list[Materia] = []
        for item in datos if isinstance(datos, list) else []:
            materia = Materia.desde_dict(item) if isinstance(item, dict) else None
            if materia and all(m.slug != materia.slug for m in materias):
                materias.append(materia)
        return materias

    def guardar(self, materia: Materia) -> None:
        materias = self.listar()
        for i, m in enumerate(materias):
            if m.slug == materia.slug:
                materias[i] = materia
                break
        else:
            materias.append(materia)
        self._escribir(materias)

    def eliminar(self, slug: str) -> bool:
        buscado = slug_materia(slug)
        materias = self.listar()
        restantes = [m for m in materias if m.slug != buscado]
        if len(restantes) == len(materias):
            return False
        self._escribir(restantes)
        return True

    def cargar_materias(self) -> list[str]:
        return [m.nombre for m in self.listar()]

    def agregar_materia(self, nueva_materia: str) -> None:
        if nueva_materia and nueva_materia.strip():
            materia = Materia.desde_nombre(nueva_materia.strip())
            materias = self.listar()
            if any(m.slug == materia.slug for m in materias):
                return
            materias.append(materia)
            self._escribir(materias)


class JsonCronogramaRepo(CronogramaRepo):
    """
    Gestión de cronogramas con persistencia de clases, material transversal y cortes de parcial.
    Identifica asignaturas por slug o nombre sin importar mayúsculas ni guiones.
    """

    def __init__(
        self, carpeta_schedules: str | None = None, almacen: AlmacenDocumentos | None = None
    ):
        if carpeta_schedules:
            self._almacen: AlmacenDocumentos | None = AlmacenArchivos(carpeta_schedules)
            self.prefijo = ""
        else:
            self._almacen = almacen
            self.prefijo = "schedules/"

    @property
    def almacen(self) -> AlmacenDocumentos:
        return self._almacen or almacen_por_defecto()

    def _nombres(self) -> list[str]:
        """Nombres de documento (sin prefijo) de todos los cronogramas."""
        return [
            clave[len(self.prefijo) :]
            for clave in self.almacen.listar(self.prefijo)
            if clave.endswith((SUFIJO_CRONOGRAMA, ".json"))
            and "/" not in clave[len(self.prefijo) :]
        ]

    @staticmethod
    def _slug(materia: str) -> str:
        return (
            "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
            .strip()
            .replace(" ", "_")
        )

    def _encontrar_clave_cronograma(self, materia: str) -> str | None:
        """
        Documento del cronograma cuyo nombre tiene el mismo slug que la materia. La coincidencia
        es exacta: "Ingenieria de Software" no debe leer, sobrescribir ni borrar el cronograma
        de "Ingenieria de Software II".
        """
        buscado = slug_materia(materia)
        if not buscado:
            return None
        for nombre in self._nombres():
            base = nombre.removesuffix(SUFIJO_CRONOGRAMA).removesuffix(".json")
            if slug_materia(base) == buscado:
                return self.prefijo + nombre
        return None

    def _leer(self, clave: str) -> Any:
        texto = self.almacen.leer(clave)
        return json.loads(texto) if texto is not None else None

    def _escribir(self, clave: str, datos: Any) -> None:
        self.almacen.escribir(clave, json.dumps(datos, indent=4, ensure_ascii=False))

    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return None
        try:
            data = self._leer(clave)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                clases = data.get("clases", data.get("cronograma", []))
                return clases if isinstance(clases, list) else []
            return None
        except Exception as e:
            print(f"⚠️ Error al leer cronograma de {materia}: {e}")
            return None

    def guardar_cronograma(self, materia: str, clases: list[dict[str, Any]]) -> str:
        asignar_ids(clases)
        clave = self._encontrar_clave_cronograma(materia) or (
            f"{self.prefijo}{slug_materia(materia)}{SUFIJO_CRONOGRAMA}"
        )

        data_orig: Any = None
        try:
            data_orig = self._leer(clave)
        except Exception:
            pass

        if isinstance(data_orig, dict):
            data_orig["clases"] = clases
            self._escribir(clave, data_orig)
        else:
            self._escribir(clave, {"clases": clases})
        return clave

    def eliminar_cronograma(self, materia: str) -> bool:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return False
        return self.almacen.eliminar(clave)

    def listar_cronogramas(self) -> dict[str, list[dict[str, Any]]]:
        cronogramas: dict[str, list[dict[str, Any]]] = {}
        for nombre in sorted(self._nombres()):
            base = nombre.removesuffix(SUFIJO_CRONOGRAMA).removesuffix(".json")
            slug = slug_materia(base)
            try:
                data = self._leer(self.prefijo + nombre)
            except Exception:
                continue
            clases = (
                data.get("clases", data.get("cronograma", [])) if isinstance(data, dict) else data
            )
            if isinstance(clases, list):
                cronogramas[slug] = clases
        return cronogramas

    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        clases = self.obtener_cronograma(materia) or []
        pendientes = [c for c in clases if not es_completada(c)]
        for c in pendientes:
            c.setdefault("subtemas_adicionales", [])
            c.setdefault("materiales_asociados", [])
        return pendientes[:5]

    def obtener_detalle_clase(
        self, materia: str, tema: str | None = None, clase_id: str | None = None
    ) -> dict[str, Any]:
        clases = self.obtener_cronograma(materia) or []
        clase = buscar_clase(clases, clase_id=clase_id, tema=tema)
        if clase is not None:
            clase.setdefault("subtemas_adicionales", [])
            clase.setdefault("materiales_asociados", [])
            return clase
        return {"subtemas_adicionales": [], "materiales_asociados": []}

    def marcar_clase(
        self,
        materia: str,
        clase_id: str | None = None,
        tema: str | None = None,
        estado: str = "completado",
    ) -> bool:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return False
        data = self._leer(clave)
        if isinstance(data, list):
            clases = data
            es_lista = True
        elif isinstance(data, dict):
            clases = data.get("clases", data.get("cronograma", []))
            es_lista = False
        else:
            return False

        if not isinstance(clases, list):
            return False

        clase = buscar_clase(clases, clase_id=clase_id, tema=tema)
        if clase is not None:
            clase["estado"] = estado
            if es_lista:
                self._escribir(clave, {"clases": clases})
            else:
                data["clases"] = clases
                self._escribir(clave, data)
            return True
        return False

    def marcar_clase_completada(
        self, materia: str, tema_exacto: str, clase_id: str | None = None
    ) -> bool:
        return self.marcar_clase(materia, clase_id=clase_id, tema=tema_exacto, estado="completado")

    def agregar_material_transversal(self, materia: str, item: dict[str, Any]) -> None:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return
        data = self._leer(clave)
        if isinstance(data, list):
            data = {"clases": data}
        elif not isinstance(data, dict):
            data = {"clases": []}
        data.setdefault("material_transversal", []).append(item)
        self._escribir(clave, data)

    def quitar_material_transversal(self, materia: str, nombre_archivo: str) -> bool:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return False
        data = self._leer(clave)
        if not isinstance(data, dict):
            return False
        items = data.get("material_transversal", [])
        restantes = [i for i in items if str(i.get("archivo", "")) != nombre_archivo]
        if len(restantes) == len(items):
            return False
        data["material_transversal"] = restantes
        self._escribir(clave, data)
        return True

    def obtener_parciales(self, materia: str) -> list[dict[str, Any]]:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return []
        data = self._leer(clave)
        if isinstance(data, dict):
            parciales = data.get("parciales", [])
            return parciales if isinstance(parciales, list) else []
        return []

    def guardar_parciales(self, materia: str, parciales: list[dict[str, Any]]) -> None:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            clave = f"{self.prefijo}{slug_materia(materia)}{SUFIJO_CRONOGRAMA}"
            data = {"clases": [], "parciales": parciales}
        else:
            data = self._leer(clave)
            if isinstance(data, list):
                data = {"clases": data}
            elif not isinstance(data, dict):
                data = {"clases": []}
            data["parciales"] = parciales
        self._escribir(clave, data)


class JsonRegistroMaterialesRepo(RegistroMaterialesRepo):
    """Registro de material en config/registro_materiales.json como [{nombre, materia, ...}]."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("config/registro_materiales.json", ruta_archivo, almacen)

    def _cargar(self) -> list[dict[str, Any]]:
        try:
            contenido = self._documento.leer(None)
        except Exception:
            return []
        if isinstance(contenido, list):
            return [r for r in contenido if isinstance(r, dict)]
        if isinstance(contenido, dict):
            return [
                {"nombre": k, "materia": v.get("materia", ""), "fecha": v.get("fecha", "")}
                for k, v in contenido.items()
                if isinstance(v, dict)
            ]
        return []

    def _escribir(self, registro: list[dict[str, Any]]) -> None:
        self._documento.escribir(registro, sangria=4)

    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        buscado = nombre_archivo.lower()
        return any(str(r.get("nombre", "")).lower() == buscado for r in self._cargar())

    def registrar_material(
        self, nombre_archivo: str, materia: str, nota: str | None = None
    ) -> None:
        buscado = nombre_archivo.lower()
        registro = [r for r in self._cargar() if str(r.get("nombre", "")).lower() != buscado]
        entrada: dict[str, Any] = {
            "nombre": nombre_archivo,
            "materia": slug_materia(materia),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        if nota:
            entrada["nota"] = nota
        registro.append(entrada)
        self._escribir(registro)

    def listar_materiales(self) -> list[dict[str, Any]]:
        return self._cargar()

    def eliminar_material(self, nombre_archivo: str) -> dict[str, Any] | None:
        buscado = nombre_archivo.lower()
        registro = self._cargar()
        quitado = next((r for r in registro if str(r.get("nombre", "")).lower() == buscado), None)
        if quitado is None:
            return None
        self._escribir([r for r in registro if r is not quitado])
        return quitado

    def eliminar_de_materia(self, materia: str) -> int:
        slug = slug_materia(materia)
        registro = self._cargar()
        restantes = [r for r in registro if slug_materia(str(r.get("materia", ""))) != slug]
        if len(restantes) != len(registro):
            self._escribir(restantes)
        return len(registro) - len(restantes)

    def vaciar(self) -> int:
        registro = self._cargar()
        total = len(registro)
        self._escribir([])
        return total


class JsonPluginConfigRepo(PluginConfigRepoPort):
    """Implementación de PluginConfigRepoPort persistiendo en config/plugins.json."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("config/plugins.json", ruta_archivo, almacen)

    def obtener_configuraciones(self) -> dict[str, dict[str, Any]]:
        datos = self._documento.leer({})
        return datos if isinstance(datos, dict) else {}

    def guardar_configuracion(
        self, clave: str, carpeta: str | None = None, materia: str | None = None
    ) -> dict[str, Any]:
        datos = self.obtener_configuraciones()
        clave_norm = clave.lower().strip()
        actual = dict(datos.get(clave_norm, {}))

        if carpeta is not None:
            actual["carpeta"] = carpeta.strip()
        if materia is not None:
            actual["materia"] = materia.strip()

        datos[clave_norm] = actual
        self._documento.escribir(datos, sangria=4)
        return actual


class JsonProyectosRepo(ProyectosRepo):
    """Implementación de ProyectosRepo persistiendo en config/proyectos.json."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("config/proyectos.json", ruta_archivo, almacen)

    def guardar(self, proyecto: Proyecto) -> None:
        datos = self._documento.leer({})
        if not isinstance(datos, dict):
            datos = {}
        datos[proyecto.id] = proyecto.a_dict()
        self._documento.escribir(datos, sangria=4)

    def obtener(self, id_proyecto: str) -> Proyecto | None:
        datos = self._documento.leer({})
        if not isinstance(datos, dict) or id_proyecto not in datos:
            return None
        return Proyecto.desde_dict(datos[id_proyecto])

    def listar(self, materia: str | None = None) -> list[Proyecto]:
        datos = self._documento.leer({})
        if not isinstance(datos, dict):
            return []
        proyectos = [Proyecto.desde_dict(v) for v in datos.values()]
        if materia:
            buscado = slug_materia(materia)
            proyectos = [p for p in proyectos if slug_materia(p.materia) == buscado]
        return sorted(proyectos, key=lambda p: (p.materia, p.parcial, p.nombre))

    def eliminar(self, id_proyecto: str) -> bool:
        datos = self._documento.leer({})
        if not isinstance(datos, dict) or id_proyecto not in datos:
            return False
        del datos[id_proyecto]
        self._documento.escribir(datos, sangria=4)
        return True

    def vaciar(self) -> int:
        datos = self._documento.leer({})
        total = len(datos) if isinstance(datos, dict) else 0
        self._documento.escribir({}, sangria=4)
        return total


__all__ = [
    "SUFIJO_CRONOGRAMA",
    "JsonCronogramaRepo",
    "JsonMateriaRepo",
    "JsonPluginConfigRepo",
    "JsonProyectosRepo",
    "JsonRegistroMaterialesRepo",
]
