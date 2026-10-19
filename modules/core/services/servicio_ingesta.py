"""
Servicio de aplicación para ingesta de material de estudio (`ml im`).

Procesa archivos (PDF/DOCX/TXT/MD) a través del puerto LLM, los anonimiza, los guarda
en la bóveda de Obsidian configurada, los registra y los alinea con el cronograma de la materia.
Además puede escanear la carpeta de cada asignatura (configurada por el usuario) y procesar
solo los archivos nuevos, igual que el gestor de plugins.
"""

import mimetypes
import os
import time
from collections.abc import Iterator

from modules.core.domain import alineador_curricular
from modules.core.services import gestor_archivos, gestor_llm, servicio_config
from modules.plugins.services import gestor_plugins

EXTENSIONES_MATERIAL = (".pdf", ".docx", ".txt", ".md")
EXTENSIONES_NO_SOPORTADAS_WEB = (".pptx",)
TIPOS_MATERIAL = ("actividad", "diapositiva", "lectura", "material_complementario")

REGLA_PRIVACIDAD = (
    "\n\n[REGLA ESTRICTA DE PRIVACIDAD Y ANONIMIZACIÓN]:\n"
    "Oculta o anonimiza cualquier nombre de estudiante, profesor, número de identificación institucional, "
    "correos electrónicos o datos personales que aparezcan en el documento. Reemplázalos por etiquetas "
    "genéricas como [ESTUDIANTE], [DOCENTE] o [ID_OMITIDO]."
)


def clasificar_tipo_material(ruta_archivo: str, ruta_raiz_lote: str) -> str:
    """
    Clasifica el material según su ubicación dentro de la carpeta de la asignatura:
    raíz -> actividad; 'MATERIAL DE ESTUDIO' -> diapositiva; 'MATERIAL ADICIONAL' -> lectura.
    """
    rel_path = os.path.relpath(ruta_archivo, ruta_raiz_lote)
    if len(rel_path.split(os.sep)) == 1:
        return "actividad"
    ruta_upper = rel_path.upper()
    if "MATERIAL DE ESTUDIO" in ruta_upper:
        return "diapositiva"
    if "MATERIAL ADICIONAL" in ruta_upper:
        return "lectura"
    return "material_complementario"


def _leer_docx(ruta: str) -> str:
    import docx

    documento = docx.Document(ruta)
    return "\n".join(p.text for p in documento.paragraphs)


def _generar_contenido(llm, ruta: str, prompt: str) -> str:
    ext = os.path.splitext(ruta)[1].lower()
    if ext == ".docx":
        texto = _leer_docx(ruta)
        return llm.generar_texto(f"{prompt}\n\nCONTENIDO DEL DOCUMENTO:\n{texto}")
    if ext in (".txt", ".md"):
        with open(ruta, encoding="utf-8", errors="replace") as f:
            return llm.generar_texto(f"{prompt}\n\nCONTENIDO DEL DOCUMENTO:\n{f.read()}")

    mime = "application/pdf" if ext == ".pdf" else (mimetypes.guess_type(ruta)[0] or "text/plain")
    with open(ruta, "rb") as f:
        datos = f.read()
    return llm.generar_texto_con_archivo({"mime_type": mime, "data": datos, "path": ruta}, prompt)


def ingestar_archivo(
    ruta_archivo: str, nombre_original: str, materia: str, tipo: str = "material_complementario"
) -> dict:
    """Ingesta un archivo y devuelve un resumen del resultado."""
    if tipo not in TIPOS_MATERIAL:
        tipo = "material_complementario"

    ruta_boveda = servicio_config.ruta_boveda()
    try:
        plantilla = gestor_archivos.leer_prompt("05_ingesta_material.md")
    except Exception:
        plantilla = "Actúa como un extractor de conocimiento experto y transcribe este documento en Markdown."

    prompt = (
        plantilla.replace("{materia}", materia)
        .replace("{tipo}", tipo)
        .replace("{fecha}", time.strftime("%Y-%m-%d"))
        .replace("{materia_slug}", materia.lower().replace(" ", "_"))
        + REGLA_PRIVACIDAD
    )

    llm = gestor_llm.obtener_llm()
    contenido_md = _generar_contenido(llm, ruta_archivo, prompt)

    carpeta_salida = os.path.join(ruta_boveda, materia, tipo.capitalize())
    os.makedirs(carpeta_salida, exist_ok=True)
    base = os.path.splitext(nombre_original)[0].replace(" ", "_")
    ruta_salida = os.path.join(carpeta_salida, f"{base}_Notas.md")
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido_md)

    gestor_archivos.registrar_material(nombre_original, materia)

    alineacion: dict = {}
    try:
        alineacion = alineador_curricular.asignar_material_a_clase(
            materia, contenido_md, nombre_original
        )
    except Exception as e:
        alineacion = {"error": str(e)}

    plugin_actualizado = False
    plugin = gestor_plugins.obtener_plugin(materia)
    if plugin:
        try:
            tecnico = llm.generar_texto(
                "Extrae únicamente un listado técnico de los comandos, nodos, topologías o "
                "configuraciones exactas que aparecen en este documento. Devuelve solo la lista, "
                f"sin introducciones.\n\nDOCUMENTO:\n{contenido_md[:8000]}"
            ).strip()
            if tecnico:
                plugin.guardar_contexto_extraido(tecnico)
                plugin_actualizado = True
        except Exception:
            pass

    return {
        "archivo": nombre_original,
        "materia": materia,
        "tipo": tipo,
        "ruta_salida": os.path.abspath(ruta_salida),
        "contenido_md": contenido_md,
        "alineacion": alineacion,
        "plugin_actualizado": plugin_actualizado,
    }


# --------------------- Escaneo de la carpeta de cada asignatura ---------------------
def escanear_materia(materia: str) -> dict:
    """Busca en la carpeta configurada de la asignatura los archivos nuevos (no ingestados)."""
    carpeta = os.path.join(servicio_config.carpeta_material(), materia)
    resultado = {
        "materia": materia,
        "carpeta": carpeta,
        "existe": os.path.isdir(carpeta),
        "total": 0,
        "omitidos": 0,
        "no_soportados": 0,
        "pendientes": [],
    }
    if not resultado["existe"]:
        return resultado

    for raiz, _, archivos in os.walk(carpeta):
        for nombre in sorted(archivos):
            ext = os.path.splitext(nombre)[1].lower()
            if ext in EXTENSIONES_NO_SOPORTADAS_WEB:
                resultado["no_soportados"] += 1
                continue
            if ext not in EXTENSIONES_MATERIAL:
                continue
            resultado["total"] += 1
            if gestor_archivos.verificar_material_ingestado(nombre):
                resultado["omitidos"] += 1
                continue
            ruta = os.path.join(raiz, nombre)
            resultado["pendientes"].append(
                {"nombre": nombre, "ruta": ruta, "tipo": clasificar_tipo_material(ruta, carpeta)}
            )
    return resultado


def escanear(materias: list[str]) -> list[dict]:
    return [escanear_materia(m) for m in materias]


def ingestar_pendientes_stream(materias: list[str]) -> Iterator[dict]:
    """
    Procesa los archivos nuevos de las asignaturas indicadas, emitiendo eventos de progreso:
    {"evento": "inicio"|"archivo"|"fin", ...}.
    """
    escaneos = escanear(materias)
    total = sum(len(e["pendientes"]) for e in escaneos)
    yield {"evento": "inicio", "total": total, "materias": materias}

    exitosos = fallidos = 0
    hecho = 0
    for escaneo in escaneos:
        for item in escaneo["pendientes"]:
            hecho += 1
            base = {
                "evento": "archivo",
                "indice": hecho,
                "total": total,
                "materia": escaneo["materia"],
                "archivo": item["nombre"],
                "tipo": item["tipo"],
            }
            try:
                r = ingestar_archivo(item["ruta"], item["nombre"], escaneo["materia"], item["tipo"])
                exitosos += 1
                al = r.get("alineacion") or {}
                yield {
                    **base,
                    "ok": True,
                    "clase_asignada": al.get("clase_asignada"),
                    "afinidad": al.get("peso_afinidad"),
                    "ruta_salida": r["ruta_salida"],
                }
            except Exception as e:
                fallidos += 1
                yield {**base, "ok": False, "error": str(e)}

    yield {
        "evento": "fin",
        "exitosos": exitosos,
        "fallidos": fallidos,
        "omitidos": sum(e["omitidos"] for e in escaneos),
    }
