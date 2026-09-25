## 🏛️ Visión General del Sistema
El sistema es una plataforma de tutoría y gestión de conocimiento académica basada en consola (CLI), desarrollada en Python y conectada a los modelos de Google Gemini (`gemini-3.5-flash-lite`). Su propósito central es automatizar procesos críticos para estudiantes universitarios:
1. **Tutoría Interactiva Guiada**: Sesiones de estudio personalizadas paso a paso sobre cualquier asignatura y tema, adaptándose al nivel de profundidad y aplicando adaptadores prácticos mediante un **Sistema de Plugins (Arquitectura Hexagonal)**. Al finalizar, consolida el conocimiento en una guía con autoevaluación exportada automáticamente a una bóveda local de Obsidian en forma de constelación de grafos.
2. **Procesamiento y Extracción de Sílabos**: Una herramienta auxiliar (`tools/extraer_silabo.py`) que procesa en lote o individualmente documentos institucionales (PDF, Markdown, TXT), delimitando la Sección 4.2 y generando bases de datos de cronogramas en formato JSON (`data/{materia}_cronograma.json`).
3. **Ingesta Inteligente de Material de Estudio**: Herramienta multimodal (`tools/ingestar_material.py`) que procesa diapositivas y documentos mediante la File API de Gemini, extrayendo texto y describiendo semánticamente diagramas e imágenes con Wikilinks y Frontmatter para Obsidian.

---

## 🧩 Arquitectura, Módulos y Principio de Responsabilidad Única (SoC)
El sistema cumple estrictamente con el **Principio de Responsabilidad Única (Single Responsibility Principle - SRP)** al separar en capas desacopladas:

- **`main.py` (Orquestador Principal)**: Coordina el ciclo de vida de la tutoría CLI. Actúa exclusivamente como director del flujo sin mezclar lógica de red ni de interfaz de usuario.
- **`modules/core/` (Capa Lógica de Negocio y Persistencia)**:
  - `ai_gemini.py`: Servicio de comunicación con la API de Google Generative AI. Gestiona la configuración del modelo, consultas de texto, Structured Outputs en JSON y spinners animados con `halo`.
  - `gestor_archivos.py`: Servicio de persistencia y disco. Lee prompts externos, gestiona asignaturas en `data/materias.txt`, consulta cronogramas pendientes en `data/`, y exporta notas Markdown con Frontmatter y Wikilinks hacia Obsidian.
- **`modules/ui/` (Capa de Interfaz de Usuario)**:
  - `formateador.py`: Responsable exclusivamente de renderizar y estilizar sintaxis Markdown con colores ANSI en la consola (`imprimir_markdown_bonito`).
  - `interaccion.py`: Administra la entrada del usuario, menús interactivos multiplataforma con `questionary.select()`, y gestión de inputs/pausas de estudio.
- **`modules/plugins/` (Arquitectura Hexagonal / Puertos y Adaptadores)**:
  - `base_plugin.py`: Puerto base (`PluginPracticoBase`).
  - `plugin_cisco.py` & `plugin_nodered.py`: Adaptadores prácticos para inyectar directivas técnicas y ejercicios boilerplate específicos de Redes/Cisco e IoT/Node-RED.
  - `gestor_plugins.py`: Factory/enrutador que selecciona dinámicamente el plugin según la asignatura.
- **`tools/` (Herramientas Auxiliares)**:
  - `extraer_silabo.py`: Ingesta de sílabos a cronogramas JSON en `data/`.
  - `ingestar_material.py`: Ingesta multimodal de diapositivas y apuntes con visión de Gemini.
- **`prompts/` (Motor de Instrucciones Externas)**: Contiene todas las directivas en formato Markdown (`01_roadmap_aprendizaje.md`, `02_explicacion_tema.md`, `03_resumen_evaluacion.md`, `04_extraccion_silabo.md`).

---

## 🔄 Flujo de Ejecución (Paso a Paso)

### Flujo A: Tutoría Personalizada (`main.py`)
1. **Paso 1**: Se cargan variables de entorno (`.env`) y se invoca `interaccion.pedir_datos_inicio()`. Se despliega un menú interactivo con `questionary` cargando asignaturas de `data/materias.txt`. El usuario selecciona la asignatura o añade una nueva.
2. **Paso 2**: Se consultan las clases pendientes del cronograma de la asignatura (`data/{materia}_cronograma.json`). El usuario puede seleccionar una clase pendiente del sílabo o ingresar un tema manual, definiendo el nivel de profundidad.
3. **Paso 3**: Se genera el roadmap estructurado en JSON mediante Structured Outputs de Gemini (`ai_gemini.consultar_gemini_json()`).
4. **Paso 4**: El orquestador recorre cada paso del roadmap. Mediante el patrón Hexagonal, se consulta a `gestor_plugins.obtener_plugin(materia)`: si la asignatura es práctica (ej. Redes o IoT), se inyectan reglas de system prompt y boilerplate técnico al prompt de explicación.
5. **Paso 5**: Se presenta la explicación con spinners animados de `halo` y formato Markdown estilizado (`formateador.py`). Se abre un bucle de resolución de dudas con contexto conversacional.
6. **Paso 6**: Al concluir, se genera la guía de repaso y autoevaluación (`03_resumen_evaluacion.md`), guardándola en Obsidian con Wikilinks bidireccionales y actualizando el nodo índice raíz para constelación de grafos.

---

## ⚙️ Diccionario de Funciones Core

- **`modules.core.ai_gemini.consultar_gemini_json(prompt: str) -> dict`**: Exige Structured Outputs en JSON a Gemini utilizando `response_mime_type="application/json"` con spinner `halo`.
- **`modules.core.gestor_archivos.obtener_proximas_clases(materia: str) -> list`**: Lee el cronograma JSON de la asignatura en `data/` y filtra las primeras 5 clases con estado pendiente.
- **`modules.ui.interaccion.seleccionar_con_flechas(opciones: list) -> str`**: Despliega un menú interactivo multiplataforma usando `questionary.select()`.
- **`modules.ui.formateador.imprimir_markdown_bonito(texto: str) -> None`**: Aplica colores ANSI y formato visual a títulos y viñetas en la consola.
- **`modules.plugins.gestor_plugins.obtener_plugin(materia: str) -> PluginPracticoBase | None`**: Enruta y devuelve el adaptador práctico adecuado según las palabras clave de la asignatura.
