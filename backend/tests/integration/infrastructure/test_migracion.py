"""Tests de integración para el script de migración sobre AlmacenArchivos."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from modular_learning.infrastructure.persistence.almacen import AlmacenArchivos

# Añadir scripts/ al path para importar migrar_datos
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
from migrar_datos import migrar


def test_migracion_idempotente_sobre_almacen_archivos(tmp_path):
    almacen = AlmacenArchivos(tmp_path)

    # 1. Configurar datos iniciales no migrados
    # Materias solo en materias.txt
    almacen.escribir("config/materias.txt", "Ingeniería de Software II\nRedes de Comunicación")

    # Cronograma antiguo en mayúsculas y clases sin id
    cronograma_datos = {
        "clases": [
            {"fecha": "01/10/2026", "tema": "VLAN", "estado": "pendiente"},
            {"fecha": "08/10/2026", "tema": "Enrutamiento", "estado": "completado"},
        ]
    }
    almacen.escribir(
        "schedules/REDES_DE_COMUNICACION_cronograma.json", json.dumps(cronograma_datos)
    )

    # Guía sin clase_id
    guias_datos = {
        "g1": {
            "id": "g1",
            "materia": "Redes de Comunicación",
            "clases": [
                {"tema": "VLAN", "fecha": "01/10/2026"},
                {"tema": "Enrutamiento", "fecha": "08/10/2026"},
            ],
        }
    }
    almacen.escribir("guias/guias.json", json.dumps(guias_datos))

    # 2. Prueba con --simular (no debe modificar nada)
    res_sim = migrar(almacen=almacen, simular=True)
    assert res_sim["materias"] == 2
    assert res_sim["cronogramas_renombrados"] == 1
    assert res_sim["ids_asignados"] == 2
    assert res_sim["guias_vinculadas"] == 2

    # Comprobar que en disco nada cambió tras simular
    assert almacen.leer("config/materias.json") is None
    assert almacen.leer("schedules/redes-de-comunicacion_cronograma.json") is None
    assert almacen.leer("schedules/REDES_DE_COMUNICACION_cronograma.json") is not None

    # 3. Primera ejecución real de migración
    res1 = migrar(almacen=almacen, simular=False)
    assert res1["materias"] == 2
    assert res1["cronogramas_renombrados"] == 1
    assert res1["ids_asignados"] == 2
    assert res1["guias_vinculadas"] == 2

    # Verificar que el cronograma fue renombrado al slug
    assert almacen.leer("schedules/REDES_DE_COMUNICACION_cronograma.json") is None
    sched_migrado = json.loads(almacen.leer("schedules/redes-de-comunicacion_cronograma.json"))
    clases_sched = sched_migrado["clases"]
    assert len(clases_sched) == 2
    id_c1 = clases_sched[0].get("id")
    id_c2 = clases_sched[1].get("id")
    assert bool(id_c1)
    assert bool(id_c2)

    # Verificar que la guía enlazó los clase_id
    guias_migrado = json.loads(almacen.leer("guias/guias.json"))
    clases_guia = guias_migrado["g1"]["clases"]
    assert clases_guia[0].get("clase_id") == id_c1
    assert clases_guia[1].get("clase_id") == id_c2

    # Guardar snapshot de todos los documentos tras la primera ejecución
    snapshot_claves = sorted(almacen.listar())
    snapshot_docs = {clave: almacen.leer(clave) for clave in snapshot_claves}

    # 4. Segunda ejecución (idempotencia)
    res2 = migrar(almacen=almacen, simular=False)
    assert res2["cronogramas_renombrados"] == 0
    assert res2["ids_asignados"] == 0
    assert res2["guias_vinculadas"] == 0

    # Verificar que el contenido de todos los documentos es 100% idéntico
    post_claves = sorted(almacen.listar())
    assert post_claves == snapshot_claves
    post_docs = {clave: almacen.leer(clave) for clave in post_claves}
    assert post_docs == snapshot_docs
