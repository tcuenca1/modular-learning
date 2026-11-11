# Pendientes

Trabajo acordado que queda para más adelante. Al terminar uno, se borra de aquí (el detalle
queda en el commit).

## Reglas para quien implemente

Lee `CLAUDE.md` antes de empezar. Además:

1. **Una tarea, un commit.** Rama `main`. El mensaje empieza con el tipo y lleva el id de la
   tarea: `fix(web): P1 enviar clase_id a la tutoria`. Sin tildes, en español.
2. **Solo lo que pide la tarea.** Nada de funcionalidades, refactors ni renombrados extra. Si
   ves otro problema, anótalo al final de este archivo en «Hallazgos» en vez de arreglarlo.
3. **Antes de cada commit, todo en verde** (desde la raíz):
   ```bash
   venv/Scripts/python.exe -m pytest -q backend
   venv/Scripts/ruff.exe check backend
   venv/Scripts/ruff.exe format <archivos .py tocados>     # solo los tocados
   venv/Scripts/python.exe -c "import sys; from importlinter.cli import lint_imports_command; sys.argv=['lint-imports','--config','backend/pyproject.toml']; lint_imports_command()"
   cd frontend && npm run lint && npm run build && npm test
   ```
   `lint-imports.exe` falla en silencio: usa la línea de arriba.
4. **El núcleo no accede al disco.** En `core/` no puede haber `open`, `os.walk`, `os.listdir`,
   `os.remove`, `os.stat`, `os.path.isdir/isfile/exists`, `print` ni `settings`
   (`os.path.join/splitext/basename` sí). Si hace falta el disco, se añade un método a un
   puerto, se implementa en `infrastructure/` y se añade al fake de
   `backend/tests/unit/application/fake_adapters.py`.
5. **Cada tarea trae su test** y lo nombra en el commit. Los tests unitarios usan los fakes,
   nunca `tmp_path` ni el LLM real.
6. **No toques `data/`** (son los datos reales del usuario) **ni `.env`**. Para probar a mano,
   copia `data/examples` a otra carpeta y apunta `ML_DATA_DIR` a ella. No hagas push.
7. **No marques nada como hecho si no cumple todos sus criterios.** Si la dejas a medias,
   escribe debajo qué falta. **No borres tareas de este archivo:** las borra Claude cuando
   aprueba la revisión.
8. **Informe en `docs/CAMBIOS_AGY.md`.** Por cada tarea añade una entrada con la plantilla de
   ese archivo (commit, archivos, qué hiciste, cómo lo verificaste con la salida real de los
   comandos, dudas). Va en un commit aparte justo después del de la tarea:
   `docs: P1 informe en CAMBIOS_AGY`.
9. **Documentación:** si la tarea cambia un comportamiento descrito en `README.md`,
   `docs/DESPLIEGUE.md` o `CLAUDE.md`, actualiza ese párrafo en el mismo commit de la tarea.
   No reescribas `docs/ARCHITECTURE.md` ni añadas documentos nuevos (salvo las tareas D1 y D2).
10. **Prueba manual de verdad.** Si la tarea cambia efectos, estado o carga de datos de una
    vista, ábrela en el navegador y describe qué hiciste y qué viste. `lint` y `build` no
    cuentan como prueba manual.

## Tareas (en orden de prioridad)

Origen: revisión con agentes simulados (usuario novato, móvil, accesibilidad, QA, auditoría
técnica y arquitectura). Son hallazgos de modelos, no de usuarios reales: **reproduce cada
problema antes de arreglarlo** y, si no se reproduce, anótalo en «Hallazgos» y no cambies nada.

### P30. Validar nombres y existencia de asignaturas

Hoy `POST /api/materias` acepta un nombre de 20 MB (listado de 60 MB y asignatura imposible de
borrar), `"   "`, `"!!!"` o `"😀"` responden 201 sin crear nada, `PUT /api/materias/{slug}`
inexistente la crea, y se crean clases y parciales en asignaturas que no existen.

- Longitud máxima razonable (p. ej. 80) y caracteres admitidos; rechazar vacío, solo
  espacios/símbolos, NUL, `/`, `\` y `..` con 422 y mensaje claro en español.
- Rechazar nombres duplicados (comparados sin tildes ni mayúsculas).
- `PUT`, altas de clase y de parcial sobre una asignatura inexistente: 404.
- La regla vive en `core` (servicio o dominio), no en el router.

**Aceptación:** tests unitarios con fakes para cada caso; la UI muestra el error al intentarlo.

### P31. Rutas del cliente y errores que filtran el servidor

`GET /api/material/escanear?materia=..%2f..%2f` listó 1417 archivos fuera de la carpeta de
material con rutas absolutas; `/api/proyectos/escanear` y la configuración de plugins aceptan
rutas del cliente de forma parecida. Los errores 400/500 muestran rutas absolutas del servidor.

- Resolver `materia` siempre contra el catálogo (slug conocido) y nunca concatenarla como ruta.
- Cualquier ruta recibida debe quedar dentro de su carpeta base (comprobar tras resolver).
- Los errores devuelven un mensaje genérico; el detalle va al log, sin rutas absolutas.
- En modo nube (`ML_EN_NUBE=1`), `GET /api/config` no devuelve rutas del equipo.

**Aceptación:** tests de integración con `tmp_path` que intentan `../` y rutas absolutas y
reciben 4xx sin datos de fuera.

### P32. Escrituras concurrentes sin pérdida de datos

8 `POST /api/materias` en paralelo dan 4 errores 500 y solo persiste 1; altas de clase en
paralelo fallan con `WinError 32`; `DELETE` doble da 500. No hay ningún bloqueo y cada
repositorio lee, modifica y reescribe el documento entero.

- Serializar lectura-modificación-escritura por documento dentro del `AlmacenDocumentos`
  (adaptador local) y escribir de forma atómica (archivo temporal y reemplazo).
- Un `DELETE` repetido responde 404 (o 204 idempotente), nunca 500.
- No cambies el contrato del puerto salvo que sea imprescindible; si lo haces, actualiza el fake.

**Aceptación:** test de integración con hilos que crea N asignaturas a la vez y comprueba
que persisten las N.

### P33. Cabeceras de seguridad, documentación de la API y compresión

No hay CSP, `X-Content-Type-Options`, `X-Frame-Options` ni validación de `Host`; `/docs`,
`/redoc` y `/openapi.json` son públicos; el JS de 947 KB sale sin compresión ni caché.

- Middleware con cabeceras de seguridad (CSP compatible con el build de Vite).
- `TrustedHostMiddleware` configurable por variable de entorno (por defecto, localhost).
- Desactivar `/docs`, `/redoc` y `/openapi.json` en modo nube.
- `GZipMiddleware` y `Cache-Control` largo para `assets/` (los nombres llevan hash).
- Documenta las variables nuevas en `docs/DESPLIEGUE.md`.

**Aceptación:** test de API que comprueba las cabeceras; la web sigue cargando en el navegador.

### P34. Dependencias y CI

- Subir `pypdf` a ≥ 6.21.4 en `backend/pyproject.toml` (procesa PDFs subidos) y reinstalar.
- En `.github/workflows/ci.yml` añadir: `npm test`, `ruff format --check`, `pip-audit` sobre el
  proyecto y `npm audit --audit-level=high`. Sin cobertura con umbral todavía.
- Añadir `.github/dependabot.yml` (pip y npm, semanal).

**Aceptación:** el CI pasa en verde con los pasos nuevos (pruébalos en local con los mismos
comandos).

### P35. Plugins sin nombres de asignatura escritos a mano

`core/application/plugins.py` (alrededor de las líneas 193-280) contiene nombres de asignaturas
del usuario y un `if/elif` por plugin con `hasattr`. `PluginPracticoBase` no declara lo que el
servicio invoca.

- Declarar en `PluginPracticoBase` los métodos que el servicio usa (o un método único
  `ejecutar(accion, datos)`), de modo que el servicio no distinga entre plugins concretos.
- Quitar del `core` cualquier nombre de asignatura; la asociación plugin-asignatura va en
  configuración o en el propio plugin.
- Tests del servicio con un plugin falso (fake) y sin `hasattr`.

**Aceptación:** `git grep -n "Internet de las Cosas\|Programacion Web\|Tecnologias de Conmutacion" backend/src/modular_learning/core`
sin resultados; comportamiento actual intacto.

### P36. Pantalla Hoy coherente y con guía de arranque

- El contador («1/2 clases (50%)») contradice «No tienes clases pendientes» y «Aún sin
  cronograma»: define un solo criterio y haz que los tres textos coincidan.
- Mostrar arriba «Siguiente clase» (asignatura, tema y fecha) si existe.
- Sin datos: tarjeta de 3 pasos (crear asignatura, subir sílabo, empezar tutoría) con enlaces.
- «Subir sílabo» aparece 5 veces: un solo botón por asignatura sin cronograma, con el nombre
  de la asignatura en su etiqueta.

**Aceptación:** prueba en el navegador (regla 10) con datos vacíos y con `data/examples`;
test de la lógica del contador en `lib/`.

### P37. Flujo «Nueva asignatura» y selector

- Enter guarda; botón con estado «Guardando…»; aviso de éxito; la asignatura nueva queda
  seleccionada (hoy tras recargar vuelve a otra) y el estado vacío indica el siguiente paso.
- El `<select>` de asignatura tiene `max-width: 100%` y trunca con puntos suspensivos; en
  móvil no hay desplazamiento horizontal.
- El panel de sílabo preselecciona la asignatura activa, no «Nueva asignatura…».

**Aceptación:** prueba en el navegador a 375 px y escritorio:
`document.documentElement.scrollWidth <= innerWidth` en Asignaturas con un nombre de 80
letras.

### P38. Accesibilidad AA

- Etiquetas (`<label htmlFor>` o `aria-label`) en los selects «Asignatura» y «Profundidad» de
  Tutoría, el select de Asignaturas, el input «Tema» y los 2 inputs de Ajustes.
- Foco visible en todos los `<select>`.
- Contraste ≥ 4,5:1 del texto secundario (claro `#9c9381` sobre crema; oscuro `#756d5e`),
  del rojo `#ec003f` y del verde de «+ Definir corte».
- Menú móvil: `aria-expanded`, cierre con Escape y foco devuelto al botón; botones de tema
  con `aria-pressed`.
- Encabezados sin saltos (h1 a h3) en Estudiar, Asignaturas y Ajustes; enlace «Saltar al
  contenido».

**Aceptación:** axe-core 4.10.2 (inyéctalo desde cdnjs) sin violaciones `serious` ni
`critical` en las 5 vistas y sus pestañas, en claro y oscuro; describe lo que viste.

### P39. Objetivos táctiles y calendario en móvil

- Controles interactivos de al menos 44×44 px en pantallas táctiles (toggles de tema,
  menú, pestañas, flechas del calendario, enlaces de acción, «Eliminar asignatura»).
- Calendario: abrir en el mes con la próxima clase (o botón «Ir a la próxima clase») y filas
  de clase tocables.
- En Asignaturas › Proyectos el `<code>` no se corta y la tarjeta «Cortes de parcial» cabe
  en 375 px.

**Aceptación:** medición con JS de los infractores en Hoy, Calendario y Asignaturas (cero
por debajo de 44 px en móvil) y prueba visual a 375 px.

### P40. Rendimiento del frontend

El bundle es un solo JS de 947 KB (271 KB gzip) y en móvil Lighthouse da rendimiento 55
(LCP 7,9 s).

- `React.lazy` y `Suspense` por vista (rutas) para dividir el bundle.
- Servir solo las fuentes KaTeX en WOFF2.
- Meta: JS inicial < 400 KB sin comprimir y rendimiento móvil ≥ 75 en Lighthouse.

**Aceptación:** `npm run build` con los tamaños por chunk y la medición de Lighthouse antes
y después (`npx lighthouse`, categoría rendimiento, móvil).

### P41. Textos sin jerga y acciones con IA avisadas

- Reemplazar o explicar «Bóveda de Obsidian», «Cortes de parcial» y «Profundidad»
  (con una línea de ayuda o texto auxiliar).
- No mostrar rutas personales completas: mostrar solo el último tramo y la ruta completa
  en un `title`.
- Los botones que llaman a la IA («Preguntas nuevas», generar guía, iniciar tutoría) llevan
  un aviso breve («usa IA»).
- Distinguir los iconos de «Hoy» y del tema claro (hoy es el mismo sol).

**Aceptación:** `git grep` de los textos viejos sin resultados; prueba en el navegador.

### P42. Tests de lo que hoy está sin cubrir

- `core/domain/sincronizador.py` (0 % de cobertura): tests unitarios de sus casos.
- `core/application/plugins.py` (60 %): tests del servicio con plugin falso.
- Un test de contrato que ejecute las mismas aserciones contra el fake y contra el adaptador
  real en disco para `CronogramaRepo` y `MateriaRepo`.

**Aceptación:** cobertura de `sincronizador.py` ≥ 80 % (`pytest --cov`, solo para medir; no
añadas la dependencia al repo si no está ya).

## Para decidir con el usuario (no implementar)

- **Material nuevo en la nube:** modo híbrido con ajustes por equipo, o leer de OneDrive con
  Microsoft Graph.
- **Medir la caché de `AlmacenPostgres`:** hay que medir la recarga en Render antes y después;
  `listar` sigue consultando Neon en cada llamada.
- **Extracción de evaluaciones del sílabo:** que `04_extraccion_silabo.md` capture los parciales
  en lugar de descartarlos, para no tener que definir a mano los cortes.
- **Tests de las vistas** (repaso, guía offline, confirmación): hace falta elegir la
  herramienta (Testing Library + jsdom).

- **Imágenes en `.docx` (DISC-07):** hoy solo se envía el texto de los párrafos (sin tablas ni
  imágenes). Opciones: convertir `.docx` a PDF con el mismo conversor de P16, o extraer tablas.
- **`apps/cli/commands/snapshot.py` (DISC-12):** no está registrado en la CLI y hace I/O fuera
  de los puertos. ¿Se borra o se integra como comando?

- **Trocear las vistas gigantes:** `MaterialView.tsx` (1279 líneas) y `SilabosView.tsx` (1226)
  son un solo componente; ¿se parten ahora o al tocarlas?
- **Tipar el dominio:** cronogramas, clases y quizzes circulan como `dict`; ¿modelos
  `dataclass`/Pydantic en `core/domain`? Implica tocar casi todo el núcleo.
- **Excepciones de dominio:** hoy los routers capturan errores sueltos; ¿manejador central?
- **`SessionStore` de tutoría:** es en memoria, sin caducidad; ¿TTL o persistencia?
- **Pruebas con usuarios reales:** 3 a 5 compañeros con tareas fijas y el cuestionario SUS;
  los agentes simulados no lo sustituyen.
- **Calidad de las respuestas de la IA:** conjunto fijo de materiales de referencia para
  detectar regresiones al cambiar prompts (consume cuota de Gemini).

## Hallazgos

*(Anota aquí lo que encuentres fuera del alcance de tu tarea.)*
