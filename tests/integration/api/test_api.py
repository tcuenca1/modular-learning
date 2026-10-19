import json

import pytest
from fastapi.testclient import TestClient

from modular_learning.core.application import tutoria as servicio_tutoria
from modular_learning.apps.api import main as web_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # Aísla prompts/ y otros del proyecto real
    monkeypatch.setenv("ML_DATA_DIR", str(tmp_path / "data"))
    web_app.SESIONES.clear()
    web_app.QUIZZES.clear()
    return TestClient(web_app.app)


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


def test_quiz_no_expone_respuesta_correcta_y_evalua(client, monkeypatch):
    preguntas = [
        {"enunciado": "P1", "opciones": ["A) x", "B) y"], "respuesta_correcta": "A) x"},
        {"enunciado": "P2", "opciones": ["A) x", "B) y"], "respuesta_correcta": "B) y"},
    ]
    monkeypatch.setattr(web_app.motor_evaluacion, "generar_quiz", lambda: preguntas)

    q = client.get("/api/quiz/generar").json()
    assert all("respuesta_correcta" not in p for p in q["preguntas"])

    r = client.post("/api/quiz/evaluar", json={"quiz_id": q["quiz_id"], "respuestas": ["A) x", "A) x"]})
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


def test_tutoria_flujo_completo(client, monkeypatch):
    sesion = servicio_tutoria.SesionTutoria(
        sesion_id="s1",
        materia="Programacion Web",
        tema="HTML",
        nivel_profundidad="INTERMEDIO",
        pasos=[{"titulo": "Paso 1", "descripcion": "d"}],
    )
    monkeypatch.setattr(web_app.servicio_tutoria, "iniciar_sesion", lambda *a, **k: sesion)
    monkeypatch.setattr(
        web_app.servicio_tutoria, "explicar_paso_stream", lambda s, i: iter(["Hola ", "mundo"])
    )
    monkeypatch.setattr(web_app.servicio_tutoria, "responder_duda", lambda s, i, d: "resp")
    monkeypatch.setattr(
        web_app.servicio_tutoria,
        "finalizar_sesion",
        lambda s: {"guia": "# G", "guardado_obsidian": True, "clase_completada": True},
    )

    r = client.post(
        "/api/tutoria/iniciar", json={"materia": "Programacion Web", "tema": "HTML"}
    ).json()
    sid = r["sesion_id"]
    assert r["pasos"][0]["titulo"] == "Paso 1"

    with client.stream("GET", f"/api/tutoria/{sid}/paso/0/stream") as s:
        texto = "".join(s.iter_text())
    chunks = [
        json.loads(linea[6:])["chunk"] for linea in texto.splitlines() if linea.startswith("data: {\"chunk")
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


def test_escanear_material_endpoint(client, tmp_path, monkeypatch):
    carpeta_estudio = tmp_path / "Uni"
    materia_dir = carpeta_estudio / "Seguridad"
    materia_dir.mkdir(parents=True)
    (materia_dir / "tema1.txt").write_text("contenido", encoding="utf-8")

    monkeypatch.setattr(
        web_app.servicio_config, "carpeta_material", lambda: str(carpeta_estudio)
    )
    monkeypatch.setattr(web_app.gestor_archivos, "cargar_materias", lambda: ["Seguridad"])

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
        "opciones": ["A) Corta", "B) Esta es la opcion super larga y detallada", "C) Media", "D) Otra"],
        "respuesta_correcta": "B) Esta es la opcion super larga y detallada",
    }
    mezclada = mezclar_opciones(pregunta)
    assert len(mezclada["opciones"]) == 4
    # La respuesta correcta debe estar entre las opciones y tener prefijo A-D
    assert mezclada["respuesta_correcta"] in mezclada["opciones"]
    assert any("Esta es la opcion super larga" in o for o in mezclada["opciones"])

