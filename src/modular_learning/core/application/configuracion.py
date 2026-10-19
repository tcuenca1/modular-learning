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


# Instancia por defecto para compatibilidad si se inyecta o enlaza en runtime
_instancia_por_defecto: ConfiguracionService | None = None


def configurar_servicio_defecto(servicio: ConfiguracionService) -> None:
    global _instancia_por_defecto
    _instancia_por_defecto = servicio


def _obtener_servicio() -> ConfiguracionService:
    if _instancia_por_defecto is None:
        raise RuntimeError(
            "ConfiguracionService no ha sido inicializado. "
            "Usa Container de modular_learning.bootstrap o llama a configurar_servicio_defecto()."
        )
    return _instancia_por_defecto


# Funciones de conveniencia que delegan al servicio
def esta_configurado() -> bool:
    return _obtener_servicio().esta_configurado()


def carpeta_material() -> str:
    return _obtener_servicio().carpeta_material()


def ruta_boveda() -> str:
    return _obtener_servicio().ruta_boveda()


def obtener_ajustes() -> dict[str, Any]:
    return _obtener_servicio().obtener_ajustes()


def guardar_ajustes(carpeta_material_nueva: str, ruta_obsidian_nueva: str) -> dict[str, Any]:
    return _obtener_servicio().guardar_ajustes(carpeta_material_nueva, ruta_obsidian_nueva)


_orig_carpeta_material = carpeta_material

__all__ = [
    "ConfiguracionService",
    "_orig_carpeta_material",
    "carpeta_material",
    "configurar_servicio_defecto",
    "esta_configurado",
    "guardar_ajustes",
    "obtener_ajustes",
    "ruta_boveda",
]
