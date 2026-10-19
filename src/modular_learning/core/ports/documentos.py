"""Contrato para la lectura y extracción de plantillas de prompts y documentos de estudio."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LectorDocumentosPort(ABC):
    """Puerto para leer archivos de prompts y contenido de documentos Markdown / texto."""

    @abstractmethod
    def leer_prompt(self, nombre_archivo: str) -> str:
        """Lee una plantilla de prompt empaquetada o configurada por nombre de archivo."""

    @abstractmethod
    def leer_material_estudio(self, ruta_archivo: str) -> str:
        """Lee el contenido de texto de un archivo de estudio local."""


__all__ = ["LectorDocumentosPort"]
