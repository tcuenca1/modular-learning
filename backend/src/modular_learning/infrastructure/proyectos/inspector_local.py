"""Lectura en disco de los proyectos de una asignatura (estructura, huella y contexto)."""

from __future__ import annotations

import hashlib
import os
from typing import Any

from modular_learning.core.domain.proyectos import HuellaProyecto, ParcialProyecto, TipoProyecto
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.proyectos import InspectorProyectosPort

CARPETAS_IGNORADAS_PROYECTO = {
    "node_modules",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "out",
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".idea",
    ".vscode",
    ".turbo",
    ".cache",
    "coverage",
    ".pytest_cache",
}

EXTENSIONES_DOCUMENTO = {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx"}
EXTENSIONES_TEXTO = {".docx", ".txt", ".md"}
MARCAS_FASES = ("01_", "02_", "03_", "04_", "normativa", "entregable", "estructura", "fase")
ARCHIVOS_MANIFIESTO = {"package.json", "pyproject.toml", "cargo.toml", "go.mod"}
EXTENSIONES_CODIGO = (".js", ".ts", ".py", ".html", ".css", ".php", ".java")
MAX_CARACTERES_DOCUMENTO = 12000
MAX_LINEAS_ARBOL = 40


def _es_ignorado(nombre: str) -> bool:
    return nombre.startswith(".env") or nombre.endswith(".tmp")


def _parcial_de_carpeta(nombre: str) -> ParcialProyecto:
    nombre = nombre.upper()
    if "PRIMER" in nombre or "1" in nombre:
        return "primer_parcial"
    if "SEGUNDO" in nombre or "2" in nombre:
        return "segundo_parcial"
    return "general"


class InspectorProyectosLocal(InspectorProyectosPort):
    """Recorre las carpetas de proyectos ignorando dependencias, compilados y secretos."""

    def __init__(self, lector_docs: LectorDocumentosPort):
        self.lector_docs = lector_docs

    def _recorrer(self, ruta: str):
        for root, dirs, files in os.walk(ruta):
            dirs[:] = [d for d in dirs if d not in CARPETAS_IGNORADAS_PROYECTO]
            yield root, dirs, files

    def _candidatos(self, carpeta: str, parcial: ParcialProyecto) -> list[dict[str, Any]]:
        encontrados = []
        for item in sorted(os.listdir(carpeta)):
            ruta = os.path.join(carpeta, item)
            nombre_base, ext = os.path.splitext(item)
            es_carpeta = os.path.isdir(ruta)
            if es_carpeta or ext.lower() in EXTENSIONES_DOCUMENTO:
                encontrados.append(
                    {
                        "parcial": parcial,
                        "nombre": item if es_carpeta else nombre_base,
                        "ruta": ruta,
                        "tipo": self.detectar_tipo(ruta),
                    }
                )
        return encontrados

    def escanear(self, carpeta_materia: str) -> list[dict[str, Any]]:
        if not os.path.isdir(carpeta_materia):
            return []
        detectados: list[dict[str, Any]] = []
        for entrada in sorted(os.listdir(carpeta_materia)):
            ruta_entrada = os.path.join(carpeta_materia, entrada)
            if not os.path.isdir(ruta_entrada):
                continue
            nombre = entrada.upper().strip()
            if nombre == "PROYECTO":
                detectados.extend(self._candidatos(ruta_entrada, "general"))
            elif nombre == "PROYECTOS":
                for sub in sorted(os.listdir(ruta_entrada)):
                    ruta_sub = os.path.join(ruta_entrada, sub)
                    if os.path.isdir(ruta_sub):
                        detectados.extend(self._candidatos(ruta_sub, _parcial_de_carpeta(sub)))
        return detectados

    def huella(self, ruta: str) -> HuellaProyecto | None:
        if not os.path.exists(ruta):
            return None
        if os.path.isfile(ruta):
            mtime = os.path.getmtime(ruta)
            size = os.path.getsize(ruta)
            firma = f"{os.path.basename(ruta)}:{mtime}:{size}"
            return HuellaProyecto(mtime, 1, hashlib.sha1(firma.encode()).hexdigest()[:12])

        mtime_max = 0.0
        elementos: list[str] = []
        for root, _dirs, files in self._recorrer(ruta):
            for f in sorted(files):
                if _es_ignorado(f):
                    continue
                f_path = os.path.join(root, f)
                try:
                    stat = os.stat(f_path)
                except OSError:
                    continue
                mtime_max = max(mtime_max, stat.st_mtime)
                elementos.append(f"{os.path.relpath(f_path, ruta)}:{stat.st_mtime}:{stat.st_size}")

        # Una muestra de los primeros archivos basta para notar cambios sin leer su contenido
        muestra = "\n".join(elementos[:200])
        h = hashlib.sha1(muestra.encode()).hexdigest()[:12] if elementos else "vacio"
        return HuellaProyecto(mtime_max, len(elementos), h)

    def detectar_tipo(self, ruta: str) -> TipoProyecto:
        if os.path.isfile(ruta):
            return "documento_rector"
        tiene_codigo = tiene_flujos_nr = False
        for _root, _dirs, files in self._recorrer(ruta):
            for f in files:
                f_low = f.lower()
                if f_low.endswith(".json") and any(
                    k in f_low for k in ("flow", "flujo", "nodered")
                ):
                    tiene_flujos_nr = True
                if f_low in ARCHIVOS_MANIFIESTO or f_low.endswith(EXTENSIONES_CODIGO):
                    tiene_codigo = True
        if tiene_flujos_nr:
            return "iot"
        if tiene_codigo:
            return "software"
        # Carpetas por fases (01_..., Entregables) o cualquier otra: documentación
        return "documental_auditoria"

    def extraer_contexto(self, ruta: str) -> str:
        if os.path.isfile(ruta):
            ext = os.path.splitext(ruta)[1].lower()
            if ext in EXTENSIONES_TEXTO:
                texto = self.lector_docs.extraer_texto(ruta)
                return (
                    texto[:MAX_CARACTERES_DOCUMENTO]
                    if texto
                    else "Documento de especificación sin texto extraíble."
                )
            return f"Archivo binario rector de proyecto ({ext})"

        lineas = [f"Árbol de directorios de {os.path.basename(ruta)}:"]
        for root, _dirs, files in self._recorrer(ruta):
            rel = os.path.relpath(root, ruta)
            sangria = "  " * (0 if rel == "." else rel.count(os.sep) + 1)
            if rel != ".":
                lineas.append(f"{sangria}📁 {os.path.basename(root)}/")
            lineas.extend(f"{sangria}  📄 {f}" for f in files[:8] if not _es_ignorado(f))
            if len(lineas) > MAX_LINEAS_ARBOL:
                lineas.append("  ... (demás archivos omitidos para brevedad)")
                break

        for nombre in ("README.md", "LEEME.md", "readme.txt"):
            r_path = os.path.join(ruta, nombre)
            if os.path.isfile(r_path):
                try:
                    with open(r_path, encoding="utf-8", errors="replace") as archivo:
                        primeras = [archivo.readline() for _ in range(30)]
                except OSError:
                    continue
                lineas.append(f"\nREADME detectado en el proyecto:\n{''.join(primeras)}")
                break

        return "\n".join(lineas)


__all__ = ["CARPETAS_IGNORADAS_PROYECTO", "EXTENSIONES_DOCUMENTO", "InspectorProyectosLocal"]
