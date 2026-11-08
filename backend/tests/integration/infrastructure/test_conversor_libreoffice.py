"""Tests de integración para el adaptador LibreOffice y el plan B con python-pptx."""

from __future__ import annotations

import os
import subprocess

import pytest
from pptx import Presentation

from modular_learning.infrastructure.documents.conversor_libreoffice import (
    ConversorLibreOffice,
    buscar_ejecutable_soffice,
)
from modular_learning.infrastructure.documents.lector_documentos import LectorDocumentosLocal


def test_conversor_libreoffice_salta_si_no_instalado():
    ejecutable = buscar_ejecutable_soffice()
    if not ejecutable:
        pytest.skip("LibreOffice (soffice) no está instalado en este sistema.")

    conversor = ConversorLibreOffice(ruta_soffice=ejecutable)
    assert conversor.ruta_soffice is not None


def test_plan_b_extraccion_pptx_con_python_pptx(tmp_path):
    # Crear presentación de prueba con python-pptx
    prs = Presentation()
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = "Arquitectura de Software"
    slide.placeholders[1].text = "Patrones y Componentes"

    # Segunda diapositiva con tabla y notas del orador
    slide2 = prs.slides.add_slide(prs.slide_layouts[5])
    slide2.shapes.title.text = "Resumen de Métricas"
    rows, cols = 2, 2
    left, top, width, height = 100, 100, 200, 200
    table_shape = slide2.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.cell(0, 0).text = "Metrica"
    table.cell(0, 1).text = "Valor"
    table.cell(1, 0).text = "Cobertura"
    table.cell(1, 1).text = "95%"

    notes_slide = slide2.notes_slide
    notes_slide.notes_text_frame.text = "Enfatizar la cobertura de pruebas"

    ruta_pptx = tmp_path / "clase.pptx"
    prs.save(str(ruta_pptx))

    # Probar extracción con LectorDocumentosLocal (Plan B)
    lector = LectorDocumentosLocal()
    texto = lector.extraer_texto(str(ruta_pptx))

    assert "Arquitectura de Software" in texto
    assert "Patrones y Componentes" in texto
    assert "Resumen de Métricas" in texto
    assert "Cobertura" in texto
    assert "95%" in texto
    assert "Enfatizar la cobertura de pruebas" in texto


def test_conversor_libreoffice_comando_incluye_user_installation(monkeypatch, tmp_path):
    archivo_prueba = tmp_path / "presentacion.pptx"
    archivo_prueba.write_text("dummy", encoding="utf-8")

    comandos_ejecutados = []

    def fake_run(cmd, **kwargs):
        comandos_ejecutados.append(cmd)

        class DummyResult:
            returncode = 0
            stderr = ""

        outdir = cmd[cmd.index("--outdir") + 1]
        pdf_falso = os.path.join(outdir, "presentacion.pdf")
        with open(pdf_falso, "w", encoding="utf-8") as f:
            f.write("dummy pdf")
        return DummyResult()

    monkeypatch.setattr(subprocess, "run", fake_run)

    conversor = ConversorLibreOffice(ruta_soffice="soffice_falso")
    ruta_pdf = conversor.convertir_a_pdf(str(archivo_prueba))

    assert ruta_pdf is not None
    assert len(comandos_ejecutados) == 1
    cmd = comandos_ejecutados[0]
    arg_env = [arg for arg in cmd if arg.startswith("-env:UserInstallation=")]
    assert len(arg_env) == 1
    assert "file:///" in arg_env[0]
    assert "perfil" in arg_env[0]

    conversor.borrar_temporal(ruta_pdf)
