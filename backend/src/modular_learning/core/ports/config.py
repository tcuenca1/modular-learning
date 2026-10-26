"""Contrato para la gestión y persistencia de ajustes de usuario del sistema."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AjustesPort(ABC):
    """Puerto para la lectura y guardado de ajustes de configuración del usuario."""

    @abstractmethod
    def esta_configurado(self) -> bool:
        """Indica si el sistema tiene las rutas esenciales configuradas."""

    @abstractmethod
    def carpeta_material(self) -> str:
        """Retorna la ruta al directorio raíz con el material académico."""

    @abstractmethod
    def ruta_boveda(self) -> str:
        """Retorna la ruta a la bóveda principal de Obsidian."""

    @abstractmethod
    def obtener_ajustes(self) -> dict[str, Any]:
        """Retorna el estado de configuración y existencia de directorios."""

    @abstractmethod
    def guardar_ajustes(
        self, carpeta_material_nueva: str, ruta_obsidian_nueva: str
    ) -> dict[str, Any]:
        """Valida y persiste las nuevas rutas de configuración del usuario."""


__all__ = ["AjustesPort"]
