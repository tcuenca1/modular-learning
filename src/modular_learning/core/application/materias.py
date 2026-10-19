"""Servicio de aplicación para la gestión de asignaturas académicas."""

from __future__ import annotations

from typing import Any

from modular_learning.core.ports.repositorios import CronogramaRepo, MateriaRepo


class MateriasService:
    """Caso de uso y operaciones para catálogo de asignaturas."""

    def __init__(
        self,
        materia_repo: MateriaRepo,
        cronograma_repo: CronogramaRepo | None = None,
    ):
        self.materia_repo = materia_repo
        self.cronograma_repo = cronograma_repo

    def listar_materias(self) -> list[str]:
        """Retorna la lista de todas las materias registradas."""
        return self.materia_repo.cargar_materias()

    def agregar_materia(self, nueva_materia: str) -> list[str]:
        """Añade una asignatura al catálogo y retorna la lista actualizada."""
        self.materia_repo.agregar_materia(nueva_materia)
        return self.materia_repo.cargar_materias()

    def obtener_proximas_clases(self, materia: str) -> list[dict[str, Any]]:
        """Retorna las clases pendientes del cronograma de la asignatura."""
        if not self.cronograma_repo:
            return []
        return self.cronograma_repo.obtener_proximas_clases(materia)


__all__ = ["MateriasService"]
