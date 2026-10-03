import os
import json
from typing import Dict, Any, List
from modules.core.services import gestor_llm


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


def asignar_material_a_clase(materia: str, contenido_md: str, nombre_archivo: str = "material_nuevo.md") -> dict:
    """
    Evalúa la afinidad del contenido de un material recién ingestado contra cada clase del cronograma oficial
    usando IA, limpia estrictamente la respuesta JSON, y asigna los subtemas y materiales asociados.
    """
    ruta_cronograma = _encontrar_ruta_cronograma(materia)
    if not ruta_cronograma or not os.path.exists(ruta_cronograma):
        print(f"⚠️ [Alineador] No se encontró cronograma para la materia '{materia}'.")
        return {"clase_asignada": 0, "peso_afinidad": 0, "justificacion": "Cronograma no encontrado", "subtemas_a_incorporar": []}

    try:
        with open(ruta_cronograma, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ [Alineador] Error al leer el cronograma: {e}")
        return {"clase_asignada": 0, "peso_afinidad": 0, "justificacion": f"Error de lectura: {e}", "subtemas_a_incorporar": []}

    if isinstance(data, list):
        cronograma_dict = {
            "clases": data,
            "material_transversal": []
        }
    elif isinstance(data, dict):
        cronograma_dict = data
        if "clases" not in cronograma_dict:
            cronograma_dict["clases"] = []
        if "material_transversal" not in cronograma_dict:
            cronograma_dict["material_transversal"] = []
    else:
        cronograma_dict = {"clases": [], "material_transversal": []}

    clases = cronograma_dict["clases"]
    if not clases:
        return {"clase_asignada": 0, "peso_afinidad": 0, "justificacion": "Cronograma vacío", "subtemas_a_incorporar": []}

    resumen_clases = []
    for idx, c in enumerate(clases, 1):
        fecha = c.get("fecha", "S/F")
        tema = c.get("tema", "Sin tema")
        contenido = c.get("contenido", "")
        resumen_clases.append(f"Clase {idx} (Fecha: {fecha}): {tema} - Contenido: {contenido}")

    resumen_clases_str = "\n".join(resumen_clases)
    extracto_material = contenido_md[:4000]

    prompt = (
        "Eres un Arquitecto de Software y Evaluador Curricular experto. "
        "A continuación tienes la lista completa de clases oficiales del cronograma de la materia y un extracto de los apuntes de un material recién ingestado.\n\n"
        f"CRONOGRAMA OFICIAL:\n{resumen_clases_str}\n\n"
        f"EXTRACTO DEL NUEVO MATERIAL ({nombre_archivo}):\n{extracto_material}\n\n"
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

    texto_respuesta = ""
    try:
        llm = gestor_llm.obtener_llm()
        texto_respuesta = llm.generar_texto(prompt)
    except Exception as e:
        try:
            res_obj = llm.generar_json_estructurado(prompt)
            texto_respuesta = json.dumps(res_obj)
        except Exception as err:
            print(f"⚠️ [Alineador] Error al consultar la IA: {err}")
            return {"clase_asignada": 1, "peso_afinidad": 50, "justificacion": "Error de comunicación con IA", "subtemas_a_incorporar": []}

    # TAREA 1: Limpieza estricta de delimitadores Markdown antes de json.loads()
    texto_limpio = texto_respuesta.strip()
    if "```json" in texto_limpio:
        texto_limpio = texto_limpio.split("```json")[1]
        if "```" in texto_limpio:
            texto_limpio = texto_limpio.split("```")[0]
    elif "```" in texto_limpio:
        texto_limpio = texto_limpio.split("```")[1]
        if "```" in texto_limpio:
            texto_limpio = texto_limpio.split("```")[0]

    texto_limpio = texto_limpio.strip()

    try:
        resultado_json = json.loads(texto_limpio)
        if not isinstance(resultado_json, dict):
            raise ValueError("El JSON parseado no es un diccionario.")
    except (json.JSONDecodeError, KeyError, ValueError, Exception) as parse_err:
        print(f"\033[1;91m❌ [ERROR] Fallo crítico al parsear respuesta JSON de la IA:\033[0m {parse_err}")
        print(f"\033[1;93m--- RESPUESTA CRUDA RECIBIDA DE LA IA ---\033[0m\n{texto_respuesta}\n\033[1;93m-----------------------------------------\033[0m")
        return {
            "clase_asignada": 1,
            "peso_afinidad": 50,
            "justificacion": f"Error de parseo JSON: {parse_err}",
            "subtemas_a_incorporar": []
        }

    # TAREA 2: Logs de depuración visibles
    peso = int(resultado_json.get("peso_afinidad", 0))
    clase_num = int(resultado_json.get("clase_asignada", 1))
    print(f"[DEBUG] IA evaluó Clase {clase_num} con Afinidad: {peso}%")

    if peso < 60:
        print("[DEBUG] Afinidad muy baja. Se enviará a material transversal.")

    subtemas = resultado_json.get("subtemas_a_incorporar", [])
    if not isinstance(subtemas, list):
        subtemas = []

    if peso >= 60:
        indice_clase = clase_num - 1
        if 0 <= indice_clase < len(clases):
            clase_target = clases[indice_clase]
        else:
            clase_target = clases[0]

        if "materiales_asociados" not in clase_target:
            clase_target["materiales_asociados"] = []
        if nombre_archivo not in clase_target["materiales_asociados"]:
            clase_target["materiales_asociados"].append(nombre_archivo)

        if "subtemas_adicionales" not in clase_target:
            clase_target["subtemas_adicionales"] = []
        for sub in subtemas:
            sub_str = str(sub).strip()
            if sub_str and sub_str not in clase_target["subtemas_adicionales"]:
                clase_target["subtemas_adicionales"].append(sub_str)
    else:
        transversal_item = {
            "archivo": nombre_archivo,
            "justificacion": resultado_json.get("justificacion", ""),
            "subtemas": subtemas,
            "peso_afinidad": peso
        }
        cronograma_dict["material_transversal"].append(transversal_item)

    # TAREA 3: Verificación de escritura en disco
    try:
        with open(ruta_cronograma, 'w', encoding='utf-8') as f:
            json.dump(cronograma_dict, f, indent=4, ensure_ascii=False)
        print("[✓] JSON del cronograma actualizado y guardado en disco correctamente.")
    except Exception as e:
        print(f"⚠️ [Alineador] Error al guardar el cronograma actualizado: {e}")

    return resultado_json
