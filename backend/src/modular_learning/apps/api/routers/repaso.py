"""Router de repaso espaciado (preguntas vencidas) e historial de estudio por clase."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import get_repaso_service, get_session_store
from modular_learning.apps.api.routers.quiz import publicar_quiz
from modular_learning.apps.api.session_store import SessionStore
from modular_learning.core.application.repaso import RepasoService

router = APIRouter(prefix="/api/repaso", tags=["repaso"])


@router.get("/resumen")
def resumen(
    servicio: Annotated[RepasoService, Depends(get_repaso_service)],
) -> dict[str, Any]:
    return servicio.resumen()


@router.get("/pendientes")
def repaso_pendiente(
    servicio: Annotated[RepasoService, Depends(get_repaso_service)],
    store: Annotated[SessionStore, Depends(get_session_store)],
) -> dict[str, Any]:
    """Crea un quiz con las preguntas cuya fecha de repaso ya llegó (sin llamar al LLM)."""
    preguntas = servicio.preguntas_pendientes()
    if not preguntas:
        raise HTTPException(status_code=404, detail="No tienes preguntas pendientes de repaso hoy.")
    return publicar_quiz(store, preguntas)


@router.get("/historial")
def historial(
    servicio: Annotated[RepasoService, Depends(get_repaso_service)],
    materia: str | None = None,
    tema: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    return {"eventos": servicio.historial(materia, tema)}
