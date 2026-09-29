# Guía de Instalación y Uso - Modular Learning CLI (ml-cli)

Esta guía detalla los pasos necesarios para instalar, configurar y utilizar **Modular Learning CLI (`ml`)**, una plataforma de tutoría académica interactiva y gestión de conocimiento conectada a Google Gemini (`gemini-3.5-flash-lite`) con exportación automática a Obsidian.

---

## 1. Arquitectura y Estructura del Proyecto
```text
modular-learning-cli/
├── cli.py                     # Enrutador principal CLI nativo (entry_point: ml)
├── main.py                    # Orquestador de sesiones de tutoría interactiva
├── pyproject.toml             # Configuración de empaquetado moderno (PEP 621, única fuente de verdad)
├── .env                       # Variables de entorno (GEMINI_API_KEY, RUTA_OBSIDIAN, RUTA_BASE_UNIVERSIDAD)
├── .env.example               # Plantilla de configuración
├── data/                      # Capa de persistencia estructurada
│   ├── config/                # materias.txt, registro_materiales.json
│   ├── schedules/             # Cronogramas en formato JSON (*_cronograma.json)
│   └── plugins/               # Memorias técnicas de plugins (*_memoria.json)
├── modules/                   # Módulos lógicos (SoC: core, ui, plugins)
│   ├── core/                  # ai_gemini.py, gestor_archivos.py
│   ├── ui/                    # formateador.py, interaccion.py
│   └── plugins/               # Adaptadores de arquitectura hexagonal (Cisco, Node-RED, Web)
├── tools/                     # Herramientas auxiliares
│   ├── extraer_silabo.py      # Extractor de sílabos (Sección 4.2)
│   ├── ingestar_material.py   # Ingesta masiva automática (Batch) con PDF y anonimización
│   └── actualizar_plugins.py  # Actualizador de contexto de código fuente (Code Snapshot)
├── prompts/                   # Directivas en Markdown para la IA
└── docs/                      # Documentación técnica y diseño de arquitectura
```

---

## 2. Requisitos Previos
- **Python 3.10 o superior** instalado en el sistema.
- Una clave de API válida de **Google Gemini** (`GEMINI_API_KEY`) obtenida en [Google AI Studio](https://aistudio.google.com/).
- (Opcional) Microsoft Word / PowerPoint instalados localmente para conversión automática de `.docx` y `.pptx`.

---

## 3. Instalación Nativa y Editable
Abre una terminal en la carpeta raíz del proyecto y ejecuta:

```bash
pip install -e .
```

Esto compila y registra globalmente el comando `ml` en tu sistema operativo, habilitando su ejecución desde cualquier terminal.

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

### A. Tutoría Personalizada (`ml init`)
Inicia el orquestador principal de tutoría guiada paso a paso:
```bash
ml init
```
- Selecciona la asignatura y tema (o elige clases pendientes del cronograma del sílabo).
- Estudia de forma interactiva y guarda tus notas en Obsidian. Al concluir, el sistema marca automáticamente la clase como **`completado`** en el cronograma JSON.

### B. Extracción de Sílabos (`ml es`)
Convierte sílabos institucionales en cronogramas JSON estructurados en `data/schedules/`:
```bash
ml es "ruta/a/tu/silabo.pdf"
```

### C. Ingesta Automática de Material (`ml im`)
Procesa carpetas completas desde `RUTA_BASE_UNIVERSIDAD/{materia}` de forma automática:
```bash
ml im
```
- Filtra silenciosamente archivos ya procesados consultando `data/config/registro_materiales.json`.
- Convierte automáticamente archivos Office a PDF, aplica **Privacidad y Anonimización Estricta** (ocultando nombres, correos e IDs) y alimenta la memoria técnica del plugin correspondiente.

### D. Actualización de Contexto de Código (`ml up`)
Analiza un proyecto local de desarrollo (VSCode), genera un snapshot del árbol de directorios y código fuente, y actualiza la memoria del adaptador práctico (ej. Programación Web):
```bash
ml up
```

### E. Panel de Ayuda (`ml --help`)
Muestra el panel de ayuda de la CLI:
```bash
ml --help
```
