"""
Contrato de `CronogramaRepo` y `MateriaRepo`: las mismas aserciones contra el fake en memoria y
contra el adaptador JSON en disco. Si alguno diverge, los tests unitarios que usan el fake
dejarían de representar el comportamiento real.
"""

from __future__ import annotations

import pytest

from modular_learning.core.domain.materias import Materia
from modular_learning.infrastructure.persistence.almacen import AlmacenArchivos
from modular_learning.infrastructure.persistence.json_repositorios import (
    JsonCronogramaRepo,
    JsonMateriaRepo,
)
from tests.unit.application.fake_adapters import InMemoryCronogramaRepo, InMemoryMateriaRepo


@pytest.fixture(params=["memoria", "disco"])
def cronograma_repo(request, tmp_path):
    if request.param == "memoria":
        return InMemoryCronogramaRepo()
    return JsonCronogramaRepo(almacen=AlmacenArchivos(tmp_path))


@pytest.fixture(params=["memoria", "disco"])
def materia_repo(request, tmp_path):
    if request.param == "memoria":
        return InMemoryMateriaRepo()
    almacen = AlmacenArchivos(tmp_path)
    almacen.escribir("config/materias.json", "[]")  # catálogo vacío, sin las asignaturas iniciales
    return JsonMateriaRepo(almacen=almacen)


def _clases() -> list[dict]:
    return [
        {"fecha": "01/10/2026", "tema": "Introducción", "estado": "completado"},
        {"fecha": "08/10/2026", "tema": "Enrutamiento", "estado": "pendiente"},
        {"fecha": "15/10/2026", "tema": "VLAN", "estado": "pendiente"},
    ]


# --------------------------------------------------------------------------- CronogramaRepo
def test_cronograma_inexistente(cronograma_repo):
    assert cronograma_repo.obtener_cronograma("Redes") is None
    assert cronograma_repo.obtener_proximas_clases("Redes") == []
    assert cronograma_repo.obtener_parciales("Redes") == []
    assert cronograma_repo.eliminar_cronograma("Redes") is False
    assert cronograma_repo.marcar_clase("Redes", tema="VLAN") is False
    assert cronograma_repo.quitar_material_transversal("Redes", "x.pdf") is False
    assert cronograma_repo.listar_cronogramas() == {}


def test_guardar_asigna_ids_y_se_lee_por_slug_o_nombre(cronograma_repo):
    ubicacion = cronograma_repo.guardar_cronograma("Redes de Datos", _clases())
    assert isinstance(ubicacion, str) and ubicacion

    for forma in ("Redes de Datos", "redes-de-datos", "REDES DE DATOS"):
        leidas = cronograma_repo.obtener_cronograma(forma)
        assert [c["tema"] for c in leidas] == ["Introducción", "Enrutamiento", "VLAN"]
        assert all(c["id"] for c in leidas)
    assert len({c["id"] for c in cronograma_repo.obtener_cronograma("redes-de-datos")}) == 3
    assert list(cronograma_repo.listar_cronogramas()) == ["redes-de-datos"]


def test_la_coincidencia_de_asignatura_es_exacta(cronograma_repo):
    cronograma_repo.guardar_cronograma("Ingenieria de Software II", _clases())
    assert cronograma_repo.obtener_cronograma("Ingenieria de Software") is None
    assert cronograma_repo.eliminar_cronograma("Ingenieria de Software") is False
    assert cronograma_repo.obtener_cronograma("ingenieria-de-software-ii") is not None


def test_proximas_clases_son_pendientes_y_como_mucho_cinco(cronograma_repo):
    clases = [{"tema": f"T{i}", "estado": "pendiente"} for i in range(7)]
    clases.insert(0, {"tema": "Hecha", "estado": "completado"})
    cronograma_repo.guardar_cronograma("Redes", clases)
    proximas = cronograma_repo.obtener_proximas_clases("Redes")
    assert [c["tema"] for c in proximas] == ["T0", "T1", "T2", "T3", "T4"]
    assert all(
        c["subtemas_adicionales"] == [] and c["materiales_asociados"] == [] for c in proximas
    )


def test_marcar_clase_por_id_y_por_tema(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes", _clases())
    ids = {c["tema"]: c["id"] for c in cronograma_repo.obtener_cronograma("Redes")}

    assert cronograma_repo.marcar_clase("Redes", clase_id=ids["VLAN"]) is True
    assert cronograma_repo.marcar_clase_completada("Redes", "Enrutamiento") is True
    assert cronograma_repo.marcar_clase("Redes", clase_id="no-existe") is False
    assert cronograma_repo.marcar_clase("Redes", tema="Tema inexistente") is False

    estados = {c["tema"]: c["estado"] for c in cronograma_repo.obtener_cronograma("Redes")}
    assert estados == {
        "Introducción": "completado",
        "Enrutamiento": "completado",
        "VLAN": "completado",
    }
    assert cronograma_repo.obtener_proximas_clases("Redes") == []

    assert cronograma_repo.marcar_clase("Redes", clase_id=ids["VLAN"], estado="pendiente") is True
    assert [c["tema"] for c in cronograma_repo.obtener_proximas_clases("Redes")] == ["VLAN"]


def test_obtener_detalle_clase(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes", _clases())
    clase_id = cronograma_repo.obtener_cronograma("Redes")[2]["id"]

    por_id = cronograma_repo.obtener_detalle_clase("Redes", clase_id=clase_id)
    por_tema = cronograma_repo.obtener_detalle_clase("Redes", tema="vlan")
    assert por_id["tema"] == por_tema["tema"] == "VLAN"
    assert por_id["subtemas_adicionales"] == [] and por_id["materiales_asociados"] == []

    vacio = cronograma_repo.obtener_detalle_clase("Redes", tema="No existe")
    assert vacio == {"subtemas_adicionales": [], "materiales_asociados": []}


def test_actualizar_cronograma_es_atomico_y_propaga_errores(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes", _clases())

    def agregar(clases):
        clases.append({"tema": "Nueva", "estado": "pendiente"})

    guardadas = cronograma_repo.actualizar_cronograma("Redes", agregar)
    assert [c["tema"] for c in guardadas][-1] == "Nueva"
    assert [c["tema"] for c in cronograma_repo.obtener_cronograma("Redes")][-1] == "Nueva"

    def reemplazar(clases):
        return [c for c in clases if c["tema"] == "VLAN"]

    assert [c["tema"] for c in cronograma_repo.actualizar_cronograma("Redes", reemplazar)] == [
        "VLAN"
    ]

    def falla(clases):
        clases.append({"tema": "NoDebeGuardarse"})
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        cronograma_repo.actualizar_cronograma("Redes", falla)
    assert [c["tema"] for c in cronograma_repo.obtener_cronograma("Redes")] == ["VLAN"]


def test_material_transversal(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes", _clases())
    cronograma_repo.agregar_material_transversal("Redes", {"archivo": "guia.pdf"})
    cronograma_repo.agregar_material_transversal("Redes", {"archivo": "lab.pdf"})

    assert cronograma_repo.quitar_material_transversal("Redes", "guia.pdf") is True
    assert cronograma_repo.quitar_material_transversal("Redes", "guia.pdf") is False
    cronograma_repo.limpiar_material_transversal("Redes")
    assert cronograma_repo.quitar_material_transversal("Redes", "lab.pdf") is False
    # Las clases no se tocan
    assert len(cronograma_repo.obtener_cronograma("Redes")) == 3


def test_parciales_se_guardan_y_se_reemplazan(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes", _clases())
    clase_id = cronograma_repo.obtener_cronograma("Redes")[1]["id"]

    cronograma_repo.guardar_parciales("Redes", [{"nombre": "Parcial 1", "hasta": clase_id}])
    assert cronograma_repo.obtener_parciales("redes") == [
        {"nombre": "Parcial 1", "hasta": clase_id}
    ]
    cronograma_repo.guardar_parciales("Redes", [])
    assert cronograma_repo.obtener_parciales("Redes") == []
    # Guardar clases de nuevo no borra los parciales
    cronograma_repo.guardar_parciales("Redes", [{"nombre": "P", "hasta": clase_id}])
    cronograma_repo.guardar_cronograma("Redes", _clases())
    assert len(cronograma_repo.obtener_parciales("Redes")) == 1


def test_eliminar_cronograma_borra_clases_y_parciales(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes", _clases())
    cronograma_repo.guardar_parciales("Redes", [{"nombre": "P", "hasta": "x"}])

    assert cronograma_repo.eliminar_cronograma("redes") is True
    assert cronograma_repo.obtener_cronograma("Redes") is None
    assert cronograma_repo.obtener_parciales("Redes") == []
    assert cronograma_repo.eliminar_cronograma("Redes") is False
    assert cronograma_repo.listar_cronogramas() == {}


def test_listar_cronogramas_por_slug(cronograma_repo):
    cronograma_repo.guardar_cronograma("Redes de Datos", _clases())
    cronograma_repo.guardar_cronograma("IoT", [{"tema": "MQTT", "estado": "pendiente"}])
    todos = cronograma_repo.listar_cronogramas()
    assert set(todos) == {"redes-de-datos", "iot"}
    assert [c["tema"] for c in todos["iot"]] == ["MQTT"]


# --------------------------------------------------------------------------- MateriaRepo
def test_catalogo_vacio(materia_repo):
    assert materia_repo.listar() == []
    assert materia_repo.cargar_materias() == []
    assert materia_repo.eliminar("redes") is False


def test_guardar_es_un_alta_o_una_actualizacion_por_slug(materia_repo):
    materia_repo.guardar(Materia.desde_nombre("Redes de Datos"))
    materia_repo.guardar(Materia.desde_nombre("IoT"))
    materia_repo.guardar(Materia(slug="redes-de-datos", nombre="Redes de Datos II"))

    assert [(m.slug, m.nombre) for m in materia_repo.listar()] == [
        ("redes-de-datos", "Redes de Datos II"),
        ("iot", "IoT"),
    ]
    assert materia_repo.cargar_materias() == ["Redes de Datos II", "IoT"]


def test_agregar_materia_es_idempotente_y_ignora_vacios(materia_repo):
    materia_repo.agregar_materia("Física Cuántica")
    materia_repo.agregar_materia("  física  cuántica ")  # mismo slug: no se duplica
    materia_repo.agregar_materia("FISICA-CUANTICA")
    materia_repo.agregar_materia("")
    materia_repo.agregar_materia("   ")

    assert [(m.slug, m.nombre) for m in materia_repo.listar()] == [
        ("fisica-cuantica", "Física Cuántica")
    ]


def test_eliminar_por_slug_o_nombre_sin_importar_el_formato(materia_repo):
    materia_repo.agregar_materia("Redes de Datos")
    materia_repo.agregar_materia("IoT")

    assert materia_repo.eliminar("REDES DE DATOS") is True
    assert materia_repo.eliminar("redes-de-datos") is False
    assert materia_repo.cargar_materias() == ["IoT"]
