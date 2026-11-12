from abc import ABC, abstractmethod
from typing import Any


class LLMNoDisponible(RuntimeError):
    """
    El modelo no pudo responder por un problema pasajero (saturación, caída, límite de uso) aun
    después de reintentar. El mensaje es apto para mostrarlo al estudiante.
    """

    def __init__(
        self,
        mensaje: str = (
            "El servicio de IA está saturado en este momento. "
            "Espera unos segundos e inténtalo de nuevo."
        ),
    ):
        super().__init__(mensaje)


class LLMAdapterBase(ABC):
    """
    Puerto base (Abstract Base Class) para la abstracción de Modelos de Lenguaje (LLM).
    Permite desacoplar la lógica de negocio de proveedores específicos (Gemini, OpenAI, Anthropic, etc.).
    """

    @abstractmethod
    def generar_texto(self, prompt: str, contexto_previo: list[dict] | None = None) -> str:
        """Envía un prompt de texto y retorna la respuesta generada, soportando historial opcional."""

    @abstractmethod
    def generar_texto_con_archivo(self, archivo_inline: dict, prompt: str) -> str:
        """Envía un archivo multimedia (PDF/imagen) junto con un prompt y retorna la respuesta generada.

        `archivo_inline` acepta {"mime_type", "path"} y opcionalmente "data" (bytes); si no se
        proveen bytes, el adaptador lee el archivo desde "path".
        """

    @abstractmethod
    def generar_json_estructurado(self, prompt: str) -> dict[str, Any]:
        """Envía un prompt exigiendo un Structured Output en formato JSON y retorna el diccionario parseado."""

    @abstractmethod
    def generar_respuesta_stream(self, prompt: str, contexto_previo: list[dict] | None = None):
        """Envía un prompt y retorna un generador que produce chunks de texto en tiempo real (streaming)."""


LLMPort = LLMAdapterBase

__all__ = ["LLMAdapterBase", "LLMNoDisponible", "LLMPort"]
