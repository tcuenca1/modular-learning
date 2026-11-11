"""Adaptador práctico para Desarrollo y Programación Web (y proyectos de software)."""

from __future__ import annotations

import json
import os
import re
import subprocess
from typing import Any

from modular_learning.core.ports.plugin_practico import PluginMetadatos, PluginPracticoBase
from modular_learning.infrastructure.persistence.almacen import DocumentoJson

CARPETAS_IGNORADAS = {
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


def es_archivo_secreto(nombre: str) -> bool:
    """Verifica si un archivo contiene secretos, variables de entorno o credenciales."""
    nombre_lower = nombre.lower()
    return (
        nombre_lower.startswith(".env")
        or "secret" in nombre_lower
        or "credential" in nombre_lower
        or nombre_lower.endswith((".env", ".pem", ".key", ".pfx", ".p12"))
    )


def extraer_readme(ruta_carpeta: str) -> str | None:
    """Busca y extrae una descripción breve del README del proyecto."""
    for nombre in ["README.md", "readme.md", "README.txt", "README"]:
        ruta = os.path.join(ruta_carpeta, nombre)
        if os.path.isfile(ruta):
            try:
                with open(ruta, "r", encoding="utf-8", errors="replace") as f:
                    lineas = [f.readline() for _ in range(40)]
                limpias = []
                for linea in lineas:
                    l = linea.strip()
                    if not l or l.startswith(("[![", "<img", "<!--")):
                        continue
                    limpias.append(l)
                    if len(limpias) >= 8:
                        break
                return "\n".join(limpias) if limpias else None
            except Exception:
                pass
    return None


def extraer_stack_dependencias(ruta_carpeta: str) -> dict[str, Any]:
    """Detecta el stack y dependencias de package.json, pyproject.toml o requirements.txt."""
    resultado: dict[str, Any] = {
        "nombre": None,
        "lenguaje_ecosistema": None,
        "frameworks": [],
        "dependencias": [],
        "scripts": [],
    }

    # 1. Node.js / JavaScript / TypeScript
    pkg_path = os.path.join(ruta_carpeta, "package.json")
    if os.path.isfile(pkg_path):
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            resultado["nombre"] = data.get("name")
            resultado["lenguaje_ecosistema"] = "Node.js / JavaScript / TypeScript"
            deps = list(data.get("dependencies", {}).keys())
            dev_deps = list(data.get("devDependencies", {}).keys())
            todas_deps = deps + dev_deps
            resultado["dependencias"] = todas_deps[:15]
            resultado["scripts"] = list(data.get("scripts", {}).keys())[:6]

            # Detectar frameworks
            for d in todas_deps:
                d_low = d.lower()
                for fw in [
                    "react",
                    "vue",
                    "angular",
                    "next",
                    "nuxt",
                    "svelte",
                    "express",
                    "nest",
                    "fastify",
                    "tailwind",
                    "prisma",
                ]:
                    if fw in d_low and fw not in resultado["frameworks"]:
                        resultado["frameworks"].append(fw)
        except Exception:
            pass

    # 2. Python
    pyproject_path = os.path.join(ruta_carpeta, "pyproject.toml")
    req_path = os.path.join(ruta_carpeta, "requirements.txt")
    if os.path.isfile(pyproject_path) or os.path.isfile(req_path):
        if not resultado["lenguaje_ecosistema"]:
            resultado["lenguaje_ecosistema"] = "Python"
        if os.path.isfile(req_path):
            try:
                with open(req_path, "r", encoding="utf-8") as f:
                    reqs = [
                        line.split("==")[0].split(">=")[0].strip()
                        for line in f
                        if line.strip() and not line.strip().startswith("#")
                    ]
                resultado["dependencias"].extend(reqs[:15])
            except Exception:
                pass
        if os.path.isfile(pyproject_path):
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    texto = f.read()
                # Extraer nombre
                m_nom = re.search(r'name\s*=\s*["\']([^"\']+)["\']', texto)
                if m_nom and not resultado["nombre"]:
                    resultado["nombre"] = m_nom.group(1)
            except Exception:
                pass

    return resultado


def explorar_estructura(ruta_carpeta: str, profundidad_max: int = 2) -> list[str]:
    """Explora la jerarquía de carpetas ignorando dependencias y secretos."""
    lineas_arbol: list[str] = []
    base_len = len(os.path.normpath(ruta_carpeta))

    for root, dirs, files in os.walk(ruta_carpeta):
        rel = os.path.normpath(root)[base_len:].lstrip(os.sep)
        profundidad = rel.count(os.sep) + 1 if rel else 0
        if profundidad > profundidad_max:
            dirs.clear()
            continue

        # Filtrar directorios ignorados in-place
        dirs[:] = [d for d in dirs if d not in CARPETAS_IGNORADAS and not es_archivo_secreto(d)]

        if rel:
            indent = "  " * (profundidad - 1)
            lineas_arbol.append(f"{indent}- 📁 `{rel}/`")

        archivos_mostrar = [
            f
            for f in files
            if not es_archivo_secreto(f)
            and f.endswith(
                (
                    ".js",
                    ".ts",
                    ".jsx",
                    ".tsx",
                    ".py",
                    ".html",
                    ".css",
                    ".json",
                    ".sql",
                    ".prisma",
                    ".php",
                )
            )
        ][:5]
        indent_arch = "  " * profundidad
        for arch in archivos_mostrar:
            lineas_arbol.append(f"{indent_arch}- 📄 `{arch}`")

        if len(lineas_arbol) > 25:
            lineas_arbol.append("  - ... (demás archivos omitidos para brevedad)")
            break

    return lineas_arbol


def extraer_rutas_y_modelos(ruta_carpeta: str) -> tuple[list[str], list[str]]:
    """Detecta definiciones de endpoints y modelos de datos en archivos fuente."""
    rutas_encontradas: list[str] = []
    modelos_encontrados: list[str] = []

    archivos_inspeccionar: list[str] = []
    for root, dirs, files in os.walk(ruta_carpeta):
        dirs[:] = [d for d in dirs if d not in CARPETAS_IGNORADAS and not es_archivo_secreto(d)]
        for f in files:
            f_low = f.lower()
            if es_archivo_secreto(f):
                continue
            if any(
                k in f_low
                for k in [
                    "route",
                    "router",
                    "controller",
                    "endpoint",
                    "api",
                    "model",
                    "schema",
                    "entity",
                ]
            ) and f.endswith((".ts", ".js", ".py", ".prisma", ".php")):
                archivos_inspeccionar.append(os.path.join(root, f))
                if len(archivos_inspeccionar) >= 8:
                    break
        if len(archivos_inspeccionar) >= 8:
            break

    for arch in archivos_inspeccionar:
        try:
            with open(arch, "r", encoding="utf-8", errors="replace") as file_obj:
                lineas = [file_obj.readline() for _ in range(120)]
            for linea in lineas:
                l = linea.strip()
                # Detección de rutas (Express, FastAPI, Next.js, etc.)
                m_ruta = re.search(
                    r'(?:router|app)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                    l,
                    re.IGNORECASE,
                )
                if m_ruta:
                    metodo, path = m_ruta.groups()
                    item = f"{metodo.upper()} {path}"
                    if item not in rutas_encontradas:
                        rutas_encontradas.append(item)

                m_fastapi = re.search(
                    r'@(?:app|router)\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                    l,
                    re.IGNORECASE,
                )
                if m_fastapi:
                    metodo, path = m_fastapi.groups()
                    item = f"{metodo.upper()} {path}"
                    if item not in rutas_encontradas:
                        rutas_encontradas.append(item)

                # Detección de modelos / entidades
                m_modelo = re.search(r"class\s+([A-Za-z0-9_]+)\s*(?:\([^)]+\))?:", l)
                if m_modelo and any(
                    kw in l.lower() for kw in ["basemodel", "model", "schema", "entity"]
                ):
                    mod_nom = m_modelo.group(1)
                    if mod_nom not in modelos_encontrados:
                        modelos_encontrados.append(mod_nom)

                m_ts_iface = re.search(r"(?:export\s+)?(?:interface|type)\s+([A-Za-z0-9_]+)", l)
                if m_ts_iface:
                    iface_nom = m_ts_iface.group(1)
                    if iface_nom not in modelos_encontrados and iface_nom.lower() not in [
                        "props",
                        "state",
                    ]:
                        modelos_encontrados.append(iface_nom)

                m_prisma = re.search(r"^model\s+([A-Za-z0-9_]+)\s*\{", l)
                if m_prisma:
                    p_nom = m_prisma.group(1)
                    if p_nom not in modelos_encontrados:
                        modelos_encontrados.append(p_nom)
        except Exception:
            pass

    return rutas_encontradas[:8], modelos_encontrados[:8]


def extraer_git_log(ruta_carpeta: str) -> list[str]:
    """Obtiene los últimos commits del repositorio git local si existe."""
    git_dir = os.path.join(ruta_carpeta, ".git")
    if not os.path.exists(git_dir):
        return []
    try:
        res = subprocess.run(
            ["git", "log", "-n", "5", "--pretty=format:%h - %s (%cr)"],
            cwd=ruta_carpeta,
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
    except Exception:
        pass
    return []


METADATOS = PluginMetadatos(
    id="web",
    nombre="Proyectos Web y Software",
    opcion_key="Web (Proyectos)",
    categoria="Desarrollo de Software",
    descripcion=(
        "Inspecciona la estructura de tu proyecto: README, dependencias, rutas, modelos "
        "y últimos commits."
    ),
    materia_defecto="programacion-web",
    claves_seleccion=("web",),
    palabras_clave=(
        "web",
        "programacion",
        "frontend",
        "backend",
        "javascript",
        "html",
        "css",
    ),
    carpeta_convencional="Programacion Web",
    etiqueta="Web",
    titulo_carpeta_asignada="Proyecto Asignado",
    titulo_carpeta_convencional="Proyecto Convencional",
    titulo_sincronizacion="Sincronización de Programación Web",
    texto_sin_contexto="Sin proyectos web registrados.",
    orden_sincronizacion=2,
)


class WebPlugin(PluginPracticoBase):
    """Adaptador práctico para Desarrollo y Programación Web (y proyectos de software)."""

    @property
    def metadatos(self) -> PluginMetadatos:
        return METADATOS

    def analizar_carpeta(self, ruta_carpeta: str) -> str:
        return self.analizar_proyecto(ruta_carpeta)

    def __init__(self, memoria: DocumentoJson | None = None):
        self._memoria = memoria or DocumentoJson("plugins/web_memoria.json")

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        metadatos = metadatos.strip()
        if not metadatos:
            return

        historial = self._memoria.leer([])
        if not isinstance(historial, list):
            historial = []

        historial.append(metadatos)
        historial = historial[-3:]

        try:
            self._memoria.escribir(historial, sangria=4)
        except Exception as e:
            print(f"⚠️ No se pudo guardar la memoria del plugin Web: {e}")

    def cargar_contexto_reciente(self) -> str:
        try:
            historial = self._memoria.leer([])
        except Exception:
            return ""
        if isinstance(historial, list) and historial:
            return historial[-1]
        return ""

    def analizar_proyecto(self, ruta_carpeta: str) -> str:
        """
        Analiza un directorio de proyecto de desarrollo sin enviar todo el código:
        README, stack/dependencias, árbol de carpetas, rutas/modelos y commits recientes.
        Ignora node_modules, dist, .venv y archivos secretos (.env).
        """
        if not os.path.isdir(ruta_carpeta):
            return f"⚠️ La carpeta configurada para proyectos Web no existe: {ruta_carpeta}"

        nombre_carpeta = os.path.basename(os.path.normpath(ruta_carpeta))
        readme_desc = extraer_readme(ruta_carpeta)
        stack_info = extraer_stack_dependencias(ruta_carpeta)
        arbol = explorar_estructura(ruta_carpeta)
        rutas, modelos = extraer_rutas_y_modelos(ruta_carpeta)
        commits = extraer_git_log(ruta_carpeta)

        lineas = [
            "### 💻 Análisis de Proyecto de Desarrollo (Web y Software)",
            f"- **Carpeta:** `{ruta_carpeta}`",
            f"- **Nombre del proyecto:** {stack_info['nombre'] or nombre_carpeta}",
        ]

        if stack_info["lenguaje_ecosistema"]:
            lineas.append(f"- **Ecosistema:** {stack_info['lenguaje_ecosistema']}")
        if stack_info["frameworks"]:
            lineas.append(f"- **Frameworks detectados:** {', '.join(stack_info['frameworks'])}")
        if stack_info["dependencias"]:
            lineas.append(
                f"- **Dependencias principales:** {', '.join(stack_info['dependencias'][:10])}"
            )
        if stack_info["scripts"]:
            lineas.append(f"- **Scripts configurados:** {', '.join(stack_info['scripts'])}")

        if readme_desc:
            lineas.append("\n#### 📖 Descripción (README):")
            lineas.append(f"> {readme_desc.replace(chr(10), ' ')}")

        if arbol:
            lineas.append("\n#### 🗂️ Estructura del Proyecto:")
            lineas.extend(arbol)

        if rutas:
            lineas.append("\n#### 🌐 Rutas y Endpoints Detectados:")
            for r in rutas:
                lineas.append(f"- `{r}`")

        if modelos:
            lineas.append("\n#### 🧱 Modelos y Esquemas:")
            for m in modelos:
                lineas.append(f"- `{m}`")

        if commits:
            lineas.append("\n#### 📜 Últimos Commits (Git):")
            for c in commits:
                lineas.append(f"- {c}")

        resultado = "\n".join(lineas)
        self.guardar_contexto_extraido(resultado)
        return resultado

    def obtener_instrucciones_ia(self) -> str:
        contexto_extra = self.cargar_contexto_reciente()
        instrucciones = (
            "[ADAPTADOR PRÁCTICO: DESARROLLO Y PROGRAMACIÓN WEB]\n"
            "Reglas estrictas de mentoría:\n"
            "1. Enfócate en buenas prácticas de arquitectura web (separación frontend/backend, controladores, rutas, modelos).\n"
            "2. Proporciona ejemplos limpios, modernos y estructurados (HTML5 semántico, CSS/Tailwind, JavaScript ES6+ / Frameworks).\n"
            "3. Si el estudiante trabaja sobre su propio código, respeta su arquitectura y convenciones actuales.\n"
        )
        if contexto_extra:
            instrucciones += (
                f"\n[PROYECTO LOCAL REAL DEL ESTUDIANTE]:\n{contexto_extra}\n"
                "DIRECTIVA OBLIGATORIA: Basa tus explicaciones, sugerencias de código y ejemplos prácticos en la estructura de carpetas, dependencias, rutas y modelos reales detectados en este proyecto.\n"
            )
        return instrucciones

    def generar_ejercicio_base(self, tema: str) -> str:
        return (
            f"### 💻 Ejercicio Práctico de Programación Web\n"
            f"- **Tema:** {tema}\n"
            f"- **Estructura recomendada:** Modular, con controladores limpios y manejo de solicitudes HTTP.\n"
        )


__all__ = [
    "CARPETAS_IGNORADAS",
    "WebPlugin",
    "es_archivo_secreto",
    "explorar_estructura",
    "extraer_git_log",
    "extraer_readme",
    "extraer_rutas_y_modelos",
    "extraer_stack_dependencias",
]
