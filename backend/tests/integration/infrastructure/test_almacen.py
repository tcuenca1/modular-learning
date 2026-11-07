"""Tests del almacén de documentos y de los repositorios sobre él, en archivos y en Postgres.

Los casos de Postgres se ejecutan solo si ML_TEST_DATABASE_URL apunta a una base de pruebas
(por ejemplo `docker run -e POSTGRES_PASSWORD=prueba -p 5433:5432 postgres:16`); la tabla
`documentos` se vacía antes de cada test.
"""

from __future__ import annotations

import os

import pytest

from modular_learning.core.domain.guia_offline import ClaseGuia, GuiaOffline
from modular_learning.infrastructure.persistence.almacen import (
    AlmacenArchivos,
    AlmacenDocumentos,
    AlmacenPostgres,
    almacen_por_defecto,
)
from modular_learning.infrastructure.persistence.json_guias import JsonGuiasRepo
from modular_learning.infrastructure.persistence.json_repaso import JsonHistorialRepo
from modular_learning.infrastructure.persistence.json_repositorios import (
    JsonCronogramaRepo,
    JsonMateriaRepo,
)

URL_PRUEBAS = os.getenv("ML_TEST_DATABASE_URL", "")


@pytest.fixture(params=["archivos", "postgres"])
def almacen(request, tmp_path) -> AlmacenDocumentos:
    if request.param == "archivos":
        return AlmacenArchivos(tmp_path)
    if not URL_PRUEBAS:
        pytest.skip("ML_TEST_DATABASE_URL no configurada")
    almacen = AlmacenPostgres(URL_PRUEBAS)
    with almacen._pool.connection() as conn:
        conn.execute("TRUNCATE documentos")
    return almacen


def test_leer_escribir_y_listar(almacen):
    assert almacen.leer("schedules/X_cronograma.json") is None

    almacen.escribir("schedules/REDES_cronograma.json", "[1]")
    almacen.escribir("schedules/IOT_cronograma.json", "[2]")
    almacen.escribir("config/materias.txt", "Redes")
    almacen.escribir("schedules/REDES_cronograma.json", "[3]")

    assert almacen.leer("schedules/REDES_cronograma.json") == "[3]"
    assert almacen.listar("schedules/") == [
        "schedules/IOT_cronograma.json",
        "schedules/REDES_cronograma.json",
    ]
    # Los "_" del prefijo no son comodines
    assert almacen.listar("schedules/RED_") == []
    assert almacen.listar("nada/") == []


def test_repositorios_sobre_el_almacen(almacen):
    cronogramas = JsonCronogramaRepo(almacen=almacen)
    assert cronogramas.listar_cronogramas() == {}

    clave = cronogramas.guardar_cronograma("Redes II", [{"tema": "VLAN", "estado": "pendiente"}])
    assert clave == "schedules/Redes_II_cronograma.json"
    assert cronogramas.marcar_clase_completada("redes ii", "VLAN")
    clases = cronogramas.obtener_cronograma("REDES II")
    assert len(clases) == 1
    assert clases[0]["tema"] == "VLAN"
    assert clases[0]["estado"] == "completado"
    assert "id" in clases[0]
    assert list(cronogramas.listar_cronogramas()) == ["Redes II"]

    materias = JsonMateriaRepo(almacen=almacen)
    assert materias.cargar_materias() == JsonMateriaRepo.MATERIAS_INICIALES
    materias.agregar_materia("Redes II")
    assert JsonMateriaRepo(almacen=almacen).cargar_materias()[-1] == "Redes II"

    historial = JsonHistorialRepo(almacen=almacen)
    historial.registrar({"tipo": "guia", "materia": "Redes II", "tema": "VLAN"})
    assert historial.listar(materia="redes ii")[0]["tipo"] == "guia"

    guias = JsonGuiasRepo(almacen=almacen)
    guia = GuiaOffline("g1", "Redes II", "completa", "2026-10-26T08:00:00", [ClaseGuia("VLAN")])
    guias.guardar(guia)
    assert JsonGuiasRepo(almacen=almacen).obtener("g1") == guia


def test_almacen_por_defecto_usa_archivos_sin_database_url(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path))
    almacen = almacen_por_defecto()
    assert isinstance(almacen, AlmacenArchivos)
    almacen.escribir("config/materias.txt", "A")
    assert (tmp_path / "config" / "materias.txt").read_text(encoding="utf-8") == "A"
