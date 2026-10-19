"""Servicio de aplicación para extracción y procesamiento de cronogramas desde sílabos."""

from __future__ import annotations

import os
from typing import Any

from pypdf import PdfReader

from modular_learning import settings
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.llm import LLMPort
from modular_learning.core.ports.repositorios import CronogramaRepo, MateriaRepo

EXTENSIONES_SILABO = (".pdf", ".md", ".txt")


class SilaboService:
    """Caso de uso para el análisis y extracción estructurada de sílabos (`ml es`)."""

    def __init__(
        self,
        llm: LLMPort,
        cronograma_repo: CronogramaRepo,
        materia_repo: MateriaRepo,
        lector_docs: LectorDocumentosPort,
        carpeta_schedules: str | None = None,
    ):
        self.llm = llm
        self.cronograma_repo = cronograma_repo
        self.materia_repo = materia_repo
        self.lector_docs = lector_docs
        self._carpeta_schedules = carpeta_schedules

    @property
    def carpeta_schedules(self) -> str:
        return self._carpeta_schedules or str(settings.ruta_cronogramas())

    def extraer_texto_local(self, ruta_archivo: str) -> str:
        """Extrae el contenido textual de un archivo local (PDF, Markdown o TXT)."""
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

    def delimitar_seccion_temas(self, texto: str) -> str:
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
            for variante in [
                "4.3.",
                "4.3 distribución",
                "5. metodología",
                "5. sistema",
                "bibliografía",
            ]:
                pos_fin = texto_lower.find(variante)
                if pos_fin != -1 and pos_fin > pos_inicio:
                    break

        if pos_inicio != -1:
            recortado = texto[pos_inicio:]
            if pos_fin != -1 and pos_fin > pos_inicio:
                recortado = recortado[: pos_fin - pos_inicio]
            return recortado
        return texto[:30000] if len(texto) > 30000 else texto

    def sugerir_nombre_materia(self, nombre_archivo: str) -> str:
        """Sugiere el nombre de la asignatura a partir del nombre del archivo."""
        base = os.path.splitext(os.path.basename(nombre_archivo))[0]
        sugerido = (
            base.replace("SYLLABUS", "").replace("syllabus", "").replace("-", "").strip()
        )
        return sugerido or base

    def slug_materia(self, nombre_materia: str) -> str:
        return (
            "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in nombre_materia)
            .strip()
            .replace(" ", "_")
        )

    def normalizar_cronograma(self, datos: dict | list) -> dict:
        """Devuelve siempre {'clases': [...]} sin importar el envoltorio que devuelva el LLM."""
        if isinstance(datos, list):
            return {"clases": datos}
        if isinstance(datos, dict):
            if isinstance(datos.get("clases"), list):
                return datos
            for valor in datos.values():
                if isinstance(valor, list) and valor and isinstance(valor[0], dict):
                    return {**{k: v for k, v in datos.items() if v is not valor}, "clases": valor}
        raise ValueError("La IA no devolvió un cronograma de clases válido.")

    def extraer_cronograma(self, ruta_archivo: str, nombre_materia: str) -> dict:
        """Analiza el sílabo con el LLM y devuelve el cronograma estructurado."""
        contenido_bruto = self.extraer_texto_local(ruta_archivo)
        if not contenido_bruto.strip():
            raise ValueError("El archivo está vacío o no contiene texto extraíble.")
        contenido_texto = self.delimitar_seccion_temas(contenido_bruto)

        try:
            plantilla = self.lector_docs.leer_prompt("04_extraccion_silabo.md")
            prompt = plantilla.format(materia=nombre_materia, contenido_texto=contenido_texto)
        except Exception:
            prompt = (
                f"Extrae el cronograma de clases en JSON.\n\n"
                f"Contenido de la Sección del Sílabo ({nombre_materia}):\n"
                f"----------------------------------------\n"
                f"{contenido_texto}\n"
                f"----------------------------------------"
            )

        datos = self.llm.generar_json_estructurado(prompt)
        return self.normalizar_cronograma(datos)

    def guardar_cronograma(self, nombre_materia: str, datos: dict | list) -> str:
        """Guarda el cronograma en el repositorio y registra la materia."""
        cronograma_norm = self.normalizar_cronograma(datos)
        clases = cronograma_norm.get("clases", [])
        self.cronograma_repo.guardar_cronograma(nombre_materia, clases)
        self.materia_repo.agregar_materia(nombre_materia)

        ruta = os.path.join(self.carpeta_schedules, f"{self.slug_materia(nombre_materia)}_cronograma.json")
        return ruta

    def procesar_archivo_individual(self, ruta_archivo: str, nombre_materia: str | None = None) -> dict[str, Any]:
        """Procesa un archivo de sílabo individual extrayendo y persistiendo su cronograma."""
        if not nombre_materia:
            nombre_materia = self.sugerir_nombre_materia(ruta_archivo)

        datos = self.extraer_cronograma(ruta_archivo, nombre_materia)
        ruta_salida = self.guardar_cronograma(nombre_materia, datos)
        clases = datos.get("clases", [])
        return {
            "materia": nombre_materia,
            "clases": clases,
            "total_clases": len(clases),
            "ruta_salida": ruta_salida,
        }

    def escanear_directorio_silabos(self, ruta_carpeta: str) -> list[str]:
        """Retorna todos los archivos compatibles (.pdf, .md, .txt) dentro de una carpeta."""
        if not os.path.isdir(ruta_carpeta):
            return []
        return [
            os.path.join(ruta_carpeta, f)
            for f in os.listdir(ruta_carpeta)
            if os.path.isfile(os.path.join(ruta_carpeta, f))
            and f.lower().endswith(EXTENSIONES_SILABO)
        ]


_instancia_por_defecto: SilaboService | None = None


def configurar_servicio_defecto(servicio: SilaboService) -> None:
    global _instancia_por_defecto
    _instancia_por_defecto = servicio


def extraer_cronograma(ruta_archivo: str, nombre_materia: str) -> dict:
    if _instancia_por_defecto is None:
        raise RuntimeError("SilaboService no inicializado en el contenedor.")
    return _instancia_por_defecto.extraer_cronograma(ruta_archivo, nombre_materia)


def guardar_cronograma(nombre_materia: str, datos: dict | list) -> str:
    if _instancia_por_defecto is None:
        raise RuntimeError("SilaboService no inicializado en el contenedor.")
    return _instancia_por_defecto.guardar_cronograma(nombre_materia, datos)


def sugerir_nombre_materia(nombre_archivo: str) -> str:
    base = os.path.splitext(os.path.basename(nombre_archivo))[0]
    sugerido = base.replace("SYLLABUS", "").replace("syllabus", "").replace("-", "").strip()
    return sugerido or base


__all__ = [
    "EXTENSIONES_SILABO",
    "SilaboService",
    "configurar_servicio_defecto",
    "extraer_cronograma",
    "guardar_cronograma",
    "sugerir_nombre_materia",
]
