from __future__ import annotations

import pytest

from modular_learning.core.application.proyectos import ProyectosService
from modular_learning.core.domain.proyectos import HuellaProyecto
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryBovedaPort,
    InMemoryInspectorProyectos,
    InMemoryLectorDocumentosPort,
    InMemoryProyectosRepo,
    InMemoryRegistroMaterialesRepo,
)

RUTA = "/material/Programacion Web/PROYECTOS/PRIMER PARCIAL/mi_app"


@pytest.fixture
def inspector():
    inspector = InMemoryInspectorProyectos()
    inspector.proyectos[RUTA] = ("software", HuellaProyecto(1000.0, 1, "abc"))
    return inspector


@pytest.fixture
def boveda():
    return InMemoryBovedaPort()


@pytest.fixture
def servicio(inspector, boveda):
    return ProyectosService(
        proyectos_repo=InMemoryProyectosRepo(),
        registro_repo=InMemoryRegistroMaterialesRepo(),
        boveda_port=boveda,
        lector_docs=InMemoryLectorDocumentosPort(),
        llm=FakeLLM(),
        inspector=inspector,
    )


def test_escanear_añade_la_materia_a_cada_candidato(servicio, inspector):
    inspector.candidatos["/material/IoT"] = [
        {"parcial": "primer_parcial", "nombre": "A07", "ruta": "/x/A07", "tipo": "iot"}
    ]
    detectados = servicio.escanear_proyectos_en_carpeta("IoT", "/material/IoT")
    assert detectados == [
        {
            "materia": "IoT",
            "parcial": "primer_parcial",
            "nombre": "A07",
            "ruta": "/x/A07",
            "tipo": "iot",
        }
    ]


def test_analizar_e_ingestar_y_trazabilidad(servicio, inspector, boveda):
    proyecto = servicio.analizar_e_ingestar_proyecto(
        materia="Programacion Web",
        nombre_proyecto="mi_app",
        parcial="primer_parcial",
        ruta_origen=RUTA,
    )

    assert proyecto.tipo == "software"
    assert proyecto.id == "programacion-web--primer-parcial--mi-app"
    assert len(boveda.notas) == 1
    assert "tipo_proyecto: software" in next(iter(boveda.notas.values()))
    assert servicio.verificar_estado_proyecto(proyecto.id)["estado"] == "al_dia"

    inspector.proyectos[RUTA] = ("software", HuellaProyecto(1010.0, 2, "def"))
    estado = servicio.verificar_estado_proyecto(proyecto.id)
    assert estado["estado"] == "cambios_detectados"
    assert servicio.actualizar_proyecto(proyecto.id).total_archivos == 2

    del inspector.proyectos[RUTA]
    assert servicio.verificar_estado_proyecto(proyecto.id)["estado"] == "carpeta_eliminada"


def test_ingestar_proyecto_inexistente_falla(servicio):
    with pytest.raises(ValueError):
        servicio.analizar_e_ingestar_proyecto("Web", "nada", "general", "/no/existe")


def test_vaciar_proyectos_borra_sus_fichas(servicio, boveda):
    servicio.analizar_e_ingestar_proyecto("Programacion Web", "mi_app", "primer_parcial", RUTA)
    assert servicio.vaciar_proyectos() == 1
    assert boveda.notas == {}
    assert servicio.listar_proyectos() == []
