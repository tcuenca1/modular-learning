# Guía de Instalación y Uso - Sistema de Tutoría CLI

Esta guía detalla los pasos necesarios para instalar, configurar y utilizar el Sistema de Tutoría Personalizado por CLI conectado a Google Gemini.

---

## 1. Arquitectura y Estructura del Proyecto
```text
SistemaAprendizaje/
├── main.py                    # Orquestador principal del tutor CLI
├── .env                       # Variables de entorno (GEMINI_API_KEY, RUTA_OBSIDIAN)
├── .env.example               # Plantilla de configuración
├── requirements.txt           # Dependencias del proyecto
├── data/
│   └── materias.txt           # Persistencia de asignaturas
├── modules/                   # Módulos lógicos del sistema
│   ├── ai_gemini.py           # Conexión con la API de Google Gemini (Gemini 3.5 Flash Lite)
│   ├── gestor_archivos.py     # Manejo de disco y generación de constelaciones en Obsidian
│   └── interaccion.py         # UI de terminal, selección interactiva con flechas y formato Markdown
├── tools/                     # Herramientas auxiliares independientes
│   └── extraer_silabo.py      # Extractor local de cronograma de sílabos (Sección 4.2)
├── prompts/                   # Instrucciones y directivas para la IA
│   ├── 01_roadmap_aprendizaje.md
│   ├── 02_explicacion_tema.md
│   ├── 03_resumen_evaluacion.md
│   └── 04_extraccion_silabo.md
└── documentation/
    └── installation_guide.md  # Esta guía de uso
```

---

## 2. Requisitos Previos
- **Python 3.10 o superior** instalado en el sistema.
- Una clave de API válida de **Google Gemini** (`GEMINI_API_KEY`) obtenida en [Google AI Studio](https://aistudio.google.com/).

---

## 3. Instalación de Dependencias
Abre una terminal en la carpeta raíz del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias (`google-generativeai`, `python-dotenv`, `pypdf`, etc.):

```bash
pip install -r requirements.txt
```

---

## 4. Configuración de Variables de Entorno
1. Crea o duplica el archivo `.env.example` renombrándolo a `.env` en la raíz del proyecto.
2. Configura tus credenciales con el siguiente formato:

```env
GEMINI_API_KEY=tu_clave_api_real_aqui
RUTA_OBSIDIAN="C:\Users\TuUsuario\Documents\Obsidian Vault"
```

---

## 5. Ejecución del Sistema

### A. Tutoría Personalizada (CLI)
Inicia el orquestador principal directamente con Python:
```bash
python main.py
```
- Selecciona tu asignatura usando las flechas del teclado `[↑]` `[↓]` y presiona `[ENTER]` (o añade una nueva).
- Ingresa el tema de estudio y el nivel de profundidad deseado.
- Estudia paso a paso de forma interactiva y guarda tus notas automáticamente en Obsidian formando un grafo de constelación.

### B. Herramienta Auxiliar: Extracción de Sílabo (`toJson`)
Si deseas convertir un sílabo (PDF, Markdown o TXT) en un archivo `_cronograma.json` (delimitando estrictamente la sección 4.2):
```bash
python tools/extraer_silabo.py
```
O pasando la ruta como argumento:
```bash
python tools/extraer_silabo.py "ruta/a/tu/silabo.pdf"
```
