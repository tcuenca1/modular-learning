# ==========================================
# Etapa 1: Compilación del Frontend (React + Tailwind v4 + Vite)
# ==========================================
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend

# Instalar dependencias usando lockfile para builds deterministas
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copiar código fuente del frontend y compilar hacia static/
COPY frontend/ ./
RUN npm run build

# ==========================================
# Etapa 2: Imagen de Producción (Python 3.12 + FastAPI)
# ==========================================
FROM python:3.12-slim AS runner
WORKDIR /app

# Instalar dependencias de sistema mínimas para comprobación de salud
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar manifiestos de empaquetado y código fuente de Python
COPY backend/pyproject.toml backend/README.md ./backend/
COPY backend/src/ ./backend/src/

# Copiar el bundle web compilado desde la etapa frontend-builder
COPY --from=frontend-builder /app/backend/src/modular_learning/apps/api/static ./backend/src/modular_learning/apps/api/static

# Instalar la aplicación con la web y el almacén en Postgres (activo si hay DATABASE_URL)
RUN pip install --no-cache-dir "./backend[web,nube]"

# Datos iniciales para el modo archivos (sin DATABASE_URL): deploy/arranque.sh los copia a
# ML_DATA_DIR si está vacía
COPY data/ ./semilla/
COPY deploy/arranque.sh /usr/local/bin/arranque
RUN sed -i 's/\r$//' /usr/local/bin/arranque && chmod +x /usr/local/bin/arranque

# Variables de entorno para despliegue en la nube; ML_REQUIERE_ACCESO activa el usuario y
# la contraseña (ML_USUARIO, ML_CONTRASENA), que se definen en la plataforma
ENV PYTHONUNBUFFERED=1 \
    WEB_HOST=0.0.0.0 \
    WEB_PORT=8000 \
    ML_DATA_DIR=/app/data \
    ML_REQUIERE_ACCESO=1

# Puerto por defecto
EXPOSE 8000

# Comprobación de salud HTTP automática
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:${PORT:-8000}/api/salud || exit 1

# Preparar la carpeta de datos y lanzar el servidor FastAPI
CMD ["arranque"]
