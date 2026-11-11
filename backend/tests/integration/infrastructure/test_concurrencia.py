"""P32: escrituras concurrentes sobre los documentos en disco sin pérdida de datos."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor

from modular_learning.core.application.materias import MateriasService
from modular_learning.infrastructure.persistence.almacen import AlmacenArchivos
from modular_learning.infrastructure.persistence.json_repositorios import (
    JsonCronogramaRepo,
    JsonMateriaRepo,
    JsonPluginConfigRepo,
    JsonRegistroMaterialesRepo,
)

N = 24


def _en_paralelo(funcion, n: int = N) -> list:
    with ThreadPoolExecutor(max_workers=n) as pool:
        return list(pool.map(funcion, range(n)))


def test_n_asignaturas_a_la_vez_persisten_todas(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    repo = JsonMateriaRepo(almacen=almacen)
    servicio = MateriasService(repo)

    _en_paralelo(lambda i: servicio.crear_materia(f"Asignatura {i:02d}"))

    nombres = JsonMateriaRepo(almacen=AlmacenArchivos(tmp_path)).cargar_materias()
    # El catálogo inicial (5 asignaturas) más las N nuevas, sin repetir ni perder ninguna
    esperadas = {f"Asignatura {i:02d}" for i in range(N)}
    assert esperadas <= set(nombres)
    assert len(nombres) == len(set(nombres)) == len(JsonMateriaRepo.MATERIAS_INICIALES) + N


def test_instancias_distintas_del_almacen_comparten_candado(tmp_path):
    def agregar(i: int) -> None:
        # Cada hilo con su propio repositorio y almacén sobre la misma carpeta
        JsonMateriaRepo(almacen=AlmacenArchivos(tmp_path)).agregar_materia(f"Otra {i:02d}")

    _en_paralelo(agregar)
    nombres = JsonMateriaRepo(almacen=AlmacenArchivos(tmp_path)).cargar_materias()
    assert {f"Otra {i:02d}" for i in range(N)} <= set(nombres)


def test_n_clases_a_la_vez_persisten_todas(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    materias = JsonMateriaRepo(almacen=almacen)
    crono = JsonCronogramaRepo(almacen=almacen)
    servicio = MateriasService(materias, crono)
    servicio.crear_materia("Redes")

    _en_paralelo(lambda i: servicio.agregar_clase("Redes", {"tema": f"Tema {i:02d}"}))

    clases = crono.obtener_cronograma("Redes")
    assert sorted(c["tema"] for c in clases) == [f"Tema {i:02d}" for i in range(N)]
    assert len({c["id"] for c in clases}) == N


def test_editar_y_eliminar_clases_a_la_vez(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    crono = JsonCronogramaRepo(almacen=almacen)
    servicio = MateriasService(JsonMateriaRepo(almacen=almacen), crono)
    servicio.crear_materia("Redes")
    ids = [servicio.agregar_clase("Redes", {"tema": f"T{i}"})["id"] for i in range(N)]

    def tocar(i: int) -> None:
        if i % 2:
            servicio.eliminar_clase("Redes", ids[i])
        else:
            servicio.editar_clase("Redes", ids[i], {"tema": f"Editada {i}"})

    _en_paralelo(tocar)
    clases = crono.obtener_cronograma("Redes")
    assert [c["id"] for c in clases] == ids[::2]
    assert all(c["tema"].startswith("Editada") for c in clases)


def test_eliminar_dos_veces_a_la_vez_no_falla(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    servicio = MateriasService(
        JsonMateriaRepo(almacen=almacen), JsonCronogramaRepo(almacen=almacen)
    )
    servicio.crear_materia("Borrar")
    resultados = _en_paralelo(lambda _: servicio.eliminar_materia("borrar"), 8)
    assert resultados.count(True) == 1 and resultados.count(False) == 7


def test_registro_y_config_de_plugins_concurrentes(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    registro = JsonRegistroMaterialesRepo(almacen=almacen)
    plugins = JsonPluginConfigRepo(almacen=almacen)

    _en_paralelo(lambda i: registro.registrar_material(f"a{i}.pdf", "Redes"))
    _en_paralelo(lambda i: plugins.guardar_configuracion(f"p{i}", carpeta=f"/x/{i}"))

    assert len(registro.listar_materiales()) == N
    assert len(plugins.obtener_configuraciones()) == N


def test_escrituras_al_mismo_documento_no_dejan_temporales_ni_json_roto(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    contenidos = [json.dumps({"i": i, "relleno": "x" * 5000}) for i in range(N)]

    _en_paralelo(lambda i: almacen.escribir("config/doc.json", contenidos[i]))

    assert json.loads(almacen.leer("config/doc.json"))["i"] in range(N)
    assert [p.name for p in (tmp_path / "config").iterdir()] == ["doc.json"]
