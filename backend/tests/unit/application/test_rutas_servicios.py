"""P31: los casos de uso no aceptan rutas ni asignaturas que se salgan de la carpeta base."""

from __future__ import annotations

import pytest

from modular_learning.core.application.ingesta import IngestaService
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.application.proyectos import ProyectosService
from modular_learning.core.domain.materias import NombreMateriaInvalido
from modular_learning.core.domain.proyectos import HuellaProyecto
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryAjustesPort,
    InMemoryBovedaPort,
    InMemoryCronogramaRepo,
    InMemoryInspectorProyectos,
    InMemoryLectorDocumentosPort,
    InMemoryMateriaRepo,
    InMemoryPluginConfigRepo,
    InMemoryProyectosRepo,
    InMemoryRegistroMaterialesRepo,
)

BASE = "/material"


def test_escanear_materia_con_ruta_relativa_no_lee_fuera_de_la_base():
    lector = InMemoryLectorDocumentosPort()
    lector.materiales["/secreto/clave.pdf"] = "x"
    lector.materiales["/material/Redes/a.pdf"] = "x"
    servicio = IngestaService(
        llm=FakeLLM(),
        registro_repo=InMemoryRegistroMaterialesRepo(),
        boveda_port=InMemoryBovedaPort(),
        lector_docs=lector,
        ajustes_port=InMemoryAjustesPort(carpeta_mat=BASE),
    )
    for malicioso in ["../secreto", "..", "../..", "/secreto", "Redes/../../secreto"]:
        escaneo = servicio.escanear_materia(malicioso)
        assert escaneo["existe"] is False
        assert escaneo["pendientes"] == []
        assert escaneo["carpeta"] == ""
    assert len(servicio.escanear_materia("Redes")["pendientes"]) == 1


def test_ingestar_proyecto_fuera_de_la_carpeta_base_falla():
    inspector = InMemoryInspectorProyectos()
    inspector.proyectos["/secreto/app"] = ("software", HuellaProyecto(1.0, 1, "h"))
    inspector.proyectos["/material/Web/app"] = ("software", HuellaProyecto(1.0, 1, "h"))
    servicio = ProyectosService(
        proyectos_repo=InMemoryProyectosRepo(),
        registro_repo=InMemoryRegistroMaterialesRepo(),
        boveda_port=InMemoryBovedaPort(),
        lector_docs=InMemoryLectorDocumentosPort(),
        llm=FakeLLM(),
        inspector=inspector,
    )
    for ruta in ["/secreto/app", "/material/../secreto/app"]:
        with pytest.raises(ValueError, match="dentro de la carpeta de material"):
            servicio.analizar_e_ingestar_proyecto("Web", "app", "general", ruta, carpeta_base=BASE)
    proyecto = servicio.analizar_e_ingestar_proyecto(
        "Web", "app", "general", "/material/Web/app", carpeta_base=BASE
    )
    assert proyecto.ruta_origen == "/material/Web/app"


def _plugins() -> PluginsService:
    return PluginsService(
        ajustes_port=InMemoryAjustesPort(carpeta_mat=BASE),
        config_repo=InMemoryPluginConfigRepo(),
        lector_docs=InMemoryLectorDocumentosPort(),
    )


def test_configurar_plugin_con_carpeta_fuera_de_la_base_falla():
    servicio = _plugins()
    for carpeta in ["/secreto", "/material/../secreto", "../x"]:
        with pytest.raises(ValueError, match="dentro de la carpeta de material"):
            servicio.guardar_configuracion_plugin("cisco", carpeta=carpeta)
    assert servicio.obtener_configuraciones() == {}
    ok = servicio.guardar_configuracion_plugin("cisco", carpeta="/material/Redes/labs")
    assert ok["carpeta"] == "/material/Redes/labs"
    # Vaciar la carpeta sigue permitido
    assert servicio.guardar_configuracion_plugin("cisco", carpeta="")["carpeta"] == ""


def test_actualizar_plugin_con_override_fuera_de_la_base_falla():
    with pytest.raises(ValueError, match="dentro de la carpeta de material"):
        _plugins().actualizar_plugin("nodered", "/secreto")


def test_validar_materia_recibida():
    servicio = MateriasService(InMemoryMateriaRepo(["Redes"]), InMemoryCronogramaRepo())
    servicio.validar_materia_recibida("redes")  # ya está en el catálogo
    servicio.validar_materia_recibida("Materia Nueva")  # válida aunque no exista
    for malo in ["../..", "a/b", "x" * 200]:
        with pytest.raises(NombreMateriaInvalido):
            servicio.validar_materia_recibida(malo)
