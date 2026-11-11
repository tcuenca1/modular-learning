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

*(Sin tareas pendientes de implementación.)*

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

## Hallazgos

*(Anota aquí lo que encuentres fuera del alcance de tu tarea.)*
