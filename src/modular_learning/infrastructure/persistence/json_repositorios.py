"""Implementaciones en JSON de los puertos de persistencia y repositorios."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, ClassVar

from modular_learning import settings
from modular_learning.core.ports.repositorios import (
    CronogramaRepo,
    MateriaRepo,
    RegistroMaterialesRepo,
)
from modular_learning.infrastructure.documents.lector_documentos import (
    leer_material_estudio,
    leer_prompt,
)
from modular_learning.infrastructure.obsidian.boveda_obsidian import (
    guardar_resumen_obsidian,
)


class JsonMateriaRepo(MateriaRepo):
    """Implementación de MateriaRepo basada en un archivo de texto data/config/materias.txt."""

    MATERIAS_INICIALES: ClassVar[list[str]] = [
        "Seguridad de la Informacion",
        "Ingenieria de Software II",
        "Programacion Web",
        "Internet de las Cosas",
        "Tecnologias de Conmutacion I",
    ]

    def __init__(self, ruta_archivo: str | None = None):
        self._ruta_archivo = ruta_archivo

    @property
    def ruta_archivo(self) -> str:
        return self._ruta_archivo or str(settings.ruta_materias())

    def cargar_materias(self) -> list[str]:
        archivo = self.ruta_archivo
        os.makedirs(os.path.dirname(archivo), exist_ok=True)

        if not os.path.exists(archivo):
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write("\n".join(self.MATERIAS_INICIALES))
            except Exception:
                pass
            return list(self.MATERIAS_INICIALES)

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                materias = [line.strip() for line in f if line.strip()]
            return materias if materias else list(self.MATERIAS_INICIALES)
        except Exception:
            return list(self.MATERIAS_INICIALES)

    def agregar_materia(self, nueva_materia: str) -> None:
        nueva_materia = nueva_materia.strip()
        if not nueva_materia:
            return
        materias = self.cargar_materias()
        if nueva_materia not in materias:
            materias.append(nueva_materia)
            try:
                os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
                with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                    f.write("\n".join(materias))
            except Exception as e:
                print(f"⚠️ No se pudo guardar la nueva materia en disco: {e}")


class JsonCronogramaRepo(CronogramaRepo):
    """Implementación de CronogramaRepo leyendo archivos en data/schedules/."""

    def __init__(self, carpeta_schedules: str | None = None):
        self._carpeta_schedules = carpeta_schedules

    @property
    def carpeta_schedules(self) -> str:
        return self._carpeta_schedules or str(settings.ruta_cronogramas())

    def _encontrar_ruta_cronograma(self, materia: str) -> str | None:
        carpeta = self.carpeta_schedules
        if not os.path.exists(carpeta):
            return None

        materia_slug = (
            "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
            .strip()
            .replace(" ", "_")
            .upper()
        )
        materia_upper = materia.upper().replace(" ", "_")

        posibles_nombres = [
            f"{materia}_cronograma.json",
            f"{materia_slug}_cronograma.json",
            f"{materia_upper}_cronograma.json",
            f"{materia_slug.lower()}_cronograma.json",
        ]

        for nombre in posibles_nombres:
            ruta_prueba = os.path.join(carpeta, nombre)
            if os.path.exists(ruta_prueba):
                return ruta_prueba

        try:
            for arch in os.listdir(carpeta):
                if arch.endswith("_cronograma.json") and materia_slug.replace("_", "") in arch.upper().replace("_", ""):
                    return os.path.join(carpeta, arch)
        except Exception:
            pass

        return None

    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        ruta = self._encontrar_ruta_cronograma(materia)
        if not ruta or not os.path.exists(ruta):
            return None
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                clases = data.get("clases", data.get("cronograma", []))
                return clases if isinstance(clases, list) else []
            return None
        except Exception as e:
            print(f"⚠️ Error al leer cronograma de {materia}: {e}")
            return None

    def guardar_cronograma(self, materia: str, clases: list[dict[str, Any]]) -> None:
        ruta = self._encontrar_ruta_cronograma(materia)
        if not ruta:
            materia_slug = (
                "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
                .strip()
                .replace(" ", "_")
            )
            os.makedirs(self.carpeta_schedules, exist_ok=True)
            ruta = os.path.join(self.carpeta_schedules, f"{materia_slug}_cronograma.json")

        es_dict = False
        data_orig = {}
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    data_orig = json.load(f)
                if isinstance(data_orig, dict):
                    es_dict = True
            except Exception:
                pass

        with open(ruta, "w", encoding="utf-8") as f:
            if es_dict:
                data_orig["clases"] = clases
                json.dump(data_orig, f, indent=4, ensure_ascii=False)
            else:
                json.dump(clases, f, indent=4, ensure_ascii=False)

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
        ruta = self._encontrar_ruta_cronograma(materia)
        if not ruta or not os.path.exists(ruta):
            return False

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)

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
                with open(ruta, "w", encoding="utf-8") as f:
                    if es_lista:
                        json.dump(clases, f, indent=4, ensure_ascii=False)
                    else:
                        data["clases"] = clases
                        json.dump(data, f, indent=4, ensure_ascii=False)
                return True

            return False
        except Exception as e:
            print(f"⚠️ Error al actualizar el estado de la clase en cronograma: {e}")
            return False


class JsonRegistroMaterialesRepo(RegistroMaterialesRepo):
    """Implementación de RegistroMaterialesRepo persistiendo en JSON."""

    def __init__(self, ruta_archivo: str | None = None):
        self._ruta_archivo = ruta_archivo

    @property
    def ruta_archivo(self) -> str:
        return self._ruta_archivo or str(settings.ruta_registro_materiales())

    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        if not os.path.exists(self.ruta_archivo):
            return False
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                registro = json.load(f)
            if isinstance(registro, list):
                return any(
                    item.get("nombre", "").lower() == nombre_archivo.lower() for item in registro
                )
            elif isinstance(registro, dict):
                return nombre_archivo in registro or nombre_archivo.lower() in [
                    k.lower() for k in registro
                ]
            return False
        except Exception:
            return False

    def registrar_material(self, nombre_archivo: str, materia: str) -> None:
        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)
        registro = []
        if os.path.exists(self.ruta_archivo):
            try:
                with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
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
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(registro, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ No se pudo guardar el registro de material: {e}")


# Instancias globales por defecto para compatibilidad
_materia_repo = JsonMateriaRepo()
_cronograma_repo = JsonCronogramaRepo()
_registro_repo = JsonRegistroMaterialesRepo()


# Funciones de conveniencia de módulo (compatibilidad retroactiva)
def cargar_materias(archivo_materias: str | None = None) -> list[str]:
    repo = JsonMateriaRepo(archivo_materias) if archivo_materias else _materia_repo
    return repo.cargar_materias()


def agregar_materia(nueva_materia: str, archivo_materias: str | None = None) -> None:
    repo = JsonMateriaRepo(archivo_materias) if archivo_materias else _materia_repo
    repo.agregar_materia(nueva_materia)


def obtener_proximas_clases(materia: str) -> list[dict[str, Any]]:
    return _cronograma_repo.obtener_proximas_clases(materia)


def obtener_detalle_clase(materia: str, tema: str) -> dict[str, Any]:
    return _cronograma_repo.obtener_detalle_clase(materia, tema)


def marcar_clase_completada(materia: str, tema_exacto: str) -> bool:
    return _cronograma_repo.marcar_clase_completada(materia, tema_exacto)


def verificar_material_ingestado(nombre_archivo: str) -> bool:
    return _registro_repo.verificar_material_ingestado(nombre_archivo)


def registrar_material(nombre_archivo: str, materia: str) -> None:
    _registro_repo.registrar_material(nombre_archivo, materia)


__all__ = [
    "JsonCronogramaRepo",
    "JsonMateriaRepo",
    "JsonRegistroMaterialesRepo",
    "agregar_materia",
    "cargar_materias",
    "guardar_resumen_obsidian",
    "leer_material_estudio",
    "leer_prompt",
    "marcar_clase_completada",
    "obtener_detalle_clase",
    "obtener_proximas_clases",
    "registrar_material",
    "verificar_material_ingestado",
]
