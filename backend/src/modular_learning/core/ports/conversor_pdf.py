"""Contrato para la conversión de documentos (como presentaciones .pptx) a PDF."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ConversorPdfPort(ABC):
    """Puerto para convertir documentos a PDF temporal para análisis multimodal."""

    @abstractmethod
    def convertir_a_pdf(self, ruta_archivo: str) -> str | None:
        """Convierte el archivo a PDF en una ruta temporal, o retorna None si no se puede."""

    @abstractmethod
    def borrar_temporal(self, ruta_pdf: str) -> None:
        """Elimina el archivo PDF temporal generado."""


__all__ = ["ConversorPdfPort"]
