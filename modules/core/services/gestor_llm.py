import os
from dotenv import load_dotenv
from modules.core.ports.llm_base import LLMAdapterBase
from modules.core.adapters.llm_gemini_adapter import LLM_GeminiAdapter

load_dotenv()


def obtener_llm() -> LLMAdapterBase:
    """
    Factory / Enrutador de Proveedores LLM.
    Lee la variable de entorno LLM_PROVIDER y retorna el adaptador correspondiente (Hexagonal).
    Por defecto utiliza Google Gemini.
    """
    proveedor = os.getenv("LLM_PROVIDER", "gemini").strip().lower()

    if proveedor == "gemini":
        return LLM_GeminiAdapter()
    # elif proveedor == "openai":
    #     return LLM_OpenAIAdapter()
    # elif proveedor == "anthropic":
    #     return LLM_AnthropicAdapter()
    else:
        # Fallback por defecto a Gemini
        return LLM_GeminiAdapter()
