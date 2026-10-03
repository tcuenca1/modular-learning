def _limpiar_artefactos_latex(texto: str) -> str:
    texto = texto.replace(r"$\rightarrow$", "->")
    return texto
