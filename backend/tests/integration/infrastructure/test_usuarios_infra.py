"""Hash scrypt y repositorio de cuentas sobre el almacén de archivos."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest

from modular_learning.core.domain.usuarios import Usuario, UsuarioDuplicado
from modular_learning.infrastructure.persistence.almacen import AlmacenArchivos
from modular_learning.infrastructure.persistence.json_usuarios import JsonUsuariosRepo
from modular_learning.infrastructure.seguridad.hasheador_scrypt import HasheadorScrypt


def test_scrypt_hashea_con_sal_y_verifica():
    h = HasheadorScrypt()
    a, b = h.hashear("una-clave-larga-1"), h.hashear("una-clave-larga-1")
    assert a != b and a.startswith("scrypt$16384$8$1$")  # sal distinta cada vez
    assert "una-clave" not in a
    assert h.verificar("una-clave-larga-1", a) is True
    assert h.verificar("una-clave-larga-2", a) is False
    assert h.verificar("ñandú-€-🙂", h.hashear("ñandú-€-🙂")) is True


@pytest.mark.parametrize(
    "malo", ["", "x", "bcrypt$1$2$3$4$5", "scrypt$a$b$c$d$e", "scrypt$1$1$1$!!$!!"]
)
def test_scrypt_con_hash_ilegible_devuelve_false(malo):
    assert HasheadorScrypt().verificar("lo-que-sea", malo) is False


def test_scrypt_respeta_los_parametros_del_hash_guardado():
    viejo = HasheadorScrypt(n=2**10).hashear("clave-larga-123")
    assert HasheadorScrypt().verificar("clave-larga-123", viejo) is True  # aunque hoy N sea mayor


def _usuario(correo: str, id_: str | None = None) -> Usuario:
    return Usuario(id=id_ or Usuario.nuevo_id(), correo=correo, nombre="X", hash_contrasena="h")


def test_repo_guarda_lee_y_actualiza(tmp_path):
    repo = JsonUsuariosRepo(AlmacenArchivos(tmp_path))
    assert repo.listar() == []
    ana = _usuario("ana@correo.com")
    repo.guardar(ana)
    ana.nombre = "Ana P."
    repo.guardar(ana)
    otro = JsonUsuariosRepo(AlmacenArchivos(tmp_path))  # otra instancia: está en disco
    assert [u.nombre for u in otro.listar()] == ["Ana P."]
    assert otro.obtener(ana.id).correo == "ana@correo.com"
    assert otro.obtener_por_correo("ana@correo.com").id == ana.id
    assert otro.obtener("no") is None and otro.obtener_por_correo("no@x.com") is None


def test_repo_rechaza_correo_duplicado_de_otra_cuenta(tmp_path):
    repo = JsonUsuariosRepo(AlmacenArchivos(tmp_path))
    repo.guardar(_usuario("ana@correo.com"))
    with pytest.raises(UsuarioDuplicado):
        repo.guardar(_usuario("ana@correo.com"))


def test_altas_simultaneas_no_pierden_cuentas(tmp_path):
    repo = JsonUsuariosRepo(AlmacenArchivos(tmp_path))
    with ThreadPoolExecutor(12) as pool:
        list(pool.map(lambda i: repo.guardar(_usuario(f"u{i}@correo.com")), range(12)))
    assert len(JsonUsuariosRepo(AlmacenArchivos(tmp_path)).listar()) == 12


def test_el_json_dañado_no_rompe_el_arranque(tmp_path):
    almacen = AlmacenArchivos(tmp_path)
    almacen.escribir("auth/usuarios.json", "{no es json")
    assert JsonUsuariosRepo(almacen).listar() == []
