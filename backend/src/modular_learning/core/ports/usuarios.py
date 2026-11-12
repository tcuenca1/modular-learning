"""Puertos de las cuentas de usuario: dónde se guardan y cómo se protegen las contraseñas."""

from __future__ import annotations

from abc import ABC, abstractmethod

from modular_learning.core.domain.usuarios import Usuario


class UsuariosRepo(ABC):
    """Repositorio de cuentas (global: no pertenece a ninguna cuenta)."""

    @abstractmethod
    def listar(self) -> list[Usuario]:
        """Todas las cuentas, en orden de creación."""

    @abstractmethod
    def obtener(self, usuario_id: str) -> Usuario | None:
        """La cuenta con ese id, o None."""

    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Usuario | None:
        """La cuenta con ese correo ya normalizado, o None."""

    @abstractmethod
    def guardar(self, usuario: Usuario) -> None:
        """Alta o actualización por id. Debe rechazar (UsuarioDuplicado) un correo ya usado."""


class HasheadorContrasenaPort(ABC):
    """Hash lento y con sal de contraseñas."""

    @abstractmethod
    def hashear(self, contrasena: str) -> str:
        """Hash autocontenido (incluye algoritmo, parámetros y sal)."""

    @abstractmethod
    def verificar(self, contrasena: str, hash_guardado: str) -> bool:
        """Compara en tiempo constante; False si el hash es ilegible."""


__all__ = ["HasheadorContrasenaPort", "UsuariosRepo"]
