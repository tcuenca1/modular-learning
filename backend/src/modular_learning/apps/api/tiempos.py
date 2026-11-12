"""Medición de cada petición: cabecera `Server-Timing` y aviso en el log de las lentas.

En Render el log se lee desde el navegador del teléfono: una línea `Petición lenta` dice qué ruta
tardó y cuánto, sin necesidad de herramientas de desarrollo. El umbral es `ML_UMBRAL_LENTA_MS`
(700 ms por defecto).
"""

from __future__ import annotations

import logging
import os
import time

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("modular_learning.api")


class MedirTiempos:
    """Añade `Server-Timing: app;dur=<ms>` y registra las peticiones más lentas que el umbral."""

    def __init__(self, app: ASGIApp, umbral_ms: float | None = None):
        self.app = app
        self.umbral_ms = (
            umbral_ms if umbral_ms is not None else float(os.getenv("ML_UMBRAL_LENTA_MS", "700"))
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        inicio = time.perf_counter()
        estado = {"codigo": 0}

        async def enviar(mensaje: Message) -> None:
            if mensaje["type"] == "http.response.start":
                ms = (time.perf_counter() - inicio) * 1000
                estado["codigo"] = mensaje["status"]
                MutableHeaders(scope=mensaje).append("Server-Timing", f"app;dur={ms:.0f}")
            await send(mensaje)

        await self.app(scope, receive, enviar)
        ms = (time.perf_counter() - inicio) * 1000
        # Los flujos SSE y descargas largas no son "lentas": solo se avisan las respuestas normales
        if ms >= self.umbral_ms and not scope["path"].endswith(("/stream", "/pdf")):
            logger.warning(
                "Petición lenta: %s %s -> %s en %.0f ms",
                scope["method"],
                scope["path"],
                estado["codigo"],
                ms,
            )


__all__ = ["MedirTiempos"]
