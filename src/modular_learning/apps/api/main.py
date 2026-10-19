"""Adaptador de entrada web (Driving Adapter) basado en FastAPI.

Ensambla los routers de la API e inyecta el contenedor IoC mediante app.state.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
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

    # Rutas estáticas y frontend
    if RUTA_ESTATICOS.exists():
        index_html = RUTA_ESTATICOS / "index.html"
        if index_html.exists():

            @app.get("/", include_in_schema=False)
            def index() -> FileResponse:
                return FileResponse(index_html)

        app.mount("/static", StaticFiles(directory=RUTA_ESTATICOS), name="static")

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
