"""Almacén en memoria de sesiones de tutoría activas y quizzes generados."""

from __future__ import annotations

from typing import Any

from modular_learning.core.application.tutoria import SesionTutoria
from modular_learning.infrastructure.persistence.almacen import cuenta_actual


def _clave(identificador: str) -> str:
    """Con login, las sesiones y quizzes son de la cuenta que los creó: otra no puede usarlos."""
    return f"{cuenta_actual() or ''}:{identificador}"


class SessionStore:
    """Adaptador de estado en memoria para la capa API."""

    def __init__(self) -> None:
        self._sesiones: dict[str, SesionTutoria] = {}
        self._quizzes: dict[str, list[dict[str, Any]]] = {}

    def guardar_sesion(self, sesion_id: str, sesion: SesionTutoria) -> None:
        self._sesiones[_clave(sesion_id)] = sesion

    def obtener_sesion(self, sesion_id: str) -> SesionTutoria | None:
        return self._sesiones.get(_clave(sesion_id))

    def eliminar_sesion(self, sesion_id: str) -> SesionTutoria | None:
        return self._sesiones.pop(_clave(sesion_id), None)

    def guardar_quiz(self, quiz_id: str, preguntas: list[dict[str, Any]]) -> None:
        self._quizzes[_clave(quiz_id)] = preguntas

    def obtener_quiz(self, quiz_id: str) -> list[dict[str, Any]] | None:
        return self._quizzes.get(_clave(quiz_id))

    def eliminar_quiz(self, quiz_id: str) -> list[dict[str, Any]] | None:
        return self._quizzes.pop(_clave(quiz_id), None)
