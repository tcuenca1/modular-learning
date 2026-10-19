"""
Servicio de configuración del usuario (sin login).

Persiste en `data/config/ajustes.json` las rutas elegidas por el usuario:
- carpeta_material: carpeta raíz con sus actividades y material de estudio (una subcarpeta por asignatura).
- ruta_obsidian: bóveda de Obsidian, usada tanto para guardar lo ingestado como para las guías de estudio.

Si no hay ajustes guardados se usan las variables de entorno (compatibilidad con el CLI) o valores por defecto.
"""

import json
import os

ARCHIVO_AJUSTES = os.path.join("data", "config", "ajustes.json")
DEFAULT_CARPETA_MATERIAL = "C:/Universidad"
DEFAULT_OBSIDIAN = "obsidian_vault"


def _leer() -> dict:
    try:
        with open(ARCHIVO_AJUSTES, encoding="utf-8") as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def esta_configurado() -> bool:
    datos = _leer()
    return bool(datos.get("carpeta_material") and datos.get("ruta_obsidian"))


def carpeta_material() -> str:
    return (
        _leer().get("carpeta_material")
        or os.getenv("RUTA_BASE_UNIVERSIDAD")
        or DEFAULT_CARPETA_MATERIAL
    )


def ruta_boveda() -> str:
    return _leer().get("ruta_obsidian") or os.getenv("RUTA_OBSIDIAN") or DEFAULT_OBSIDIAN


def obtener_ajustes() -> dict:
    return {
        "configurado": esta_configurado(),
        "carpeta_material": carpeta_material(),
        "ruta_obsidian": ruta_boveda(),
        "carpeta_material_existe": os.path.isdir(carpeta_material()),
        "ruta_obsidian_existe": os.path.isdir(ruta_boveda()),
    }


def guardar_ajustes(carpeta_material_nueva: str, ruta_obsidian_nueva: str) -> dict:
    """Valida y guarda las rutas. La carpeta de material debe existir; la bóveda se crea si falta."""
    material = os.path.normpath(carpeta_material_nueva.strip().strip('"'))
    boveda = os.path.normpath(ruta_obsidian_nueva.strip().strip('"'))
    if not carpeta_material_nueva.strip() or not ruta_obsidian_nueva.strip():
        raise ValueError("Debes indicar ambas rutas.")
    if not os.path.isdir(material):
        raise ValueError(f"La carpeta de material no existe: {material}")
    try:
        os.makedirs(boveda, exist_ok=True)
    except OSError as e:
        raise ValueError(f"No se pudo crear la bóveda de Obsidian en {boveda}: {e}") from e

    os.makedirs(os.path.dirname(ARCHIVO_AJUSTES), exist_ok=True)
    with open(ARCHIVO_AJUSTES, "w", encoding="utf-8") as f:
        json.dump({"carpeta_material": material, "ruta_obsidian": boveda}, f, indent=4, ensure_ascii=False)
    return obtener_ajustes()
