#!/bin/sh
# Arranque del contenedor en la nube.
# El volumen persistente se monta en $ML_DATA_DIR y llega vacío la primera vez: se siembra
# con los datos incluidos en la imagen (/app/semilla) una sola vez. Los siguientes despliegues
# no tocan lo que haya en el volumen.
set -e

DATOS="${ML_DATA_DIR:-/app/data}"
MARCA="$DATOS/.sembrado"

mkdir -p "$DATOS"
if [ ! -f "$MARCA" ]; then
    cp -rn /app/semilla/. "$DATOS"/
    mkdir -p "$DATOS/boveda" "$DATOS/material"
    date -u +"%Y-%m-%dT%H:%M:%SZ" > "$MARCA"
    echo "Volumen de datos sembrado en $DATOS"
fi

exec ml-web
