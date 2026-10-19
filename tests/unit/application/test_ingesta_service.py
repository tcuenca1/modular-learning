"""Tests unitarios para IngestaService usando FakeLLM y adaptadores en memoria."""

from __future__ import annotations

import os

import pytest

from modular_learning.core.application.ingesta import IngestaService
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryAjustesPort,
    InMemoryBovedaPort,
    InMemoryCronogramaRepo,
    InMemoryLectorDocumentosPort,
    InMemoryRegistroMaterialesRepo,
)


@pytest.fixture
def ingesta_env(tmp_path):
    boveda_dir = tmp_path / "boveda"
    boveda_dir.mkdir()
    material_dir = tmp_path / "material"
    material_dir.mkdir()

    fake_llm = FakeLLM(
        texto_default="# Notas del Material\n\nResumen estructurado en Markdown.",
        json_default={"clase_asignada": 1, "peso_afinidad": 95, "subtemas_a_incorporar": ["Subtema A"]},
    )
    registro_repo = InMemoryRegistroMaterialesRepo()
    boveda_port = InMemoryBovedaPort()
    lector_docs = InMemoryLectorDocumentosPort()
    ajustes_port = InMemoryAjustesPort(carpeta_mat=str(material_dir), ruta_bov=str(boveda_dir))
    cronograma_repo = InMemoryCronogramaRepo()

    service = IngestaService(
        llm=fake_llm,
        registro_repo=registro_repo,
        boveda_port=boveda_port,
        lector_docs=lector_docs,
        ajustes_port=ajustes_port,
        cronograma_repo=cronograma_repo,
    )

    return {
        "service": service,
        "llm": fake_llm,
        "registro": registro_repo,
        "boveda_dir": boveda_dir,
        "material_dir": material_dir,
    }


def test_clasificar_tipo_material(ingesta_env):
    service = ingesta_env["service"]
    raiz = "C:/Universidad/Redes"

    t1 = service.clasificar_tipo_material("C:/Universidad/Redes/Lab1.pdf", raiz)
    assert t1 == "actividad"

    t2 = service.clasificar_tipo_material("C:/Universidad/Redes/Material de Estudio/Semana1.pdf", raiz)
    assert t2 == "diapositiva"

    t3 = service.clasificar_tipo_material("C:/Universidad/Redes/Material Adicional/Articulo.pdf", raiz)
    assert t3 == "lectura"


def test_ingestar_archivo_txt(ingesta_env, tmp_path):
    service = ingesta_env["service"]
    registro = ingesta_env["registro"]

    archivo_fuente = tmp_path / "Guia_Comandos.txt"
    archivo_fuente.write_text("Comandos Cisco Packet Tracer: enable, configure terminal", encoding="utf-8")

    resultado = service.ingestar_archivo(
        ruta_archivo=str(archivo_fuente),
        nombre_original="Guia_Comandos.txt",
        materia="Redes",
        tipo="actividad",
    )

    assert resultado["archivo"] == "Guia_Comandos.txt"
    assert resultado["materia"] == "Redes"
    assert resultado["tipo"] == "actividad"
    assert os.path.exists(resultado["ruta_salida"])
    assert registro.verificar_material_ingestado("Guia_Comandos.txt")


def test_escanear_materia(ingesta_env):
    service = ingesta_env["service"]
    material_dir = ingesta_env["material_dir"]
    registro = ingesta_env["registro"]

    # Crear carpeta de materia y archivos
    materia_folder = material_dir / "Redes"
    materia_folder.mkdir()
    (materia_folder / "lab1.pdf").write_text("dummy", encoding="utf-8")
    (materia_folder / "lab2.docx").write_text("dummy", encoding="utf-8")
    (materia_folder / "presentacion.pptx").write_text("dummy", encoding="utf-8")

    # Marcar lab1 como ya procesado
    registro.registrar_material("lab1.pdf", "Redes")

    escaneo = service.escanear_materia("Redes")
    assert escaneo["existe"] is True
    assert escaneo["total"] == 2  # lab1.pdf y lab2.docx
    assert escaneo["omitidos"] == 1  # lab1.pdf
    assert escaneo["no_soportados"] == 1  # presentacion.pptx
    assert len(escaneo["pendientes"]) == 1
    assert escaneo["pendientes"][0]["nombre"] == "lab2.docx"
