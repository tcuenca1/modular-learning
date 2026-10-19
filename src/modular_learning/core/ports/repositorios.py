"""Contratos de persistencia y repositorios para el dominio académico."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CronogramaRepo(ABC):
    """Puerto de repositorio para la gestión de cronogramas y clases de asignaturas."""

    @abstractmethod
    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        """Retorna las próximas clases pendientes del cronograma de la materia."""

    @abstractmethod
    def obtener_detalle_clase(self, materia: str, tema: str) -> dict[str, Any]:
        """Obtiene la información detallada de una clase por su tema."""

    @abstractmethod
    def marcar_clase_completada(self, materia: str, tema_exacto: str) -> bool:
        """Marca una clase específica como completada en el cronograma."""

    @abstractmethod
    def obtener_cronograma(self, materia: str) -> list[dict[str, Any]] | None:
        """Retorna la lista completa de clases del cronograma de la materia."""

    @abstractmethod
    def guardar_cronograma(self, materia: str, clases: list[dict[str, Any]]) -> None:
        """Guarda o actualiza la lista completa de clases del cronograma."""


class MateriaRepo(ABC):
    """Puerto de repositorio para el catálogo de asignaturas del estudiante."""

    @abstractmethod
    def cargar_materias(self) -> list[str]:
        """Retorna el listado de materias registradas."""

    @abstractmethod
    def agregar_materia(self, nueva_materia: str) -> None:
        """Registra una nueva asignatura en el sistema."""


class RegistroMaterialesRepo(ABC):
    """Puerto de repositorio para la auditoría y control de materiales ingestados."""

    @abstractmethod
    def verificar_material_ingestado(self, nombre_archivo: str) -> bool:
        """Indica si un archivo ya ha sido procesado previamente."""

    @abstractmethod
    def registrar_material(self, nombre_archivo: str, materia: str) -> None:
        """Registra un archivo procesado con su timestamp y asignatura."""


__all__ = [
    "CronogramaRepo",
    "MateriaRepo",
    "RegistroMaterialesRepo",
]
