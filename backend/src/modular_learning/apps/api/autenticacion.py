"""Middleware de sesión por cookie: identifica la cuenta de cada petición y protege `/api/`.

Con login activo (ML_REQUIERE_ACCESO) toda ruta `/api/*` exige una sesión válida, salvo la de
salud, el inicio de sesión y la consulta de sesión. La web estática (HTML, JS, CSS) es pública:
no lleva datos y debe poder cargar para mostrar la pantalla de acceso.
"""

from __future__ import annotations

from http.cookies import CookieError, SimpleCookie

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from modular_learning.core.application.autenticacion import AutenticacionService
from modular_learning.infrastructure.persistence.almacen import en_cuenta

NOMBRE_COOKIE = "ml_sesion"
RUTAS_LIBRES = ("/api/salud", "/api/auth/login", "/api/auth/yo")


def token_de_cookie(cabecera: str) -> str:
    try:
        cookie: SimpleCookie = SimpleCookie()
        cookie.load(cabecera)
        return cookie[NOMBRE_COOKIE].value if NOMBRE_COOKIE in cookie else ""
    except CookieError:
        return ""


class Autenticacion:
    """Fija la cuenta activa (para el almacén por cuenta) y responde 401 sin sesión."""

    def __init__(self, app: ASGIApp, servicio: AutenticacionService | None):
        self.app = app
        self.servicio = servicio

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ruta = scope.get("path", "")
        if scope["type"] != "http" or not ruta.startswith("/api/"):
            await self.app(scope, receive, send)
            return

        if self.servicio is None:  # login activo pero sin ML_CONTRASENA: nunca queda abierto
            if ruta == "/api/salud":
                await self.app(scope, receive, send)
                return
            respuesta = JSONResponse(
                {"detail": "Falta configurar ML_CONTRASENA en el servidor."}, status_code=503
            )
            await respuesta(scope, receive, send)
            return

        cabeceras = {k.decode().lower(): v.decode() for k, v in scope["headers"]}
        usuario = None
        token = token_de_cookie(cabeceras.get("cookie", ""))
        if token and ruta != "/api/salud":
            usuario = self.servicio.usuario_de_token(token)
        scope.setdefault("state", {})["usuario"] = usuario

        if usuario is None and ruta not in RUTAS_LIBRES:
            respuesta = JSONResponse({"detail": "Inicia sesión para continuar."}, status_code=401)
            await respuesta(scope, receive, send)
            return

        with en_cuenta(usuario.id if usuario else None):
            await self.app(scope, receive, send)


__all__ = ["NOMBRE_COOKIE", "RUTAS_LIBRES", "Autenticacion", "token_de_cookie"]
