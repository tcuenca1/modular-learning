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

### P12. Seleccionar la asignatura recién guardada aunque lleve tildes

En `frontend/src/views/SilabosView.tsx` (guardar sílabo), `slugGuardado` se calcula con
`toLowerCase().replace(/\s+/g, '-')`, que no quita tildes: para «Ingeniería de Software» da
`ingeniería-de-software` y no coincide con el slug del backend (`ingenieria-de-software`), así
que se queda seleccionada la asignatura anterior.

- Busca la asignatura en la lista que devuelve `api.getMaterias()` comparando con `clave()` de
  `lib/asignaturas.ts` (nombre o slug), en vez de construir el slug a mano. Si hace falta,
  `cargarCatalogo` puede aceptar el nombre además del slug.

**Aceptación:** guardar un sílabo para una asignatura con tildes la deja seleccionada y muestra
sus clases (prueba en el navegador, regla 10). `npm run lint` sin avisos.

### P13. «Vaciar cronograma» no debe borrar la asignatura

`DELETE /api/materias/{materia}/cronograma` (`apps/api/routers/materias.py`) llama a
`servicio.eliminar_cronograma(materia, borrar_materia=True)`, así que la asignatura desaparece
del catálogo aunque el diálogo de `SilabosView` dice «se conservará la asignatura».

- El endpoint usa `borrar_materia=False`. La asignatura sigue en el catálogo, sin clases, igual
  que las que nunca tuvieron cronograma.
- Revisa que `SilabosView` siga mostrando la asignatura seleccionada tras vaciar.

**Aceptación:** test de API: tras `DELETE /api/materias/redes/cronograma`, `GET /api/materias`
sigue incluyendo «Redes» y `GET /api/materias/redes/cronograma` devuelve `{"clases": []}`.

### P14. No sobrescribir el nombre de la asignatura del catálogo

Al guardar un sílabo, `SilaboService.guardar_cronograma` llama a
`materia_repo.agregar_materia(nombre)`, y `JsonMateriaRepo.guardar` sustituye el nombre si el
slug ya existe. Si el campo Asignatura se deja vacío, el nombre sale del archivo
(«INGENIERIA DE SOFTWARE II») y pisa «Ingeniería de Software II». Lo mismo pasa al crear una
asignatura con otra escritura.

- `agregar_materia` (repositorio JSON y fake) **no cambia** una asignatura que ya existe por
  slug: solo añade las nuevas. El nombre solo cambia con «Renombrar» (`guardar`).
- Los casos de uso que reciben una asignatura escrita por el usuario la traducen al nombre del
  catálogo con `resolver_materia` antes de usarla: `SilaboService.guardar_cronograma`, la
  ingesta (`core/application/ingesta.py`, que decide la carpeta de la nota en Obsidian) y
  `TutoriaService.iniciar_sesion`. Si no está en el catálogo, se usa lo escrito.

**Aceptación:** tests unitarios: con «Ingeniería de Software II» en el catálogo, guardar un
sílabo como «INGENIERIA DE SOFTWARE II» deja el nombre del catálogo intacto y el cronograma en
la misma clave; ingestar un archivo con «ingenieria de software ii» escribe la nota en la carpeta
«Ingeniería de Software II».

### P15. Desplegable de asignaturas al subir archivos

En `MaterialView` (subida individual) y en `SilabosView` (subir sílabo) la asignatura se escribe
a mano.

- `MaterialView`: un `<select>` con el catálogo (`api.getMaterias()`), sin texto libre; se sube
  solo a asignaturas que existen.
- `SilabosView`: un `<select>` con el catálogo más una opción «Nueva asignatura…» que muestra el
  campo de texto. Si al extraer se sugiere un nombre que coincide con una del catálogo
  (comparando con `clave()`), se selecciona esa en vez de rellenar el texto.

**Aceptación:** prueba en el navegador (regla 10) de los dos formularios, incluido un sílabo
cuyo archivo está en mayúsculas: queda seleccionada la asignatura existente. `npm run lint` sin
avisos.

### P16. Ingestar `.pptx` convirtiéndolo a PDF

Gemini no acepta presentaciones como archivo, y muchas diapositivas son imágenes sin texto, así
que no basta con extraer el texto: hay que convertir a PDF y enviar el PDF, que Gemini lee
también visualmente.

- Puerto nuevo `ConversorPdfPort` en `core/ports/` con `convertir_a_pdf(ruta) -> str | None`
  (ruta de un PDF temporal, o `None` si no se puede convertir) y su fake en
  `fake_adapters.py`.
- Adaptador `infrastructure/documents/conversor_libreoffice.py`: ejecuta
  `soffice --headless --convert-to pdf --outdir <tmp> <archivo>` con `subprocess` (sin
  `shell=True`, con `timeout`). Busca `soffice` en el `PATH` y en
  `C:\Program Files\LibreOffice\program\`; ruta configurable con la variable `ML_SOFFICE`.
- `IngestaService`: para `.pptx`, convierte y manda el PDF como hoy se manda un PDF. Si no hay
  conversor disponible, **plan B**: extrae el texto con `python-pptx` (títulos, cuadros de texto,
  tablas y notas del orador) y avisa en el resultado de que se perdieron las imágenes. Añade
  `python-pptx` a `backend/pyproject.toml` y quita `.pptx` de `EXTENSIONES_NO_SOPORTADAS_WEB`.
- Borra el PDF temporal al terminar, también si falla.
- No añadas LibreOffice al `Dockerfile` (pesa cientos de MB); en la nube se usa el plan B.
- Documenta en `README.md` que para las presentaciones hay que instalar LibreOffice.

**Aceptación:** tests unitarios con fakes: con conversor se envía un PDF; sin conversor se envía
el texto y el resultado lleva el aviso; el temporal se borra si el LLM falla. Test de
integración del plan B con un `.pptx` creado con `python-pptx` en `tmp_path`. El test del
adaptador de LibreOffice se salta (`pytest.skip`) si `soffice` no está instalado.

### P17. Material: lo ingestado primero

En `MaterialView`, revisar el material ingestado es lo principal y subir un archivo suelto es
ocasional, pero hoy el orden es: resultados del escaneo → subida individual → historial.

- El historial de materiales ingestados pasa arriba como bloque principal de la pestaña.
- La subida individual queda plegada tras un botón «Subir un archivo» (cerrada por defecto).
- Los resultados del escaneo solo se muestran cuando hay un escaneo en esta visita.
- Solo se cambia la disposición: nada de cambios en la lógica ni en la API.

**Aceptación:** prueba en el navegador (regla 10), en escritorio y en una ventana estrecha
(móvil). `npm run lint` sin avisos.

### P18. Docker Compose para pruebas tipo producción

Complemento del venv, no sustituto: sirve para probar la misma imagen que Render y el modo
Postgres sin tocar Neon.

- `docker-compose.yml` en la raíz con dos servicios: `app` (el `Dockerfile` actual) y `db`
  (`postgres:16-alpine`, volumen con nombre). `DATABASE_URL` apunta a `db`.
- La app usa una copia de `data/examples` y una bóveda de ejemplo montadas como volúmenes;
  **nunca** `data/` ni la bóveda real. `GEMINI_API_KEY` llega con `env_file: .env`, sin copiar
  `.env` a la imagen (comprueba `.dockerignore`).
- Sección nueva en `docs/DESPLIEGUE.md`: cómo levantarlo, cómo ensayar
  `scripts/migrar_datos.py --simular` contra el Postgres del compose y cómo borrarlo todo.

**Aceptación:** `docker compose up --build` arranca, `GET /api/salud` responde 200 en
`localhost:8000` y la web carga. Pega en el informe la salida de `docker compose ps`.

### P19. Hoy: desbordamiento en móvil y avisos agrupados

Hazla después de P18. En las capturas (390 px de ancho) la vista Hoy se sale por la derecha: los
avisos de guías y la cabecera quedan cortados. Además, la vista empieza con un aviso amarillo por
cada guía pendiente de confirmar (hoy hay 6, con duplicados y dos de una asignatura que ya no
está en el catálogo) antes de lo importante.

- Corrige el desbordamiento horizontal en móvil en Hoy (y revisa la barra superior de móvil del
  layout). Ninguna vista debe tener scroll horizontal a 390 px.
- Sustituye la pila de avisos por una sola línea: «N guías por confirmar →» que lleva a la lista
  de guías. Con una sola guía, puede seguir mostrando su asignatura.
- En el número de «9 preguntas para hoy» se ve un recuadro amarillo extraño debajo del número
  (en Hoy y en Repaso): corrige el estilo para que el resaltado se vea como subrayado o quítalo.

**Aceptación:** capturas o prueba en el navegador a 390 px y a 1440 px (regla 10), con varias
guías pendientes en una copia de `data/examples`. `npm run lint` sin avisos.

### P20. Asignaturas: un solo selector y acciones peligrosas apartadas

Hazla después de P15 y P17 (tocan los mismos archivos). Hoy Asignaturas tiene tres niveles de
navegación seguidos (pestañas Cronogramas/Material → «Gestionar / Subir sílabo» → chips de
asignatura) y Material tiene además sus propias pestañas. Los botones que borran están al lado
de los normales.

- Estructura: arriba, el selector de asignatura (uno solo, compartido); debajo, tres pestañas:
  **Clases**, **Material** y **Proyectos**. «Subir sílabo» es un botón dentro de Clases (y el
  estado vacío de una asignatura sin clases lo ofrece directamente). La pestaña se refleja en la
  URL (`?tab=`) y las URL antiguas siguen funcionando.
- Acciones de borrado (vaciar cronograma, eliminar asignatura, vaciar todo el material) en un
  menú «⋯» o en una sección «Zona peligrosa» al final, nunca junto al botón principal. Siguen
  pidiendo confirmación.
- No mostrar el slug al usuario.
- Solo reorganizar: sin cambios de API ni de lógica de datos.

**Aceptación:** prueba en el navegador (regla 10) de cada acción que había antes (todas siguen
accesibles), en escritorio y a 390 px. Lista en el informe dónde quedó cada botón.

### P21. Menú de 9 entradas a 5

Hazla después de P20. Menú actual: Hoy, Calendario, Tutoría, Repaso, Guía offline, Progreso,
Asignaturas, Plugins, Configuración.

- **Hoy** incorpora el resumen de Progreso (avance por asignatura); la vista Progreso se elimina.
- **Estudiar** agrupa Tutoría, Repaso y Guía offline como tres pestañas o modos de una misma
  pantalla.
- **Calendario** y **Asignaturas** se quedan.
- **Ajustes** agrupa Configuración y Plugins.
- Todas las rutas antiguas (`/tutoria`, `/repaso`, `/guia`, `/progreso`, `/plugins`, `/config`)
  redirigen a su nuevo sitio conservando la query (`/tutoria?materia=…&clase_id=…` debe seguir
  funcionando: lo usan los enlaces de P1).
- Actualiza los enlaces internos.

**Aceptación:** prueba en el navegador (regla 10) de todas las rutas antiguas y de los enlaces
«Estudiar» de Hoy y Calendario. `npm run lint`, `npm run build` y `npm test` en verde.

### P22. Textos más cortos y consistentes

Hazla al final de la interfaz (después de P21).

- Las introducciones de cada vista, una sola línea (Guía offline y Repaso tienen párrafos de tres
  líneas); lo demás, en un icono de ayuda o en el estado vacío.
- Siempre «asignatura», nunca «materia», en la interfaz.
- Botones con mayúscula solo en la primera palabra («Añadir clase», no «Añadir Clase»).
- Sin jerga: «Ingestar documento individual» → «Convertir en nota» (revisa «ingestar» en toda la
  interfaz).
- Plugins: el «Registro de sincronización» solo aparece después de pulsar «Actualizar».

**Aceptación:** `git grep -n "Materia\b\|materia " frontend/src/views` sin textos visibles con
«materia»; capturas antes y después de 3 vistas en el informe. `npm run lint` sin avisos.

## Documentación funcional (tarea aparte, no toca código)

### D1. Manual funcional del sistema en PDF

Un documento que explique **qué hace el sistema y cómo debería comportarse**, para revisar los
flujos de forma sistemática en vez de encontrar errores por casualidad. No sustituye a
`README.md` ni a `ARCHITECTURE.md`: está escrito para el usuario y para quien revise.

**Fuentes:** el código (`core/application/*`, `apps/api/routers/*`, `apps/cli/commands/*`,
`frontend/src/views/*`), `README.md`, `CLAUDE.md`, `docs/*.md` y el historial de git. Lo que el
sistema *debería* hacer sale de esas fuentes y de la lista «Comportamiento esperado» de abajo.
**No ejecutes la app contra `data/`, no llames a Gemini y no modifiques código.**

**Contenido** (en `docs/manual/MANUAL_FUNCIONAL.md`, en español):

1. Qué es y para quién: propósito, interfaces (web y CLI), modo local, nube e híbrido.
2. Conceptos: asignatura (slug y nombre), cronograma, clase (id, estado), parcial, material,
   nota en Obsidian, proyecto, guía offline, repaso, plugin práctico.
3. Datos: qué se guarda, dónde (archivo en `data/` o tabla en Postgres) y qué escribe fuera
   (bóveda de Obsidian, cuota de Gemini).
4. **Casos de uso**, uno por sección con id (`CU-01`…): actor, precondiciones, flujo principal
   en pasos numerados, flujos alternativos y errores, datos que lee y escribe, resultado
   esperado, y dónde está en el código (`archivo:línea`) y en la interfaz (vista o comando).
   Como mínimo: gestionar asignaturas (crear, renombrar, eliminar), subir y extraer un sílabo,
   editar el cronograma y los parciales, vaciar el cronograma, escanear e ingestar material,
   subir un archivo suelto, revisar y quitar lo ingestado, proyectos, tutoría, quiz, repaso,
   guía offline (crear, exportar, revisar, deshacer), plugins, ajustes, estadísticas, vaciar
   datos, migración.
5. Flujos de extremo a extremo del semestre (empezar el curso, una semana normal, antes de un
   parcial), enlazando los casos de uso.
6. **Discrepancias**: tabla con caso de uso, comportamiento esperado, comportamiento actual
   según el código (con `archivo:línea`) y gravedad. Es la parte más importante. Si algo ya
   está en `PENDIENTES.md`, cita la tarea.

Sin diagramas Mermaid (no salen en el PDF): flujos en pasos numerados y tablas.

**PDF:** `scripts/generar_manual.py` convierte el Markdown en `docs/manual/MANUAL_FUNCIONAL.pdf`
con `markdown-it-py` y `fitz.Story` de PyMuPDF (ya son dependencias; mira cómo lo hace el
exportador de guías en `infrastructure/`). Se versionan los dos.

**Comportamiento esperado** (indicado por el usuario):
- Una asignatura escrita con otra escritura (mayúsculas, sin tildes) es la misma; el nombre del
  catálogo no cambia salvo al renombrar.
- Vaciar el cronograma deja la asignatura en el catálogo, sin clases.
- Lo principal de Material es revisar lo ingestado; subir un archivo suelto es ocasional.
- Al subir archivos, la asignatura se elige de una lista.
- Las presentaciones `.pptx` se pueden ingestar, incluidas las que son solo imágenes.
- En la nube no se escanean carpetas locales; en modo híbrido sí.
- Cerrar una tutoría o revisar una guía marca la clase concreta (por id), no otra con el mismo
  tema; deshacer solo revierte lo que hizo esa acción.

**Aceptación:** todos los endpoints de `apps/api/routers/` y los comandos de `apps/cli/`
aparecen en algún caso de uso (al final, una tabla endpoint o comando → CU). Claude revisará una
muestra de casos contra el código. Commit `docs: D1 manual funcional`; las discrepancias no se
arreglan, solo se documentan.

### D2. Poner al día la documentación y limpiar restos

Hazla **después de D1**: el manual te da el inventario de lo que existe de verdad.

- **Borrar** (están obsoletos): `docs/TECHNICAL_WRITER_REPORT.md` (informe de octubre que aún
  llama al proyecto `ml-cli`) y `docs/CHANGELOG.md` (habla de agentes CrewAI que ya no existen;
  el historial de git hace de changelog). Quita los enlaces que apunten a ellos.
- **`README.md`**: que describa el sistema actual: qué es, requisitos (incluido LibreOffice si
  P16 ya está hecha), instalación con `backend/` y `frontend/`, arranque local, comandos de la
  CLI y enlaces a `docs/manual/`, `docs/ARCHITECTURE.md` y `docs/DESPLIEGUE.md`. Corto: el
  detalle va en el manual.
- **`docs/ARCHITECTURE.md`**: comprobar cada afirmación contra el código (capas, puertos,
  adaptadores, almacén de documentos, contratos de import-linter) y corregir lo que no
  coincida. Sin inventar: si algo no está en el código, no va.
- **`docs/DESPLIEGUE.md`**: comprobar contra `render.yaml`, `Dockerfile` y `deploy/`.
- **`GEMINI.md`**: reducirlo a «sigue `CLAUDE.md` y las reglas de `docs/PENDIENTES.md`» más los
  pasos de trabajo (tarea → verificación → commit → informe → detenerse), sin copiar las
  reglas, para que no se desincronicen.
- **No toques** `CLAUDE.md` ni `docs/PENDIENTES.md` (salvo «Hallazgos»): son las
  instrucciones de trabajo y las mantiene Claude. Si ves algo mal en ellos, anótalo en
  «Hallazgos».
- **Restos sin versionar** en la raíz (están ignorados por git, solo ocupan disco): borra
  `build/`, `modular_learning_cli.egg-info/`, `tests/` de la raíz (solo tiene `__pycache__`;
  los tests están en `backend/tests/`), `__pycache__/`, `.import_linter_cache/` y
  `.aider.chat.history.md`. **No borres `obsidian_vault/`** ni nada de `data/`: lo decide el
  usuario.

**Aceptación:** ningún documento menciona `ml-cli`, CrewAI ni rutas que no existan (compruébalo
con `git grep`). Todos los comandos del README funcionan copiándolos tal cual (pégalos con su
salida en el informe). Commit `docs: D2 documentacion al dia` y su informe aparte.

## Para decidir con el usuario (no implementar)

- **Material nuevo en la nube:** modo híbrido con ajustes por equipo, o leer de OneDrive con
  Microsoft Graph.
- **Medir la caché de `AlmacenPostgres`:** hay que medir la recarga en Render antes y después;
  `listar` sigue consultando Neon en cada llamada.
- **Extracción de evaluaciones del sílabo:** que `04_extraccion_silabo.md` capture los parciales
  en lugar de descartarlos, para no tener que definir a mano los cortes.
- **Tests de las vistas** (repaso, guía offline, confirmación): hace falta elegir la
  herramienta (Testing Library + jsdom).

## Hallazgos

*(Anota aquí lo que encuentres fuera del alcance de tu tarea.)*
