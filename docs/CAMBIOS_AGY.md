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
<!-- lo rellena Claude -->

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
<!-- lo rellena Claude -->

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
<!-- lo rellena Claude -->

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
*(Pendiente de revisión)*

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
*(Pendiente de revisión)*

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
*(Pendiente de revisión)*

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
*(Pendiente de revisión)*

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
*(Pendiente de revisión)*
