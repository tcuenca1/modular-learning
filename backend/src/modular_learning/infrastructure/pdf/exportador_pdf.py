"""Adaptador de infraestructura para exportación de guías en formato PDF usando PyMuPDF."""

from __future__ import annotations

import html
import tempfile
from pathlib import Path

import fitz
import markdown_it

from modular_learning.core.domain.guia_offline import GuiaOffline
from modular_learning.core.ports.guias import ExportadorPdfPort


class ExportadorPdfPyMuPDF(ExportadorPdfPort):
    """Genera documentos PDF en formato A5 a partir de una GuiaOffline."""

    def __init__(self) -> None:
        self._md = markdown_it.MarkdownIt().enable("table")

    def exportar_guia(self, guia: GuiaOffline) -> bytes:
        page_rect = fitz.Rect(0, 0, 420, 595)  # A5 (148 x 210 mm)
        content_rect = fitz.Rect(35, 35, 385, 560)

        html_partes = [
            """
            <style>
              body { font-family: sans-serif; font-size: 9.5pt; line-height: 1.45; color: #1e293b; }
              h1 { font-size: 16pt; color: #0f172a; margin-top: 24px; margin-bottom: 8px; font-weight: bold; }
              h2 { font-size: 12pt; color: #1e1b4b; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; margin-top: 14px; margin-bottom: 6px; font-weight: bold; }
              h3 { font-size: 10pt; color: #334155; margin-top: 10px; margin-bottom: 4px; font-weight: bold; }
              p { margin: 5px 0; }
              ul, ol { margin: 5px 0; padding-left: 18px; }
              li { margin-bottom: 3px; }
              table { border-collapse: collapse; margin: 6px 0; }
              th { background-color: #e2e8f0; font-weight: bold; text-align: left; }
              th, td { border: 1px solid #cbd5e1; padding: 3px 6px; font-size: 8.5pt; }
              blockquote { margin: 6px 0 6px 6px; padding-left: 8px; border-left: 3px solid #fcd34d; color: #475569; }
              pre { background-color: #f1f5f9; padding: 5px; }
              code { font-family: monospace; font-size: 8.5pt; background-color: #f1f5f9; padding: 1px 3px; }
              .portada { text-align: center; margin-top: 80px; margin-bottom: 40px; }
              .cifra { font-size: 8pt; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
              .subtitulo { font-size: 10pt; color: #64748b; margin-top: 6px; }
              .indice { margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; }
              .salto-pagina { page-break-before: always; }
              .bloque-clase { margin-top: 10px; }
              .fecha-clase { font-size: 8.5pt; color: #64748b; margin-bottom: 4px; }
            </style>
            """,
            f"""
            <div class="portada">
              <p class="cifra">Modular Learning · Guía de Estudio Offline</p>
              <h1>{html.escape(guia.materia)}</h1>
              <p class="subtitulo">{len(guia.clases)} clases · Versión {guia.extension.capitalize()}</p>
            </div>
            <div class="indice">
              <h2>Índice de Clases</h2>
              <ol>
            """,
        ]

        for c in guia.clases:
            fecha_str = f" ({c.fecha})" if c.fecha else ""
            html_partes.append(
                f"<li><strong>{html.escape(c.tema)}</strong>{html.escape(fecha_str)}</li>"
            )

        html_partes.append('</ol></div><div class="salto-pagina"></div>')

        for idx, c in enumerate(guia.clases, start=1):
            fecha_str = f" · {c.fecha}" if c.fecha else ""
            html_partes.append(f"""
            <div class="bloque-clase">
              <p class="fecha-clase">CLASE {idx}{fecha_str}</p>
              <h1>{html.escape(c.tema)}</h1>
              {self._md.render(c.contenido or "*(Contenido en desarrollo)*")}
            </div>
            """)
            if idx < len(guia.clases) or any(cl.respuestas for cl in guia.clases):
                html_partes.append('<div class="salto-pagina"></div>')

        # Respuestas de autoevaluación al final si existen
        clases_con_respuestas = [c for c in guia.clases if c.respuestas]
        if clases_con_respuestas:
            html_partes.append("""
            <div class="bloque-clase">
              <h1>Respuestas de Autoevaluación</h1>
              <p class="cifra">Comprueba tus respuestas una vez realizados los ejercicios</p>
            """)
            for c in clases_con_respuestas:
                html_partes.append(f"""
                <h2>{html.escape(c.tema)}</h2>
                {self._md.render(c.respuestas)}
                """)
            html_partes.append("</div>")

        html_final = "".join(html_partes)

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            writer = fitz.DocumentWriter(str(tmp_path))
            story = fitz.Story(html=html_final)
            while True:
                device = writer.begin_page(page_rect)
                more, _ = story.place(content_rect)
                story.draw(device)
                writer.end_page()
                if not more:
                    break
            writer.close()
            del writer
            return tmp_path.read_bytes()
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


__all__ = ["ExportadorPdfPyMuPDF"]
