from unittest.mock import MagicMock

from modular_learning.core.domain.alineador_curricular import asignar_material_a_clase


def test_asignar_material_a_clase(mocker):
    # Mock de los datos del cronograma
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data='{"clases": [{"fecha": "1", "tema": "test", "contenido": ""}]}'),
    )
    mocker.patch(
        "modular_learning.core.domain.alineador_curricular._encontrar_ruta_cronograma",
        return_value="ruta/falsa.json",
    )

    # Mock del puerto LLM (inyección de dependencias)
    mock_llm = MagicMock()
    mock_llm.generar_texto.return_value = (
        '{"clase_asignada": 1, "peso_afinidad": 90, "subtemas_a_incorporar": []}'
    )

    # Ejecución
    resultado = asignar_material_a_clase("Materia", "Contenido", "test.md", llm=mock_llm)

    assert resultado["clase_asignada"] == 1
    assert resultado["peso_afinidad"] == 90
