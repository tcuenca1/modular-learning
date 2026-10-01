# 🏛️ Arquitectura y Diseño de Sistema - Modular Learning CLI (ml-cli)

El sistema es una plataforma de tutoría y gestión de conocimiento académica basada en consola (CLI), desarrollada en Python y conectada a los modelos de Google Gemini (`gemini-3.5-flash-lite`). Su propósito central es automatizar procesos críticos para estudiantes universitarios aplicando el **Principio de Responsabilidad Única (SoC)** y **Arquitectura Hexagonal (Puertos y Adaptadores)**.

---

## 🧩 Estructura de Capas y Módulos

- **`cli.py` & `main.py`**:
  - `cli.py`: Enrutador nativo multiplataforma basado en `entry_points` (`console_scripts`: `ml = "cli:app"`).
  - `main.py`: Orquestador principal del ciclo de vida de la tutoría CLI.
- **`modules/core/` (Capa Lógica de Negocio y Persistencia)**:
  - `gestor_llm.py`: Fábrica y enrutador de adaptadores LLM (Hexagonal).
  - `llm_gemini_adapter.py`: Adaptador concreto para Google Gemini (`gemini-3.5-flash-lite`).
  - `alineador_curricular.py`: Motor de mapeo curricular con pesos y afinidad (Segundo Cerebro), asignando material nuevo a clases oficiales (`subtemas_adicionales` y `materiales_asociados`) o transversalmente.
  - `gestor_archivos.py`: Operaciones de disco, gestión de asignaturas (`data/config/materias.txt`), cronogramas enriquecidos en `data/schedules/`, tracking en `data/config/registro_materiales.json`, y exportación a Obsidian.
- **`modules/ui/` (Capa de Interfaz de Usuario)**:
  - `formateador.py`: Renderizado y estilización universal de sintaxis Markdown con colores ANSI en consola.
  - `interaccion.py`: Menús interactivos multiplataforma con `questionary.select()`.
- **`modules/plugins/` (Arquitectura Hexagonal / Memoria Técnica)**:
  - `base_plugin.py`: Puerto base (`PluginPracticoBase`).
  - `plugin_cisco.py`, `plugin_nodered.py`, `plugin_web.py`: Adaptadores prácticos para Redes/Cisco, IoT/Node-RED y Desarrollo Web, dotados de memoria persistente en `data/plugins/` y sincronización con el Vault.
  - `gestor_plugins.py`: Enrutador dinámico de adaptadores.
- **`tools/` (Herramientas Auxiliares)**:
  - `extraer_silabo.py`: Extracción masiva de sílabos a cronogramas JSON.
  - `ingestar_material.py`: Ingesta masiva (Batch) desde `RUTA_BASE_UNIVERSIDAD`, conversión automática a PDF, anonimización y retroalimentación de plugins.
  - `actualizar_plugins.py`: Generador de Code Snapshots para proyectos locales de desarrollo.
- **`prompts/`**: Directivas externas en Markdown (`01_`, `02_`, `03_`, `04_`, `05_`).

---

## 🔄 Ciclos de Retroalimentación y Memoria Persistente
1. **Cronogramas**: Al completar una sesión de tutoría, se actualiza automáticamente el estado de la clase a `"completado"` en su respectivo JSON bajo `data/schedules/`.
2. **Memoria de Plugins**: Cada ingesta de material extrae extractos técnicos que alimentan las memorias persistentes en `data/plugins/`, permitiendo que la IA mantenga contexto especializado en las sesiones de mentoría práctica.
3. **Code Snapshots**: El comando `ml up` genera una instantánea estructurada del código fuente local del estudiante, inyectándola en el adaptador Web para ofrecer mentoría basada en su propia arquitectura.
