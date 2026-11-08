"""Tests para comprobar que la CLI propaga clase_id al iniciar tutoría (P26)."""

from unittest.mock import MagicMock, patch

from modular_learning.apps.cli.commands import init
from modular_learning.apps.cli.ui import interaccion
from modular_learning.core.application.tutoria import SesionTutoria


def test_pedir_datos_inicio_devuelve_clase_id_de_la_segunda_clase():
    materias_srv = MagicMock()
    materias_srv.listar_materias.return_value = ["Redes"]
    clase_1 = {"id": "clase-redes-1", "tema": "Enrutamiento", "fecha": "2026-04-01"}
    clase_2 = {"id": "clase-redes-2", "tema": "Enrutamiento", "fecha": "2026-04-08"}
    materias_srv.obtener_proximas_clases.return_value = [clase_1, clase_2]

    # Simulamos elegir la segunda clase (que tiene el mismo tema "Enrutamiento")
    mock_select_obj = MagicMock()
    mock_select_obj.ask.return_value = clase_2

    with (
        patch("modular_learning.apps.cli.ui.interaccion.seleccionar_con_flechas", return_value="Redes"),
        patch("questionary.select", return_value=mock_select_obj),
        patch("builtins.input", return_value="2"),
    ):
        datos = interaccion.pedir_datos_inicio(materias_srv)

    assert datos["materia"] == "Redes"
    assert datos["tema"] == "Enrutamiento"
    assert datos["clase_id"] == "clase-redes-2"


def test_init_run_pasa_clase_id_a_iniciar_sesion():
    container = MagicMock()
    sesion_mock = SesionTutoria(
        sesion_id="test-sesion",
        materia="Redes",
        tema="Enrutamiento",
        nivel_profundidad="INTERMEDIO",
        pasos=[],
        clase_id="clase-redes-2",
    )
    container.tutoria_service.iniciar_sesion.return_value = sesion_mock
    container.tutoria_service.finalizar_sesion.return_value = {"guardado_obsidian": True}

    with patch(
        "modular_learning.apps.cli.ui.interaccion.pedir_datos_inicio",
        return_value={
            "materia": "Redes",
            "tema": "Enrutamiento",
            "nivel_profundidad": "INTERMEDIO",
            "clase_id": "clase-redes-2",
        },
    ):
        init.run(container)

    container.tutoria_service.iniciar_sesion.assert_called_once_with(
        sesion_id=container.tutoria_service.iniciar_sesion.call_args.kwargs["sesion_id"],
        materia="Redes",
        tema="Enrutamiento",
        nivel_profundidad="INTERMEDIO",
        clase_id="clase-redes-2",
    )
