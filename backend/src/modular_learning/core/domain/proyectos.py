"""Dominio para la gestión, clasificación y trazabilidad de proyectos académicos."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

from modular_learning.core.domain.materias import slug_materia

TipoProyecto = Literal["software", "iot", "documental_auditoria", "documento_rector"]
ParcialProyecto = Literal["general", "primer_parcial", "segundo_parcial"]


# Tolerancia al comparar fechas de modificación: algunos sistemas de archivos redondean
TOLERANCIA_MTIME_SEGUNDOS = 2.0


def slug_proyecto(materia: str, nombre: str, parcial: str = "general") -> str:
    """Genera un slug único para un proyecto combinando materia, parcial y nombre."""
    return f"{slug_materia(materia)}--{slug_materia(parcial)}--{slug_materia(nombre)}"


def etiqueta_parcial(parcial: str) -> str:
    return {"primer_parcial": "Primer Parcial", "segundo_parcial": "Segundo Parcial"}.get(
        parcial, "General"
    )


@dataclass(frozen=True)
class HuellaProyecto:
    """Estado del proyecto en disco: sirve para saber si cambió desde su último análisis."""

    mtime: float
    total_archivos: int
    hash_estado: str


@dataclass(frozen=True)
class Proyecto:
    """Entidad que representa un proyecto integral de una asignatura."""

    id: str
    nombre: str
    materia: str
    parcial: ParcialProyecto
    tipo: TipoProyecto
    ruta_origen: str
    ruta_nota_obsidian: str
    fecha_analisis: str
    mtime_archivos: float
    total_archivos: int
    hash_estado: str

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> Proyecto:
        return cls(
            id=str(datos.get("id") or ""),
            nombre=str(datos.get("nombre") or ""),
            materia=str(datos.get("materia") or ""),
            parcial=datos.get("parcial", "general"),
            tipo=datos.get("tipo", "documento_rector"),
            ruta_origen=str(datos.get("ruta_origen") or ""),
            ruta_nota_obsidian=str(datos.get("ruta_nota_obsidian") or ""),
            fecha_analisis=str(datos.get("fecha_analisis") or ""),
            mtime_archivos=float(datos.get("mtime_archivos") or 0.0),
            total_archivos=int(datos.get("total_archivos") or 0),
            hash_estado=str(datos.get("hash_estado") or ""),
        )


__all__ = [
    "TOLERANCIA_MTIME_SEGUNDOS",
    "HuellaProyecto",
    "ParcialProyecto",
    "Proyecto",
    "TipoProyecto",
    "etiqueta_parcial",
    "slug_proyecto",
]
