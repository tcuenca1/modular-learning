import json
import os

from modules.core.services import gestor_llm


def generar_quiz() -> list[dict]:
    """
    Lee los archivos JSON en data/schedules/, filtra los temas marcados con estado "completado"
    y solicita al gestor_llm generar 3 preguntas de opción múltiple basadas en esos temas.
    Maneja excepciones si la carpeta o los archivos están vacíos o no hay temas completados.
    """
    carpeta_schedules = os.path.join("data", "schedules")
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
                clases = data.get("clases", [])
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
    preguntas = respuesta_json.get("preguntas", [])
    if not preguntas:
        raise RuntimeError("El LLM no generó preguntas válidas para el quiz.")
    return preguntas
