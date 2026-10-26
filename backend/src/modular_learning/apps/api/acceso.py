"""Control de acceso con usuario y contraseña (HTTP Basic) para el despliegue en la nube.

En local no se activa. En la nube (`ML_REQUIERE_ACCESO=1`, lo fija el Dockerfile) toda la web
y la API piden las credenciales de `ML_USUARIO` y `ML_CONTRASENA`; si faltan, el servidor
responde 503 en lugar de quedar abierto. `/api/salud` queda libre para el healthcheck.
"""

from __future__ import annotations

import base64
import binascii
import os
import secrets

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.types import ASGIApp

RUTAS_LIBRES = ("/api/salud",)


def _credenciales(cabecera: str) -> tuple[str, str] | None:
    esquema, _, valor = cabecera.partition(" ")
    if esquema.lower() != "basic" or not valor:
        return None
    try:
        usuario, separador, contrasena = base64.b64decode(valor).decode("utf-8").partition(":")
    except (binascii.Error, UnicodeDecodeError):
        return None
    return (usuario, contrasena) if separador else None


class AccesoBasico(BaseHTTPMiddleware):
    """Exige usuario y contraseña en cada petición salvo en las rutas libres."""

    def __init__(self, app: ASGIApp, usuario: str, contrasena: str):
        super().__init__(app)
        self.usuario = usuario
        self.contrasena = contrasena

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in RUTAS_LIBRES:
            return await call_next(request)
        if not self.contrasena:
            return JSONResponse(
                {"detail": "Falta configurar ML_CONTRASENA en el servidor."}, status_code=503
            )

        recibidas = _credenciales(request.headers.get("authorization", ""))
        if recibidas and all(
            secrets.compare_digest(a.encode(), b.encode())
            for a, b in zip(recibidas, (self.usuario, self.contrasena), strict=True)
        ):
            return await call_next(request)
        return PlainTextResponse(
            "Acceso restringido.",
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="Modular Learning", charset="UTF-8"'},
        )


def parametros_acceso() -> dict[str, str] | None:
    """Usuario y contraseña para `AccesoBasico`, o None si el acceso no está activado."""
    if os.getenv("ML_REQUIERE_ACCESO", "").strip().lower() not in ("1", "true", "si", "sí"):
        return None
    return {
        "usuario": os.getenv("ML_USUARIO", "").strip() or "estudiante",
        "contrasena": os.getenv("ML_CONTRASENA", ""),
    }


__all__ = ["RUTAS_LIBRES", "AccesoBasico", "parametros_acceso"]
