import os
import re


def _limpiar_artefactos_latex(texto: str) -> str:
    """Limpia artefactos matemáticos de LaTeX y cabeceras sueltas en el texto."""
    if not isinstance(texto, str):
        return str(texto)

    reemplazos = {
        r"\$\rightarrow\$": "->",
        r"\$\leftarrow\$": "<-",
        r"\$\leftrightarrow\$": "<->",
        r"\$\Rightarrow\$": "=>",
        r"\$\Leftarrow\$": "<=",
        r"\\\$\rightarrow\$": "->",
        r"\\\$\leftarrow\$": "<-",
    }
    for pat, reemplazo in reemplazos.items():
        texto = re.sub(pat, reemplazo, texto, flags=re.IGNORECASE)

    # Limpiar cualquier símbolo $ sobrante de fórmulas matemáticas en línea simples
    texto = re.sub(r"\$(.*?)\$", r"\1", texto)

    return texto


def imprimir_markdown_bonito(texto: str) -> None:
    """Formatea texto Markdown con colores y estilos ANSI atractivos para la consola, limpiando artefactos LaTeX."""
    os.system("")
    texto = _limpiar_artefactos_latex(texto)
    lineas = texto.split("\n")
    for linea in lineas:
        if linea.startswith("# "):
            print(f"\n\033[1;95m{linea[2:].upper()}\033[0m")
        elif linea.startswith("## "):
            print(f"\n\033[1;94m{linea[3:]}\033[0m")
        elif linea.startswith("### "):
            print(f"\n\033[1;96m  🔹 {linea[4:]}\033[0m")
        elif linea.startswith("- ") or linea.startswith("* "):
            linea_fmt = re.sub(r"\*\*(.*?)\*\*", r"\033[1m\1\033[0m", linea[2:])
            print(f"    • {linea_fmt}")
        else:
            linea_fmt = re.sub(r"\*\*(.*?)\*\*", r"\033[1m\1\033[0m", linea)
            print(f"    {linea_fmt}")
    print()
