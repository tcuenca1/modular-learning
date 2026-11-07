"""Router de tutoría interactiva personalizada."""

from __future__ import annotations

import json
import uuid
from collections.abc import Iterator
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from modular_learning.apps.api.dependencies import (
    get_materias_service,
    get_session_store,
    get_tutoria_service,
)
from modular_learning.apps.api.schemas import Duda, IniciarTutoria
from modular_learning.apps.api.session_store import SessionStore
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.tutoria import SesionTutoria, TutoriaService

router = APIRouter(prefix="/api/tutoria", tags=["tutoria"])


def _obtener_sesion_activa(sesion_id: str, store: SessionStore) -> SesionTutoria:
    sesion = store.obtener_sesion(sesion_id)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión de tutoría no encontrada o expirada.")
    return sesion


@router.post("/iniciar")
def iniciar_tutoria(
    body: IniciarTutoria,
    servicio: Annotated[TutoriaService, Depends(get_tutoria_service)],
    materias_srv: Annotated[MateriasService, Depends(get_materias_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> dict[str, Any]:
    sesion_id = uuid.uuid4().hex
    try:
        sesion = servicio.iniciar_sesion(
            sesion_id=sesion_id,
            materia=body.materia.strip(),
            tema=body.tema.strip(),
            nivel_profundidad=body.nivel_profundidad,
            enfoque=body.enfoque,
            clase_id=body.clase_id,
        )
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    materias_srv.agregar_materia(body.materia.strip())
    store.guardar_sesion(sesion_id, sesion)

    return {
        "sesion_id": sesion_id,
        "materia": sesion.materia,
        "tema": sesion.tema,
        "nivel_profundidad": sesion.nivel_profundidad,
        "pasos": sesion.pasos,
        "materiales_asociados": sesion.materiales_asociados,
        "subtemas_adicionales": sesion.subtemas_adicionales,
        "enfoque": sesion.enfoque,
        "fallos_previos": sesion.fallos_previos,
        "clase_id": sesion.clase_id,
    }


@router.get("/{sesion_id}/paso/{indice}/stream")
def explicar_paso(
    sesion_id: str,
    indice: int,
    servicio: Annotated[TutoriaService, Depends(get_tutoria_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> StreamingResponse:
    """Streaming SSE de la explicación del tutor para un paso."""
    sesion = _obtener_sesion_activa(sesion_id, store)
    if not 0 <= indice < len(sesion.pasos):
        raise HTTPException(status_code=404, detail="Paso inexistente en la sesión.")

    stream_iter = servicio.explicar_paso_stream(sesion, indice)

    def eventos() -> Iterator[str]:
        try:
            for chunk in stream_iter:
                yield f"data: {json.dumps({'chunk': chunk}, ensure_ascii=False)}\n\n"
            yield "event: fin\ndata: {}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        eventos(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/{sesion_id}/duda")
def resolver_duda(
    sesion_id: str,
    body: Duda,
    servicio: Annotated[TutoriaService, Depends(get_tutoria_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> dict[str, str]:
    sesion = _obtener_sesion_activa(sesion_id, store)
    try:
        respuesta = servicio.responder_duda(sesion, body.paso, body.duda.strip())
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return {"respuesta": respuesta}


@router.post("/{sesion_id}/finalizar")
def finalizar_tutoria(
    sesion_id: str,
    servicio: Annotated[TutoriaService, Depends(get_tutoria_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> dict[str, Any]:
    sesion = _obtener_sesion_activa(sesion_id, store)
    try:
        resultado = servicio.finalizar_sesion(sesion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    store.eliminar_sesion(sesion_id)
    return resultado


__all__ = ["router"]
