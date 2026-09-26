# Guía de Instalación y Uso - Modular Learning CLI (ml-cli)

Esta guía detalla los pasos necesarios para instalar, configurar y utilizar **Modular Learning CLI (`ml`)**, una plataforma de tutoría académica interactiva y gestión de conocimiento conectada a Google Gemini (`gemini-3.5-flash-lite`) con exportación automática a Obsidian.

---

## 1. Arquitectura y Estructura del Proyecto
```text
modular-learning-cli/
├── cli.py                     # Enrutador principal CLI nativo (entry_point: ml)
├── main.py                    # Orquestador de sesiones de tutoría interactiva
├── pyproject.toml             # Configuración de empaquetado moderno (PEP 621)
├── .env                       # Variables de entorno (GEMINI_API_KEY, RUTA_OBSIDIAN)
├── .env.example               # Plantilla de configuración
├── requirements.txt           # Dependencias del proyecto
├── data/                      # Base de datos local (cronogramas JSON y materias.txt)
├── modules/                   # Módulos lógicos (capas de negocio, UI y adaptadores)
│   ├── core/                  # ai_gemini.py, gestor_archivos.py
│   ├── ui/                    # formateador.py, interaccion.py
│   └── plugins/               # Sistema de plugins para arquitectura hexagonal (Cisco, Node-RED)
├── tools/                     # Herramientas auxiliares
│   ├── extraer_silabo.py      # Extractor masivo/individual de sílabos (Sección 4.2)
│   └── ingestar_material.py   # Ingesta multimodal con conversión automática a PDF y tracking
├── prompts/                   # Instrucciones externas en Markdown
└── obsidian_vault/            # Bóveda local de Obsidian (constelación de grafos)
```

---

## 2. Requisitos Previos
- **Python 3.10 o superior** instalado en el sistema.
- Una clave de API válida de **Google Gemini** (`GEMINI_API_KEY`) obtenida en [Google AI Studio](https://aistudio.google.com/).
- (Opcional para conversión Office) Microsoft Word / PowerPoint instalados localmente para procesamiento de `.docx` y `.pptx`.

---

## 3. Instalación Nativa y Editable
Abre una terminal en la carpeta raíz del proyecto y ejecuta el comando de instalación editable:

```bash
pip install -e .
```

Esto registrará globalmente el comando `ml` en tu sistema operativo, permitiéndote ejecutarlo desde cualquier terminal.

---

## 4. Configuración de Variables de Entorno
1. Duplica el archivo `.env.example` y nómbralo `.env` en la raíz del proyecto.
2. Configura tus credenciales:
```env
GEMINI_API_KEY=tu_clave_api_real_aqui
RUTA_OBSIDIAN="C:\Users\TuUsuario\Documents\Obsidian Vault"
```

---

## 5. Uso del Comando Global `ml`

El enrutador nativo expone las siguientes opciones:

### A. Tutoría Personalizada (`ml init`)
Inicia el orquestador principal de tutoría guiada paso a paso:
```bash
ml init
```
- Selecciona la asignatura y tema (o elige clases pendientes del cronograma del sílabo).
- Estudia de forma interactiva con explicaciones técnicas adaptadas por IA y guárdalo automáticamente en tu bóveda de Obsidian. Al concluir, el sistema marcará automáticamente la clase como **`completado`** en el cronograma JSON.

### B. Extracción de Sílabos (`ml es`)
Convierte sílabos (archivos individuales o carpetas completas en formato PDF, Markdown o TXT) en cronogramas JSON estructurados ubicados en `data/`:
```bash
ml es "ruta/a/tu/carpeta_o_silabo.pdf"
```

### C. Ingesta Inteligente de Material (`ml im`)
Procesa diapositivas, lecturas, documentos Word (`.docx`), presentaciones PowerPoint (`.pptx`) o imágenes mediante visión multimodal de Gemini y los convierte en notas formateadas para Obsidian:
```bash
ml im "ruta/a/tu/material.pptx"
```
*Características avanzadas:*
- **Conversión Automática**: Convierte archivos `.docx` y `.pptx` a PDF en segundo plano (`docx2pdf` / `comtypes`) antes de enviarlos a Gemini.
- **Sistema de Tracking / Registro**: Evita procesar documentos duplicados consultando `data/registro_materiales.json`, preguntando mediante confirmación interactiva si se desea forzar el reprocesamiento.

### D. Panel de Ayuda (`ml --help`)
Muestra las opciones disponibles en pantalla:
```bash
ml --help
```
