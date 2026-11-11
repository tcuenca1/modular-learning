"""Router para la gestión y actualización de plugins prácticos interactivos."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import get_plugins_service
from modular_learning.apps.api.errores import error_cliente, error_interno
from modular_learning.apps.api.schemas import ActualizarPlugin, ConfigurarPlugin
from modular_learning.core.application.plugins import PluginsService

router = APIRouter(prefix="/api/plugins", tags=["plugins"])

OPCIONES_PLUGIN = [
    "Cisco (Actividades)",
    "Web (Proyectos)",
    "Node-RED (Flujos JSON)",
    "Todos",
]


@router.get("")
def listar_plugins(
    servicio: Annotated[PluginsService, Depends(get_plugins_service)],
) -> dict[str, Any]:
    return {
        "opciones": OPCIONES_PLUGIN,
        "plugins": servicio.listar_info_plugins(),
    }


@router.post("/config")
def configurar_plugin(
    body: ConfigurarPlugin,
    servicio: Annotated[PluginsService, Depends(get_plugins_service)],
) -> dict[str, Any]:
    try:
        config = servicio.guardar_configuracion_plugin(body.clave, body.carpeta, body.materia)
    except ValueError as e:
        raise error_cliente(e) from e
    return {"ok": True, "config": config, "plugins": servicio.listar_info_plugins()}


@router.post("/actualizar")
def actualizar_plugin(
    body: ActualizarPlugin,
    servicio: Annotated[PluginsService, Depends(get_plugins_service)],
) -> dict[str, Any]:
    opciones_permitidas = OPCIONES_PLUGIN + ["cisco", "nodered", "web", "todos"]
    if body.seleccion not in opciones_permitidas and body.seleccion.lower() not in [
        o.lower() for o in opciones_permitidas
    ]:
        raise HTTPException(
            status_code=400,
            detail=f"Plugin no válido. Opciones permitidas: {', '.join(OPCIONES_PLUGIN)}.",
        )
    try:
        resultado = servicio.actualizar_plugin(body.seleccion, body.carpeta_override)
    except ValueError as e:
        raise error_cliente(e) from e
    except Exception as e:
        raise error_interno(e) from e

    return {"seleccion": body.seleccion, "resultado": resultado}
