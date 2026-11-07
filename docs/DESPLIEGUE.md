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
