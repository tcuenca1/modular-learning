"""Punto de entrada para la versión web: `python run_web.py` (http://127.0.0.1:8000)."""

import os
import sys

import uvicorn

RAIZ = os.path.dirname(os.path.abspath(__file__))
os.chdir(RAIZ)  # Los servicios usan rutas relativas (data/, prompts/)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)


def run() -> None:
    host = os.getenv("WEB_HOST", "127.0.0.1")
    port = int(os.getenv("WEB_PORT", "8000"))
    uvicorn.run("modules.web.app:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run()
