"""Login por cuentas: sesión, aislamiento de datos entre usuarios y administración."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from modular_learning import bootstrap
from modular_learning.apps.api.main import create_app

ADMIN, CLAVE_ADMIN = "estudiante", "clave-del-administrador-1"
ANA, CLAVE_ANA = "ana@correo.com", "clave-de-ana-12345"


def _crear_cliente(https: bool = False) -> TestClient:
    url = "https://testserver" if https else "http://testserver"
    cliente = TestClient(create_app(bootstrap.build_container()), base_url=url)
    cliente.__enter__()  # ejecuta el arranque: crea la cuenta de administrador
    return cliente


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("ML_REQUIERE_ACCESO", "1")
    monkeypatch.setenv("ML_USUARIO", ADMIN)
    monkeypatch.setenv("ML_CONTRASENA", CLAVE_ADMIN)
    return tmp_path


@pytest.fixture
def cliente(entorno):
    c = _crear_cliente()
    yield c
    c.__exit__(None, None, None)


def entrar(cliente: TestClient, correo: str, clave: str):
    return cliente.post("/api/auth/login", json={"correo": correo, "contrasena": clave})


def cliente_de(correo: str, clave: str) -> TestClient:
    """Un navegador distinto (cookies propias) ya con la sesión iniciada."""
    c = _crear_cliente()
    assert entrar(c, correo, clave).status_code == 200
    return c


# ----------------------------------------------------------------------------- sesión
def test_sin_sesion_la_api_responde_401_pero_la_web_y_la_salud_son_publicas(cliente):
    r = cliente.get("/api/materias")
    assert r.status_code == 401 and r.json() == {"detail": "Inicia sesión para continuar."}
    assert (
        cliente.post("/api/tutoria/iniciar", json={"materia": "x", "tema": "y"}).status_code == 401
    )
    assert cliente.get("/api/salud").status_code == 200
    assert cliente.get("/").status_code == 200
    assert cliente.get("/ajustes").status_code == 200  # ruta de la SPA


def test_yo_informa_si_hay_login_y_quien_es(cliente):
    assert cliente.get("/api/auth/yo").json() == {"autenticacion": True, "usuario": None}
    entrar(cliente, ADMIN, CLAVE_ADMIN)
    usuario = cliente.get("/api/auth/yo").json()["usuario"]
    assert usuario["correo"] == ADMIN and usuario["es_admin"] is True
    assert "hash_contrasena" not in usuario


def test_login_correcto_pone_una_cookie_httponly_y_da_acceso(cliente):
    r = entrar(cliente, "  ESTUDIANTE ", CLAVE_ADMIN)
    assert r.status_code == 200 and r.json()["usuario"]["correo"] == ADMIN
    cookie = r.headers["set-cookie"].lower()
    assert "ml_sesion=" in cookie and "httponly" in cookie and "samesite=lax" in cookie
    assert "secure" not in cookie  # solo en la nube (HTTPS)
    assert cliente.get("/api/materias").status_code == 200


def test_login_incorrecto_da_401_sin_decir_que_fallo(cliente):
    for correo, clave in [(ADMIN, "mala-clave-123"), ("nadie@x.com", CLAVE_ADMIN)]:
        r = entrar(cliente, correo, clave)
        assert r.status_code == 401
        assert r.json() == {"detail": "Correo o contraseña incorrectos."}
    assert cliente.get("/api/materias").status_code == 401


def test_cinco_fallos_bloquean_con_429(cliente):
    for _ in range(5):
        assert entrar(cliente, ADMIN, "mala-clave-123").status_code == 401
    r = entrar(cliente, ADMIN, CLAVE_ADMIN)  # ni la buena
    assert r.status_code == 429 and int(r.headers["retry-after"]) > 0


def test_logout_cierra_la_sesion(cliente):
    entrar(cliente, ADMIN, CLAVE_ADMIN)
    assert cliente.post("/api/auth/logout").json() == {"ok": True}
    assert cliente.get("/api/materias").status_code == 401


def test_cookie_manipulada_no_vale(cliente):
    entrar(cliente, ADMIN, CLAVE_ADMIN)
    token = cliente.cookies["ml_sesion"]
    medio = len(token) // 3
    cambiado = "A" if token[medio] != "A" else "B"
    cliente.cookies.clear()
    cliente.cookies.set("ml_sesion", token[:medio] + cambiado + token[medio + 1 :])
    assert cliente.get("/api/materias").status_code == 401


def test_cookie_secure_en_la_nube(entorno, monkeypatch):
    monkeypatch.setenv("ML_EN_NUBE", "1")
    monkeypatch.setenv("ML_HOSTS_PERMITIDOS", "testserver")
    c = _crear_cliente()
    r = entrar(c, ADMIN, CLAVE_ADMIN)
    assert "secure" in r.headers["set-cookie"].lower()


def test_sin_contrasena_de_administrador_la_api_no_queda_abierta(entorno, monkeypatch):
    monkeypatch.setenv("ML_CONTRASENA", "")
    c = _crear_cliente()
    assert c.get("/api/materias").status_code == 503
    assert c.get("/api/salud").status_code == 200


def test_sin_login_activo_todo_sigue_abierto_como_en_local(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("ML_REQUIERE_ACCESO", raising=False)
    c = TestClient(create_app(bootstrap.build_container()))
    assert c.get("/api/materias").status_code == 200
    assert c.get("/api/auth/yo").json() == {"autenticacion": False, "usuario": None}
    assert c.post("/api/auth/login", json={"correo": "a", "contrasena": "b"}).status_code == 404


# ----------------------------------------------------------------------------- administración
def _admin(entorno) -> TestClient:
    return cliente_de(ADMIN, CLAVE_ADMIN)


def test_el_admin_crea_lista_y_los_demas_no_pueden(entorno):
    admin = _admin(entorno)
    r = admin.post(
        "/api/auth/usuarios", json={"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA}
    )
    assert r.status_code == 201 and r.json()["usuario"]["es_admin"] is False
    assert {u["correo"] for u in admin.get("/api/auth/usuarios").json()["usuarios"]} == {ADMIN, ANA}

    ana = cliente_de(ANA, CLAVE_ANA)
    assert ana.get("/api/auth/usuarios").status_code == 403
    assert (
        ana.post(
            "/api/auth/usuarios", json={"correo": "b@x.com", "nombre": "B", "contrasena": CLAVE_ANA}
        ).status_code
        == 403
    )
    assert ana.patch("/api/auth/usuarios/x", json={"activo": False}).status_code == 403


def test_alta_con_datos_invalidos_o_duplicados(entorno):
    admin = _admin(entorno)
    cuerpo = {"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA}
    assert admin.post("/api/auth/usuarios", json=cuerpo).status_code == 201
    assert (
        admin.post("/api/auth/usuarios", json={**cuerpo, "correo": "ANA@correo.com"}).status_code
        == 409
    )
    assert admin.post("/api/auth/usuarios", json={**cuerpo, "correo": "malo"}).status_code == 422
    assert (
        admin.post(
            "/api/auth/usuarios", json={**cuerpo, "correo": "b@x.com", "contrasena": "corta"}
        ).status_code
        == 422
    )


def test_desactivar_cierra_la_sesion_y_reactivar_permite_volver(entorno):
    admin = _admin(entorno)
    ana_id = admin.post(
        "/api/auth/usuarios", json={"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA}
    ).json()["usuario"]["id"]
    ana = cliente_de(ANA, CLAVE_ANA)
    assert ana.get("/api/materias").status_code == 200

    assert admin.patch(f"/api/auth/usuarios/{ana_id}", json={"activo": False}).status_code == 200
    assert ana.get("/api/materias").status_code == 401
    assert entrar(_crear_cliente(), ANA, CLAVE_ANA).status_code == 401
    assert admin.patch(f"/api/auth/usuarios/{ana_id}", json={"activo": True}).status_code == 200
    assert entrar(_crear_cliente(), ANA, CLAVE_ANA).status_code == 200


def test_el_admin_no_puede_desactivarse_y_los_ids_inexistentes_dan_404(entorno):
    admin = _admin(entorno)
    mi_id = admin.get("/api/auth/yo").json()["usuario"]["id"]
    assert admin.patch(f"/api/auth/usuarios/{mi_id}", json={"activo": False}).status_code == 422
    assert admin.patch("/api/auth/usuarios/no-existe", json={"activo": False}).status_code == 404


def test_restablecer_la_contrasena_de_otra_cuenta(entorno):
    admin = _admin(entorno)
    ana_id = admin.post(
        "/api/auth/usuarios", json={"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA}
    ).json()["usuario"]["id"]
    admin.patch(f"/api/auth/usuarios/{ana_id}", json={"contrasena": "restablecida-12345"})
    assert entrar(_crear_cliente(), ANA, CLAVE_ANA).status_code == 401
    assert entrar(_crear_cliente(), ANA, "restablecida-12345").status_code == 200


def test_cambiar_la_propia_contrasena(entorno):
    admin = _admin(entorno)
    admin.post("/api/auth/usuarios", json={"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA})
    ana, otra_sesion = cliente_de(ANA, CLAVE_ANA), cliente_de(ANA, CLAVE_ANA)

    assert (
        ana.post(
            "/api/auth/contrasena", json={"actual": "no-es-12345", "nueva": "nueva-clave-12345"}
        ).status_code
        == 401
    )
    assert (
        ana.post("/api/auth/contrasena", json={"actual": CLAVE_ANA, "nueva": "corta"}).status_code
        == 422
    )
    assert ana.post(
        "/api/auth/contrasena", json={"actual": CLAVE_ANA, "nueva": "nueva-clave-12345"}
    ).json() == {"ok": True}
    assert ana.get("/api/materias").status_code == 200  # la sesión actual se renueva
    assert otra_sesion.get("/api/materias").status_code == 401  # las demás se invalidan
    assert entrar(_crear_cliente(), ANA, "nueva-clave-12345").status_code == 200


def test_cambiar_ml_contrasena_recupera_el_acceso_del_admin(entorno, monkeypatch):
    viejo = _admin(entorno)
    monkeypatch.setenv("ML_CONTRASENA", "contraseña-nueva-del-entorno")
    assert entrar(_crear_cliente(), ADMIN, "contraseña-nueva-del-entorno").status_code == 200
    assert entrar(_crear_cliente(), ADMIN, CLAVE_ADMIN).status_code == 401
    assert viejo.get("/api/materias").status_code == 401


# ----------------------------------------------------------------------------- aislamiento
def test_cada_cuenta_ve_solo_sus_datos(entorno):
    admin = _admin(entorno)
    admin.post("/api/auth/usuarios", json={"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA})
    ana = cliente_de(ANA, CLAVE_ANA)

    assert admin.post("/api/materias", json={"nombre": "Solo del admin"}).status_code == 201
    assert ana.post("/api/materias", json={"nombre": "Solo de Ana"}).status_code == 201
    ana.post("/api/materias/solo-de-ana/clases", json={"tema": "Tema de Ana"})

    nombres_admin = admin.get("/api/materias").json()["materias"]
    nombres_ana = ana.get("/api/materias").json()["materias"]
    assert "Solo del admin" in nombres_admin and "Solo de Ana" not in nombres_admin
    assert "Solo de Ana" in nombres_ana and "Solo del admin" not in nombres_ana
    assert admin.get("/api/materias/solo-de-ana/cronograma").json() == {"clases": []}
    assert [
        c["tema"] for c in ana.get("/api/materias/solo-de-ana/cronograma").json()["clases"]
    ] == ["Tema de Ana"]
    assert "solo-de-ana" not in admin.get("/api/materias/cronogramas").json()["cronogramas"]


def test_los_datos_se_guardan_bajo_el_prefijo_de_la_cuenta(entorno):
    admin = _admin(entorno)
    admin.post("/api/materias", json={"nombre": "Redes"})
    admin_id = admin.get("/api/auth/yo").json()["usuario"]["id"]
    assert (entorno / "data" / "cuentas" / admin_id / "config" / "materias.json").is_file()
    assert not (entorno / "data" / "config" / "materias.json").exists()


def test_la_sesion_de_tutoria_de_una_cuenta_no_la_usa_otra(entorno):
    from modular_learning.apps.api.session_store import SessionStore
    from modular_learning.infrastructure.persistence.almacen import en_cuenta

    store = SessionStore()
    with en_cuenta("aaaa"):
        store.guardar_sesion("s1", object())  # type: ignore[arg-type]
        store.guardar_quiz("q1", [{"p": 1}])
        assert store.obtener_sesion("s1") is not None
    with en_cuenta("bbbb"):
        assert store.obtener_sesion("s1") is None
        assert store.obtener_quiz("q1") is None
        assert store.eliminar_sesion("s1") is None
    with en_cuenta("aaaa"):
        assert store.obtener_quiz("q1") == [{"p": 1}]


def test_sin_cuenta_activa_el_almacen_se_niega_a_servir_datos(entorno):
    from modular_learning.infrastructure.persistence.almacen import almacen_por_defecto

    with pytest.raises(PermissionError):
        almacen_por_defecto()


def test_la_boveda_del_servidor_es_una_subcarpeta_por_cuenta(entorno):
    from modular_learning.infrastructure.persistence.almacen import en_cuenta
    from modular_learning.infrastructure.persistence.json_ajustes import JsonAjustesRepo

    ajustes = JsonAjustesRepo()
    with en_cuenta("aaaa"):
        a = ajustes.ruta_boveda()
    with en_cuenta("bbbb"):
        b = ajustes.ruta_boveda()
    assert a != b and a.endswith(os.path.join("obsidian_vault", "aaaa"))


def test_config_no_se_puede_cambiar_en_la_nube(entorno, monkeypatch):
    monkeypatch.setenv("ML_EN_NUBE", "1")
    monkeypatch.setenv("ML_HOSTS_PERMITIDOS", "testserver")
    c = _crear_cliente(https=True)  # la cookie Secure solo viaja por HTTPS
    entrar(c, ADMIN, CLAVE_ADMIN)
    r = c.post("/api/config", json={"carpeta_material": "/tmp", "ruta_obsidian": "/tmp/b"})
    assert r.status_code == 403


# ----------------------------------------------------------------------------- datos de ejemplo
def test_el_admin_arranca_con_datos_de_ejemplo_y_los_demas_vacios(entorno, monkeypatch):
    semilla = entorno / "semilla"
    (semilla / "schedules").mkdir(parents=True)
    (semilla / "schedules" / "EJEMPLO_ASIGNATURA_cronograma.json").write_text(
        '{"clases": [{"tema": "Tema 1", "estado": "pendiente"}]}', encoding="utf-8"
    )
    (semilla / "README.md").write_text("no se copia", encoding="utf-8")
    monkeypatch.setenv("ML_SEMBRAR_EJEMPLOS", "1")
    monkeypatch.setenv("ML_SEMILLA_DIR", str(semilla))

    admin = _admin(entorno)
    assert "Ejemplo Asignatura" in admin.get("/api/materias").json()["materias"]
    assert [
        c["tema"] for c in admin.get("/api/materias/ejemplo-asignatura/cronograma").json()["clases"]
    ] == ["Tema 1"]

    admin.post("/api/auth/usuarios", json={"correo": ANA, "nombre": "Ana", "contrasena": CLAVE_ANA})
    ana = cliente_de(ANA, CLAVE_ANA)
    assert ana.get("/api/materias").json()["materias"] == []  # sin ejemplos ni asignaturas ajenas

    # Reiniciar el servidor no vuelve a sembrar ni pisa lo que el admin hizo
    admin.post("/api/materias/ejemplo-asignatura/clases", json={"tema": "Tema propio"})
    otra = cliente_de(ADMIN, CLAVE_ADMIN)
    assert len(otra.get("/api/materias/ejemplo-asignatura/cronograma").json()["clases"]) == 2


# ----------------------------------------------------------------------------- endurecimiento (P49)
def test_el_secreto_de_sesion_es_aleatorio_persistente_y_no_depende_de_la_contrasena(
    entorno, monkeypatch
):
    monkeypatch.delenv("ML_SECRETO_SESION", raising=False)
    primero = _crear_cliente()
    entrar(primero, ADMIN, CLAVE_ADMIN)
    guardado = (entorno / "data" / "auth" / "secreto.json").read_text(encoding="utf-8")
    assert "secreto" in guardado and CLAVE_ADMIN not in guardado
    # Un reinicio (otra app) reutiliza el secreto: la sesión sigue valiendo
    segundo = _crear_cliente()
    segundo.cookies.set("ml_sesion", primero.cookies["ml_sesion"])
    assert segundo.get("/api/materias").status_code == 200


def test_secreto_explicito_por_variable_de_entorno(entorno, monkeypatch):
    monkeypatch.setenv("ML_SECRETO_SESION", "x" * 40)
    c = _crear_cliente()
    entrar(c, ADMIN, CLAVE_ADMIN)
    assert not (entorno / "data" / "auth" / "secreto.json").exists()


def test_la_contrasena_del_admin_cambiada_en_la_web_sobrevive_a_un_reinicio(entorno):
    admin = _admin(entorno)
    assert (
        admin.post(
            "/api/auth/contrasena", json={"actual": CLAVE_ADMIN, "nueva": "elegida-en-la-web-12"}
        ).status_code
        == 200
    )
    # Reinicio del servidor con la misma ML_CONTRASENA del entorno
    assert entrar(_crear_cliente(), ADMIN, "elegida-en-la-web-12").status_code == 200
    assert entrar(_crear_cliente(), ADMIN, CLAVE_ADMIN).status_code == 401


def test_config_no_se_cambia_con_login_aunque_no_sea_la_nube(entorno):
    admin = _admin(entorno)
    r = admin.post("/api/config", json={"carpeta_material": "/tmp", "ruta_obsidian": "/tmp/b"})
    assert r.status_code == 403


def test_si_ml_contrasena_es_corta_el_login_explica_que_falta_la_cuenta(entorno, monkeypatch):
    monkeypatch.setenv(
        "ML_CONTRASENA", "corta"
    )  # menos de 10 caracteres: no se puede crear el admin
    c = _crear_cliente()
    r = entrar(c, ADMIN, "corta")
    assert r.status_code == 503
    assert "ML_CONTRASENA" in r.json()["detail"] and "10 caracteres" in r.json()["detail"]
    assert c.get("/api/salud").status_code == 200  # el servicio sigue vivo
