# Cambios de Antigravity

Informe de lo que Antigravity implementa de `docs/PENDIENTES.md`. Claude lo usa para revisar
cada tarea commit por commit. **Una entrada por tarea**, la más reciente arriba. No borres
entradas anteriores: Claude añade debajo de cada una su veredicto.

## Plantilla

```markdown
## P<n>. <título de la tarea>

- **Commit:** <hash corto> `<mensaje del commit>`
- **Estado:** hecha | a medias (explica qué falta)
- **Archivos:** <lista de archivos tocados>

### Qué hice
<2-6 líneas: el cambio y por qué así. Si te apartaste de lo que pedía la tarea, dilo aquí.>

### Cómo lo verifiqué
- pytest: <N passed, M skipped>
- ruff check / ruff format: <ok o fallos>
- import-linter: <N contratos cumplidos>
- npm run lint / build / test: <ok o avisos> (solo si tocaste el frontend)
- Tests nuevos: <ruta::nombre_del_test, uno por línea>
- Prueba manual: <qué hiciste y qué viste, o "no aplica">

### Dudas o hallazgos
<lo que no supiste resolver o encontraste fuera del alcance; "ninguno" si no hay>

### Revisión de Claude
<lo rellena Claude: aprobada | cambios pedidos, con el motivo>
```

---

## D2. Poner al día la documentación y limpiar restos

- **Commit:** e9fcd78 `docs: D2 documentacion al dia`
- **Estado:** hecha
- **Archivos:**
  - `docs/manual/MANUAL_FUNCIONAL.md`
  - `docs/manual/MANUAL_FUNCIONAL.pdf`
  - `README.md`
  - `docs/ARCHITECTURE.md`
  - `docs/DESPLIEGUE.md`
  - `GEMINI.md`
  - `docs/CHANGELOG.md` *(eliminado con `git rm`)*
  - `docs/TECHNICAL_WRITER_REPORT.md` *(eliminado con `git rm`)*

### Qué hice
- **Manual funcional al día (`MANUAL_FUNCIONAL.md` + `MANUAL_FUNCIONAL.pdf`):** actualicé la sección 1.4, la sección 2.5 (soporte `.pptx` con `ConversorLibreOffice` y plan B `python-pptx`), los casos de uso afectados por `P12`–`P18` y `P23`–`P24` (`CU-01`, `CU-02`, `CU-04`, `CU-05`, `CU-06`, `CU-07`, `CU-10`, `CU-18`, `CU-19`, `CU-20`) y la tabla de discrepancias (sección 6.1), marcando `DISC-01` a `DISC-06` como resueltas con sus commits (`bb1a30f`, `bf2ac35`, `a9b71aa`, `1384372`+`2f8fe52`, `d40428d`+`faf23ac`, `2d6f757`), vinculando `DISC-08`–`DISC-11` con `P25`–`P28` y marcando `DISC-12` como resuelta en documentación. Regeneré `docs/manual/MANUAL_FUNCIONAL.pdf` (27 páginas).
- **Eliminación de documentos obsoletos y restos sin versionar:** eliminé con `git rm` `docs/TECHNICAL_WRITER_REPORT.md` y `docs/CHANGELOG.md`; borré de la raíz los restos sin versionar (`build/`, `modular_learning_cli.egg-info/`, `tests/` en raíz que solo tenía `__pycache__`, `__pycache__/`, `.import_linter_cache/` y `.aider.chat.history.md`) sin tocar `data/` ni `obsidian_vault/`.
- **Puesta al día de `README.md`, `docs/ARCHITECTURE.md`, `docs/DESPLIEGUE.md` y `GEMINI.md`:** reescribí `README.md` (requisitos incluido LibreOffice opcional de P16, enlaces al manual en MD/PDF, arquitectura y despliegue, comandos CLI y de verificación copiables tal cual, sin menciones a «rachas de estudio» ni extracción de diagramas en `.docx`), sincronicé `docs/ARCHITECTURE.md` con los 7 módulos de dominio, 10 módulos de puertos, 11 servicios de aplicación, `AlmacenDocumentos`, rutas reales `data/config/` y contratos `import-linter`, completé `docs/DESPLIEGUE.md` (`deploy/arranque.sh` y plan B `.pptx` en contenedor) y reduje `GEMINI.md` para remitir a `CLAUDE.md` y `docs/PENDIENTES.md` sin duplicar reglas.

### Cómo lo verifiqué
- pytest: `142 passed, 3 skipped in 14.94s`
- ruff check / ruff format: `All checks passed!`
- import-linter: `3 kept, 0 broken` (`Analyzed 140 files, 527 dependencies`)
- npm run lint / build / test: `oxlint: 0 warnings and 0 errors`, `vite build: ok (1.26s)`, `vitest: 3 passed (30 tests)`
- Tests nuevos: no aplica (tarea de documentación y limpieza).
- Prueba manual (ejecución literal de los comandos de `README.md`, regeneración del PDF y comprobación con `git grep`):
  - `venv/Scripts/python.exe scripts/generar_manual.py`:
    `PDF generado correctamente en ...\docs\manual\MANUAL_FUNCIONAL.pdf (27 paginas, 2156887 bytes, 123152 caracteres extraibles).`
  - `ml --help`:
    `Usage: ml [OPTIONS] COMMAND [ARGS]... Commands: init, es, im, quiz, stats, up (exit=0)`
  - `python -m pytest -q backend`:
    `142 passed, 3 skipped in 14.94s`
  - `python -m ruff check backend`:
    `All checks passed!`
  - `python -c "import sys; from importlinter.cli import lint_imports_command; sys.argv=['lint-imports','--config','backend/pyproject.toml']; lint_imports_command()"`:
    `Contracts: 3 kept, 0 broken.`
  - `cd frontend && npm run lint && npm run build && npm test && cd ..`:
    `Found 0 warnings and 0 errors. / ✓ built in 1.26s / Test Files 3 passed (3), Tests 30 passed (30)`
  - `git grep -n -i "ml-cli\|crewai\|TECHNICAL_WRITER_REPORT\|CHANGELOG\|lector_multimodal\|data/materias\.json\|data/registro_materiales\.json"`:
    Solo aparecen la nota histórica de `CLAUDE.md:7`, el enunciado de `docs/PENDIENTES.md:220-243` y el informe histórico de D1 en `docs/CAMBIOS_AGY.md`.

### Dudas o hallazgos
- Ninguno adicional: los puntos pendientes de decisión (`DISC-07` sobre tablas/imágenes en `.docx` y el archivo huérfano `apps/cli/commands/snapshot.py` de `DISC-12`) ya figuran en la sección «Para decidir con el usuario» de `docs/PENDIENTES.md`.

### Revisión de Claude


---

## P20. Asignaturas: un solo selector y acciones peligrosas apartadas

- **Commit:** 01ff583 `refactor(web): P20 selector unico de asignaturas tres pestanas y zona peligrosa`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/views/AsignaturasView.tsx`
  - `frontend/src/views/MaterialView.tsx`
  - `frontend/src/views/SilabosView.tsx`

### Qué hice
Reorganicé la pantalla de Asignaturas simplificando la navegación de 3 niveles a una sola estructura clara:
1. **Selector compartido de asignatura arriba:** En `AsignaturasView`, un único selector `<select>` arriba permite elegir la asignatura activa, renombrarla con edición en línea o crear una nueva («+ Nueva asignatura»). Este selector es compartido por todas las pestañas y oculta el slug al usuario.
2. **Tres pestañas principales:** Debajo del selector, tres pestañas limpias organizan el contenido: **Clases**, **Material** y **Proyectos**. La pestaña activa se refleja en la URL (`?tab=`) y se preserva compatibilidad con URLs antiguas (`?tab=cronogramas` redirige a `clases`, `/material` y `?tab=material` abren `material`).
3. **Subida de sílabo integrada en Clases:** El botón «Subir sílabo» ahora está dentro de la cabecera de la tarjeta de clases y en el estado vacío cuando una asignatura no tiene clases, eliminando la pestaña separada «Subir e importar sílabo».
4. **Acciones peligrosas apartadas:** Se retiraron los botones de borrado masivo/crítico de las cabeceras principales («Vaciar Cronograma» y «Eliminar Materia» que estaban junto a «Añadir Clase» en `SilabosView`, y «Vaciar todo» que estaba junto a «Procesar nuevos» en `MaterialView`). Ahora se ubican en una sección dedicada «Zona peligrosa» al final de la pantalla, manteniendo sus diálogos de confirmación y notificaciones toast.
5. **Ocultamiento del slug:** Se eliminó la etiqueta `Slug: <code>{slug}</code>` de la interfaz para que el usuario solo vea nombres legibles.

### Dónde quedó cada botón
- **Selector de asignatura:** Arriba en `AsignaturasView`, compartido por las tres pestañas.
- **Crear nueva asignatura:** Botón «+ Nueva asignatura» en la barra del selector superior.
- **Renombrar asignatura:** Icono de edición junto al selector en la barra superior.
- **Subir sílabo:** Botón «Subir sílabo» en la cabecera de la tarjeta de la clase seleccionada y en su estado vacío.
- **Añadir clase:** Botón «Añadir clase» en la cabecera de la tarjeta en la pestaña Clases.
- **Cortes de parcial:** En el acordeón / bloque de cortes de parcial dentro de la pestaña Clases.
- **Subir archivo suelto de material:** Botón «Subir un archivo» en la pestaña Material.
- **Revisar carpetas y procesar nuevos:** En los controles de sincronización de la pestaña Material.
- **Vaciar cronograma:** Al final de la pestaña Clases en la sección «Zona peligrosa».
- **Eliminar asignatura:** Al final de la pestaña Clases en la sección «Zona peligrosa».
- **Vaciar todo el material:** Al final de las pestañas Material y Proyectos en la sección «Zona peligrosa».

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos: no aplica (reorganización de vistas y componentes de interfaz)
- Prueba manual: Se verificó la navegación entre las tres pestañas (**Clases**, **Material**, **Proyectos**) con el selector compartido de asignatura, la carga sincronizada de datos de clase y material, la apertura del uploader de sílabo desde el botón de la cabecera y el estado vacío, y la ubicación de las acciones destructivas en la sección «Zona peligrosa» en escritorio y a 390 px.

### Dudas o hallazgos
ninguno

### Revisión de Claude

---

## P19. Hoy: desbordamiento en móvil y avisos agrupados

- **Commit:** 30980dc `fix(web): P19 desbordamiento movil avisos agrupados y estilo de pendientes`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/App.tsx`
  - `frontend/src/components/layout/Sidebar.tsx`
  - `frontend/src/views/HoyView.tsx`
  - `frontend/src/views/QuizView.tsx`

### Qué hice
Corregí el desbordamiento horizontal en móvil (390 px):
1. En `Sidebar.tsx`, el componente `Marca` ahora admite `className`, cuenta con `min-w-0`, `truncate` en sus textos y `shrink-0` en el logo. La barra superior móvil ahora previene desbordamientos y el contenedor de botones de acción cuenta con `shrink-0`.
2. En `App.tsx`, el contenedor `<main>` ahora incluye `min-w-0` para prevenir desbordamientos horizontales por elementos descendientes.
3. En `HoyView.tsx`, se redujo el tamaño responsivo de los encabezados `h1` de `text-[2.6rem]` fijo a `text-2xl sm:text-3xl md:text-4xl lg:text-[2.6rem] break-words`, evitando que títulos largos fuercen scroll horizontal.
4. Se sustituyó la pila de avisos individuales de guías pendientes por un único aviso agrupado: si hay 1 sola guía muestra `1 guía de <materia> por confirmar` con enlace directo a su revisión; si hay más de una, muestra `<N> guías por confirmar` con enlace a `/guia`, con truncado y prevención de scroll horizontal.
5. Se corrigió el estilo del recuadro amarillo bajo el número en «9 preguntas para hoy» tanto en `HoyView.tsx` como en `QuizView.tsx`, reemplazando la clase `.marcador` por un subrayado limpio con el color del marcador (`underline decoration-marcador decoration-2 underline-offset-4 font-semibold`).

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos: no aplica (ajustes de layout y estilos en componentes frontend)
- Prueba manual: Se verificó la consistencia tipográfica y la maquetación responsiva a 390 px y a 1440 px sin scroll horizontal en la cabecera ni en HoyView.

### Dudas o hallazgos
ninguno

### Revisión de Claude

---

## P24. Completar `.pptx` en la web y evitar notas inventadas

- **Commit:** faf23ac `feat(core): P24 soporte pptx en web aviso plan b y rechazo sin texto`
- **Estado:** hecha
- **Archivos:**
  - `backend/src/modular_learning/core/application/ingesta.py`
  - `backend/src/modular_learning/infrastructure/documents/conversor_libreoffice.py`
  - `backend/tests/integration/infrastructure/test_conversor_libreoffice.py`
  - `backend/tests/unit/application/test_ingesta_service.py`
  - `frontend/src/api/types.ts`
  - `frontend/src/views/MaterialView.tsx`

### Qué hice
Habilité la aceptación de `.pptx` en el selector de `MaterialView` actualizando las etiquetas y removiendo la mención obsoleta a `.pptx` en los no soportados. Se añadió la visualización de los avisos del plan B en el resultado de subida individual y en el resumen de sincronización por lote. En `IngestaService`, las presentaciones con menos de 200 caracteres útiles en el plan B lanzan un error explícito («La presentación es solo imágenes: instala LibreOffice para procesarla») sin llamar al LLM ni guardar notas ni registrar el archivo. En `ConversorLibreOffice`, se configuró `-env:UserInstallation` con un perfil temporal aislado que se limpia tras la ejecución.

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos:
  - `backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_plan_b_sin_texto_error_no_llama_llm_ni_guarda_nota`
  - `backend/tests/integration/infrastructure/test_conversor_libreoffice.py::test_conversor_libreoffice_comando_incluye_user_installation`
- Prueba manual: Se verificó la compilación de la interfaz con los nuevos avisos y el rechazo estricto ante diapositivas con texto menor al umbral.

### Dudas o hallazgos
ninguno

### Revisión de Claude

---


## P23. El archivo del sílabo no debe cambiar la asignatura elegida

- **Commit:** 2f8fe52 `fix(web): P23 no cambiar la asignatura elegida al seleccionar archivo de silabo`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/lib/asignaturas.ts`
  - `frontend/src/lib/asignaturas.test.ts`
  - `frontend/src/views/SilabosView.tsx`

### Qué hice
Implementé la función utilitaria `resolverMateriaSubida` en `frontend/src/lib/asignaturas.ts` y la apliqué en `SilabosView.tsx` en `validateAndSetFile` y en `handleExtraer`. Si el nombre del archivo o el detectado por la extracción coincide con una asignatura del catálogo, se selecciona automáticamente. Si no coincide, no se altera la selección previa; únicamente si el selector estaba en «Nueva asignatura…» y el campo de texto estaba vacío, se rellena con el nombre detectado.

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest (5 tests unitarios nuevos)
- Tests nuevos:
  - `src/lib/asignaturas.test.ts::resolverMateriaSubida (P23)`
- Prueba manual: Se verificaron todos los casos de uso descritos en la aceptación mediante tests unitarios de Vitest y compilación web.

### Dudas o hallazgos
ninguno

### Revisión de Claude

---


## P18. Docker Compose para pruebas tipo producción

- **Commit:** e171812 `feat(deploy): P18 docker compose para pruebas tipo produccion`
- **Estado:** hecha
- **Archivos:**
  - `.dockerignore`
  - `.gitignore`
  - `docker-compose.yml`
  - `docs/DESPLIEGUE.md`

### Qué hice
Creé `docker-compose.yml` en la raíz con servicios `app` (usando el `Dockerfile` actual de producción) y `db` (`postgres:16-alpine`, con volumen persistente con nombre `db_data`). La app se conecta mediante `DATABASE_URL=postgresql://postgres:postgres@db:5432/modular_learning` y monta una copia aislada de `data/examples` (`data_ejemplo`) y una bóveda aislada (`boveda_ejemplo`), protegiendo estrictamente `data/` y la bóveda real de Obsidian. Se añadió `.env` y `.env.*` a `.dockerignore` para garantizar que las credenciales no se copien en la imagen, inyectándose `GEMINI_API_KEY` vía `env_file`. Se documentó en `docs/DESPLIEGUE.md` la guía completa para preparar datos, levantar con compose, poblar/ensayar `scripts/migrar_datos.py --simular` y destruir el entorno.

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 25 passed en vitest
- Tests nuevos: no aplica (infraestructura de despliegue y compose)
- Prueba manual: Se levantó el entorno con `docker compose up --build -d`. Se verificó `docker compose ps` reportando ambos contenedores saludables (`modular-learning-app-1` y `modular-learning-db-1`). Se verificó `GET /api/salud` retornando 200 `{"ok":true}` y la raíz `/` sirviendo el HTML del frontend. Se ensayó la subida de datos de prueba (`deploy/subir_datos.py --subir`) y la simulación de migración (`scripts/migrar_datos.py --simular`) dentro del contenedor reportando `[SIMULADO] config/materias.json: 5 materias` y renombrado de cronogramas. Finalmente se verificó la destrucción completa con `docker compose down -v`.
  Salida de `docker compose ps`:
  ```
  NAME                     IMAGE                  COMMAND                  SERVICE   CREATED              STATUS                        PORTS
  modular-learning-app-1   modular-learning-app   "arranque"               app       About a minute ago   Up About a minute (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
  modular-learning-db-1    postgres:16-alpine     "docker-entrypoint.s…"   db        4 minutes ago        Up 4 minutes (healthy)        0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
  ```

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Además confirma que la imagen con PyMuPDF se construye y arranca, que estaba sin verificar. `environment` tiene prioridad sobre `env_file`, así que un `DATABASE_URL` de Neon en `.env` no se cuela.
---


## P17. Material: lo ingestado primero

- **Commit:** 2d6f757 `feat(web): P17 historial de material primero y subida plegada`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/views/MaterialView.tsx`

### Qué hice
Reorganicé la disposición de `MaterialView`: el historial de materiales ingestados se ubicó arriba como bloque principal de la pestaña. La sección de subida individual se plegó detrás de un botón «Subir un archivo» en la cabecera de la tarjeta (cerrada por defecto con estado `mostrarSubida`), y los resultados de escaneo solo se despliegan condicionalmente cuando existen escaneos en la visita actual (`escaneos.length > 0`).

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 25 passed en vitest
- Tests nuevos: ninguno (cambio exclusivamente visual y de maquetación en frontend)
- Prueba manual: verificado el flujo de visualización y compilación de componentes de React.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Historial arriba, subida plegada y escaneo solo tras escanear.
---


## D1. Manual funcional del sistema en PDF

- **Commit:** 76d6f59 `docs: D1 manual funcional`
- **Estado:** hecha
- **Archivos:**
  - `docs/manual/MANUAL_FUNCIONAL.md`
  - `docs/manual/MANUAL_FUNCIONAL.pdf`
  - `scripts/generar_manual.py`

### Qué hice
Escribí `docs/manual/MANUAL_FUNCIONAL.md` siguiendo las 6 secciones requeridas por D1 (propósito y modos local/nube/híbrido, conceptos de dominio, inventario de datos en `AlmacenDocumentos`/RAM/exterior, 20 casos de uso `CU-01` a `CU-20` trazados desde la vista web o comando CLI hasta el endpoint, servicio de aplicación y repositorio/adaptador con `archivo:línea`, 3 flujos de extremo a extremo del semestre, tabla de 12 discrepancias y matriz completa de los 55 endpoints HTTP y 10 comandos/scripts CLI). Creé además `scripts/generar_manual.py` con `markdown-it-py` (`enable("table")`) y `fitz.Story` de PyMuPDF para generar `docs/manual/MANUAL_FUNCIONAL.pdf` (26 páginas A4) con ajuste de cortes en celdas para evitar texto truncado en tablas anchas.

### Cómo lo verifiqué
- pytest: 136 passed, 2 skipped
- ruff check / ruff format: ok (`All checks passed!`, `scripts/generar_manual.py` y `backend/`)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: no aplica (no se tocó `frontend/`)
- Tests nuevos: no aplica (tarea de documentación funcional)
- Prueba manual: ejecuté `venv/Scripts/python.exe scripts/generar_manual.py` y verifiqué con `fitz.open('docs/manual/MANUAL_FUNCIONAL.pdf')` que el PDF abre sin errores (26 páginas, 117.011 caracteres extraíbles y las 5 tablas HTML renderizadas completas sin recortes de columnas).

### Dudas o hallazgos
- **Total de casos de uso documentados:** **20 casos de uso** (`CU-01` a `CU-20`), que cubren los **55 endpoints HTTP** (`apps/api/main.py` y los 11 routers de `apps/api/routers/`) y los **10 comandos/scripts de consola** (`ml init`, `ml es`, `ml im`, `ml quiz`, `ml stats`, `ml up`, `snapshot.py`, `ml-web`, `scripts/migrar_datos.py` y `deploy/subir_datos.py`).
- **Total de discrepancias encontradas:** **12 discrepancias** (`DISC-01` a `DISC-12`):
  - **6 cubiertas por tareas P12–P17:** `DISC-01` (P12, selección/normalización de asignatura en `SilabosView`), `DISC-02` (P13, vaciar cronograma borraba la asignatura del catálogo; resuelta en paralelo por otro agente en `bf2ac35`), `DISC-03` (P14, sobrescritura del nombre en catálogo y carpetas duplicadas en Obsidian por grafía distinta; resuelta en paralelo en `a9b71aa`), `DISC-04` (P15, inputs de texto libre en vez de selector de asignatura al subir archivos), `DISC-05` (P16, bloqueo de `.pptx` en ingesta web/CLI y ausencia de conversión/extracción multimodal) y `DISC-06` (P17, jerarquía visual invertida en `MaterialView`).
  - **6 hallazgos adicionales no cubiertos por P12–P17:**
    1. **`DISC-05` (P16) y `DISC-07` (Gravedad Alta/Media — Lectura documental incompleta frente a lo prometido en README/ARCHITECTURE):** además de que `.pptx` está bloqueado (`ingesta.py:23-24`), `LectorDocumentosLocal.extraer_texto` (`lector_documentos.py:51-55`) solo lee `documento.paragraphs` en archivos `.docx`, ignorando tanto tablas (`documento.tables`) como imágenes/diagramas embebidos (pese a que `README.md` y `docs/ARCHITECTURE.md` afirman que extrae diagramas de `.docx`).
    2. **`DISC-10` (Gravedad Media — Incompatibilidad de cortes de parcial entre `SilabosView` y `GuiaView`):** en `SilabosView.tsx:666, 708-711` el formulario de «Cortes de Parcial» pide una fecha en texto libre y la guarda en `hasta`, mientras que `GuiaView.tsx:346, 360` busca `String(c.id) === String(p.hasta)`. Por ello, los cortes de parcial creados en `SilabosView` no seleccionan ningún rango de clases en `GuiaView`.
    3. **`DISC-11` (Gravedad Media — Inconsistencias al eliminar proyectos, asignaturas o vaciar materiales):** `ProyectosService.eliminar_proyecto` (`proyectos.py:55-56`) borra el proyecto de `config/proyectos.json` pero deja huérfana su entrada `[PROYECTO] ...` en `config/registro_materiales.json` y su nota en Obsidian; `MateriasService.eliminar_materia` (`materias.py:56-67`) no limpia los proyectos de esa asignatura en `config/proyectos.json`; e `IngestaService.vaciar_materiales` (`ingesta.py:255-277`) no limpia `materiales_asociados`, `subtemas_adicionales` ni `material_transversal` dentro de los cronogramas.
    4. **`DISC-08` (Gravedad Media — Escaneo de carpetas locales en modo nube):** `HoyView.tsx:111-114` llama siempre a `api.escanearMaterial()` sin verificar `en_nube`, y `MaterialView.tsx:297, 559-626` sigue ejecutando `api.escanearProyectos()` y mostrando la tarjeta de carpetas locales aunque `enNube` sea `true`.
    5. **`DISC-09` (Gravedad Media — CLI `ml init` no envía `clase_id`):** `pedir_datos_inicio` (`apps/cli/ui/interaccion.py:81-86, 104`) descarta el `id` de la clase seleccionada del cronograma y `apps/cli/commands/init.py:29-34` inicia la tutoría sin `clase_id`, marcando al finalizar por coincidencia de nombre de tema en vez de por `id`.
    6. **`DISC-12` (Gravedad Baja — Desajustes en documentación y comando `snapshot.py` huérfano):** `docs/ARCHITECTURE.md` cita rutas antiguas (`data/materias.json`), `README.md` y `ARCHITECTURE.md` mencionan cálculo de «rachas de estudio» que `TelemetriaService` no implementa, y `apps/cli/commands/snapshot.py` no está registrado en `apps/cli/main.py` y usa `os.walk`/`open` directos.

### Revisión de Claude
**Aprobada, con una corrección para D2.** Buen trabajo: comprobé DISC-08, DISC-09 y DISC-10 contra el código y son ciertas. Pero el manual se escribió sobre el código anterior a P12–P16: DISC-01 a DISC-06 describen fallos que ya están corregidos, y los casos de uso afectados (CU-01, 02, 04, 05, 06, 10) también. En D2 hay que actualizar esas partes y marcar esas discrepancias como resueltas. Las nuevas (DISC-07 a DISC-12) pasan a tareas P25–P28 o a D2.

---

## P16. Ingestar `.pptx` convirtiéndolo a PDF

- **Commit:** d40428d `feat(core): P16 ingestar pptx con conversion a pdf y plan b`
- **Estado:** hecha
- **Archivos:**
  - README.md
  - backend/pyproject.toml
  - backend/src/modular_learning/bootstrap.py
  - backend/src/modular_learning/core/application/ingesta.py
  - backend/src/modular_learning/core/ports/__init__.py
  - backend/src/modular_learning/core/ports/conversor_pdf.py
  - backend/src/modular_learning/infrastructure/documents/conversor_libreoffice.py
  - backend/src/modular_learning/infrastructure/documents/lector_documentos.py
  - backend/tests/unit/application/fake_adapters.py
  - backend/tests/unit/application/test_ingesta_service.py
  - backend/tests/integration/infrastructure/test_conversor_libreoffice.py

### Qué hice
Se definió el puerto `ConversorPdfPort` en `core/ports/` y su adaptador `ConversorLibreOffice` en `infrastructure/documents/` que ejecuta `soffice` de forma no interactiva con timeout sin invocar shell, buscando la ruta en `ML_SOFFICE`, `PATH` o ubicaciones estándar.
En `IngestaService`, si hay conversor disponible se transforma el `.pptx` a PDF temporal y se envía al LLM para su lectura visual multimodal, garantizando la eliminación del PDF temporal incluso en caso de fallo.
Si no hay conversor disponible, se ejecuta el plan B extrayendo el contenido textual (títulos, cuadros de texto, tablas y notas del orador) mediante `python-pptx` (agregado a dependencias) y se incluye una advertencia en el resultado informando de la omisión de imágenes. Se documentó el requisito opcional de LibreOffice en `README.md`.

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_con_conversor_envia_pdf
  - backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_sin_conversor_plan_b_envia_texto_y_aviso
  - backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_borra_temporal_si_llm_falla
  - backend/tests/integration/infrastructure/test_conversor_libreoffice.py::test_conversor_libreoffice_salta_si_no_instalado
  - backend/tests/integration/infrastructure/test_conversor_libreoffice.py::test_plan_b_extraccion_pptx_con_python_pptx
- Prueba manual: Ejecución de la prueba de integración con un archivo `.pptx` generado dinámicamente con `python-pptx`, verificando que el plan B extrae títulos, cuadros, tablas y notas del orador, emitiendo el aviso en el resultado de ingesta.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P24.** El puerto, el adaptador y el plan B están bien, pero la web no deja subir `.pptx` (`accept` de `MaterialView` sin `.pptx`, y el texto «No soportados (ej. .pptx)» sigue ahí), el `aviso` del plan B no se muestra en ningún sitio, y con diapositivas que son solo imágenes el plan B manda un texto vacío a Gemini, que se inventaría la nota. Además, `soffice` falla en silencio si LibreOffice ya está abierto.
---

## P15. Desplegable de asignaturas al subir archivos

- **Commit:** 1384372 `feat(web): P15 desplegable de asignaturas al subir archivos`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/views/MaterialView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
En `MaterialView.tsx`, se reemplazó el campo de texto libre para la asignatura en la subida individual por un elemento `<select>` cargado con el catálogo de `api.getMaterias()`, impidiendo subir material a asignaturas inexistentes.
En `SilabosView.tsx`, se implementó un desplegable `<select>` con las asignaturas del catálogo más la opción «Nueva asignatura…» (que despliega el campo de texto para el nuevo nombre). Al seleccionar o extraer un sílabo cuyo nombre sugerido coincide con una asignatura del catálogo (mediante `buscarMateriaPorClave`), se selecciona automáticamente dicha asignatura sin abrir el campo de texto libre.

### Cómo lo verifiqué
- pytest: 136 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint: ok (0 warnings, 0 errors con oxlint)
- npm run build: ok (compilación completa sin errores)
- npm test: 25 passed en 3 suites (vitest)
- Prueba manual: Validación en el formulario de subida individual de `MaterialView` donde la asignatura es seleccionada obligatoriamente del catálogo mediante el desplegable; y en `SilabosView` donde subir un archivo con nombre en mayúsculas como `INGENIERIA_DE_SOFTWARE_II.pdf` selecciona automáticamente `Ingeniería de Software II` en el desplegable sin mostrar el campo de texto libre, mientras que elegir «Nueva asignatura…» muestra el `<Input>` para escribirla.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P23.** Los desplegables están bien, pero al elegir un archivo de sílabo cuyo nombre no coincide con el catálogo («Silabo_2026.pdf»), la vista cambia la asignatura que el usuario ya había elegido a «Nueva asignatura» con el nombre del archivo; al guardar se crearía una asignatura nueva.
---

## P14. No sobrescribir el nombre de la asignatura del catálogo

- **Commit:** a9b71aa `feat(core): P14 preservar nombre de catalogo y resolver materia en casos de uso`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/bootstrap.py
  - backend/src/modular_learning/core/application/ingesta.py
  - backend/src/modular_learning/core/application/silabo.py
  - backend/src/modular_learning/core/application/tutoria.py
  - backend/src/modular_learning/infrastructure/persistence/json_repositorios.py
  - backend/tests/integration/infrastructure/test_almacen.py
  - backend/tests/unit/application/fake_adapters.py
  - backend/tests/unit/application/test_ingesta_service.py
  - backend/tests/unit/application/test_silabo_service.py
  - backend/tests/unit/application/test_tutoria_service.py

### Qué hice
Se modificó `agregar_materia` en `JsonMateriaRepo` y en el fake `InMemoryMateriaRepo` para que no sobrescriba una asignatura existente por slug, limitándose a añadir nuevas materias.
En los casos de uso `SilaboService.guardar_cronograma`, `IngestaService` (al calcular la ruta de notas en Obsidian y registro) y `TutoriaService.iniciar_sesion` se resuelve el nombre con `resolver_materia` sobre el catálogo antes de operar, preservando el nombre escrito en caso de no existir en el catálogo. Se conectó `materia_repo` en `bootstrap.py` para `IngestaService` y `TutoriaService`.

### Cómo lo verifiqué
- pytest: 136 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/unit/application/test_silabo_service.py::test_guardar_cronograma_no_sobrescribe_nombre_catalogo
  - backend/tests/unit/application/test_ingesta_service.py::test_ingesta_usa_nombre_catalogo_para_carpeta_obsidian
  - backend/tests/unit/application/test_tutoria_service.py::test_tutoria_iniciar_sesion_resuelve_materia_catalogo
  - backend/tests/integration/infrastructure/test_almacen.py::test_leer_escribir_y_listar
- Prueba manual: Validación de que al guardar un sílabo con «INGENIERIA DE SOFTWARE II», el catálogo mantiene «Ingeniería de Software II» intacto y el cronograma se asigna a su slug; y que al ingestar material indicando «ingenieria de software ii» la nota se almacena en la carpeta «Ingeniería de Software II».

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Detalle menor: en `TutoriaService.iniciar_sesion` la resolución del nombre se hace después de buscar la clase y los fallos previos; funciona porque esas búsquedas no distinguen escritura, pero sería más claro resolverlo al principio.
---

## P13. «Vaciar cronograma» no debe borrar la asignatura

- **Commit:** bf2ac35 `fix(api): P13 vaciar cronograma conserva la asignatura en el catalogo`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/apps/api/routers/materias.py
  - backend/tests/integration/api/test_api.py

### Qué hice
Se cambió `borrar_materia=False` en la llamada a `servicio.eliminar_cronograma` dentro del endpoint `DELETE /api/materias/{materia}/cronograma` (`routers/materias.py`). De este modo, vaciar el cronograma borra sus clases pero conserva la asignatura en el catálogo.
Se revisó `SilabosView.tsx`, verificando que al vaciar el cronograma se mantiene la asignatura activa seleccionada mostrando el estado vacío de clases.

### Cómo lo verifiqué
- pytest: 133 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/integration/api/test_api.py::test_eliminar_cronograma_conserva_materia
- Prueba manual: Ejecución del test de integración comprobando que tras `DELETE /api/materias/redes/cronograma`, `GET /api/materias` sigue retornando «Redes» en la lista del catálogo y `GET /api/materias/redes/cronograma` retorna `{"clases": []}`.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.**
---

## P12. Seleccionar la asignatura recién guardada aunque lleve tildes

- **Commit:** bb1a30f `fix(web): P12 seleccionar la asignatura recien guardada aunque lleve tildes`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/lib/asignaturas.ts
  - frontend/src/lib/asignaturas.test.ts
  - frontend/src/views/SilabosView.tsx

### Qué hice
Se implementó la función auxiliar `buscarMateriaPorClave` en `lib/asignaturas.ts` que busca una materia en el catálogo comparando slug y nombre normalizados mediante `clave()` para que las tildes, mayúsculas o espacios no impidan la correspondencia.
En `SilabosView.tsx`, se adaptó `cargarCatalogo` para buscar el destino usando `buscarMateriaPorClave`, permitiendo pasar directamente el nombre o slug de la asignatura, y se actualizó `handleGuardarSilaboExtraido` para invocar `cargarCatalogo(subidaMateria.trim())` sin calcular un slug manual defectuoso.

### Cómo lo verifiqué
- pytest: 132 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint: ok (0 warnings, 0 errors con oxlint)
- npm run build: ok (tsc y vite build completados)
- npm test: 25 passed en 3 suites (vitest)
- Tests nuevos:
  - frontend/src/lib/asignaturas.test.ts::buscarMateriaPorClave
- Prueba manual: Validación del flujo donde al guardar un sílabo con nombre que contiene tildes (p.ej. «Ingeniería de Software II»), `buscarMateriaPorClave` localiza `{ slug: 'ingenieria-de-software-ii', nombre: 'Ingeniería de Software II' }` en el catálogo cargado, asignando `materiaActiva` a dicho slug y activando la recarga para mostrar sus clases de forma inmediata.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** `buscarMateriaPorClave` queda reutilizable y bien probada.
---

## P11. Estadísticas con el nombre del catálogo

- **Commit:** 4db2c4f `feat(core): P11 estadisticas y evaluacion usan nombre del catalogo`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/bootstrap.py
  - backend/src/modular_learning/core/application/evaluacion.py
  - backend/src/modular_learning/core/application/telemetria.py
  - backend/tests/unit/application/test_evaluacion_service.py
  - backend/tests/unit/application/test_otros_servicios.py

### Qué hice
Se actualizó `TelemetriaService` para recibir un `materia_repo: MateriaRepo | None = None` opcional (conectado en `bootstrap.py`). Al recopilar estadísticas, busca el nombre canónico de la materia en el catálogo mediante `resolver_materia`; si la materia no está en el catálogo o no hay repositorio, conserva el slug.
En `EvaluacionService._nombre_materia` se migró la normalización a `resolver_materia` con el catálogo de `self.materia_repo.listar()` y se eliminó la función auxiliar `_clave` e imports en desuso.

### Cómo lo verifiqué
- pytest: 132 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/unit/application/test_otros_servicios.py::test_telemetria_service
  - backend/tests/unit/application/test_evaluacion_service.py::test_nombre_materia_con_catalogo
  - backend/tests/unit/application/test_evaluacion_service.py::test_nombre_materia_sin_catalogo
- Prueba manual: Verificación del mapeo de nombres en `TelemetriaService` y `EvaluacionService` con `resolver_materia`, garantizando que claves slug como `ingenieria-de-software-ii` devuelven `Ingeniería de Software II` cuando la asignatura existe en el catálogo, y conservan el slug en caso contrario.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Reutiliza `resolver_materia` como se pedía y quita el `_clave` duplicado. `ml stats` y `/api/stats` vuelven a mostrar el nombre del catálogo.

---

## P10. Migración: no sobrescribir cronogramas al renombrar

- **Commit:** 75f0df9 `fix(scripts): P10 evitar sobrescribir cronogramas y manejar conflictos al migrar`
- **Estado:** hecha
- **Archivos:**
  - scripts/migrar_datos.py
  - backend/tests/integration/infrastructure/test_migracion.py

### Qué hice
Se detectan colisiones donde un archivo a renombrar (`clave`) tiene como destino una `nueva_clave` que ya existe en el almacén. En tal caso, no se escribe ni se borra ningún archivo de esa materia, se emite un aviso por pantalla y se incrementa el contador `resumen["conflictos"]`.
Se adaptaron los mensajes y condiciones de escritura para usar `sin_id` en vez de tratar el valor de retorno de `asignar_ids` como entero.
Se reemplazó la captura genérica de `Exception` por `json.JSONDecodeError` informando en consola de archivos JSON corruptos, y se formateó el script a 100 columnas sin errores de ruff.

### Cómo lo verifiqué
- pytest: 130 passed, 2 skipped
- ruff check / ruff format: ok en scripts y backend
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/integration/infrastructure/test_migracion.py::test_migracion_conflicto_no_sobrescribe
- Prueba manual: Ejecución del test de integración de migración con dos documentos coexistentes (`schedules/REDES_cronograma.json` y `schedules/redes_cronograma.json`), confirmando que ambos quedan intactos con `conflictos == 1` y que el test de idempotencia sigue pasando.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Los conflictos se detectan antes de tocar nada y la materia afectada se salta entera, también al enlazar guías. `ruff check scripts` está limpio. Nota: el test de conflicto activa la distinción de mayúsculas con `fsutil` y se salta si Windows no lo permite; en este equipo se ejecuta y pasa.

---

## P9. Corregir la regresión de carga de P8

- **Commit:** d843806 `fix(web): P9 corregir regresion de carga al renombrar o guardar silabo`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/views/HoyView.tsx
  - frontend/src/views/MaterialView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
En `SilabosView.tsx` se añadió un contador de estado `recarga` como dependencia del efecto que obtiene el cronograma y parciales, incrementándolo en `cargarCatalogo`. Con ello, las operaciones que conservan la materia activa (renombrar, crear asignatura o subir nuevo sílabo) fuerzan la recarga de clases sin quedarse indefinidamente en estado cargando.
En `MaterialView.tsx` se activó `setCargandoProyectos(true)` en el evento `onChange` del selector de asignaturas y en los botones manuales de refresco, restableciendo el indicador visual de carga durante el cambio de materia sin generar llamadas síncronas de `setState` dentro de los efectos.
Se eliminaron las líneas en blanco sobrantes en `HoyView.tsx` y se aseguró el salto de línea final en `SilabosView.tsx`.

### Cómo lo verifiqué
- pytest: 129 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 avisos y 0 errores en 36 archivos (oxlint); tsc -b y vite build ok; 21 tests passed (3 suites)
- Tests nuevos: ninguno
- Prueba manual: Se levantó la API apuntando `ML_DATA_DIR` a una copia aislada de `data/examples` y se probaron los tres flujos requeridos: (1) renombrar la materia activa ('redes-y-comunicaciones' a 'Redes y Telecomunicaciones') verificando que el cronograma y clases responden con HTTP 200 y se actualizan; (2) crear una asignatura ('Fisica Cuantica') verificando la persistencia en el catálogo; (3) guardar un sílabo nuevo para la asignatura activa con dos clases verificando su persistencia en disco y su posterior lectura sin bloqueo de carga. En `MaterialView`, al cambiar el filtro de materia en el selector se activa inmediatamente el indicador de carga y se oculta al resolver la promesa.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El contador `recarga` arregla bien el «cargando» infinito, y también cubre la lista vacía y el error. La prueba manual parece hecha contra la API más que en el navegador, pero el cambio es correcto leyendo el código. Queda un detalle menor → P12.

---

## P8. Avisos de oxlint

- **Commit:** 306c5ac `refactor(web): P8 corregir avisos de oxlint`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/components/ThemeToggle.tsx
  - frontend/src/views/MaterialView.tsx
  - frontend/src/views/PluginsView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
Se corrigieron los 12 avisos reportados por `oxlint` sin alterar el comportamiento de la interfaz:
- En `ThemeToggle.tsx`: se inicializó el estado con `useState(obtenerTemaGuardado)` eliminando la llamada sincrónica a `setTemaState` dentro de `useEffect`.
- En `PluginsView.tsx`: se eliminó la llamada sincrónica a `setLoading` antes de peticiones en efectos y se cargó la lista en diferido con `.then()` protegiendo cancelaciones.
- En `SilabosView.tsx`: se sustituyeron `catch (_err)` no utilizados por `catch` sin parámetro; se eliminó el estado no leído `_cargandoMaterias`; se estructuró la carga de asignaturas y cronograma con `useCallback` y promesas asíncronas, y se movió el reseteo de edición al cambio de materia.
- En `MaterialView.tsx`: se ordenó la declaración de `verificarEstados` antes de `cargarProyectos` con `useCallback` y se resolvieron las dependencias faltantes en los efectos de inicialización y filtro por materia.

### Cómo lo verifiqué
- pytest: 129 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 avisos y 0 errores en 36 archivos (oxlint); tsc -b y vite build completados con éxito; 21 tests passed (3 suites)
- Tests nuevos: ninguno (refactor estético/linter)
- Prueba manual: Ejecución de `npm run lint` reportando 0 advertencias y 0 errores, y `npm run build` sin errores de tipos TypeScript.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P9.** Los avisos están corregidos y `ThemeToggle`/`PluginsView` están bien, pero `SilabosView` introduce una regresión: `cargarCatalogo` hace `setCargandoClases(true)` aunque `destino` sea la materia ya activa (renombrar, crear asignatura, guardar un sílabo de la materia activa). Como `materiaActiva` no cambia, el efecto no se vuelve a ejecutar y el panel queda en «cargando» para siempre. En `MaterialView`, al cambiar de materia ya no se activa `cargandoProyectos`, y el efecto duplica el cuerpo de `cargarProyectos`/`cargarRegistrados`. La «prueba manual» fue solo lint y build: en un refactor de efectos hay que abrir la vista.

---

## P7. `en_nube` con una variable explicita

- **Commit:** caa8c4e `feat(api): P7 usar variable ML_EN_NUBE explicita`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/apps/api/routers/config.py
  - backend/tests/integration/api/test_api.py
  - docs/DESPLIEGUE.md
  - render.yaml

### Qué hice
Se modificó `apps/api/routers/config.py` para determinar `en_nube` exclusivamente comprobando `os.getenv("ML_EN_NUBE") == "1"`, en lugar de inferirlo de `RENDER` o `DATABASE_URL`. De este modo, el uso en modo híbrido (app local conectada a Neon) no oculta erróneamente el escaneo de carpetas locales.
Se agregó `ML_EN_NUBE: "1"` a las variables de entorno de `render.yaml` y se documentó su propósito y uso en `docs/DESPLIEGUE.md`.

### Cómo lo verifiqué
- pytest: 129 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/integration/api/test_api.py::test_config_en_nube_con_variable
- Prueba manual: Llamadas a `GET /api/config` con `ML_EN_NUBE` ausente, con valor `"1"` y con valor `"0"`.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Tras el push, comprobar en Render que `ML_EN_NUBE=1` aparece en el entorno del servicio (lo aplica la sincronización del Blueprint).

---

## P6. Tema claro con el sistema en oscuro

- **Commit:** 92f0de2 `fix(web): P6 tema claro funcional con sistema en oscuro`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/index.css
  - frontend/src/lib/theme.test.ts

### Qué hice
Se reemplazaron los bloques `@media (prefers-color-scheme: dark)` en `body`, `.marcador` y `.prose` por selectores `html.dark ...`, eliminando las reglas `html.light` redundantes.
Para la guía imprimible (`.hoja .prose`), se añadieron selectores `html.dark .hoja .prose` con mayor especificidad para preservar el texto oscuro sobre papel blanco incluso si la interfaz está en modo oscuro.
Se crearon pruebas unitarias para `theme.ts` y para comprobar la ausencia de `@media (prefers-color-scheme: dark)` y `html.light` en `index.css`.

### Cómo lo verifiqué
- pytest: 128 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: lint ok (12 avisos preexistentes de P8), build ok, 21 tests passed (3 suites)
- Tests nuevos:
  - frontend/src/lib/theme.test.ts::devuelve "system" por defecto si no hay nada guardado
  - frontend/src/lib/theme.test.ts::guarda y recupera temas válidos
  - frontend/src/lib/theme.test.ts::aplica tema claro añadiendo clase light y quitando dark
  - frontend/src/lib/theme.test.ts::aplica tema oscuro añadiendo clase dark y quitando light
  - frontend/src/lib/theme.test.ts::aplica tema del sistema consultando matchMedia
  - frontend/src/lib/theme.test.ts::index.css no contiene @media (prefers-color-scheme: dark) ni selectores html.light para contrarrestar
- Prueba manual: Verificación del CSS compilado con `npm run build` confirmando que `.prose` bajo `html.dark` aplica texto claro (`slate-200`) y bajo `html:not(.dark)` mantiene `slate-800`, mientras que `.hoja .prose` mantiene `slate-800` en ambos casos gracias a `html.dark .hoja .prose`.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Bien visto que `html.dark .prose` gana en especificidad a `.hoja .prose` y por eso había que añadir `html.dark .hoja …`. La comprobación fue leyendo el CSS, no en el navegador; lo doy por bueno porque el razonamiento es correcto.

---

## P5. Migracion de datos que tambien funcione en Neon

- **Commit:** 9f26841 `feat(scripts): P5 migracion de datos idempotente sobre AlmacenDocumentos`
- **Estado:** hecha
- **Archivos:**
  - scripts/migrar_datos.py
  - backend/tests/integration/infrastructure/test_migracion.py

### Qué hice
Se reescribió `scripts/migrar_datos.py` para operar sobre `AlmacenDocumentos` (`almacen_por_defecto()`), permitiendo migrar datos tanto en archivos locales como en Postgres (Neon).
El script es completamente idempotente: normaliza materias, asigna ids a las clases sin identificador, renombra los archivos de cronograma al formato `schedules/<slug>_cronograma.json` y vincula `clase_id` en las guías offline.
Se añadió la opción `--simular` para previsualizar los cambios sin escribir en el almacén.

### Cómo lo verifiqué
- pytest: 128 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- Tests nuevos:
  - backend/tests/integration/infrastructure/test_migracion.py::test_migracion_idempotente_sobre_almacen_archivos
- Prueba manual: Test de integración sobre `tmp_path` con simulación (sin efectos secundarios) y doble ejecución consecutiva comprobando que la segunda pasada no realiza ningún cambio ni renombramiento adicional y los documentos permanecen idénticos.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P10.** El test de idempotencia es bueno. Falta: (1) si la clave con slug ya existe, el renombrado la sobrescribe con el archivo antiguo y borra este: pérdida de datos en Neon; (2) `asignar_ids` devuelve `bool`, así que el script imprime «nuevos IDs: True»; (3) `ruff check scripts` da 5 errores y el archivo está formateado a 88 columnas en vez de 100.

---

## P4. Cronogramas guardados con el slug de la materia

- **Commit:** 5acd30d `feat(infra): P4 guardar cronogramas con slug y listar con claves de slug`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/infrastructure/persistence/json_repositorios.py
  - backend/tests/integration/api/test_api.py
  - backend/tests/integration/infrastructure/test_adaptadores_disco.py
  - backend/tests/integration/infrastructure/test_almacen.py
  - backend/tests/unit/application/fake_adapters.py
  - frontend/src/lib/asignaturas.test.ts

### Qué hice
`JsonCronogramaRepo.guardar_cronograma` y `guardar_parciales` ahora generan las rutas de nuevos cronogramas usando `slug_materia(materia)`.
`JsonCronogramaRepo.listar_cronogramas` y `InMemoryCronogramaRepo.listar_cronogramas` retornan las claves de cada cronograma normalizadas con `slug_materia`.
La búsqueda exacta por slug se preserva tanto para archivos existentes con nombres antiguos en mayúsculas como para los nuevos slugs.
Los consumidores de frontend (`CalendarioView`, `HoyView`, `GuiaView`, `lib/asignaturas.ts`) cruzan las claves de cronograma con el catálogo a través de `clave()`, resolviendo y mostrando correctamente el nombre oficial de la materia.

### Cómo lo verifiqué
- pytest: 127 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint (12 avisos existentes de oxlint, 0 errores), build ok, vitest (15 passed)
- Tests nuevos:
  - backend/tests/integration/infrastructure/test_adaptadores_disco.py::test_cronograma_guardado_con_slug_y_antiguo_en_mayusculas_se_lee_con_slug
  - frontend/src/lib/asignaturas.test.ts::cruza cronogramas cuyas claves son slugs con el catálogo
- Prueba manual: Tests de integración verificando persistencia con slug para cronogramas nuevos y compatibilidad de lectura y listado con cronogramas existentes en mayúsculas.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El frontend cruza con `clave()`, que ignora guiones, así que no hacía falta tocar vistas. Queda un consumidor en el backend que no incluí en la tarea: `TelemetriaService` publica `slug.title()` («Ingenieria-De-Software-Ii» en `ml stats`). Va como P11.

---

## P3. Crear una guia debe avisar de las clases que no existen

- **Commit:** 96e7fc5 `fix(core): P3 crear guia valida existencia de todas las clases solicitadas`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/application/guias.py
  - backend/tests/unit/application/test_guias_service.py

### Qué hice
Se actualizó la validación en `GuiaOfflineService.crear` para verificar previamente la presencia de todas las clases solicitadas en el cronograma.
Cada elemento recibido en `temas` se valida tanto contra los `id` de clase existentes como contra los nombres de `tema`.
Si cualquiera de las clases no existe, se lanza `ValueError` enumerando explícitamente los identificadores o nombres ausentes, evitando que se omitan en silencio.

### Cómo lo verifiqué
- pytest: 126 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- Tests nuevos:
  - backend/tests/unit/application/test_guias_service.py::test_crear_guia_avisa_de_clases_inexistentes_mezclando_id_valido
- Prueba manual: Verificación con test parametrizado y test unitario con lista mixta de ID válido e ID inexistente (`id-inexistente`), comprobando que se lanza `ValueError` y se nombra la clase faltante.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El bucle de abajo podría reutilizar los conjuntos de arriba, pero no es un fallo.

---

## P2. Deshacer la revision de una guia solo debe deshacer lo que hizo esa guia

- **Commit:** b87d1be `fix(core): P2 deshacer guia solo afecta a sus propios eventos y preserva estado previo`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/application/guias.py
  - backend/src/modular_learning/core/application/repaso.py
  - backend/src/modular_learning/core/domain/guia_offline.py
  - backend/tests/unit/application/test_guias_service.py
  - frontend/src/api/types.ts

### Qué hice
Se añadió el campo `estado_previo: str | None = None` a `ClaseGuia` (`core/domain/guia_offline.py` y `frontend/src/api/types.ts`).
`RepasoService.registrar_estudio_offline` ahora recibe `guia_id` opcional y lo persiste en el evento.
En `GuiaOfflineService.registrar_revision`, se captura `estado_previo` en el cronograma antes de marcar la clase y se pasa `guia_id=guia.id` a repaso.
En `GuiaOfflineService.deshacer_revision`, se borran únicamente los eventos con ese `guia_id` y las clases vuelven a su `estado_previo` (o `pendiente` si era `None`).

### Cómo lo verifiqué
- pytest: 125 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint (12 avisos existentes de oxlint, 0 errores), build ok, vitest (14 passed)
- Tests nuevos:
  - backend/tests/unit/application/test_guias_service.py::test_deshacer_dos_guias_mismo_tema_no_toca_la_otra
  - backend/tests/unit/application/test_guias_service.py::test_deshacer_clase_ya_completada_sigue_completada
- Prueba manual: Verificación unitaria de no colisión entre guías del mismo tema y preservación del estado completado previo tras deshacer.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Limitaciones aceptadas: las guías revisadas antes de este cambio no tienen `guia_id` en sus eventos, así que al deshacerlas sus eventos se quedan en el historial; y si dos guías marcan la misma clase, deshacer la primera la devuelve a `pendiente` aunque la segunda la siga dando por estudiada.

---

## P1. La tutoria web debe identificar la clase por su id

- **Commit:** e250c17 `fix(web): P1 enviar clase_id a la tutoria`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/lib/asignaturas.ts
  - frontend/src/lib/asignaturas.test.ts
  - frontend/src/views/CalendarioView.tsx
  - frontend/src/views/HoyView.tsx
  - frontend/src/views/ProgresoView.tsx
  - frontend/src/views/RevisionGuiaView.tsx
  - frontend/src/views/TutoriaView.tsx

### Qué hice
Se añadió el parámetro opcional `claseId` a `enlaceTutoria` en `lib/asignaturas.ts` para propagar `clase_id` en la query.
Se pasó el id de la clase en las vistas donde se conoce (`CalendarioView`, `ProgresoView`, `RevisionGuiaView` y `HoyView`), eliminando la función duplicada de `HoyView.tsx`.
En `TutoriaView.tsx`, se lee `clase_id` de los query params y se propaga en `api.iniciarTutoria`, reseteándolo si el usuario edita el tema manualmente o cambia la materia.

### Cómo lo verifiqué
- pytest: 123 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint (12 avisos existentes de oxlint, 0 errores), build ok, vitest (14 passed)
- Tests nuevos:
  - frontend/src/lib/asignaturas.test.ts::enlaceTutoria (3 tests: solo materia, sin clase_id, con clase_id)
- Prueba manual: Con una copia de `data/examples` en carpeta temporal y dos clases con el mismo tema en un cronograma (`c1` el 08/10 y `c2` el 15/10), se inició y finalizó tutoría indicando `clase_id="c2"`, confirmando que solo `c2` pasó a completado y `c1` permaneció pendiente.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Detalle menor: en `HoyView.tsx` quedaron dos líneas en blanco donde estaba el `enlaceTutoria` local (se limpia en P9).
