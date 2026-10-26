"""Utilidades puras para interpretar respuestas JSON devueltas por un LLM."""

from __future__ import annotations

import json
from typing import Any


def limpiar_bloque_markdown(texto: str) -> str:
    """Elimina delimitadores ```json ... ``` que los LLM suelen añadir alrededor del JSON."""
    limpio = texto.strip()
    if "```json" in limpio:
        limpio = limpio.split("```json", 1)[1]
    elif "```" in limpio:
        limpio = limpio.split("```", 1)[1]
    if "```" in limpio:
        limpio = limpio.split("```", 1)[0]
    return limpio.strip()


def parsear_json_llm(texto: str) -> Any:
    """Parsea la respuesta del LLM como JSON tolerando bloques Markdown."""
    return json.loads(limpiar_bloque_markdown(texto))


__all__ = ["limpiar_bloque_markdown", "parsear_json_llm"]
