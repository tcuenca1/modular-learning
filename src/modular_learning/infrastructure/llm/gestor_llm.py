"""Factory / Enrutador de Proveedores LLM."""

import os
from dotenv import load_dotenv

from modular_learning.core.ports.llm import LLMAdapterBase
from modular_learning.infrastructure.llm.gemini_adapter import LLM_GeminiAdapter

load_dotenv()


def obtener_llm() -> LLMAdapterBase:
    """Retorna el adaptador LLM configurado (por defecto Google Gemini)."""
    return LLM_GeminiAdapter()
