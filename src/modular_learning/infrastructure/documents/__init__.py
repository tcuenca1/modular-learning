"""Adaptadores para la lectura y gestión de documentos y prompts."""

from modular_learning.infrastructure.documents.lector_documentos import (
    LectorDocumentosLocal,
    leer_material_estudio,
    leer_prompt,
)

__all__ = [
    "LectorDocumentosLocal",
    "leer_material_estudio",
    "leer_prompt",
]
