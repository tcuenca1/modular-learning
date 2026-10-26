import json

import pytest
from fastapi.testclient import TestClient

from modular_learning import bootstrap
from modular_learning.apps.api.dependencies import get_evaluacion_service, get_tutoria_service
from modular_learning.apps.api.main import create_app
from modular_learning.core.application import tutoria as servicio_tutoria
from modular_learning.core.application.evaluacion import EvaluacionService


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # Aísla prompts/ y otros del proyecto real
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))
    return create_app(bootstrap.build_container())


@pytest.fixture
def client(app):
    return TestClient(app)


def test_index_sirve_frontend(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Modular Learning" in r.text


def test_materias_crear_y_listar(client):
    r = client.post("/api/materias", json={"nombre": "Bases de Datos"})
    assert r.status_code == 201
    assert "Bases de Datos" in r.json()["materias"]
    assert "Bases de Datos" in client.get("/api/materias").json()["materias"]


def test_stats_sin_datos(client):
    r = client.get("/api/stats")
    assert r.status_code == 200
    assert r.json()["total_temas"] == 0


def test_quiz_no_expone_respuesta_correcta_y_evalua(app, client):
    preguntas = [
        {"enunciado": "P1", "opciones": ["A) x", "B) y"], "respuesta_correcta": "A) x"},
        {"enunciado": "P2", "opciones": ["A) x", "B) y"], "respuesta_correcta": "B) y"},
    ]

    class EvaluacionFija(EvaluacionService):
        def generar_quiz(self):
            return preguntas

    servicio = EvaluacionFija(llm=None, cronograma_repo=None)  # type: ignore[arg-type]
    app.dependency_overrides[get_evaluacion_service] = lambda: servicio

    q = client.get("/api/quiz/generar").json()
    assert all("respuesta_correcta" not in p for p in q["preguntas"])

    r = client.post(
        "/api/quiz/evaluar", json={"quiz_id": q["quiz_id"], "respuestas": ["A) x", "A) x"]}
    )
    body = r.json()
    assert body["aciertos"] == 1 and body["total"] == 2 and body["porcentaje"] == 50


def test_quiz_sin_temas_completados_devuelve_400(client):
    r = client.get("/api/quiz/generar")
    assert r.status_code == 400


def test_quiz_evaluar_id_invalido(client):
    r = client.post("/api/quiz/evaluar", json={"quiz_id": "nope", "respuestas": []})
    assert r.status_code == 404


def test_plugin_invalido(client):
    assert client.post("/api/plugins/actualizar", json={"seleccion": "Hack"}).status_code == 400


def test_silabo_formato_no_soportado(client):
    r = client.post("/api/silabo/extraer", files={"archivo": ("x.exe", b"abc")})
    assert r.status_code == 400


def test_tutoria_flujo_completo(app, client):
    sesion = servicio_tutoria.SesionTutoria(
        sesion_id="s1",
        materia="Programacion Web",
        tema="HTML",
        nivel_profundidad="INTERMEDIO",
        pasos=[{"titulo": "Paso 1", "descripcion": "d"}],
    )

    class TutoriaFalsa:
        def iniciar_sesion(self, **_):
            return sesion

        def explicar_paso_stream(self, s, i):
            return iter(["Hola ", "mundo"])

        def responder_duda(self, s, i, d):
            return "resp"

        def finalizar_sesion(self, s):
            return {"guia": "# G", "guardado_obsidian": True, "clase_completada": True}

    app.dependency_overrides[get_tutoria_service] = TutoriaFalsa

    r = client.post(
        "/api/tutoria/iniciar", json={"materia": "Programacion Web", "tema": "HTML"}
    ).json()
    sid = r["sesion_id"]
    assert r["pasos"][0]["titulo"] == "Paso 1"

    with client.stream("GET", f"/api/tutoria/{sid}/paso/0/stream") as s:
        texto = "".join(s.iter_text())
    chunks = [
        json.loads(linea[6:])["chunk"]
        for linea in texto.splitlines()
        if linea.startswith('data: {"chunk')
    ]
    assert "".join(chunks) == "Hola mundo"
    assert "event: fin" in texto

    assert client.post(f"/api/tutoria/{sid}/duda", json={"paso": 0, "duda": "?"}).json() == {
        "respuesta": "resp"
    }
    assert client.post(f"/api/tutoria/{sid}/finalizar").json()["clase_completada"] is True
    assert client.post(f"/api/tutoria/{sid}/finalizar").status_code == 404


def test_normalizar_roadmap_tolerante():
    pasos = servicio_tutoria.normalizar_roadmap(
        {" pasos ": [{"Title": "A", "description": "d"}, "B"]}
    )
    assert pasos == [{"titulo": "A", "descripcion": "d"}, {"titulo": "B", "descripcion": ""}]
    with pytest.raises(ValueError):
        servicio_tutoria.normalizar_roadmap({})


def test_config_obtener_y_guardar(client, tmp_path):
    res_get = client.get("/api/config")
    assert res_get.status_code == 200
    assert "carpeta_material" in res_get.json()

    carpeta_estudio = tmp_path / "MiUniversidad"
    carpeta_estudio.mkdir()
    boveda_obsidian = tmp_path / "Boveda"

    res_post = client.post(
        "/api/config",
        json={"carpeta_material": str(carpeta_estudio), "ruta_obsidian": str(boveda_obsidian)},
    )
    assert res_post.status_code == 200
    assert res_post.json()["carpeta_material_existe"] is True


def test_escanear_material_endpoint(client, tmp_path):
    carpeta_estudio = tmp_path / "Uni"
    materia_dir = carpeta_estudio / "Seguridad"
    materia_dir.mkdir(parents=True)
    (materia_dir / "tema1.txt").write_text("contenido", encoding="utf-8")

    res_config = client.post(
        "/api/config",
        json={"carpeta_material": str(carpeta_estudio), "ruta_obsidian": str(tmp_path / "Boveda")},
    )
    assert res_config.status_code == 200

    res = client.get("/api/material/escanear?materia=Seguridad")
    assert res.status_code == 200
    escaneos = res.json()["escaneos"]
    assert len(escaneos) == 1
    assert escaneos[0]["materia"] == "Seguridad"
    assert len(escaneos[0]["pendientes"]) == 1


def test_motor_evaluacion_mezclar_opciones():
    from modular_learning.core.application.evaluacion import mezclar_opciones

    pregunta = {
        "enunciado": "¿Qué es X?",
        "opciones": [
            "A) Corta",
            "B) Esta es la opcion super larga y detallada",
            "C) Media",
            "D) Otra",
        ],
        "respuesta_correcta": "B) Esta es la opcion super larga y detallada",
    }
    mezclada = mezclar_opciones(pregunta)
    assert len(mezclada["opciones"]) == 4
    # La respuesta correcta debe estar entre las opciones y tener prefijo A-D
    assert mezclada["respuesta_correcta"] in mezclada["opciones"]
    assert any("Esta es la opcion super larga" in o for o in mezclada["opciones"])


def test_repaso_espaciado_por_api(app, client):
    preguntas = [
        {
            "enunciado": "P1",
            "opciones": ["A) x", "B) y"],
            "respuesta_correcta": "A) x",
            "materia": "Redes",
            "tema": "VLAN",
            "explicacion": "Porque x.",
        }
    ]

    class EvaluacionFija(EvaluacionService):
        def generar_quiz(self):
            return preguntas

    contenedor = app.state.container
    servicio = EvaluacionFija(
        llm=None,  # type: ignore[arg-type]
        cronograma_repo=contenedor.cronograma_repo,
        repaso=contenedor.repaso_service,
    )
    app.dependency_overrides[get_evaluacion_service] = lambda: servicio

    assert client.get("/api/repaso/resumen").json() == {
        "pendientes_hoy": 0,
        "total": 0,
        "dominadas": 0,
    }
    assert client.get("/api/repaso/pendientes").status_code == 404

    q = client.get("/api/quiz/generar").json()
    assert q["preguntas"][0]["tema"] == "VLAN"
    assert "respuesta_correcta" not in q["preguntas"][0]
    r = client.post(
        "/api/quiz/evaluar", json={"quiz_id": q["quiz_id"], "respuestas": ["B) y"]}
    ).json()
    assert r["detalle"][0]["explicacion"] == "Porque x."

    assert client.get("/api/repaso/resumen").json()["total"] == 1
    eventos = client.get("/api/repaso/historial", params={"materia": "Redes"}).json()["eventos"]
    assert eventos[0]["falladas"] == ["P1"]


def test_cronogramas_para_calendario(client, tmp_path):
    import json as _json

    carpeta = tmp_path / "data" / "schedules"
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "Redes_cronograma.json").write_text(
        _json.dumps({"clases": [{"fecha": "27/10/2026", "tema": "VLAN"}]}), encoding="utf-8"
    )
    datos = client.get("/api/materias/cronogramas").json()["cronogramas"]
    assert datos == {"Redes": [{"fecha": "27/10/2026", "tema": "VLAN"}]}


def test_guia_offline_flujo_completo(app, client, tmp_path):
    from modular_learning.apps.api.dependencies import get_guias_service
    from modular_learning.core.application.guias import GuiaOfflineService
    from modular_learning.core.domain.guia_offline import MARCADOR_RESPUESTAS
    from modular_learning.infrastructure.persistence.json_guias import JsonGuiasRepo
    from tests.unit.application.fake_adapters import (
        FakeLLM,
        InMemoryCronogramaRepo,
        InMemoryLectorDocumentosPort,
    )

    cronograma = InMemoryCronogramaRepo(
        {"Redes": [{"tema": "VLAN", "estado": "pendiente"}, {"tema": "STP", "estado": "pendiente"}]}
    )
    servicio = GuiaOfflineService(
        llm=FakeLLM(texto_default=f"## Explicación\nx\n{MARCADOR_RESPUESTAS}\n1. y"),
        cronograma_repo=cronograma,
        lector_docs=InMemoryLectorDocumentosPort(),
        guias_repo=JsonGuiasRepo(str(tmp_path / "guias.json")),
    )
    app.dependency_overrides[get_guias_service] = lambda: servicio

    assert client.post("/api/guias", json={"materia": "Redes", "temas": ["X"]}).status_code == 400
    guia = client.post("/api/guias", json={"materia": "Redes", "temas": ["VLAN", "STP"]}).json()
    assert guia["completa"] is False and len(guia["clases"]) == 2

    for i in range(2):
        clase = client.post(f"/api/guias/{guia['id']}/clases/{i}").json()
        assert clase["respuestas"] == "1. y"
    pendientes = client.get("/api/guias/pendientes").json()["guias"]
    assert [g["id"] for g in pendientes] == [guia["id"]]
    assert client.get(f"/api/guias/{guia['id']}").json()["clases"][1]["contenido"]

    r = client.post(
        f"/api/guias/{guia['id']}/revision",
        json={
            "resultados": [
                {"indice": 0, "resultado": "entendida"},
                {"indice": 1, "resultado": "pendiente"},
            ]
        },
    )
    assert r.json()["completadas"] == ["VLAN"]
    assert client.get("/api/guias/pendientes").json()["guias"] == []
    assert client.get("/api/guias/nope").status_code == 404


def test_acceso_desactivado_en_local(client, monkeypatch):
    monkeypatch.delenv("ML_REQUIERE_ACCESO", raising=False)
    assert client.get("/api/materias").status_code == 200
    assert client.get("/api/salud").json() == {"ok": True}


def _cliente_con_acceso(tmp_path, monkeypatch, contrasena):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("ML_REQUIERE_ACCESO", "1")
    monkeypatch.setenv("ML_USUARIO", "ana")
    monkeypatch.setenv("ML_CONTRASENA", contrasena)
    return TestClient(create_app(bootstrap.build_container()))


def test_acceso_exige_usuario_y_contrasena(tmp_path, monkeypatch):
    client = _cliente_con_acceso(tmp_path, monkeypatch, "clave-larga")

    r = client.get("/api/materias")
    assert r.status_code == 401 and "Basic" in r.headers["www-authenticate"]
    assert client.get("/", auth=("ana", "otra")).status_code == 401
    assert client.get("/api/materias", auth=("ana", "clave-larga")).status_code == 200
    assert client.get("/api/salud").status_code == 200


def test_acceso_sin_contrasena_configurada_no_queda_abierto(tmp_path, monkeypatch):
    client = _cliente_con_acceso(tmp_path, monkeypatch, "")
    assert client.get("/api/materias", auth=("ana", "")).status_code == 503
    assert client.get("/api/salud").status_code == 200
