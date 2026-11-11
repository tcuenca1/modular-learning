"""P31: comprobaciones léxicas de rutas recibidas del cliente."""

from __future__ import annotations

import pytest

from modular_learning.core.domain.rutas import esta_dentro, unir_dentro


@pytest.mark.parametrize(
    ("ruta", "esperado"),
    [
        ("/uni", True),
        ("/uni/Redes", True),
        ("/uni/Redes/../IoT", True),
        ("/uni/../etc", False),
        ("/unix", False),
        ("/otra", False),
        ("relativa", False),
        ("", False),
        ("/uni/a\x00b", False),
    ],
)
def test_esta_dentro(ruta, esperado):
    assert esta_dentro("/uni", ruta) is esperado


def test_esta_dentro_excluye_la_base_si_se_pide():
    assert esta_dentro("/uni", "/uni", incluir_base=False) is False
    assert esta_dentro("/uni", "/uni/", incluir_base=True) is True


@pytest.mark.parametrize(
    "materia", ["..", "../..", "../fuera", "Redes/../..", "/etc", "", ".", "Redes\x00"]
)
def test_unir_dentro_rechaza_escapes(materia):
    assert unir_dentro("/uni", materia) is None


def test_unir_dentro_acepta_subcarpetas():
    assert unir_dentro("/uni", "Redes") == "/uni/Redes"
    assert unir_dentro("/uni", "Redes", "Labs") == "/uni/Redes/Labs"
