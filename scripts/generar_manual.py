"""Genera docs/manual/MANUAL_FUNCIONAL.pdf a partir de docs/manual/MANUAL_FUNCIONAL.md.

Usa markdown-it-py (con soporte de tablas habilitado) y fitz.Story (PyMuPDF),
siguiendo el mismo patrón de infrastructure/pdf/exportador_pdf.py.

Uso:
    venv/Scripts/python.exe scripts/generar_manual.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import fitz
from markdown_it import MarkdownIt

RAIZ = Path(__file__).resolve().parent.parent
RUTA_MD = RAIZ / "docs" / "manual" / "MANUAL_FUNCIONAL.md"
RUTA_PDF = RAIZ / "docs" / "manual" / "MANUAL_FUNCIONAL.pdf"

# Tamaño A4 en puntos tipográficos (1 pt = 1/72 in): 595 x 842 pt
_ANCHO_A4 = 595
_ALTO_A4 = 842
_MARGEN = 28

_CSS = """
body {
    font-family: sans-serif;
    font-size: 8.5pt;
    line-height: 1.38;
    color: #18181b;
}
h1 {
    font-size: 16pt;
    margin-top: 0;
    margin-bottom: 8pt;
    color: #09090b;
}
h2 {
    font-size: 12.5pt;
    margin-top: 14pt;
    margin-bottom: 6pt;
    border-bottom: 1pt solid #d4d4d8;
    padding-bottom: 3pt;
    color: #18181b;
}
h3 {
    font-size: 10.5pt;
    margin-top: 10pt;
    margin-bottom: 4pt;
    color: #27272a;
}
h4 {
    font-size: 9.5pt;
    margin-top: 8pt;
    margin-bottom: 3pt;
    color: #27272a;
}
p {
    margin-top: 0;
    margin-bottom: 5pt;
}
ul, ol {
    margin-top: 2pt;
    margin-bottom: 6pt;
    padding-left: 14pt;
}
li {
    margin-bottom: 2.5pt;
}
code {
    font-family: monospace;
    font-size: 7.5pt;
    background-color: #f4f4f5;
    padding: 1pt 2pt;
}
pre {
    font-family: monospace;
    font-size: 7.5pt;
    background-color: #f4f4f5;
    padding: 6pt;
    margin-bottom: 6pt;
    white-space: pre-wrap;
}
hr {
    border: none;
    border-top: 0.5pt solid #d4d4d8;
    margin-top: 10pt;
    margin-bottom: 10pt;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 6pt;
    margin-bottom: 10pt;
    font-size: 7pt;
}
th {
    background-color: #f4f4f5;
    border: 0.5pt solid #a1a1aa;
    padding: 3pt;
    text-align: left;
    font-weight: bold;
}
td {
    border: 0.5pt solid #d4d4d8;
    padding: 3pt;
    vertical-align: top;
}
"""


def _permitir_cortes_en_tablas(html: str) -> str:
    """Inserta puntos de corte invisibles tras '/', '_' y '.' dentro de tablas para evitar recortes."""

    def _procesar_bloque_tabla(match: re.Match[str]) -> str:
        bloque = match.group(0)
        partes = re.split(r"(<[^>]+>)", bloque)
        for i in range(0, len(partes), 2):
            partes[i] = re.sub(r"([/_.])", r"\1&#8203;", partes[i])
        return "".join(partes)

    return re.sub(r"<table>.*?</table>", _procesar_bloque_tabla, html, flags=re.DOTALL)


def construir_html(markdown_texto: str) -> str:
    """Convierte el documento Markdown a un documento HTML completo con tablas."""
    md = MarkdownIt("commonmark").enable("table")
    cuerpo = _permitir_cortes_en_tablas(md.render(markdown_texto))
    return f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{cuerpo}</body></html>"


def renderizar_pdf(html: str) -> bytes:
    """Maqueta el HTML en páginas A4 usando fitz.Story y fitz.DocumentWriter."""
    historia = fitz.Story(html=html, user_css=_CSS)
    mediabox = fitz.Rect(0, 0, _ANCHO_A4, _ALTO_A4)
    area_util = fitz.Rect(
        _MARGEN,
        _MARGEN,
        _ANCHO_A4 - _MARGEN,
        _ALTO_A4 - _MARGEN,
    )

    buffer = io.BytesIO()
    escritor = fitz.DocumentWriter(buffer)
    mas = 1
    while mas:
        dispositivo = escritor.begin_page(mediabox)
        mas, _ = historia.place(area_util)
        historia.draw(dispositivo)
        escritor.end_page()
    escritor.close()
    return buffer.getvalue()


def main() -> int:
    if not RUTA_MD.exists():
        raise FileNotFoundError(f"No se encontró el archivo fuente: {RUTA_MD}")

    texto_md = RUTA_MD.read_text(encoding="utf-8")
    html = construir_html(texto_md)
    pdf_bytes = renderizar_pdf(html)

    RUTA_PDF.parent.mkdir(parents=True, exist_ok=True)
    RUTA_PDF.write_bytes(pdf_bytes)

    with fitz.open(RUTA_PDF) as doc:
        num_paginas = len(doc)
        texto_extraido = "".join(pagina.get_text() for pagina in doc)

    print(
        f"PDF generado correctamente en {RUTA_PDF} "
        f"({num_paginas} paginas, {len(pdf_bytes)} bytes, "
        f"{len(texto_extraido)} caracteres extraibles)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
