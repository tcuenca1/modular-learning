"""Servicio de aplicación para configuración de usuario."""

from __future__ import annotations

from typing import Any

from modular_learning.core.ports.config import AjustesPort


class ConfiguracionService:
    """Caso de uso para la administración y validación de rutas de estudio y bóvedas."""

    def __init__(self, ajustes_repo: AjustesPort):
        self.ajustes_repo = ajustes_repo

    def esta_configurado(self) -> bool:
        return self.ajustes_repo.esta_configurado()

    def carpeta_material(self) -> str:
        return self.ajustes_repo.carpeta_material()

    def ruta_boveda(self) -> str:
        return self.ajustes_repo.ruta_boveda()

    def obtener_ajustes(self) -> dict[str, Any]:
        return self.ajustes_repo.obtener_ajustes()

    def guardar_ajustes(
        self, carpeta_material_nueva: str, ruta_obsidian_nueva: str
    ) -> dict[str, Any]:
        return self.ajustes_repo.guardar_ajustes(carpeta_material_nueva, ruta_obsidian_nueva)


__all__ = ["ConfiguracionService"]
