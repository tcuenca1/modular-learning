"""Contrato para la exportación y sincronización de notas en bóvedas (Obsidian)."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BovedaNotasPort(ABC):
    """Puerto de integración para la persistencia de resúmenes y notas en la bóveda de Obsidian."""

    @abstractmethod
    def guardar_resumen(
        self, materia: str, tema: str, contenido: str, ruta_boveda: str | None = None
    ) -> bool:
        """Guarda un resumen o guía de estudio en formato Markdown dentro de la bóveda."""

    @abstractmethod
    def guardar_nota(
        self,
        materia: str,
        subcarpeta: str,
        nombre_base: str,
        contenido: str,
        ruta_boveda: str | None = None,
    ) -> str:
        """Guarda una nota Markdown en <bóveda>/<materia>/<subcarpeta> y retorna su ruta absoluta."""

    @abstractmethod
    def actualizar_indice_materia(
        self, materia: str, tema_sanitizado: str, ruta_boveda: str | None = None
    ) -> bool:
        """Actualiza el archivo índice de la asignatura con un enlace bidireccional a la nota."""

    @abstractmethod
    def eliminar_nota(self, ruta: str, ruta_boveda: str | None = None) -> bool:
        """Borra una nota Markdown de la bóveda; solo actúa dentro de ella. False si no existía."""


__all__ = ["BovedaNotasPort"]
