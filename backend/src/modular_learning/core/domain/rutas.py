"""Comprobaciones de rutas puramente léxicas (sin tocar el disco) para recibir rutas del cliente."""

from __future__ import annotations

import os


def esta_dentro(base: str, ruta: str, *, incluir_base: bool = True) -> bool:
    """
    Indica si `ruta` queda dentro de `base` tras normalizarla (resuelve `..` y `.`).

    No resuelve enlaces simbólicos porque no accede al disco. Con `incluir_base=False` la
    propia carpeta base no cuenta como "dentro".
    """
    if not base or not ruta or "\x00" in base or "\x00" in ruta:
        return False
    b = os.path.normcase(os.path.normpath(base))
    r = os.path.normcase(os.path.normpath(ruta))
    try:
        dentro = os.path.commonpath([b, r]) == b
    except ValueError:  # una absoluta y otra relativa, o unidades distintas
        return False
    return dentro and (incluir_base or r != b)


def unir_dentro(base: str, *partes: str) -> str | None:
    """
    Une `base` con `partes` y retorna la ruta normalizada, o None si alguna parte es vacía o
    absoluta, o si el resultado se sale de `base` (o es la propia base).
    """
    if not base or any(not p or os.path.isabs(p) or "\x00" in p for p in partes):
        return None
    ruta = os.path.normpath(os.path.join(base, *partes))
    return ruta if esta_dentro(base, ruta, incluir_base=False) else None


__all__ = ["esta_dentro", "unir_dentro"]
