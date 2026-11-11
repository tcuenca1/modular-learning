"""Errores HTTP que no filtran detalles del servidor (rutas absolutas, trazas)."""

from __future__ import annotations

import logging
import re

from fastapi import HTTPException

logger = logging.getLogger("modular_learning.api")

MENSAJE_ERROR_INTERNO = "Ocurrió un error interno. Revisa el registro del servidor."

_RUTA_WINDOWS = re.compile(r"[A-Za-z]:[\\/][^\n'\"`<>|]*")
_RUTA_POSIX = re.compile(r"(?<![\w.:])/(?:[^\s/'\"`<>|]+/)+[^\s/'\"`<>|]*")


def sin_rutas(texto: str) -> str:
    """Sustituye las rutas absolutas (Windows o POSIX) de un mensaje por «<ruta>»."""
    return _RUTA_POSIX.sub("<ruta>", _RUTA_WINDOWS.sub("<ruta>", texto))


def error_cliente(e: Exception, status: int = 400) -> HTTPException:
    """Error 4xx con el mensaje de la excepción, sin rutas absolutas; el detalle va al log."""
    logger.warning("Solicitud rechazada (%s): %s", status, e)
    return HTTPException(status_code=status, detail=sin_rutas(str(e)))


def error_interno(e: Exception) -> HTTPException:
    """Error 500 genérico; la excepción completa se registra en el log."""
    logger.error("Error interno: %s", e, exc_info=e)
    return HTTPException(status_code=500, detail=MENSAJE_ERROR_INTERNO)


def mensaje_evento_error(e: Exception) -> str:
    """Texto para un evento SSE de error: genérico, con el detalle en el log."""
    logger.error("Error en un flujo de eventos: %s", e, exc_info=e)
    return MENSAJE_ERROR_INTERNO


__all__ = [
    "MENSAJE_ERROR_INTERNO",
    "error_cliente",
    "error_interno",
    "mensaje_evento_error",
    "sin_rutas",
]
