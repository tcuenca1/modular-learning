"""P43: Server-Timing en cada respuesta y aviso de las peticiones lentas."""

from __future__ import annotations

import logging

from fastapi.testclient import TestClient

from modular_learning import bootstrap
from modular_learning.apps.api.main import create_app


def _cliente(tmp_path, monkeypatch, **env):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return TestClient(create_app(bootstrap.build_container()))


def test_server_timing_en_cada_respuesta(tmp_path, monkeypatch):
    r = _cliente(tmp_path, monkeypatch).get("/api/salud")
    assert r.headers["server-timing"].startswith("app;dur=")


def test_peticion_lenta_se_registra(tmp_path, monkeypatch, caplog):
    cliente = _cliente(tmp_path, monkeypatch, ML_UMBRAL_LENTA_MS="0")
    with caplog.at_level(logging.WARNING, logger="modular_learning.api"):
        cliente.get("/api/materias")
    assert "Petición lenta: GET /api/materias -> 200" in caplog.text


def test_peticion_rapida_no_se_registra(tmp_path, monkeypatch, caplog):
    cliente = _cliente(tmp_path, monkeypatch, ML_UMBRAL_LENTA_MS="60000")
    with caplog.at_level(logging.WARNING, logger="modular_learning.api"):
        cliente.get("/api/materias")
    assert "Petición lenta" not in caplog.text
