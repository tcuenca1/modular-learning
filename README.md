# modular-learning-cli (ml-cli)

`ml-cli` es una herramienta de terminal (CLI) diseñada para automatizar la ingesta, análisis y organización de material académico multimodal (PDF, DOCX, PPTX). Transforma documentos técnicos desestructurados en notas de conocimiento estructuradas para [Obsidian](https://obsidian.md/), utilizando Google Gemini como motor de razonamiento multimodal.

## Arquitectura
El sistema sigue un diseño de **Arquitectura Hexagonal**:
- **Core (Dominio):** Lógica central, puertos y servicios.
- **Adapters (Puertos):** Integración con Google Gemini (SDK `google-genai`), manejo de archivos y almacenamiento.
- **Plugins:** Módulos extensibles para extraer contextos técnicos de disciplinas específicas (Cisco, Node-RED, Web).

## Stack Tecnológico
- **Python 3.10+**
- **Google GenAI SDK:** Inteligencia artificial multimodal.
- **`python-docx`:** Procesamiento *headless* nativo (sin MS Word) de documentos .docx, incluyendo extracción de texto e imágenes.
- **Typer & Rich:** Interfaz de consola elegante y logs informativos.
- **Questionary & Halo:** Interactividad y estados de carga en consola.

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repo>
   cd ml-cli
   ```

2. **Entorno virtual:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Configuración:**
   Copia `.env.example` a `.env` y configura tus variables:
   ```bash
   cp .env.example .env
   ```

4. **Instalación:**
   ```bash
   pip install -e .
   ```

## Comandos
- `ml init`: Inicializa la estructura del proyecto y carpetas.
- `ml im`: Ingesta interactiva de material (PDF/DOCX/PPTX). Los documentos .docx se procesan extrayendo texto e imágenes automáticamente.
- `ml up`: Actualiza la memoria de los plugins (Node-RED, Cisco, Web).

## Aplicación Web
Además del CLI, el proyecto incluye una interfaz web con las mismas funciones (tutoría con streaming, quiz, dashboard, sílabos, ingesta y plugins):

```bash
pip install -e .
python run_web.py   # o: ml-web  → http://127.0.0.1:8000
```

La web es un nuevo **adaptador de entrada** (`modules/web/`, FastAPI) que reutiliza los servicios del núcleo (`servicio_tutoria`, `servicio_silabo`, `servicio_ingesta`, `motor_evaluacion`, `telemetria`, `gestor_plugins`) sin duplicar lógica de negocio. Variables opcionales: `WEB_HOST`, `WEB_PORT`.

## Plugins
El sistema permite extender sus capacidades mediante plugins en `modules/plugins/`. Actualmente, procesa archivos JSON de configuración de redes y topologías para alimentar la "memoria" del asistente.

## SQA (Calidad de Software)
Ejecuta las herramientas integradas para mantener el código limpio:
- **Linting:** `ruff check .`
- **Seguridad:** `bandit -r modules/ tools/ -ll`
- **Tests:** `pytest`
