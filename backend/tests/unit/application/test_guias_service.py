"""Tests unitarios del servicio de guías de estudio offline."""

from __future__ import annotations

import pytest

from modular_learning.core.application.guias import GuiaOfflineService
from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.domain.guia_offline import MARCADOR_RESPUESTAS
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryCronogramaRepo,
    InMemoryGuiasRepo,
    InMemoryHistorialRepo,
    InMemoryLectorDocumentosPort,
    InMemoryTarjetasRepo,
)

CLASES = [
    {"fecha": "01/10/2026", "tema": "VLAN", "objetivo": "Segmentar", "estado": "completado"},
    {"fecha": "08/10/2026", "tema": "Trunking", "contenido": "802.1Q", "estado": "pendiente"},
    {"fecha": "15/10/2026", "tema": "STP", "estado": "pendiente"},
]


@pytest.fixture
def contexto():
    cronograma = InMemoryCronogramaRepo({"Redes": [dict(c) for c in CLASES]})
    historial = InMemoryHistorialRepo()
    llm = FakeLLM(texto_default=f"## Explicación\nTexto\n{MARCADOR_RESPUESTAS}\n1. Respuesta")
    servicio = GuiaOfflineService(
        llm=llm,
        cronograma_repo=cronograma,
        lector_docs=InMemoryLectorDocumentosPort(),
        guias_repo=InMemoryGuiasRepo(),
        repaso=RepasoService(tarjetas_repo=InMemoryTarjetasRepo(), historial_repo=historial),
    )
    return servicio, cronograma, historial, llm


def _guia_generada(servicio, temas):
    guia = servicio.crear("Redes", temas)
    for i in range(len(guia.clases)):
        servicio.generar_clase(guia.id, i)
    return guia


def test_crear_respeta_el_orden_del_cronograma(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["stp", "Trunking"])

    assert [c.tema for c in guia.clases] == ["Trunking", "STP"]
    assert guia.clases[0].fecha == "08/10/2026"
    assert guia.extension == "completa"
    assert not guia.completa
    assert servicio.pendientes_de_confirmar() == []


@pytest.mark.parametrize(
    ("materia", "temas", "mensaje"),
    [
        ("Redes", [], "al menos una"),
        ("Redes", ["Inexistente"], "no están en el cronograma"),
        ("Bases de Datos", ["VLAN"], "no tiene cronograma"),
    ],
)
def test_crear_valida_las_clases(contexto, materia, temas, mensaje):
    servicio, *_ = contexto
    with pytest.raises(ValueError, match=mensaje):
        servicio.crear(materia, temas)


def test_generar_clase_usa_el_detalle_del_silabo_y_separa_respuestas(contexto):
    servicio, _, _, llm = contexto
    guia = servicio.crear("Redes", ["Trunking"])

    clase = servicio.generar_clase(guia.id, 0)

    assert clase.contenido == "## Explicación\nTexto"
    assert clase.respuestas == "1. Respuesta"
    prompt = llm.llamadas_texto[-1]["prompt"]
    assert "Trunking" in prompt and "802.1Q" in prompt and MARCADOR_RESPUESTAS in prompt
    assert servicio.obtener(guia.id).pendiente_de_confirmar


def test_generar_clase_fuera_de_rango(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["VLAN"])
    with pytest.raises(ValueError):
        servicio.generar_clase(guia.id, 3)


def test_revision_marca_vistas_las_entendidas_y_deja_pendientes_las_demas(contexto):
    servicio, cronograma, historial, _ = contexto
    guia = _guia_generada(servicio, ["Trunking", "STP"])

    resultado = servicio.registrar_revision(
        guia.id, {0: ("con_dudas", "  ¿Qué es la VLAN nativa?  "), 1: ("pendiente", "ignorado")}
    )

    assert resultado == {
        "materia": "Redes",
        "completadas": ["Trunking"],
        "pendientes": ["STP"],
        "dudas": [{"tema": "Trunking", "dudas": "¿Qué es la VLAN nativa?"}],
    }
    estados = {c["tema"]: c["estado"] for c in cronograma.cronogramas["Redes"]}
    assert estados == {"VLAN": "completado", "Trunking": "completado", "STP": "pendiente"}
    assert [(e["tipo"], e["tema"], e["resultado"]) for e in historial.eventos] == [
        ("guia", "Trunking", "con_dudas"),
        ("guia", "STP", "pendiente"),
    ]
    assert servicio.obtener(guia.id).revisada
    assert servicio.pendientes_de_confirmar() == []


def test_revision_exige_guia_completa_y_todas_las_clases(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["Trunking", "STP"])
    with pytest.raises(ValueError, match="generada"):
        servicio.registrar_revision(guia.id, {0: ("entendida", ""), 1: ("entendida", "")})

    servicio.generar_clase(guia.id, 0)
    servicio.generar_clase(guia.id, 1)
    with pytest.raises(ValueError, match="cada clase"):
        servicio.registrar_revision(guia.id, {0: ("entendida", "")})
    with pytest.raises(ValueError, match="no válido"):
        servicio.registrar_revision(guia.id, {0: ("quizas", ""), 1: ("entendida", "")})


def test_revision_no_se_repite(contexto):
    servicio, *_ = contexto
    guia = _guia_generada(servicio, ["VLAN"])
    servicio.registrar_revision(guia.id, {0: ("entendida", "")})
    with pytest.raises(ValueError, match="ya se confirmó"):
        servicio.registrar_revision(guia.id, {0: ("entendida", "")})


def test_obtener_inexistente(contexto):
    servicio, *_ = contexto
    with pytest.raises(LookupError):
        servicio.obtener("nope")
