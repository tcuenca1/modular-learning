"""Router para el procesamiento y extracción de cronogramas a partir de sílabos."""

from __future__ import annotations

import os
import shutil
import tempfile
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from modular_learning.apps.api.dependencies import (
    get_materias_service,
    get_silabo_service,
)
from modular_learning.apps.api.schemas import GuardarCronograma
from modular_learning.core.application.materias import MateriasService
from modular_learning.core.application.silabo import EXTENSIONES_SILABO, SilaboService

router = APIRouter(prefix="/api/silabo", tags=["silabo"])


@router.post("/extraer")
def extraer_silabo(
    archivo: Annotated[UploadFile, File()],
    servicio: Annotated[SilaboService, Depends(get_silabo_service)],
    materia: Annotated[str, Form()] = "",
) -> dict[str, Any]:
    nombre = archivo.filename or "silabo.txt"
    ext = os.path.splitext(nombre)[1].lower()
    if ext not in EXTENSIONES_SILABO:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado ({ext}). Formatos válidos: {', '.join(EXTENSIONES_SILABO)}.",
        )

    materia_final = materia.strip() or servicio.sugerir_nombre_materia(nombre)

    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, os.path.basename(nombre))
        with open(ruta, "wb") as f:
            shutil.copyfileobj(archivo.file, f)
        try:
            datos = servicio.extraer_cronograma(ruta, materia_final)
        except (ValueError, FileNotFoundError) as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    return {"materia": materia_final, "datos": datos}


@router.post("/guardar")
def guardar_silabo(
    body: GuardarCronograma,
    servicio: Annotated[SilaboService, Depends(get_silabo_service)],
    materias_srv: Annotated[MateriasService, Depends(get_materias_service)],
) -> dict[str, Any]:
    try:
        ruta = servicio.guardar_cronograma(body.materia.strip(), body.datos)
    except (ValueError, FileNotFoundError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    # Clave del cronograma en el almacén de datos (archivo local o documento en Postgres)
    return {"ruta": ruta, "materias": materias_srv.listar_materias()}
