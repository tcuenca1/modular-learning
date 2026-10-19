"""
Servicio de aplicación de Tutoría.

Encapsula la lógica del flujo `ml init` (roadmap, explicación por paso, dudas y guía final)
sin depender de la consola ni de HTTP, de modo que cualquier adaptador de entrada
(CLI, Web, etc.) pueda reutilizarla.
"""

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from modular_learning.core.application import configuracion as servicio_config
from modular_learning.core.application import plugins as gestor_plugins
from modular_learning.infrastructure.llm import gestor_llm
from modular_learning.infrastructure.persistence import json_repositorios as gestor_archivos

NIVELES_PROFUNDIDAD = {
    "BASICO": "BÁSICO",
    "BÁSICO": "BÁSICO",
    "INTERMEDIO": "INTERMEDIO",
    "AVANZADO": "AVANZADO",
}


@dataclass
class SesionTutoria:
    """Estado de una sesión de tutoría en curso."""

    sesion_id: str
    materia: str
    tema: str
    nivel_profundidad: str
    pasos: list[dict[str, str]]
    materiales_asociados: list[str] = field(default_factory=list)
    subtemas_adicionales: list[str] = field(default_factory=list)
    historial: list[dict[str, Any]] = field(default_factory=list)
    pasos_completados: set[int] = field(default_factory=set)


def normalizar_nivel(nivel: str | None) -> str:
    """Normaliza el nivel de profundidad; por defecto INTERMEDIO."""
    return NIVELES_PROFUNDIDAD.get((nivel or "").strip().upper(), "INTERMEDIO")


def normalizar_roadmap(data_roadmap: Any) -> list[dict[str, str]]:
    """Extrae una lista limpia de pasos {titulo, descripcion} desde la respuesta del LLM."""
    pasos_raw: Any = []
    if isinstance(data_roadmap, dict):
        data_dict = {str(k).strip(): v for k, v in data_roadmap.items()}
        pasos_raw = data_dict.get("pasos", [])
        if not pasos_raw:
            for k, v in data_dict.items():
                if "paso" in k.lower():
                    pasos_raw = v
                    break
    elif isinstance(data_roadmap, list):
        pasos_raw = data_roadmap

    pasos: list[dict[str, str]] = []
    if isinstance(pasos_raw, list):
        for p in pasos_raw:
            if isinstance(p, dict):
                limpio = {str(k).strip().lower(): v for k, v in p.items()}
                titulo = (
                    limpio.get("titulo")
                    or limpio.get("title")
                    or limpio.get("nombre")
                    or limpio.get("paso")
                    or "Paso"
                )
                descripcion = (
                    limpio.get("descripcion")
                    or limpio.get("description")
                    or limpio.get("detalle")
                    or limpio.get("contenido")
                    or ""
                )
                pasos.append({"titulo": str(titulo), "descripcion": str(descripcion)})
            elif isinstance(p, str):
                pasos.append({"titulo": p, "descripcion": ""})

    if not pasos:
        raise ValueError("El JSON del roadmap no contiene una lista de 'pasos' válida.")
    return pasos


def iniciar_sesion(
    sesion_id: str, materia: str, tema: str, nivel_profundidad: str | None
) -> SesionTutoria:
    """Genera el roadmap con el LLM y construye la sesión (equivale a las etapas 1-2 de `ml init`)."""
    nivel = normalizar_nivel(nivel_profundidad)
    detalle = gestor_archivos.obtener_detalle_clase(materia, tema)

    prompt_roadmap = gestor_archivos.leer_prompt("01_roadmap_aprendizaje.md").format(
        tema=tema,
        objetivo=f"Estudiar y dominar a fondo el tema dentro de la asignatura {materia}",
    )
    llm = gestor_llm.obtener_llm()
    data_roadmap = llm.generar_json_estructurado(prompt_roadmap)
    pasos = normalizar_roadmap(data_roadmap)

    return SesionTutoria(
        sesion_id=sesion_id,
        materia=materia,
        tema=tema,
        nivel_profundidad=nivel,
        pasos=pasos,
        materiales_asociados=list(detalle.get("materiales_asociados", [])),
        subtemas_adicionales=list(detalle.get("subtemas_adicionales", [])),
        historial=[
            {"role": "user", "parts": [prompt_roadmap]},
            {"role": "model", "parts": [json.dumps(data_roadmap, ensure_ascii=False)]},
        ],
    )


def construir_prompt_explicacion(sesion: SesionTutoria, indice_paso: int) -> str:
    """Arma el prompt de explicación del paso, con Segundo Cerebro y plugin práctico."""
    paso = sesion.pasos[indice_paso]
    titulo = paso.get("titulo", f"Paso {indice_paso + 1}")
    descripcion = paso.get("descripcion", "")

    prompt = gestor_archivos.leer_prompt("02_explicacion_tema.md").format(
        tema=f"{titulo}: {descripcion}",
        nivel_profundidad=sesion.nivel_profundidad,
        contexto_roadmap=(
            f"Asignatura: {sesion.materia}. Tema principal: {sesion.tema}. Paso actual: {titulo}"
        ),
    )

    if sesion.materiales_asociados or sesion.subtemas_adicionales:
        materiales = ", ".join(sesion.materiales_asociados) or "Ninguno específico"
        subtemas = ", ".join(sesion.subtemas_adicionales) or "Ninguno específico"
        prompt += f"""

CONTEXTO DEL SEGUNDO CEREBRO (Material local del estudiante):
- Archivos de referencia: {materiales}
- Subtemas clave a integrar: {subtemas}

DIRECTIVA OBLIGATORIA: En tu respuesta, DEBES hacer referencia explícitamente a que estás utilizando estos subtemas extraídos de sus propios apuntes. Hazlo de forma natural pero evidente (ej. "Basándome en tu archivo X, profundicemos en Y..."). Integra estos subtemas en tu explicación del tema principal.
"""

    plugin = gestor_plugins.obtener_plugin(sesion.materia)
    if plugin:
        prompt += (
            f"\n\n{plugin.obtener_instrucciones_ia()}\n\n{plugin.generar_ejercicio_base(titulo)}"
        )
    return prompt


def explicar_paso_stream(sesion: SesionTutoria, indice_paso: int) -> Iterator[str]:
    """Genera la explicación del paso en streaming y actualiza el historial al terminar."""
    if not 0 <= indice_paso < len(sesion.pasos):
        raise IndexError(f"El paso {indice_paso} no existe en la sesión.")

    prompt = construir_prompt_explicacion(sesion, indice_paso)
    llm = gestor_llm.obtener_llm()
    chunks: list[str] = []
    for chunk in llm.generar_respuesta_stream(prompt, contexto_previo=sesion.historial):
        chunks.append(chunk)
        yield chunk

    sesion.historial.append({"role": "user", "parts": [prompt]})
    sesion.historial.append({"role": "model", "parts": ["".join(chunks)]})
    sesion.pasos_completados.add(indice_paso)


def responder_duda(sesion: SesionTutoria, indice_paso: int, duda: str) -> str:
    """Resuelve una duda del estudiante sobre un paso, manteniendo el contexto."""
    if not 0 <= indice_paso < len(sesion.pasos):
        raise IndexError(f"El paso {indice_paso} no existe en la sesión.")
    titulo = sesion.pasos[indice_paso].get("titulo", f"Paso {indice_paso + 1}")
    prompt = (
        f"Tengo esta duda sobre el paso '{titulo}': {duda}. "
        "Respóndela técnicamente y de forma clara."
    )
    llm = gestor_llm.obtener_llm()
    respuesta = llm.generar_texto(prompt, contexto_previo=sesion.historial)
    sesion.historial.append({"role": "user", "parts": [prompt]})
    sesion.historial.append({"role": "model", "parts": [respuesta]})
    return respuesta


def finalizar_sesion(sesion: SesionTutoria) -> dict[str, Any]:
    """Genera la guía de estudio, la guarda en Obsidian y marca la clase como completada."""
    ruta_boveda = servicio_config.ruta_boveda()
    nombres_pasos = [p.get("titulo", "") for p in sesion.pasos]
    prompt_resumen = gestor_archivos.leer_prompt("03_resumen_evaluacion.md").format(
        materia=sesion.materia,
        contenido_apuntes=(
            f"Tema de estudio: {sesion.tema}\nPasos cubiertos:\n{', '.join(nombres_pasos)}"
        ),
    )
    llm = gestor_llm.obtener_llm()
    guia = llm.generar_texto(prompt_resumen, contexto_previo=sesion.historial)

    guardado = gestor_archivos.guardar_resumen_obsidian(
        sesion.materia, sesion.tema, guia, ruta_boveda
    )
    completada = gestor_archivos.marcar_clase_completada(sesion.materia, sesion.tema) if guardado else False
    return {"guia": guia, "guardado_obsidian": guardado, "clase_completada": completada}
