"""Implementaciones en JSON de los repositorios de repaso espaciado e historial."""

from __future__ import annotations

import unicodedata
from typing import Any

from modular_learning.core.domain.repaso_espaciado import Tarjeta
from modular_learning.core.ports.repaso import HistorialRepo, TarjetasRepo
from modular_learning.infrastructure.persistence.almacen import AlmacenDocumentos, DocumentoJson


def _normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    return " ".join(sin_tildes.lower().split())


class JsonTarjetasRepo(TarjetasRepo):
    """Tarjetas en repaso/tarjetas.json como {id: tarjeta}."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("repaso/tarjetas.json", ruta_archivo, almacen)

    def _cargar(self) -> dict[str, dict[str, Any]]:
        datos = self._documento.leer({})
        return datos if isinstance(datos, dict) else {}

    def listar(self) -> list[Tarjeta]:
        return [Tarjeta.desde_dict(d) for d in self._cargar().values()]

    def obtener(self, tarjeta_id: str) -> Tarjeta | None:
        datos = self._cargar().get(tarjeta_id)
        return Tarjeta.desde_dict(datos) if datos else None

    def guardar(self, tarjeta: Tarjeta) -> None:
        datos = self._cargar()
        datos[tarjeta.id] = tarjeta.a_dict()
        self._documento.escribir(datos)


class JsonHistorialRepo(HistorialRepo):
    """Eventos de estudio en repaso/historial.json como lista cronológica."""

    def __init__(self, ruta_archivo: str | None = None, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("repaso/historial.json", ruta_archivo, almacen)

    def _cargar(self) -> list[dict[str, Any]]:
        datos = self._documento.leer([])
        return datos if isinstance(datos, list) else []

    def registrar(self, evento: dict[str, Any]) -> None:
        eventos = self._cargar()
        eventos.append(evento)
        self._documento.escribir(eventos)

    def listar(self, materia: str | None = None, tema: str | None = None) -> list[dict[str, Any]]:
        materia_n = _normalizar(materia) if materia else None
        tema_n = _normalizar(tema) if tema else None
        resultado = []
        for evento in reversed(self._cargar()):
            if materia_n and _normalizar(str(evento.get("materia", ""))) != materia_n:
                continue
            if tema_n:
                tema_evento = _normalizar(str(evento.get("tema", "")))
                if not tema_evento or (tema_n not in tema_evento and tema_evento not in tema_n):
                    continue
            resultado.append(evento)
        return resultado


__all__ = ["JsonHistorialRepo", "JsonTarjetasRepo"]
