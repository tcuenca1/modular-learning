"""Configuración global de fixtures para pytest."""

import pytest


@pytest.fixture(autouse=True)
def _hosts_de_prueba(monkeypatch):
    """El TestClient de Starlette usa el host `testserver`; el API solo acepta los configurados."""
    monkeypatch.setenv("ML_HOSTS_PERMITIDOS", "testserver,localhost")
