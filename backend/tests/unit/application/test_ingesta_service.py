"""Tests unitarios para el servicio de ingesta de material de estudio."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from modular_learning.core.application.ingesta import IngestaService
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryAjustesPort,
    InMemoryBovedaPort,
    InMemoryCronogramaRepo,
    InMemoryLectorDocumentosPort,
    InMemoryMateriaRepo,
    InMemoryRegistroMaterialesRepo,
)


@pytest.fixture
def mock_plugins_service():
    service = MagicMock()
    service.obtener_plugin.return_value = None
    return service


def test_clasificar_tipo_material():
    service = IngestaService(
        llm=FakeLLM(),
        registro_repo=InMemoryRegistroMaterialesRepo(),
        boveda_port=InMemoryBovedaPort(),
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
    )

    raiz = "/data/material/Redes"

    assert service.clasificar_tipo_material("/data/material/Redes/Tarea1.pdf", raiz) == "actividad"
    assert (
        service.clasificar_tipo_material(
            "/data/material/Redes/Material de Estudio/Semana1.pdf", raiz
        )
        == "diapositiva"
    )
    assert (
        service.clasificar_tipo_material("/data/material/Redes/Material Adicional/RFC.pdf", raiz)
        == "lectura"
    )
    assert (
        service.clasificar_tipo_material("/data/material/Redes/Otros/info.pdf", raiz)
        == "material_complementario"
    )


def test_ingestar_archivo_txt(mock_plugins_service):
    lector_docs = InMemoryLectorDocumentosPort()
    lector_docs.materiales["/tmp/apuntes.txt"] = "Conceptos de redes y sockets."

    registro_repo = InMemoryRegistroMaterialesRepo()
    boveda_port = InMemoryBovedaPort()
    ajustes_port = InMemoryAjustesPort()
    cronograma_repo = InMemoryCronogramaRepo(
        {"Redes": [{"tema": "Sockets", "estado": "pendiente"}]}
    )

    service = IngestaService(
        llm=FakeLLM(texto_default="# Resumen de Apuntes"),
        registro_repo=registro_repo,
        boveda_port=boveda_port,
        lector_docs=lector_docs,
        ajustes_port=ajustes_port,
        plugins_service=mock_plugins_service,
        cronograma_repo=cronograma_repo,
    )

    resultado = service.ingestar_archivo(
        ruta_archivo="/tmp/apuntes.txt",
        nombre_original="apuntes.txt",
        materia="Redes",
        tipo="lectura",
    )

    assert resultado["archivo"] == "apuntes.txt"
    assert resultado["materia"] == "Redes"
    assert resultado["contenido_md"] == "# Resumen de Apuntes"
    assert registro_repo.verificar_material_ingestado("apuntes.txt") is True
    assert len(boveda_port.notas) == 1


def test_escanear_materia():
    lector_docs = InMemoryLectorDocumentosPort()
    lector_docs.materiales = {
        "/material/Redes/lab1.pdf": "...",
        "/material/Redes/lab2.docx": "...",
        "/material/Redes/presentacion.pptx": "...",
        "/material/Redes/imagen.png": "...",
    }

    registro_repo = InMemoryRegistroMaterialesRepo()
    registro_repo.registrar_material("lab1.pdf", "Redes")

    service = IngestaService(
        llm=FakeLLM(),
        registro_repo=registro_repo,
        boveda_port=InMemoryBovedaPort(),
        lector_docs=lector_docs,
        ajustes_port=InMemoryAjustesPort(carpeta_mat="/material"),
    )

    escaneo = service.escanear_materia("Redes")

    assert escaneo["materia"] == "Redes"
    assert escaneo["existe"] is True
    assert escaneo["total"] == 2  # lab1.pdf y lab2.docx
    assert escaneo["omitidos"] == 1  # lab1.pdf
    assert escaneo["no_soportados"] == 1  # presentacion.pptx
    assert len(escaneo["pendientes"]) == 1
    assert escaneo["pendientes"][0]["nombre"] == "lab2.docx"


@pytest.mark.parametrize(("peso", "asignado"), [(90, True), (30, False)])
def test_ingesta_alinea_material_con_cronograma(peso, asignado):
    respuesta = json.dumps(
        {"clase_asignada": 1, "peso_afinidad": peso, "subtemas_a_incorporar": ["VLANs"]}
    )
    cronograma_repo = InMemoryCronogramaRepo(
        {"Redes": [{"tema": "Switching", "estado": "pendiente"}]}
    )
    service = IngestaService(
        llm=FakeLLM(texto_default=respuesta),
        registro_repo=InMemoryRegistroMaterialesRepo(),
        boveda_port=InMemoryBovedaPort(),
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
        cronograma_repo=cronograma_repo,
    )

    resultado = service.ingestar_archivo("/x/lab.txt", "lab.txt", "Redes", "actividad")

    assert resultado["alineacion"]["asignado"] is asignado
    clase = cronograma_repo.obtener_cronograma("Redes")[0]
    if asignado:
        assert clase["materiales_asociados"] == ["lab.txt"]
        assert clase["subtemas_adicionales"] == ["VLANs"]
        assert "Redes" not in cronograma_repo.transversal
    else:
        assert "materiales_asociados" not in clase
        assert cronograma_repo.transversal["Redes"][0]["archivo"] == "lab.txt"


def test_eliminar_material_reversibilidad():
    registro_repo = InMemoryRegistroMaterialesRepo()
    boveda_port = InMemoryBovedaPort()
    cronograma_repo = InMemoryCronogramaRepo(
        {
            "Redes": [
                {
                    "tema": "Switching",
                    "estado": "pendiente",
                    "materiales_asociados": ["guia1.pdf", "otro.pdf"],
                }
            ]
        }
    )
    cronograma_repo.agregar_material_transversal("Redes", {"archivo": "guia2.pdf"})

    nota_path = boveda_port.guardar_nota("Redes", "Actividad", "guia1_Notas", "# Notas")
    registro_repo.registrar_material("guia1.pdf", "Redes", nota=nota_path)
    registro_repo.registrar_material("guia2.pdf", "Redes")

    service = IngestaService(
        llm=FakeLLM(),
        registro_repo=registro_repo,
        boveda_port=boveda_port,
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
        cronograma_repo=cronograma_repo,
    )

    assert registro_repo.verificar_material_ingestado("guia1.pdf") is True
    assert nota_path in boveda_port.notas

    # Eliminar guia1.pdf (asociado a clase y con nota en bóveda)
    res = service.eliminar_material("guia1.pdf", borrar_nota=True)
    assert res is not None
    assert registro_repo.verificar_material_ingestado("guia1.pdf") is False
    assert nota_path not in boveda_port.notas
    clase = cronograma_repo.obtener_cronograma("Redes")[0]
    assert clase["materiales_asociados"] == ["otro.pdf"]

    # Eliminar guia2.pdf (transversal)
    service.eliminar_material("guia2.pdf", borrar_nota=False)
    assert "Redes" in cronograma_repo.transversal
    assert len(cronograma_repo.transversal["Redes"]) == 0


def test_vaciar_materiales_solo_borra_las_notas_registradas():
    registro_repo = InMemoryRegistroMaterialesRepo()
    boveda = InMemoryBovedaPort()
    nota_generada = boveda.guardar_nota("Redes", "Actividad", "Tarea1_Notas", "# Tarea 1")
    nota_propia = boveda.guardar_nota("Redes", "Actividad", "Mis_apuntes", "# Escrita a mano")
    registro_repo.registrar_material("Tarea1.pdf", "Redes", nota=nota_generada)

    service = IngestaService(
        llm=FakeLLM(),
        registro_repo=registro_repo,
        boveda_port=boveda,
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
    )
    resultado = service.vaciar_materiales(borrar_notas_obsidian=True)

    assert resultado["total_materiales_eliminados"] == 1
    assert resultado["notas_obsidian_borradas"] == 1
    assert nota_generada not in boveda.notas
    assert nota_propia in boveda.notas
    assert registro_repo.listar_materiales() == []


def test_ingesta_usa_nombre_catalogo_para_carpeta_obsidian():
    materia_repo = InMemoryMateriaRepo(["Ingeniería de Software II"])
    boveda = InMemoryBovedaPort()
    registro_repo = InMemoryRegistroMaterialesRepo()
    service = IngestaService(
        llm=FakeLLM(texto_default="# Resumen de prueba"),
        registro_repo=registro_repo,
        boveda_port=boveda,
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
        materia_repo=materia_repo,
    )

    res = service.ingestar_archivo(
        ruta_archivo="archivo.txt",
        nombre_original="archivo.txt",
        materia="ingenieria de software ii",
    )

    nota_path = res["ruta_salida"]
    assert "Ingeniería de Software II" in nota_path
    assert any("/Ingeniería de Software II/" in k for k in boveda.notas)
