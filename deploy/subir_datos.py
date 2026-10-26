"""Copia los datos locales (data/) a Postgres para el despliegue en la nube.

Uso, desde la raíz del repositorio y con la cadena de conexión de Neon en DATABASE_URL:

    venv/Scripts/python.exe deploy/subir_datos.py            # muestra qué subiría
    venv/Scripts/python.exe deploy/subir_datos.py --subir    # lo sube

Sube cronogramas, materias, repaso, historial, guías y memoria de plugins tal cual. Los ajustes
se reemplazan por rutas del servidor: allí no existen la bóveda de Obsidian ni las carpetas de
material de este equipo. Volver a ejecutarlo sobrescribe en la nube lo que haya cambiado.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from modular_learning import settings
from modular_learning.infrastructure.persistence.almacen import (
    AlmacenArchivos,
    AlmacenPostgres,
)

# Rutas dentro del contenedor (ML_DATA_DIR=/app/data en el Dockerfile)
AJUSTES_NUBE = {
    "carpeta_material": "/app/data/material",
    "ruta_obsidian": "/app/data/boveda",
}
EXCLUIDOS = ("examples/", "README.md")


def documentos_locales(origen: AlmacenArchivos) -> list[str]:
    claves = []
    for raiz, _, archivos in os.walk(origen.raiz):
        for nombre in archivos:
            relativa = os.path.relpath(os.path.join(raiz, nombre), origen.raiz)
            clave = relativa.replace(os.sep, "/")
            if not clave.startswith(EXCLUIDOS) and not clave.endswith(".tmp"):
                claves.append(clave)
    return sorted(claves)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--subir", action="store_true", help="subir de verdad (sin esto, simula)"
    )
    args = parser.parse_args()

    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        print("Falta DATABASE_URL con la cadena de conexión de Neon.", file=sys.stderr)
        return 1

    origen = AlmacenArchivos(settings.ruta_data())
    claves = documentos_locales(origen)
    print(f"Datos locales en {origen.raiz}: {len(claves)} documentos")
    for clave in claves:
        print(f"  {clave}")
    if not args.subir:
        print("\nSimulación: añade --subir para copiarlos a Postgres.")
        return 0

    destino = AlmacenPostgres(url)
    for clave in claves:
        contenido = origen.leer(clave)
        if contenido is None:
            continue
        if clave == "config/ajustes.json":
            contenido = json.dumps(AJUSTES_NUBE, indent=4, ensure_ascii=False)
        destino.escribir(clave, contenido)
    print(f"\nSubidos {len(claves)} documentos a Postgres.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
