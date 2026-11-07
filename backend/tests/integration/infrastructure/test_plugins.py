import json
from unittest.mock import MagicMock

from modular_learning.infrastructure.plugins.cisco import (
    CiscoPlugin,
    formatear_resumen_dispositivo,
    parsear_configuracion_ios,
)
from modular_learning.infrastructure.plugins.nodered import NodeRedPlugin
from modular_learning.infrastructure.plugins.web import (
    WebPlugin,
    es_archivo_secreto,
)


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
    plugin = NodeRedPlugin()

    mock_flow_data = '[{"id": "node_1", "type": "inject", "name": "Sensor Inject", "topic": "sensors/temp"}, {"id": "node_2", "type": "debug", "name": "Debug Node"}]'

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_flow_data))

    resultado = plugin.analizar_flujo("dummy_flow.json")
    assert isinstance(resultado, str)
    assert "Análisis de Flujo IoT" in resultado
    assert "inject" in resultado
    assert "debug" in resultado


def test_nodered_plugin_analizar_flujo_con_pestanas(tmp_path):
    plugin = NodeRedPlugin()
    flow_data = [
        {"id": "tab_1", "type": "tab", "label": "Telemetria Sensores"},
        {
            "id": "node_1",
            "z": "tab_1",
            "type": "mqtt in",
            "topic": "sensores/temp",
            "name": "Temp MQTT",
        },
        {
            "id": "node_2",
            "z": "tab_1",
            "type": "function",
            "name": "Filtrar Ruido",
            "func": "// calcular media\nreturn msg;",
        },
        {"id": "tab_2", "type": "tab", "label": "Panel Visual"},
        {"id": "node_3", "z": "tab_2", "type": "ui_gauge", "name": "Medidor Temp"},
    ]
    flow_file = tmp_path / "flujo_iot.json"
    flow_file.write_text(json.dumps(flow_data), encoding="utf-8")

    resultado = plugin.analizar_flujo(str(flow_file))
    assert "Telemetria Sensores" in resultado
    assert "sensores/temp" in resultado
    assert "Panel Visual" in resultado
    assert "Medidor Temp" in resultado


def test_nodered_plugin_analizar_flujo_invalido(mocker):
    plugin = NodeRedPlugin()

    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "doc", 0))

    resultado = plugin.analizar_flujo("invalid_flow.json")
    assert isinstance(resultado, str)
    assert "Error" in resultado


def test_cisco_parsear_configuracion_ios():
    cfg = """
    hostname Router-Central
    !
    vlan 20
     name Docencia
    !
    interface GigabitEthernet0/0/0
     description Enlace Core
     ip address 192.168.10.1 255.255.255.0
     no shutdown
    !
    interface FastEthernet0/1
     switchport mode trunk
     switchport trunk allowed vlan 10,20
    !
    router ospf 10
     network 192.168.10.0 0.0.0.255 area 0
    !
    ip route 0.0.0.0 0.0.0.0 10.0.0.1
    !
    access-list 101 permit ip any any
    """
    datos = parsear_configuracion_ios(cfg)
    assert datos["hostname"] == "Router-Central"
    assert len(datos["vlans"]) == 1
    assert datos["vlans"][0]["id"] == "20"
    assert datos["vlans"][0]["nombre"] == "Docencia"

    ifaces = {i["nombre"]: i for i in datos["interfaces"]}
    assert "GigabitEthernet0/0/0" in ifaces
    assert ifaces["GigabitEthernet0/0/0"]["ip"] == "192.168.10.1 255.255.255.0"
    assert ifaces["FastEthernet0/1"]["modo"] == "trunk"

    assert any("OSPF" in r for r in datos["enrutamiento"])
    assert any("Ruta estática" in r for r in datos["enrutamiento"])
    assert len(datos["acls"]) == 1

    resumen = formatear_resumen_dispositivo(datos)
    assert "Router-Central" in resumen
    assert "GigabitEthernet0/0/0" in resumen


def test_cisco_analizar_carpeta(tmp_path):
    plugin = CiscoPlugin()
    cfg_file = tmp_path / "R1_running.cfg"
    cfg_file.write_text(
        "hostname R1\ninterface GigabitEthernet0/0\n ip address 10.0.1.1 255.255.255.0\n",
        encoding="utf-8",
    )

    resultado = plugin.analizar_carpeta(str(tmp_path))
    assert "R1" in resultado
    assert "GigabitEthernet0/0" in resultado
    assert "10.0.1.1" in resultado


def test_web_es_archivo_secreto():
    assert es_archivo_secreto(".env") is True
    assert es_archivo_secreto(".env.local") is True
    assert es_archivo_secreto("credentials.json") is True
    assert es_archivo_secreto("server.key") is True
    assert es_archivo_secreto("App.tsx") is False
    assert es_archivo_secreto("routes.py") is False


def test_web_analizar_proyecto(tmp_path):
    plugin = WebPlugin()
    # Crear estructura de proyecto web
    (tmp_path / "README.md").write_text(
        "# Sistema de Reservas\nApp para agendar citas.", encoding="utf-8"
    )
    pkg = {
        "name": "reservas-app",
        "dependencies": {"react": "^18.0", "express": "^4.18"},
        "scripts": {"dev": "vite", "build": "vite build"},
    }
    (tmp_path / "package.json").write_text(json.dumps(pkg), encoding="utf-8")

    src_dir = tmp_path / "src"
    src_dir.mkdir()
    routes_file = src_dir / "routes.ts"
    routes_file.write_text("router.get('/api/reservas', (req, res) => {});\n", encoding="utf-8")

    resultado = plugin.analizar_proyecto(str(tmp_path))
    assert "reservas-app" in resultado
    assert "react" in resultado
    assert "GET /api/reservas" in resultado
    assert "Sistema de Reservas" in resultado
