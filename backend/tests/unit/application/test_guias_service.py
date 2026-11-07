"""Tests unitarios del servicio de guías de estudio offline."""

from __future__ import annotations

import pytest

from modular_learning.core.application.guias import GuiaOfflineService
from modular_learning.core.application.repaso import RepasoService
from modular_learning.core.domain.guia_offline import MARCADOR_RESPUESTAS
from tests.unit.application.fake_adapters import (
    FakeLLM,
    InMemoryCronogramaRepo,
    InMemoryExportadorPdfPort,
    InMemoryGuiasRepo,
    InMemoryHistorialRepo,
    InMemoryLectorDocumentosPort,
    InMemoryTarjetasRepo,
)

CLASES = [
    {"fecha": "01/10/2026", "tema": "VLAN", "objetivo": "Segmentar", "estado": "completado"},
    {"fecha": "08/10/2026", "tema": "Trunking", "contenido": "802.1Q", "estado": "pendiente"},
    {"fecha": "15/10/2026", "tema": "STP", "estado": "pendiente"},
]


@pytest.fixture
def contexto():
    cronograma = InMemoryCronogramaRepo({"Redes": [dict(c) for c in CLASES]})
    historial = InMemoryHistorialRepo()
    llm = FakeLLM(texto_default=f"## Explicación\nTexto\n{MARCADOR_RESPUESTAS}\n1. Respuesta")
    exportador_pdf = InMemoryExportadorPdfPort()
    servicio = GuiaOfflineService(
        llm=llm,
        cronograma_repo=cronograma,
        lector_docs=InMemoryLectorDocumentosPort(),
        guias_repo=InMemoryGuiasRepo(),
        repaso=RepasoService(tarjetas_repo=InMemoryTarjetasRepo(), historial_repo=historial),
        exportador_pdf=exportador_pdf,
    )
    return servicio, cronograma, historial, llm


def _guia_generada(servicio, temas):
    guia = servicio.crear("Redes", temas)
    for i in range(len(guia.clases)):
        servicio.generar_clase(guia.id, i)
    return guia


def test_crear_respeta_el_orden_del_cronograma(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["stp", "Trunking"])

    assert [c.tema for c in guia.clases] == ["Trunking", "STP"]
    assert guia.clases[0].fecha == "08/10/2026"
    assert guia.extension == "completa"
    assert not guia.completa
    assert servicio.pendientes_de_confirmar() == []


@pytest.mark.parametrize(
    ("materia", "temas", "mensaje"),
    [
        ("Redes", [], "al menos una"),
        ("Redes", ["x", "y"], "no están en el cronograma"),
        ("Bases de Datos", ["SQL"], "no tiene cronograma"),
    ],
)
def test_crear_valida_las_clases(contexto, materia, temas, mensaje):
    servicio, *_ = contexto
    with pytest.raises(ValueError, match=mensaje):
        servicio.crear(materia, temas)


def test_generar_clase_usa_el_detalle_del_silabo_y_separa_respuestas(contexto):
    servicio, _, _, llm = contexto
    guia = servicio.crear("Redes", ["Trunking"])
    clase = servicio.generar_clase(guia.id, 0)

    assert clase.contenido == "## Explicación\nTexto"
    assert clase.respuestas == "1. Respuesta"
    assert "802.1Q" in llm.llamadas_texto[-1]["prompt"]


def test_generar_clase_fuera_de_rango(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["STP"])
    with pytest.raises(ValueError, match="no tiene la clase"):
        servicio.generar_clase(guia.id, 5)


def test_revision_marca_vistas_las_entendidas_y_deja_pendientes_las_demas(contexto):
    servicio, cronograma, historial, _ = contexto
    guia = _guia_generada(servicio, ["Trunking", "STP"])

    resumen = servicio.registrar_revision(
        guia.id,
        {
            0: ("entendida", ""),
            1: ("con_dudas", "cómo converge el puerto raíz"),
        },
    )

    assert resumen["completadas"] == ["Trunking", "STP"]
    assert resumen["dudas"] == [{"tema": "STP", "dudas": "cómo converge el puerto raíz"}]
    # Ambas quedaron completadas en el cronograma
    clases = {c["tema"]: c["estado"] for c in cronograma.obtener_cronograma("Redes")}
    assert clases["Trunking"] == "completado"
    assert clases["STP"] == "completado"
    # Quedaron registradas en el historial de estudio
    assert len(historial.listar(materia="Redes")) == 2
    # La guía ya no figura como pendiente
    assert servicio.pendientes_de_confirmar() == []


def test_revision_exige_guia_completa_y_todas_las_clases(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["Trunking", "STP"])
    with pytest.raises(ValueError, match="generada"):
        servicio.registrar_revision(guia.id, {0: ("entendida", ""), 1: ("entendida", "")})

    servicio.generar_clase(guia.id, 0)
    servicio.generar_clase(guia.id, 1)
    with pytest.raises(ValueError, match="cada clase"):
        servicio.registrar_revision(guia.id, {0: ("entendida", "")})
    with pytest.raises(ValueError, match="no válido"):
        servicio.registrar_revision(guia.id, {0: ("quizas", ""), 1: ("entendida", "")})


def test_revision_no_se_repite(contexto):
    servicio, *_ = contexto
    guia = _guia_generada(servicio, ["VLAN"])
    servicio.registrar_revision(guia.id, {0: ("entendida", "")})
    with pytest.raises(ValueError, match="ya se confirmó"):
        servicio.registrar_revision(guia.id, {0: ("entendida", "")})


def test_obtener_inexistente(contexto):
    servicio, *_ = contexto
    with pytest.raises(LookupError):
        servicio.obtener("nope")


def test_clases_con_mismo_tema_tienen_contenido_e_identidad_distinta():
    # Dos clases con el mismo tema en fechas y con objetivos diferentes
    clase_1 = {
        "id": "c1",
        "fecha": "10/09/2026",
        "tema": "Modelos de calidad",
        "objetivo": "Introducción y Garvin",
        "estado": "pendiente",
    }
    clase_2 = {
        "id": "c2",
        "fecha": "11/09/2026",
        "tema": "Modelos de calidad",
        "objetivo": "McCall e ISO 9126",
        "estado": "pendiente",
    }
    cronograma = InMemoryCronogramaRepo({"Software": [clase_1, clase_2]})
    historial = InMemoryHistorialRepo()
    llm = FakeLLM()
    servicio = GuiaOfflineService(
        llm=llm,
        cronograma_repo=cronograma,
        lector_docs=InMemoryLectorDocumentosPort(),
        guias_repo=InMemoryGuiasRepo(),
        repaso=RepasoService(tarjetas_repo=InMemoryTarjetasRepo(), historial_repo=historial),
    )

    # Creamos la guía por IDs para ambas clases del mismo tema
    guia = servicio.crear("Software", ["c1", "c2"])
    assert len(guia.clases) == 2
    assert guia.clases[0].clase_id == "c1"
    assert guia.clases[1].clase_id == "c2"

    servicio.generar_clase(guia.id, 0)
    assert "Introducción y Garvin" in llm.llamadas_texto[-1]["prompt"]

    servicio.generar_clase(guia.id, 1)
    assert "McCall e ISO 9126" in llm.llamadas_texto[-1]["prompt"]

    # Completamos solo la primera clase
    servicio.registrar_revision(guia.id, {0: ("entendida", ""), 1: ("pendiente", "")})

    c_actualizadas = cronograma.obtener_cronograma("Software")
    c1 = next(c for c in c_actualizadas if c["id"] == "c1")
    c2 = next(c for c in c_actualizadas if c["id"] == "c2")
    assert c1["estado"] == "completado"
    assert c2["estado"] == "pendiente"


def test_reparto_extension_segun_tiempo_disponible():
    from modular_learning.core.domain.guia_offline import elegir_extension

    # 4 clases con 4 horas (240 min) -> 60 min/clase -> completa
    assert elegir_extension(4, tiempo_minutos=240) == "completa"
    # 4 clases con 100 min -> 25 min/clase -> estandar
    assert elegir_extension(4, tiempo_minutos=100) == "estandar"
    # 4 clases con 50 min -> 12.5 min/clase -> sintesis
    assert elegir_extension(4, tiempo_minutos=50) == "sintesis"


def test_deshacer_revision_reinvierte_estado_y_limpia_historial(contexto):
    servicio, cronograma, historial, _ = contexto
    guia = _guia_generada(servicio, ["Trunking"])
    servicio.registrar_revision(guia.id, {0: ("entendida", "")})

    assert cronograma.obtener_cronograma("Redes")[1]["estado"] == "completado"
    assert len(historial.listar(materia="Redes")) == 1

    # Deshacer confirmación
    res = servicio.deshacer_revision(guia.id)
    assert res["revertidas"] == ["Trunking"]

    # Estado en cronograma vuelve a pendiente
    assert cronograma.obtener_cronograma("Redes")[1]["estado"] == "pendiente"
    # Historial queda limpio
    assert len(historial.listar(materia="Redes")) == 0
    # Guía vuelve a estar completa pero sin confirmar
    g = servicio.obtener(guia.id)
    assert g.revisada is None
    assert g.pendiente_de_confirmar


def test_eliminar_guia(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["VLAN"])
    assert servicio.obtener(guia.id) is not None
    assert servicio.eliminar_guia(guia.id) is True
    assert servicio.eliminar_guia(guia.id) is False
    with pytest.raises(LookupError):
        servicio.obtener(guia.id)


def test_exportar_pdf(contexto):
    servicio, *_ = contexto
    guia = servicio.crear("Redes", ["VLAN"])
    pdf_bytes, filename = servicio.exportar_pdf(guia.id)
    assert len(pdf_bytes) > 0
    assert filename == f"Guia_redes_{guia.id}.pdf"
    assert len(servicio.exportador_pdf.guias_exportadas) == 1
    assert servicio.exportador_pdf.guias_exportadas[0].id == guia.id


def test_deshacer_dos_guias_mismo_tema_no_toca_la_otra(contexto):
    servicio, _cronograma, historial, _ = contexto
    g1 = _guia_generada(servicio, ["Trunking"])
    g2 = _guia_generada(servicio, ["Trunking"])

    servicio.registrar_revision(g1.id, {0: ("entendida", "")})
    servicio.registrar_revision(g2.id, {0: ("con_dudas", "duda en g2")})

    eventos = historial.listar(materia="Redes")
    assert len(eventos) == 2
    assert any(e.get("guia_id") == g1.id for e in eventos)
    assert any(e.get("guia_id") == g2.id for e in eventos)

    # Deshacer g1 no toca los eventos de g2
    servicio.deshacer_revision(g1.id)
    eventos_restantes = historial.listar(materia="Redes")
    assert len(eventos_restantes) == 1
    assert eventos_restantes[0].get("guia_id") == g2.id


def test_deshacer_clase_ya_completada_sigue_completada(contexto):
    servicio, cronograma, _historial, _ = contexto
    # VLAN ya está completada antes de la guía (CLASES[0]["estado"] == "completado")
    assert cronograma.obtener_cronograma("Redes")[0]["estado"] == "completado"

    guia = _guia_generada(servicio, ["VLAN"])
    servicio.registrar_revision(guia.id, {0: ("entendida", "")})

    # Al deshacer, debe volver a su estado_previo ("completado"), no a "pendiente"
    servicio.deshacer_revision(guia.id)
    assert cronograma.obtener_cronograma("Redes")[0]["estado"] == "completado"
