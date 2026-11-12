"""Caso de uso de cuentas: inicio de sesión, alta de usuarios y cambio de contraseña."""

from __future__ import annotations

import hashlib
import time
from collections.abc import Callable
from datetime import datetime, timezone

from modular_learning.core.domain.usuarios import (
    CredencialesInvalidas,
    LimitadorIntentos,
    Usuario,
    UsuarioDuplicado,
    UsuarioInvalido,
    UsuarioNoEncontrado,
    firmar_sesion,
    leer_sesion,
    normalizar_identificador,
    validar_contrasena,
    validar_correo,
    validar_nombre,
)
from modular_learning.core.ports.usuarios import HasheadorContrasenaPort, UsuariosRepo

DURACION_SESION_SEGUNDOS = 14 * 24 * 3600
# Tope de fallos por cuenta sin importar el origen (frena la fuerza bruta distribuida)
FALLOS_MAXIMOS_POR_CUENTA = 20


class AutenticacionService:
    """Cuentas con contraseña y sesiones firmadas; no sabe nada de HTTP ni de cookies."""

    def __init__(
        self,
        repo: UsuariosRepo,
        hasheador: HasheadorContrasenaPort,
        secreto: str,
        limitador: LimitadorIntentos | None = None,
        ahora: Callable[[], float] = time.time,
        duracion: int = DURACION_SESION_SEGUNDOS,
    ):
        if len(secreto) < 16:
            raise ValueError("El secreto de sesión debe tener al menos 16 caracteres.")
        self.repo = repo
        self.hasheador = hasheador
        self._secreto = secreto
        self.limitador = limitador or LimitadorIntentos()
        self.limitador_cuenta = LimitadorIntentos(maximo=FALLOS_MAXIMOS_POR_CUENTA)
        self._ahora = ahora
        self.duracion = duracion

    # ----------------------------------------------------------------------- sesión
    def iniciar_sesion(
        self, identificador: str, contrasena: str, origen: str = ""
    ) -> tuple[Usuario, str]:
        """Valida las credenciales y retorna (usuario, token de sesión)."""
        correo = normalizar_identificador(identificador)
        clave = f"{origen}|{correo}"
        self.limitador.comprobar(clave, self._ahora())
        self.limitador_cuenta.comprobar(correo, self._ahora())
        usuario = self.repo.obtener_por_correo(correo)
        # Se verifica siempre (aunque no exista la cuenta) para no revelar cuáles existen por el tiempo
        hash_guardado = usuario.hash_contrasena if usuario else self._hash_falso()
        correcta = self.hasheador.verificar(contrasena or "", hash_guardado)
        if not (usuario and usuario.activo and correcta):
            self.limitador.registrar_fallo(clave, self._ahora())
            self.limitador_cuenta.registrar_fallo(correo, self._ahora())
            raise CredencialesInvalidas("Correo o contraseña incorrectos.")
        self.limitador.limpiar(clave)
        self.limitador_cuenta.limpiar(correo)
        return usuario, firmar_sesion(self._secreto, usuario, self._ahora() + self.duracion)

    def usuario_de_token(self, token: str) -> Usuario | None:
        """La cuenta a la que pertenece un token vigente; None si es inválido, caducó o cambió."""
        leido = leer_sesion(self._secreto, token, self._ahora())
        if leido is None:
            return None
        usuario_id, huella = leido
        usuario = self.repo.obtener(usuario_id)
        if usuario is None or not usuario.activo or usuario.huella_sesion() != huella:
            return None
        return usuario

    def _hash_falso(self) -> str:
        if not hasattr(self, "_falso"):
            self._falso = self.hasheador.hashear("contraseña-que-nadie-usa")
        return self._falso

    # ----------------------------------------------------------------------- administración
    def crear_usuario(
        self, correo: str, nombre: str, contrasena: str, es_admin: bool = False
    ) -> Usuario:
        correo_ok = validar_correo(correo)
        usuario = Usuario(
            id=Usuario.nuevo_id(),
            correo=correo_ok,
            nombre=validar_nombre(nombre),
            hash_contrasena=self.hasheador.hashear(validar_contrasena(contrasena)),
            es_admin=es_admin,
            creado=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        if self.repo.obtener_por_correo(correo_ok):
            raise UsuarioDuplicado(f"Ya existe una cuenta con el correo {correo_ok}.")
        self.repo.guardar(usuario)
        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        return self.repo.listar()

    def actualizar_usuario(
        self, usuario_id: str, activo: bool | None = None, contrasena: str | None = None
    ) -> Usuario:
        usuario = self._exigir(usuario_id)
        if activo is not None:
            if usuario.es_admin and not activo:
                otros = [
                    u for u in self.repo.listar() if u.es_admin and u.activo and u.id != usuario.id
                ]
                if not otros:
                    raise UsuarioInvalido("No se puede desactivar al único administrador activo.")
            usuario.activo = activo
        if contrasena is not None:
            usuario.hash_contrasena = self.hasheador.hashear(validar_contrasena(contrasena))
        self.repo.guardar(usuario)
        return usuario

    def cambiar_contrasena(self, usuario_id: str, actual: str, nueva: str) -> str:
        """Cambia la contraseña propia y retorna un token nuevo (el anterior queda invalidado)."""
        usuario = self._exigir(usuario_id)
        if not self.hasheador.verificar(actual or "", usuario.hash_contrasena):
            raise CredencialesInvalidas("La contraseña actual no es correcta.")
        usuario.hash_contrasena = self.hasheador.hashear(validar_contrasena(nueva))
        self.repo.guardar(usuario)
        return firmar_sesion(self._secreto, usuario, self._ahora() + self.duracion)

    @staticmethod
    def _huella_entorno(contrasena: str) -> str:
        return hashlib.sha256(contrasena.encode()).hexdigest()[:16]

    def asegurar_admin(self, identificador: str, nombre: str, contrasena: str) -> Usuario:
        """
        Crea la cuenta de administrador del entorno. En arranques posteriores NO pisa la
        contraseña que el administrador haya cambiado en la web: solo la restablece cuando
        ML_CONTRASENA cambió respecto de la última vez (es la vía de recuperación).
        """
        correo = normalizar_identificador(identificador)
        validar_contrasena(contrasena)
        huella = self._huella_entorno(contrasena)
        existente = self.repo.obtener_por_correo(correo)
        if existente is None:
            usuario = Usuario(
                id=Usuario.nuevo_id(),
                correo=correo,
                nombre=validar_nombre(nombre),
                hash_contrasena=self.hasheador.hashear(contrasena),
                es_admin=True,
                creado=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                huella_entorno=huella,
            )
            self.repo.guardar(usuario)
            return usuario
        cambios = False
        if existente.huella_entorno != huella:
            existente.hash_contrasena = self.hasheador.hashear(contrasena)
            existente.huella_entorno = huella
            cambios = True
        if not (existente.es_admin and existente.activo):
            existente.es_admin, existente.activo = True, True
            cambios = True
        if cambios:
            self.repo.guardar(existente)
        return existente

    def _exigir(self, usuario_id: str) -> Usuario:
        usuario = self.repo.obtener(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontrado("Cuenta no encontrada.")
        return usuario


__all__ = ["DURACION_SESION_SEGUNDOS", "AutenticacionService"]
