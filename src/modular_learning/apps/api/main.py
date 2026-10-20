"""Adaptador de entrada web (Driving Adapter) basado en FastAPI.

Ensambla los routers de la API e inyecta el contenedor IoC mediante app.state.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles

from modular_learning import bootstrap
from modular_learning.apps.api.routers import (
    config,
    material,
    materias,
    plugins,
    quiz,
    silabo,
    stats,
    tutoria,
)
from modular_learning.apps.api.session_store import session_store
from modular_learning.core.application import (
    configuracion as servicio_config,
)
from modular_learning.core.application import (
    evaluacion as motor_evaluacion,
)
from modular_learning.core.application import (
    ingesta as servicio_ingesta,
)
from modular_learning.core.application import (
    plugins as gestor_plugins,
)
from modular_learning.core.application import (
    silabo as servicio_silabo,
)
from modular_learning.core.application import (
    telemetria,
)
from modular_learning.core.application import (
    tutoria as servicio_tutoria,
)
from modular_learning.infrastructure.persistence import json_repositorios as gestor_archivos

load_dotenv()

RUTA_ESTATICOS = Path(__file__).parent / "static"

# Compatibilidad con accesos directos al almacén de sesiones y quizzes
SESIONES = session_store._sesiones
QUIZZES = session_store._quizzes


def create_app(container: bootstrap.Container | None = None) -> FastAPI:
    """Crea y configura la aplicación FastAPI con dependencias inyectadas en app.state."""
    app = FastAPI(title="Modular Learning Web", version="2.0.0")

    # Inyección del contenedor IoC y almacén de sesiones en el estado de la aplicación
    app.state.container = container
    app.state.session_store = session_store

    # Registro de routers
    app.include_router(config.router)
    app.include_router(materias.router)
    app.include_router(tutoria.router)
    app.include_router(quiz.router)
    app.include_router(stats.router)
    app.include_router(silabo.router)
    app.include_router(material.router)
    app.include_router(plugins.router)

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

    host = os.getenv("WEB_HOST", "127.0.0.1")
    port = int(os.getenv("WEB_PORT", "8000"))
    uvicorn.run("modular_learning.apps.api.main:app", host=host, port=port, reload=False)


__all__ = [
    "QUIZZES",
    "SESIONES",
    "app",
    "bootstrap",
    "create_app",
    "gestor_archivos",
    "gestor_plugins",
    "motor_evaluacion",
    "run",
    "servicio_config",
    "servicio_ingesta",
    "servicio_silabo",
    "servicio_tutoria",
    "telemetria",
]


if __name__ == "__main__":
    run()
