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
    agregar_materia,
    cargar_materias,
    guardar_resumen_obsidian,
    leer_material_estudio,
    leer_prompt,
    marcar_clase_completada,
    obtener_detalle_clase,
    obtener_proximas_clases,
    registrar_material,
    verificar_material_ingestado,
)

__all__ = [
    "DEFAULT_CARPETA_MATERIAL",
    "DEFAULT_OBSIDIAN",
    "JsonAjustesRepo",
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
