"""Router de cuentas: sesión, contraseña propia y administración de usuarios."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field

from modular_learning.apps.api.autenticacion import NOMBRE_COOKIE
from modular_learning.apps.api.dependencies import get_container
from modular_learning.apps.api.errores import error_cliente
from modular_learning.apps.api.seguridad import en_nube
from modular_learning.bootstrap import Container
from modular_learning.core.application.autenticacion import AutenticacionService
from modular_learning.core.domain.usuarios import (
    CredencialesInvalidas,
    DemasiadosIntentos,
    Usuario,
    UsuarioDuplicado,
    UsuarioInvalido,
    UsuarioNoEncontrado,
)
from modular_learning.infrastructure.persistence.almacen import cuentas_activas

router = APIRouter(prefix="/api/auth", tags=["auth"])


class Login(BaseModel):
    correo: str = Field(min_length=1, max_length=200)
    contrasena: str = Field(min_length=1, max_length=500)


class CambioContrasena(BaseModel):
    actual: str = Field(max_length=500)
    nueva: str = Field(max_length=500)


class NuevoUsuario(BaseModel):
    correo: str = Field(max_length=200)
    nombre: str = Field(max_length=200)
    contrasena: str = Field(max_length=500)


class CambiosUsuario(BaseModel):
    activo: bool | None = None
    contrasena: str | None = Field(default=None, max_length=500)


def _servicio(contenedor: Annotated[Container, Depends(get_container)]) -> AutenticacionService:
    if contenedor.autenticacion_service is None:
        raise HTTPException(status_code=404, detail="El acceso con cuentas no está activo.")
    return contenedor.autenticacion_service


def _usuario(request: Request) -> Usuario:
    usuario = getattr(request.state, "usuario", None)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Inicia sesión para continuar.")
    return usuario


def _admin(usuario: Annotated[Usuario, Depends(_usuario)]) -> Usuario:
    if not usuario.es_admin:
        raise HTTPException(status_code=403, detail="Solo el administrador puede hacer esto.")
    return usuario


def _origen(request: Request) -> str:
    """IP del cliente. Tras el proxy de Render la última entrada de X-Forwarded-For es la real."""
    reenviado = request.headers.get("x-forwarded-for", "")
    if en_nube() and reenviado:
        return reenviado.split(",")[-1].strip()
    return request.client.host if request.client else ""


def _poner_cookie(respuesta: Response, token: str, segundos: int) -> None:
    respuesta.set_cookie(
        NOMBRE_COOKIE,
        token,
        max_age=segundos,
        httponly=True,
        secure=en_nube(),
        samesite="lax",
        path="/",
    )


@router.get("/yo")
def yo(request: Request) -> dict[str, Any]:
    usuario = getattr(request.state, "usuario", None)
    return {
        "autenticacion": cuentas_activas(),
        "usuario": usuario.publico() if usuario else None,
    }


@router.post("/login")
def iniciar_sesion(
    body: Login,
    request: Request,
    respuesta: Response,
    servicio: Annotated[AutenticacionService, Depends(_servicio)],
) -> dict[str, Any]:
    if not servicio.listar_usuarios():
        # Ninguna cuenta existe: el arranque no pudo crear la del administrador (p. ej. porque
        # ML_CONTRASENA es demasiado corta). Decirlo evita que parezca "credenciales incorrectas".
        raise HTTPException(
            status_code=503,
            detail=(
                "El servidor aún no tiene la cuenta de administrador. Revisa en Render que "
                "ML_USUARIO y ML_CONTRASENA estén definidas y que la contraseña tenga al menos "
                "10 caracteres; el servicio se reinicia solo al guardar."
            ),
        )
    try:
        usuario, token = servicio.iniciar_sesion(body.correo, body.contrasena, _origen(request))
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except DemasiadosIntentos as e:
        raise HTTPException(
            status_code=429, detail=str(e), headers={"Retry-After": str(e.espera_segundos)}
        ) from e
    _poner_cookie(respuesta, token, servicio.duracion)
    return {"usuario": usuario.publico()}


@router.post("/logout")
def cerrar_sesion(respuesta: Response) -> dict[str, bool]:
    respuesta.delete_cookie(NOMBRE_COOKIE, path="/")
    return {"ok": True}


@router.post("/contrasena")
def cambiar_contrasena(
    body: CambioContrasena,
    respuesta: Response,
    usuario: Annotated[Usuario, Depends(_usuario)],
    servicio: Annotated[AutenticacionService, Depends(_servicio)],
) -> dict[str, bool]:
    try:
        token = servicio.cambiar_contrasena(usuario.id, body.actual, body.nueva)
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except UsuarioInvalido as e:
        raise error_cliente(e, 422) from e
    _poner_cookie(respuesta, token, servicio.duracion)  # la sesión anterior queda invalidada
    return {"ok": True}


@router.get("/usuarios")
def listar_usuarios(
    _: Annotated[Usuario, Depends(_admin)],
    servicio: Annotated[AutenticacionService, Depends(_servicio)],
) -> dict[str, Any]:
    return {"usuarios": [u.publico() for u in servicio.listar_usuarios()]}


@router.post("/usuarios", status_code=201)
def crear_usuario(
    body: NuevoUsuario,
    _: Annotated[Usuario, Depends(_admin)],
    servicio: Annotated[AutenticacionService, Depends(_servicio)],
) -> dict[str, Any]:
    try:
        return {
            "usuario": servicio.crear_usuario(body.correo, body.nombre, body.contrasena).publico()
        }
    except UsuarioDuplicado as e:
        raise error_cliente(e, 409) from e
    except UsuarioInvalido as e:
        raise error_cliente(e, 422) from e


@router.patch("/usuarios/{usuario_id}")
def actualizar_usuario(
    usuario_id: str,
    body: CambiosUsuario,
    _: Annotated[Usuario, Depends(_admin)],
    servicio: Annotated[AutenticacionService, Depends(_servicio)],
) -> dict[str, Any]:
    try:
        return {
            "usuario": servicio.actualizar_usuario(
                usuario_id, body.activo, body.contrasena
            ).publico()
        }
    except UsuarioNoEncontrado as e:
        raise error_cliente(e, 404) from e
    except UsuarioInvalido as e:
        raise error_cliente(e, 422) from e


__all__ = ["router"]
