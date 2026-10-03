# Changelog

## [2026-10-03]
- feat: estabilización del orquestador con CrewAI y LiteLLM (`gemini/gemini-3.5-flash-lite`).
- feat: incorporación del agente de documentación (`docs_agent`) y herramienta de actualización automática de `CHANGELOG.md`.
- chore: purga de dependencias en `pyproject.toml` conservando exclusivamente dependencias de CLI y QA.
- refactor: validación estricta de Conventional Commits en la herramienta `ejecutar_git`.
- test: ejecución exitosa de pruebas unitarias (Pytest: 3 pasadas, 0 fallidas) y verificación con Ruff.
