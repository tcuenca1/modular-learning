from modules.core.domain.alineador_curricular import asignar_material_a_clase


def test_asignar_material_a_clase(mocker):
    # Mock de los datos del cronograma
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch(
        "builtins.open",
        mocker.mock_open(read_data='{"clases": [{"fecha": "1", "tema": "test", "contenido": ""}]}'),
    )
    mocker.patch(
        "modules.core.domain.alineador_curricular._encontrar_ruta_cronograma",
        return_value="ruta/falsa.json",
    )

    # Mock de la llamada a la IA
    mock_llm = mocker.patch("modules.core.services.gestor_llm.obtener_llm")
    llm_instance = mock_llm.return_value
    llm_instance.generar_texto.return_value = (
        '{"clase_asignada": 1, "peso_afinidad": 90, "subtemas_a_incorporar": []}'
    )

    # Ejecución
    resultado = asignar_material_a_clase("Materia", "Contenido", "test.md")

    assert resultado["clase_asignada"] == 1
    assert resultado["peso_afinidad"] == 90
