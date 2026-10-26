# Modular Learning · backend

Núcleo en Python de Modular Learning con arquitectura hexagonal: casos de uso, adaptadores
(Gemini, JSON en disco, Obsidian) y dos interfaces de entrada, la CLI `ml` (Typer) y la API
web `ml-web` (FastAPI), que sirve el frontend compilado desde `src/modular_learning/apps/api/static/`.

```bash
python -m pip install -e "backend[all]"   # desde la raíz del repositorio
python -m pytest -q backend
```

La documentación completa, la instalación y la arquitectura están en el
[README principal](../README.md) y en [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).
