# 🧠 Modular Learning v2.0

> **Segundo Cerebro Académico y Tutor Personalizado con IA**

`modular-learning` es una plataforma de estudio universitario que organiza asignaturas y cronogramas a partir de sílabos oficiales, ingesta material académico (`.pdf`, `.docx`, `.pptx`, `.txt`, `.md`) hacia una bóveda de [Obsidian](https://obsidian.md/), ofrece sesiones interactivas de tutoría paso a paso, genera cuadernos de estudio en PDF A5 para trabajar sin conexión y programa repasos espaciados (SM-2) mediante Google Gemini (`google-genai`).

El sistema sigue una **Arquitectura Hexagonal estricta** (Puertos y Adaptadores) que desacopla el núcleo de negocio (`core/`) de las interfaces (`ml` CLI y `ml-web` SPA en React 19 + FastAPI) y de los adaptadores de infraestructura.

---

## 📚 Documentación del Proyecto

- 📘 **[Manual Funcional del Sistema (Markdown)](docs/manual/MANUAL_FUNCIONAL.md)** · **[Versión PDF](docs/manual/MANUAL_FUNCIONAL.pdf)** — Especificación completa de casos de uso (`CU-01` a `CU-20`), flujos del semestre, matriz de trazabilidad de endpoints/CLI y registro de discrepancias.
- 🏛️ **[Arquitectura del Sistema (`docs/ARCHITECTURE.md`)](docs/ARCHITECTURE.md)** — Capas de la arquitectura hexagonal, puertos, adaptadores, persistencia (`AlmacenDocumentos`) y contratos `import-linter`.
- ☁️ **[Guía de Despliegue (`docs/DESPLIEGUE.md`)](docs/DESPLIEGUE.md)** — Puesta en marcha en la nube (Render + Neon Postgres), modo híbrido y contenedor local con Docker Compose.

---

## 🚀 Características Principales

- **🗺️ Asignaturas, Sílabos y Cronogramas:** Catálogo normalizado por `slug`, extracción asistida por IA de sesiones desde sílabos `.pdf` o `.docx`, edición de clases (`id` único) y definición de cortes de parcial.
- **📄 Ingesta y Alineación Curricular:** Lectura multimodal de `.pdf` con Gemini, extracción de texto de `.docx` (`python-docx`), `.txt` y `.md`, y soporte de presentaciones `.pptx` mediante conversión headless a PDF con LibreOffice (o plan B de extracción de texto con `python-pptx`), generando apuntes en Markdown enlazados en Obsidian y alineados automáticamente con la clase correspondiente del cronograma.
- **👨‍🏫 Tutoría Interactiva por Pasos:** Sesiones guiadas con explicaciones en *streaming* (SSE), resolución de dudas con contexto curricular y práctico, y consolidación del resumen final en Obsidian.
- **📖 Guías de Estudio Offline (PDF A5):** Generación de cuadernos de estudio imprimibles para una o varias clases (o por corte de parcial) y registro posterior de clases entendidas o con dudas.
- **🎯 Evaluación Activa y Repaso Espaciado (SM-2):** Cuestionarios de opción múltiple y preguntas abiertas calificadas con IA sobre temas completados, con programación automática de tarjetas de repaso.
- **🔌 Proyectos y Plugins de Contexto Técnico:** Seguimiento de proyectos prácticos por asignatura e inspección de laboratorios de **Cisco Packet Tracer**, flujos de **Node-RED** y proyectos de **Desarrollo Web**.

---

## 📁 Estructura del Repositorio

```text
modular-learning/
├── backend/                # Python (pyproject.toml, src/modular_learning/ y tests/)
├── frontend/               # SPA en React 19 + TypeScript + Tailwind CSS v4 + Vite
├── data/                   # Datos locales (config/, schedules/, repaso/, guias/, plugins/)
├── deploy/                 # Scripts de arranque en contenedor y subida a PostgreSQL
├── scripts/                # Utilidades de migración de datos y generación del manual PDF
└── docs/                   # Manual funcional, arquitectura y guía de despliegue
```

---

## ⚙️ Requisitos

- **Python** 3.10 o superior.
- **Node.js** 22+ y **npm** (para compilar y desarrollar el frontend).
- **Clave de API de Google Gemini** (`GEMINI_API_KEY`).
- **LibreOffice** (`soffice`, *opcional*): recomendado para ingestar presentaciones `.pptx` convirtiéndolas a PDF y aprovechando la lectura visual de Gemini (imágenes y diagramas). Si no está instalado, el sistema utiliza automáticamente el plan B con `python-pptx` (extracción de texto, tablas y notas del orador).

---

## 📦 Instalación

### 1. Clonar el repositorio y crear el entorno virtual
```bash
git clone https://github.com/tcuenca1/modular-learning.git
cd modular-learning

python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux / macOS
```

### 2. Configurar variables de entorno
Copia la plantilla `.env.example` y define tu clave de Gemini:
```bash
cp .env.example .env
```
En `.env`:
```ini
GEMINI_API_KEY=tu_clave_de_api_aqui
ML_DATA_DIR=data
```

### 3. Instalar el backend y el frontend
Desde la raíz del repositorio (con el entorno virtual activo):

```bash
# Instalación completa del backend (CLI + API Web + herramientas de test/lint)
pip install -e "./backend[all]"

# Instalación de dependencias del frontend y compilación del cliente web
cd frontend && npm ci && npm run build && cd ..
```

*(También puedes instalar grupos individuales de `backend/pyproject.toml` con `pip install -e "./backend[cli]"`, `pip install -e "./backend[web]"` o `pip install -e "./backend[dev]"`).*

---

## 💻 Uso Local

### Aplicación Web (`ml-web`)
Con el frontend compilado en `backend/src/modular_learning/apps/api/static/` (generado por `cd frontend && npm run build`), inicia el servidor FastAPI en `http://127.0.0.1:8000`:

```bash
ml-web
```

Para desarrollo del frontend con recarga en caliente (*hot-reload* en `http://localhost:5173` con proxy a `:8000`):
```bash
cd frontend && npm run dev
```

### Interfaz de Línea de Comandos (`ml`)
```bash
ml --help         # Lista todos los subcomandos disponibles
ml init           # Inicia una sesión interactiva de tutoría guiada en terminal
ml es             # Extrae las clases de un sílabo (.pdf/.docx) y genera su cronograma
ml im             # Ingesta interactiva de documentos académicos hacia Obsidian
ml quiz           # Ejecuta un cuestionario de evaluación sobre temas completados
ml stats          # Muestra el progreso de clases por asignatura y plugins activos
ml up             # Actualiza la memoria técnica de un plugin práctico (cisco, nodered, web)
```

---

## 🧪 Verificación y Pruebas

Desde la raíz del repositorio (con el entorno virtual activado):

```bash
# Pruebas unitarias y de integración del backend
python -m pytest -q backend

# Linter de Python
python -m ruff check backend

# Verificación de contratos de arquitectura hexagonal
python -c "import sys; from importlinter.cli import lint_imports_command; sys.argv=['lint-imports','--config','backend/pyproject.toml']; lint_imports_command()"

# Linter, compilación y pruebas del frontend
cd frontend && npm run lint && npm run build && npm test && cd ..
```

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta `LICENSE` para más información.
