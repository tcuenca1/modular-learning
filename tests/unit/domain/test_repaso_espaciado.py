from datetime import date

from modular_learning.core.domain.repaso_espaciado import Tarjeta, id_tarjeta, programar

HOY = date(2026, 10, 25)


def _tarjeta() -> Tarjeta:
    return Tarjeta(
        id="t1",
        materia="Redes",
        tema="VLAN",
        enunciado="¿Qué es una VLAN?",
        opciones=["A) x", "B) y"],
        respuesta_correcta="A) x",
    )


def test_aciertos_alargan_el_intervalo_segun_sm2():
    t = _tarjeta()
    programar(t, True, HOY)
    assert (t.intervalo, t.proxima) == (1, "2026-10-26")
    programar(t, True, HOY)
    assert t.intervalo == 6
    programar(t, True, HOY)
    assert t.intervalo == round(6 * t.facilidad) > 6
    assert len(t.intentos) == 3 and all(i.correcto for i in t.intentos)


def test_fallo_reinicia_la_tarjeta_y_baja_la_facilidad():
    t = _tarjeta()
    programar(t, True, HOY)
    programar(t, True, HOY)
    facilidad = t.facilidad
    programar(t, False, HOY, elegida="B) y")

    assert t.repeticiones == 0
    assert t.intervalo == 1
    assert t.proxima == "2026-10-26"
    assert t.facilidad < facilidad
    assert t.ultimo_fallo
    assert t.intentos[-1].elegida == "B) y"


def test_facilidad_nunca_baja_del_minimo():
    t = _tarjeta()
    for _ in range(20):
        programar(t, False, HOY)
    assert t.facilidad == 1.3


def test_vence_y_serializacion():
    t = programar(_tarjeta(), True, HOY)
    assert not t.vence(HOY)
    assert t.vence(date(2026, 10, 26))
    assert Tarjeta.desde_dict(t.a_dict()) == t


def test_id_tarjeta_ignora_tildes_mayusculas_y_espacios():
    assert id_tarjeta("Redes", "¿Qué es  una VLAN?") == id_tarjeta("redes", "¿que es una vlan?")
    assert id_tarjeta("Redes", "A") != id_tarjeta("IoT", "A")
