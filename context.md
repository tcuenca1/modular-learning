## 🏛️ Visión General del Sistema
El sistema es una plataforma de tutoría y gestión de conocimiento académica basada en consola (CLI), desarrollada en Python y conectada a los modelos de lenguaje de Google Gemini (`gemini-3.5-flash-lite` y `gemini-1.5-flash`). Su propósito central es automatizar dos procesos críticos para estudiantes universitarios:
1. **Tutoría Interactiva Guiada**: Conduce sesiones de estudio personalizadas paso a paso sobre cualquier asignatura y tema, adaptándose al nivel de profundidad técnica seleccionado y manteniendo un historial conversacional contextual para resolver dudas en tiempo real. Al finalizar, consolida el conocimiento en una guía de estudio con autoevaluación exportada automáticamente a una bóveda local de Obsidian estructurada en grafos de constelación.
2. **Procesamiento de Sílabos**: Una herramienta auxiliar independiente (`extraer_silabo.py`) que analiza documentos locales (PDFs, Markdown o TXT), delimita estrictamente la sección académica de contenidos (Sección 4.2), extrae el cronograma de clases mediante extracción de texto local con `pypdf` y estructuración semántica con IA, y genera una base de datos estructurada en formato JSON (`_cronograma.json`).

---

## 🧩 Arquitectura y Módulos Principales
La arquitectura se organiza de forma estrictamente modular y desacoplada en el espacio de trabajo:
- **`main.py` (Orquestador Principal)**: Coordina el flujo completo de la sesión de tutoría, desde la selección interactiva de asignaturas hasta la síntesis final y guardado en Obsidian.
- **`modules/` (Capa Lógica de Negocio)**:
  - `ai_gemini.py`: Servicio de comunicación con la API de Google Generative AI. Gestiona la configuración del modelo, los chats multi-turno con historial y las excepciones de red.
  - `gestor_archivos.py`: Servicio de persistencia y gestión de disco. Lee prompts externos, carga y actualiza la lista persistente de asignaturas (`data/materias.txt`), y exporta las notas finales estructurando archivos Markdown con frontmatter y enlaces raíz bidireccionales (`[[Wikilinks]]`) para el grafo de constelación de Obsidian.
  - `interaccion.py`: Interfaz de usuario de terminal (UI). Implementa un menú interactivo navegable mediante las flechas del teclado (`[↑]` / `[↓]`) usando `msvcrt`, formateador de sintaxis Markdown en consola con secuencias de escape ANSI, y gestión de inputs/pausas de estudio.
- **`tools/` (Herramientas Auxiliares)**:
  - `extraer_silabo.py`: Script independiente para la conversión de sílabos institucionales a cronogramas JSON estructurados mediante análisis de texto local y prompts especializados.
- **`prompts/` (Motor de Instrucciones Externas)**: Contiene todas las directivas y roles en formato Markdown (`01_roadmap_aprendizaje.md`, `02_explicacion_tema.md`, `03_resumen_evaluacion.md`, `04_extraccion_silabo.md`). Ningún prompt se encuentra hardcodeado en la lógica del código fuente.
- **`data/` (Capa de Datos)**: Almacena los registros persistentes del sistema, como `materias.txt`.

---

## 🔄 Flujo de Ejecución (Paso a Paso)

### Flujo A: Tutoría Personalizada (`main.py`)
1. **Paso 1 (Selección e Inicialización)**: Se cargan las variables de entorno (`.env`) y se invoca `interaccion.pedir_datos_inicio()`. El sistema lee `data/materias.txt` y despliega un menú interactivo basado en terminal. El usuario selecciona la asignatura con las flechas o añade una nueva. A continuación, ingresa el tema específico de estudio y define el nivel de profundidad (`BÁSICO`, `INTERMEDIO`, `AVANZADO`).
2. **Paso 2 (Generación del Roadmap de Sesión)**: El gestor de archivos lee el prompt `01_roadmap_aprendizaje.md`, inyecta el tema y el objetivo, y envía la petición a `ai_gemini.consultar_gemini()`. La IA devuelve una ruta estructurada de la sesión compuesta por pasos secuenciales (Fundamentos, Desarrollo, Aplicación).
3. **Paso 3 (Bucle Interactivo de Explicación y Dudas)**: El orquestador extrae los pasos lógicos del roadmap. Para cada paso:
   - Carga el prompt `02_explicacion_tema.md`, sustituyendo el subtema actual y el nivel de profundidad.
   - Solicita la explicación técnica al modelo de IA pasando el historial acumulado de la sesión (`contexto_previo`).
   - Imprime el resultado formateado en consola mediante `imprimir_markdown_bonito()`.
   - Se pausa la ejecución (`interaccion.pausa_estudio()`): si el usuario presiona ENTER, el sistema avanza; si escribe una pregunta o duda, se genera una consulta contextual a la IA sin perder el hilo de la clase.
4. **Paso 4 (Consolidación y Exportación a Obsidian)**: Al concluir todos los pasos, se carga el prompt `03_resumen_evaluacion.md`. La IA sintetiza toda la sesión de mentoría generando una guía de repaso con glosario, procesos técnicos paso a paso y autoevaluación.
5. **Paso 5 (Constelación de Datos)**: `gestor_archivos.guardar_resumen_obsidian()` crea el archivo de notas con Frontmatter YAML y Wikilinks de retroalimentación (`[[Asignatura]]`), actualizando simultáneamente un archivo índice raíz en la bóveda para forzar el grafo visual de conexiones en Obsidian.

### Flujo B: Extracción de Sílabos (`tools/extraer_silabo.py`)
1. **Paso 1 (Ingreso y Carga Local)**: El script recibe la ruta del documento (PDF, Markdown o TXT) por argumento de línea de comandos o mediante solicitud interactiva por consola.
2. **Paso 2 (Extracción y Delimitación Estricta)**: 
   - Si es PDF, `pypdf` extrae el texto bruto de todas las páginas de forma local.
   - La función `delimitar_seccion_temas()` escanea el texto buscando exclusivamente el rango entre `"4.2 Estructura de la unidad didáctica por temas"` y `"4.3 Distribución de horas..."`, descartando el resto del documento para optimizar tokens y evitar errores de cuota.
3. **Paso 3 (Estructuración Semántica por IA)**: Se carga el prompt externo `04_extraccion_silabo.md`, se combina con el texto delimitado de la sección 4.2 y se envía a `modelo.generate_content()` configurando estrictamente `response_mime_type="application/json"`.
4. **Paso 4 (Persistencia del Cronograma)**: Se parsea la respuesta JSON garantizando el esquema de clases (fecha, tema, objetivo, contenido, estado pendiente) y se almacena en disco como `[nombre_original]_cronograma.json`.

---

## ⚙️ Diccionario de Funciones Core

- **`modules.ai_gemini.configurar_ia() -> genai.GenerativeModel`**
  - *Recibe*: Nada (lee `GEMINI_API_KEY` del entorno).
  - *Procesa*: Valida la existencia de la clave, configura el SDK y devuelve la instancia del modelo `gemini-3.5-flash-lite`.
  - *Devuelve*: Objeto `GenerativeModel`.

- **`modules.ai_gemini.consultar_gemini(prompt: str, contexto_previo: List[dict] = None) -> str`**
  - *Recibe*: Un texto de instrucción (`prompt`) y opcionalmente el historial de chat (`contexto_previo`).
  - *Procesa*: Inicia una sesión de chat o genera contenido directo contra la API de Gemini manejando excepciones de red.
  - *Devuelve*: La respuesta generada en texto plano (`str`).

- **`modules.gestor_archivos.leer_prompt(nombre_archivo: str) -> str`**
  - *Recibe*: Nombre del archivo de directivas (ej. `'01_roadmap_aprendizaje.md'`).
  - *Procesa*: Construye la ruta absoluta hacia `prompts/` y abre el archivo con codificación UTF-8.
  - *Devuelve*: El contenido completo del prompt (`str`).

- **`modules.gestor_archivos.guardar_resumen_obsidian(materia: str, tema: str, contenido: str, ruta_boveda: str) -> bool`**
  - *Recibe*: Asignatura, nombre del tema, contenido en Markdown generado por la IA y la ruta de la bóveda de Obsidian.
  - *Procesa*: Crea la subcarpeta de la asignatura, sanitiza el nombre del tema, inyecta el Frontmatter YAML y los Wikilinks, escribe el archivo de sesión y actualiza el archivo índice raíz de la asignatura.
  - *Devuelve*: `True` si la operación concluyó con éxito, `False` en caso de excepción.

- **`modules.interaccion.seleccionar_con_flechas(opciones: List[str]) -> str`**
  - *Recibe*: Una lista de opciones en texto (asignaturas disponibles + opción de añadir nueva).
  - *Procesa*: Captura eventos de teclado a bajo nivel mediante la librería estándar `msvcrt` en Windows, permitiendo navegar visualmente con las flechas verticales y confirmar con ENTER mediante borrado dinámico de búfer de terminal.
  - *Devuelve*: La opción seleccionada (`str`).

- **`modules.interaccion.imprimir_markdown_bonito(texto: str) -> None`**
  - *Recibe*: Texto plano que contiene sintaxis Markdown básica.
  - *Procesa*: Analiza línea por línea mediante expresiones regulares (`re.sub`) reemplazando títulos (`#`, `##`, `###`) por colores ANSI (magenta, azul, cian) y formateando negritas (`**`) para una visualización avanzada en consola.
  - *Devuelve*: Ninguno (imprime directamente en `stdout`).

- **`tools.extraer_silabo.delimitar_seccion_temas(texto: str) -> str`**
  - *Recibe*: El texto bruto extraído de un sílabo académico extenso.
  - *Procesa*: Realiza búsquedas insensibles a mayúsculas para localizar los delimitadores numéricos institucionales de la unidad didáctica (Sección 4.2), recortando los bloques irrelevantes (portada, bibliografía, políticas).
  - *Devuelve*: El subconjunto exacto de texto optimizado para análisis (`str`).

---

## ⚠️ Zonas Grises o Complejas
1. **Dependencia del Formato Institucional en `delimitar_seccion_temas()`**: La función asume que los sílabos universitarios utilizan la nomenclatura estándar `"4.2 Estructura de la unidad didáctica por temas"` y `"4.3 Distribución de horas"`. Si una facultad использует un formato de numeración diferente o etiquetas de texto totalmente distintas, la función recurrirá a un mecanismo de seguridad (truncar a 30,000 caracteres) o analizará el documento completo, lo que podría reintroducir advertencias de límites de cuota (Error 429).
2. **Controlador de Teclado Dependiente del Sistema Operativo (`msvcrt`)**: La navegación interactiva con flechas utiliza el módulo nativo `msvcrt`, el cual es exclusivo de plataformas Windows (`win32`). Si el sistema fuera ejecutado en entornos basados en POSIX (Linux o macOS), la función lanzaría un error de importación, limitando la portabilidad multiplataforma actual a menos que se implemente un fallback condicional.
3. **Parsing Dinámico de Roadmaps con Expresiones Regulares**: En `main.py`, la función `extraer_pasos_roadmap()` extrae los pasos buscando patrones estrictos del tipo `### Paso X:`. Si la IA genera un formato de encabezado alternativo que rompa dicha expresión regular, el sistema recurrirá a un array de respaldo estático, lo que podría desalinear la tutoría interactiva del roadmap real generado.
