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
            "redes": [
                {"tema": "Tema 1", "estado": "completado"},
                {"tema": "Tema 2", "estado": "pendiente"},
            ]
        }
    )
    service = TelemetriaService(cronograma_repo)
    stats = service.obtener_estadisticas()

    assert stats["total_temas"] == 2
    assert stats["temas_completados"] == 1
    assert stats["porcentaje_global"] == 50.0
    assert "Redes" in stats["materias"]
