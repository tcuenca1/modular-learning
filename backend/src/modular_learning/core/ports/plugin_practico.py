from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PluginPracticoBase(ABC):
    """
    Puerto base (Abstract Base Class) para la arquitectura hexagonal de plugins prácticos.
    Define la interfaz estándar que todos los adaptadores de materias prácticas deben implementar.
    """

    @abstractmethod
    def obtener_instrucciones_ia(self) -> str:
        """Devuelve las directivas y restricciones de system prompt específicas de la herramienta práctica."""

    @abstractmethod
    def generar_ejercicio_base(self, tema: str) -> str:
        """Devuelve el contexto técnico inicial, plantilla o boilerplate práctico para el tema indicado."""

    @abstractmethod
    def guardar_contexto_extraido(self, metadatos: str) -> None:
        """Guarda y acumula contexto técnico extraído de materiales ingestados (historial máx. 5)."""

    @abstractmethod
    def cargar_contexto_reciente(self) -> str:
        """Carga el contexto técnico reciente guardado para inyectarlo al system prompt de la IA."""


class PluginConfigRepoPort(ABC):
    """Puerto para persistir la configuración de carpetas y materias de los plugins prácticos."""

    @abstractmethod
    def obtener_configuraciones(self) -> dict[str, dict[str, Any]]:
        """Retorna todas las configuraciones almacenadas por clave de plugin."""

    @abstractmethod
    def guardar_configuracion(
        self, clave: str, carpeta: str | None = None, materia: str | None = None
    ) -> dict[str, Any]:
        """Guarda o actualiza la configuración para el plugin indicado."""


__all__ = ["PluginConfigRepoPort", "PluginPracticoBase"]
