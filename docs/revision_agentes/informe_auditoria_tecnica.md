# Informe de auditoría técnica – Modular Learning

Fecha: 2026-11-11. Repo sin cambios (git status limpio al terminar). Herramientas instaladas solo en `scratchpad\herr` (venv aparte), `scratchpad\ext` (pytest-cov/coverage para inyectar vía PYTHONPATH) y `scratchpad\fe2` (copia del frontend para vitest coverage). Lighthouse vía `npx lighthouse@12`.

## 1. Tabla de resultados por herramienta

| # | Herramienta | Comando exacto (desde la raíz; `$S` = scratchpad) | Resultado real | Interpretación |
|---|---|---|---|---|
| 1 | pytest + cobertura backend | `COVERAGE_FILE=$S/.coverage PYTHONPATH=$S/ext venv/Scripts/python.exe -m pytest -q backend -p no:cacheprovider --cov=modular_learning --cov-report=json:$S/cov.json --cov-report=term:skip-covered` | 147 passed, 3 skipped. **Cobertura total 71 %** (4919 stmts, 1435 sin cubrir). Ver sección 2 | Suite sana. Core bien cubierto salvo `sincronizador.py` (0 %) y `plugins.py` (60 %). CLI y adaptadores Gemini/Obsidian casi sin cubrir |
| 2 | vitest --coverage | Copia del frontend en `$S/fe2`: `npm ci; npm i --no-save @vitest/coverage-v8@5.1.0; npx vitest run --coverage --coverage.include='src/**'` | 4 archivos, 37 tests pasan. Cobertura global: Stmts 6.57 %, Branches 6.16 %, Funcs 3.97 %, Lines 5.52 % | `@vitest/coverage-v8` NO está instalado en el repo (se instaló solo en la copia). Solo `src/lib` está probado (~95 %); vistas, componentes, `api/client.ts` y `hooks` al 0 % |
| 3a | pip-audit (pyproject) | `$S/herr/Scripts/pip-audit --progress-spinner off ./backend` | "No known vulnerabilities found" | Resuelve solo las dependencias base declaradas con la última versión compatible: no refleja lo realmente instalado |
| 3b | pip-audit (entorno real) | `pip-audit --path venv/Lib/site-packages -f json` | 13 paquetes con vulnerabilidades, 105 avisos en total. Paquetes: pillow 12.3.0 (39), pypdf 6.19.0 (18), filelock 4.0.9 (13), aiohttp 3.14.3 (8), virtualenv 21.14.5 (8), chromadb 1.1.1 (5), mcp 1.28.1 (4), pyasn1 0.6.4 (4), certifi 2026.7.22 (2), langgraph-sdk, oauthlib, opentelemetry-api, uv (1 c/u) | **Directa y en runtime: pypdf 6.19.0** (12+ CVE con fix en 6.21.0 a 6.21.4; la app procesa PDFs subidos por el usuario). El resto (pillow, chromadb, aiohttp, mcp, etc.) viene de paquetes extra del venv (crewai, etc.) que no están en `pyproject.toml`; venv contaminado, no afecta al despliegue (Dockerfile) |
| 3c | npm audit | `cd frontend; npm audit` y `npm audit --omit=dev` | 4 vulnerabilidades **low**: katex 0.11.0-0.18.1 (GHSA-238p-pmpm-9mq7, prototype pollution que evita trust) y su cadena rehype-katex, remark-math, micromark-extension-math. También en prod. Fix: katex 0.19.1 (breaking) | Riesgo bajo; el contenido renderizado viene del LLM/usuario, no de terceros. Revisar al actualizar |
| 4 | bandit | `$S/herr/Scripts/bandit -r backend/src -f json` | 7457 LOC; 31 hallazgos: 3 High, 5 Medium, 23 Low | High: B324 SHA1 en `core/domain/repaso_espaciado.py:25` y `infrastructure/proyectos/inspector_local.py:108,126` (uso no criptográfico; falso positivo, basta `usedforsecurity=False`). Medium: B104 bind 0.0.0.0 en `apps/api/main.py:139` (esperado en contenedor); B608 en `persistence/almacen.py:129,139,149,159` (SQL con f-string; revisar que solo interpolen constantes/nombre de tabla). Low: B110 try/except/pass x10, B112 continue x2, B311 random x2, subprocess (B404/B603/B607) en `system/` |
| 5 | mypy (permisivo) | `mypy backend/src --ignore-missing-imports --follow-imports=silent --python-executable <venv>` | **9 errores en 2 archivos** (96 archivos revisados) | 7 en `llm/gemini_adapter.py` (retornos `str \| None` donde se declara `str`, tipos de `history`/`contents` del SDK). 2 en `json_repositorios.py`: línea 58 `materias` redefinida (no-redef) y línea 247 asignación `Any \| None` a `list`. Ninguno es grave; el más relevante es el posible `None` devuelto por el LLM sin controlar |
| 6a | radon cc | `radon cc backend/src -n C -s` / `-a` | 582 bloques, complejidad media **A (3.53)**. 32 bloques (funciones, métodos o clases) en C o peor: 8 en D o peor | Peores: `cisco.parsear_configuracion_ios` **F (46)**, `nodered.NodeRedPlugin.analizar_flujo` **F (50)**, `PluginsService.actualizar_plugin` **E (38)**, `web.extraer_rutas_y_modelos` D (29), `sincronizador.extraer_y_fusionar_subtemas` D (26), `lector_documentos.extraer_texto` D (24), `GuiaOfflineService.crear` D (22), `tutoria.normalizar_roadmap` D (21). |
| 6b | radon mi | `radon mi backend/src -s` | Todos los archivos A salvo `persistence/json_repositorios.py` = **B (11.08)** | Único archivo con MI bajo; 330 stmts y `JsonMateriaRepo.listar` C (14). Candidato a dividir por repositorio |
| 6c | tamaño de archivos frontend | `find frontend/src -name "*.ts*" \| xargs wc -l` | `MaterialView.tsx` 1279, `SilabosView.tsx` 1226, `TutoriaView.tsx` 697, `GuiaView.tsx` 612, `QuizView.tsx` 559, `HoyView.tsx` 386, `PluginsView.tsx` 345, `RevisionGuiaView.tsx` 304, `AsignaturasView.tsx` 294 (+ `types.ts` 473, `client.ts` 457). Total 8909 líneas | Dos vistas superan 1200 líneas y no tienen tests: difíciles de mantener |
| 7a | Lighthouse escritorio | `npx lighthouse@12 http://localhost:8001/ --preset=desktop --output=json ... --only-categories=performance,accessibility,best-practices,seo --chrome-flags="--headless=new --no-sandbox"` (Chrome instalado en Program Files) | Performance **89**, Accessibility **92**, Best Practices **96**, SEO **92**. FCP 1.3 s, LCP 1.7 s, TBT 0 ms, CLS 0.058 | Bueno. Informe JSON: `lh_desktop.json` |
| 7b | Lighthouse móvil | igual sin `--preset` (emulación móvil + throttling 4G lento) | Performance **55**, Accessibility 92, Best Practices 96, SEO 92. FCP 7.3 s, LCP 7.9 s, TBT 230 ms, CLS 0, TTI 7.9 s | Rendimiento móvil débil por un único JS de 947 KB sin comprimir. Informe JSON: `lh_mobile.json` |
| 7c | Lighthouse: auditorías fallidas (ambos) | (mismo informe) | `uses-text-compression` ahorro 743 KiB; `unused-javascript` 545 KiB; `cache-insight` 1020 KiB (3 recursos sin caché larga); `render-blocking` (1800 ms móvil); `color-contrast`; `aria-prohibited-attr`; `errors-in-console`; `robots-txt` inválido (21 errores: la SPA devuelve HTML en `/robots.txt`); `valid-source-maps` | Compresión gzip y cabeceras de caché de `/assets` (hash en el nombre) son lo más rentable. Accesibilidad: contraste y ARIA prohibido |
| 7d | Bundle | `ls -l backend/src/modular_learning/apps/api/static/assets` + `gzip -9 -c` | `static/` ocupa ~2.2 MB, 61 archivos en assets. `index-DaURkXLy.js` **947 191 B (≈925 KB) / 270 966 B gzip**; `index-DTddP3qS.css` 95 794 B / 18 752 B gzip; el resto son fuentes KaTeX (.ttf/.woff/.woff2, máx. 63 KB) | Un solo chunk JS (sin code splitting): recharts, react-markdown, katex y todas las vistas cargan de entrada. Fuentes KaTeX incluidas en TTF+WOFF+WOFF2 (solo hace falta WOFF2) |
| 8 | Revisión de `.github/workflows/ci.yml` | lectura | Ver sección 3 | |

## 2. Cobertura backend por módulo (pytest-cov)

Total 71 %. Core (core/domain + core/application):

| Módulo | Stmts | Falta | Cobertura |
|---|---|---|---|
| core/domain/sincronizador.py | 54 | 54 | **0 %** |
| core/application/plugins.py | 131 | 53 | **60 %** |
| core/application/silabo.py | 86 | 21 | 76 % |
| core/application/ingesta.py | 222 | 44 | 80 % |
| core/application/materias.py | 113 | 18 | 84 % |
| core/domain/alineador_curricular.py | 55 | 8 | 85 % |
| core/domain/cronograma.py | 41 | 5 | 88 % |
| core/application/evaluacion.py | 85 | 8 | 91 % |
| core/application/telemetria.py | 35 | 3 | 91 % |
| core/application/tutoria.py | 145 | 9 | 94 % |
| core/application/proyectos.py | 82 | 5 | 94 % |
| core/domain/materias.py | 35 | 2 | 94 % |
| core/application/guias.py | 135 | 5 | 96 % |
| core/application/repaso.py | 76 | 3 | 96 % |
| core/domain/guia_offline.py | 70 | 1 | 99 % |
| (39 archivos más al 100 %, incluidos puertos y varios del dominio) | | | 100 % |

Módulos por debajo del 70 % (todos):

| Módulo | Cobertura |
|---|---|
| apps/cli/commands/es.py, im.py, quiz.py, snapshot.py, stats.py, up.py, apps/cli/main.py | 0 % (7 archivos, ≈ 336 stmts) |
| core/domain/sincronizador.py | 0 % |
| infrastructure/llm/gestor_llm.py | 0 % |
| infrastructure/system/security_utils.py, subprocess_adapter.py | 0 % |
| infrastructure/obsidian/boveda_obsidian.py | 35 % |
| infrastructure/llm/gemini_adapter.py | 43 % |
| apps/api/routers/silabo.py | 50 % |
| apps/api/routers/material.py | 51 % |
| apps/cli/ui/interaccion.py | 58 % |
| apps/api/routers/materias.py | 59 % |
| core/application/plugins.py | 60 % |
| apps/cli/commands/init.py | 61 % |
| settings.py | 65 % |
| infrastructure/persistence/json_repositorios.py | 66 % |
| apps/api/routers/proyectos.py | 67 % |
| apps/api/routers/guias.py, infrastructure/plugins/web.py, documents/conversor_libreoffice.py | 69 % |

Entre 70 % y 72 %: lector_documentos 70 %, nodered 70 %, almacen 72 %, cisco 72 %.

## 3. CI (`.github/workflows/ci.yml`)

Comprueba hoy:
- Job `python` (ubuntu, Python 3.12, con Postgres 16 de servicio): `pip install -e "./backend[all]"`, `ruff check backend`, `lint-imports`, `pytest -q backend`.
- Job `frontend` (Node 22): `npm ci`, `npm run lint` (oxlint), `npm run build` (tsc -b + vite build).
- Disparadores: push a main/master/`refactor/**` y PR a main/master.

Falta:
- Ejecutar `npm test` (vitest): hay 37 tests que no se ejecutan en CI.
- Cobertura: ni pytest-cov ni umbral (`--cov-fail-under`), ni vitest coverage (ni siquiera `@vitest/coverage-v8` está en devDependencies).
- Auditoría de dependencias: ni `pip-audit` ni `npm audit --omit=dev`; tampoco Dependabot/Renovate (no comprobado si existe `.github/dependabot.yml`).
- `ruff format --check` (el pre-commit lo usa, CI no).
- Análisis estático extra: bandit, mypy/pyright (hoy solo 9 errores en modo permisivo).
- Pruebas de contenedor: no construye el Dockerfile.
- Lighthouse CI o presupuesto de tamaño de bundle.
- No hay concurrency/cancelación de ejecuciones, ni caché del venv más allá de pip, ni matriz de versiones de Python (pyproject exige >=3.10, CI solo 3.12).
- Los 3 tests saltados dependen de `ML_TEST_DATABASE_URL`: confirmar que en CI sí corren.

## 4. Acciones priorizadas

1. **Alta**: subir `pypdf` a >=6.21.4 en `backend/pyproject.toml` (pin mínimo) – 18 avisos, procesa archivos subidos por el usuario.
2. **Alta**: añadir a CI `npm test`, `pip-audit` (contra el entorno instalado, no solo pyproject) y `npm audit --omit=dev --audit-level=high`.
3. **Alta (móvil)**: habilitar compresión (GZipMiddleware en FastAPI o `fastapi` + `brotli`) y `Cache-Control: immutable` para `/assets/*` – ahorro estimado 743 KiB y 1 MB de caché; subiría el rendimiento móvil (hoy 55) de forma notable.
4. **Alta (móvil)**: code splitting con `React.lazy` por vista (rutas) y `manualChunks` para recharts/katex/react-markdown; hoy un JS de 925 KB (271 KB gzip), con 545 KiB de JS sin usar en la carga inicial.
5. **Media**: añadir `pytest-cov` a extras `dev` y `@vitest/coverage-v8` a devDependencies; umbral inicial de CI de 70 % backend.
6. **Media**: tests para `core/domain/sincronizador.py` (0 %, función D 26), `core/application/plugins.py` (60 %, `actualizar_plugin` E 38), `boveda_obsidian.py` (35 %), `gemini_adapter.py` (43 %) con fakes, y routers `silabo`/`material`/`materias`.
7. **Media**: refactor de las funciones más complejas: `NodeRedPlugin.analizar_flujo` (F 50), `parsear_configuracion_ios` (F 46), `PluginsService.actualizar_plugin` (E 38); dividir en funciones pequeñas con tests previos.
8. **Media**: tests frontend: `api/client.ts`, `hooks/` y las vistas críticas (con Testing Library); partir `MaterialView.tsx` (1279 líneas) y `SilabosView.tsx` (1226).
9. **Media**: accesibilidad: corregir contraste y atributos ARIA prohibidos (`color-contrast`, `aria-prohibited-attr`); servir `robots.txt` real o 404 en vez del HTML de la SPA; revisar el error de consola.
10. **Baja**: bandit: `hashlib.sha1(..., usedforsecurity=False)` en 3 sitios; revisar el SQL de `almacen.py` (nombres de tabla constantes); sustituir `except: pass` por registro de log cuando proceda.
11. **Baja**: arreglar los 9 errores de mypy (`gemini_adapter` devolver `""` o lanzar si el texto es `None`; renombrar variable duplicada en `json_repositorios.py:58`) y añadir mypy permisivo a CI.
12. **Baja**: eliminar fuentes KaTeX `.ttf` y `.woff` del build (dejar solo WOFF2), actualizar katex a >=0.19.1 cuando sea viable, añadir `ruff format --check` y Dependabot, y limpiar el venv del proyecto (paquetes ajenos como crewai/chromadb generan la mayoría de los avisos de pip-audit).

## 5. Limitaciones y notas

- Lighthouse se ejecutó contra el servidor que ya respondía en `localhost:8001` (sirve el build compilado actual de `apps/api/static`); no se arrancó ni se tocó ningún servidor propio. Los datos dependen de ese servidor y no se inspeccionaron.
- La cobertura de vitest se midió en una copia del frontend porque instalar `@vitest/coverage-v8` en el repo habría modificado `package.json`.
- pytest-cov se inyectó con `PYTHONPATH=$S/ext` para no instalar nada en el venv del proyecto.
- No se leyeron `data/` ni `.env`.
- El conteo de funciones C y peor (32) proviene de contar bloques de la salida `radon cc -n C`; la lista completa está en la salida de la herramienta (reproducible con el comando indicado).
