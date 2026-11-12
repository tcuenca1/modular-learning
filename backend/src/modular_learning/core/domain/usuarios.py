"""Cuentas de usuario: identidad, validación de datos y sesiones firmadas (sin acceso a disco)."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import re
import secrets
import threading
from dataclasses import asdict, dataclass
from typing import Any

LONGITUD_MINIMA_CONTRASENA = 10
LONGITUD_MAXIMA_CONTRASENA = 128
_FORMATO_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UsuarioInvalido(ValueError):
    """Los datos de la cuenta no cumplen las reglas (correo, nombre o contraseña)."""


class UsuarioDuplicado(ValueError):
    """Ya existe una cuenta con ese correo."""


class UsuarioNoEncontrado(LookupError):
    """No existe la cuenta."""


class CredencialesInvalidas(Exception):
    """Correo o contraseña incorrectos, o cuenta desactivada. El mensaje no dice cuál."""


class DemasiadosIntentos(Exception):
    """Demasiados intentos fallidos: hay que esperar `espera_segundos`."""

    def __init__(self, espera_segundos: int):
        super().__init__(f"Demasiados intentos. Espera {max(1, espera_segundos // 60)} min.")
        self.espera_segundos = espera_segundos


def normalizar_identificador(texto: str) -> str:
    """Correo o usuario en minúsculas y sin espacios alrededor: así se compara y se guarda."""
    return str(texto or "").strip().lower()


def validar_correo(correo: str) -> str:
    """Retorna el correo normalizado o lanza UsuarioInvalido."""
    limpio = normalizar_identificador(correo)
    if len(limpio) > 120 or not _FORMATO_CORREO.match(limpio):
        raise UsuarioInvalido("Escribe un correo válido, como nombre@correo.com.")
    return limpio


def validar_nombre(nombre: str) -> str:
    limpio = " ".join(str(nombre or "").split())
    if not limpio or len(limpio) > 80 or any(c in limpio for c in "<>\x00"):
        raise UsuarioInvalido("El nombre es obligatorio y debe tener 80 caracteres o menos.")
    return limpio


def validar_contrasena(contrasena: str) -> str:
    if not LONGITUD_MINIMA_CONTRASENA <= len(contrasena or "") <= LONGITUD_MAXIMA_CONTRASENA:
        raise UsuarioInvalido(
            f"La contraseña debe tener entre {LONGITUD_MINIMA_CONTRASENA} y "
            f"{LONGITUD_MAXIMA_CONTRASENA} caracteres."
        )
    return contrasena


@dataclass
class Usuario:
    """Una cuenta. El `id` nombra la carpeta/prefijo de sus datos y nunca cambia."""

    id: str
    correo: str
    nombre: str
    hash_contrasena: str
    es_admin: bool = False
    activo: bool = True
    creado: str = ""
    # Huella de la ML_CONTRASENA con que se sincronizó (solo el administrador del entorno)
    huella_entorno: str = ""

    @staticmethod
    def nuevo_id() -> str:
        return secrets.token_hex(8)

    def a_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> Usuario | None:
        campos = cls.__dataclass_fields__
        if not datos.get("id") or not datos.get("correo"):
            return None
        return cls(**{k: v for k, v in datos.items() if k in campos})

    def publico(self) -> dict[str, Any]:
        """Lo que ve el cliente: nunca el hash de la contraseña."""
        return {
            "id": self.id,
            "correo": self.correo,
            "nombre": self.nombre,
            "es_admin": self.es_admin,
            "activo": self.activo,
            "creado": self.creado,
        }

    def huella_sesion(self) -> str:
        """Cambia al cambiar la contraseña: invalida las sesiones anteriores."""
        return hashlib.sha256(self.hash_contrasena.encode()).hexdigest()[:12]


# ------------------------------------------------------------------------------ sesiones firmadas
def _b64(datos: bytes) -> str:
    return base64.urlsafe_b64encode(datos).rstrip(b"=").decode()


def _desb64(texto: str) -> bytes:
    return base64.urlsafe_b64decode(texto + "=" * (-len(texto) % 4))


def firmar_sesion(secreto: str, usuario: Usuario, expira: float) -> str:
    """Token `<carga>.<firma>` con el id, la huella de la contraseña y la fecha de caducidad."""
    carga = _b64(
        json.dumps(
            {"u": usuario.id, "v": usuario.huella_sesion(), "e": int(expira)},
            separators=(",", ":"),
        ).encode()
    )
    firma = hmac.new(secreto.encode(), carga.encode(), hashlib.sha256).digest()
    return f"{carga}.{_b64(firma)}"


def leer_sesion(secreto: str, token: str, ahora: float) -> tuple[str, str] | None:
    """(id_usuario, huella) si el token es auténtico y no caducó; None en cualquier otro caso."""
    try:
        carga, _, firma = (token or "").partition(".")
        esperada = hmac.new(secreto.encode(), carga.encode(), hashlib.sha256).digest()
        if not carga or not hmac.compare_digest(esperada, _desb64(firma)):
            return None
        datos = json.loads(_desb64(carga))
        if float(datos["e"]) < ahora:
            return None
        return str(datos["u"]), str(datos["v"])
    except (ValueError, KeyError, TypeError, binascii.Error):
        return None


class LimitadorIntentos:
    """
    Frena la fuerza bruta: tras `maximo` fallos en `ventana` segundos para una misma clave
    (origen + usuario) bloquea esa clave hasta que pasa la ventana. En memoria y por proceso.
    """

    MAXIMO_CLAVES = 10_000  # tope de memoria: claves inventadas no crecen sin límite

    def __init__(self, maximo: int = 5, ventana: int = 900):
        self.maximo, self.ventana = maximo, ventana
        self._fallos: dict[str, list[float]] = {}
        self._candado = threading.Lock()  # los endpoints síncronos corren en hilos distintos

    def _vigentes(self, clave: str, ahora: float) -> list[float]:
        vigentes = [t for t in self._fallos.get(clave, []) if ahora - t < self.ventana]
        if vigentes:
            self._fallos[clave] = vigentes
        else:
            self._fallos.pop(clave, None)
        return vigentes

    def comprobar(self, clave: str, ahora: float) -> None:
        with self._candado:
            vigentes = self._vigentes(clave, ahora)
            if len(vigentes) >= self.maximo:
                raise DemasiadosIntentos(int(self.ventana - (ahora - vigentes[0])))

    def registrar_fallo(self, clave: str, ahora: float) -> None:
        with self._candado:
            if len(self._fallos) >= self.MAXIMO_CLAVES:
                for k in list(self._fallos):  # poda las claves ya caducadas
                    self._vigentes(k, ahora)
            if len(self._fallos) < self.MAXIMO_CLAVES:
                self._fallos.setdefault(clave, []).append(ahora)

    def limpiar(self, clave: str) -> None:
        with self._candado:
            self._fallos.pop(clave, None)


__all__ = [
    "LONGITUD_MINIMA_CONTRASENA",
    "CredencialesInvalidas",
    "DemasiadosIntentos",
    "LimitadorIntentos",
    "Usuario",
    "UsuarioDuplicado",
    "UsuarioInvalido",
    "UsuarioNoEncontrado",
    "firmar_sesion",
    "leer_sesion",
    "normalizar_identificador",
    "validar_contrasena",
    "validar_correo",
    "validar_nombre",
]
