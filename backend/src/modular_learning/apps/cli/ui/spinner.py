"""Utilidades de spinner para feedback visual en CLI."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from halo import Halo


@contextmanager
def spinner(texto: str = "Procesando...", spinner_style: str = "line") -> Iterator[Halo]:
    """Context manager para mostrar un spinner de consola durante operaciones prolongadas."""
    sp = Halo(text=texto, spinner=spinner_style)
    sp.start()
    try:
        yield sp
    except Exception:
        sp.fail(f"Fallo durante: {texto}")
        raise
    else:
        if sp.text == texto:
            sp.succeed()
        else:
            sp.stop()


__all__ = ["spinner"]
