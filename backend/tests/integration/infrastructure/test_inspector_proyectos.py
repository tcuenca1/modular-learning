"""Tests de integración del inspector de proyectos en disco."""

from __future__ import annotations

import pytest

from modular_learning.infrastructure.documents.lector_documentos import LectorDocumentosLocal
from modular_learning.infrastructure.proyectos.inspector_local import InspectorProyectosLocal


@pytest.fixture
def inspector():
    return InspectorProyectosLocal(LectorDocumentosLocal())


def test_detectar_tipo(tmp_path, inspector):
    doc = tmp_path / "informe.docx"
    doc.write_text("dummy", encoding="utf-8")
    assert inspector.detectar_tipo(str(doc)) == "documento_rector"

    soft = tmp_path / "app_web"
    soft.mkdir()
    (soft / "package.json").write_text('{"name": "test"}', encoding="utf-8")
    assert inspector.detectar_tipo(str(soft)) == "software"

    iot = tmp_path / "iot_nodes"
    iot.mkdir()
    (iot / "flujo_temperatura.json").write_text('[{"type": "inject"}]', encoding="utf-8")
    assert inspector.detectar_tipo(str(iot)) == "iot"

    sgsi = tmp_path / "sgsi"
    sgsi.mkdir()
    (sgsi / "01_Base_Normativa").mkdir()
    assert inspector.detectar_tipo(str(sgsi)) == "documental_auditoria"


def test_huella_ignora_dependencias_y_secretos(tmp_path, inspector):
    (tmp_path / "index.js").write_text("hola", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRETO=1", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "lib.js").write_text("x", encoding="utf-8")

    huella = inspector.huella(str(tmp_path))
    assert huella is not None
    assert huella.total_archivos == 1
    assert huella.mtime > 0
    assert inspector.huella(str(tmp_path / "no_existe")) is None


def test_escanear_singular_y_plural(tmp_path, inspector):
    seguridad = tmp_path / "Seguridad"
    (seguridad / "PROYECTO" / "SGSI_ISP").mkdir(parents=True)

    iot = tmp_path / "IoT" / "PROYECTOS"
    (iot / "PRIMER PARCIAL" / "A07_Grupo8").mkdir(parents=True)
    (iot / "SEGUNDO PARCIAL" / "A08_Final").mkdir(parents=True)

    det_a = inspector.escanear(str(seguridad))
    assert [(d["nombre"], d["parcial"]) for d in det_a] == [("SGSI_ISP", "general")]

    det_b = {d["nombre"]: d["parcial"] for d in inspector.escanear(str(tmp_path / "IoT"))}
    assert det_b == {"A07_Grupo8": "primer_parcial", "A08_Final": "segundo_parcial"}
    assert inspector.escanear(str(tmp_path / "no_existe")) == []


def test_extraer_contexto_no_incluye_secretos(tmp_path, inspector):
    (tmp_path / "README.md").write_text("# Mi proyecto\nDescripción", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRETO=1", encoding="utf-8")
    contexto = inspector.extraer_contexto(str(tmp_path))
    assert "README.md" in contexto
    assert "Mi proyecto" in contexto
    assert ".env" not in contexto
