"""P43: la instantánea de AlmacenPostgres evita consultas repetidas y respeta su caducidad.

Usa un pool falso en memoria que cuenta las consultas: no necesita Postgres.
"""

from __future__ import annotations

from contextlib import contextmanager

from modular_learning.infrastructure.persistence.almacen import AlmacenPostgres


class _Cursor:
    def __init__(self, filas=None, rowcount=0):
        self._filas, self.rowcount = filas or [], rowcount

    def fetchall(self):
        return list(self._filas)


class _BaseFalsa:
    """Imita solo las 4 sentencias que usa AlmacenPostgres."""

    def __init__(self):
        self.tabla: dict[str, str] = {}
        self.consultas: list[str] = []

    @contextmanager
    def connection(self):
        yield self

    def execute(self, sql, params=()):
        self.consultas.append(sql.split()[0])
        if sql.startswith("SELECT"):
            return _Cursor(sorted(self.tabla.items()))
        if sql.startswith("INSERT"):
            self.tabla[params[0]] = params[1]
            return _Cursor()
        if sql.startswith("DELETE"):
            existia = params[0] in self.tabla
            self.tabla.pop(params[0], None)
            return _Cursor(rowcount=1 if existia else 0)
        return _Cursor()  # CREATE TABLE


def _almacen(segundos=30.0):
    base = _BaseFalsa()
    return AlmacenPostgres("postgresql://falsa", pool=base, segundos_cache=segundos), base


def test_lecturas_y_listados_usan_una_sola_consulta():
    almacen, base = _almacen()
    base.tabla = {"a/x.json": "1", "a/y.json": "2", "b/z.json": "3"}
    base.consultas.clear()

    assert almacen.leer("a/x.json") == "1"
    assert almacen.leer("no/existe") is None
    assert almacen.listar("a/") == ["a/x.json", "a/y.json"]
    assert almacen.listar("") == ["a/x.json", "a/y.json", "b/z.json"]
    assert base.consultas == ["SELECT"]


def test_escribir_y_eliminar_actualizan_la_instantanea_sin_recargar():
    almacen, base = _almacen()
    almacen.precalentar()
    base.consultas.clear()

    almacen.escribir("c/n.json", "nuevo")
    assert almacen.leer("c/n.json") == "nuevo"
    assert almacen.listar("c/") == ["c/n.json"]
    assert almacen.eliminar("c/n.json") is True
    assert almacen.eliminar("c/n.json") is False
    assert almacen.leer("c/n.json") is None
    assert base.consultas == ["INSERT", "DELETE", "DELETE"]
    assert base.tabla == {}


def test_la_instantanea_caduca_y_ve_cambios_de_otro_proceso():
    almacen, base = _almacen(segundos=0.0)  # caduca siempre
    assert almacen.leer("k") is None
    base.tabla["k"] = "externo"  # lo escribe otro proceso
    assert almacen.leer("k") == "externo"


def test_vaciar_cache_fuerza_una_nueva_consulta():
    almacen, base = _almacen()
    almacen.precalentar()
    base.tabla["k"] = "externo"
    assert almacen.leer("k") is None  # aún en la instantánea
    almacen.vaciar_cache()
    assert almacen.leer("k") == "externo"
