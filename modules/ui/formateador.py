import re
from rich.console import Console
from rich.markdown import Markdown


def _limpiar_artefactos_latex(texto: str) -> str:
    """
    Limpia artefactos comunes de LaTeX en el texto.
    """
    if not texto:
        return ""

    # Ejemplo de uso de raw strings r"" para evitar problemas con secuencias de escape
    # Corregido el error de escape en expresiones regulares
    texto = re.sub(r"\\textbf{(.*?)}", r"\1", texto)
    texto = re.sub(r"\\textit{(.*?)}", r"\1", texto)
    texto = re.sub(r"\\begin{.*?}", "", texto)
    texto = re.sub(r"\\end{.*?}", "", texto)

    return texto.strip()


def formatear_texto(texto: str) -> str:
    """
    Formatea el texto general aplicando limpieza de LaTeX.
    """
    return _limpiar_artefactos_latex(texto)


def imprimir_markdown_bonito(texto: str) -> None:
    """
    Imprime texto en formato Markdown renderizado con Rich y limpiando artefactos LaTeX.
    """
    texto_limpio = formatear_texto(texto)
    console = Console()
    console.print(Markdown(texto_limpio))
