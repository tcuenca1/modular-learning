"""Implementación en JSON del repositorio de guías de estudio offline."""

from __future__ import annotations

from typing import Any

from modular_learning import settings
from modular_learning.core.domain.guia_offline import GuiaOffline
from modular_learning.core.ports.guias import GuiasRepo
from modular_learning.infrastructure.persistence.json_repaso import _escribir_json, _leer_json


class JsonGuiasRepo(GuiasRepo):
    """Guías en data/guias/guias.json como {id: guía}."""

    def __init__(self, ruta_archivo: str | None = None):
        self._ruta_archivo = ruta_archivo

    @property
    def ruta_archivo(self) -> str:
        return self._ruta_archivo or str(settings.ruta_guias() / "guias.json")

    def _cargar(self) -> dict[str, dict[str, Any]]:
        datos = _leer_json(self.ruta_archivo, {})
        return datos if isinstance(datos, dict) else {}

    def listar(self) -> list[GuiaOffline]:
        guias = [GuiaOffline.desde_dict(d) for d in self._cargar().values()]
        return sorted(guias, key=lambda g: g.creada, reverse=True)

    def obtener(self, guia_id: str) -> GuiaOffline | None:
        datos = self._cargar().get(guia_id)
        return GuiaOffline.desde_dict(datos) if datos else None

    def guardar(self, guia: GuiaOffline) -> None:
        datos = self._cargar()
        datos[guia.id] = guia.a_dict()
        _escribir_json(self.ruta_archivo, datos)


__all__ = ["JsonGuiasRepo"]
