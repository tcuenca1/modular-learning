"""Repaso espaciado: tarjetas de preguntas y programación SM-2 de su próxima revisión."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from typing import Any

FACILIDAD_INICIAL = 2.5
FACILIDAD_MINIMA = 1.3
# Calidad de respuesta en la escala 0-5 de SM-2 para un quiz de opción múltiple
CALIDAD_ACIERTO = 4
CALIDAD_FALLO = 1
# A partir de este intervalo una tarjeta se considera dominada
INTERVALO_DOMINADA = 21


def id_tarjeta(materia: str, enunciado: str) -> str:
    """Identificador estable de una pregunta, independiente de mayúsculas, tildes y espacios."""
    base = unicodedata.normalize("NFD", f"{materia}|{enunciado}").encode("ascii", "ignore").decode()
    base = re.sub(r"\s+", " ", base.lower()).strip()
    return hashlib.sha1(base.encode()).hexdigest()[:16]


@dataclass
class Intento:
    fecha: str
    correcto: bool
    elegida: str = ""


@dataclass
class Tarjeta:
    """Una pregunta de repaso ligada a la clase (materia + tema) de la que salió."""

    id: str
    materia: str
    tema: str
    enunciado: str
    opciones: list[str]
    respuesta_correcta: str
    explicacion: str = ""
    creada: str = ""
    repeticiones: int = 0
    intervalo: int = 0
    facilidad: float = FACILIDAD_INICIAL
    proxima: str = ""
    intentos: list[Intento] = field(default_factory=list)

    @property
    def ultimo_fallo(self) -> bool:
        return bool(self.intentos) and not self.intentos[-1].correcto

    @property
    def dominada(self) -> bool:
        return self.intervalo >= INTERVALO_DOMINADA

    def vence(self, hoy: date) -> bool:
        return not self.proxima or date.fromisoformat(self.proxima) <= hoy

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> Tarjeta:
        campos = {k: v for k, v in datos.items() if k in cls.__dataclass_fields__}
        campos["intentos"] = [Intento(**i) for i in datos.get("intentos", [])]
        return cls(**campos)


def programar(tarjeta: Tarjeta, correcto: bool, hoy: date, elegida: str = "") -> Tarjeta:
    """
    Aplica SM-2: un acierto alarga el intervalo (1 → 6 → intervalo × facilidad días);
    un fallo reinicia la tarjeta para volver a verla mañana. Modifica y retorna la tarjeta.
    """
    calidad = CALIDAD_ACIERTO if correcto else CALIDAD_FALLO

    if correcto:
        if tarjeta.repeticiones == 0:
            tarjeta.intervalo = 1
        elif tarjeta.repeticiones == 1:
            tarjeta.intervalo = 6
        else:
            tarjeta.intervalo = round(tarjeta.intervalo * tarjeta.facilidad)
        tarjeta.repeticiones += 1
    else:
        tarjeta.repeticiones = 0
        tarjeta.intervalo = 1

    tarjeta.facilidad = max(
        FACILIDAD_MINIMA,
        tarjeta.facilidad + 0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02),
    )
    tarjeta.proxima = (hoy + timedelta(days=tarjeta.intervalo)).isoformat()
    tarjeta.intentos.append(Intento(fecha=hoy.isoformat(), correcto=correcto, elegida=elegida))
    return tarjeta


__all__ = [
    "INTERVALO_DOMINADA",
    "Intento",
    "Tarjeta",
    "id_tarjeta",
    "programar",
]
