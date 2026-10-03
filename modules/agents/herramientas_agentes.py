import os
import subprocess
from datetime import datetime

from crewai.tools import tool


@tool
def ejecutar_pruebas(query: str = ""):
    """Ejecuta pytest y ruff para verificar la calidad del código."""
    try:
        pytest_res = subprocess.run(
            ["pytest", "tests/"], capture_output=True, text=True, encoding="utf-8"
        )
        ruff_res = subprocess.run(
            ["ruff", "check", "."], capture_output=True, text=True, encoding="utf-8"
        )
        return f"Pytest: {pytest_res.stdout}\nRuff: {ruff_res.stdout}\nErrores: {pytest_res.stderr} {ruff_res.stderr}"
    except Exception as e:
        return f"Error ejecutando pruebas: {e!s}"


@tool
def modificar_codigo(ruta_archivo: str, nuevo_codigo: str):
    """Sobrescribe un archivo con nuevo código."""
    try:
        import difflib

        os.makedirs("data/config", exist_ok=True)
        log_path = "data/config/agent_changes.log"

        contenido_anterior = ""
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, "r", encoding="utf-8") as f:
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

        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(nuevo_codigo)
        return f"Archivo {ruta_archivo} actualizado correctamente."
    except Exception as e:
        return f"Error modificando archivo: {e!s}"


@tool
def ejecutar_git(mensaje_commit: str = ""):
    """Realiza git add y commit manejando pre-commit hooks con resiliencia y reportando errores claramente."""
    try:
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if not status_res.stdout.strip():
            return "No hay cambios para commitear."

        if not mensaje_commit:
            mensaje_commit = "chore: actualización del sistema"
        else:
            prefixes = ("feat:", "fix:", "docs:", "chore:", "refactor:", "test:")
            if not mensaje_commit.startswith(prefixes):
                mensaje_commit = f"chore: {mensaje_commit}"

        subprocess.run(["git", "add", "."], capture_output=True, text=True, encoding="utf-8")

        res = subprocess.run(
            ["git", "commit", "-m", mensaje_commit],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if res.returncode != 0:
            subprocess.run(["git", "add", "."], capture_output=True, text=True, encoding="utf-8")
            res2 = subprocess.run(
                ["git", "commit", "-m", mensaje_commit],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if res2.returncode != 0:
                return f"Fallo al hacer commit. Error de Git/pre-commit: {res2.stdout} \n {res2.stderr}"

        return "Commit realizado exitosamente."
    except Exception as e:
        return f"Error en Git: {e!s}"


@tool
def actualizar_documentacion(resumen: str):
    """Actualiza o crea el archivo docs/CHANGELOG.md añadiendo un bloque con la fecha actual y los cambios realizados."""
    try:
        os.makedirs("docs", exist_ok=True)
        changelog_path = "docs/CHANGELOG.md"
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

        subprocess.run(["git", "add", changelog_path], check=True)
        return f"Documentación actualizada en {changelog_path} y añadida a git."
    except Exception as e:
        return f"Error actualizando documentación: {e!s}"
