import sys
import os
import questionary

ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_script)
sys.path.append(ruta_raiz)

from modules.core.services import gestor_archivos
from modules.plugins.services import gestor_plugins
from modules.ui import formateador


def generar_snapshot_proyecto(ruta_proyecto: str) -> str:
    """
    Recorre la ruta del proyecto local excluyendo carpetas basura, 
    genera un árbol de directorios en texto y lee el contenido de archivos fuente.
    """
    ruta_proyecto = ruta_proyecto.strip('"').strip("'")
    if not os.path.exists(ruta_proyecto) or not os.path.isdir(ruta_proyecto):
        raise NotADirectoryError(f"La ruta no es un directorio válido: {ruta_proyecto}")

    exclusiones = {"node_modules", "venv", ".git", "__pycache__", "bin", "obj", ".idea", "dist", "build", ".next"}
    extensiones_fuente = {".py", ".js", ".ts", ".html", ".css", ".json", ".php", ".sql", ".md"}

    arbol_texto = [f"📁 Proyecto Raíz: {os.path.basename(ruta_proyecto)}"]
    archivos_codigo = []

    for root, dirs, files in os.walk(ruta_proyecto):
        dirs[:] = [d for d in dirs if d not in exclusiones and not d.startswith('.')]
        
        nivel = root.replace(ruta_proyecto, '').count(os.sep)
        indent = " " * 4 * nivel
        subindent = " " * 4 * (nivel + 1)
        
        if nivel > 0:
            arbol_texto.append(f"{indent}📂 {os.path.basename(root)}/")
            
        for file in files:
            if not file.startswith('.'):
                arbol_texto.append(f"{subindent}📄 {file}")
                ext = os.path.splitext(file)[1].lower()
                if ext in extensiones_fuente:
                    archivos_codigo.append(os.path.join(root, file))

    snapshot_partes = [
        "### 🌳 Estructura de Directorios del Proyecto:",
        "```text",
        "\n".join(arbol_texto),
        "```\n",
        "### 📄 Contenido de Archivos Fuente Principales:"
    ]

    for archivo in archivos_codigo:
        rel_name = os.path.relpath(archivo, ruta_proyecto)
        try:
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
            if len(contenido) > 5000:
                contenido = contenido[:5000] + "\n... [Código truncado por tamaño] ..."
            
            snapshot_partes.append(f"**Archivo: `{rel_name}`**")
            snapshot_partes.append(f"```code\n{contenido}\n```\n")
        except Exception as e:
            snapshot_partes.append(f"**Archivo: `{rel_name}`** (Error al leer: {e})\n")

    return "\n".join(snapshot_partes)


def run():
    print("=" * 65)
    print(" 🔄 ACTUALIZADOR DE CONTEXTO DE PROYECTOS (ml up)")
    print("=" * 65)

    materias = gestor_archivos.cargar_materias()
    seleccion = questionary.select(
        "Selecciona la asignatura a actualizar:",
        choices=materias,
        style=questionary.Style([
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
            ('answer', 'fg:green bold'),
        ])
    ).ask()

    if not seleccion:
        print("Operación cancelada.")
        return

    plugin = gestor_plugins.obtener_plugin(seleccion)
    if not plugin:
        print(f"❌ La asignatura '{seleccion}' no tiene un plugin práctico asociado con memoria de código fuente.")
        return

    ruta_proyecto = input("👉 Ingresa la ruta absoluta o relativa de tu proyecto local en VSCode: ").strip()
    if not ruta_proyecto:
        print("❌ Ruta no válida.")
        return

    try:
        print("🔍 Analizando estructura y generando snapshot del código fuente...")
        snapshot = generar_snapshot_proyecto(ruta_proyecto)
        plugin.guardar_contexto_extraido(snapshot)
        print(f"\n[ÉXITO] Contexto del proyecto sincronizado y guardado en la memoria del plugin para '{seleccion}'.")
    except Exception as e:
        print(f"\n❌ Error al generar el snapshot del proyecto: {e}")

    input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    run()
