"""Implementación en JSON del repositorio de guías de estudio offline."""

from __future__ import annotations

from typing import Any

from modular_learning.core.domain.guia_offline import GuiaOffline
from modular_learning.core.ports.guias import GuiasRepo
from modular_learning.infrastructure.persistence.almacen import AlmacenDocumentos, DocumentoJson


class JsonGuiasRepo(GuiasRepo):
    """Guías en guias/guias.json como {id: guía}."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("guias/guias.json", ruta_archivo, almacen)

    def _cargar(self) -> dict[str, dict[str, Any]]:
        datos = self._documento.leer({})
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
        self._documento.escribir(datos)

    def eliminar(self, ids: list[str]) -> int:
        datos = self._cargar()
        quitadas = [i for i in ids if datos.pop(i, None) is not None]
        if quitadas:
            self._documento.escribir(datos)
        return len(quitadas)


__all__ = ["JsonGuiasRepo"]
