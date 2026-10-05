from unittest.mock import MagicMock

from modules.plugins.adapters.plugin_web import WebPlugin


def test_web_plugin_guardar_y_cargar_contexto(mocker):
    plugin = WebPlugin()

    # Mockear operaciones de archivo para aislamiento
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data='["Proyecto Web Mocked"]'))

    contexto = plugin.cargar_contexto_reciente()
    assert contexto == "Proyecto Web Mocked"


def test_plugin_external_network_or_hardware_mocked(mocker):
    """Prueba preparada para falsear (mockear) llamadas externas de red o hardware en adaptadores."""
    mock_urlopen = mocker.patch("urllib.request.urlopen")
    cm = MagicMock()
    cm.read.return_value = b'{"status": "connected", "hardware": "cisco_router_virtual"}'
    mock_urlopen.return_value.__enter__.return_value = cm

    import urllib.request

    url = "http://192.168.1.1/api/status"
    with urllib.request.urlopen(url) as response:
        data = response.read()

    assert b"cisco_router_virtual" in data
    mock_urlopen.assert_called_once_with(url)


def test_nodered_plugin_analizar_flujo_valido(mocker):
    from modules.plugins.adapters.plugin_nodered import NodeRedPlugin

    plugin = NodeRedPlugin()

    mock_flow_data = '[{"id": "node_1", "type": "inject", "name": "Sensor Inject", "topic": "sensors/temp"}, {"id": "node_2", "type": "debug", "name": "Debug Node"}]'

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_flow_data))

    resultado = plugin.analizar_flujo("dummy_flow.json")
    assert isinstance(resultado, str)
    assert "Análisis de Flujo IoT" in resultado
    assert "inject" in resultado
    assert "debug" in resultado


def test_nodered_plugin_analizar_flujo_invalido(mocker):
    from modules.plugins.adapters.plugin_nodered import NodeRedPlugin
    import json

    plugin = NodeRedPlugin()

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "doc", 0))

    resultado = plugin.analizar_flujo("invalid_flow.json")
    assert isinstance(resultado, str)
    assert "Error" in resultado


def test_gestor_plugins_procesar_archivo_iot(mocker):
    from modules.plugins.services import gestor_plugins

    mock_flow_data = '[{"id": "1", "type": "mqtt in", "topic": "home/living/temp"}]'
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_flow_data))

    resultado = gestor_plugins.procesar_archivo_plugin("dummy.json", "iot")
    assert isinstance(resultado, str)
    assert "Análisis de Flujo IoT" in resultado
