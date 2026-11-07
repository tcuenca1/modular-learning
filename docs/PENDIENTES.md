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
10. **Prueba manual de verdad.** Si la tarea cambia efectos, estado o carga de datos de una
    vista, ábrela en el navegador y describe qué hiciste y qué viste. `lint` y `build` no
    cuentan como prueba manual.

## Tareas (en orden de prioridad)

### P9. Corregir la regresión de carga de P8

En `frontend/src/views/SilabosView.tsx`, `cargarCatalogo` llama a `setCargandoClases(true)` aunque
`destino` sea la materia que ya está activa. Pasa al renombrar (`cargarCatalogo(materiaActiva)`),
al crear una asignatura y al guardar un sílabo de la materia activa. Como `materiaActiva` no
cambia, el efecto que carga el cronograma no se vuelve a ejecutar y el panel se queda en
«cargando» para siempre.

- Que el cronograma se recargue también cuando `destino` es la materia activa (por ejemplo, un
  contador `recarga` en las dependencias del efecto, o extraer la carga a una función que use
  tanto el efecto como `cargarCatalogo`). Así, al guardar un sílabo de la materia activa se ven
  las clases nuevas.
- `frontend/src/views/MaterialView.tsx`: al cambiar de materia vuelve a mostrarse el indicador
  de carga de proyectos (antes de P8 lo hacía). Quita la duplicación entre el efecto y
  `cargarProyectos`/`cargarRegistrados` si se puede sin volver a los avisos de oxlint.
- Añade el salto de línea final de `SilabosView.tsx` y quita las dos líneas en blanco que quedaron
  en `HoyView.tsx` donde estaba el `enlaceTutoria` local.

**Aceptación:** `npm run lint` sigue sin avisos. **Prueba en el navegador** (con
`npm run dev` y la API sobre una copia de `data/examples`): renombrar la asignatura activa, crear
una asignatura y guardar un sílabo de la asignatura activa; en los tres casos el cronograma se
muestra y no se queda cargando. Cambiar de materia en Material muestra el indicador. Describe
en el informe qué viste.

### P10. Migración: no sobrescribir cronogramas al renombrar

En `scripts/migrar_datos.py`:

- Si `nueva_clave` ya existe en el almacén y es distinta de `clave`, **no escribas ni borres
  nada** para esa materia: muestra un aviso con las dos claves y súmalo a un contador nuevo
  `resumen["conflictos"]`. El usuario decidirá cuál conservar.
- `asignar_ids` devuelve `bool`, no un número: usa `sin_id` en los mensajes («3 ids nuevos») y
  en la condición de escritura.
- `venv/Scripts/ruff.exe check scripts` sin errores y `ruff format scripts/migrar_datos.py`
  (100 columnas, como el resto). Para las excepciones, captura `json.JSONDecodeError` en vez de
  `Exception` y avisa por pantalla del documento que no se pudo leer.

**Aceptación:** en `test_migracion.py`, un test con `schedules/REDES_cronograma.json` y
`schedules/redes_cronograma.json` con clases distintas: tras migrar, los dos siguen intactos y
`conflictos == 1`. El test de idempotencia sigue pasando.

### P11. Estadísticas con el nombre del catálogo

Desde P4, `listar_cronogramas` devuelve slugs y `TelemetriaService.obtener_estadisticas`
(`core/application/telemetria.py`) publica `materia.title()`: `ml stats` y `/api/stats` muestran
«Ingenieria-De-Software-Ii».

- `TelemetriaService` recibe `materia_repo: MateriaRepo | None = None` (conéctalo en
  `bootstrap.py`) y usa como clave el nombre del catálogo con `resolver_materia`
  (`core/domain/materias.py`); si la materia no está en el catálogo, usa el slug tal cual.
- Haz lo mismo en `EvaluacionService._nombre_materia` (`core/application/evaluacion.py`) con
  `resolver_materia` y borra su `_clave` local si queda sin uso.

**Aceptación:** test unitario de `TelemetriaService` con fakes: un cronograma con clave
`ingenieria-de-software-ii` y la materia «Ingeniería de Software II» en el catálogo da la clave
«Ingeniería de Software II» en `materias`; sin catálogo, la clave es el slug.

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
