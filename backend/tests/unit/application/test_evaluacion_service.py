"""Tests unitarios para EvaluacionService usando FakeLLM y adaptadores en memoria."""

from __future__ import annotations

import pytest

from modular_learning.core.application.evaluacion import (
    EvaluacionService,
    mezclar_opciones,
)
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryCronogramaRepo,
    InMemoryMateriaRepo,
)


@pytest.fixture
def evaluacion_env():
    # Cronograma con 1 clase completada
    cronograma_repo = InMemoryCronogramaRepo(
        {
            "redes": [
                {"tema": "Arquitectura TCP/IP", "estado": "completado"},
                {"tema": "Modelo OSI", "estado": "pendiente"},
            ]
        }
    )

    fake_llm = FakeLLM(
        json_default={
            "preguntas": [
                {
                    "enunciado": "¿Qué capa de TCP/IP maneja el direccionamiento IP?",
                    "opciones": ["A) Aplicación", "B) Internet", "C) Transporte", "D) Enlace"],
                    "respuesta_correcta": "B) Internet",
                }
            ]
        }
    )

    service = EvaluacionService(llm=fake_llm, cronograma_repo=cronograma_repo)

    return {"service": service, "llm": fake_llm}


def test_generar_quiz_exitoso(evaluacion_env):
    service = evaluacion_env["service"]
    preguntas = service.generar_quiz()

    assert len(preguntas) == 1
    p = preguntas[0]
    assert p["enunciado"] == "¿Qué capa de TCP/IP maneja el direccionamiento IP?"
    assert len(p["opciones"]) == 4
    assert any("Internet" in opt for opt in p["opciones"])
    assert "Internet" in p["respuesta_correcta"]


def test_generar_quiz_sin_temas_completados():
    # Cronograma sin clases completadas
    cronograma_repo = InMemoryCronogramaRepo(
        {"materia": [{"tema": "Tema 1", "estado": "pendiente"}]}
    )
    service = EvaluacionService(llm=FakeLLM(), cronograma_repo=cronograma_repo)

    with pytest.raises(ValueError, match="No hay temas marcados con estado 'completado'"):
        service.generar_quiz()


def test_evaluar_respuestas():
    service = EvaluacionService(llm=FakeLLM(), cronograma_repo=InMemoryCronogramaRepo())
    preguntas = [
        {
            "enunciado": "P1",
            "opciones": ["A) Opt1", "B) Opt2"],
            "respuesta_correcta": "A) Opt1",
        },
        {
            "enunciado": "P2",
            "opciones": ["A) Opt1", "B) Opt2"],
            "respuesta_correcta": "B) Opt2",
        },
    ]

    resultado = service.evaluar_respuestas(preguntas, ["A) Opt1", "A) Opt1"])
    assert resultado["aciertos"] == 1
    assert resultado["total"] == 2
    assert resultado["porcentaje"] == 50
    assert resultado["detalle"][0]["correcto"] is True
    assert resultado["detalle"][1]["correcto"] is False


def test_generar_quiz_sin_cronogramas():
    service = EvaluacionService(llm=FakeLLM(), cronograma_repo=InMemoryCronogramaRepo())
    with pytest.raises(FileNotFoundError):
        service.generar_quiz()


def test_mezclar_opciones():
    pregunta = {
        "enunciado": "Capital de Francia",
        "opciones": ["A) Madrid", "B) París", "C) Roma", "D) Berlín"],
        "respuesta_correcta": "B) París",
    }
    mezclada = mezclar_opciones(pregunta)
    assert len(mezclada["opciones"]) == 4
    assert "París" in mezclada["respuesta_correcta"]
    for opt in mezclada["opciones"]:
        assert opt[0] in "ABCD"


def test_nombre_materia_con_catalogo():
    materia_repo = InMemoryMateriaRepo(["Ingeniería de Software II"])
    service = EvaluacionService(
        llm=FakeLLM(), cronograma_repo=InMemoryCronogramaRepo(), materia_repo=materia_repo
    )
    assert service._nombre_materia("ingenieria-de-software-ii") == "Ingeniería de Software II"
    assert service._nombre_materia("otra-materia") == "otra-materia"


def test_nombre_materia_sin_catalogo():
    service = EvaluacionService(llm=FakeLLM(), cronograma_repo=InMemoryCronogramaRepo())
    assert service._nombre_materia("ingenieria-de-software-ii") == "ingenieria-de-software-ii"
