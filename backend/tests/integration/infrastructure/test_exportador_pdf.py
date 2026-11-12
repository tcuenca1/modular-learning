"""Tests de integración para ExportadorPdfPyMuPDF."""

from __future__ import annotations

from modular_learning.core.domain.guia_offline import ClaseGuia, GuiaOffline
from modular_learning.infrastructure.pdf.exportador_pdf import ExportadorPdfPyMuPDF


def test_exportar_guia_genera_pdf_valido():
    exportador = ExportadorPdfPyMuPDF()
    clases = [
        ClaseGuia(
            clase_id="c1",
            tema="Arquitectura Hexagonal",
            fecha="10/10/2026",
            contenido="## Objetivo\nEntender puertos y adaptadores.\n\n## Explicación\nEl núcleo no depende de frameworks.",
            respuestas="1. Separación de responsabilidades.",
        ),
        ClaseGuia(
            clase_id="c2",
            tema="Inyección de Dependencias",
            fecha="12/10/2026",
            contenido="## Explicación\nFacilita la testabilidad.",
        ),
    ]
    guia = GuiaOffline(
        id="g_test_123",
        materia="Ingeniería de Software II",
        extension="estandar",
        creada="2026-10-26T12:00:00",
        clases=clases,
    )

    pdf_bytes = exportador.exportar_guia(guia)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF-")


def test_el_pdf_dibuja_tablas_y_no_interpreta_html_de_los_titulos():
    import fitz

    guia = GuiaOffline(
        id="g2",
        materia="Redes <b>X</b>",
        extension="estandar",
        creada="2026-10-26",
        clases=[
            ClaseGuia(
                tema="A & B",
                contenido="| Capa | PDU |\n|---|---|\n| Enlace | Trama |\n\n> Nota importante",
            )
        ],
    )
    pdf = fitz.open(stream=ExportadorPdfPyMuPDF().exportar_guia(guia), filetype="pdf")
    texto = "".join(p.get_text() for p in pdf)
    assert "| Capa |" not in texto and "|---|" not in texto  # la tabla ya no sale como texto crudo
    assert "Enlace" in texto and "Trama" in texto
    assert (
        "Redes <b>X</b>" in texto and "A & B" in texto
    )  # los títulos se escapan, no se interpretan
