"""Tests unitarios para servicios auxiliares: Configuración, Materias y Telemetría."""

from __future__ import annotations

from modular_learning.core.application.configuracion import ConfiguracionService
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.telemetria import TelemetriaService
from tests.unit.application.fake_adapters import (
    InMemoryAjustesPort,
    InMemoryCronogramaRepo,
    InMemoryMateriaRepo,
    InMemoryRegistroMaterialesRepo,
)


def test_configuracion_service():
    ajustes_port = InMemoryAjustesPort(carpeta_mat="/mat", ruta_bov="/bov")
    service = ConfiguracionService(ajustes_port)

    assert service.esta_configurado() is True
    assert service.carpeta_material() == "/mat"
    assert service.ruta_boveda() == "/bov"

    service.guardar_ajustes("/nueva_mat", "/nueva_bov")
    assert service.carpeta_material() == "/nueva_mat"
    assert service.ruta_boveda() == "/nueva_bov"


def test_materias_service():
    materia_repo = InMemoryMateriaRepo(["Redes", "IoT"])
    cronograma_repo = InMemoryCronogramaRepo({"Redes": [{"tema": "Tema 1", "estado": "pendiente"}]})
    registro_repo = InMemoryRegistroMaterialesRepo()
    registro_repo.registrar_material("guia.pdf", "Redes")
    service = MateriasService(materia_repo, cronograma_repo, registro_repo)

    assert service.listar_materias() == ["Redes", "IoT"]
    actualizadas = service.agregar_materia("Web")
    assert "Web" in actualizadas

    # Catálogo estructurado
    catalogo = service.listar_catalogo()
    assert any(m["slug"] == "redes" and m["nombre"] == "Redes" for m in catalogo)

    # Renombrar materia (mantiene slug)
    m = service.renombrar_materia("redes", "Redes de Datos II")
    assert m.slug == "redes"
    assert m.nombre == "Redes de Datos II"
    assert service.obtener_materia("redes").nombre == "Redes de Datos II"

    proximas = service.obtener_proximas_clases("Redes")
    assert len(proximas) == 1
    assert proximas[0]["tema"] == "Tema 1"
    clase_id = proximas[0]["id"]

    # Editar clase
    service.editar_clase("Redes", clase_id, {"tema": "Tema 1 Modificado"})
    assert service.obtener_cronograma("Redes")[0]["tema"] == "Tema 1 Modificado"

    # Cambiar estado
    service.cambiar_estado_clase("Redes", clase_id, "completado")
    assert service.obtener_cronograma("Redes")[0]["estado"] == "completado"

    # Añadir clase manual
    nueva = service.agregar_clase("Redes", {"tema": "Tema Nuevo", "fecha": "20/11/2026"})
    assert nueva["id"]
    assert len(service.obtener_cronograma("Redes")) == 2

    # Eliminar clase
    service.eliminar_clase("Redes", clase_id)
    assert len(service.obtener_cronograma("Redes")) == 1
    assert service.obtener_cronograma("Redes")[0]["id"] == nueva["id"]

    # Parciales
    service.guardar_parciales("Redes", [{"nombre": "Parcial 1", "hasta": nueva["id"]}])
    parciales = service.obtener_parciales("Redes")
    assert len(parciales) == 1
    assert parciales[0]["nombre"] == "Parcial 1"

    # Eliminar materia en cascada
    assert service.eliminar_materia("redes", borrar_cronograma=True) is True
    assert service.obtener_materia("redes") is None
    assert service.obtener_cronograma("redes") is None
    assert not registro_repo.verificar_material_ingestado("guia.pdf")


def test_telemetria_service():
    cronograma_repo = InMemoryCronogramaRepo(
        {
            "ingenieria-de-software-ii": [
                {"tema": "Tema 1", "estado": "completado"},
                {"tema": "Tema 2", "estado": "pendiente"},
            ]
        }
    )
    # Sin catálogo: la clave es el slug
    service_sin = TelemetriaService(cronograma_repo)
    stats_sin = service_sin.obtener_estadisticas()
    assert stats_sin["total_temas"] == 2
    assert stats_sin["temas_completados"] == 1
    assert stats_sin["porcentaje_global"] == 50.0
    assert "ingenieria-de-software-ii" in stats_sin["materias"]

    # Con catálogo: la clave usa el nombre del catálogo
    materia_repo = InMemoryMateriaRepo(["Ingeniería de Software II"])
    service_con = TelemetriaService(cronograma_repo, materia_repo=materia_repo)
    stats_con = service_con.obtener_estadisticas()
    assert "Ingeniería de Software II" in stats_con["materias"]


def test_eliminar_materia_elimina_proyectos_asociados():
    from modular_learning.core.domain.proyectos import Proyecto
    from tests.unit.application.fake_adapters import InMemoryProyectosRepo

    materia_repo = InMemoryMateriaRepo(["Redes", "IoT"])
    proyectos_repo = InMemoryProyectosRepo(
        [
            Proyecto(
                id="redes--app1",
                nombre="App Redes",
                materia="Redes",
                parcial="primer_parcial",
                tipo="software",
                ruta_origen="/rutas/app1",
                ruta_nota_obsidian="Redes/Proyectos/App.md",
                fecha_analisis="2026-10-01T10:00:00",
                mtime_archivos=1000.0,
                total_archivos=1,
                hash_estado="abc",
            ),
            Proyecto(
                id="iot--sensor",
                nombre="Sensor IoT",
                materia="IoT",
                parcial="segundo_parcial",
                tipo="iot",
                ruta_origen="/rutas/sensor",
                ruta_nota_obsidian="IoT/Proyectos/Sensor.md",
                fecha_analisis="2026-10-01T10:00:00",
                mtime_archivos=1000.0,
                total_archivos=1,
                hash_estado="def",
            ),
        ]
    )

    service = MateriasService(materia_repo, proyectos_repo=proyectos_repo)
    assert len(proyectos_repo.listar("redes")) == 1
    assert len(proyectos_repo.listar("iot")) == 1

    assert service.eliminar_materia("redes") is True
    assert proyectos_repo.listar("redes") == []
    # Los proyectos de otras materias se mantienen intactos
    assert len(proyectos_repo.listar("iot")) == 1
