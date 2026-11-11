"""P31: los mensajes de error no filtran rutas absolutas del servidor."""

from __future__ import annotations

import logging

from modular_learning.apps.api.errores import (
    MENSAJE_ERROR_INTERNO,
    error_cliente,
    error_interno,
    sin_rutas,
)


def test_sin_rutas_oculta_rutas_posix_y_windows():
    assert sin_rutas("No existe /home/user/datos/x.pdf aquí") == "No existe <ruta> aquí"
    assert sin_rutas("Falla C:\\Users\\yo\\Documentos\\a.pdf") == "Falla <ruta>"
    assert sin_rutas("Falla D:/uni/Redes") == "Falla <ruta>"


def test_sin_rutas_respeta_textos_normales():
    assert sin_rutas("Formato no soportado (.pdf/.docx). y/o algo") == (
        "Formato no soportado (.pdf/.docx). y/o algo"
    )


def test_error_cliente_oculta_rutas_y_registra_el_detalle(caplog):
    with caplog.at_level(logging.WARNING, logger="modular_learning.api"):
        exc = error_cliente(ValueError("No existe /srv/app/datos/x"))
    assert exc.status_code == 400
    assert "/srv" not in exc.detail
    assert "/srv/app/datos/x" in caplog.text


def test_error_interno_es_generico_y_registra_la_traza(caplog):
    with caplog.at_level(logging.ERROR, logger="modular_learning.api"):
        exc = error_interno(RuntimeError("boom en /srv/app/secreto.py"))
    assert exc.status_code == 500
    assert exc.detail == MENSAJE_ERROR_INTERNO
    assert "/srv" not in exc.detail
    assert "/srv/app/secreto.py" in caplog.text
