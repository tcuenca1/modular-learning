# 🧠 Modular Learning v2.0

> **Segundo Cerebro Académico & Tutor Personalizado con IA para Estudiantes de Ingeniería**

`modular-learning` es una plataforma integral que automatiza la ingesta, análisis y organización de material académico multimodal (PDF, DOCX con extracción nativa de diagramas, PPTX) para transformarlo en notas estructuradas en [Obsidian](https://obsidian.md/), ofreciendo además sesiones interactivas de tutoría técnica guiada y cuestionarios de recuerdo activo mediante Google Gemini.

El proyecto está diseñado bajo una **Arquitectura Hexagonal estricta** (Puertos y Adaptadores), permitiendo desacoplar completamente la lógica de negocio de las interfaces de usuario (CLI y Web SPA) y de la infraestructura externa.

---

## 🚀 Características Principales

- **📄 Ingesta Multimodal Headless:** Extracción de texto y diagramas embebidos desde `.docx` (sin depender de suites ofimáticas), PDFs y presentaciones `.pptx`, sincronizando notas en Markdown con enlaces cruzados para Obsidian.
- **🗺️ Alineación Curricular y Cronogramas:** Extracción estructurada de sílabos analíticos y seguimiento semanal del cronograma de clases.
- **👨‍🏫 Tutoría Interactiva por Pasos:** Sesiones de estudio personalizadas con roadmaps progresivos, explicaciones técnicas transmitidas por **streaming en tiempo real**, resolución de dudas inline y consolidación final en Obsidian.
- **🎯 Recuerdo Activo (Active Recall):** Generación de preguntas técnicas avanzadas basadas exclusivamente en temas completados, diseñadas con reglas anti-patrón (distractores plausibles y homogéneos).
- **🔌 Plugins de Contexto Técnico:** Módulos de memoria técnica especializada para Cisco Packet Tracer, flujos de Node-RED y proyectos Web.
- **🖥️ Dos Interfaces Unificadas:**
  - **CLI Moderna (`ml`):** Consola enriquecida con `Typer`, `Rich`, `Questionary` y spinners elegantes con `Halo`.
  - **Web SPA SaaS (`ml-web`):** Aplicación web reactiva con diseño SaaS sobrio construida con **React 19**, **Tailwind CSS v4**, **TypeScript**, **Recharts** y **Sonner**.

---

## 🏛️ Arquitectura del Sistema

El proyecto sigue una **Arquitectura Hexagonal (Puertos y Adaptadores)** con Inversión de Control (IoC):

```
src/modular_learning/
├── core/                   # Núcleo de Negocio Agnóstico (sin dependencias externas)
│   ├── domain/             # Entidades, alineador curricular y algoritmos
│   ├── ports/              # Contratos abstractos (LLMPort, Repos, Boveda, Documentos)
│   └── application/        # Casos de uso (Tutoria, Evaluacion, Silabo, Ingesta, etc.)
├── infrastructure/         # Adaptadores Secundarios (Salida)
│   ├── llm/                # Adaptador Gemini (google-genai SDK moderno)
│   ├── persistence/        # Repositorios JSON desacoplados
│   ├── obsidian/           # Bóveda y generador de notas Markdown
│   └── documents/          # Procesamiento multimodal nativo
├── apps/                   # Adaptadores Primarios (Entrada)
│   ├── cli/                # Terminal CLI (Typer, Rich, Questionary, Halo)
│   └── api/                # FastAPI Web Server (REST, SSE Streaming y SPA Fallback)
├── bootstrap.py            # Contenedor IoC centralizado (Composition Root)
└── settings.py             # Configuración y resolución de rutas de datos
```

> 📖 **Para una descripción detallada, diagrama de componentes y contratos de arquitectura, consulta [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).**

El desacoplamiento está blindado mediante contratos de `import-linter`: la capa `core` no puede importar de `infrastructure`, `apps`, `bootstrap`, `settings` ni de librerías externas (`fastapi`, `typer`, `google`, `pypdf`, `docx`…), el dominio no depende de los casos de uso y la infraestructura solo depende de los puertos.

---

## 📦 Instalación

### 1. Clonar el repositorio y configurar entorno
```bash
git clone https://github.com/tcuenca1/modular-learning.git
cd modular-learning

python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux / macOS
```

### 2. Configurar variables de entorno
Copia la plantilla `.env.example` y define tu clave de API de Gemini:
```bash
cp .env.example .env
```
En `.env`:
```ini
GEMINI_API_KEY=tu_clave_de_api_aqui
ML_DATA_DIR=data
```

### 3. Grupos de Instalación Opcionales

Puedes instalar únicamente los componentes que necesites utilizando las opciones de `pyproject.toml`:

```bash
# Solo herramientas de consola (CLI):
pip install -e ".[cli]"

# Solo servidor web y backend API:
pip install -e ".[web]"

# Solo herramientas de desarrollo, pruebas y linters:
pip install -e ".[dev]"

# Instalación completa (Recomendado para desarrollo integral):
pip install -e ".[all]"
```

---

## 💻 Uso de la Aplicación

### Interfaz de Consola (CLI)
Una vez instalado, el comando `ml` está disponible globalmente en tu terminal:

```bash
ml --help         # Muestra todos los comandos disponibles
ml init           # Inicia una sesión interactiva de tutoría guiada
ml es             # Extrae temas de un sílabo (PDF/DOCX) y genera cronograma
ml im             # Ingesta interactiva de documentos académicos a la bóveda
ml quiz           # Inicia un quiz de recuerdo activo sobre temas completados
ml stats          # Muestra métricas de estudio y racha en consola con Rich
ml up             # Actualiza la memoria técnica de plugins prácticos
```

### Interfaz Web (React + FastAPI)

Para ejecutar la aplicación web en modo producción:
```bash
# 1. Compilar el frontend React:
cd frontend
npm ci
npm run build
cd ..

# 2. Iniciar el servidor web unificado:
ml-web
```
Abre tu navegador en `http://127.0.0.1:8000` para acceder al Dashboard interactivo.

Para desarrollo frontend con hot-reload:
```bash
cd frontend
npm run dev       # Proxy configurado hacia http://127.0.0.1:8000
```

---

## 🧪 Pruebas y Aseguramiento de Calidad (SQA)

El proyecto cuenta con integración continua (CI) en GitHub Actions y validaciones locales en pre-commit:

```bash
# Linter de código Python con autofix
ruff check src tests

# Validación de contratos de arquitectura hexagonal
lint-imports

# Ejecución de la suite completa de pruebas unitarias e integración
pytest -q

# Linter del cliente web
cd frontend && npm run lint && cd ..

# Compilación estricta de TypeScript y Vite
cd frontend && npm run build && cd ..
```

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta `LICENSE` para más información.
