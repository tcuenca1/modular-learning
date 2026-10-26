"""Tests unitarios para SilaboService usando FakeLLM y adaptadores en memoria."""

from __future__ import annotations

import pytest

from modular_learning.core.application.silabo import SilaboService
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryCronogramaRepo,
    InMemoryLectorDocumentosPort,
    InMemoryMateriaRepo,
)


@pytest.fixture
def silabo_env():
    cronograma_repo = InMemoryCronogramaRepo()
    materia_repo = InMemoryMateriaRepo(["Redes"])
    lector_docs = InMemoryLectorDocumentosPort()

    fake_llm = FakeLLM(
        json_default={
            "clases": [
                {"clase": 1, "tema": "Introducción a IoT", "estado": "pendiente"},
                {"clase": 2, "tema": "Protocolo MQTT", "estado": "pendiente"},
            ]
        }
    )

    service = SilaboService(
        llm=fake_llm,
        cronograma_repo=cronograma_repo,
        materia_repo=materia_repo,
        lector_docs=lector_docs,
    )

    return {
        "service": service,
        "llm": fake_llm,
        "cronograma": cronograma_repo,
        "materias": materia_repo,
        "lector": lector_docs,
    }


def test_extraer_cronograma(silabo_env, tmp_path):
    service = silabo_env["service"]

    # Crear archivo de prueba
    archivo_silabo = tmp_path / "SYLLABUS-Internet-de-las-Cosas.md"
    silabo_env["lector"].materiales[str(archivo_silabo)] = (
        "4.2 Estructura de la unidad didáctica por temas\nClase 1: Introducción\n4.3 Distribución de horas"
    )

    resultado = service.extraer_cronograma(str(archivo_silabo), "Internet de las Cosas")
    assert "clases" in resultado
    assert len(resultado["clases"]) == 2
    assert resultado["clases"][0]["tema"] == "Introducción a IoT"


def test_guardar_cronograma(silabo_env):
    service = silabo_env["service"]
    cronograma_repo = silabo_env["cronograma"]
    materia_repo = silabo_env["materias"]

    datos = [
        {"clase": 1, "tema": "Tema 1", "estado": "pendiente"},
        {"clase": 2, "tema": "Tema 2", "estado": "pendiente"},
    ]

    ruta = service.guardar_cronograma("Sistemas Distribuidos", datos)
    assert "sistemas_distribuidos_cronograma.json" in ruta.lower()
    assert "Sistemas Distribuidos" in materia_repo.cargar_materias()
    assert len(cronograma_repo.obtener_cronograma("Sistemas Distribuidos")) == 2


def test_sugerir_nombre_materia():
    service = SilaboService(
        llm=FakeLLM(),
        cronograma_repo=InMemoryCronogramaRepo(),
        materia_repo=InMemoryMateriaRepo(),
        lector_docs=InMemoryLectorDocumentosPort(),
    )

    sug1 = service.sugerir_nombre_materia("SYLLABUS-Redes-de-Computadoras.pdf")
    assert "Redes" in sug1

    sug2 = service.sugerir_nombre_materia("Syllabus_Sistemas_Operativos.txt")
    assert "Sistemas" in sug2


def test_delimitar_seccion_temas():
    service = SilaboService(
        llm=FakeLLM(),
        cronograma_repo=InMemoryCronogramaRepo(),
        materia_repo=InMemoryMateriaRepo(),
        lector_docs=InMemoryLectorDocumentosPort(),
    )

    texto = (
        "1. Datos Generales\n"
        "4.2 Estructura de la unidad didáctica por temas\n"
        "Semana 1: Protocolos de enrutamiento\n"
        "4.3 Distribución de horas en unidades y temas\n"
        "5. Metodología"
    )

    delimitado = service.delimitar_seccion_temas(texto)
    assert "4.2 Estructura" in delimitado
    assert "Semana 1: Protocolos" in delimitado
    assert "5. Metodología" not in delimitado
