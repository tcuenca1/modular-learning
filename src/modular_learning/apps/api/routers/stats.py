"""Router de telemetría y dashboard de avance académico."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from modular_learning.apps.api.dependencies import get_telemetria_service
from modular_learning.core.application.telemetria import TelemetriaService

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
def estadisticas(
    servicio: Annotated[TelemetriaService, Depends(get_telemetria_service)],
) -> dict[str, Any]:
    return servicio.obtener_estadisticas()
