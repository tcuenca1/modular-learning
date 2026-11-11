"""Router de guías de estudio offline: creación, generación por clase y confirmación al volver."""

from __future__ import annotations

from dataclasses import asdict
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response

from modular_learning.apps.api.dependencies import get_guias_service
from modular_learning.apps.api.errores import error_cliente, error_interno
from modular_learning.apps.api.schemas import NuevaGuia, RevisionGuia
from modular_learning.core.application.guias import GuiaOfflineService
from modular_learning.core.domain.guia_offline import GuiaOffline

router = APIRouter(prefix="/api/guias", tags=["guias"])

Servicio = Annotated[GuiaOfflineService, Depends(get_guias_service)]


def _resumen(guia: GuiaOffline) -> dict[str, Any]:
    """Datos de una guía sin el contenido de las clases, para listados."""
    return {
        "id": guia.id,
        "materia": guia.materia,
        "extension": guia.extension,
        "creada": guia.creada,
        "revisada": guia.revisada,
        "completa": guia.completa,
        "pendiente_de_confirmar": guia.pendiente_de_confirmar,
        "tiempo_minutos": guia.tiempo_minutos,
        "temas": [c.tema for c in guia.clases],
    }


def _obtener(servicio: GuiaOfflineService, guia_id: str) -> GuiaOffline:
    try:
        return servicio.obtener(guia_id)
    except LookupError as e:
        raise error_cliente(e, 404) from e


@router.get("")
def listar_guias(servicio: Servicio) -> dict[str, list[dict[str, Any]]]:
    return {"guias": [_resumen(g) for g in servicio.listar()]}


@router.get("/pendientes")
def guias_pendientes(servicio: Servicio) -> dict[str, list[dict[str, Any]]]:
    """Guías generadas que el estudiante aún no ha confirmado si revisó."""
    return {"guias": [_resumen(g) for g in servicio.pendientes_de_confirmar()]}


@router.post("", status_code=201)
def crear_guia(body: NuevaGuia, servicio: Servicio) -> dict[str, Any]:
    try:
        guia = servicio.crear(body.materia.strip(), body.temas, tiempo_minutos=body.tiempo_minutos)
    except ValueError as e:
        raise error_cliente(e) from e
    return guia.a_dict()


@router.get("/{guia_id}")
def obtener_guia(guia_id: str, servicio: Servicio) -> dict[str, Any]:
    return _obtener(servicio, guia_id).a_dict()


@router.delete("/{guia_id}")
def eliminar_guia(guia_id: str, servicio: Servicio) -> dict[str, Any]:
    ok = servicio.eliminar_guia(guia_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Guía no encontrada.")
    return {"ok": True}


@router.get("/{guia_id}/pdf")
def descargar_pdf(guia_id: str, servicio: Servicio) -> Response:
    """Descarga directamente la guía formateada y estructurada como archivo PDF."""
    try:
        pdf_bytes, filename = servicio.exportar_pdf(guia_id)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except LookupError as e:
        raise error_cliente(e, 404) from e
    except Exception as e:
        raise error_interno(e) from e


@router.post("/{guia_id}/clases/{indice}")
def generar_clase(guia_id: str, indice: int, servicio: Servicio) -> dict[str, Any]:
    """Genera con el LLM una clase de la guía; el cliente las pide una a una para mostrar avance."""
    _obtener(servicio, guia_id)
    try:
        clase = servicio.generar_clase(guia_id, indice)
    except ValueError as e:
        raise error_cliente(e) from e
    except Exception as e:
        raise error_interno(e) from e
    return asdict(clase)


@router.post("/{guia_id}/revision")
def registrar_revision(guia_id: str, body: RevisionGuia, servicio: Servicio) -> dict[str, Any]:
    _obtener(servicio, guia_id)
    resultados = {r.indice: (r.resultado, r.dudas) for r in body.resultados}
    try:
        return servicio.registrar_revision(guia_id, resultados)
    except ValueError as e:
        raise error_cliente(e) from e


@router.post("/{guia_id}/deshacer")
def deshacer_revision(guia_id: str, servicio: Servicio) -> dict[str, Any]:
    _obtener(servicio, guia_id)
    try:
        return servicio.deshacer_revision(guia_id)
    except ValueError as e:
        raise error_cliente(e) from e


__all__ = ["router"]
