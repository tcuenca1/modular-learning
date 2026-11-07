"""Guía de estudio offline: clases para leer sin conexión y su confirmación al volver."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# Cuánto se extiende cada clase según cuántas entran en la guía y el tiempo disponible
EXTENSIONES = {
    "completa": "Explicación completa y detallada, con ejemplos desarrollados.",
    "estandar": "Explicación clara de lo esencial, con un ejemplo por concepto importante.",
    "sintesis": "Síntesis breve: ideas clave, definiciones y lo imprescindible para un examen.",
}

# Resultado de cada clase cuando el estudiante confirma su revisión
ENTENDIDA = "entendida"
CON_DUDAS = "con_dudas"
PENDIENTE = "pendiente"
RESULTADOS = (ENTENDIDA, CON_DUDAS, PENDIENTE)

MAXIMO_CLASES = 16

# El prompt separa la explicación de las respuestas de la autoevaluación con este marcador,
# para poder llevar todas las respuestas al final del documento
MARCADOR_RESPUESTAS = "<!-- RESPUESTAS -->"


def elegir_extension(n_clases: int, tiempo_minutos: int | None = None) -> str:
    """
    Determina la extensión de las explicaciones:
    - Si se indica tiempo disponible (en minutos), reparte el presupuesto:
      >= 45 min/clase -> 'completa'
      >= 20 min/clase -> 'estandar'
      < 20 min/clase  -> 'sintesis'
    - Si no se indica tiempo, se guía por la cantidad de clases:
      <= 2 clases -> 'completa'
      <= 5 clases -> 'estandar'
      > 5 clases  -> 'sintesis'
    """
    if n_clases <= 0:
        return "estandar"
    if tiempo_minutos is not None and tiempo_minutos > 0:
        minutos_por_clase = tiempo_minutos / n_clases
        if minutos_por_clase >= 45:
            return "completa"
        if minutos_por_clase >= 20:
            return "estandar"
        return "sintesis"
    if n_clases <= 2:
        return "completa"
    if n_clases <= 5:
        return "estandar"
    return "sintesis"


def separar_respuestas(texto: str) -> tuple[str, str]:
    """Divide la salida del LLM en (explicación, respuestas de la autoevaluación)."""
    if MARCADOR_RESPUESTAS not in texto:
        return texto.strip(), ""
    explicacion, respuestas = texto.split(MARCADOR_RESPUESTAS, 1)
    return explicacion.strip(), respuestas.strip()


@dataclass
class ClaseGuia:
    """Una clase dentro de la guía: su contenido generado y lo que el estudiante dijo al volver."""

    tema: str
    fecha: str = ""
    contenido: str = ""
    respuestas: str = ""
    resultado: str | None = None
    dudas: str = ""
    clase_id: str = ""
    estado_previo: str | None = None

    @property
    def generada(self) -> bool:
        return bool(self.contenido)


@dataclass
class GuiaOffline:
    """Guía de una o varias clases de una asignatura, pendiente de confirmar hasta que se revise."""

    id: str
    materia: str
    extension: str
    creada: str
    clases: list[ClaseGuia] = field(default_factory=list)
    revisada: str | None = None
    tiempo_minutos: int | None = None

    @property
    def completa(self) -> bool:
        return all(c.generada for c in self.clases)

    @property
    def pendiente_de_confirmar(self) -> bool:
        return self.revisada is None and self.completa

    def a_dict(self) -> dict[str, Any]:
        datos = asdict(self)
        datos["completa"] = self.completa
        datos["pendiente_de_confirmar"] = self.pendiente_de_confirmar
        return datos

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> GuiaOffline:
        campos_clase = ClaseGuia.__dataclass_fields__
        clases = [
            ClaseGuia(**{k: v for k, v in c.items() if k in campos_clase})
            for c in datos.get("clases", [])
        ]
        campos = {k: v for k, v in datos.items() if k in cls.__dataclass_fields__ and k != "clases"}
        return cls(**campos, clases=clases)


__all__ = [
    "CON_DUDAS",
    "ENTENDIDA",
    "EXTENSIONES",
    "MARCADOR_RESPUESTAS",
    "MAXIMO_CLASES",
    "PENDIENTE",
    "RESULTADOS",
    "ClaseGuia",
    "GuiaOffline",
    "elegir_extension",
    "separar_respuestas",
]
