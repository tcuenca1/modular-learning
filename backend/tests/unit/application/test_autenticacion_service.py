"""AutenticacionService con fakes: sesión, alta de cuentas, cambio de contraseña y bloqueo."""

from __future__ import annotations

import pytest

from modular_learning.core.application.autenticacion import AutenticacionService
from modular_learning.core.domain.usuarios import (
    CredencialesInvalidas,
    DemasiadosIntentos,
    UsuarioDuplicado,
    UsuarioInvalido,
    UsuarioNoEncontrado,
)
from tests.unit.application.fake_adapters import FakeHasheador, InMemoryUsuariosRepo

SECRETO = "secreto-de-prueba-0123456789"
CLAVE = "una-clave-larga-1"


class Reloj:
    def __init__(self) -> None:
        self.t = 1_000_000.0

    def __call__(self) -> float:
        return self.t


@pytest.fixture
def reloj() -> Reloj:
    return Reloj()


@pytest.fixture
def servicio(reloj) -> AutenticacionService:
    return AutenticacionService(
        InMemoryUsuariosRepo(), FakeHasheador(), SECRETO, ahora=reloj, duracion=3600
    )


def test_el_secreto_corto_se_rechaza():
    with pytest.raises(ValueError):
        AutenticacionService(InMemoryUsuariosRepo(), FakeHasheador(), "corto")


def test_crear_usuario_normaliza_y_no_expone_el_hash(servicio):
    u = servicio.crear_usuario("  Ana@Correo.COM ", "  Ana   Pérez ", CLAVE)
    assert (u.correo, u.nombre, u.es_admin, u.activo) == (
        "ana@correo.com",
        "Ana Pérez",
        False,
        True,
    )
    assert "hash_contrasena" not in u.publico()
    assert len(u.id) == 16


@pytest.mark.parametrize(
    ("correo", "nombre", "clave"),
    [
        ("sin-arroba", "Ana", CLAVE),
        ("a@b", "Ana", CLAVE),
        ("ana@correo.com", "", CLAVE),
        ("ana@correo.com", "x" * 81, CLAVE),
        ("ana@correo.com", "Ana", "corta"),
        ("ana@correo.com", "Ana", "x" * 129),
    ],
)
def test_crear_usuario_valida(servicio, correo, nombre, clave):
    with pytest.raises(UsuarioInvalido):
        servicio.crear_usuario(correo, nombre, clave)
    assert servicio.listar_usuarios() == []


def test_correo_duplicado(servicio):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    with pytest.raises(UsuarioDuplicado):
        servicio.crear_usuario("ANA@correo.com", "Otra", CLAVE)


def test_iniciar_sesion_y_leer_el_token(servicio):
    ana = servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    usuario, token = servicio.iniciar_sesion(" ANA@correo.com ", CLAVE)
    assert usuario.id == ana.id
    assert servicio.usuario_de_token(token).id == ana.id


def test_credenciales_incorrectas_no_dicen_cual_falla(servicio):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    for correo, clave in [("ana@correo.com", "mala-clave-123"), ("nadie@correo.com", CLAVE)]:
        with pytest.raises(CredencialesInvalidas) as e:
            servicio.iniciar_sesion(correo, clave)
        assert str(e.value) == "Correo o contraseña incorrectos."


def test_con_una_cuenta_inexistente_tambien_se_verifica_un_hash(servicio):
    servicio.hasheador.verificaciones.clear()
    with pytest.raises(CredencialesInvalidas):
        servicio.iniciar_sesion("nadie@correo.com", CLAVE)
    assert servicio.hasheador.verificaciones == [CLAVE]  # mismo trabajo que con una cuenta real


def test_cuenta_desactivada_no_entra_y_pierde_la_sesion(servicio):
    ana = servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    _, token = servicio.iniciar_sesion("ana@correo.com", CLAVE)
    servicio.actualizar_usuario(ana.id, activo=False)
    assert servicio.usuario_de_token(token) is None
    with pytest.raises(CredencialesInvalidas):
        servicio.iniciar_sesion("ana@correo.com", CLAVE)


def test_el_token_caduca(servicio, reloj):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    _, token = servicio.iniciar_sesion("ana@correo.com", CLAVE)
    reloj.t += 3599
    assert servicio.usuario_de_token(token) is not None
    reloj.t += 2
    assert servicio.usuario_de_token(token) is None


def test_token_manipulado_o_de_otro_secreto_no_vale(servicio):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    _, token = servicio.iniciar_sesion("ana@correo.com", CLAVE)
    carga, firma = token.split(".")
    for malo in ["", "x", "a.b", f"{carga}.{firma[:-2]}AA", f"{carga[:-2]}AA.{firma}", f"{carga}."]:
        assert servicio.usuario_de_token(malo) is None
    otro = AutenticacionService(servicio.repo, FakeHasheador(), "otro-secreto-0123456789")
    assert otro.usuario_de_token(token) is None


def test_cambiar_contrasena_invalida_los_tokens_anteriores(servicio):
    ana = servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    _, viejo = servicio.iniciar_sesion("ana@correo.com", CLAVE)
    nuevo = servicio.cambiar_contrasena(ana.id, CLAVE, "otra-clave-larga-2")
    assert servicio.usuario_de_token(viejo) is None
    assert servicio.usuario_de_token(nuevo).id == ana.id
    servicio.iniciar_sesion("ana@correo.com", "otra-clave-larga-2")


def test_cambiar_contrasena_exige_la_actual_y_una_valida(servicio):
    ana = servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    with pytest.raises(CredencialesInvalidas):
        servicio.cambiar_contrasena(ana.id, "no-es-la-actual", "otra-clave-larga-2")
    with pytest.raises(UsuarioInvalido):
        servicio.cambiar_contrasena(ana.id, CLAVE, "corta")
    servicio.iniciar_sesion("ana@correo.com", CLAVE)  # sigue la anterior


def test_restablecer_contrasena_como_admin(servicio):
    ana = servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    servicio.actualizar_usuario(ana.id, contrasena="restablecida-123")
    servicio.iniciar_sesion("ana@correo.com", "restablecida-123")
    with pytest.raises(UsuarioNoEncontrado):
        servicio.actualizar_usuario("no-existe", activo=False)


def test_bloqueo_tras_cinco_fallos_y_libera_con_el_tiempo(servicio, reloj):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    for _ in range(5):
        with pytest.raises(CredencialesInvalidas):
            servicio.iniciar_sesion("ana@correo.com", "mala-clave-123", origen="1.2.3.4")
    with pytest.raises(DemasiadosIntentos) as e:
        servicio.iniciar_sesion("ana@correo.com", CLAVE, origen="1.2.3.4")  # ni con la buena
    assert e.value.espera_segundos > 0
    servicio.iniciar_sesion(
        "ana@correo.com", CLAVE, origen="9.9.9.9"
    )  # otro origen no se ve afectado
    reloj.t += 901
    servicio.iniciar_sesion("ana@correo.com", CLAVE, origen="1.2.3.4")


def test_un_acierto_reinicia_el_contador(servicio):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    for _ in range(4):
        with pytest.raises(CredencialesInvalidas):
            servicio.iniciar_sesion("ana@correo.com", "mala-clave-123")
    servicio.iniciar_sesion("ana@correo.com", CLAVE)
    for _ in range(4):
        with pytest.raises(CredencialesInvalidas):
            servicio.iniciar_sesion("ana@correo.com", "mala-clave-123")


def test_asegurar_admin_crea_y_sincroniza_con_el_entorno(servicio):
    admin = servicio.asegurar_admin("Estudiante", "Administrador", "clave-del-entorno-1")
    assert (admin.correo, admin.es_admin) == ("estudiante", True)
    servicio.iniciar_sesion("estudiante", "clave-del-entorno-1")

    # Idempotente: no crea otra cuenta
    assert (
        servicio.asegurar_admin("estudiante", "Administrador", "clave-del-entorno-1").id == admin.id
    )
    assert len(servicio.listar_usuarios()) == 1

    # Cambiar ML_CONTRASENA recupera el acceso (y revoca las sesiones anteriores)
    _, token = servicio.iniciar_sesion("estudiante", "clave-del-entorno-1")
    servicio.asegurar_admin("estudiante", "Administrador", "clave-nueva-del-entorno")
    assert servicio.usuario_de_token(token) is None
    servicio.iniciar_sesion("estudiante", "clave-nueva-del-entorno")


def test_asegurar_admin_reactiva_la_cuenta(servicio):
    admin = servicio.asegurar_admin("estudiante", "Admin", "clave-del-entorno-1")
    admin.activo = False
    servicio.repo.guardar(admin)
    assert servicio.asegurar_admin("estudiante", "Admin", "clave-del-entorno-1").activo is True


def test_no_se_puede_desactivar_al_admin(servicio):
    admin = servicio.asegurar_admin("estudiante", "Admin", "clave-del-entorno-1")
    with pytest.raises(UsuarioInvalido):
        servicio.actualizar_usuario(admin.id, activo=False)


# ----------------------------------------------------------------------------- endurecimiento (P49)
def test_la_contrasena_cambiada_en_la_web_sobrevive_a_los_reinicios(servicio):
    admin = servicio.asegurar_admin("estudiante", "Admin", "clave-del-entorno-1")
    servicio.cambiar_contrasena(admin.id, "clave-del-entorno-1", "clave-elegida-en-la-web")
    # Reinicio con la misma ML_CONTRASENA: no se pisa la contraseña elegida
    servicio.asegurar_admin("estudiante", "Admin", "clave-del-entorno-1")
    servicio.iniciar_sesion("estudiante", "clave-elegida-en-la-web")
    with pytest.raises(CredencialesInvalidas):
        servicio.iniciar_sesion("estudiante", "clave-del-entorno-1")
    # Solo cuando ML_CONTRASENA cambia se restablece (recuperación)
    servicio.asegurar_admin("estudiante", "Admin", "clave-nueva-del-entorno")
    servicio.iniciar_sesion("estudiante", "clave-nueva-del-entorno")


def test_se_puede_desactivar_a_un_admin_si_queda_otro_activo(servicio):
    viejo = servicio.asegurar_admin("antiguo", "Admin", "clave-del-entorno-1")
    nuevo = servicio.asegurar_admin("nuevo", "Admin", "clave-del-entorno-2")  # cambió ML_USUARIO
    servicio.actualizar_usuario(viejo.id, activo=False)
    with pytest.raises(CredencialesInvalidas):
        servicio.iniciar_sesion("antiguo", "clave-del-entorno-1")
    with pytest.raises(UsuarioInvalido):  # el último no
        servicio.actualizar_usuario(nuevo.id, activo=False)


def test_tope_de_fallos_por_cuenta_aunque_cambie_el_origen(servicio):
    servicio.crear_usuario("ana@correo.com", "Ana", CLAVE)
    for i in range(20):
        with pytest.raises(CredencialesInvalidas):
            servicio.iniciar_sesion("ana@correo.com", "mala-clave-123", origen=f"10.0.0.{i}")
    with pytest.raises(DemasiadosIntentos):
        servicio.iniciar_sesion("ana@correo.com", CLAVE, origen="10.9.9.9")  # ni desde otro origen


def test_el_limitador_acota_su_memoria_y_es_seguro_entre_hilos():
    from concurrent.futures import ThreadPoolExecutor

    from modular_learning.core.domain.usuarios import LimitadorIntentos

    limitador = LimitadorIntentos(maximo=5, ventana=900)
    limitador.MAXIMO_CLAVES = 100
    with ThreadPoolExecutor(8) as pool:
        list(pool.map(lambda i: limitador.registrar_fallo(f"clave-{i}", 1.0), range(500)))
    assert len(limitador._fallos) <= 100
    # Con el tiempo las caducadas se podan y vuelve a haber sitio
    limitador.registrar_fallo("nueva", 5_000.0)
    assert "nueva" in limitador._fallos and len(limitador._fallos) == 1
