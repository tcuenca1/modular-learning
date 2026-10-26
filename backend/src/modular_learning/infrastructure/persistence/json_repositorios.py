"""Implementaciones en JSON de los puertos de persistencia y repositorios."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, ClassVar

from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)
from modular_learning.infrastructure.persistence.almacen import (
    AlmacenArchivos,
    AlmacenDocumentos,
    DocumentoJson,
    almacen_en,
    almacen_por_defecto,
)

SUFIJO_CRONOGRAMA = "_cronograma.json"


class JsonMateriaRepo(MateriaRepo):
    """Implementación de MateriaRepo basada en el documento de texto config/materias.txt."""

    MATERIAS_INICIALES: ClassVar[list[str]] = [
        "Seguridad de la Informacion",
        "Ingenieria de Software II",
        "Programacion Web",
        "Internet de las Cosas",
        "Tecnologias de Conmutacion I",
    ]

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        explicito = almacen_en(ruta_archivo)
        self._almacen, self.clave = explicito if explicito else (almacen, "config/materias.txt")

    @property
    def almacen(self) -> AlmacenDocumentos:
        return self._almacen or almacen_por_defecto()

    def _escribir(self, materias: list[str]) -> None:
        try:
            self.almacen.escribir(self.clave, "\n".join(materias))
        except Exception as e:
            print(f"⚠️ No se pudo guardar la lista de materias: {e}")

    def cargar_materias(self) -> list[str]:
        try:
            texto = self.almacen.leer(self.clave)
        except Exception:
            return list(self.MATERIAS_INICIALES)
        if texto is None:
            self._escribir(self.MATERIAS_INICIALES)
            return list(self.MATERIAS_INICIALES)
        materias = [linea.strip() for linea in texto.splitlines() if linea.strip()]
        return materias if materias else list(self.MATERIAS_INICIALES)

    def agregar_materia(self, nueva_materia: str) -> None:
        nueva_materia = nueva_materia.strip()
        if not nueva_materia:
            return
        materias = self.cargar_materias()
        if nueva_materia not in materias:
            materias.append(nueva_materia)
            self._escribir(materias)


class JsonCronogramaRepo(CronogramaRepo):
    """Implementación de CronogramaRepo con un documento `<MATERIA>_cronograma.json` por materia."""

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
            if clave.endswith(SUFIJO_CRONOGRAMA) and "/" not in clave[len(self.prefijo) :]
        ]

    @staticmethod
    def _slug(materia: str) -> str:
        return (
            "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
            .strip()
            .replace(" ", "_")
        )

    def _encontrar_clave_cronograma(self, materia: str) -> str | None:
        nombres = self._nombres()
        if not nombres:
            return None

        materia_slug = self._slug(materia).upper()
        materia_upper = materia.upper().replace(" ", "_")
        posibles_nombres = [
            f"{materia}{SUFIJO_CRONOGRAMA}",
            f"{materia_slug}{SUFIJO_CRONOGRAMA}",
            f"{materia_upper}{SUFIJO_CRONOGRAMA}",
            f"{materia_slug.lower()}{SUFIJO_CRONOGRAMA}",
        ]
        for nombre in posibles_nombres:
            if nombre in nombres:
                return self.prefijo + nombre

        buscado = materia_slug.replace("_", "")
        for nombre in nombres:
            if buscado in nombre.upper().replace("_", ""):
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
        clave = self._encontrar_clave_cronograma(materia) or (
            f"{self.prefijo}{self._slug(materia)}{SUFIJO_CRONOGRAMA}"
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
            self._escribir(clave, clases)
        return clave

    def listar_cronogramas(self) -> dict[str, list[dict[str, Any]]]:
        cronogramas: dict[str, list[dict[str, Any]]] = {}
        for nombre in sorted(self._nombres()):
            materia = nombre.removesuffix(SUFIJO_CRONOGRAMA).replace("_", " ")
            try:
                data = self._leer(self.prefijo + nombre)
            except Exception:
                continue
            clases = (
                data.get("clases", data.get("cronograma", [])) if isinstance(data, dict) else data
            )
            if isinstance(clases, list):
                cronogramas[materia] = clases
        return cronogramas

    def agregar_material_transversal(self, materia: str, item: dict[str, Any]) -> None:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return
        data = self._leer(clave)
        if isinstance(data, list):
            data = {"clases": data}
        data.setdefault("material_transversal", []).append(item)
        self._escribir(clave, data)

    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        clases = self.obtener_cronograma(materia)
        if not clases:
            return []

        pendientes = [c for c in clases if c.get("estado", "").lower() == "pendiente"]
        for c in pendientes:
            if "subtemas_adicionales" not in c:
                c["subtemas_adicionales"] = []
            if "materiales_asociados" not in c:
                c["materiales_asociados"] = []
        return pendientes[:5]

    def obtener_detalle_clase(self, materia: str, tema: str) -> dict[str, Any]:
        clases = self.obtener_cronograma(materia)
        if not clases:
            return {"subtemas_adicionales": [], "materiales_asociados": []}

        tema_buscado = tema.strip().lower()
        for clase in clases:
            tema_clase = clase.get("tema", "").strip().lower()
            if (
                tema_buscado in tema_clase
                or tema_clase in tema_buscado
                or tema_buscado == tema_clase
            ):
                if "subtemas_adicionales" not in clase:
                    clase["subtemas_adicionales"] = []
                if "materiales_asociados" not in clase:
                    clase["materiales_asociados"] = []
                return clase

        return {"subtemas_adicionales": [], "materiales_asociados": []}

    def marcar_clase_completada(self, materia: str, tema_exacto: str) -> bool:
        clave = self._encontrar_clave_cronograma(materia)
        if not clave:
            return False

        try:
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

            actualizado = False
            tema_buscado = tema_exacto.strip().lower()

            for clase in clases:
                tema_clase = clase.get("tema", "").strip().lower()
                if (
                    tema_buscado in tema_clase
                    or tema_clase in tema_buscado
                    or tema_buscado == tema_clase
                ):
                    clase["estado"] = "completado"
                    actualizado = True

            if actualizado:
                if es_lista:
                    self._escribir(clave, clases)
                else:
                    data["clases"] = clases
                    self._escribir(clave, data)
                return True

            return False
        except Exception as e:
            print(f"⚠️ Error al actualizar el estado de la clase en cronograma: {e}")
            return False


class JsonRegistroMaterialesRepo(RegistroMaterialesRepo):
    """Implementación de RegistroMaterialesRepo persistiendo en config/registro_materiales.json."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("config/registro_materiales.json", ruta_archivo, almacen)

    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        try:
            registro = self._documento.leer(None)
        except Exception:
            return False
        if isinstance(registro, list):
            return any(
                item.get("nombre", "").lower() == nombre_archivo.lower() for item in registro
            )
        if isinstance(registro, dict):
            return nombre_archivo in registro or nombre_archivo.lower() in [
                k.lower() for k in registro
            ]
        return False

    def registrar_material(self, nombre_archivo: str, materia: str) -> None:
        registro: list[dict[str, Any]] = []
        try:
            contenido = self._documento.leer(None)
            if isinstance(contenido, list):
                registro = contenido
            elif isinstance(contenido, dict):
                registro = [
                    {
                        "nombre": k,
                        "materia": v.get("materia", ""),
                        "fecha": v.get("fecha", ""),
                    }
                    for k, v in contenido.items()
                ]
        except Exception:
            registro = []

        nombre_lower = nombre_archivo.lower()
        registro = [r for r in registro if r.get("nombre", "").lower() != nombre_lower]

        registro.append(
            {
                "nombre": nombre_archivo,
                "materia": materia,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        try:
            self._documento.escribir(registro, sangria=4)
        except Exception as e:
            print(f"⚠️ No se pudo guardar el registro de material: {e}")


__all__ = [
    "JsonCronogramaRepo",
    "JsonMateriaRepo",
    "JsonRegistroMaterialesRepo",
]
