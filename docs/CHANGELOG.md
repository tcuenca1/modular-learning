# Changelog

## [2026-10-03]
- feat(agents): incorporar `arquitecto_agent` y `seguridad_agent` al orquestador de CrewAI con flujo secuencial estricto.
- refactor(cli): implementar lazy loading de dependencias de CrewAI en el comando `ml dev` y definir empaquetado portátil con dependencias opcionales `[dev]` en `pyproject.toml`.
- docs: actualización exhaustiva de toda la documentación (`README.md`, `docs/installation_guide.md`, `docs/ARCHITECTURE.md`, `docs/CHANGELOG.md`).
- fix: corregir manejo explícito de errores de git/pre-commit en la herramienta `ejecutar_git` y exportación de `imprimir_markdown_bonito`.
- test: ejecución exitosa de la suite completa de pruebas unitarias (Pytest: 5 pasadas, 0 fallidas) y análisis estático con Ruff.

## [2026-10-03]
- feat: estabilización del orquestador con CrewAI y LiteLLM (`gemini/gemini-3.5-flash-lite`).
- feat: incorporación del agente de documentación (`docs_agent`) y herramienta de actualización automática de `CHANGELOG.md`.
- chore: purga de dependencias en `pyproject.toml` conservando exclusivamente dependencias de CLI y QA.
- refactor: validación estricta de Conventional Commits en la herramienta `ejecutar_git`.
- test: ejecución exitosa de pruebas unitarias (Pytest: 3 pasadas, 0 fallidas) y verificación con Ruff.

## [2026-10-03]
- Actualización exhaustiva de documentación: README.md, docs/installation_guide.md, docs/ARCHITECTURE.md y registro en docs/CHANGELOG.md reflejando empaquetado portable, dependencias opcionales, comandos CLI completos, Lazy Loading y nuevos roles de agentes.
