"""PluginsService con plugins falsos: el servicio solo usa lo declarado en el puerto."""

from __future__ import annotations

import pytest

from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.ports.plugin_practico import PluginMetadatos
from tests.unit.application.fake_adapters import (
    FakePluginPractico,
    InMemoryAjustesPort,
    InMemoryLectorDocumentosPort,
    InMemoryPluginConfigRepo,
)

BASE = "/material"
BOVEDA = "/boveda"


def _meta(id_: str, **extra) -> PluginMetadatos:
    base = {
        "id": id_,
        "nombre": f"Plugin {id_}",
        "opcion_key": f"{id_.title()} (Opción)",
        "categoria": f"Categoría {id_}",
        "descripcion": f"Descripción de {id_}",
        "materia_defecto": f"asignatura-{id_}",
        "claves_seleccion": (id_,),
        "palabras_clave": (f"clave{id_}",),
        "carpeta_convencional": f"Carpeta {id_}",
        "etiqueta": id_.title(),
        "texto_sin_contexto": f"Sin nada en {id_}.",
    }
    return PluginMetadatos(**{**base, **extra})


@pytest.fixture
def lector() -> InMemoryLectorDocumentosPort:
    lector = InMemoryLectorDocumentosPort()
    lector.carpetas.add("/material/mis_labs")
    return lector


@pytest.fixture
def plugins() -> dict[str, FakePluginPractico]:
    return {
        "alfa": FakePluginPractico(_meta("alfa", orden_sincronizacion=1, limite_contexto=10)),
        "beta": FakePluginPractico(
            _meta("beta", orden_sincronizacion=0, extension_archivos=".json")
        ),
        "gama": FakePluginPractico(
            _meta(
                "gama",
                orden_sincronizacion=2,
                titulo_carpeta_asignada="Proyecto Asignado",
                titulo_carpeta_convencional="Proyecto Convencional",
                titulo_sincronizacion="Sincronización de Gama",
            ),
            analiza_archivos=False,
        ),
    }


@pytest.fixture
def servicio(plugins, lector) -> PluginsService:
    return PluginsService(
        plugins=plugins,
        ajustes_port=InMemoryAjustesPort(carpeta_mat=BASE, ruta_bov=BOVEDA),
        carpeta_plugins="/memoria",
        lector_docs=lector,
        config_repo=InMemoryPluginConfigRepo(),
    )


def test_listar_info_plugins_sale_de_los_metadatos(servicio, plugins):
    plugins["alfa"].contexto = "memoria alfa"
    servicio.guardar_configuracion_plugin("beta", materia="otra-asignatura")
    info = {p["id"]: p for p in servicio.listar_info_plugins()}
    assert set(info) == {"alfa", "beta", "gama"}
    assert info["alfa"]["nombre"] == "Plugin alfa"
    assert info["alfa"]["opcion_key"] == "Alfa (Opción)"
    assert info["alfa"]["categoria"] == "Categoría alfa"
    assert info["alfa"]["materia"] == "asignatura-alfa"
    assert info["alfa"]["contexto_reciente"] == "memoria alfa"
    assert info["beta"]["materia"] == "otra-asignatura"


def test_guardar_y_obtener_configuracion(servicio, lector):
    res = servicio.guardar_configuracion_plugin(
        "ALFA", carpeta="/material/mis_labs", materia="laboratorio"
    )
    assert res == {"carpeta": "/material/mis_labs", "materia": "laboratorio"}
    assert servicio.obtener_configuraciones()["alfa"]["carpeta"] == "/material/mis_labs"
    info = {p["id"]: p for p in servicio.listar_info_plugins()}
    assert info["alfa"]["carpeta_existe"] is True
    assert info["beta"]["carpeta_existe"] is False


def test_obtener_plugin_por_materia_configurada(servicio, plugins):
    servicio.guardar_configuracion_plugin("gama", materia="desarrollo-fullstack")
    assert servicio.obtener_plugin("Desarrollo Fullstack") is plugins["gama"]


def test_obtener_plugin_por_materia_por_defecto_y_por_palabra_clave(servicio, plugins):
    assert servicio.obtener_plugin("Asignatura Beta") is plugins["beta"]
    assert servicio.obtener_plugin("Taller de clavegama avanzado") is plugins["gama"]
    assert servicio.obtener_plugin("Historia Universal") is None


def test_palabras_clave_respetan_el_orden_de_registro(plugins):
    servicio = PluginsService(plugins={"gama": plugins["gama"], "alfa": plugins["alfa"]})
    # Ambas claves aparecen: gana el primer plugin registrado
    assert servicio.obtener_plugin("clavealfa clavegama") is plugins["gama"]


def test_actualizar_con_carpeta_override(servicio, plugins):
    res = servicio.actualizar_plugin("alfa", carpeta_override="/material/mis_labs")
    assert res == (
        "### [Alfa] Carpeta Asignada: `/material/mis_labs`\n"
        "Carpeta /material/mis_labs analizada por alfa"
    )
    assert plugins["alfa"].carpetas_analizadas == ["/material/mis_labs"]
    assert plugins["beta"].carpetas_analizadas == []


def test_actualizar_usa_la_carpeta_configurada(servicio, plugins):
    servicio.guardar_configuracion_plugin("gama", carpeta="/material/mis_labs")
    res = servicio.actualizar_plugin("Gama (Opción)")
    assert res.startswith("### [Gama] Proyecto Asignado: `/material/mis_labs`")
    assert plugins["gama"].carpetas_analizadas == ["/material/mis_labs"]


def test_actualizar_usa_la_carpeta_convencional(servicio, plugins, lector):
    lector.carpetas.add("/material/Carpeta alfa")
    res = servicio.actualizar_plugin("alfa")
    assert res.startswith("### [Alfa] Carpeta de Materia: `/material/Carpeta alfa`")
    assert plugins["alfa"].carpetas_analizadas == ["/material/Carpeta alfa"]

    lector.carpetas.add("/material/Carpeta gama")
    assert servicio.actualizar_plugin("gama").startswith(
        "### [Gama] Proyecto Convencional: `/material/Carpeta gama`"
    )


def test_actualizar_con_extension_analiza_hasta_tres_archivos(servicio, plugins, lector):
    for nombre in ("a.json", "b.json", "c.json", "d.json", "beta_memoria.json", "x.txt"):
        lector.materiales[f"/material/Carpeta beta/{nombre}"] = "{}"
    lector.materiales["/boveda/Carpeta beta/e.json"] = "{}"
    res = servicio.actualizar_plugin("beta")
    assert plugins["beta"].archivos_analizados == [
        "/material/Carpeta beta/a.json",
        "/material/Carpeta beta/b.json",
        "/material/Carpeta beta/c.json",
    ]
    assert res.count("### [Beta] Archivo: ") == 3


def test_actualizar_sin_nada_cae_a_la_memoria_del_plugin(servicio, plugins):
    assert servicio.actualizar_plugin("beta") == (
        "### [Beta] Sincronización\nContexto activo:\nSin nada en beta."
    )
    plugins["alfa"].contexto = "0123456789ABCDEF"
    # `limite_contexto` recorta la memoria que se muestra
    assert servicio.actualizar_plugin("alfa").endswith("Contexto activo:\n0123456789")
    assert "Sincronización de Gama" in servicio.actualizar_plugin("gama")


def test_extension_con_plugin_que_no_analiza_archivos_cae_a_la_memoria(servicio, plugins, lector):
    plugins["beta"].analiza_archivos = False
    lector.materiales["/material/Carpeta beta/a.json"] = "{}"
    res = servicio.actualizar_plugin("beta")
    assert plugins["beta"].archivos_analizados == []
    assert "Contexto activo:" in res


def test_todos_sincroniza_en_el_orden_declarado_por_los_plugins(servicio):
    res = servicio.actualizar_plugin("Todos")
    orden = [res.index(f"### [{e}]") for e in ("Beta", "Alfa", "Gama")]
    assert orden == sorted(orden)


def test_seleccion_desconocida_avisa(servicio):
    assert servicio.actualizar_plugin("nada").startswith("⚠️ No se encontró contenido")


def test_procesar_archivo_plugin(servicio, plugins):
    servicio_con_tipos = PluginsService(
        plugins={
            "beta": FakePluginPractico(_meta("beta", tipos_archivo=("tipob", "otro"))),
            "gama": FakePluginPractico(
                _meta("gama", tipos_archivo=("tipog",)), analiza_archivos=False
            ),
        }
    )
    assert servicio_con_tipos.procesar_archivo_plugin("/x/a.json", "TipoB") == (
        "Archivo /x/a.json analizado por beta"
    )
    assert "no soporta el análisis de archivos" in servicio_con_tipos.procesar_archivo_plugin(
        "/x/a.txt", "tipog"
    )
    assert "Tipo de plugin no soportado" in servicio_con_tipos.procesar_archivo_plugin("/x", "zzz")
    assert "Tipo de plugin no soportado" in servicio.procesar_archivo_plugin("/x", "tipob")


def test_registrar_plugin_agrega_al_catalogo(servicio):
    nuevo = FakePluginPractico(_meta("delta"))
    servicio.registrar_plugin("DELTA", nuevo)
    assert servicio.plugins["delta"] is nuevo
    assert servicio.obtener_plugin("Asignatura Delta") is nuevo
