"""Servicio de aplicación para el motor de recuerdo activo y evaluación adaptativa."""

from __future__ import annotations

import json
import os
import random
import re
from typing import Any

from modular_learning import settings
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import CronogramaRepo

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
        cronograma_repo: CronogramaRepo | None = None,
        carpeta_schedules: str | None = None,
    ):
        self.llm = llm
        self.cronograma_repo = cronograma_repo
        self._carpeta_schedules = carpeta_schedules

    @property
    def carpeta_schedules(self) -> str:
        return self._carpeta_schedules or str(settings.ruta_cronogramas())

    def obtener_temas_completados(self) -> list[str]:
        """Obtiene la lista de temas completados a través de los cronogramas."""
        if not os.path.exists(self.carpeta_schedules):
            raise FileNotFoundError(
                "La carpeta data/schedules/ no existe. Ingesta un sílabo primero utilizando 'ml es'."
            )

        archivos = [f for f in os.listdir(self.carpeta_schedules) if f.endswith("_cronograma.json")]
        if not archivos:
            raise FileNotFoundError(
                "No se encontraron cronogramas en data/schedules/. Ejecuta 'ml es' para extraer sílabos."
            )

        temas_completados: list[str] = []
        for arch in archivos:
            ruta = os.path.join(self.carpeta_schedules, arch)
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    clases = data.get("clases", []) if isinstance(data, dict) else data
                    if not isinstance(clases, list):
                        continue
                    for clase in clases:
                        if clase.get("estado", "").lower() == "completado":
                            tema = clase.get("tema")
                            if tema and tema not in temas_completados:
                                temas_completados.append(tema)
            except Exception:
                continue

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
Actúa como un profesor experto y evaluador académico riguroso. Basándote exclusivamente en los siguientes temas que el estudiante ya ha completado:
{json.dumps(temas_completados, ensure_ascii=False)}

Genera exactamente 3 preguntas de opción múltiple de nivel técnico avanzado basadas en dichos temas.

REGLAS ANTI-PATRÓN (obligatorias, el quiz no debe ser adivinable por su forma):
- Las 4 opciones de cada pregunta deben tener una LONGITUD y nivel de detalle similares (diferencia máxima de ~20% en caracteres). La opción correcta NO debe ser la más larga ni la más detallada.
- Los distractores deben ser plausibles, técnicamente creíbles y basarse en errores conceptuales comunes; nada de opciones absurdas ni evidentemente falsas.
- Evita palabras absolutas como "siempre" o "nunca" solo en los distractores, y evita frases como "todas las anteriores" o "ninguna de las anteriores".
- Varía la posición de la respuesta correcta entre las preguntas.

Devuelve la respuesta en formato JSON estricto con la siguiente estructura exacta:
{{
  "preguntas": [
    {{
      "enunciado": "Texto de la pregunta...",
      "opciones": ["A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4"],
      "respuesta_correcta": "A) Opción 1"
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
                preguntas.append(mezclar_opciones(p))
            except (ValueError, AttributeError, TypeError):
                continue

        if not preguntas:
            raise RuntimeError("El LLM no generó preguntas válidas para el quiz.")
        return preguntas

    def evaluar_respuestas(
        self, preguntas: list[dict[str, Any]], respuestas: list[str]
    ) -> dict[str, Any]:
        """Evalúa las respuestas de un quiz comparándolas con las respuestas correctas."""
        detalle = []
        aciertos = 0
        for idx, p in enumerate(preguntas):
            elegida = respuestas[idx] if idx < len(respuestas) else ""
            correcta = p.get("respuesta_correcta", "")
            ok = elegida.strip().lower() == str(correcta).strip().lower()
            aciertos += int(ok)
            detalle.append({"correcto": ok, "respuesta_correcta": correcta, "elegida": elegida})

        total = len(preguntas)
        return {
            "aciertos": aciertos,
            "total": total,
            "porcentaje": round(aciertos / total * 100) if total else 0,
            "detalle": detalle,
        }


_instancia_por_defecto: EvaluacionService | None = None


def configurar_servicio_defecto(servicio: EvaluacionService) -> None:
    global _instancia_por_defecto
    _instancia_por_defecto = servicio


def generar_quiz() -> list[dict[str, Any]]:
    if _instancia_por_defecto is None:
        raise RuntimeError("EvaluacionService no ha sido inicializado en el contenedor.")
    return _instancia_por_defecto.generar_quiz()


_orig_generar_quiz = generar_quiz

__all__ = [
    "EvaluacionService",
    "_orig_generar_quiz",
    "configurar_servicio_defecto",
    "generar_quiz",
    "mezclar_opciones",
]
