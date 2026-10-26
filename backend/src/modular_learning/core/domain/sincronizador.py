"""Lógica de dominio para sincronización y enriquecimiento de subtemas curriculares."""

from __future__ import annotations

import json
import logging
from typing import Any

from modular_learning.core.domain.json_llm import parsear_json_llm
from modular_learning.core.ports.llm import LLMPort

logger = logging.getLogger(__name__)


def extraer_y_fusionar_subtemas(
    cronograma_data: list[dict[str, Any]], contenido_md: str, llm: LLMPort
) -> int:
    """
    Envía el cronograma oficial y los apuntes a la IA para extraer conceptos/subtemas técnicos
    no incluidos en el cronograma, y los fusiona in situ en `cronograma_data`.
    Retorna la cantidad de nuevos subtemas inyectados; la persistencia corre por cuenta del llamador.
    """
    if not cronograma_data:
        return 0

    cronograma_str = json.dumps(cronograma_data, indent=2, ensure_ascii=False)

    prompt = (
        "Aquí tienes el cronograma oficial de la materia y unos apuntes recién extraídos. "
        "Identifica qué conceptos técnicos, subtemas o herramientas aparecen en los apuntes que "
        "NO estén mencionados explícitamente en el cronograma. "
        "Devuelve ÚNICAMENTE un JSON estructurado con el formato: "
        '[{"fecha_o_tema_relacionado": "...", "nuevos_subtemas": ["subtema1", "subtema2"]}].\n\n'
        f"Cronograma Oficial:\n{cronograma_str}\n\n"
        f"Apuntes Nuevos:\n{contenido_md}"
    )

    try:
        resultado_json = llm.generar_json_estructurado(prompt)
    except Exception:
        try:
            resultado_json = parsear_json_llm(llm.generar_texto(prompt))
        except Exception as e:
            logger.warning("No se pudo parsear la respuesta de la IA como JSON: %s", e)
            return 0

    if not isinstance(resultado_json, list):
        return 0

    subtemas_nuevos_totales = 0

    for item in resultado_json:
        if not isinstance(item, dict):
            continue
        ref = str(item.get("fecha_o_tema_relacionado", "")).strip().lower()
        nuevos = item.get("nuevos_subtemas", [])
        if not nuevos or not isinstance(nuevos, list):
            continue

        encontrado = False
        for clase in cronograma_data:
            fecha_clase = str(clase.get("fecha", "")).strip().lower()
            tema_clase = str(clase.get("tema", "")).strip().lower()

            if ref and (ref == fecha_clase or ref in tema_clase or tema_clase in ref):
                if "subtemas_adicionales" not in clase:
                    clase["subtemas_adicionales"] = []
                for sub in nuevos:
                    sub_str = str(sub).strip()
                    if sub_str and sub_str not in clase["subtemas_adicionales"]:
                        clase["subtemas_adicionales"].append(sub_str)
                        subtemas_nuevos_totales += 1
                encontrado = True

        if not encontrado and cronograma_data:
            clase_target = next(
                (c for c in cronograma_data if c.get("estado", "").lower() == "pendiente"),
                cronograma_data[-1],
            )
            if "subtemas_adicionales" not in clase_target:
                clase_target["subtemas_adicionales"] = []
            for sub in nuevos:
                sub_str = str(sub).strip()
                if sub_str and sub_str not in clase_target["subtemas_adicionales"]:
                    clase_target["subtemas_adicionales"].append(sub_str)
                    subtemas_nuevos_totales += 1

    return subtemas_nuevos_totales


__all__ = ["extraer_y_fusionar_subtemas"]
