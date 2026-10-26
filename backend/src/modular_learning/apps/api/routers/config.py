"""Router de configuración del sistema."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import get_configuracion_service
from modular_learning.apps.api.schemas import GuardarConfig
from modular_learning.core.application.configuracion import ConfiguracionService

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("")
def obtener_configuracion(
    servicio: Annotated[ConfiguracionService, Depends(get_configuracion_service)],
) -> dict[str, Any]:
    return servicio.obtener_ajustes()


@router.post("")
def guardar_configuracion(
    body: GuardarConfig,
    servicio: Annotated[ConfiguracionService, Depends(get_configuracion_service)],
) -> dict[str, Any]:
    try:
        return servicio.guardar_ajustes(body.carpeta_material, body.ruta_obsidian)
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(400, str(e)) from e
    except Exception as e:
        raise HTTPException(500, str(e)) from e
