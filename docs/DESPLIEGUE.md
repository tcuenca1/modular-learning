# Despliegue en Render + Neon

La web corre en Render (plan gratuito, con el `Dockerfile`) y los datos viven en Postgres en
Neon (plan gratuito). El disco del plan gratuito de Render se borra en cada reinicio, así que
el backend guarda cronogramas, repasos, historial, guías y ajustes en la tabla `documentos`
cuando existe `DATABASE_URL` (ver `infrastructure/persistence/almacen.py`). En local, sin esa
variable, todo sigue en `data/`.

## 1. Base de datos en Neon

1. Crea una cuenta y un proyecto en <https://neon.tech> (región cercana, por ejemplo
   `aws-us-east-1`).
2. En **Connection Details**, copia la cadena de conexión (`postgresql://…?sslmode=require`).
3. Sube tus datos locales desde la raíz del repositorio (PowerShell):

   ```powershell
   $env:DATABASE_URL = 'postgresql://…'
   venv\Scripts\python.exe deploy\subir_datos.py           # muestra qué subiría
   venv\Scripts\python.exe deploy\subir_datos.py --subir   # lo sube
   ```

   Los ajustes se reemplazan por rutas del servidor. Puedes repetirlo cuando quieras: sobrescribe
   en la nube con lo que tengas en local.

## 2. Servicio web en Render

1. Crea una cuenta en <https://render.com> y conecta tu GitHub.
2. **New → Blueprint** y elige el repositorio `tcuenca1/modular-learning`. Render lee
   `render.yaml` (servicio `modular-learning`, rama `main`).
3. Rellena las variables que pide:
   - `DATABASE_URL`: la cadena de Neon.
   - `GEMINI_API_KEY`: tu clave de Gemini.
   - `ML_USUARIO` y `ML_CONTRASENA`: el acceso a la web (sin contraseña responde 503).
   - `ML_EN_NUBE`: definida automáticamente como `1` en `render.yaml` (indica a la app que oculte el escaneo e ingesta de carpetas locales). En modo híbrido (app local conectada a Neon con `DATABASE_URL`), se deja sin definir para conservar el escaneo local de material.
4. **Apply**. El primer build tarda unos minutos; la URL queda como
   `https://modular-learning-xxxx.onrender.com`.

Cada push a la rama vuelve a desplegar. En el plan gratuito el servicio se duerme tras 15
minutos sin uso: la primera visita después tarda alrededor de un minuto.

## Qué no funciona en la nube

- **Ingesta desde carpetas y sincronización de material**: leen carpetas de este equipo.
- **Bóveda de Obsidian**: las guías de las tutorías se escriben en el disco temporal del
  servidor y se pierden al reiniciar; la clase sí queda marcada como completada en Postgres.

## 3. Pruebas locales con Docker Compose (tipo producción)

Para probar la imagen de producción y el comportamiento con Postgres sin tocar la base de datos de Neon ni los datos reales del usuario (`data/`), se utiliza `docker-compose.yml`.

### Arquitectura de los servicios
- `db`: Contenedor Postgres 16 (`postgres:16-alpine`) con un volumen persistente con nombre `db_data`. Expone el puerto `5432` en el host para permitir herramientas y scripts de migración.
- `app`: Imagen compilada con el `Dockerfile` de producción. Conecta a `db` vía `DATABASE_URL=postgresql://postgres:postgres@db:5432/modular_learning` y monta una copia de `data/examples` (`data_ejemplo`) y una bóveda aislada (`boveda_ejemplo`). La clave de Gemini se toma de `.env` vía `env_file`.

### Paso a paso

1. **Preparar datos y bóveda de ejemplo (si no existen):**
   ```powershell
   # En Windows PowerShell:
   Copy-Item -Recurse -Force data/examples data_ejemplo
   New-Item -ItemType Directory -Force boveda_ejemplo
   ```
   ```bash
   # En Linux / macOS:
   cp -r data/examples data_ejemplo
   mkdir -p boveda_ejemplo
   ```

2. **Construir e iniciar los servicios:**
   ```bash
   docker compose up --build
   ```
   O en segundo plano:
   ```bash
   docker compose up --build -d
   ```

3. **Verificar el estado y la salud del sistema:**
   ```bash
   docker compose ps
   curl http://localhost:8000/api/salud
   ```
   Abre en el navegador <http://localhost:8000> para comprobar la carga de la interfaz web.

4. **Ensayar la migración contra el Postgres de Compose:**
   Para poblar primero la base de datos con los datos de ejemplo y simular la migración:
   ```powershell
   # En Windows PowerShell:
   $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/modular_learning"
   $env:ML_DATA_DIR = "data/examples"
   venv/Scripts/python.exe deploy/subir_datos.py --subir
   venv/Scripts/python.exe scripts/migrar_datos.py --simular
   ```
   ```bash
   # En Linux / macOS / Bash:
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/modular_learning" ML_DATA_DIR="data/examples" venv/bin/python deploy/subir_datos.py --subir
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/modular_learning" venv/bin/python scripts/migrar_datos.py --simular
   ```

   Alternativamente, puedes ejecutar ambos comandos directamente dentro del contenedor `app` sin necesidad de configurar variables de entorno ni librerías en el host:
   ```bash
   docker compose exec app python deploy/subir_datos.py --subir
   docker compose exec app python scripts/migrar_datos.py --simular
   ```

5. **Limpieza y borrado completo:**
   Para detener los contenedores y eliminar tanto las redes como el volumen con nombre de Postgres (`db_data`):
   ```bash
   docker compose down -v
   ```
   Para limpiar también las carpetas temporales de prueba locales:
   ```powershell
   Remove-Item -Recurse -Force data_ejemplo, boveda_ejemplo
   ```
