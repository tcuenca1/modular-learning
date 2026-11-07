"""Router para la gestión, inspección y trazabilidad de proyectos académicos."""

from __future__ import annotations

import os
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import (
    get_configuracion_service,
    get_materias_service,
    get_proyectos_service,
)
from modular_learning.apps.api.schemas import IngestarProyectoRequest
from modular_learning.core.application.configuracion import ConfiguracionService
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.proyectos import ProyectosService

router = APIRouter(prefix="/api/proyectos", tags=["proyectos"])


@router.get("")
def listar_proyectos(
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
    materia: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    proyectos = servicio.listar_proyectos(materia)
    return {"proyectos": [p.a_dict() for p in proyectos]}


@router.get("/escanear")
def escanear_proyectos_disponibles(
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
    config_srv: Annotated[ConfiguracionService, Depends(get_configuracion_service)],
    materias_srv: Annotated[MateriasService, Depends(get_materias_service)],
    materia: str | None = None,
) -> dict[str, Any]:
    ruta_material = config_srv.carpeta_material()
    materias = [materia] if materia and materia != "__todas__" else materias_srv.listar_materias()

    todos_detectados: list[dict[str, Any]] = []
    for m in materias:
        carpeta_m = os.path.join(ruta_material, m)
        detectados = servicio.escanear_proyectos_en_carpeta(m, carpeta_m)
        todos_detectados.extend(detectados)

    return {"candidatos": todos_detectados}


@router.get("/{id_proyecto:path}/estado")
def verificar_estado_proyecto(
    id_proyecto: str,
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
) -> dict[str, Any]:
    estado = servicio.verificar_estado_proyecto(id_proyecto)
    if not estado.get("existe") and estado.get("estado") == "no_encontrado":
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return estado


@router.get("/{id_proyecto:path}")
def obtener_proyecto(
    id_proyecto: str,
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
) -> dict[str, Any]:
    proyecto = servicio.obtener_proyecto(id_proyecto)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return {"proyecto": proyecto.a_dict()}


@router.post("/ingestar")
def ingestar_proyecto(
    body: IngestarProyectoRequest,
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
) -> dict[str, Any]:
    try:
        proyecto = servicio.analizar_e_ingestar_proyecto(
            materia=body.materia,
            nombre_proyecto=body.nombre,
            parcial=body.parcial,  # type: ignore[arg-type]
            ruta_origen=body.ruta,
            tipo_forzado=body.tipo,  # type: ignore[arg-type]
        )
        return {"ok": True, "proyecto": proyecto.a_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{id_proyecto:path}/actualizar")
def actualizar_proyecto(
    id_proyecto: str,
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
) -> dict[str, Any]:
    try:
        proyecto = servicio.actualizar_proyecto(id_proyecto)
        return {"ok": True, "proyecto": proyecto.a_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{id_proyecto:path}")
def eliminar_proyecto(
    id_proyecto: str,
    servicio: Annotated[ProyectosService, Depends(get_proyectos_service)],
) -> dict[str, Any]:
    ok = servicio.eliminar_proyecto(id_proyecto)
    if not ok:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado.")
    return {"ok": True, "eliminado": id_proyecto}


__all__ = ["router"]
