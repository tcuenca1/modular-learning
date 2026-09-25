import os
import re


def imprimir_markdown_bonito(texto: str) -> None:
    """Formatea texto Markdown con colores y estilos ANSI atractivos para la consola."""
    os.system('')
    lineas = texto.split('\n')
    for linea in lineas:
        if linea.startswith('# '):
            print(f"\n\033[1;95m{linea[2:].upper()}\033[0m")
        elif linea.startswith('## '):
            print(f"\n\033[1;94m{linea[3:]}\033[0m")
        elif linea.startswith('### '):
            print(f"\n\033[1;96m  🔹 {linea[4:]}\033[0m")
        elif linea.startswith('- ') or linea.startswith('* '):
            linea_fmt = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', linea[2:])
            print(f"    • {linea_fmt}")
        else:
            linea_fmt = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', linea)
            print(f"    {linea_fmt}")
    print()
