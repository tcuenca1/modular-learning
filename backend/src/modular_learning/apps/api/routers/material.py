"""Router para la ingesta multimodal de material y sincronización con Obsidian."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
from collections.abc import Iterator
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from modular_learning.apps.api.dependencies import (
    get_ingesta_service,
    get_materias_service,
)
from modular_learning.apps.api.schemas import SincronizarMaterial, VaciarMaterialesRequest
from modular_learning.core.application.ingesta import EXTENSIONES_MATERIAL, IngestaService
from modular_learning.core.application.materias import MateriasService

router = APIRouter(prefix="/api/material", tags=["material"])


@router.get("/registrados")
def listar_materiales_registrados(
    servicio: Annotated[IngestaService, Depends(get_ingesta_service)],
) -> dict[str, list[dict[str, Any]]]:
    return {"materiales": servicio.listar_materiales_ingestados()}


@router.post("/vaciar")
def vaciar_materiales(
    body: VaciarMaterialesRequest,
    servicio: Annotated[IngestaService, Depends(get_ingesta_service)],
) -> dict[str, Any]:
    resultado = servicio.vaciar_materiales(borrar_notas_obsidian=body.borrar_notas_obsidian)
    return {"ok": True, "resultado": resultado}


@router.delete("/{nombre_archivo:path}")
def eliminar_material(
    nombre_archivo: str,
    servicio: Annotated[IngestaService, Depends(get_ingesta_service)],
    borrar_nota: bool = True,
) -> dict[str, Any]:
    eliminado = servicio.eliminar_material(nombre_archivo, borrar_nota=borrar_nota)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Material no encontrado en el registro.")
    return {"ok": True, "eliminado": eliminado}


@router.get("/escanear")
def escanear_material(
    servicio: Annotated[IngestaService, Depends(get_ingesta_service)],
    materias_srv: Annotated[MateriasService, Depends(get_materias_service)],
    materia: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    materias = [materia] if materia and materia != "__todas__" else materias_srv.listar_materias()
    return {"escaneos": servicio.escanear(materias)}


@router.post("/sincronizar/stream")
def sincronizar_material_stream(
    body: SincronizarMaterial,
    servicio: Annotated[IngestaService, Depends(get_ingesta_service)],
    materias_srv: Annotated[MateriasService, Depends(get_materias_service)],
) -> StreamingResponse:
    materias = [body.materia] if body.materia != "__todas__" else materias_srv.listar_materias()

    def eventos() -> Iterator[str]:
        try:
            for ev in servicio.ingestar_pendientes_stream(materias):
                yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"
            yield "event: fin\ndata: {}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        eventos(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/ingestar")
def ingestar_material(
    archivo: Annotated[UploadFile, File()],
    materia: Annotated[str, Form()],
    servicio: Annotated[IngestaService, Depends(get_ingesta_service)],
    materias_srv: Annotated[MateriasService, Depends(get_materias_service)],
    tipo: Annotated[str, Form()] = "material_complementario",
) -> dict[str, Any]:
    nombre = os.path.basename(archivo.filename or "material")
    ext = os.path.splitext(nombre)[1].lower()
    if ext not in EXTENSIONES_MATERIAL:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado ({ext}). Formatos válidos: {', '.join(EXTENSIONES_MATERIAL)}.",
        )
    if not materia.strip():
        raise HTTPException(status_code=400, detail="Debes indicar la asignatura.")

    materia_limpia = materia.strip()
    materias_srv.agregar_materia(materia_limpia)

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, nombre)
        with open(ruta, "wb") as f:
            shutil.copyfileobj(archivo.file, f)
        try:
            return servicio.ingestar_archivo(ruta, nombre, materia_limpia, tipo)
        except (ValueError, FileNotFoundError) as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e


__all__ = ["router"]
