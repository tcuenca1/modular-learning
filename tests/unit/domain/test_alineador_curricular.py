from unittest.mock import MagicMock

from modular_learning.core.domain.alineador_curricular import asignar_material_a_clase
from modular_learning.core.domain.json_llm import limpiar_bloque_markdown


def _llm(respuesta: str) -> MagicMock:
    llm = MagicMock()
    llm.generar_texto.return_value = respuesta
    return llm


def test_asignar_material_a_clase_afin_modifica_clase():
    clases = [{"fecha": "1", "tema": "test", "contenido": ""}]
    llm = _llm(
        '```json\n{"clase_asignada": 1, "peso_afinidad": 90, "subtemas_a_incorporar": ["A"]}\n```'
    )

    resultado = asignar_material_a_clase(clases, "Contenido", "test.md", llm=llm)

    assert resultado["clase_asignada"] == 1
    assert resultado["peso_afinidad"] == 90
    assert resultado["asignado"] is True
    assert clases[0]["materiales_asociados"] == ["test.md"]
    assert clases[0]["subtemas_adicionales"] == ["A"]


def test_asignar_material_a_clase_baja_afinidad_no_modifica():
    clases = [{"tema": "test"}]
    llm = _llm('{"clase_asignada": 1, "peso_afinidad": 20}')

    resultado = asignar_material_a_clase(clases, "Contenido", "test.md", llm=llm)

    assert resultado["asignado"] is False
    assert clases == [{"tema": "test"}]


def test_asignar_material_respuesta_invalida_no_evalua():
    clases = [{"tema": "test"}]
    resultado = asignar_material_a_clase(clases, "x", "t.md", llm=_llm("no es json"))
    assert resultado["asignado"] is None
    assert clases == [{"tema": "test"}]


def test_asignar_material_sin_cronograma_no_llama_llm():
    llm = _llm("{}")
    resultado = asignar_material_a_clase([], "x", "t.md", llm=llm)
    assert resultado["asignado"] is None
    llm.generar_texto.assert_not_called()


def test_limpiar_bloque_markdown():
    assert limpiar_bloque_markdown('```json\n{"a": 1}\n```') == '{"a": 1}'
    assert limpiar_bloque_markdown("```\n[1]\n```") == "[1]"
    assert limpiar_bloque_markdown(' {"a": 1} ') == '{"a": 1}'
