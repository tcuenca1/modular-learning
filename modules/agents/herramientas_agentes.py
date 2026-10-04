import os
import subprocess
from datetime import datetime

from crewai.tools import tool

BASE_PATH = os.environ.get("TARGET_PROJECT_PATH", os.getcwd())


def _resolver_ruta(ruta_archivo: str) -> str:
    base = os.path.abspath(BASE_PATH)
    if os.path.isabs(ruta_archivo):
        completa = os.path.abspath(ruta_archivo)
    else:
        completa = os.path.abspath(os.path.join(base, ruta_archivo))
    if not completa.startswith(base):
        return base
    return completa


@tool
def ejecutar_pruebas(query: str = ""):
    """Ejecuta pytest y ruff para verificar la calidad del código en el proyecto objetivo."""
    try:
        pytest_res = subprocess.run(
            ["pytest", "tests/"], capture_output=True, text=True, encoding="utf-8", cwd=BASE_PATH
        )
        ruff_res = subprocess.run(
            ["ruff", "check", "."], capture_output=True, text=True, encoding="utf-8", cwd=BASE_PATH
        )
        return f"Pytest: {pytest_res.stdout}\nRuff: {ruff_res.stdout}\nErrores: {pytest_res.stderr} {ruff_res.stderr}"
    except Exception as e:
        return f"Error ejecutando pruebas: {e!s}"


@tool
def leer_archivo(ruta_archivo: str):
    """Lee y retorna el contenido completo de un archivo (OBLIGATORIO antes de modificar cualquier archivo de documentación para preservar su contexto histórico)."""
    try:
        path_real = _resolver_ruta(ruta_archivo)
        if not os.path.exists(path_real):
            return f"Error: El archivo {ruta_archivo} no existe."
        with open(path_real, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo archivo: {e!s}"


@tool
def modificar_codigo(ruta_archivo: str, nuevo_codigo: str):
    """Sobrescribe un archivo con nuevo código en el proyecto objetivo."""
    try:
        import difflib

        path_real = _resolver_ruta(ruta_archivo)
        os.makedirs(os.path.dirname(path_real), exist_ok=True)

        log_dir = os.path.join(BASE_PATH, "data", "config")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "agent_changes.log")

        contenido_anterior = ""
        if os.path.exists(path_real):
            with open(path_real, "r", encoding="utf-8") as f:
                contenido_anterior = f.read()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        diff = "".join(
            difflib.unified_diff(
                contenido_anterior.splitlines(keepends=True),
                nuevo_codigo.splitlines(keepends=True),
                fromfile=f"a/{ruta_archivo}",
                tofile=f"b/{ruta_archivo}",
            )
        )
        if not diff:
            diff = "Sin cambios aparentes en el contenido."

        log_entry = (
            f"[{timestamp}] Archivo modificado: {ruta_archivo}\n--- Diff / Resumen ---\n{diff}\n"
            + "=" * 60
            + "\n"
        )

        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

        with open(path_real, "w", encoding="utf-8") as f:
            f.write(nuevo_codigo)
        return f"Archivo {ruta_archivo} actualizado correctamente."
    except Exception as e:
        return f"Error modificando archivo: {e!s}"


@tool
def ejecutar_git(mensaje_commit: str = ""):
    """Realiza git add y commit manejando pre-commit hooks con resiliencia y reportando errores claramente en el proyecto objetivo."""
    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=BASE_PATH,
        )
        if not status_res.stdout.strip():
            return "No hay cambios para commitear."

        if not mensaje_commit:
            mensaje_commit = "chore: actualización del sistema"
        else:
            prefixes = ("feat:", "fix:", "docs:", "chore:", "refactor:", "test:")
            if not mensaje_commit.startswith(prefixes):
                mensaje_commit = f"chore: {mensaje_commit}"

        subprocess.run(
            ["git", "add", "."], capture_output=True, text=True, encoding="utf-8", cwd=BASE_PATH
        )

        res = subprocess.run(
            ["git", "commit", "-m", mensaje_commit],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=BASE_PATH,
        )
        if res.returncode != 0:
            subprocess.run(
                ["git", "add", "."], capture_output=True, text=True, encoding="utf-8", cwd=BASE_PATH
            )
            res2 = subprocess.run(
                ["git", "commit", "-m", mensaje_commit],
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=BASE_PATH,
            )
            if res2.returncode != 0:
                return f"Fallo al hacer commit. Error de Git/pre-commit: {res2.stdout} \n {res2.stderr}"

        return "Commit realizado exitosamente."
    except Exception as e:
        return f"Error en Git: {e!s}"


@tool
def actualizar_documentacion(resumen: str):
    """Actualiza o crea el archivo docs/CHANGELOG.md añadiendo un bloque con la fecha actual y los cambios realizados en el proyecto objetivo."""
    try:
        docs_dir = os.path.join(BASE_PATH, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        changelog_path = os.path.join(docs_dir, "CHANGELOG.md")
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nuevo_bloque = f"\n## [{fecha_actual}]\n- {resumen}\n"

        contenido_actual = ""
        if os.path.exists(changelog_path):
            with open(changelog_path, "r", encoding="utf-8") as f:
                contenido_actual = f.read()

        if not contenido_actual.strip():
            contenido_actual = "# Changelog\n"

        nuevo_contenido = contenido_actual + nuevo_bloque
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)

        subprocess.run(["git", "add", "docs/CHANGELOG.md"], check=True, cwd=BASE_PATH)
        return "Documentación actualizada en docs/CHANGELOG.md y añadida a git."
    except Exception as e:
        return f"Error actualizando documentación: {e!s}"
