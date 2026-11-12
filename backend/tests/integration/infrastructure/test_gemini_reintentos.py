"""Reintentos del adaptador de Gemini ante fallos pasajeros (503 «alta demanda», 429, red)."""

from __future__ import annotations

import pytest

from modular_learning.core.ports.llm import LLMNoDisponible
from modular_learning.infrastructure.llm import gemini_adapter
from modular_learning.infrastructure.llm.gemini_adapter import LLM_GeminiAdapter

ERROR_503 = "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand.'}}"


class _Respuesta:
    def __init__(self, text):
        self.text = text


class _Chunk:
    def __init__(self, text):
        self.text = text


class _Modelos:
    """Cada llamada saca el siguiente guion: una excepción o un resultado."""

    def __init__(self, guion, registro):
        self.guion, self.registro = list(guion), registro

    def _siguiente(self, modelo, tipo):
        self.registro.append((tipo, modelo))
        paso = self.guion.pop(0)
        if isinstance(paso, Exception):
            raise paso
        return paso

    def generate_content(self, model, contents, config=None):
        return _Respuesta(self._siguiente(model, "texto"))

    def generate_content_stream(self, model, contents):
        return self._siguiente(model, "stream")


class _Cliente:
    def __init__(self, guion):
        self.registro: list[tuple[str, str]] = []
        self.models = _Modelos(guion, self.registro)


def _adaptador(monkeypatch, guion, respaldo="") -> tuple[LLM_GeminiAdapter, _Cliente, list[float]]:
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    monkeypatch.setenv("GEMINI_MODEL", "principal")
    if respaldo:
        monkeypatch.setenv("GEMINI_MODELO_RESPALDO", respaldo)
    else:
        monkeypatch.delenv("GEMINI_MODELO_RESPALDO", raising=False)
    esperas: list[float] = []
    monkeypatch.setattr(gemini_adapter.time, "sleep", esperas.append)
    adaptador = LLM_GeminiAdapter()
    cliente = _Cliente(guion)
    adaptador._cliente = cliente  # type: ignore[assignment]
    return adaptador, cliente, esperas


# ----------------------------------------------------------------------------- clasificación
@pytest.mark.parametrize(
    "texto",
    [
        ERROR_503,
        "ServerError: 500 INTERNAL",
        "504 DEADLINE_EXCEEDED",
        "model is overloaded",
        "httpx.ConnectError: [Errno 104]",
        "ReadTimeout",
        "RemoteProtocolError: peer closed",
    ],
)
def test_errores_pasajeros_se_reconocen(texto):
    assert LLM_GeminiAdapter._es_transitorio(Exception(texto)) is True


@pytest.mark.parametrize(
    "texto",
    [
        "400 INVALID_ARGUMENT",
        "401 UNAUTHENTICATED API key not valid",
        "403 PERMISSION_DENIED",
        "se usaron 5000 tokens",
        "Falta la variable GEMINI_API_KEY",
    ],
)
def test_errores_definitivos_no_se_reintentan(texto):
    assert LLM_GeminiAdapter._es_transitorio(Exception(texto)) is False


# ----------------------------------------------------------------------------- texto y JSON
def test_un_503_se_reintenta_con_espera_creciente_y_termina_bien(monkeypatch):
    adaptador, cliente, esperas = _adaptador(
        monkeypatch, [Exception(ERROR_503), Exception(ERROR_503), "Hola"]
    )
    assert adaptador.generar_texto("hola") == "Hola"
    assert esperas == [1.5, 3.0]
    assert len(cliente.registro) == 3


def test_si_el_503_no_cede_avisa_con_un_mensaje_claro(monkeypatch):
    adaptador, cliente, esperas = _adaptador(monkeypatch, [Exception(ERROR_503)] * 4)
    with pytest.raises(LLMNoDisponible) as e:
        adaptador.generar_texto("hola")
    assert "saturado" in str(e.value) and "inténtalo de nuevo" in str(e.value)
    assert esperas == [1.5, 3.0, 6.0] and len(cliente.registro) == 4


def test_pasa_al_modelo_de_respaldo_cuando_el_principal_sigue_caido(monkeypatch):
    adaptador, cliente, _ = _adaptador(
        monkeypatch, [Exception(ERROR_503)] * 4 + ["desde el respaldo"], respaldo="respaldo"
    )
    assert adaptador.generar_texto("hola") == "desde el respaldo"
    assert [m for _, m in cliente.registro] == ["principal"] * 4 + ["respaldo"]


def test_un_error_definitivo_se_propaga_sin_reintentar(monkeypatch):
    adaptador, cliente, esperas = _adaptador(monkeypatch, [Exception("400 INVALID_ARGUMENT")])
    with pytest.raises(RuntimeError, match="INVALID_ARGUMENT"):
        adaptador.generar_texto("hola")
    assert esperas == [] and len(cliente.registro) == 1


def test_limite_429_espera_20_40_60_y_avisa(monkeypatch):
    adaptador, _, esperas = _adaptador(monkeypatch, [Exception("429 RESOURCE_EXHAUSTED")] * 4)
    with pytest.raises(LLMNoDisponible):
        adaptador.generar_texto("hola")
    assert esperas == [20, 40, 60]


def test_json_estructurado_reintenta_y_parsea(monkeypatch):
    adaptador, _, esperas = _adaptador(monkeypatch, [Exception(ERROR_503), '{"pasos": [1]}'])
    assert adaptador.generar_json_estructurado("x") == {"pasos": [1]}
    assert esperas == [1.5]


def test_json_estructurado_agotado_da_llm_no_disponible(monkeypatch):
    adaptador, _, _ = _adaptador(monkeypatch, [Exception(ERROR_503)] * 4)
    with pytest.raises(LLMNoDisponible):
        adaptador.generar_json_estructurado("x")


# ----------------------------------------------------------------------------- streaming
def _consumir(adaptador) -> list[str]:
    return list(adaptador.generar_respuesta_stream("explica"))


def test_stream_reintenta_si_falla_antes_de_emitir_y_no_duplica_texto(monkeypatch):
    adaptador, cliente, esperas = _adaptador(
        monkeypatch, [Exception(ERROR_503), iter([_Chunk("Hola "), _Chunk(""), _Chunk("mundo")])]
    )
    assert _consumir(adaptador) == ["Hola ", "mundo"]
    assert esperas == [1.5] and len(cliente.registro) == 2


def test_stream_que_se_corta_a_mitad_no_se_reintenta_y_lo_dice(monkeypatch):
    def a_medias():
        yield _Chunk("Primera parte ")
        raise RuntimeError(ERROR_503)

    adaptador, cliente, esperas = _adaptador(monkeypatch, [a_medias()])
    salida: list[str] = []
    with pytest.raises(LLMNoDisponible) as e:
        salida.extend(adaptador.generar_respuesta_stream("explica"))
    assert salida == ["Primera parte "]  # lo emitido no se repite ni se pierde
    assert "interrumpió" in str(e.value) and "Reintentar" in str(e.value)
    assert esperas == [] and len(cliente.registro) == 1


def test_stream_con_503_persistente_avisa_y_usa_el_respaldo_si_existe(monkeypatch):
    adaptador, cliente, _ = _adaptador(
        monkeypatch, [Exception(ERROR_503)] * 4 + [iter([_Chunk("ok")])], respaldo="respaldo"
    )
    assert _consumir(adaptador) == ["ok"]
    assert [m for _, m in cliente.registro][-1] == "respaldo"

    adaptador, _, _ = _adaptador(monkeypatch, [Exception(ERROR_503)] * 4)
    with pytest.raises(LLMNoDisponible):
        _consumir(adaptador)


def test_stream_con_error_definitivo_no_se_reintenta(monkeypatch):
    adaptador, cliente, esperas = _adaptador(monkeypatch, [Exception("401 UNAUTHENTICATED")])
    with pytest.raises(RuntimeError, match="UNAUTHENTICATED"):
        _consumir(adaptador)
    assert esperas == [] and len(cliente.registro) == 1
