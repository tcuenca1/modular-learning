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
   - `ML_USUARIO` y `ML_CONTRASENA`: la cuenta de **administrador** (lo que escribes en «Correo o usuario» y «Contraseña»). Sin contraseña la API responde 503. La contraseña que cambies en Ajustes › Cuenta se conserva entre reinicios; si la olvidas, pon un valor **distinto** en `ML_CONTRASENA` y reinicia: el arranque lo detecta, restablece la contraseña y cierra las sesiones anteriores. Ver «Cuentas y login».
   - `ML_SECRETO_SESION` (opcional; el blueprint lo genera): firma las sesiones. Si falta, el servidor genera un secreto aleatorio una vez y lo guarda en la base (`auth/secreto.json`), así las sesiones sobreviven a los reinicios. Nunca se deriva de la contraseña.
   - `ML_SEMBRAR_EJEMPLOS=1`: carga `data/examples` en la cuenta de administrador la primera vez que arranca (solo si la cuenta no tiene datos). Quítala cuando subas tus datos reales.
   - `ML_EN_NUBE`: definida automáticamente como `1` en `render.yaml` (indica a la app que oculte el escaneo e ingesta de carpetas locales). En modo híbrido (app local conectada a Neon con `DATABASE_URL`), se deja sin definir para conservar el escaneo local de material. Con `ML_EN_NUBE=1`, `GET /api/config` no devuelve las rutas del servidor (`carpeta_material` y `ruta_obsidian` van vacías) y los errores del API muestran mensajes sin rutas absolutas (el detalle queda en el log).
   - `ML_HOSTS_PERMITIDOS` (opcional): hosts que acepta el servidor, separados por comas
     (`mi-app.onrender.com,localhost`); un `Host` distinto recibe 400, salvo `/api/salud`. Por
     defecto `localhost,127.0.0.1` y, si existe, `RENDER_EXTERNAL_HOSTNAME` (Render lo define solo,
     así que en Render no hace falta tocarla). Para abrir la web local desde otro equipo de la red
     hay que añadir su IP o nombre; `*` desactiva la comprobación.

   Además, el servidor envía cabeceras de seguridad (CSP, `X-Content-Type-Options`,
   `X-Frame-Options`, `Referrer-Policy`), comprime las respuestas con gzip y da caché de un año a
   `/assets/` (los archivos llevan hash). Con `ML_EN_NUBE=1` añade HSTS y no publica `/docs`,
   `/redoc` ni `/openapi.json`.
4. **Apply**. El primer build tarda unos minutos; la URL queda como
   `https://modular-learning-xxxx.onrender.com`.

Cada push a la rama vuelve a desplegar. En el plan gratuito el servicio se duerme tras 15
minutos sin uso: la primera visita después tarda alrededor de un minuto.

## Cuentas y login

Con `ML_REQUIERE_ACCESO=1` (lo fija el `Dockerfile`) la web pide iniciar sesión.

- **Cuentas propias:** correo (o usuario) y contraseña de 10 a 128 caracteres, guardadas con hash `scrypt` en el documento `auth/usuarios.json`. No hay registro abierto: el administrador crea las cuentas en **Ajustes › Cuenta › Crear usuario** (se puede hacer desde el teléfono) y puede desactivarlas o restablecer su contraseña. Cinco fallos por origen y usuario, o 20 por cuenta desde cualquier origen, bloquean 15 minutos.
- **Sesión:** cookie `ml_sesion` `HttpOnly`, `SameSite=Lax` y `Secure` en la nube, firmada con HMAC y válida 14 días. Cambiar la contraseña cierra las demás sesiones. Cinco intentos fallidos en 15 minutos bloquean ese usuario desde ese origen.
- **Datos por cuenta:** cada documento se guarda bajo `cuentas/<id>/…` (asignaturas, cronogramas, repaso, historial, guías, ajustes y memoria de plugins). Una cuenta nunca ve los datos de otra, y el servidor se niega a leer datos sin una cuenta activa. Las sesiones de tutoría y quizzes en memoria también son de la cuenta que las creó, y la bóveda de notas del disco del servidor es una subcarpeta por cuenta.
- **Cuenta nueva:** empieza sin asignaturas. Solo el administrador recibe los datos de ejemplo (`ML_SEMBRAR_EJEMPLOS`).
- **Local:** sin `ML_REQUIERE_ACCESO` no hay login y todo sigue en `data/` como siempre.

### Subir tus datos reales a tu cuenta (desde tu PC)

Cuando tengas acceso a tu PC, con la cadena de Neon en `DATABASE_URL` y `ML_REQUIERE_ACCESO=1`:

```bash
python deploy/subir_datos.py --usuario TU_USUARIO                       # simula
python deploy/subir_datos.py --usuario TU_USUARIO --reemplazar --subir  # borra los ejemplos y sube los tuyos
```

La cuenta debe existir (el administrador se crea al arrancar el servidor). Los ajustes se reemplazan por rutas del servidor.

## Rendimiento y cómo medirlo

- **Instantánea en memoria:** `AlmacenPostgres` carga toda la tabla `documentos` en una consulta y sirve lecturas y listados de memoria; las escrituras actualizan la base y la instantánea. Caduca a los 30 s (`ML_CACHE_SEGUNDOS`) para ver cambios hechos por otro proceso, como `subir_datos.py`. Con 80 ms de latencia por consulta, la pantalla Hoy pasó de 16 a 2 consultas en frío y de 7 a 0 en caliente. Está pensado para un solo proceso y pocos datos (≤ 3 usuarios).
- **Precalentado:** al arrancar, el servidor carga la instantánea en segundo plano; así Neon empieza a despertar mientras el servidor termina de iniciar.
- **Medición:** cada respuesta lleva `Server-Timing: app;dur=<ms>` y las peticiones de más de 700 ms (`ML_UMBRAL_LENTA_MS`) dejan en el log `Petición lenta: GET /ruta -> 200 en 1234 ms`. En Render se lee en **Logs**, también desde el teléfono.
- **Lo que no se puede evitar en el plan gratuito:** Render duerme el servicio tras 15 minutos sin tráfico (la primera visita tarda alrededor de un minuto) y Neon suspende su cómputo tras unos 5 minutos sin consultas (la primera consulta tarda 1-3 s). Para que Neon y Render estén en la misma región, revisa ambas en sus paneles: cada consulta entre regiones distintas suma 50-150 ms.

## Qué cambia o no funciona en la nube

- **Arranque del contenedor (`deploy/arranque.sh`)**: el punto de entrada `arranque` del `Dockerfile` crea `/app/data/boveda` y `/app/data/material`, siembra `/app/data` una única vez desde `/app/semilla` cuando no existe `DATABASE_URL` y lanza `ml-web` con `ML_REQUIERE_ACCESO=1` (login por cuentas obligatorio en `/api/*`, salvo `GET /api/salud` y las rutas de inicio de sesión).
- **Ingesta desde carpetas y sincronización de material**: leen carpetas locales del equipo del estudiante, por lo que no están disponibles en Render (`ML_EN_NUBE=1`).
- **Presentaciones `.pptx` sin LibreOffice**: la imagen `python:3.12-slim` del `Dockerfile` no incluye LibreOffice para mantener bajo el consumo de memoria en el plan gratuito; si se sube un `.pptx` individual, `IngestaService` aplica automáticamente el plan B (`python-pptx`) extrayendo texto, tablas y notas del orador sin renderizado visual de diapositivas.
- **Bóveda de Obsidian**: las notas generadas durante las tutorías se escriben en el disco temporal del contenedor (`/app/data/boveda`) y se pierden al reiniciar el servicio en Render; la clase y las tarjetas de repaso sí quedan guardadas en Postgres.

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
