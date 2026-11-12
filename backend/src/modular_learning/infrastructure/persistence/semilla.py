"""Carga los datos de ejemplo (data/examples) en una cuenta que aún no tiene datos."""

from __future__ import annotations

import logging
import os

from modular_learning.core.domain.materias import Materia
from modular_learning.infrastructure.persistence.almacen import AlmacenDocumentos

logger = logging.getLogger(__name__)
SUFIJO_CRONOGRAMA = "_cronograma.json"


def sembrar_cuenta(almacen: AlmacenDocumentos, carpeta_semilla: str) -> int:
    """
    Copia los .json y .txt de `carpeta_semilla` al almacén de la cuenta si está vacío y retorna
    cuántos documentos creó. Cada cronograma de ejemplo se da de alta también en el catálogo de
    asignaturas (si no, no aparecería en Hoy ni en Asignaturas).
    """
    if not os.path.isdir(carpeta_semilla) or almacen.listar(""):
        return 0
    creados = 0
    for raiz, _, archivos in os.walk(carpeta_semilla):
        for nombre in sorted(archivos):
            if not nombre.endswith((".json", ".txt")):
                continue
            ruta = os.path.join(raiz, nombre)
            clave = os.path.relpath(ruta, carpeta_semilla).replace(os.sep, "/")
            with open(ruta, encoding="utf-8") as f:
                almacen.escribir(clave, f.read())
            creados += 1

    from modular_learning.infrastructure.persistence.json_repositorios import JsonMateriaRepo

    materias = JsonMateriaRepo(almacen=almacen)
    for clave in almacen.listar("schedules/"):
        base = clave.rsplit("/", 1)[-1].removesuffix(SUFIJO_CRONOGRAMA).removesuffix(".json")
        materias.guardar(Materia.desde_nombre(base.replace("_", " ").title()))
    logger.info("Datos de ejemplo cargados: %s documentos", creados)
    return creados


__all__ = ["sembrar_cuenta"]
