"""Configuración global de fixtures para pytest."""

import pytest

from modular_learning import bootstrap


@pytest.fixture(autouse=True)
def setup_test_container():
    """Garantiza que el contenedor de dependencias esté inicializado en cada test."""
    container = bootstrap.build_container()
    return container
