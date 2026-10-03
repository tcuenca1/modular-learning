# 🏛️ Arquitectura y Diseño de Sistema - Modular Learning CLI (ml-cli)

El sistema es una plataforma de tutoría y gestión de conocimiento académica basada en consola (CLI), desarrollada en Python y conectada a los modelos de Google Gemini (`gemini-3.5-flash-lite`). Su propósito central es automatizar procesos críticos para estudiantes universitarios aplicando el **Principio de Responsabilidad Única (SoC)** y **Arquitectura Hexagonal (Puertos y Adaptadores)**.

---

## 🧩 Estructura de Capas y Módulos (Arquitectura Hexagonal)

- **`cli.py` & `main.py`**:
  - `cli.py`: Enrutador nativo multiplataforma basado en `entry_points` con manejo limpio de interrupciones (`Ctrl + C`).
  - `main.py`: Orquestador principal del ciclo de vida de la tutoría CLI y consumidor del Segundo Cerebro.

- **`modules/core/` (Núcleo del Sistema y Dominio Académico)**:
  - **`domain/`**: Lógica de negocio pura y reglas de dominio. Contiene `alineador_curricular.py` (motor de mapeo curricular con pesos y afinidad para el Segundo Cerebro) y `sincronizador.py`.
  - **`ports/`**: Interfaces abstractas (Contratos). Contiene `llm_base.py` (`LLMAdapterBase`), que define el puerto para la comunicación con modelos de lenguaje.
  - **`adapters/`**: Implementaciones concretas de infraestructura para los puertos. Contiene `llm_gemini_adapter.py` para Google Gemini (`gemini-3.5-flash-lite`).
  - **`services/`**: Casos de uso y orquestación de servicios transversales. Contiene `gestor_llm.py` (fábrica/enrutador de proveedores LLM) y `gestor_archivos.py` (persistencia, gestión de asignaturas, cronogramas y exportación a Obsidian).

- **`modules/ui/` (Capa de Interfaz de Usuario)**:
  - `formateador.py`: Renderizado universal de Markdown con colores ANSI y limpieza estricta de artefactos LaTeX (como `$\rightarrow$`).
  - `interaccion.py`: Menús interactivos multiplataforma con `questionary.select()`.

- **`modules/plugins/` (Sistema de Adaptadores Prácticos / Memoria Técnica)**:
  - **`ports/`**: Interfaces base para extensiones prácticas. Contiene `base_plugin.py` (`PluginPracticoBase`).
  - **`adapters/`**: Adaptadores específicos por dominio tecnológico. Contiene `plugin_cisco.py`, `plugin_nodered.py` y `plugin_web.py`.
  - **`services/`**: Enrutador y gestor de adaptadores prácticos. Contiene `gestor_plugins.py`.

- **`tools/` (Herramientas Auxiliares de Ingesta y Procesamiento)**:
  - `extraer_silabo.py`: Extracción masiva de sílabos a cronogramas JSON.
  - `ingestar_material.py`: Ingesta masiva (individual o global por lotes) desde `RUTA_BASE_UNIVERSIDAD`, conversión a PDF, anonimización y alineación curricular.
  - `actualizar_plugins.py`: Generador de Code Snapshots para proyectos locales.

- **`prompts/`**: Directivas externas en Markdown (`01_` a `05_`).

---

## 🔄 Ciclos de Retroalimentación y Memoria Persistente
1. **Cronogramas**: Al completar una sesión de tutoría, se actualiza automáticamente el estado de la clase a `"completado"` en su respectivo JSON bajo `data/schedules/`.
2. **Memoria de Plugins**: Cada ingesta de material extrae extractos técnicos que alimentan las memorias persistentes en `data/plugins/`, permitiendo que la IA mantenga contexto especializado en las sesiones de mentoría práctica.
3. **Code Snapshots**: El comando `ml up` genera una instantánea estructurada del código fuente local del estudiante, inyectándola en el adaptador Web para ofrecer mentoría basada en su propia arquitectura.
