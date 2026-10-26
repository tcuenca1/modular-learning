"""Tests de dominio de la guía de estudio offline."""

from __future__ import annotations

from modular_learning.core.domain.guia_offline import (
    MARCADOR_RESPUESTAS,
    ClaseGuia,
    GuiaOffline,
    elegir_extension,
    separar_respuestas,
)


def test_extension_se_reduce_con_mas_clases():
    assert elegir_extension(1) == "completa"
    assert elegir_extension(2) == "completa"
    assert elegir_extension(4) == "estandar"
    assert elegir_extension(9) == "sintesis"


def test_separar_respuestas():
    texto = f"## Explicación\nHola\n\n{MARCADOR_RESPUESTAS}\n1. Porque sí"
    assert separar_respuestas(texto) == ("## Explicación\nHola", "1. Porque sí")
    assert separar_respuestas("  Solo explicación  ") == ("Solo explicación", "")


def test_pendiente_de_confirmar_solo_cuando_esta_generada_y_sin_revisar():
    guia = GuiaOffline(
        id="g1",
        materia="Redes",
        extension="completa",
        creada="2026-10-26T08:00:00",
        clases=[ClaseGuia(tema="VLAN"), ClaseGuia(tema="STP")],
    )
    assert not guia.completa and not guia.pendiente_de_confirmar

    for clase in guia.clases:
        clase.contenido = "texto"
    assert guia.pendiente_de_confirmar

    guia.revisada = "2026-10-26T13:00:00"
    assert not guia.pendiente_de_confirmar


def test_guia_ida_y_vuelta_a_dict():
    guia = GuiaOffline(
        id="g1",
        materia="Redes",
        extension="estandar",
        creada="2026-10-26T08:00:00",
        clases=[ClaseGuia(tema="VLAN", fecha="01/10/2026", contenido="c", resultado="entendida")],
    )
    datos = guia.a_dict()
    assert datos["completa"] is True and datos["pendiente_de_confirmar"] is True
    assert GuiaOffline.desde_dict(datos) == guia
