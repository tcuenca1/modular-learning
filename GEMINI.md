# Protocolo de Trabajo para Antigravity en Modular Learning

Este proyecto sigue una disciplina estricta de desarrollo basada en arquitectura hexagonal, pruebas automatizadas y trazabilidad de cambios. Antigravity debe apegarse rigurosamente a las normas de `CLAUDE.md` y al flujo de `docs/PENDIENTES.md`.

---

## 1. Reglas Generales del Repositorio (heredadas de `CLAUDE.md`)

- **Arquitectura Hexagonal (no negociable):**
  - El núcleo (`core/`) no realiza I/O directo: prohibido el uso de `open`, `os.walk`, `os.listdir`, `os.remove`, `os.stat`, `os.path.isdir/isfile/exists`, `print` o `settings` (`os.path.join/splitext/basename` sí están permitidos).
  - Cualquier interacción con el exterior (disco, LLM, APIs) debe hacerse a través de puertos en `core/ports/`, implementados en adaptadores dentro de `infrastructure/`.
  - Al añadir o modificar métodos en un puerto, actualizar siempre el fake correspondiente en `backend/tests/unit/application/fake_adapters.py`.
- **Datos y entorno protegidos:**
  - Prohibido modificar o alterar `data/` (datos de usuario) o `.env`. Para pruebas que requieran datos, usar copias temporales apuntadas mediante `ML_DATA_DIR` o fixtures en `tmp_path` (solo en tests de integración).
- **Idioma y convenciones:**
  - Código, docstrings, identificadores y mensajes de error en **español**.
  - Commits en **español, sin tildes**, siguiendo formato Conventional Commits: `<tipo>(<scope>): P<n> <descripcion>`.
- **Alcance estricto:**
  - Implementar exclusivamente lo solicitado por la tarea. No realizar refactors oportunistas, renombrados ni funcionalidades extra. Si se detecta un problema adicional, registrarlo en la sección «Hallazgos» al final de `docs/PENDIENTES.md`.

---

## 2. Flujo de Trabajo Tarea por Tarea (`PENDIENTES.md`)

Cada pendiente debe resolverse de forma estrictamente individual y secuencial (una a una), siguiendo el orden de prioridad definido (`P1`, `P2`, etc.):

### Paso 1: Implementación y Tests
1. Leer detenidamente la descripción y los criterios de aceptación de la tarea en `docs/PENDIENTES.md`.
2. Realizar los cambios mínimos y necesarios en el código.
3. Si cambia un comportamiento descrito en `README.md`, `docs/DESPLIEGUE.md` o `CLAUDE.md`, actualizarlo en este mismo paso.
4. Escribir o actualizar las pruebas unitarias/integración correspondientes a la tarea.

### Paso 2: Verificación de Calidad (Todo en Verde)
Antes de realizar cualquier commit, deben pasar con éxito todas las comprobaciones desde la raíz del proyecto:

```bash
# Backend: tests, formato y linting
venv/Scripts/python.exe -m pytest -q backend
venv/Scripts/ruff.exe check backend
venv/Scripts/ruff.exe format <archivos_py_tocados>
venv/Scripts/python.exe -c "import sys; from importlinter.cli import lint_imports_command; sys.argv=['lint-imports','--config','backend/pyproject.toml']; lint_imports_command()"

# Frontend (si se modificó código en frontend/)
cd frontend && npm run lint && npm run build && npm test
```

### Paso 3: Commit de la Tarea
Hacer el commit de la implementación con el id de la tarea y en rama `main`:
```bash
git add <archivos tocados>
git commit -m "<tipo>(<scope>): P<n> <descripcion>"
# Ejemplo: git commit -m "fix(web): P1 enviar clase_id a la tutoria"
```

### Paso 4: Registro en `docs/CAMBIOS_AGY.md`
Añadir una nueva entrada al principio de `docs/CAMBIOS_AGY.md` (la más reciente arriba, debajo de `## Plantilla` y separador) completando todos los campos con la información real:
- **Commit:** Hash corto del commit del Paso 3 + mensaje.
- **Estado:** `hecha` (o `a medias` con explicación de qué falta).
- **Archivos:** Lista de archivos tocados.
- **Qué hice:** 2 a 6 líneas explicando el cambio técnico y su justificación.
- **Cómo lo verifiqué:** Salidas resumidas de `pytest`, `ruff`, `import-linter`, `npm` (si aplica), tests nuevos añadidos y prueba manual efectuada.
- **Dudas o hallazgos:** Aspectos fuera del alcance o "ninguno".

### Paso 5: Commit del Informe
Hacer un commit independiente para la documentación del informe:
```bash
git add docs/CAMBIOS_AGY.md
git commit -m "docs: P<n> informe en CAMBIOS_AGY"
```

### Paso 6: Control de Flujo y Pausa
- **No borrar la tarea de `docs/PENDIENTES.md`:** La tarea permanece allí hasta que Claude o el usuario verifiquen y aprueben la revisión.
- **Detenerse:** Una vez completado el commit del informe, Antigravity debe detenerse, presentar al usuario el resumen del trabajo realizado y esperar su visto bueno antes de iniciar la siguiente tarea (salvo que el usuario haya indicado explícitamente el modo continuo o el comando `/goal`).
