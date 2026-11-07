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
