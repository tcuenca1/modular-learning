"""DTOs Pydantic para el API web de Modular Learning."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NuevaMateria(BaseModel):
    nombre: str = Field(min_length=1)


class RenombrarMateria(BaseModel):
    nombre: str = Field(min_length=1)


class IniciarTutoria(BaseModel):
    materia: str = Field(min_length=1)
    tema: str = Field(min_length=1)
    nivel_profundidad: str = "INTERMEDIO"
    enfoque: str | None = None
    clase_id: str | None = None


class Duda(BaseModel):
    paso: int
    duda: str = Field(min_length=1)


class NuevaGuia(BaseModel):
    materia: str = Field(min_length=1)
    temas: list[str] = Field(min_length=1)
    tiempo_minutos: int | None = None


class ResultadoClaseGuia(BaseModel):
    indice: int = Field(ge=0)
    resultado: str
    dudas: str = ""


class RevisionGuia(BaseModel):
    resultados: list[ResultadoClaseGuia]


class RespuestaQuiz(BaseModel):
    quiz_id: str
    respuestas: list[str]


class GuardarCronograma(BaseModel):
    materia: str = Field(min_length=1)
    datos: dict[str, Any] | list[Any]


class ActualizarPlugin(BaseModel):
    seleccion: str
    carpeta_override: str | None = None


class ConfigurarPlugin(BaseModel):
    clave: str = Field(min_length=1)
    carpeta: str | None = None
    materia: str | None = None


class GuardarConfig(BaseModel):
    carpeta_material: str = Field(min_length=1)
    ruta_obsidian: str = Field(min_length=1)


class SincronizarMaterial(BaseModel):
    materia: str = Field(min_length=1)


class EditarClase(BaseModel):
    campos: dict[str, Any]


class NuevaClase(BaseModel):
    tema: str = Field(min_length=1)
    fecha: str = ""
    objetivo: str = ""
    contenido: str = ""
    estado: str = "pendiente"


class GuardarParciales(BaseModel):
    parciales: list[dict[str, Any]]


class IngestarProyectoRequest(BaseModel):
    materia: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    parcial: str = "general"
    ruta: str = Field(min_length=1)
    tipo: str | None = None


class VaciarMaterialesRequest(BaseModel):
    borrar_notas_obsidian: bool = True
