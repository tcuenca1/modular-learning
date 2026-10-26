"""Tests unitarios del repaso espaciado, del historial y de su integración con quiz y tutoría."""

from __future__ import annotations

import random
from datetime import date, timedelta

from modular_learning.core.application.evaluacion import EvaluacionService
from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.application.tutoria import TutoriaService
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryAjustesPort,
    InMemoryBovedaPort,
    InMemoryCronogramaRepo,
    InMemoryHistorialRepo,
    InMemoryLectorDocumentosPort,
    InMemoryMateriaRepo,
    InMemoryTarjetasRepo,
)

HOY = date(2026, 10, 25)

PREGUNTAS = [
    {
        "enunciado": "¿Qué protocolo usa el puerto 443?",
        "opciones": ["A) HTTP", "B) HTTPS", "C) FTP", "D) SSH"],
        "respuesta_correcta": "B) HTTPS",
        "materia": "Redes",
        "tema": "Capa de aplicación",
        "explicacion": "HTTPS usa TLS sobre el puerto 443.",
    },
    {
        "enunciado": "¿Qué capa encamina paquetes?",
        "opciones": ["A) Red", "B) Enlace", "C) Física", "D) Transporte"],
        "respuesta_correcta": "A) Red",
        "materia": "Redes",
        "tema": "Capa de red",
    },
]


def _servicio() -> RepasoService:
    return RepasoService(InMemoryTarjetasRepo(), InMemoryHistorialRepo(), rng=random.Random(1))


def _detalle(*correctas: bool) -> list[dict]:
    return [{"correcto": c, "elegida": "A) HTTP" if not c else ""} for c in correctas]


def test_registrar_resultados_crea_tarjetas_y_historial():
    servicio = _servicio()
    servicio.registrar_resultados(PREGUNTAS, _detalle(False, True), hoy=HOY)

    tarjetas = {t.tema: t for t in servicio.tarjetas_repo.listar()}
    assert tarjetas["Capa de aplicación"].ultimo_fallo
    assert tarjetas["Capa de aplicación"].proxima == "2026-10-26"
    assert tarjetas["Capa de aplicación"].explicacion.startswith("HTTPS")
    assert not tarjetas["Capa de red"].ultimo_fallo

    eventos = servicio.historial(materia="Redes")
    assert {e["tema"]: (e["aciertos"], e["total"]) for e in eventos} == {
        "Capa de aplicación": (0, 1),
        "Capa de red": (1, 1),
    }
    fallo = next(e for e in eventos if e["tema"] == "Capa de aplicación")
    assert fallo["falladas"] == [PREGUNTAS[0]["enunciado"]]


def test_preguntas_sin_materia_no_se_registran():
    servicio = _servicio()
    servicio.registrar_resultados(
        [{"enunciado": "X", "opciones": [], "respuesta_correcta": ""}], _detalle(True), HOY
    )
    assert servicio.tarjetas_repo.listar() == []


def test_pendientes_y_preguntas_pendientes_conservan_la_tarjeta():
    servicio = _servicio()
    servicio.registrar_resultados(PREGUNTAS, _detalle(False, True), hoy=HOY)
    manana = HOY + timedelta(days=1)

    assert servicio.pendientes(HOY) == []
    assert len(servicio.pendientes(manana)) == 2

    preguntas = servicio.preguntas_pendientes(manana, limite=1)
    assert len(preguntas) == 1
    p = preguntas[0]
    assert p["tarjeta_id"] and p["materia"] == "Redes"
    assert p["respuesta_correcta"] in p["opciones"]

    # Responder la pendiente usa la misma tarjeta (no crea otra)
    servicio.registrar_resultados(preguntas, _detalle(True), hoy=manana)
    assert len(servicio.tarjetas_repo.listar()) == 2


def test_resumen_y_fallos_previos():
    servicio = _servicio()
    servicio.registrar_resultados(PREGUNTAS, _detalle(False, True), hoy=HOY)

    assert servicio.resumen(HOY + timedelta(days=1)) == {
        "pendientes_hoy": 2,
        "total": 2,
        "dominadas": 0,
    }
    assert servicio.fallos_previos("redes", "capa de aplicación") == [PREGUNTAS[0]["enunciado"]]
    assert servicio.fallos_previos("Redes", "Capa de red") == []


def test_evaluar_respuestas_reprograma_y_devuelve_la_clase_de_cada_pregunta():
    repaso = _servicio()
    servicio = EvaluacionService(
        llm=FakeLLM(), cronograma_repo=InMemoryCronogramaRepo(), repaso=repaso
    )

    resultado = servicio.evaluar_respuestas(PREGUNTAS, ["A) HTTP", "A) Red"])

    assert resultado["aciertos"] == 1
    assert resultado["detalle"][0]["tema"] == "Capa de aplicación"
    assert resultado["detalle"][0]["explicacion"]
    assert len(repaso.tarjetas_repo.listar()) == 2


def test_generar_quiz_usa_el_nombre_del_catalogo_y_conserva_la_clase():
    llm = FakeLLM(
        json_default={
            "preguntas": [
                {
                    "materia": "INGENIERIA DE SOFTWARE II",
                    "tema": "Pruebas",
                    "enunciado": "¿Qué es TDD?",
                    "opciones": ["A) a", "B) b", "C) c", "D) d"],
                    "respuesta_correcta": "A) a",
                    "explicacion": "Porque sí.",
                }
            ]
        }
    )
    cronograma = InMemoryCronogramaRepo(
        {"INGENIERIA DE SOFTWARE II": [{"tema": "Pruebas", "estado": "completado"}]}
    )
    servicio = EvaluacionService(
        llm=llm,
        cronograma_repo=cronograma,
        materia_repo=InMemoryMateriaRepo(["Ingeniería de Software II"]),
    )

    assert servicio.obtener_temas_completados() == [
        {"materia": "Ingeniería de Software II", "tema": "Pruebas"}
    ]
    pregunta = servicio.generar_quiz()[0]
    assert pregunta["materia"] == "Ingeniería de Software II"
    assert pregunta["tema"] == "Pruebas"
    assert pregunta["explicacion"] == "Porque sí."


def _tutoria(repaso: RepasoService, llm: FakeLLM | None = None) -> TutoriaService:
    return TutoriaService(
        llm=llm or FakeLLM(),
        cronograma_repo=InMemoryCronogramaRepo(
            {"Redes": [{"tema": "Capa de aplicación", "estado": "pendiente"}]}
        ),
        boveda_port=InMemoryBovedaPort(),
        lector_docs=InMemoryLectorDocumentosPort(),
        ajustes_port=InMemoryAjustesPort(),
        repaso=repaso,
    )


def test_tutoria_de_refuerzo_incluye_la_pregunta_fallada_y_fallos_previos():
    repaso = _servicio()
    repaso.registrar_resultados(PREGUNTAS, _detalle(False, True), hoy=HOY)
    llm = FakeLLM()
    servicio = _tutoria(repaso, llm)

    sesion = servicio.iniciar_sesion(
        "s1", "Redes", "Capa de aplicación", "BASICO", enfoque="¿Por qué falla X?"
    )

    assert sesion.enfoque == "¿Por qué falla X?"
    assert sesion.fallos_previos == [PREGUNTAS[0]["enunciado"]]
    assert "¿Por qué falla X?" in llm.llamadas_json[0]
    prompt = servicio.construir_prompt_explicacion(sesion, 0)
    assert "PUNTOS QUE EL ESTUDIANTE NO DOMINA DE ESTE TEMA" in prompt
    assert PREGUNTAS[0]["enunciado"] in prompt


def test_finalizar_tutoria_queda_en_el_historial():
    repaso = _servicio()
    servicio = _tutoria(repaso)
    sesion = servicio.iniciar_sesion("s1", "Redes", "Capa de aplicación", "AVANZADO")

    servicio.finalizar_sesion(sesion)

    evento = repaso.historial("Redes")[0]
    assert evento["tipo"] == "tutoria"
    assert evento["tema"] == "Capa de aplicación"
    assert evento["nivel"] == "AVANZADO"
