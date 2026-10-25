"""Router para el motor de recuerdo activo y evaluación formativa (quiz)."""

from __future__ import annotations

import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import (
    get_evaluacion_service,
    get_session_store,
)
from modular_learning.apps.api.schemas import RespuestaQuiz
from modular_learning.apps.api.session_store import SessionStore
from modular_learning.core.application.evaluacion import EvaluacionService

router = APIRouter(prefix="/api/quiz", tags=["quiz"])

CAMPOS_PUBLICOS = ("enunciado", "opciones", "materia", "tema")


def publicar_quiz(store: SessionStore, preguntas: list[dict[str, Any]]) -> dict[str, Any]:
    """Guarda el quiz completo en sesión y expone al cliente las preguntas sin la respuesta."""
    quiz_id = uuid.uuid4().hex
    store.guardar_quiz(quiz_id, preguntas)
    publicas = [{campo: p.get(campo, "") for campo in CAMPOS_PUBLICOS} for p in preguntas]
    return {"quiz_id": quiz_id, "preguntas": publicas}


@router.get("/generar")
def generar_quiz(
    servicio: Annotated[EvaluacionService, Depends(get_evaluacion_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> dict[str, Any]:
    try:
        preguntas = servicio.generar_quiz()
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    return publicar_quiz(store, preguntas)


@router.post("/evaluar")
def evaluar_quiz(
    body: RespuestaQuiz,
    servicio: Annotated[EvaluacionService, Depends(get_evaluacion_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> dict[str, Any]:
    preguntas = store.obtener_quiz(body.quiz_id)
    if preguntas is None:
        raise HTTPException(status_code=404, detail="Quiz no encontrado o expirado.")

    resultado = servicio.evaluar_respuestas(preguntas, body.respuestas)
    store.eliminar_quiz(body.quiz_id)
    return resultado
