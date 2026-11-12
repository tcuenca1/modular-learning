"""Hash de contraseñas con scrypt (biblioteca estándar: sin dependencias nuevas)."""

from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import secrets

from modular_learning.core.ports.usuarios import HasheadorContrasenaPort

# N=2^14, r=8, p=1: unos 16 MiB y ~50 ms en un PC; es el mínimo recomendado por OWASP para scrypt
N, R, P = 2**14, 8, 1
LONGITUD_CLAVE = 32


class HasheadorScrypt(HasheadorContrasenaPort):
    """Formato: `scrypt$N$r$p$<sal base64>$<clave base64>`; guarda sus propios parámetros."""

    def __init__(self, n: int = N, r: int = R, p: int = P):
        self.n, self.r, self.p = n, r, p

    @staticmethod
    def _derivar(contrasena: str, sal: bytes, n: int, r: int, p: int) -> bytes:
        return hashlib.scrypt(
            contrasena.encode(), salt=sal, n=n, r=r, p=p, dklen=LONGITUD_CLAVE, maxmem=64 * 1024**2
        )

    def hashear(self, contrasena: str) -> str:
        sal = secrets.token_bytes(16)
        clave = self._derivar(contrasena, sal, self.n, self.r, self.p)
        b64 = lambda b: base64.b64encode(b).decode()
        return f"scrypt${self.n}${self.r}${self.p}${b64(sal)}${b64(clave)}"

    def verificar(self, contrasena: str, hash_guardado: str) -> bool:
        try:
            esquema, n, r, p, sal, clave = hash_guardado.split("$")
            if esquema != "scrypt":
                return False
            esperada = base64.b64decode(clave)
            obtenida = self._derivar(contrasena, base64.b64decode(sal), int(n), int(r), int(p))
        except (ValueError, binascii.Error, MemoryError):
            return False
        return hmac.compare_digest(esperada, obtenida)


__all__ = ["HasheadorScrypt"]
