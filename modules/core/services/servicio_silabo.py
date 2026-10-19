"""
Servicio de aplicación para extracción de cronogramas desde sílabos (`ml es`).

Versión sin I/O de consola: recibe rutas/archivos y devuelve datos estructurados.
"""

import json
import os

from pypdf import PdfReader

from modules.core.services import gestor_archivos, gestor_llm

EXTENSIONES_SILABO = (".pdf", ".md", ".txt")


def extraer_texto_local(ruta_archivo: str) -> str:
    """Extrae el texto de un archivo local (PDF, Markdown o TXT)."""
    ext = os.path.splitext(ruta_archivo)[1].lower()
    if ext == ".pdf":
        try:
            reader = PdfReader(ruta_archivo)
            return "\n".join(t for t in (p.extract_text() for p in reader.pages) if t)
        except Exception as e:
            raise RuntimeError(f"No se pudo extraer texto del PDF con pypdf: {e}") from e
    try:
        with open(ruta_archivo, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(ruta_archivo, encoding="latin-1") as f:
            return f.read()


def delimitar_seccion_temas(texto: str) -> str:
    """Delimita el texto para analizar únicamente la Sección 4.2 del sílabo."""
    inicio_clave = "4.2 Estructura de la unidad didáctica por temas"
    fin_clave = "4.3 Distribución de horas en unidades y temas"
    texto_lower = texto.lower()
    pos_inicio = texto_lower.find(inicio_clave.lower())

    if pos_inicio == -1:
        for variante in [
            "4.2. estructura",
            "4.2 estructura",
            "unidad didáctica por temas",
            "estructura de la unidad",
        ]:
            pos_inicio = texto_lower.find(variante)
            if pos_inicio != -1:
                break

    pos_fin = texto_lower.find(fin_clave.lower())
    if pos_fin == -1:
        for variante in ["4.3.", "4.3 distribución", "5. metodología", "5. sistema", "bibliografía"]:
            pos_fin = texto_lower.find(variante)
            if pos_fin != -1 and pos_fin > pos_inicio:
                break

    if pos_inicio != -1:
        recortado = texto[pos_inicio:]
        if pos_fin != -1 and pos_fin > pos_inicio:
            recortado = recortado[: pos_fin - pos_inicio]
        return recortado
    return texto[:30000] if len(texto) > 30000 else texto


def sugerir_nombre_materia(nombre_archivo: str) -> str:
    """Sugiere el nombre de la asignatura a partir del nombre del archivo."""
    base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    sugerido = base.replace("SYLLABUS", "").replace("syllabus", "").replace("-", "").strip()
    return sugerido or base


def slug_materia(nombre_materia: str) -> str:
    return (
        "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in nombre_materia)
        .strip()
        .replace(" ", "_")
    )


def normalizar_cronograma(datos: dict | list) -> dict:
    """Devuelve siempre {"clases": [...]} sin importar si el LLM respondió con lista u objeto."""
    if isinstance(datos, list):
        return {"clases": datos}
    if isinstance(datos, dict):
        if isinstance(datos.get("clases"), list):
            return datos
        for valor in datos.values():
            if isinstance(valor, list) and valor and isinstance(valor[0], dict):
                return {**{k: v for k, v in datos.items() if v is not valor}, "clases": valor}
    raise ValueError("La IA no devolvió un cronograma de clases válido.")


def extraer_cronograma(ruta_archivo: str, nombre_materia: str) -> dict:
    """Analiza el sílabo con el LLM y devuelve el cronograma estructurado (sin guardarlo)."""
    contenido_bruto = extraer_texto_local(ruta_archivo)
    if not contenido_bruto.strip():
        raise ValueError("El archivo está vacío o no contiene texto extraíble.")
    contenido_texto = delimitar_seccion_temas(contenido_bruto)

    prompt = gestor_archivos.leer_prompt("04_extraccion_silabo.md").format(
        materia=nombre_materia, contenido_texto=contenido_texto
    )
    datos = gestor_llm.obtener_llm().generar_json_estructurado(prompt)
    return normalizar_cronograma(datos)


def guardar_cronograma(nombre_materia: str, datos: dict | list) -> str:
    """Guarda el cronograma en data/schedules/ y registra la materia. Retorna la ruta."""
    carpeta = os.path.join("data", "schedules")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f"{slug_materia(nombre_materia)}_cronograma.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    gestor_archivos.agregar_materia(nombre_materia)
    return ruta
