"""P32: altas, ediciones y bajas de clase pasan por `actualizar_cronograma` del puerto."""

from __future__ import annotations

import pytest

from modular_learning.core.application.materias import MateriasService
from tests.unit.application.fake_adapters import InMemoryCronogramaRepo, InMemoryMateriaRepo


def _servicio() -> tuple[MateriasService, InMemoryCronogramaRepo]:
    crono = InMemoryCronogramaRepo()
    return MateriasService(InMemoryMateriaRepo(["Redes"]), crono), crono


def test_actualizar_cronograma_propaga_el_error_de_la_transformacion():
    _, crono = _servicio()

    def falla(clases):
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        crono.actualizar_cronograma("Redes", falla)
    assert crono.obtener_cronograma("Redes") is None


def test_editar_clase_inexistente_no_toca_el_cronograma():
    servicio, crono = _servicio()
    servicio.agregar_clase("Redes", {"tema": "A"})
    with pytest.raises(LookupError):
        servicio.editar_clase("Redes", "no-existe", {"tema": "X"})
    assert [c["tema"] for c in crono.obtener_cronograma("Redes")] == ["A"]


def test_agregar_editar_y_eliminar_clase():
    servicio, crono = _servicio()
    clase = servicio.agregar_clase("Redes", {"tema": "ARP"})
    assert clase["estado"] == "pendiente" and clase["id"]
    editada = servicio.editar_clase("Redes", clase["id"], {"tema": "ARP y NDP", "id": "otro"})
    assert editada["tema"] == "ARP y NDP" and editada["id"] == clase["id"]
    assert servicio.eliminar_clase("Redes", clase["id"]) is True
    assert servicio.eliminar_clase("Redes", clase["id"]) is False
    assert crono.obtener_cronograma("Redes") == []


def test_editar_clase_sin_cronograma_falla_y_no_lo_crea():
    servicio, crono = _servicio()
    with pytest.raises(LookupError):
        servicio.editar_clase("Redes", "x", {"tema": "T"})
    assert crono.obtener_cronograma("Redes") is None
