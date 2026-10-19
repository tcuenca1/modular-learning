"""
Adaptador de entrada web (Driving Adapter) basado en FastAPI.

No contiene lógica de negocio: traduce peticiones HTTP a llamadas a los servicios
del núcleo (modular_learning.core.application) y devuelve DTOs JSON.
"""

import json
import os
import shutil
import tempfile
import uuid
from collections.abc import Iterator
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from modular_learning.core.application import (
    configuracion as servicio_config,
    evaluacion as motor_evaluacion,
    ingesta as servicio_ingesta,
    plugins as gestor_plugins,
    silabo as servicio_silabo,
    telemetria,
    tutoria as servicio_tutoria,
)
from modular_learning.core.application.tutoria import SesionTutoria
from modular_learning.infrastructure.persistence import json_repositorios as gestor_archivos

load_dotenv()

RUTA_ESTATICOS = Path(__file__).parent / "static"
OPCIONES_PLUGIN = ["Cisco (Actividades)", "Web (Proyectos)", "Node-RED (Flujos JSON)", "Todos"]

app = FastAPI(title="Modular Learning Web", version="1.0.0")

# Almacén en memoria de sesiones de tutoría activas (adaptador de estado de la capa web).
SESIONES: dict[str, SesionTutoria] = {}
# Quizzes generados, para evaluar sin exponer la respuesta correcta al cliente.
QUIZZES: dict[str, list[dict]] = {}


# ----------------------------- DTOs -----------------------------
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
    datos: dict | list


class ActualizarPlugin(BaseModel):
    seleccion: str


class GuardarConfig(BaseModel):
    carpeta_material: str = Field(min_length=1)
    ruta_obsidian: str = Field(min_length=1)


class SincronizarMaterial(BaseModel):
    materia: str = Field(min_length=1)


def _sesion(sesion_id: str) -> SesionTutoria:
    sesion = SESIONES.get(sesion_id)
    if not sesion:
        raise HTTPException(404, "Sesión de tutoría no encontrada o expirada.")
    return sesion


def _error(e: Exception) -> HTTPException:
    if isinstance(e, FileNotFoundError | ValueError):
        return HTTPException(400, str(e))
    return HTTPException(500, str(e))


# ----------------------------- Configuración de Usuario -----------------------------
@app.get("/api/config")
def obtener_configuracion() -> dict:
    return servicio_config.obtener_ajustes()


@app.post("/api/config")
def guardar_configuracion(body: GuardarConfig) -> dict:
    try:
        return servicio_config.guardar_ajustes(body.carpeta_material, body.ruta_obsidian)
    except Exception as e:
        raise _error(e) from e


# ----------------------------- Materias -----------------------------
@app.get("/api/materias")
def listar_materias() -> dict:
    return {"materias": gestor_archivos.cargar_materias()}


@app.post("/api/materias", status_code=201)
def crear_materia(body: NuevaMateria) -> dict:
    gestor_archivos.agregar_materia(body.nombre)
    return {"materias": gestor_archivos.cargar_materias()}


@app.get("/api/materias/{materia}/clases")
def proximas_clases(materia: str) -> dict:
    return {"clases": gestor_archivos.obtener_proximas_clases(materia)}


# ----------------------------- Tutoría (ml init) -----------------------------
@app.post("/api/tutoria/iniciar")
def iniciar_tutoria(body: IniciarTutoria) -> dict:
    sesion_id = uuid.uuid4().hex
    try:
        sesion = servicio_tutoria.iniciar_sesion(
            sesion_id, body.materia.strip(), body.tema.strip(), body.nivel_profundidad
        )
    except Exception as e:
        raise _error(e) from e
    gestor_archivos.agregar_materia(body.materia)
    SESIONES[sesion_id] = sesion
    return {
        "sesion_id": sesion_id,
        "materia": sesion.materia,
        "tema": sesion.tema,
        "nivel_profundidad": sesion.nivel_profundidad,
        "pasos": sesion.pasos,
        "materiales_asociados": sesion.materiales_asociados,
        "subtemas_adicionales": sesion.subtemas_adicionales,
    }


@app.get("/api/tutoria/{sesion_id}/paso/{indice}/stream")
def explicar_paso(sesion_id: str, indice: int) -> StreamingResponse:
    """Streaming SSE de la explicación del tutor para un paso."""
    sesion = _sesion(sesion_id)
    if not 0 <= indice < len(sesion.pasos):
        raise HTTPException(404, "Paso inexistente.")

    def eventos() -> Iterator[str]:
        try:
            for chunk in servicio_tutoria.explicar_paso_stream(sesion, indice):
                yield f"data: {json.dumps({'chunk': chunk}, ensure_ascii=False)}\n\n"
            yield "event: fin\ndata: {}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        eventos(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/tutoria/{sesion_id}/duda")
def resolver_duda(sesion_id: str, body: Duda) -> dict:
    sesion = _sesion(sesion_id)
    try:
        respuesta = servicio_tutoria.responder_duda(sesion, body.paso, body.duda.strip())
    except IndexError as e:
        raise HTTPException(404, str(e)) from e
    except Exception as e:
        raise _error(e) from e
    return {"respuesta": respuesta}


@app.post("/api/tutoria/{sesion_id}/finalizar")
def finalizar_tutoria(sesion_id: str) -> dict:
    sesion = _sesion(sesion_id)
    try:
        resultado = servicio_tutoria.finalizar_sesion(sesion)
    except Exception as e:
        raise _error(e) from e
    SESIONES.pop(sesion_id, None)
    return resultado


# ----------------------------- Telemetría (ml stats) -----------------------------
@app.get("/api/stats")
def estadisticas() -> dict:
    return telemetria.obtener_estadisticas()


# ----------------------------- Quiz (ml quiz) -----------------------------
@app.get("/api/quiz/generar")
def generar_quiz() -> dict:
    try:
        preguntas = motor_evaluacion.generar_quiz()
    except Exception as e:
        raise _error(e) from e
    quiz_id = uuid.uuid4().hex
    QUIZZES[quiz_id] = preguntas
    publicas = [
        {"enunciado": p.get("enunciado", ""), "opciones": p.get("opciones", [])} for p in preguntas
    ]
    return {"quiz_id": quiz_id, "preguntas": publicas}


@app.post("/api/quiz/evaluar")
def evaluar_quiz(body: RespuestaQuiz) -> dict:
    preguntas = QUIZZES.get(body.quiz_id)
    if preguntas is None:
        raise HTTPException(404, "Quiz no encontrado o expirado.")
    detalle = []
    aciertos = 0
    for idx, p in enumerate(preguntas):
        elegida = body.respuestas[idx] if idx < len(body.respuestas) else ""
        correcta = p.get("respuesta_correcta", "")
        ok = elegida.strip().lower() == str(correcta).strip().lower()
        aciertos += ok
        detalle.append({"correcto": ok, "respuesta_correcta": correcta, "elegida": elegida})
    total = len(preguntas)
    QUIZZES.pop(body.quiz_id, None)
    return {
        "aciertos": aciertos,
        "total": total,
        "porcentaje": round(aciertos / total * 100) if total else 0,
        "detalle": detalle,
    }


# ----------------------------- Sílabos (ml es) -----------------------------
@app.post("/api/silabo/extraer")
def extraer_silabo(
    archivo: Annotated[UploadFile, File()], materia: Annotated[str, Form()] = ""
) -> dict:
    nombre = archivo.filename or "silabo.txt"
    ext = os.path.splitext(nombre)[1].lower()
    if ext not in servicio_silabo.EXTENSIONES_SILABO:
        raise HTTPException(400, "Formato no soportado. Usa PDF, MD o TXT.")
    materia = materia.strip() or servicio_silabo.sugerir_nombre_materia(nombre)
    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, os.path.basename(nombre))
        with open(ruta, "wb") as f:
            shutil.copyfileobj(archivo.file, f)
        try:
            datos = servicio_silabo.extraer_cronograma(ruta, materia)
        except Exception as e:
            raise _error(e) from e
    return {"materia": materia, "datos": datos}


@app.post("/api/silabo/guardar")
def guardar_silabo(body: GuardarCronograma) -> dict:
    ruta = servicio_silabo.guardar_cronograma(body.materia.strip(), body.datos)
    return {"ruta": os.path.abspath(ruta), "materias": gestor_archivos.cargar_materias()}


# ----------------------------- Ingesta (ml im) -----------------------------
@app.get("/api/material/escanear")
def escanear_material(materia: str | None = None) -> dict:
    materias = (
        [materia]
        if materia and materia != "__todas__"
        else gestor_archivos.cargar_materias()
    )
    return {"escaneos": servicio_ingesta.escanear(materias)}


@app.post("/api/material/sincronizar/stream")
def sincronizar_material_stream(body: SincronizarMaterial) -> StreamingResponse:
    materias = (
        [body.materia]
        if body.materia != "__todas__"
        else gestor_archivos.cargar_materias()
    )

    def eventos() -> Iterator[str]:
        try:
            for ev in servicio_ingesta.ingestar_pendientes_stream(materias):
                yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"
            yield "event: fin\ndata: {}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        eventos(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/material/ingestar")
def ingestar_material(
    archivo: Annotated[UploadFile, File()],
    materia: Annotated[str, Form()],
    tipo: Annotated[str, Form()] = "material_complementario",
) -> dict:
    nombre = os.path.basename(archivo.filename or "material")
    ext = os.path.splitext(nombre)[1].lower()
    if ext not in servicio_ingesta.EXTENSIONES_MATERIAL:
        raise HTTPException(400, "Formato no soportado. Usa PDF, DOCX, TXT o MD.")
    if not materia.strip():
        raise HTTPException(400, "Debes indicar la asignatura.")
    gestor_archivos.agregar_materia(materia)
    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, nombre)
        with open(ruta, "wb") as f:
            shutil.copyfileobj(archivo.file, f)
        try:
            return servicio_ingesta.ingestar_archivo(ruta, nombre, materia.strip(), tipo)
        except Exception as e:
            raise _error(e) from e


# ----------------------------- Plugins (ml up) -----------------------------
@app.get("/api/plugins")
def listar_plugins() -> dict:
    return {"opciones": OPCIONES_PLUGIN}


@app.post("/api/plugins/actualizar")
def actualizar_plugin(body: ActualizarPlugin) -> dict:
    if body.seleccion not in OPCIONES_PLUGIN:
        raise HTTPException(400, "Plugin no válido.")
    try:
        resultado = gestor_plugins.actualizar_plugin(body.seleccion)
    except Exception as e:
        raise _error(e) from e
    return {"seleccion": body.seleccion, "resultado": resultado}


# ----------------------------- Frontend estático -----------------------------
@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(RUTA_ESTATICOS / "index.html")


app.mount("/static", StaticFiles(directory=RUTA_ESTATICOS), name="static")


def run() -> None:
    """Punto de entrada para el servidor web: `ml-web`."""
    import uvicorn

    host = os.getenv("WEB_HOST", "127.0.0.1")
    port = int(os.getenv("WEB_PORT", "8000"))
    uvicorn.run("modular_learning.apps.api.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
