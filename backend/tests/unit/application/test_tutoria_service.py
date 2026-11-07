"""Tests unitarios para TutoriaService usando FakeLLM y adaptadores en memoria."""

from __future__ import annotations

import pytest

from modular_learning.core.application.tutoria import TutoriaService
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryAjustesPort,
    InMemoryBovedaPort,
    InMemoryCronogramaRepo,
    InMemoryLectorDocumentosPort,
    InMemoryMateriaRepo,
)


@pytest.fixture
def tutoria_env():
    fake_llm = FakeLLM(
        texto_default="Explicación detallada del paso por el FakeLLM.",
        json_default={
            "pasos": [
                {"titulo": "Introducción", "descripcion": "Conceptos clave"},
                {"titulo": "Desarrollo", "descripcion": "Profundización técnica"},
            ]
        },
        stream_chunks=["Hola ", "estudiante, ", "aquí está la explicación."],
    )
    cronograma_repo = InMemoryCronogramaRepo(
        {
            "Redes": [
                {
                    "clase": 1,
                    "tema": "Subnetting",
                    "estado": "pendiente",
                    "materiales_asociados": ["guia1.pdf"],
                    "subtemas_adicionales": ["VLSM", "CIDR"],
                }
            ]
        }
    )
    boveda_port = InMemoryBovedaPort()
    lector_docs = InMemoryLectorDocumentosPort()
    ajustes_port = InMemoryAjustesPort()

    service = TutoriaService(
        llm=fake_llm,
        cronograma_repo=cronograma_repo,
        boveda_port=boveda_port,
        lector_docs=lector_docs,
        ajustes_port=ajustes_port,
    )

    return {
        "service": service,
        "llm": fake_llm,
        "cronograma": cronograma_repo,
        "boveda": boveda_port,
    }


def test_iniciar_sesion(tutoria_env):
    service = tutoria_env["service"]
    sesion = service.iniciar_sesion(
        sesion_id="sesion-123",
        materia="Redes",
        tema="Subnetting",
        nivel_profundidad="avanzado",
    )

    assert sesion.sesion_id == "sesion-123"
    assert sesion.materia == "Redes"
    assert sesion.tema == "Subnetting"
    assert sesion.nivel_profundidad == "AVANZADO"
    assert len(sesion.pasos) == 2
    assert sesion.pasos[0]["titulo"] == "Introducción"
    assert "guia1.pdf" in sesion.materiales_asociados
    assert "VLSM" in sesion.subtemas_adicionales
    assert len(sesion.historial) == 2


def test_explicar_paso(tutoria_env):
    service = tutoria_env["service"]
    sesion = service.iniciar_sesion("s1", "Redes", "Subnetting", "intermedio")

    explicacion = service.explicar_paso(sesion, 0)
    assert explicacion == "Explicación detallada del paso por el FakeLLM."
    assert 0 in sesion.pasos_completados
    # Historial: 2 iniciales + 2 de la explicación
    assert len(sesion.historial) == 4


def test_explicar_paso_stream(tutoria_env):
    service = tutoria_env["service"]
    sesion = service.iniciar_sesion("s1", "Redes", "Subnetting", "intermedio")

    chunks = list(service.explicar_paso_stream(sesion, 1))
    assert "".join(chunks) == "Hola estudiante, aquí está la explicación."
    assert 1 in sesion.pasos_completados
    assert len(sesion.historial) == 4


def test_responder_duda(tutoria_env):
    service = tutoria_env["service"]
    sesion = service.iniciar_sesion("s1", "Redes", "Subnetting", "intermedio")
    service.explicar_paso(sesion, 0)

    respuesta = service.responder_duda(sesion, 0, "¿Qué es una máscara /24?")
    assert respuesta == "Explicación detallada del paso por el FakeLLM."
    assert len(sesion.historial) == 6


def test_finalizar_sesion(tutoria_env):
    service = tutoria_env["service"]
    cronograma = tutoria_env["cronograma"]
    boveda = tutoria_env["boveda"]

    sesion = service.iniciar_sesion("s1", "Redes", "Subnetting", "intermedio")
    service.explicar_paso(sesion, 0)

    resultado = service.finalizar_sesion(sesion)
    assert resultado["guardado_obsidian"] is True
    assert resultado["clase_completada"] is True
    assert ("Redes", "Subnetting") in boveda.resumenes

    detalle = cronograma.obtener_detalle_clase("Redes", "Subnetting")
    assert detalle["estado"] == "completado"


def test_paso_invalido_lanza_error(tutoria_env):
    service = tutoria_env["service"]
    sesion = service.iniciar_sesion("s1", "Redes", "Subnetting", "intermedio")

    with pytest.raises(IndexError):
        service.explicar_paso(sesion, 99)

    with pytest.raises(IndexError):
        list(service.explicar_paso_stream(sesion, -1))


def test_tutoria_iniciar_sesion_resuelve_materia_catalogo():
    materia_repo = InMemoryMateriaRepo(["Ingeniería de Software II"])
    cronograma_repo = InMemoryCronogramaRepo()
    llm = FakeLLM(json_default={"pasos": [{"titulo": "Paso 1", "objetivo": "Obj 1"}]})
    service = TutoriaService(
        llm=llm,
        cronograma_repo=cronograma_repo,
        boveda_port=InMemoryBovedaPort(),
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
        materia_repo=materia_repo,
    )
    sesion = service.iniciar_sesion("s1", "ingenieria de software ii", "Patrones", "intermedio")
    assert sesion.materia == "Ingeniería de Software II"
