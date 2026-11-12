"""Cuentas de usuario en `auth/usuarios.json` del almacén global (no de una cuenta)."""

from __future__ import annotations

from modular_learning.core.domain.usuarios import Usuario, UsuarioDuplicado
from modular_learning.core.ports.usuarios import UsuariosRepo
from modular_learning.infrastructure.persistence.almacen import (
    AlmacenDocumentos,
    DocumentoJson,
    almacen_global,
)


class JsonUsuariosRepo(UsuariosRepo):
    def __init__(self, almacen: AlmacenDocumentos | None = None):
        self._documento = DocumentoJson("auth/usuarios.json", None, almacen or almacen_global())

    def _cargar(self) -> list[Usuario]:
        datos = self._documento.leer([])
        usuarios = [Usuario.desde_dict(d) for d in datos if isinstance(d, dict)]
        return [u for u in usuarios if u is not None]

    def listar(self) -> list[Usuario]:
        return self._cargar()

    def obtener(self, usuario_id: str) -> Usuario | None:
        return next((u for u in self._cargar() if u.id == usuario_id), None)

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        return next((u for u in self._cargar() if u.correo == correo), None)

    def guardar(self, usuario: Usuario) -> None:
        with self._documento.bloqueo():
            usuarios = self._cargar()
            if any(u.correo == usuario.correo and u.id != usuario.id for u in usuarios):
                raise UsuarioDuplicado(f"Ya existe una cuenta con el correo {usuario.correo}.")
            for i, existente in enumerate(usuarios):
                if existente.id == usuario.id:
                    usuarios[i] = usuario
                    break
            else:
                usuarios.append(usuario)
            self._documento.escribir([u.a_dict() for u in usuarios], sangria=2)


__all__ = ["JsonUsuariosRepo"]
