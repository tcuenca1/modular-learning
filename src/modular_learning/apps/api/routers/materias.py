"""Router para la gestión de asignaturas y cronogramas de clases."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from modular_learning.apps.api.dependencies import get_materias_service
from modular_learning.apps.api.schemas import NuevaMateria
from modular_learning.core.application.materias import MateriasService

router = APIRouter(prefix="/api/materias", tags=["materias"])


@router.get("")
def listar_materias(
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, list[str]]:
    return {"materias": servicio.listar_materias()}


@router.post("", status_code=201)
def crear_materia(
    body: NuevaMateria,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, list[str]]:
    materias = servicio.agregar_materia(body.nombre)
    return {"materias": materias}


@router.get("/{materia}/clases")
def proximas_clases(
    materia: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, list[dict[str, Any]]]:
    return {"clases": servicio.obtener_proximas_clases(materia)}
