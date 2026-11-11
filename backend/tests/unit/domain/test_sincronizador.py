"""Tests de `core.domain.sincronizador`: fusión de subtemas extraídos por la IA en el cronograma."""

from __future__ import annotations

import logging
from typing import Any

from modular_learning.core.domain.sincronizador import extraer_y_fusionar_subtemas
from tests.unit.application.fake_adapters import FakeLLM


def _clases() -> list[dict[str, Any]]:
    return [
        {"fecha": "01/10/2026", "tema": "Introducción a las redes", "estado": "completado"},
        {"fecha": "08/10/2026", "tema": "Enrutamiento estático", "estado": "pendiente"},
        {"fecha": "15/10/2026", "tema": "VLAN y trunking", "estado": "pendiente"},
    ]


def _llm(respuesta: Any) -> FakeLLM:
    return FakeLLM(json_default=respuesta)


def test_sin_cronograma_no_llama_a_la_ia():
    llm = _llm([])
    assert extraer_y_fusionar_subtemas([], "apuntes", llm) == 0
    assert llm.llamadas_json == []


def test_el_prompt_lleva_el_cronograma_y_los_apuntes():
    llm = _llm([])
    extraer_y_fusionar_subtemas(_clases(), "APUNTES DE PRUEBA", llm)
    prompt = llm.llamadas_json[0]
    assert "Enrutamiento estático" in prompt
    assert "APUNTES DE PRUEBA" in prompt


def test_asigna_por_fecha_exacta():
    clases = _clases()
    n = extraer_y_fusionar_subtemas(
        clases, "x", _llm([{"fecha_o_tema_relacionado": "15/10/2026", "nuevos_subtemas": ["STP"]}])
    )
    assert n == 1
    assert clases[2]["subtemas_adicionales"] == ["STP"]
    assert "subtemas_adicionales" not in clases[0]


def test_asigna_por_tema_contenido_en_ambos_sentidos():
    clases = _clases()
    respuesta = [
        {"fecha_o_tema_relacionado": "VLAN", "nuevos_subtemas": ["802.1Q"]},  # ref dentro del tema
        {
            "fecha_o_tema_relacionado": "enrutamiento estático y dinámico",  # tema dentro de la ref
            "nuevos_subtemas": ["OSPF"],
        },
    ]
    assert extraer_y_fusionar_subtemas(clases, "x", _llm(respuesta)) == 2
    assert clases[2]["subtemas_adicionales"] == ["802.1Q"]
    assert clases[1]["subtemas_adicionales"] == ["OSPF"]


def test_una_referencia_puede_coincidir_con_varias_clases():
    clases = [
        {"fecha": "a", "tema": "Redes I", "estado": "pendiente"},
        {"fecha": "b", "tema": "Redes II", "estado": "pendiente"},
    ]
    n = extraer_y_fusionar_subtemas(
        clases, "x", _llm([{"fecha_o_tema_relacionado": "redes", "nuevos_subtemas": ["NAT"]}])
    )
    assert n == 2
    assert all(c["subtemas_adicionales"] == ["NAT"] for c in clases)


def test_sin_coincidencia_va_a_la_primera_clase_pendiente():
    clases = _clases()
    n = extraer_y_fusionar_subtemas(
        clases, "x", _llm([{"fecha_o_tema_relacionado": "otro tema", "nuevos_subtemas": ["QoS"]}])
    )
    assert n == 1
    assert clases[1]["subtemas_adicionales"] == ["QoS"]


def test_sin_coincidencia_ni_pendientes_va_a_la_ultima_clase():
    clases = [
        {"fecha": "a", "tema": "A", "estado": "completado"},
        {"fecha": "b", "tema": "B", "estado": "completado"},
    ]
    extraer_y_fusionar_subtemas(
        clases, "x", _llm([{"fecha_o_tema_relacionado": "zzz", "nuevos_subtemas": ["Z"]}])
    )
    assert clases[1]["subtemas_adicionales"] == ["Z"]
    assert "subtemas_adicionales" not in clases[0]


def test_referencia_vacia_se_trata_como_sin_coincidencia():
    clases = _clases()
    extraer_y_fusionar_subtemas(
        clases, "x", _llm([{"fecha_o_tema_relacionado": "  ", "nuevos_subtemas": ["Q"]}])
    )
    assert clases[1]["subtemas_adicionales"] == ["Q"]


def test_no_duplica_ignora_vacios_y_conserva_los_existentes():
    clases = _clases()
    clases[2]["subtemas_adicionales"] = ["STP"]
    respuesta = [
        {
            "fecha_o_tema_relacionado": "vlan",
            "nuevos_subtemas": ["STP", " RSTP ", "", "   ", 802, "RSTP"],
        }
    ]
    n = extraer_y_fusionar_subtemas(clases, "x", _llm(respuesta))
    assert n == 2  # RSTP y "802" (convertido a texto); STP ya estaba y RSTP no se repite
    assert clases[2]["subtemas_adicionales"] == ["STP", "RSTP", "802"]


def test_ignora_elementos_mal_formados():
    clases = _clases()
    respuesta = [
        "texto suelto",
        {"fecha_o_tema_relacionado": "vlan"},
        {"fecha_o_tema_relacionado": "vlan", "nuevos_subtemas": []},
        {"fecha_o_tema_relacionado": "vlan", "nuevos_subtemas": "no es lista"},
        {"fecha_o_tema_relacionado": "vlan", "nuevos_subtemas": ["Válido"]},
    ]
    assert extraer_y_fusionar_subtemas(clases, "x", _llm(respuesta)) == 1
    assert clases[2]["subtemas_adicionales"] == ["Válido"]


def test_respuesta_que_no_es_lista_devuelve_cero():
    clases = _clases()
    assert extraer_y_fusionar_subtemas(clases, "x", _llm({"subtemas": ["A"]})) == 0
    assert all("subtemas_adicionales" not in c for c in clases)


class _LLMJsonRoto(FakeLLM):
    """El modo JSON estructurado falla; queda el texto libre."""

    def generar_json_estructurado(self, prompt: str):
        raise RuntimeError("sin modo json")


def test_si_falla_el_json_estructurado_parsea_el_texto():
    clases = _clases()
    llm = _LLMJsonRoto(
        texto_default='```json\n[{"fecha_o_tema_relacionado": "VLAN", "nuevos_subtemas": ["VTP"]}]\n```'
    )
    assert extraer_y_fusionar_subtemas(clases, "x", llm) == 1
    assert clases[2]["subtemas_adicionales"] == ["VTP"]
    assert len(llm.llamadas_texto) == 1


def test_si_todo_falla_devuelve_cero_y_lo_registra(caplog):
    clases = _clases()
    llm = _LLMJsonRoto(texto_default="no es JSON en absoluto")
    with caplog.at_level(logging.WARNING):
        assert extraer_y_fusionar_subtemas(clases, "x", llm) == 0
    assert "No se pudo parsear" in caplog.text
    assert all("subtemas_adicionales" not in c for c in clases)
