"""Almacén en memoria de sesiones de tutoría activas y quizzes generados."""

from __future__ import annotations

from typing import Any

from modular_learning.core.application.tutoria import SesionTutoria


class SessionStore:
    """Adaptador de estado en memoria para la capa API."""

    def __init__(self) -> None:
        self._sesiones: dict[str, SesionTutoria] = {}
        self._quizzes: dict[str, list[dict[str, Any]]] = {}

    def guardar_sesion(self, sesion_id: str, sesion: SesionTutoria) -> None:
        self._sesiones[sesion_id] = sesion

    def obtener_sesion(self, sesion_id: str) -> SesionTutoria | None:
        return self._sesiones.get(sesion_id)

    def eliminar_sesion(self, sesion_id: str) -> SesionTutoria | None:
        return self._sesiones.pop(sesion_id, None)

    def guardar_quiz(self, quiz_id: str, preguntas: list[dict[str, Any]]) -> None:
        self._quizzes[quiz_id] = preguntas

    def obtener_quiz(self, quiz_id: str) -> list[dict[str, Any]] | None:
        return self._quizzes.get(quiz_id)

    def eliminar_quiz(self, quiz_id: str) -> list[dict[str, Any]] | None:
        return self._quizzes.pop(quiz_id, None)
