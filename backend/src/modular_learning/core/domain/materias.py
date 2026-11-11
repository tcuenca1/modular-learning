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


LONGITUD_MAXIMA_NOMBRE = 80
_SIGNOS_PERMITIDOS = frozenset(" -_.,()'&+:#ºª°")


class NombreMateriaInvalido(ValueError):
    """El nombre de la asignatura no cumple las reglas (vacío, largo o con caracteres no válidos)."""


class MateriaDuplicada(ValueError):
    """Ya existe otra asignatura con el mismo nombre (sin contar tildes ni mayúsculas)."""


class MateriaNoEncontrada(LookupError):
    """La asignatura no está en el catálogo."""


def validar_nombre_materia(nombre: str) -> str:
    """
    Normaliza espacios y valida el nombre de una asignatura; retorna el nombre limpio.

    Admite letras, dígitos y unos pocos signos; rechaza vacío, solo símbolos, caracteres de
    control (incluido NUL), `/`, `\\` y `..`, y más de LONGITUD_MAXIMA_NOMBRE caracteres.
    """
    limpio = " ".join(str(nombre).split())
    if not limpio:
        raise NombreMateriaInvalido("El nombre de la asignatura no puede estar vacío.")
    if len(limpio) > LONGITUD_MAXIMA_NOMBRE:
        raise NombreMateriaInvalido(
            f"El nombre de la asignatura no puede superar {LONGITUD_MAXIMA_NOMBRE} caracteres."
        )
    if ".." in limpio or any(not (c.isalnum() or c in _SIGNOS_PERMITIDOS) for c in limpio):
        raise NombreMateriaInvalido(
            "El nombre de la asignatura solo admite letras, números, espacios y los signos "
            "- _ . , ( ) ' & + : # (sin barras ni «..»)."
        )
    if not slug_materia(limpio):
        raise NombreMateriaInvalido("El nombre de la asignatura debe contener letras o números.")
    return limpio


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


__all__ = [
    "LONGITUD_MAXIMA_NOMBRE",
    "Materia",
    "MateriaDuplicada",
    "MateriaNoEncontrada",
    "NombreMateriaInvalido",
    "resolver_materia",
    "slug_materia",
    "validar_nombre_materia",
]
