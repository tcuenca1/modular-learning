import os
import json
from typing import List, Dict, Any
from halo import Halo
from modules.core import gestor_llm


def _encontrar_ruta_cronograma(materia: str) -> str:
    """Busca y retorna la ruta del archivo cronograma.json de la materia."""
    carpeta_data = os.path.join("data", "schedules")
    if not os.path.exists(carpeta_data):
        return ""

    materia_slug = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in materia).strip().replace(' ', '_').upper()
    materia_upper = materia.upper().replace(' ', '_')
    
    posibles_nombres = [
        f"{materia}_cronograma.json",
        f"{materia_slug}_cronograma.json",
        f"{materia_upper}_cronograma.json",
        f"{materia_slug.lower()}_cronograma.json"
    ]

    for nombre in posibles_nombres:
        ruta_prueba = os.path.join(carpeta_data, nombre)
        if os.path.exists(ruta_prueba):
            return ruta_prueba

    try:
        for arch in os.listdir(carpeta_data):
            if arch.endswith("_cronograma.json"):
                if materia_slug.replace("_", "") in arch.upper().replace("_", ""):
                    return os.path.join(carpeta_data, arch)
    except Exception:
        pass

    return ""


def extraer_y_fusionar_subtemas(materia: str, contenido_md: str) -> int:
    """
    Envía el cronograma oficial y los apuntes a la IA para extraer conceptos/subtemas técnicos
    no incluidos en el cronograma, y los fusiona en el archivo JSON de la materia.
    Retorna la cantidad de nuevos subtemas inyectados.
    """
    ruta_cronograma = _encontrar_ruta_cronograma(materia)
    if not ruta_cronograma or not os.path.exists(ruta_cronograma):
        print(f"⚠️ [Sincronizador] No se encontró cronograma para la materia '{materia}'.")
        return 0

    try:
        with open(ruta_cronograma, 'r', encoding='utf-8') as f:
            cronograma_data = json.load(f)
    except Exception as e:
        print(f"⚠️ [Sincronizador] Error al leer el cronograma: {e}")
        return 0

    if not isinstance(cronograma_data, list):
        return 0

    try:
        llm = gestor_llm.obtener_llm()
    except Exception as e:
        print(f"⚠️ [Sincronizador] Error al inicializar gestor_llm: {e}")
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
            texto_resp = llm.generar_texto(prompt)
            texto_limpio = texto_resp.strip()
            if texto_limpio.startswith("```json"):
                texto_limpio = texto_limpio[7:]
            if texto_limpio.startswith("```"):
                texto_limpio = texto_limpio[3:]
            if texto_limpio.endswith("```"):
                texto_limpio = texto_limpio[:-3]
            resultado_json = json.loads(texto_limpio.strip())
        except Exception as e:
            print(f"⚠️ [Sincronizador] No se pudo parsear la respuesta de la IA como JSON: {e}")
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
            clase_target = next((c for c in cronograma_data if c.get("estado", "").lower() == "pendiente"), cronograma_data[-1])
            if "subtemas_adicionales" not in clase_target:
                clase_target["subtemas_adicionales"] = []
            for sub in nuevos:
                sub_str = str(sub).strip()
                if sub_str and sub_str not in clase_target["subtemas_adicionales"]:
                    clase_target["subtemas_adicionales"].append(sub_str)
                    subtemas_nuevos_totales += 1

    if subtemas_nuevos_totales > 0:
        try:
            with open(ruta_cronograma, 'w', encoding='utf-8') as f:
                json.dump(cronograma_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ [Sincronizador] Error al guardar el cronograma actualizado: {e}")

    return subtemas_nuevos_totales
