"""Adaptador concreto para la persistencia de ajustes en JSON."""

from __future__ import annotations

import os
from typing import Any

from modular_learning.core.ports.config import AjustesPort
from modular_learning.infrastructure.persistence.almacen import AlmacenDocumentos, DocumentoJson

DEFAULT_CARPETA_MATERIAL = "C:/Universidad"
DEFAULT_OBSIDIAN = "obsidian_vault"


class JsonAjustesRepo(AjustesPort):
    """Implementación del puerto AjustesPort persistiendo en config/ajustes.json."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("config/ajustes.json", ruta_archivo, almacen)

    def _leer(self) -> dict[str, Any]:
        datos = self._documento.leer({})
        return datos if isinstance(datos, dict) else {}

    def esta_configurado(self) -> bool:
        datos = self._leer()
        return bool(datos.get("carpeta_material") and datos.get("ruta_obsidian"))

    def carpeta_material(self) -> str:
        return (
            self._leer().get("carpeta_material")
            or os.getenv("RUTA_BASE_UNIVERSIDAD")
            or DEFAULT_CARPETA_MATERIAL
        )

    def ruta_boveda(self) -> str:
        return self._leer().get("ruta_obsidian") or os.getenv("RUTA_OBSIDIAN") or DEFAULT_OBSIDIAN

    def obtener_ajustes(self) -> dict[str, Any]:
        return {
            "configurado": self.esta_configurado(),
            "carpeta_material": self.carpeta_material(),
            "ruta_obsidian": self.ruta_boveda(),
            "carpeta_material_existe": os.path.isdir(self.carpeta_material()),
            "ruta_obsidian_existe": os.path.isdir(self.ruta_boveda()),
        }

    def guardar_ajustes(
        self, carpeta_material_nueva: str, ruta_obsidian_nueva: str
    ) -> dict[str, Any]:
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

        self._documento.escribir({"carpeta_material": material, "ruta_obsidian": boveda}, sangria=4)
        return self.obtener_ajustes()


__all__ = ["DEFAULT_CARPETA_MATERIAL", "DEFAULT_OBSIDIAN", "JsonAjustesRepo"]
