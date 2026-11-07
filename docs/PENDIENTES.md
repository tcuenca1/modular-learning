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
   No reescribas `docs/ARCHITECTURE.md` ni añadas documentos nuevos.

## Tareas (en orden de prioridad)

### P1. La tutoría web debe identificar la clase por su id

El backend ya acepta `clase_id` en `POST /api/tutoria` (`IniciarTutoria.clase_id`,
`TutoriaService.iniciar_sesion`), pero el frontend solo envía el tema, así que se usa la
primera clase pendiente con ese tema.

- `frontend/src/lib/asignaturas.ts`: `enlaceTutoria(materia, tema?, enfoque?, claseId?)`
  añade `clase_id` a la query si viene.
- Pasar el id donde se conoce: `CalendarioView.tsx:32`, `ProgresoView.tsx:58`, los enlaces de
  `RevisionGuiaView.tsx` (`ClaseGuia.clase_id`) y `HoyView.tsx`, que tiene su propio
  `enlaceTutoria` local en la línea 39: elimínalo y usa el de `lib/`.
- `frontend/src/views/TutoriaView.tsx`: lee `params.get('clase_id')` y lo envía en
  `api.iniciarTutoria`. Si el usuario cambia el tema a mano, deja de enviarlo.
- `frontend/src/api/types.ts`: añade `clase_id?: string` a la petición si no está.

**Aceptación:** test en `lib/asignaturas.test.ts` para `enlaceTutoria` con y sin id. Con dos
clases del mismo tema en fechas distintas, abrir la tutoría desde la segunda y cerrarla marca
como completada la segunda, no la primera (compruébalo con una copia de `data/examples`).

### P2. Deshacer la revisión de una guía solo debe deshacer lo que hizo esa guía

`GuiaOfflineService.deshacer_revision` (`core/application/guias.py`) borra del historial
todos los eventos `tipo == "guia"` con el mismo tema, aunque sean de otra guía, y pone como
pendientes clases que quizá ya estaban completadas antes de la guía.

- `RepasoService.registrar_estudio_offline` recibe `guia_id` y lo guarda en el evento.
- `registrar_revision` guarda en cada `ClaseGuia` el estado de la clase antes de marcarla
  (campo nuevo `estado_previo: str | None = None` en `core/domain/guia_offline.py`).
- `deshacer_revision` borra solo los eventos con ese `guia_id` y devuelve cada clase a su
  `estado_previo` (si es `None`, a `pendiente`).

**Aceptación:** tests en `tests/unit/application/test_guias_service.py`:
(a) dos guías con el mismo tema; deshacer una no toca los eventos de la otra;
(b) una clase ya completada antes de la guía sigue completada al deshacer.

### P3. Crear una guía debe avisar de las clases que no existen

`GuiaOfflineService.crear` solo falla si no encuentra ninguna clase; si falta alguna, la
ignora en silencio. Debe lanzar `ValueError` con las que faltan, como antes, comprobando por
id las que llegan como id y por tema las que llegan como tema.

**Aceptación:** test con `["<id válido>", "id-inexistente"]` que espera `ValueError` y nombra
`id-inexistente`.

### P4. Cronogramas guardados con el slug de la materia

El catálogo usa slug + nombre, pero los documentos siguen como
`schedules/INGENIERIA_DE_SOFTWARE_II_cronograma.json` y `listar_cronogramas` devuelve
"INGENIERIA DE SOFTWARE II".

- `JsonCronogramaRepo.guardar_cronograma` y `guardar_parciales`: los cronogramas nuevos se
  crean como `schedules/<slug>_cronograma.json` (con `slug_materia`, no con `_slug`).
- `listar_cronogramas` devuelve las claves como slug.
- Revisa los consumidores del frontend de `GET /api/materias/cronogramas`
  (`SilabosView`, `HoyView`, `lib/asignaturas.ts`…), que hoy cruzan los nombres con `clave()`,
  y muestra el nombre del catálogo.
- La búsqueda de cronogramas debe seguir siendo **exacta por slug** (no reintroduzcas
  coincidencias parciales: borrar "Ingenieria de Software" no debe tocar la "II"; hay un test
  en `test_adaptadores_disco.py` que debe seguir pasando).

**Aceptación:** tests de integración del repositorio: un cronograma nuevo se guarda con el
nombre del slug; uno antiguo en mayúsculas se sigue leyendo y `listar_cronogramas` lo
devuelve con su slug.

### P5. Migración de datos que también funcione en Neon

`scripts/migrar_datos.py` escribe directamente en `data/` y no sirve con Postgres.

- Reescríbelo sobre `AlmacenDocumentos` (`almacen_por_defecto()` de
  `infrastructure/persistence/almacen.py`) para que use archivos o Postgres según
  `DATABASE_URL`.
- Debe ser idempotente: asignar ids a las clases que no lo tengan, renombrar los
  cronogramas al slug (P4, si ya está hecha) y enlazar `clase_id` en las guías.
- Opción `--simular` que solo muestra lo que cambiaría.

**Aceptación:** test de integración con `AlmacenArchivos` sobre `tmp_path`: ejecutarlo dos
veces da el mismo resultado. **No lo ejecutes contra Neon ni contra `data/`:** eso lo hace el
usuario.

### P6. Tema claro con el sistema en oscuro

`frontend/src/index.css` aún tiene tres bloques `@media (prefers-color-scheme: dark)` (líneas
~128, ~172 y ~293; el último es `.prose`). Con el sistema en oscuro y la app en «claro», las
notas salen con texto claro sobre fondo claro.

- Sustitúyelos por selectores `html.dark …` (la variante `dark` ya está definida al inicio
  del archivo), y borra los `html.light …` que solo existían para contrarrestarlos.

**Aceptación:** con el sistema en oscuro, las tres opciones del selector (claro, oscuro,
sistema) se ven bien en una nota con `.prose` y en la guía imprimible. Describe en el commit
cómo lo comprobaste.

### P7. `en_nube` con una variable explícita

`apps/api/routers/config.py` deduce `en_nube` de `RENDER` o `DATABASE_URL`, así que en modo
híbrido (app local contra Neon) ocultaría el escaneo de carpetas. Usa solo la variable
`ML_EN_NUBE=1`, defínela en `render.yaml` y documéntala en `docs/DESPLIEGUE.md`.

**Aceptación:** test de API con y sin `ML_EN_NUBE` (usa `monkeypatch.setenv`).

### P8. Avisos de oxlint

`npm run lint` da 12 avisos (`MaterialView`, `SilabosView`, `PluginsView`, `ThemeToggle`):
dependencias de efectos que faltan, `setState` dentro de efectos y `catch (_err)` sin usar.
Corrígelos sin cambiar el comportamiento.

**Aceptación:** `npm run lint` sin avisos.

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
