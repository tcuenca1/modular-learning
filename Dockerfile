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

# Instalar la aplicación con el grupo de dependencias web
RUN pip install --no-cache-dir "./backend[web]"

# Copiar datos iniciales y esquemas por defecto
COPY data/ ./data/

# Variables de entorno para despliegue en la nube
ENV PYTHONUNBUFFERED=1 \
    WEB_HOST=0.0.0.0 \
    WEB_PORT=8000 \
    ML_DATA_DIR=/app/data

# Puerto por defecto
EXPOSE 8000

# Comprobación de salud HTTP automática
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:${PORT:-8000}/api/config || exit 1

# Lanzar servidor FastAPI
CMD ["ml-web"]
