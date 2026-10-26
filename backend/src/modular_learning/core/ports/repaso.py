"""Contratos de persistencia para el repaso espaciado y el historial de estudio."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from modular_learning.core.domain.repaso_espaciado import Tarjeta


class TarjetasRepo(ABC):
    """Puerto de repositorio de tarjetas de repaso espaciado."""

    @abstractmethod
    def listar(self) -> list[Tarjeta]:
        """Retorna todas las tarjetas registradas."""

    @abstractmethod
    def obtener(self, tarjeta_id: str) -> Tarjeta | None:
        """Retorna la tarjeta con ese identificador, si existe."""

    @abstractmethod
    def guardar(self, tarjeta: Tarjeta) -> None:
        """Crea o actualiza una tarjeta."""


class HistorialRepo(ABC):
    """Puerto de repositorio del historial de actividad de estudio por clase."""

    @abstractmethod
    def registrar(self, evento: dict[str, Any]) -> None:
        """Añade un evento (tutoría o repaso) al historial."""

    @abstractmethod
    def listar(self, materia: str | None = None, tema: str | None = None) -> list[dict[str, Any]]:
        """Retorna los eventos, del más reciente al más antiguo, filtrados opcionalmente."""


__all__ = ["HistorialRepo", "TarjetasRepo"]
