# Guía de Instalación y Uso - Modular Learning CLI (`ml-cli`)

Esta guía detalla los pasos necesarios para instalar, configurar y utilizar **Modular Learning CLI (`ml`)**, una plataforma de tutoría académica interactiva y gestión de conocimiento conectada a Google Gemini (`gemini-3.5-flash-lite`) con exportación automática a Obsidian.

---

## 1. Arquitectura y Estructura del Proyecto
```text
modular-learning-cli/
├── cli.py                     # Enrutador principal CLI nativo (entry_point: ml, con Lazy Loading)
├── main.py                    # Orquestador de sesiones de tutoría interactiva
├── pyproject.toml             # Configuración de empaquetado moderno (PEP 621, dependencias opcionales dev)
├── .env                       # Variables de entorno (GEMINI_API_KEY, RUTA_OBSIDIAN, RUTA_BASE_UNIVERSIDAD)
├── .env.example               # Plantilla de configuración
├── data/                      # Capa de persistencia estructurada
├── modules/                   # Módulos lógicos (core, ui, plugins, agents)
├── tools/                     # Herramientas auxiliares (ingestar_material, extraer_silabo, etc.)
├── prompts/                   # Directivas en Markdown para la IA
└── docs/                      # Documentación técnica y diseño de arquitectura
```

---

## 2. Requisitos Previos
- **Python 3.10 o superior** instalado en el sistema.
- Una clave de API válida de **Google Gemini** (`GEMINI_API_KEY`) obtenida en [Google AI Studio](https://aistudio.google.com/).

---

## 3. Sistema de Empaquetado Portátil y Modos de Instalación

Para garantizar portabilidad total, el proyecto separa las dependencias de producción de las herramientas pesadas de desarrollo y agentes (CrewAI):

### A. Instalación para Usuario Final (Versión Ligera)
Instalación rápida sin CrewAI ni dependencias de pruebas:
```bash
pip install .
```

### B. Instalación para Desarrolladores y Agentes (`[dev]`)
Instalación en modo editable con todas las herramientas de QA, linter (`ruff`), pre-commit y el framework CrewAI para agentes autónomos:
```bash
pip install -e ".[dev]"
```

Esto compila y registra globalmente el comando `ml` en tu sistema operativo.

---

## 4. Configuración de Variables de Entorno (`.env`)
Duplica el archivo `.env.example` y configúralo en la raíz del proyecto:
```env
GEMINI_API_KEY=tu_clave_api_real_aqui
RUTA_OBSIDIAN="C:\Users\TuUsuario\Documents\Obsidian Vault"
RUTA_BASE_UNIVERSIDAD="C:\Universidad"
```

---

## 5. Uso del Comando Global `ml`

- **`ml init`**: Inicia el orquestador principal de tutoría guiada paso a paso.
- **`ml es`**: Extrae cronogramas de sílabos institucionales a formato JSON.
- **`ml im`**: Ingesta masiva y automática de material de estudio hacia Obsidian.
- **`ml up`**: Actualiza el contexto técnico y code snapshots de proyectos locales.
- **`ml quiz`**: Ejecuta el Motor de Recuerdo Activo (Quiz interactivo).
- **`ml stats`**: Muestra el Dashboard visual de telemetría y progreso académico.
- **`ml dev`**: Inicia el entorno de desarrollo y auditoría autónoma con agentes (CrewAI).
- **`ml --help`**: Muestra el panel de ayuda.
