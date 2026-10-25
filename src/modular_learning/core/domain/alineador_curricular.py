"""Lógica de dominio para alinear un material ingestado con la clase más afín del cronograma."""

from __future__ import annotations

import json
import logging
from typing import Any

from modular_learning.core.domain.json_llm import parsear_json_llm
from modular_learning.core.ports.llm import LLMPort

logger = logging.getLogger(__name__)

UMBRAL_AFINIDAD = 60


def _resultado_por_defecto(clase: int, peso: int, justificacion: str) -> dict[str, Any]:
    return {
        "clase_asignada": clase,
        "peso_afinidad": peso,
        "justificacion": justificacion,
        "subtemas_a_incorporar": [],
        "asignado": None,  # No evaluado: no se modifica ni se registra nada
    }


def _construir_prompt(clases: list[dict[str, Any]], contenido_md: str, nombre_archivo: str) -> str:
    resumen_clases = "\n".join(
        f"Clase {idx} (Fecha: {c.get('fecha', 'S/F')}): {c.get('tema', 'Sin tema')} - "
        f"Contenido: {c.get('contenido', '')}"
        for idx, c in enumerate(clases, 1)
    )
    return (
        "Eres un Arquitecto de Software y Evaluador Curricular experto. "
        "A continuación tienes la lista completa de clases oficiales del cronograma de la materia y un extracto de los apuntes de un material recién ingestado.\n\n"
        f"CRONOGRAMA OFICIAL:\n{resumen_clases}\n\n"
        f"EXTRACTO DEL NUEVO MATERIAL ({nombre_archivo}):\n{contenido_md[:4000]}\n\n"
        "TAREA:\n"
        "Evalúa y asigna un peso de afinidad (0 a 100) contra cada clase del cronograma y determina cuál es la clase más afín. "
        "Identifica también los subtemas técnicos o herramientas nuevos que aporta el material.\n"
        "Devuelve ÚNICAMENTE un objeto JSON estructurado con este formato estricto:\n"
        "{\n"
        '  "clase_asignada": número_de_clase (entero, ej: 3),\n'
        '  "peso_afinidad": número_de_0_a_100 (entero, ej: 85),\n'
        '  "justificacion": "Breve explicación de por qué este material corresponde a esta clase.",\n'
        '  "subtemas_a_incorporar": ["subtema1", "subtema2"]\n'
        "}"
    )


def asignar_material_a_clase(
    clases: list[dict[str, Any]],
    contenido_md: str,
    nombre_archivo: str,
    llm: LLMPort,
) -> dict[str, Any]:
    """
    Evalúa con el LLM la afinidad del material contra cada clase del cronograma.

    Si la afinidad alcanza el umbral, modifica `clases` in situ añadiendo el material y los
    subtemas a la clase elegida y retorna `asignado=True`. Con afinidad baja retorna
    `asignado=False` para que el caso de uso lo registre como material transversal, y
    `asignado=None` si no pudo evaluarse.
    La persistencia del cronograma es responsabilidad del llamador.
    """
    if not clases:
        return _resultado_por_defecto(0, 0, "Cronograma vacío o inexistente")

    prompt = _construir_prompt(clases, contenido_md, nombre_archivo)
    try:
        texto_respuesta = llm.generar_texto(prompt)
    except Exception:
        try:
            texto_respuesta = json.dumps(llm.generar_json_estructurado(prompt))
        except Exception as err:
            logger.warning("Error al consultar la IA para alinear '%s': %s", nombre_archivo, err)
            return _resultado_por_defecto(1, 50, "Error de comunicación con IA")

    try:
        resultado = parsear_json_llm(texto_respuesta)
        if not isinstance(resultado, dict):
            raise ValueError("El JSON parseado no es un diccionario.")
        peso = int(resultado.get("peso_afinidad", 0))
        clase_num = int(resultado.get("clase_asignada", 1))
    except (ValueError, TypeError) as parse_err:
        logger.error("Respuesta de alineación no válida: %s\n%s", parse_err, texto_respuesta)
        return _resultado_por_defecto(1, 50, f"Error de parseo JSON: {parse_err}")

    subtemas = resultado.get("subtemas_a_incorporar", [])
    if not isinstance(subtemas, list):
        subtemas = []

    resultado.update(peso_afinidad=peso, clase_asignada=clase_num, subtemas_a_incorporar=subtemas)
    resultado["asignado"] = peso >= UMBRAL_AFINIDAD
    logger.debug("IA evaluó Clase %s con afinidad %s%%", clase_num, peso)

    if resultado["asignado"]:
        indice = clase_num - 1
        clase_target = clases[indice] if 0 <= indice < len(clases) else clases[0]
        materiales = clase_target.setdefault("materiales_asociados", [])
        if nombre_archivo not in materiales:
            materiales.append(nombre_archivo)
        existentes = clase_target.setdefault("subtemas_adicionales", [])
        for sub in subtemas:
            sub_str = str(sub).strip()
            if sub_str and sub_str not in existentes:
                existentes.append(sub_str)

    return resultado


def item_material_transversal(nombre_archivo: str, resultado: dict[str, Any]) -> dict[str, Any]:
    """Construye la entrada de material transversal para un material sin clase afín."""
    return {
        "archivo": nombre_archivo,
        "justificacion": resultado.get("justificacion", ""),
        "subtemas": resultado.get("subtemas_a_incorporar", []),
        "peso_afinidad": resultado.get("peso_afinidad", 0),
    }


__all__ = ["UMBRAL_AFINIDAD", "asignar_material_a_clase", "item_material_transversal"]
