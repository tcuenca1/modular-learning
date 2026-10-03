from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class LLMAdapterBase(ABC):
    """
    Puerto base (Abstract Base Class) para la abstracción de Modelos de Lenguaje (LLM).
    Permite desacoplar la lógica de negocio de proveedores específicos (Gemini, OpenAI, Anthropic, etc.).
    """

    @abstractmethod
    def generar_texto(self, prompt: str, contexto_previo: Optional[List[dict]] = None) -> str:
        """Envía un prompt de texto y retorna la respuesta generada, soportando historial opcional."""
        pass

    @abstractmethod
    def generar_texto_con_archivo(self, archivo_inline: dict, prompt: str) -> str:
        """Envía un archivo multimedia (PDF/imagen) junto con un prompt y retorna la respuesta generada."""
        pass

    @abstractmethod
    def generar_json_estructurado(self, prompt: str) -> Dict[str, Any]:
        """Envía un prompt exigiendo un Structured Output en formato JSON y retorna el diccionario parseado."""
        pass
