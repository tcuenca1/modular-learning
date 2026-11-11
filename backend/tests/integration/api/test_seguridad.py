"""P33: cabeceras de seguridad, validación de Host, documentación de la API y compresión."""

from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

from modular_learning import bootstrap
from modular_learning.apps.api.main import RUTA_ESTATICOS, create_app
from modular_learning.apps.api.seguridad import CABECERAS_SEGURIDAD, hosts_permitidos

requiere_build = pytest.mark.skipif(
    not (RUTA_ESTATICOS / "assets").exists(), reason="el frontend no está compilado"
)


@pytest.fixture
def crear_cliente(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))

    def _crear() -> TestClient:
        return TestClient(create_app(bootstrap.build_container()))

    return _crear


def test_toda_respuesta_lleva_las_cabeceras_de_seguridad(crear_cliente):
    cliente = crear_cliente()
    for ruta in ("/", "/api/materias", "/api/salud", "/ruta-spa-cualquiera"):
        r = cliente.get(ruta)
        for nombre, valor in CABECERAS_SEGURIDAD.items():
            assert r.headers[nombre] == valor, (ruta, nombre)
    assert r.headers["x-content-type-options"] == "nosniff"
    assert r.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in r.headers["content-security-policy"]
    assert "strict-transport-security" not in r.headers


def test_csp_permite_lo_que_usa_el_build(crear_cliente):
    csp = crear_cliente().get("/").headers["content-security-policy"]
    assert "script-src 'self'" in csp and "'unsafe-inline'" not in csp.split("style-src")[0]
    assert "https://fonts.googleapis.com" in csp and "https://fonts.gstatic.com" in csp


def test_hsts_solo_en_la_nube(crear_cliente, monkeypatch):
    monkeypatch.setenv("ML_EN_NUBE", "1")
    assert "max-age" in crear_cliente().get("/").headers["strict-transport-security"]


def test_host_no_permitido_da_400_pero_el_healthcheck_pasa(crear_cliente):
    cliente = crear_cliente()
    assert cliente.get("/api/materias", headers={"Host": "evil.example"}).status_code == 400
    assert cliente.get("/", headers={"Host": "evil.example"}).status_code == 400
    assert cliente.get("/api/salud", headers={"Host": "evil.example"}).status_code == 200
    assert cliente.get("/api/materias", headers={"Host": "localhost:8000"}).status_code == 200


def test_hosts_configurables_por_entorno(monkeypatch):
    monkeypatch.setenv("ML_HOSTS_PERMITIDOS", "mi.app, otra.app")
    monkeypatch.setenv("RENDER_EXTERNAL_HOSTNAME", "svc.onrender.com")
    assert hosts_permitidos() == ["mi.app", "otra.app", "svc.onrender.com"]
    monkeypatch.delenv("ML_HOSTS_PERMITIDOS")
    monkeypatch.delenv("RENDER_EXTERNAL_HOSTNAME")
    assert hosts_permitidos() == ["localhost", "127.0.0.1"]


def test_documentacion_de_la_api_solo_fuera_de_la_nube(crear_cliente, monkeypatch):
    local = crear_cliente()
    assert all(local.get(r).status_code == 200 for r in ("/docs", "/redoc", "/openapi.json"))
    monkeypatch.setenv("ML_EN_NUBE", "1")
    nube = crear_cliente()
    assert all(nube.get(r).status_code == 404 for r in ("/docs", "/redoc", "/openapi.json"))
    assert nube.get("/api/materias").status_code == 200


@requiere_build
def test_assets_comprimidos_y_con_cache_larga(crear_cliente):
    cliente = crear_cliente()
    html = cliente.get("/")
    assert html.headers["cache-control"] == "no-cache"
    js = re.search(r'/assets/[^"]+\.js', html.text).group(0)
    r = cliente.get(js, headers={"Accept-Encoding": "gzip"})
    assert r.status_code == 200
    assert r.headers["content-encoding"] == "gzip"
    assert r.headers["cache-control"] == "public, max-age=31536000, immutable"
    assert "/assets/" not in cliente.get("/api/materias").headers.get("cache-control", "")


def test_los_eventos_sse_no_se_comprimen(app_con_stream):
    r = app_con_stream.get("/api/prueba-sse", headers={"Accept-Encoding": "gzip"})
    assert "content-encoding" not in r.headers
    assert "data: hola" in r.text


@pytest.fixture
def app_con_stream(crear_cliente):
    from fastapi.responses import StreamingResponse
    from fastapi.routing import APIRoute

    cliente = crear_cliente()

    def prueba_sse() -> StreamingResponse:
        return StreamingResponse(iter(["data: hola\n\n" * 200]), media_type="text/event-stream")

    # Antes del comodín de la SPA, que si no respondería 404
    cliente.app.router.routes.insert(0, APIRoute("/api/prueba-sse", prueba_sse))
    return cliente
