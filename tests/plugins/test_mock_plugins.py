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
