"""Tests de integración de los adaptadores de disco (cronogramas, documentos y bóveda)."""

from __future__ import annotations

import json

from modular_learning.infrastructure.documents.lector_documentos import LectorDocumentosLocal
from modular_learning.infrastructure.obsidian.boveda_obsidian import BovedaObsidianAdapter
from modular_learning.infrastructure.persistence.json_repositorios import JsonCronogramaRepo


def test_cronograma_repo_listar_y_material_transversal(tmp_path):
    (tmp_path / "Redes_cronograma.json").write_text(
        json.dumps({"clases": [{"tema": "VLAN", "estado": "completado"}]}), encoding="utf-8"
    )
    (tmp_path / "IoT_cronograma.json").write_text(
        json.dumps([{"tema": "MQTT", "estado": "pendiente"}]), encoding="utf-8"
    )
    repo = JsonCronogramaRepo(str(tmp_path))

    assert repo.listar_cronogramas() == {
        "IoT": [{"tema": "MQTT", "estado": "pendiente"}],
        "Redes": [{"tema": "VLAN", "estado": "completado"}],
    }

    repo.agregar_material_transversal("IoT", {"archivo": "x.pdf"})
    data = json.loads((tmp_path / "IoT_cronograma.json").read_text(encoding="utf-8"))
    assert data == {
        "clases": [{"tema": "MQTT", "estado": "pendiente"}],
        "material_transversal": [{"archivo": "x.pdf"}],
    }

    # Guardar clases conserva el material transversal y retorna la ruta
    ruta = repo.guardar_cronograma("IoT", [{"tema": "CoAP", "estado": "pendiente"}])
    data = json.loads((tmp_path / "IoT_cronograma.json").read_text(encoding="utf-8"))
    assert ruta.endswith("IoT_cronograma.json")
    assert data["material_transversal"] == [{"archivo": "x.pdf"}]
    assert data["clases"][0]["tema"] == "CoAP"


def test_cronograma_repo_carpeta_inexistente(tmp_path):
    assert JsonCronogramaRepo(str(tmp_path / "no_existe")).listar_cronogramas() == {}


def test_lector_documentos_extraer_y_listar(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.txt").write_text("hola", encoding="utf-8")
    (tmp_path / "b.md").write_bytes("canción".encode("latin-1"))
    (tmp_path / "sub" / "c.txt").write_text("x", encoding="utf-8")
    lector = LectorDocumentosLocal()

    assert lector.extraer_texto(str(tmp_path / "a.txt")) == "hola"
    assert lector.extraer_texto(str(tmp_path / "b.md")) == "canción"
    assert lector.listar_archivos(str(tmp_path / "nada")) is None
    assert sorted(
        p.replace("\\", "/").rsplit("/", 1)[-1] for p in lector.listar_archivos(str(tmp_path))
    ) == [
        "a.txt",
        "b.md",
        "c.txt",
    ]
    assert len(lector.listar_archivos(str(tmp_path), recursivo=False)) == 2


def test_boveda_guardar_nota(tmp_path):
    ruta = BovedaObsidianAdapter(str(tmp_path)).guardar_nota(
        "Redes", "Lectura", "Doc_Notas", "# Hola"
    )
    assert ruta.replace("\\", "/").endswith("Redes/Lectura/Doc_Notas.md")
    assert (tmp_path / "Redes" / "Lectura" / "Doc_Notas.md").read_text(encoding="utf-8") == "# Hola"
