"""P30: validación de nombres y existencia de asignaturas en MateriasService."""

from __future__ import annotations

import pytest

from modular_learning.core.application.materias import MateriasService
from modular_learning.core.domain.materias import (
    LONGITUD_MAXIMA_NOMBRE,
    MateriaDuplicada,
    MateriaNoEncontrada,
    NombreMateriaInvalido,
    validar_nombre_materia,
)
from tests.unit.application.fake_adapters import InMemoryCronogramaRepo, InMemoryMateriaRepo


def _servicio(materias: list[str] | None = None) -> MateriasService:
    return MateriasService(
        InMemoryMateriaRepo(materias or ["Redes de Datos"]), InMemoryCronogramaRepo()
    )


@pytest.mark.parametrize(
    "nombre",
    [
        "",
        "   ",
        "!!!",
        "😀",
        "a/b",
        "a\\b",
        "..",
        "Redes..II",
        "Redes\x00",
        "Redes\x07II",
        "x" * (LONGITUD_MAXIMA_NOMBRE + 1),
        "x" * 20_000_000,
        "- - -",
    ],
)
def test_crear_materia_rechaza_nombres_invalidos(nombre):
    servicio = _servicio()
    with pytest.raises(NombreMateriaInvalido):
        servicio.crear_materia(nombre)
    assert servicio.listar_materias() == ["Redes de Datos"]


def test_crear_materia_acepta_nombre_normal_y_normaliza_espacios():
    servicio = _servicio()
    materia = servicio.crear_materia("  Cálculo   II (Avanzado) ")
    assert materia.nombre == "Cálculo II (Avanzado)"
    assert materia.slug == "calculo-ii-avanzado"
    assert "Cálculo II (Avanzado)" in servicio.listar_materias()


def test_crear_materia_acepta_longitud_maxima():
    nombre = "x" * LONGITUD_MAXIMA_NOMBRE
    assert validar_nombre_materia(nombre) == nombre


@pytest.mark.parametrize("duplicado", ["redes de datos", "REDES DE DATOS", "Redes  de  Datos"])
def test_crear_materia_rechaza_duplicados_sin_tildes_ni_mayusculas(duplicado):
    servicio = _servicio()
    with pytest.raises(MateriaDuplicada):
        servicio.crear_materia(duplicado)
    assert len(servicio.listar_catalogo()) == 1


def test_duplicado_sin_tildes():
    servicio = _servicio(["Ingeniería de Software"])
    with pytest.raises(MateriaDuplicada):
        servicio.crear_materia("INGENIERIA DE SOFTWARE")


def test_renombrar_materia_inexistente_no_la_crea():
    servicio = _servicio()
    with pytest.raises(MateriaNoEncontrada):
        servicio.renombrar_materia("fantasma", "Fantasma")
    assert servicio.listar_materias() == ["Redes de Datos"]


def test_renombrar_valida_el_nombre_y_los_duplicados():
    servicio = _servicio(["Redes de Datos", "Fisica"])
    with pytest.raises(NombreMateriaInvalido):
        servicio.renombrar_materia("fisica", "a/b")
    with pytest.raises(MateriaDuplicada):
        servicio.renombrar_materia("fisica", "redes de datos")
    # Corregir tildes o mayúsculas de la propia asignatura sí se permite
    assert servicio.renombrar_materia("fisica", "Física").nombre == "Física"


def test_agregar_clase_a_materia_inexistente_falla_y_no_crea_cronograma():
    servicio = _servicio()
    with pytest.raises(MateriaNoEncontrada):
        servicio.agregar_clase("fantasma", {"tema": "T"})
    assert servicio.listar_cronogramas() == {}


def test_guardar_parciales_en_materia_inexistente_falla():
    servicio = _servicio()
    with pytest.raises(MateriaNoEncontrada):
        servicio.guardar_parciales("fantasma", [{"nombre": "P1", "hasta": "x"}])
    assert servicio.obtener_parciales("fantasma") == []


def test_agregar_clase_y_parciales_en_materia_existente():
    servicio = _servicio()
    clase = servicio.agregar_clase("redes-de-datos", {"tema": "Capa 2"})
    servicio.guardar_parciales("Redes de Datos", [{"nombre": "P1", "hasta": clase["id"]}])
    assert servicio.obtener_parciales("redes-de-datos")[0]["hasta"] == clase["id"]
