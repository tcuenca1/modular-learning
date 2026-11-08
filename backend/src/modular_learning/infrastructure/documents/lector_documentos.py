"""Adaptador para lectura de plantillas de prompts y documentos de estudio."""

from __future__ import annotations

import os

from modular_learning import settings
from modular_learning.core.ports.documentos import LectorDocumentosPort


class LectorDocumentosLocal(LectorDocumentosPort):
    """Implementación local de lectura de archivos, plantillas y extracción de texto."""

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

    def extraer_texto(self, ruta_archivo: str) -> str:
        """Extrae texto plano de PDF (pypdf), DOCX (python-docx) o archivos de texto."""
        ext = os.path.splitext(ruta_archivo)[1].lower()
        if ext == ".pdf":
            from pypdf import PdfReader

            try:
                reader = PdfReader(ruta_archivo)
                return "\n".join(t for t in (p.extract_text() for p in reader.pages) if t)
            except Exception as e:
                raise RuntimeError(f"No se pudo extraer texto del PDF con pypdf: {e}") from e
        if ext == ".docx":
            import docx

            documento = docx.Document(ruta_archivo)
            return "\n".join(p.text for p in documento.paragraphs)
        if ext == ".pptx":
            from pptx import Presentation

            try:
                prs = Presentation(ruta_archivo)
                bloques: list[str] = []
                for i, slide in enumerate(prs.slides, start=1):
                    partes: list[str] = [f"--- Diapositiva {i} ---"]
                    for shape in slide.shapes:
                        if shape.has_text_frame:
                            for paragraph in shape.text_frame.paragraphs:
                                t = paragraph.text.strip()
                                if t:
                                    partes.append(t)
                        if shape.has_table:
                            for row in shape.table.rows:
                                celdas = [
                                    cell.text.strip() for cell in row.cells if cell.text.strip()
                                ]
                                if celdas:
                                    partes.append(" | ".join(celdas))
                    if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                        notas = slide.notes_slide.notes_text_frame.text.strip()
                        if notas:
                            partes.append(f"[Notas del orador: {notas}]")
                    bloques.append("\n".join(partes))
                return "\n\n".join(bloques)
            except Exception as e:
                raise RuntimeError(f"No se pudo extraer texto del PPTX con python-pptx: {e}") from e
        try:
            with open(ruta_archivo, encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(ruta_archivo, encoding="latin-1") as f:
                return f.read()

    def listar_archivos(self, carpeta: str, recursivo: bool = True) -> list[str] | None:
        """Lista archivos de la carpeta (ordenados por nombre dentro de cada directorio)."""
        if not os.path.isdir(carpeta):
            return None
        if not recursivo:
            return [
                os.path.join(carpeta, f)
                for f in sorted(os.listdir(carpeta))
                if os.path.isfile(os.path.join(carpeta, f))
            ]
        return [
            os.path.join(raiz, nombre)
            for raiz, _, archivos in os.walk(carpeta)
            for nombre in sorted(archivos)
        ]


__all__ = ["LectorDocumentosLocal"]
