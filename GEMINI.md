# Protocolo de Trabajo para Antigravity en Modular Learning

Antigravity debe seguir estrictamente **[`CLAUDE.md`](CLAUDE.md)** (arquitectura hexagonal, comandos de calidad, restricciones y estilo) y las **reglas 1 a 10 de [`docs/PENDIENTES.md`](docs/PENDIENTES.md)**. Las reglas no se duplican aquí para evitar desfases.

---

## Flujo por cada tarea de `docs/PENDIENTES.md`

Cada tarea (`P<n>` o `D<n>`) se resuelve una por una en el siguiente orden:

1. **Tarea (implementación y tests):** leer la descripción y criterios de aceptación en `docs/PENDIENTES.md`, aplicar únicamente los cambios requeridos, actualizar `fake_adapters.py` o la documentación si corresponde y escribir/actualizar los tests.
2. **Verificación en verde:** ejecutar desde la raíz las comprobaciones indicadas en `CLAUDE.md` (`pytest`, `ruff`, `import-linter` y, si se tocó `frontend/`, `npm run lint && npm run build && npm test`).
3. **Commit de la tarea:** añadir solo los archivos modificados por la tarea (`git add <archivos>`, nunca `git add -A`) y hacer commit en `main` con `<tipo>(<scope>): <ID> <descripcion>` (sin tildes).
4. **Informe en `docs/CAMBIOS_AGY.md`:** añadir la entrada al principio de `docs/CAMBIOS_AGY.md` siguiendo la plantilla definida en `docs/PENDIENTES.md`.
5. **Commit del informe:** `git add docs/CAMBIOS_AGY.md && git commit -m "docs: <ID> informe en CAMBIOS_AGY"`.
6. **Detenerse:** no borrar la tarea de `docs/PENDIENTES.md` ni hacer `git push`; presentar el resumen al usuario y esperar su revisión antes de pasar a la siguiente tarea.
