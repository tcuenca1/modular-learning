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


def test_eliminar_cronograma_conserva_materia(client):
    # Crear materia Redes
    r_mat = client.post("/api/materias", json={"nombre": "Redes"})
    assert r_mat.status_code == 201

    # Añadir clase
    r_clase = client.post("/api/materias/redes/clases", json={"tema": "Enrutamiento IP"})
    assert r_clase.status_code == 201

    # Verificar que el cronograma tiene la clase
    r_crono_antes = client.get("/api/materias/redes/cronograma")
    assert r_crono_antes.status_code == 200
    assert len(r_crono_antes.json()["clases"]) == 1

    # Eliminar/vaciar cronograma
    r_del = client.delete("/api/materias/redes/cronograma")
    assert r_del.status_code == 200

    # GET /api/materias sigue incluyendo "Redes"
    materias = client.get("/api/materias").json()["materias"]
    assert "Redes" in materias

    # GET /api/materias/redes/cronograma devuelve {"clases": []}
    r_crono_despues = client.get("/api/materias/redes/cronograma")
    assert r_crono_despues.status_code == 200
    assert r_crono_despues.json() == {"clases": []}


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


def test_plugins_listar_y_configurar(client, tmp_path):
    # Listar plugins
    res_list = client.get("/api/plugins")
    assert res_list.status_code == 200
    datos = res_list.json()
    assert "opciones" in datos
    assert "plugins" in datos
    assert any(p["id"] == "cisco" for p in datos["plugins"])

    # Configurar carpeta y materia para cisco (la carpeta debe estar dentro del material)
    client.post(
        "/api/config",
        json={"carpeta_material": str(tmp_path), "ruta_obsidian": str(tmp_path / "Boveda")},
    )
    carpeta_redes = str(tmp_path / "redes_lab")
    res_cfg = client.post(
        "/api/plugins/config",
        json={"clave": "cisco", "carpeta": carpeta_redes, "materia": "conmutacion-avanzada"},
    )
    assert res_cfg.status_code == 200
    cfg_data = res_cfg.json()
    assert cfg_data["ok"] is True
    assert cfg_data["config"]["carpeta"] == carpeta_redes
    assert cfg_data["config"]["materia"] == "conmutacion-avanzada"


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


def test_config_en_nube_con_variable(client, monkeypatch):
    monkeypatch.delenv("ML_EN_NUBE", raising=False)
    res = client.get("/api/config")
    assert res.status_code == 200
    assert res.json()["en_nube"] is False

    monkeypatch.setenv("ML_EN_NUBE", "1")
    res = client.get("/api/config")
    assert res.status_code == 200
    assert res.json()["en_nube"] is True

    monkeypatch.setenv("ML_EN_NUBE", "0")
    res = client.get("/api/config")
    assert res.status_code == 200
    assert res.json()["en_nube"] is False


def test_escanear_material_endpoint(client, tmp_path, monkeypatch):
    carpeta_estudio = tmp_path / "Uni"
    materia_dir = carpeta_estudio / "Seguridad"
    materia_dir.mkdir(parents=True)
    (materia_dir / "tema1.txt").write_text("contenido", encoding="utf-8")

    res_config = client.post(
        "/api/config",
        json={"carpeta_material": str(carpeta_estudio), "ruta_obsidian": str(tmp_path / "Boveda")},
    )
    assert res_config.status_code == 200
    assert client.post("/api/materias", json={"nombre": "Seguridad"}).status_code == 201

    res = client.get("/api/material/escanear?materia=Seguridad")
    assert res.status_code == 200
    escaneos = res.json()["escaneos"]
    assert len(escaneos) == 1
    assert escaneos[0]["materia"] == "Seguridad"
    assert len(escaneos[0]["pendientes"]) == 1

    # Con ML_EN_NUBE=1, los escaneos responden vacío
    monkeypatch.setenv("ML_EN_NUBE", "1")
    res_nube = client.get("/api/material/escanear?materia=Seguridad")
    assert res_nube.status_code == 200
    assert res_nube.json()["escaneos"] == []

    res_proy_nube = client.get("/api/proyectos/escanear?materia=Seguridad")
    assert res_proy_nube.status_code == 200
    assert res_proy_nube.json()["candidatos"] == []


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
    assert datos == {"redes": [{"fecha": "27/10/2026", "tema": "VLAN"}]}


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


def test_proyectos_endpoints(client, tmp_path):
    proy_dir = tmp_path / "sgsi_proyecto"
    proy_dir.mkdir()
    (proy_dir / "01_normativa.txt").write_text("politica de seguridad", encoding="utf-8")

    client.post(
        "/api/config",
        json={"carpeta_material": str(tmp_path), "ruta_obsidian": str(tmp_path / "Boveda")},
    )

    # Listar inicialmente
    r_list = client.get("/api/proyectos")
    assert r_list.status_code == 200
    assert "proyectos" in r_list.json()

    # Ingestar proyecto
    r_ing = client.post(
        "/api/proyectos/ingestar",
        json={
            "materia": "Seguridad de la Informacion",
            "nombre": "sgsi_proyecto",
            "parcial": "general",
            "ruta": str(proy_dir),
            "tipo": "documental_auditoria",
        },
    )
    assert r_ing.status_code == 200
    proy = r_ing.json()["proyecto"]
    p_id = proy["id"]

    # Consultar proyecto y estado
    r_get = client.get(f"/api/proyectos/{p_id}")
    assert r_get.status_code == 200
    assert r_get.json()["proyecto"]["nombre"] == "sgsi_proyecto"

    r_est = client.get(f"/api/proyectos/{p_id}/estado")
    assert r_est.status_code == 200
    assert r_est.json()["estado"] == "al_dia"

    # Actualizar proyecto
    r_act = client.post(f"/api/proyectos/{p_id}/actualizar")
    assert r_act.status_code == 200

    # Vaciar materiales y proyectos
    r_vac = client.post("/api/material/vaciar", json={"borrar_notas_obsidian": False})
    assert r_vac.status_code == 200
    assert r_vac.json()["ok"] is True


@pytest.mark.parametrize("nombre", ["   ", "!!!", "😀", "a/b", "..", "x" * 81])
def test_crear_materia_nombre_invalido_422(client, nombre):
    antes = client.get("/api/materias").json()["catalogo"]
    r = client.post("/api/materias", json={"nombre": nombre})
    assert r.status_code == 422
    assert isinstance(r.json()["detail"], str)
    assert client.get("/api/materias").json()["catalogo"] == antes


def test_crear_materia_duplicada_409(client):
    assert client.post("/api/materias", json={"nombre": "Bases de Datos"}).status_code == 201
    r = client.post("/api/materias", json={"nombre": "bases DE datos"})
    assert r.status_code == 409
    nombres = client.get("/api/materias").json()["materias"]
    assert nombres.count("Bases de Datos") == 1


def test_materia_inexistente_da_404_en_put_clases_y_parciales(client):
    assert client.put("/api/materias/fantasma", json={"nombre": "Fantasma"}).status_code == 404
    assert client.post("/api/materias/fantasma/clases", json={"tema": "T"}).status_code == 404
    r = client.post("/api/materias/fantasma/parciales", json={"parciales": []})
    assert r.status_code == 404
    assert client.get("/api/materias/cronogramas").json()["cronogramas"].get("fantasma") is None
    assert "fantasma" not in [m["slug"] for m in client.get("/api/materias").json()["catalogo"]]


def _preparar_material(client, tmp_path):
    uni = tmp_path / "Uni"
    (uni / "Redes").mkdir(parents=True)
    (uni / "Redes" / "tema1.txt").write_text("contenido", encoding="utf-8")
    fuera = tmp_path / "fuera"
    (fuera / "proy").mkdir(parents=True)
    (fuera / "secreto.txt").write_text("no debe salir", encoding="utf-8")
    r = client.post(
        "/api/config",
        json={"carpeta_material": str(uni), "ruta_obsidian": str(tmp_path / "Boveda")},
    )
    assert r.status_code == 200
    assert client.post("/api/materias", json={"nombre": "Redes"}).status_code == 201
    return uni, fuera


@pytest.mark.parametrize("materia", ["../fuera", "..%2ffuera", "..%2f..%2f", "%2e%2e", "/etc"])
def test_escanear_material_no_acepta_rutas_del_cliente(client, tmp_path, materia):
    _preparar_material(client, tmp_path)
    r = client.get(f"/api/material/escanear?materia={materia}")
    assert r.status_code in (404, 422)
    assert "secreto" not in r.text and str(tmp_path) not in r.text


def test_escanear_material_resuelve_contra_el_catalogo(client, tmp_path):
    _preparar_material(client, tmp_path)
    r = client.get("/api/material/escanear?materia=redes")
    assert r.status_code == 200
    assert [e["materia"] for e in r.json()["escaneos"]] == ["Redes"]
    assert len(r.json()["escaneos"][0]["pendientes"]) == 1


def test_sincronizar_stream_rechaza_asignatura_fuera_del_catalogo(client, tmp_path):
    _preparar_material(client, tmp_path)
    r = client.post("/api/material/sincronizar/stream", json={"materia": "../fuera"})
    assert r.status_code == 404


def test_proyectos_escanear_e_ingestar_no_aceptan_rutas_externas(client, tmp_path):
    _, fuera = _preparar_material(client, tmp_path)
    assert client.get("/api/proyectos/escanear?materia=../fuera").status_code == 404
    r = client.post(
        "/api/proyectos/ingestar",
        json={"materia": "Redes", "nombre": "x", "ruta": str(fuera / "proy")},
    )
    assert r.status_code == 400
    assert str(tmp_path) not in r.text
    r = client.post(
        "/api/proyectos/ingestar",
        json={"materia": "../fuera", "nombre": "x", "ruta": str(fuera / "proy")},
    )
    assert r.status_code == 404
    assert client.get("/api/proyectos").json()["proyectos"] == []


def test_plugins_no_aceptan_carpetas_externas(client, tmp_path):
    _, fuera = _preparar_material(client, tmp_path)
    r = client.post("/api/plugins/config", json={"clave": "nodered", "carpeta": str(fuera)})
    assert r.status_code == 400
    r = client.post(
        "/api/plugins/actualizar", json={"seleccion": "nodered", "carpeta_override": str(fuera)}
    )
    assert r.status_code == 400
    assert str(tmp_path) not in r.text


def test_errores_no_muestran_rutas_absolutas(client, tmp_path):
    inexistente = tmp_path / "no_existe_nunca"
    r = client.post(
        "/api/config",
        json={"carpeta_material": str(inexistente), "ruta_obsidian": str(tmp_path / "B")},
    )
    assert r.status_code == 400
    assert str(tmp_path) not in r.text


def test_error_inesperado_responde_generico(app, client):
    from modular_learning.apps.api.dependencies import get_tutoria_service

    class Roto:
        def iniciar_sesion(self, **_):
            raise RuntimeError("fallo interno en /srv/app/secreto.py")

    app.dependency_overrides[get_tutoria_service] = lambda: Roto()
    r = client.post("/api/tutoria/iniciar", json={"materia": "Redes", "tema": "ARP"})
    assert r.status_code == 500
    assert "/srv" not in r.text and "secreto" not in r.text


def test_config_en_nube_no_devuelve_rutas(client, tmp_path, monkeypatch):
    _preparar_material(client, tmp_path)
    assert str(tmp_path) in client.get("/api/config").json()["carpeta_material"]
    monkeypatch.setenv("ML_EN_NUBE", "1")
    datos = client.get("/api/config").json()
    assert datos["en_nube"] is True
    assert datos["carpeta_material"] == "" and datos["ruta_obsidian"] == ""
    assert str(tmp_path) not in str(datos)


def test_eliminar_asignatura_dos_veces_no_da_500(client):
    assert client.post("/api/materias", json={"nombre": "Temporal"}).status_code == 201
    assert client.delete("/api/materias/temporal").status_code == 200
    assert client.delete("/api/materias/temporal").status_code == 404


def test_generar_cronograma_devuelve_un_borrador_sin_guardarlo(app, client):
    from modular_learning.apps.api.dependencies import get_silabo_service
    from modular_learning.core.application.silabo import SilaboService
    from tests.unit.application.fake_adapters import (
        FakeLLM,
        InMemoryCronogramaRepo,
        InMemoryLectorDocumentosPort,
        InMemoryMateriaRepo,
    )

    clases = [
        {"tema": f"Tema {i}", "objetivo": "Comprender.", "contenido": "Subtemas."}
        for i in range(10)
    ]
    servicio = SilaboService(
        FakeLLM(json_default=clases),
        InMemoryCronogramaRepo(),
        InMemoryMateriaRepo(),
        InMemoryLectorDocumentosPort(),
    )
    app.dependency_overrides[get_silabo_service] = lambda: servicio

    r = client.post("/api/silabo/generar", json={"materia": "Redes de Datos"})
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["materia"] == "Redes de Datos" and len(cuerpo["datos"]["clases"]) == 10
    assert client.get("/api/materias/redes-de-datos/cronograma").json() == {
        "clases": []
    }  # no se guardó

    assert client.post("/api/silabo/generar", json={"materia": "a/b"}).status_code == 422
    assert (
        client.post("/api/silabo/generar", json={"materia": "Redes", "num_clases": 99}).status_code
        == 422
    )
    assert (
        client.post(
            "/api/silabo/generar", json={"materia": "Redes", "nivel": "experto"}
        ).status_code
        == 422
    )
