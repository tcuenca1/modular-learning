"""Router de configuración del sistema."""

from __future__ import annotations

import os
from typing import Annotated, Any

from fastapi import APIRouter, Depends

from modular_learning.apps.api.dependencies import get_configuracion_service
from modular_learning.apps.api.errores import error_cliente, error_interno
from modular_learning.apps.api.schemas import GuardarConfig
from modular_learning.core.application.configuracion import ConfiguracionService

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("")
def obtener_configuracion(
    servicio: Annotated[ConfiguracionService, Depends(get_configuracion_service)],
) -> dict[str, Any]:
    datos = dict(servicio.obtener_ajustes())
    datos["en_nube"] = os.getenv("ML_EN_NUBE") == "1"
    if datos["en_nube"]:
        # En la nube las rutas son del servidor, no del equipo del usuario: no se exponen
        datos["carpeta_material"] = ""
        datos["ruta_obsidian"] = ""
    return datos


@router.post("")
def guardar_configuracion(
    body: GuardarConfig,
    servicio: Annotated[ConfiguracionService, Depends(get_configuracion_service)],
) -> dict[str, Any]:
    try:
        return servicio.guardar_ajustes(body.carpeta_material, body.ruta_obsidian)
    except (FileNotFoundError, ValueError) as e:
        raise error_cliente(e) from e
    except Exception as e:
        raise error_interno(e) from e
