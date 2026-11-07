"""Identidad de una asignatura: un identificador estable (slug) y un nombre para mostrar."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass
from typing import Any


def slug_materia(texto: str) -> str:
    """
    Identificador de una asignatura a partir de cualquier forma de escribirla.

    "Ingeniería de Software II", "INGENIERIA_DE_SOFTWARE_II" e "ingenieria-de-software-ii"
    dan todos "ingenieria-de-software-ii". Es idempotente: el slug de un slug es el mismo.
    """
    sin_tildes = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sin_tildes.lower()).strip("-")


@dataclass(frozen=True)
class Materia:
    """Asignatura del catálogo. El slug no cambia aunque se corrija el nombre."""

    slug: str
    nombre: str

    @classmethod
    def desde_nombre(cls, nombre: str) -> Materia:
        nombre = " ".join(nombre.split())
        return cls(slug=slug_materia(nombre), nombre=nombre)

    def a_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> Materia | None:
        nombre = " ".join(str(datos.get("nombre") or "").split())
        slug = str(datos.get("slug") or "").strip() or slug_materia(nombre)
        return cls(slug=slug, nombre=nombre or slug) if slug else None


def resolver_materia(materias: list[Materia], texto: str) -> Materia | None:
    """Busca en el catálogo por slug o por nombre, sin importar mayúsculas, tildes ni separadores."""
    buscado = slug_materia(texto)
    if not buscado:
        return None
    for m in materias:
        if m.slug == buscado:
            return m
    for m in materias:
        if slug_materia(m.nombre) == buscado:
            return m
    return None


__all__ = ["Materia", "resolver_materia", "slug_materia"]
