"""Puerto para la persistencia y consulta de proyectos académicos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from modular_learning.core.domain.proyectos import HuellaProyecto, Proyecto, TipoProyecto


class ProyectosRepo(ABC):
    """Puerto para la persistencia y consulta del registro de proyectos."""

    @abstractmethod
    def guardar(self, proyecto: Proyecto) -> None:
        """Guarda o actualiza la ficha de un proyecto."""

    @abstractmethod
    def obtener(self, id_proyecto: str) -> Proyecto | None:
        """Busca un proyecto por su identificador único."""

    @abstractmethod
    def listar(self, materia: str | None = None) -> list[Proyecto]:
        """Retorna todos los proyectos registrados, opcionalmente filtrados por materia."""

    @abstractmethod
    def eliminar(self, id_proyecto: str) -> bool:
        """Elimina el proyecto del registro."""

    @abstractmethod
    def vaciar(self) -> int:
        """Vacía todos los proyectos registrados y retorna la cantidad eliminada."""


class InspectorProyectosPort(ABC):
    """Puerto para leer del disco los proyectos de una asignatura sin mandar todo su código."""

    @abstractmethod
    def escanear(self, carpeta_materia: str) -> list[dict[str, Any]]:
        """
        Proyectos dentro de PROYECTO/ (parcial general) o PROYECTOS/PRIMER|SEGUNDO PARCIAL/:
        [{parcial, nombre, ruta, tipo}]. Lista vacía si la carpeta no existe.
        """

    @abstractmethod
    def huella(self, ruta: str) -> HuellaProyecto | None:
        """Fecha de modificación más reciente, número de archivos y hash; None si no existe."""

    @abstractmethod
    def detectar_tipo(self, ruta: str) -> TipoProyecto:
        """Clasifica el proyecto (software, IoT, documental o documento rector)."""

    @abstractmethod
    def extraer_contexto(self, ruta: str) -> str:
        """Árbol de carpetas, README o texto del documento, sin secretos ni dependencias."""


__all__ = ["InspectorProyectosPort", "ProyectosRepo"]
