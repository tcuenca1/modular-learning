from __future__ import annotations

import pytest

from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.ports.plugin_practico import PluginPracticoBase
from tests.unit.application.fake_adapters import (
    InMemoryLectorDocumentosPort,
    InMemoryPluginConfigRepo,
)


class FakePlugin(PluginPracticoBase):
    def __init__(self, nombre: str = "Fake") -> None:
        self.nombre = nombre
        self.contexto = ""
        self.carpeta_analizada = ""

    def obtener_instrucciones_ia(self) -> str:
        return f"[INSTRUCCIONES {self.nombre}]"

    def generar_ejercicio_base(self, tema: str) -> str:
        return f"[EJERCICIO {self.nombre}: {tema}]"

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        self.contexto = metadatos

    def cargar_contexto_reciente(self) -> str:
        return self.contexto

    def analizar_carpeta(self, ruta_carpeta: str) -> str:
        self.carpeta_analizada = ruta_carpeta
        return f"Analizado {ruta_carpeta} en {self.nombre}"

    def analizar_proyecto(self, ruta_carpeta: str) -> str:
        self.carpeta_analizada = ruta_carpeta
        return f"Proyecto {ruta_carpeta} analizado en {self.nombre}"


@pytest.fixture
def servicio() -> PluginsService:
    config_repo = InMemoryPluginConfigRepo()
    plugins = {
        "cisco": FakePlugin("Cisco"),
        "nodered": FakePlugin("NodeRed"),
        "web": FakePlugin("Web"),
    }
    lector = InMemoryLectorDocumentosPort()
    lector.carpetas.add("/material/mis_redes")
    return PluginsService(plugins=plugins, config_repo=config_repo, lector_docs=lector)


def test_listar_info_plugins(servicio: PluginsService):
    info = servicio.listar_info_plugins()
    assert len(info) == 3
    ids = [p["id"] for p in info]
    assert "cisco" in ids
    assert "nodered" in ids
    assert "web" in ids


def test_guardar_y_obtener_configuracion(servicio: PluginsService):
    carpeta_test = "/material/mis_redes"
    res = servicio.guardar_configuracion_plugin(
        "cisco", carpeta=carpeta_test, materia="redes-avanzadas"
    )
    assert res["carpeta"] == carpeta_test
    assert res["materia"] == "redes-avanzadas"

    configs = servicio.obtener_configuraciones()
    assert configs["cisco"]["carpeta"] == carpeta_test
    assert configs["cisco"]["materia"] == "redes-avanzadas"


def test_obtener_plugin_por_materia_configurada(servicio: PluginsService):
    servicio.guardar_configuracion_plugin("web", materia="desarrollo-fullstack")
    plugin = servicio.obtener_plugin("Desarrollo Fullstack")
    assert plugin is not None
    assert getattr(plugin, "nombre", None) == "Web"


def test_obtener_plugin_por_defecto_o_palabra_clave(servicio: PluginsService):
    # Coincidencia con materia por defecto
    plugin_cisco = servicio.obtener_plugin("Tecnologías de Conmutación I")
    assert plugin_cisco is not None
    assert getattr(plugin_cisco, "nombre", None) == "Cisco"

    # Coincidencia por palabra clave
    plugin_iot = servicio.obtener_plugin("Taller de IoT y Sensores")
    assert plugin_iot is not None
    assert getattr(plugin_iot, "nombre", None) == "NodeRed"

    # Materia desconocida
    assert servicio.obtener_plugin("Historia Universal") is None


def test_actualizar_plugin_con_carpeta_override(servicio: PluginsService):
    carpeta = "/material/mis_redes"
    res = servicio.actualizar_plugin("cisco", carpeta_override=carpeta)
    assert carpeta in res
    cisco_plugin = servicio.plugins["cisco"]
    assert cisco_plugin.carpeta_analizada == carpeta
