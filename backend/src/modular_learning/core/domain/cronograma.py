"""Reglas sobre las clases de un cronograma: identidad estable, estado y búsqueda."""

from __future__ import annotations

import uuid
from typing import Any

PENDIENTE = "pendiente"
COMPLETADO = "completado"
ESTADOS = (PENDIENTE, COMPLETADO)


def nuevo_id_clase() -> str:
    return uuid.uuid4().hex[:8]


def asignar_ids(clases: list[dict[str, Any]]) -> bool:
    """
    Da un `id` a cada clase que no lo tenga (o lo tenga repetido). Dos clases con el mismo
    tema en días distintos son clases distintas: se identifican por su id, no por el tema.
    Retorna True si cambió alguna.
    """
    vistos: set[str] = set()
    cambio = False
    for clase in clases:
        actual = str(clase.get("id") or "").strip()
        if not actual or actual in vistos:
            actual = nuevo_id_clase()
            while actual in vistos:
                actual = nuevo_id_clase()
            clase["id"] = actual
            cambio = True
        vistos.add(actual)
    return cambio


def es_completada(clase: dict[str, Any]) -> bool:
    return str(clase.get("estado", "")).strip().lower().startswith("complet")


def _normalizar(texto: Any) -> str:
    return " ".join(str(texto or "").lower().split())


def buscar_clase(
    clases: list[dict[str, Any]], clase_id: str | None = None, tema: str | None = None
) -> dict[str, Any] | None:
    """
    La clase con ese id. Sin id (CLI, temas escritos a mano) se busca por tema: primero la
    primera pendiente con ese tema exacto, luego cualquiera con ese tema y, por último, una
    cuyo tema contenga al buscado o viceversa.
    """
    if clase_id:
        return next((c for c in clases if str(c.get("id")) == clase_id), None)
    buscado = _normalizar(tema)
    if not buscado:
        return None
    exactas = [c for c in clases if _normalizar(c.get("tema")) == buscado]
    pendiente = next((c for c in exactas if not es_completada(c)), None)
    if pendiente or exactas:
        return pendiente or exactas[0]
    for c in clases:
        tema_clase = _normalizar(c.get("tema"))
        if tema_clase and (buscado in tema_clase or tema_clase in buscado):
            return c
    return None


__all__ = [
    "COMPLETADO",
    "ESTADOS",
    "PENDIENTE",
    "asignar_ids",
    "buscar_clase",
    "es_completada",
    "nuevo_id_clase",
]
