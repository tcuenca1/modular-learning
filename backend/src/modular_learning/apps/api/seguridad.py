"""Cabeceras de seguridad, cabeceras de caché y validación del encabezado Host.

Variables de entorno (ver docs/DESPLIEGUE.md):
- `ML_HOSTS_PERMITIDOS`: hosts aceptados, separados por comas (`*` desactiva la comprobación).
  Por defecto `localhost,127.0.0.1`; en Render se añade `RENDER_EXTERNAL_HOSTNAME`.
- `ML_EN_NUBE=1`: añade HSTS y desactiva `/docs`, `/redoc` y `/openapi.json`.
"""

from __future__ import annotations

import os

from starlette.datastructures import MutableHeaders
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send

RUTAS_LIBRES = ("/api/salud",)
HOSTS_POR_DEFECTO = ("localhost", "127.0.0.1")

# Compatible con el build de Vite: scripts y estilos propios; las fuentes vienen de Google Fonts
# y los estilos en línea los emite React (atributo style).
POLITICA_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' data: https://fonts.gstatic.com; "
    "img-src 'self' data: blob:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'"
)

CABECERAS_SEGURIDAD = {
    "Content-Security-Policy": POLITICA_CSP,
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "same-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}
CACHE_ASSETS = "public, max-age=31536000, immutable"


def en_nube() -> bool:
    return os.getenv("ML_EN_NUBE") == "1"


def hosts_permitidos() -> list[str]:
    """Hosts aceptados según `ML_HOSTS_PERMITIDOS` (o los de por defecto)."""
    configurados = [h.strip() for h in os.getenv("ML_HOSTS_PERMITIDOS", "").split(",") if h.strip()]
    hosts = configurados or list(HOSTS_POR_DEFECTO)
    render = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
    if render and render not in hosts:
        hosts.append(render)
    return hosts


class HostsConfiables(TrustedHostMiddleware):
    """Rechaza Host no permitidos, pero deja pasar el healthcheck de la plataforma."""

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope["path"] in RUTAS_LIBRES:
            await self.app(scope, receive, send)
            return
        await super().__call__(scope, receive, send)


class CabecerasSeguridad:
    """Añade las cabeceras de seguridad a toda respuesta y la caché larga a `/assets/`."""

    def __init__(self, app: ASGIApp, hsts: bool = False):
        self.app = app
        self.hsts = hsts

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        path = scope["path"]

        async def enviar(mensaje: Message) -> None:
            if mensaje["type"] == "http.response.start":
                cabeceras = MutableHeaders(scope=mensaje)
                for nombre, valor in CABECERAS_SEGURIDAD.items():
                    cabeceras.setdefault(nombre, valor)
                if self.hsts:
                    cabeceras.setdefault("Strict-Transport-Security", "max-age=31536000")
                if path.startswith("/assets/") and mensaje["status"] == 200:
                    # Los nombres de /assets llevan hash del contenido: pueden cachearse siempre
                    cabeceras.setdefault("Cache-Control", CACHE_ASSETS)
                elif path == "/" or path == "/index.html":
                    cabeceras.setdefault("Cache-Control", "no-cache")
            await send(mensaje)

        await self.app(scope, receive, enviar)


__all__ = [
    "CABECERAS_SEGURIDAD",
    "CACHE_ASSETS",
    "POLITICA_CSP",
    "CabecerasSeguridad",
    "HostsConfiables",
    "en_nube",
    "hosts_permitidos",
]
