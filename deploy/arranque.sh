#!/bin/sh
# Arranque del contenedor en la nube.
# Con DATABASE_URL los datos viven en Postgres y la carpeta ML_DATA_DIR solo aloja la bóveda y
# el material del servidor. Sin DATABASE_URL (Docker local con volumen) la carpeta es el
# almacén: llega vacía la primera vez y se siembra una sola vez con los datos de la imagen.
set -e

DATOS="${ML_DATA_DIR:-/app/data}"
MARCA="$DATOS/.sembrado"

mkdir -p "$DATOS/boveda" "$DATOS/material"
if [ -z "$DATABASE_URL" ] && [ ! -f "$MARCA" ]; then
    cp -rn /app/semilla/. "$DATOS"/
    date -u +"%Y-%m-%dT%H:%M:%SZ" > "$MARCA"
    echo "Carpeta de datos sembrada en $DATOS"
fi

exec ml-web
