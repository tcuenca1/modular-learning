"""Tests unitarios para ConfiguracionService, MateriasService, TelemetriaService y PluginsService."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from modular_learning.core.application.configuracion import ConfiguracionService
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.application.telemetria import TelemetriaService
from tests.unit.application.fake_adapters import (
    InMemoryAjustesPort,
    InMemoryCronogramaRepo,
    InMemoryMateriaRepo,
)


def test_configuracion_service():
    ajustes = InMemoryAjustesPort(carpeta_mat="/mat", ruta_bov="/bov", configurado=True)
    service = ConfiguracionService(ajustes)

    assert service.esta_configurado() is True
    assert service.carpeta_material() == "/mat"
    assert service.ruta_boveda() == "/bov"

    service.guardar_ajustes("/nueva_mat", "/nueva_bov")
    assert service.carpeta_material() == "/nueva_mat"
    assert service.ruta_boveda() == "/nueva_bov"


def test_materias_service():
    materia_repo = InMemoryMateriaRepo(["Redes", "IoT"])
    cronograma_repo = InMemoryCronogramaRepo(
        {"Redes": [{"tema": "Tema 1", "estado": "pendiente"}]}
    )
    service = MateriasService(materia_repo, cronograma_repo)

    assert service.listar_materias() == ["Redes", "IoT"]
    actualizadas = service.agregar_materia("Web")
    assert "Web" in actualizadas

    proximas = service.obtener_proximas_clases("Redes")
    assert len(proximas) == 1
    assert proximas[0]["tema"] == "Tema 1"


def test_telemetria_service(tmp_path):
    schedules_dir = tmp_path / "schedules"
    schedules_dir.mkdir()

    cronograma_data = {
        "clases": [
            {"tema": "Tema 1", "estado": "completado"},
            {"tema": "Tema 2", "estado": "pendiente"},
        ]
    }
    (schedules_dir / "redes_cronograma.json").write_text(
        json.dumps(cronograma_data), encoding="utf-8"
    )

    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    service = TelemetriaService(
        carpeta_schedules=str(schedules_dir),
        carpeta_plugins=str(plugins_dir),
    )

    stats = service.obtener_estadisticas()
    assert stats["total_temas"] == 2
    assert stats["temas_completados"] == 1
    assert stats["porcentaje_global"] == 50.0
    assert "Redes" in stats["materias"]


def test_plugins_service():
    mock_plugin = MagicMock()
    mock_plugin.cargar_contexto_reciente.return_value = "Memoria de Cisco."

    service = PluginsService(plugins={"cisco": mock_plugin})

    # Enrutamiento de plugin por materia
    plugin_hallado = service.obtener_plugin("Conmutación y Redes Cisco")
    assert plugin_hallado is mock_plugin

    plugin_no_hallado = service.obtener_plugin("Filosofía")
    assert plugin_no_hallado is None

    # Actualización de plugin
    resultado = service.actualizar_plugin("Cisco (Actividades)")
    assert "Memoria de Cisco." in resultado
