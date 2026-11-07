"""Router para la gestión de asignaturas y cronogramas de clases."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException

from modular_learning.apps.api.dependencies import get_materias_service
from modular_learning.apps.api.schemas import (
    EditarClase,
    GuardarParciales,
    NuevaClase,
    NuevaMateria,
    RenombrarMateria,
)
from modular_learning.core.application.materias import MateriasService

router = APIRouter(prefix="/api/materias", tags=["materias"])


@router.get("")
def listar_materias(
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    return {
        "materias": servicio.listar_materias(),
        "catalogo": servicio.listar_catalogo(),
    }


@router.post("", status_code=201)
def crear_materia(
    body: NuevaMateria,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    materias = servicio.agregar_materia(body.nombre)
    return {"materias": materias, "catalogo": servicio.listar_catalogo()}


@router.put("/{slug}")
def renombrar_materia(
    slug: str,
    body: RenombrarMateria,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    try:
        materia = servicio.renombrar_materia(slug, body.nombre)
        return {"materia": materia.a_dict(), "catalogo": servicio.listar_catalogo()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{slug}")
def eliminar_materia(
    slug: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    eliminada = servicio.eliminar_materia(slug, borrar_cronograma=True)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Asignatura no encontrada.")
    return {"ok": True, "catalogo": servicio.listar_catalogo()}


@router.get("/cronogramas")
def cronogramas(
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    return {"cronogramas": servicio.listar_cronogramas()}


@router.get("/{materia}/cronograma")
def obtener_cronograma(
    materia: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    clases = servicio.obtener_cronograma(materia)
    return {"clases": clases or []}


@router.delete("/{materia}/cronograma")
def eliminar_cronograma(
    materia: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    ok = servicio.eliminar_cronograma(materia, borrar_materia=True)
    if not ok:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado.")
    return {"ok": True, "catalogo": servicio.listar_catalogo()}


@router.get("/{materia}/clases")
def proximas_clases(
    materia: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, list[dict[str, Any]]]:
    return {"clases": servicio.obtener_proximas_clases(materia)}


@router.post("/{materia}/clases", status_code=201)
def agregar_clase(
    materia: str,
    body: NuevaClase,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    try:
        nueva = servicio.agregar_clase(materia, body.model_dump())
        return {"clase": nueva}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("/{materia}/clases/{clase_id}")
def editar_clase(
    materia: str,
    clase_id: str,
    body: EditarClase,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    try:
        clase = servicio.editar_clase(materia, clase_id, body.campos)
        return {"clase": clase}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/{materia}/clases/{clase_id}")
def eliminar_clase(
    materia: str,
    clase_id: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    ok = servicio.eliminar_clase(materia, clase_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    return {"ok": True}


@router.patch("/{materia}/clases/{clase_id}/estado")
def cambiar_estado_clase(
    materia: str,
    clase_id: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
    estado: str = "completado",
) -> dict[str, Any]:
    ok = servicio.cambiar_estado_clase(materia, clase_id, estado)
    if not ok:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    return {"ok": True, "estado": estado}


@router.get("/{materia}/parciales")
def obtener_parciales(
    materia: str,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, list[dict[str, Any]]]:
    return {"parciales": servicio.obtener_parciales(materia)}


@router.post("/{materia}/parciales")
def guardar_parciales(
    materia: str,
    body: GuardarParciales,
    servicio: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    try:
        parciales = servicio.guardar_parciales(materia, body.parciales)
        return {"parciales": parciales}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


__all__ = ["router"]
