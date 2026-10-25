# CLAUDE.md

Guía para trabajar en **Modular Learning**: tutor académico con IA (Gemini) que ingesta material de clase, lo alinea con el cronograma del sílabo y lo publica como notas en Obsidian. Tiene dos interfaces sobre el mismo núcleo: CLI `ml` (Typer) y web `ml-web` (FastAPI + React).

## Comandos

Usar siempre el intérprete del venv con `python -m`. Varios `.exe` de `venv/Scripts/` apuntan a la ruta antigua `ml-cli` y fallan en silencio.

```bash
venv/Scripts/python.exe -m pytest -q                 # tests (unit + integración)
venv/Scripts/ruff.exe check src tests                # lint (también lo corre CI)
venv/Scripts/ruff.exe format <archivos tocados>      # formato (pre-commit usa ruff-format)
venv/Scripts/lint-imports.exe                        # contratos de arquitectura
venv/Scripts/python.exe -m pip install -e ".[all]"   # reinstalar el paquete si cambia pyproject
```

Frontend (`frontend/`, React 19 + Tailwind v4 + Vite):

```bash
npm run build      # tsc -b && vite build → genera src/modular_learning/apps/api/static/
npm run lint       # oxlint
npm run dev        # Vite en :5173 (proxy a la API en :8000)
```

Servidor web: `.claude/launch.json` → configuración `ml-web` en el puerto 8000. Sirve el build compilado en `apps/api/static`, así que después de editar `frontend/src` hay que ejecutar `npm run build`.

## Arquitectura hexagonal (no negociable)

```
src/modular_learning/
├── core/domain/        lógica pura (alineación curricular, parseo JSON del LLM)
├── core/ports/         ABCs: LLMPort, CronogramaRepo, MateriaRepo, RegistroMaterialesRepo,
│                       LectorDocumentosPort, BovedaNotasPort, AjustesPort, PluginPracticoBase
├── core/application/   casos de uso (*Service) que solo reciben puertos por constructor
├── infrastructure/     adaptadores: Gemini, JSON en disco, Obsidian, lector de documentos, plugins
├── apps/api|cli/       adaptadores de entrada (routers FastAPI, comandos Typer)
├── bootstrap.py        composition root: único lugar donde se instancian y conectan
└── settings.py         rutas de datos (ML_DATA_DIR); solo lo usan infraestructura y bootstrap
```

Reglas que hacen cumplir `import-linter` (ver `pyproject.toml`) y la revisión:

- `core` no hace I/O: nada de `open`, `os.walk`, `print`, `settings`, `pypdf`, `docx` ni `dotenv`. Si un caso de uso necesita disco, se añade un método al puerto y se implementa en el adaptador.
- `core.domain` no importa `core.application`; `infrastructure` no importa `apps`, `bootstrap` ni `core.application`.
- Nada de instancias globales de servicios ni funciones de módulo "de compatibilidad". La API obtiene los servicios con `Depends(get_*_service)` desde `apps/api/dependencies.py`.
- Un puerto nuevo o un método nuevo de un puerto implica actualizar también el fake de `tests/unit/application/fake_adapters.py`.

## Tests

- Casos de uso: tests unitarios con los fakes en memoria de `fake_adapters.py`; nunca usar el disco ni el LLM real.
- API: `create_app(bootstrap.build_container())` con `ML_DATA_DIR` apuntando a `tmp_path`; sustituir servicios con `app.dependency_overrides[get_x_service]`.
- Adaptadores de disco: tests de integración en `tests/integration/infrastructure/` con `tmp_path`.

## Convenciones

- Código, identificadores, docstrings, mensajes de error y commits **en español** (sin tildes en los commits, como el historial). Commits con Conventional Commits: `feat(web): ...`, `refactor(core): ...`.
- Python ≥ 3.10, líneas de hasta 100 caracteres, `from __future__ import annotations`, `__all__` explícito en cada módulo.
- Los prompts de LLM viven en `core/prompts/*.md` y se cargan con `LectorDocumentosPort.leer_prompt`.

## Cuidado

- `data/` contiene los datos reales del usuario (cronogramas, ajustes, memoria de plugins). Para pruebas manuales, copiar `data/examples` a otra carpeta y apuntar `ML_DATA_DIR` a esa copia.
- La ingesta y el cierre de una tutoría escriben en la bóveda real de Obsidian configurada en `data/config/ajustes.json`.
- `.env` contiene `GEMINI_API_KEY`: no leerlo, imprimirlo ni commitearlo. Los endpoints de tutoría, quiz e ingesta consumen cuota real de Gemini.
