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


def test_repos_de_repaso_persisten_tarjetas_e_historial(tmp_path):
    from datetime import date

    from modular_learning.core.domain.repaso_espaciado import Tarjeta, programar
    from modular_learning.infrastructure.persistence.json_repaso import (
        JsonHistorialRepo,
        JsonTarjetasRepo,
    )

    tarjetas = JsonTarjetasRepo(str(tmp_path / "repaso" / "tarjetas.json"))
    assert tarjetas.listar() == []
    t = Tarjeta(
        id="a1",
        materia="Redes",
        tema="VLAN",
        enunciado="¿Qué es?",
        opciones=["A) x"],
        respuesta_correcta="A) x",
    )
    tarjetas.guardar(programar(t, False, date(2026, 10, 25)))
    recuperada = JsonTarjetasRepo(str(tmp_path / "repaso" / "tarjetas.json")).obtener("a1")
    assert recuperada == t
    assert recuperada.ultimo_fallo

    historial = JsonHistorialRepo(str(tmp_path / "repaso" / "historial.json"))
    historial.registrar({"tipo": "tutoria", "materia": "Redes", "tema": "VLAN y trunking"})
    historial.registrar({"tipo": "repaso", "materia": "IoT", "tema": "MQTT"})
    assert [e["tipo"] for e in historial.listar()] == ["repaso", "tutoria"]
    assert len(historial.listar(materia="redes", tema="vlan")) == 1
    assert historial.listar(materia="Redes", tema="MQTT") == []


def test_repo_de_guias_persiste_y_ordena(tmp_path):
    from modular_learning.core.domain.guia_offline import ClaseGuia, GuiaOffline
    from modular_learning.infrastructure.persistence.json_guias import JsonGuiasRepo

    ruta = str(tmp_path / "guias" / "guias.json")
    repo = JsonGuiasRepo(ruta)
    assert repo.listar() == [] and repo.obtener("x") is None

    antigua = GuiaOffline("a", "Redes", "completa", "2026-10-20T08:00:00", [ClaseGuia("VLAN")])
    nueva = GuiaOffline("b", "IoT", "sintesis", "2026-10-26T08:00:00", [ClaseGuia("MQTT", "", "c")])
    repo.guardar(antigua)
    repo.guardar(nueva)

    releida = JsonGuiasRepo(ruta)
    assert [g.id for g in releida.listar()] == ["b", "a"]
    assert releida.obtener("b") == nueva
