"""Servicio de aplicación para el motor de recuerdo activo y evaluación adaptativa."""

from __future__ import annotations

import json
import random
import re
from typing import Any

from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.domain.materias import resolver_materia
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import CronogramaRepo, MateriaRepo

LETRAS = "ABCD"
_PREFIJO_OPCION = re.compile(r"^\s*[A-Da-d][\)\.\-:]\s*")


def _limpiar_opcion(texto: str) -> str:
    """Quita el prefijo de letra ('A) ', 'b.', etc.) de una opción."""
    return _PREFIJO_OPCION.sub("", str(texto)).strip()


def mezclar_opciones(pregunta: dict, rng: random.Random | None = None) -> dict:
    """
    Elimina sesgos del LLM: quita las letras, baraja las opciones, y vuelve a etiquetarlas A-D
    de modo que la respuesta correcta quede en una posición aleatoria.
    """
    rng = rng or random.Random()
    opciones = [_limpiar_opcion(o) for o in pregunta.get("opciones", [])]
    correcta_bruta = str(pregunta.get("respuesta_correcta", ""))
    correcta = _limpiar_opcion(correcta_bruta)

    if correcta not in opciones:
        m = re.match(r"^\s*([A-Da-d])\b", correcta_bruta)
        if m and "ABCD".index(m.group(1).upper()) < len(pregunta.get("opciones", [])):
            correcta = opciones[LETRAS.index(m.group(1).upper())]
        else:
            raise ValueError("La respuesta correcta no coincide con ninguna opción.")

    rng.shuffle(opciones)
    etiquetadas = [f"{LETRAS[i]}) {o}" for i, o in enumerate(opciones)]
    return {
        "enunciado": pregunta.get("enunciado", ""),
        "opciones": etiquetadas,
        "respuesta_correcta": etiquetadas[opciones.index(correcta)],
    }


class EvaluacionService:
    """Caso de uso para la generación y calificación de quizzes académicos."""

    def __init__(
        self,
        llm: LLMPort,
        cronograma_repo: CronogramaRepo,
        materia_repo: MateriaRepo | None = None,
        repaso: RepasoService | None = None,
    ):
        self.llm = llm
        self.cronograma_repo = cronograma_repo
        self.materia_repo = materia_repo
        self.repaso = repaso

    def _nombre_materia(self, nombre_cronograma: str) -> str:
        """Usa el nombre del catálogo (con su escritura real) si la asignatura está registrada."""
        if self.materia_repo:
            m_obj = resolver_materia(self.materia_repo.listar(), nombre_cronograma)
            if m_obj:
                return m_obj.nombre
        return nombre_cronograma

    def obtener_temas_completados(self) -> list[dict[str, str]]:
        """Obtiene las clases completadas como [{materia, tema}] a través de los cronogramas."""
        cronogramas = self.cronograma_repo.listar_cronogramas()
        if not cronogramas:
            raise FileNotFoundError(
                "No se encontraron cronogramas en data/schedules/. Ejecuta 'ml es' para extraer sílabos."
            )

        temas_completados: list[dict[str, str]] = []
        for materia, clases in cronogramas.items():
            nombre = self._nombre_materia(materia)
            for clase in clases:
                if str(clase.get("estado", "")).lower() == "completado":
                    tema = clase.get("tema")
                    item = {"materia": nombre, "tema": str(tema)}
                    if tema and item not in temas_completados:
                        temas_completados.append(item)
        return temas_completados

    def generar_quiz(self) -> list[dict[str, Any]]:
        """Genera un quiz de 3 preguntas de opción múltiple usando temas completados."""
        temas_completados = self.obtener_temas_completados()
        if not temas_completados:
            raise ValueError(
                "No hay temas marcados con estado 'completado' en los cronogramas. "
                "Completa sesiones de estudio con 'ml init' para desbloquear el quiz de repaso activo."
            )

        prompt = f"""
Actúa como un profesor experto y evaluador académico riguroso. Basándote exclusivamente en las siguientes clases que el estudiante ya ha completado (materia y tema):
{json.dumps(temas_completados, ensure_ascii=False)}

Genera exactamente 3 preguntas de opción múltiple de nivel técnico avanzado basadas en dichas clases.

REGLAS ANTI-PATRÓN (obligatorias, el quiz no debe ser adivinable por su forma):
- Las 4 opciones de cada pregunta deben tener una LONGITUD y nivel de detalle similares (diferencia máxima de ~20% en caracteres). La opción correcta NO debe ser la más larga ni la más detallada.
- Los distractores deben ser plausibles, técnicamente creíbles y basarse en errores conceptuales comunes; nada de opciones absurdas ni evidentemente falsas.
- Evita palabras absolutas como "siempre" o "nunca" solo en los distractores, y evita frases como "todas las anteriores" o "ninguna de las anteriores".
- Varía la posición de la respuesta correcta entre las preguntas.

REGLAS DE TRAZABILIDAD:
- En "materia" y "tema" copia EXACTAMENTE la materia y el tema de la clase de la lista en la que se basa la pregunta.
- En "explicacion" justifica en una o dos oraciones por qué la respuesta correcta lo es.
- Si la pregunta incluye fórmulas, escríbelas en LaTeX entre signos de dólar.

Devuelve la respuesta en formato JSON estricto con la siguiente estructura exacta:
{{
  "preguntas": [
    {{
      "materia": "Materia de la clase",
      "tema": "Tema de la clase",
      "enunciado": "Texto de la pregunta...",
      "opciones": ["A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4"],
      "respuesta_correcta": "A) Opción 1",
      "explicacion": "Por qué es la correcta."
    }}
  ]
}}
Devuelve ÚNICAMENTE el JSON válido, sin bloques markdown de código adicionales ni texto introductorio.
"""
        respuesta_json = self.llm.generar_json_estructurado(prompt)
        if isinstance(respuesta_json, list):
            preguntas_brutas = respuesta_json
        else:
            preguntas_brutas = respuesta_json.get("preguntas", [])

        preguntas: list[dict[str, Any]] = []
        for p in preguntas_brutas:
            try:
                mezclada = mezclar_opciones(p)
            except (ValueError, AttributeError, TypeError):
                continue
            preguntas.append(
                {
                    **mezclada,
                    "materia": self._nombre_materia(str(p.get("materia") or "")),
                    "tema": str(p.get("tema") or ""),
                    "explicacion": str(p.get("explicacion") or ""),
                }
            )

        if not preguntas:
            raise RuntimeError("El LLM no generó preguntas válidas para el quiz.")
        return preguntas

    def evaluar_respuestas(
        self, preguntas: list[dict[str, Any]], respuestas: list[str]
    ) -> dict[str, Any]:
        """Evalúa las respuestas y, si hay repaso espaciado, reprograma cada pregunta."""
        detalle = []
        aciertos = 0
        for idx, p in enumerate(preguntas):
            elegida = respuestas[idx] if idx < len(respuestas) else ""
            correcta = p.get("respuesta_correcta", "")
            ok = elegida.strip().lower() == str(correcta).strip().lower()
            aciertos += int(ok)
            detalle.append(
                {
                    "correcto": ok,
                    "respuesta_correcta": correcta,
                    "elegida": elegida,
                    "materia": p.get("materia", ""),
                    "tema": p.get("tema", ""),
                    "explicacion": p.get("explicacion", ""),
                }
            )

        if self.repaso:
            self.repaso.registrar_resultados(preguntas, detalle)

        total = len(preguntas)
        return {
            "aciertos": aciertos,
            "total": total,
            "porcentaje": round(aciertos / total * 100) if total else 0,
            "detalle": detalle,
        }


__all__ = [
    "EvaluacionService",
    "mezclar_opciones",
]
