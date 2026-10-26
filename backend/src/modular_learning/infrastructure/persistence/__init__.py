"""Adaptadores de persistencia en disco y JSON."""

from modular_learning.infrastructure.persistence.json_ajustes import (
    DEFAULT_CARPETA_MATERIAL,
    DEFAULT_OBSIDIAN,
    JsonAjustesRepo,
)
from modular_learning.infrastructure.persistence.json_repositorios import (
    JsonCronogramaRepo,
    JsonMateriaRepo,
    JsonRegistroMaterialesRepo,
)

__all__ = [
    "DEFAULT_CARPETA_MATERIAL",
    "DEFAULT_OBSIDIAN",
    "JsonAjustesRepo",
    "JsonCronogramaRepo",
    "JsonMateriaRepo",
    "JsonRegistroMaterialesRepo",
]
