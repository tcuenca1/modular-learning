"""Adaptador para lectura de plantillas de prompts y documentos de estudio."""

from __future__ import annotations

import os

from modular_learning import settings
from modular_learning.core.ports.documentos import LectorDocumentosPort


class LectorDocumentosLocal(LectorDocumentosPort):
    """Implementación local de lectura de archivos y plantillas Markdown."""

    def leer_prompt(self, nombre_archivo: str) -> str:
        """Lee un archivo de instrucciones desde el paquete de prompts."""
        ruta_completa = settings.ruta_prompt(nombre_archivo)
        try:
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                return archivo.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"El archivo de prompt '{nombre_archivo}' no se encontró en {ruta_completa}."
            )
        except Exception as e:
            raise OSError(f"Error al leer el prompt '{nombre_archivo}': {e}")

    def leer_material_estudio(self, ruta_archivo: str) -> str:
        """Lee el contenido de un archivo de material de estudio en formato Markdown (.md)."""
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(
                f"El archivo de material de estudio no existe en la ruta: {ruta_archivo}"
            )

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return archivo.read()
        except Exception as e:
            raise OSError(f"Error al leer el material de estudio en '{ruta_archivo}': {e}")


def leer_prompt(nombre_archivo: str) -> str:
    """Función de conveniencia para leer un prompt."""
    return LectorDocumentosLocal().leer_prompt(nombre_archivo)


def leer_material_estudio(ruta_archivo: str) -> str:
    """Función de conveniencia para leer material de estudio."""
    return LectorDocumentosLocal().leer_material_estudio(ruta_archivo)


__all__ = [
    "LectorDocumentosLocal",
    "leer_material_estudio",
    "leer_prompt",
]
