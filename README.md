# 🎓 Modular Learning CLI (`ml`)

Plataforma de tutoría académica y gestión de conocimiento basada en consola (CLI) conectada a Google Gemini (`gemini-3.5-flash-lite`), diseñada bajo Arquitectura Hexagonal y Principio de Responsabilidad Única (SoC), con exportación automática a Obsidian.

---

## 📋 Requisitos Previos

- **Python 3.10 o superior** instalado en el sistema.
- Una clave de API válida de **Google Gemini** (`GEMINI_API_KEY`) obtenida en [Google AI Studio](https://aistudio.google.com/).

---

## 📁 Estructura del Proyecto

```text
modular-learning-cli/
├── cli.py                     # Enrutador principal CLI nativo (entry_point: ml)
├── main.py                    # Orquestador de sesiones de tutoría interactiva
├── pyproject.toml             # Configuración de empaquetado (PEP 621)
├── .env                       # Variables de entorno (GEMINI_API_KEY, RUTA_OBSIDIAN, RUTA_BASE_UNIVERSIDAD)
├── .env.example               # Plantilla de configuración
├── data/                      # Capa de persistencia estructurada
├── modules/                   # Módulos lógicos (core, ui, plugins)
├── tools/                     # Herramientas auxiliares (ingestar_material, extraer_silabo, etc.)
├── prompts/                   # Directivas en Markdown para la IA
└── docs/                      # Documentación técnica y diseño de arquitectura
```

---

## 🚀 Guía de Instalación

### 1. Configuración de Variables de Entorno (`.env`)
Duplica el archivo `.env.example` en la raíz del proyecto y configúralo con tus credenciales:
```env
GEMINI_API_KEY=tu_clave_api_de_google_gemini
RUTA_OBSIDIAN="C:\Users\TuUsuario\Documents\Obsidian Vault"
RUTA_BASE_UNIVERSIDAD="C:\Universidad"
```

### 2. Modos de Instalación
Puedes instalar el paquete como usuario final o en modo desarrollo editable:

- **Instalación estándar (Usuario Final):**
  ```bash
  pip install .
  ```
- **Instalación en modo editable (Desarrollador):**
  ```bash
  pip install -e .
  ```

Esto compila y registra globalmente el comando `ml` en tu sistema operativo.

---

## 🛠️ CLI Reference (Comandos Disponibles)

El comando global `ml` ofrece los siguientes subcomandos:

- **`ml init`**
  - **Descripción**: Inicia la sesión de tutoría interactiva personalizada guiada por el tutor IA.
  - **Uso**: `ml init`
- **`ml es`**
  - **Descripción**: Extrae cronogramas de sílabos (PDFs o archivos locales) y genera cronogramas estructurados en JSON.
  - **Uso**: `ml es "ruta/al/silabo.pdf"`
- **`ml im`**
  - **Descripción**: Ingesta masiva y automatizada de material de estudio multimodal (PDFs, PPTx, DOCx) hacia Obsidian con anonimización estricta.
  - **Uso**: `ml im`
- **`ml quiz`**
  - **Descripción**: Ejecuta el Motor de Recuerdo Activo (quiz interactivo de temas completados).
  - **Uso**: `ml quiz`
- **`ml stats`**
  - **Descripción**: Muestra un Dashboard visual interactivo con telemetría, progreso global y desglose por asignatura.
  - **Uso**: `ml stats`
- **`ml --help`**
  - **Descripción**: Muestra el panel de ayuda y comandos disponibles.
  - **Uso**: `ml --help`

---

## 🏛️ Arquitectura del Sistema

Consulta [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) para más detalles sobre la Arquitectura Hexagonal, puertos y adaptadores.
