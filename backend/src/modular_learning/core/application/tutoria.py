"""Servicio de aplicación de Tutoría interactiva personalizada."""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from modular_learning.core.application.plugins import PluginsService
from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.ports.boveda import BovedaNotasPort
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import CronogramaRepo

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
    # Pregunta de repaso fallada que motivó la sesión (modo refuerzo)
    enfoque: str | None = None
    # Preguntas de este tema que el estudiante falló en repasos anteriores
    fallos_previos: list[str] = field(default_factory=list)


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


class TutoriaService:
    """Caso de uso de tutoría interactiva (roadmap, explicación, dudas y finalización)."""

    def __init__(
        self,
        llm: LLMPort,
        cronograma_repo: CronogramaRepo,
        boveda_port: BovedaNotasPort,
        lector_docs: LectorDocumentosPort,
        ajustes_port: AjustesPort,
        plugins_service: PluginsService | None = None,
        repaso: RepasoService | None = None,
    ):
        self.llm = llm
        self.cronograma_repo = cronograma_repo
        self.boveda_port = boveda_port
        self.lector_docs = lector_docs
        self.ajustes_port = ajustes_port
        self.plugins_service = plugins_service
        self.repaso = repaso

    def iniciar_sesion(
        self,
        sesion_id: str,
        materia: str,
        tema: str,
        nivel_profundidad: str | None,
        enfoque: str | None = None,
    ) -> SesionTutoria:
        """Genera el roadmap con el LLM y construye la sesión inicial.

        Con `enfoque` (una pregunta de repaso fallada) la ruta se orienta a corregir ese error.
        """
        nivel = normalizar_nivel(nivel_profundidad)
        detalle = self.cronograma_repo.obtener_detalle_clase(materia, tema)
        fallos = self.repaso.fallos_previos(materia, tema) if self.repaso else []
        enfoque = (enfoque or "").strip() or None

        objetivo = f"Estudiar y dominar a fondo el tema dentro de la asignatura {materia}"
        if enfoque:
            objetivo = (
                f"Reforzar el tema dentro de la asignatura {materia}. En un repaso fallé esta "
                f"pregunta: «{enfoque}». Construye la ruta para entender exactamente el concepto "
                "que me hizo fallar, empezando por la causa más probable del error."
            )
        if fallos:
            objetivo += ". Otras preguntas de este tema que fallé antes: " + " | ".join(fallos)

        prompt_plantilla = self.lector_docs.leer_prompt("01_roadmap_aprendizaje.md")
        prompt_roadmap = prompt_plantilla.format(tema=tema, objetivo=objetivo)
        data_roadmap = self.llm.generar_json_estructurado(prompt_roadmap)
        pasos = normalizar_roadmap(data_roadmap)

        return SesionTutoria(
            sesion_id=sesion_id,
            materia=materia,
            tema=tema,
            nivel_profundidad=nivel,
            pasos=pasos,
            materiales_asociados=list(detalle.get("materiales_asociados", [])),
            subtemas_adicionales=list(detalle.get("subtemas_adicionales", [])),
            enfoque=enfoque,
            fallos_previos=fallos,
            historial=[
                {"role": "user", "parts": [prompt_roadmap]},
                {"role": "model", "parts": [json.dumps(data_roadmap, ensure_ascii=False)]},
            ],
        )

    def construir_prompt_explicacion(self, sesion: SesionTutoria, indice_paso: int) -> str:
        """Arma el prompt de explicación del paso con contexto de Segundo Cerebro y plugins."""
        paso = sesion.pasos[indice_paso]
        titulo = paso.get("titulo", f"Paso {indice_paso + 1}")
        descripcion = paso.get("descripcion", "")

        plantilla = self.lector_docs.leer_prompt("02_explicacion_tema.md")
        prompt = plantilla.format(
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

        if sesion.enfoque or sesion.fallos_previos:
            fallidas = [sesion.enfoque] if sesion.enfoque else []
            fallidas += [f for f in sesion.fallos_previos if f != sesion.enfoque]
            listado = "\n".join(f"- {f}" for f in fallidas)
            prompt += f"""

PREGUNTAS DE REPASO QUE EL ESTUDIANTE FALLÓ SOBRE ESTE TEMA:
{listado}

DIRECTIVA: Cuando el paso actual tenga relación con estas preguntas, aclara explícitamente el error
conceptual que lleva a fallarlas, sin limitarte a dar la respuesta.
"""

        if self.plugins_service:
            plugin = self.plugins_service.obtener_plugin(sesion.materia)
            if plugin:
                prompt += f"\n\n{plugin.obtener_instrucciones_ia()}\n\n{plugin.generar_ejercicio_base(titulo)}"

        return prompt

    def explicar_paso(self, sesion: SesionTutoria, indice_paso: int) -> str:
        """Genera la explicación completa de un paso y actualiza el historial."""
        if not 0 <= indice_paso < len(sesion.pasos):
            raise IndexError(f"El paso {indice_paso} no existe en la sesión.")
        prompt = self.construir_prompt_explicacion(sesion, indice_paso)
        respuesta = self.llm.generar_texto(prompt, contexto_previo=sesion.historial)
        sesion.historial.append({"role": "user", "parts": [prompt]})
        sesion.historial.append({"role": "model", "parts": [respuesta]})
        sesion.pasos_completados.add(indice_paso)
        return respuesta

    def explicar_paso_stream(self, sesion: SesionTutoria, indice_paso: int) -> Iterator[str]:
        """Genera la explicación del paso en streaming y actualiza el historial al terminar."""
        if not 0 <= indice_paso < len(sesion.pasos):
            raise IndexError(f"El paso {indice_paso} no existe en la sesión.")

        prompt = self.construir_prompt_explicacion(sesion, indice_paso)
        chunks: list[str] = []
        for chunk in self.llm.generar_respuesta_stream(prompt, contexto_previo=sesion.historial):
            chunks.append(chunk)
            yield chunk

        sesion.historial.append({"role": "user", "parts": [prompt]})
        sesion.historial.append({"role": "model", "parts": ["".join(chunks)]})
        sesion.pasos_completados.add(indice_paso)

    def responder_duda(self, sesion: SesionTutoria, indice_paso: int, duda: str) -> str:
        """Resuelve una duda del estudiante sobre un paso manteniendo el contexto de la sesión."""
        if not 0 <= indice_paso < len(sesion.pasos):
            raise IndexError(f"El paso {indice_paso} no existe en la sesión.")
        titulo = sesion.pasos[indice_paso].get("titulo", f"Paso {indice_paso + 1}")
        prompt = (
            f"Tengo esta duda sobre el paso '{titulo}': {duda}. "
            "Respóndela técnicamente y de forma clara. Si usas fórmulas, escríbelas en LaTeX "
            "entre signos de dólar."
        )
        respuesta = self.llm.generar_texto(prompt, contexto_previo=sesion.historial)
        sesion.historial.append({"role": "user", "parts": [prompt]})
        sesion.historial.append({"role": "model", "parts": [respuesta]})
        return respuesta

    def finalizar_sesion(self, sesion: SesionTutoria) -> dict[str, Any]:
        """Genera la guía de estudio final, la guarda en Obsidian y marca la clase como completada."""
        ruta_boveda = self.ajustes_port.ruta_boveda()
        nombres_pasos = [p.get("titulo", "") for p in sesion.pasos]

        plantilla_resumen = self.lector_docs.leer_prompt("03_resumen_evaluacion.md")
        prompt_resumen = plantilla_resumen.format(
            materia=sesion.materia,
            contenido_apuntes=(
                f"Tema de estudio: {sesion.tema}\nPasos cubiertos:\n{', '.join(nombres_pasos)}"
            ),
        )
        guia = self.llm.generar_texto(prompt_resumen, contexto_previo=sesion.historial)

        guardado = self.boveda_port.guardar_resumen(sesion.materia, sesion.tema, guia, ruta_boveda)
        completada = (
            self.cronograma_repo.marcar_clase_completada(sesion.materia, sesion.tema)
            if guardado
            else False
        )
        if self.repaso:
            self.repaso.registrar_tutoria(
                sesion.materia, sesion.tema, sesion.nivel_profundidad, sesion.enfoque
            )
        return {"guia": guia, "guardado_obsidian": guardado, "clase_completada": completada}


__all__ = [
    "NIVELES_PROFUNDIDAD",
    "SesionTutoria",
    "TutoriaService",
    "normalizar_nivel",
    "normalizar_roadmap",
]
