from crewai.tools import tool
import subprocess
import os
from datetime import datetime


@tool
def ejecutar_pruebas(query: str = ""):
    """Ejecuta pytest y ruff para verificar la calidad del código."""
    try:
        pytest_res = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)
        ruff_res = subprocess.run(["ruff", "check", "."], capture_output=True, text=True)
        return f"Pytest: {pytest_res.stdout}\nRuff: {ruff_res.stdout}\nErrores: {pytest_res.stderr} {ruff_res.stderr}"
    except Exception as e:
        return f"Error ejecutando pruebas: {str(e)}"


@tool
def modificar_codigo(ruta_archivo: str, nuevo_codigo: str):
    """Sobrescribe un archivo con nuevo código."""
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(nuevo_codigo)
        return f"Archivo {ruta_archivo} actualizado correctamente."
    except Exception as e:
        return f"Error modificando archivo: {str(e)}"


@tool
def ejecutar_git(mensaje_commit: str = ""):
    """Realiza git add y commit validando conventional commits."""
    try:
        prefixes = ("feat:", "fix:", "docs:", "chore:", "refactor:", "test:")
        if not mensaje_commit.startswith(prefixes):
            mensaje_commit = f"chore: {mensaje_commit}"
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", mensaje_commit], check=True)
        return f"Cambios consolidados en Git con mensaje: {mensaje_commit}"
    except Exception as e:
        return f"Error en Git: {str(e)}"


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
        return f"Error actualizando documentación: {str(e)}"
