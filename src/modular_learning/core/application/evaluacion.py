import json
import os
import random
import re

from modular_learning import settings
from modular_learning.infrastructure.llm import gestor_llm

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
        # Respuesta dada solo como letra (ej. "B") o texto no coincidente: intenta resolver por letra.
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


def generar_quiz() -> list[dict]:
    """
    Lee los archivos JSON en data/schedules/, filtra los temas marcados con estado "completado"
    y solicita al gestor_llm generar 3 preguntas de opción múltiple basadas en esos temas.
    Maneja excepciones si la carpeta o los archivos están vacíos o no hay temas completados.
    """
    carpeta_schedules = str(settings.ruta_cronogramas())
    if not os.path.exists(carpeta_schedules):
        raise FileNotFoundError(
            "La carpeta data/schedules/ no existe. Ingesta un sílabo primero utilizando 'ml es'."
        )

    archivos = [f for f in os.listdir(carpeta_schedules) if f.endswith("_cronograma.json")]
    if not archivos:
        raise FileNotFoundError(
            "No se encontraron cronogramas en data/schedules/. Ejecuta 'ml es' para extraer sílabos."
        )

    temas_completados = []
    for arch in archivos:
        ruta = os.path.join(carpeta_schedules, arch)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                clases = data.get("clases", []) if isinstance(data, dict) else data
                for clase in clases:
                    if clase.get("estado") == "completado":
                        tema = clase.get("tema")
                        if tema and tema not in temas_completados:
                            temas_completados.append(tema)
        except Exception:
            continue

    if not temas_completados:
        raise ValueError(
            "No hay temas marcados con estado 'completado' en los cronogramas. "
            "Completa sesiones de estudio con 'ml init' para desbloquear el quiz de repaso activo."
        )

    llm = gestor_llm.obtener_llm()
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

    respuesta_json = llm.generar_json_estructurado(prompt)
    if isinstance(respuesta_json, list):
        preguntas_brutas = respuesta_json
    else:
        preguntas_brutas = respuesta_json.get("preguntas", [])

    preguntas = []
    for p in preguntas_brutas:
        try:
            preguntas.append(mezclar_opciones(p))
        except (ValueError, AttributeError, TypeError):
            continue
    if not preguntas:
        raise RuntimeError("El LLM no generó preguntas válidas para el quiz.")
    return preguntas
