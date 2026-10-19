"""Configuración centralizada y resolución de rutas para Modular Learning.

Permite desacoplar el sistema del directorio de trabajo actual (CWD),
eliminando la dependencia de os.chdir() o sys.path.insert().
"""

from __future__ import annotations

import os
from pathlib import Path

# Raíz del paquete (src/modular_learning) y raíz del repositorio (ml-cli)
PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent.parent

def ruta_data() -> Path:
    """Retorna la ruta raíz del directorio de datos (resuelto dinámicamente desde ML_DATA_DIR)."""
    env_dir = os.environ.get("ML_DATA_DIR")
    if env_dir:
        return Path(env_dir).resolve()
    return (REPO_ROOT / "data").resolve()


def __getattr__(name: str):
    if name == "DATA_DIR":
        return ruta_data()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Directorio empaquetado de prompts del core
PROMPTS_DIR = (PACKAGE_ROOT / "core" / "prompts").resolve()


def ruta_cronogramas() -> Path:
    """Retorna la ruta al directorio de cronogramas académicos (schedules)."""
    return ruta_data() / "schedules"


def ruta_materias() -> Path:
    """Retorna la ruta al archivo de texto con las materias registradas."""
    return ruta_data() / "config" / "materias.txt"


def ruta_registro_materiales() -> Path:
    """Retorna la ruta al archivo JSON de auditoría y tracking de materiales."""
    return ruta_data() / "config" / "registro_materiales.json"


def ruta_ajustes() -> Path:
    """Retorna la ruta al archivo de configuración persistida (ajustes.json)."""
    return ruta_data() / "config" / "ajustes.json"


def ruta_plugins_memoria() -> Path:
    """Retorna la ruta a la carpeta de memorias persistentes de plugins."""
    return ruta_data() / "plugins"


def ruta_vectordb() -> Path:
    """Retorna la ruta a la base de datos vectorial de embeddings."""
    return ruta_data() / "vectordb"


def ruta_prompts() -> Path:
    """Retorna la ruta al directorio de plantillas de prompts del core."""
    return PROMPTS_DIR


def ruta_prompt(nombre_archivo: str) -> Path:
    """Retorna la ruta completa a un archivo de prompt específico."""
    return PROMPTS_DIR / nombre_archivo


def ruta_boveda_defecto() -> Path:
    """Retorna la ruta por defecto a la bóveda de Obsidian."""
    return REPO_ROOT / "obsidian_vault"


def ensure_data_dirs() -> None:
    """Garantiza la existencia física de las carpetas mínimas requeridas en data."""
    for path in (
        ruta_cronogramas(),
        ruta_data() / "config",
        ruta_plugins_memoria(),
    ):
        path.mkdir(parents=True, exist_ok=True)
