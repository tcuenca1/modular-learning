"""Comando CLI: `ml es` - Extracción de cronogramas a partir de sílabos."""

from __future__ import annotations

import os
import sys

from modular_learning import bootstrap
from modular_learning.apps.cli.ui.spinner import spinner


def procesar_ruta(ruta: str, container: bootstrap.Container | None = None) -> None:
    """Procesa un archivo individual o escanea una carpeta completa de sílabos."""
    cont = container or bootstrap.get_container()
    silabo_service = cont.silabo_service

    ruta = ruta.strip('"').strip("'")
    if not os.path.exists(ruta):
        print(f"❌ [ERROR] La ruta especificada no existe: {ruta}")
        return

    if os.path.isdir(ruta):
        print(f"📁 [CARPETA] Analizando carpeta de sílabos:\n   {ruta}")
        archivos = silabo_service.escanear_directorio_silabos(ruta)
        if not archivos:
            print("⚠️ [AVISO] No se encontraron archivos PDF, MD o TXT en la carpeta.")
            return

        print(f"🚀 [LOTE] Se encontraron {len(archivos)} archivos. Iniciando extracción...")
        for idx, archivo in enumerate(archivos, 1):
            print("\n" + "=" * 55)
            print(f" ARCHIVO {idx} DE {len(archivos)}: {os.path.basename(archivo)}")
            print("=" * 55)
            _procesar_archivo_cli(archivo, silabo_service)
    else:
        _procesar_archivo_cli(ruta, silabo_service)


def _procesar_archivo_cli(ruta_archivo: str, silabo_service) -> None:
    nombre_sugerido = silabo_service.sugerir_nombre_materia(ruta_archivo)
    print(f"📚 [MATERIA] Asignatura sugerida: \033[1;92m{nombre_sugerido}\033[0m")
    try:
        nombre_materia = input(
            f"-> Presiona ENTER para aceptar '{nombre_sugerido}' o escribe otro nombre: "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        nombre_materia = ""

    if not nombre_materia:
        nombre_materia = nombre_sugerido

    try:
        with spinner(f"Extrayendo y estructurando cronograma para '{nombre_materia}'..."):
            res = silabo_service.procesar_archivo_individual(ruta_archivo, nombre_materia)

        print(f"✅ [ÉXITO] Se extrajeron {res['total_clases']} clases para '{res['materia']}'.")
        print(f"📄 Guardado en: {res['ruta_salida']}\n")
    except Exception as e:
        print(f"❌ [ERROR] Falló el procesamiento de '{nombre_materia}': {e}")


def run() -> None:
    """Punto de entrada de CLI para el comando `ml es`."""
    if len(sys.argv) > 1:
        procesar_ruta(sys.argv[1])
    else:
        print("=" * 55)
        print(" EXTRACTOR DE CRONOGRAMAS DE SÍLABOS (ML ES)")
        print("=" * 55)
        try:
            ruta_input = input("-> Ingresa la ruta de un archivo o carpeta con sílabos: ").strip()
            if ruta_input:
                procesar_ruta(ruta_input)
            else:
                print("❌ [ERROR] Ruta no válida.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")


if __name__ == "__main__":
    run()
