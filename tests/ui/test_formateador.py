from modules.ui.formateador import _limpiar_artefactos_latex


def test_limpiar_texto_matematico():
    entrada = "Texto $\\rightarrow$ Más texto"
    esperado = "Texto -> Más texto"
    assert _limpiar_artefactos_latex(entrada) == esperado


def test_limpiar_texto_vacio():
    assert _limpiar_artefactos_latex("") == ""
