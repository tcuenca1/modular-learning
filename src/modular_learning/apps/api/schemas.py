"""DTOs Pydantic para el API web de Modular Learning."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NuevaMateria(BaseModel):
    nombre: str = Field(min_length=1)


class IniciarTutoria(BaseModel):
    materia: str = Field(min_length=1)
    tema: str = Field(min_length=1)
    nivel_profundidad: str = "INTERMEDIO"


class Duda(BaseModel):
    paso: int
    duda: str = Field(min_length=1)


class RespuestaQuiz(BaseModel):
    quiz_id: str
    respuestas: list[str]


class GuardarCronograma(BaseModel):
    materia: str = Field(min_length=1)
    datos: dict[str, Any] | list[Any]


class ActualizarPlugin(BaseModel):
    seleccion: str


class GuardarConfig(BaseModel):
    carpeta_material: str = Field(min_length=1)
    ruta_obsidian: str = Field(min_length=1)


class SincronizarMaterial(BaseModel):
    materia: str = Field(min_length=1)
