"""Adaptador de entrada web (Driving Adapter) basado en FastAPI.

Ensambla los routers de la API e inyecta el contenedor IoC mediante app.state.
"""

from __future__ import annotations

import logging
import os
import threading
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.gzip import GZipMiddleware

from modular_learning import bootstrap
from modular_learning.apps.api.autenticacion import Autenticacion
from modular_learning.apps.api.routers import (
    auth,
    config,
    guias,
    material,
    materias,
    plugins,
    proyectos,
    quiz,
    repaso,
    silabo,
    stats,
    tutoria,
)
from modular_learning.apps.api.seguridad import (
    CabecerasSeguridad,
    HostsConfiables,
    en_nube,
    hosts_permitidos,
)
from modular_learning.apps.api.session_store import SessionStore
from modular_learning.apps.api.tiempos import MedirTiempos
from modular_learning.infrastructure.persistence.almacen import (
    almacen_global,
    almacen_por_defecto,
    cuentas_activas,
    en_cuenta,
)
from modular_learning.infrastructure.persistence.semilla import sembrar_cuenta

load_dotenv()

logger = logging.getLogger("modular_learning.api")

RUTA_ESTATICOS = Path(__file__).parent / "static"


def _precalentar_almacen() -> None:
    """
    Con Postgres, carga la instantánea de datos en segundo plano al arrancar: así la primera
    petición no paga la consulta y Neon empieza a despertar mientras el servidor termina de iniciar.
    """

    def tarea() -> None:
        try:
            almacen = almacen_global()
            precalentar = getattr(almacen, "precalentar", None)
            if precalentar:
                precalentar()
        except Exception as e:
            logger.warning("No se pudo precalentar el almacén: %s", e)

    threading.Thread(target=tarea, name="precalentar-almacen", daemon=True).start()


def _servicio_de_autenticacion(app: FastAPI, container: bootstrap.Container | None):
    cont = container or bootstrap.get_container()
    app.state.container = cont
    return cont.autenticacion_service


def _preparar_cuentas(app: FastAPI) -> None:
    """Al arrancar: deja lista la cuenta de administrador y, si se pide, sus datos de ejemplo."""
    servicio = app.state.container.autenticacion_service if app.state.container else None
    if servicio is None:
        logger.error("Login activo pero falta ML_CONTRASENA: la API responde 503.")
        return
    identificador = os.getenv("ML_USUARIO", "").strip() or "estudiante"
    admin = servicio.asegurar_admin(
        identificador, os.getenv("ML_NOMBRE_ADMIN", "Administrador"), os.getenv("ML_CONTRASENA", "")
    )
    if os.getenv("ML_SEMBRAR_EJEMPLOS", "").strip().lower() in ("1", "true", "si", "sí"):
        semilla = os.getenv("ML_SEMILLA_DIR", "/app/semilla")
        with en_cuenta(admin.id):
            sembrar_cuenta(almacen_por_defecto(), semilla)


@asynccontextmanager
async def _ciclo_de_vida(app: FastAPI):
    if cuentas_activas():
        try:
            _preparar_cuentas(app)
        except Exception as e:  # no tumbar el servidor: el detalle queda en el log
            logger.error("No se pudo preparar la cuenta de administrador: %s", e, exc_info=e)
    yield


def create_app(
    container: bootstrap.Container | None = None,
    session_store: SessionStore | None = None,
) -> FastAPI:
    """Crea y configura la aplicación FastAPI con dependencias inyectadas en app.state.

    Si no se provee contenedor, se resuelve de forma perezosa con `bootstrap.get_container()`.
    """
    # En la nube la documentación interactiva de la API no se publica
    sin_docs = {"docs_url": None, "redoc_url": None, "openapi_url": None} if en_nube() else {}
    app = FastAPI(
        title="Modular Learning Web", version="2.0.0", lifespan=_ciclo_de_vida, **sin_docs
    )

    _precalentar_almacen()

    # Inyección del contenedor IoC y almacén de sesiones en el estado de la aplicación
    app.state.container = container
    app.state.session_store = session_store or SessionStore()

    # Con login activo (ML_REQUIERE_ACCESO) `/api/` exige sesión por cuenta (ver autenticacion.py)
    if cuentas_activas():
        app.add_middleware(Autenticacion, servicio=_servicio_de_autenticacion(app, container))

    # De dentro hacia fuera: compresión, cabeceras de seguridad y, la primera barrera, el Host
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    app.add_middleware(MedirTiempos)
    app.add_middleware(CabecerasSeguridad, hsts=en_nube())
    app.add_middleware(HostsConfiables, allowed_hosts=hosts_permitidos())

    @app.get("/api/salud", include_in_schema=False)
    def salud() -> dict[str, bool]:
        """Comprobación de vida para el healthcheck de la plataforma; no requiere acceso."""
        return {"ok": True}

    # Registro de routers
    app.include_router(auth.router)
    app.include_router(config.router)
    app.include_router(materias.router)
    app.include_router(tutoria.router)
    app.include_router(quiz.router)
    app.include_router(repaso.router)
    app.include_router(guias.router)
    app.include_router(stats.router)
    app.include_router(silabo.router)
    app.include_router(material.router)
    app.include_router(plugins.router)
    app.include_router(proyectos.router)

    # Rutas estáticas y fallback SPA
    index_html = RUTA_ESTATICOS / "index.html"
    assets_dir = RUTA_ESTATICOS / "assets"

    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    if RUTA_ESTATICOS.exists():
        app.mount("/static", StaticFiles(directory=RUTA_ESTATICOS), name="static")

    aviso_no_compilado = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Modular Learning - Frontend no compilado</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; background: #09090b; color: #f4f4f5; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .card { background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 2.5rem; max-width: 540px; text-align: center; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
    h1 { font-size: 1.5rem; color: #e4e4e7; margin-bottom: 0.75rem; font-weight: 700; }
    p { font-size: 0.875rem; color: #a1a1aa; line-height: 1.6; margin-bottom: 1.25rem; }
    code { background: #27272a; color: #818cf8; padding: 0.25rem 0.6rem; border-radius: 6px; font-family: monospace; font-size: 0.875rem; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Modular Learning - Frontend no compilado</h1>
    <p>El cliente web aún no se ha compilado en la carpeta <code>static/</code>.</p>
    <p>Para compilar el frontend React, ejecuta en la terminal:</p>
    <p><code>cd frontend && npm run build</code></p>
  </div>
</body>
</html>"""

    @app.get("/", include_in_schema=False, response_model=None)
    def index() -> Response:
        if index_html.exists() and assets_dir.exists():
            return FileResponse(index_html)
        return HTMLResponse(content=aviso_no_compilado, status_code=200)

    @app.get("/{full_path:path}", include_in_schema=False, response_model=None)
    def spa_fallback(full_path: str) -> Response:
        if full_path.startswith("api/") or full_path in ("docs", "redoc", "openapi.json"):
            raise HTTPException(status_code=404, detail="Endpoint no encontrado")

        if full_path:
            posible_archivo = RUTA_ESTATICOS / full_path
            if posible_archivo.is_file():
                return FileResponse(posible_archivo)

        if index_html.exists() and assets_dir.exists():
            return FileResponse(index_html)

        return HTMLResponse(content=aviso_no_compilado, status_code=200)

    return app


app = create_app()


def run() -> None:
    """Punto de entrada para el servidor web: `ml-web`."""
    import uvicorn

    host = os.getenv("WEB_HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
    port = int(os.getenv("PORT", os.getenv("WEB_PORT", "8000")))
    uvicorn.run("modular_learning.apps.api.main:app", host=host, port=port, reload=False)


__all__ = ["app", "create_app", "run"]


if __name__ == "__main__":
    run()
