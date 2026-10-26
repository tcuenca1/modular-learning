"""Router para la gestión y actualización de plugins prácticos interactivos."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import get_plugins_service
from modular_learning.apps.api.schemas import ActualizarPlugin
from modular_learning.core.application.plugins import PluginsService

router = APIRouter(prefix="/api/plugins", tags=["plugins"])

OPCIONES_PLUGIN = [
    "Cisco (Actividades)",
    "Web (Proyectos)",
    "Node-RED (Flujos JSON)",
    "Todos",
]


@router.get("")
def listar_plugins() -> dict[str, list[str]]:
    return {"opciones": OPCIONES_PLUGIN}


@router.post("/actualizar")
def actualizar_plugin(
    body: ActualizarPlugin,
    servicio: Annotated[PluginsService, Depends(get_plugins_service)],
) -> dict[str, Any]:
    if body.seleccion not in OPCIONES_PLUGIN:
        raise HTTPException(
            status_code=400,
            detail=f"Plugin no válido. Opciones permitidas: {', '.join(OPCIONES_PLUGIN)}.",
        )
    try:
        resultado = servicio.actualizar_plugin(body.seleccion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return {"seleccion": body.seleccion, "resultado": resultado}
