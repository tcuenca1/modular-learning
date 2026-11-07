"""Contrato de persistencia de las guías de estudio offline."""

from __future__ import annotations

from abc import ABC, abstractmethod

from modular_learning.core.domain.guia_offline import GuiaOffline


class GuiasRepo(ABC):
    """Puerto de repositorio de guías offline."""

    @abstractmethod
    def listar(self) -> list[GuiaOffline]:
        """Retorna todas las guías, de la más reciente a la más antigua."""

    @abstractmethod
    def obtener(self, guia_id: str) -> GuiaOffline | None:
        """Retorna la guía con ese identificador, si existe."""

    @abstractmethod
    def guardar(self, guia: GuiaOffline) -> None:
        """Crea o actualiza una guía."""

    @abstractmethod
    def eliminar(self, ids: list[str]) -> int:
        """Elimina las guías con esos identificadores; retorna cuántas había."""


class ExportadorPdfPort(ABC):
    """Puerto para la generación y renderizado de guías de estudio en formato PDF."""

    @abstractmethod
    def exportar_guia(self, guia: GuiaOffline) -> bytes:
        """Genera el contenido binario del PDF para la guía especificada."""


__all__ = ["ExportadorPdfPort", "GuiasRepo"]
