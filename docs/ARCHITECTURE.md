# 🏛️ Arquitectura y Diseño de Sistema - Modular Learning CLI (`ml-cli`)

El sistema es una plataforma de tutoría y gestión de conocimiento académica basada en consola (CLI), desarrollada en Python y conectada a los modelos de Google Gemini (`gemini-3.5-flash-lite`). Su propósito central es automatizar procesos críticos para estudiantes universitarios aplicando el **Principio de Responsabilidad Única (SoC)** y **Arquitectura Hexagonal (Puertos y Adaptadores)**.

---

## 🧩 Estructura de Capas y Módulos (Arquitectura Hexagonal)

- **`cli.py` & `main.py`**:
  - `cli.py`: Enrutador nativo multiplataforma basado en `entry_points` (`ml = cli:app`). Implementa **Lazy Loading** para el comando `ml dev`, aislando la carga de CrewAI para garantizar una ejecución ligera en usuarios finales.
  - `main.py`: Orquestador principal del ciclo de vida de la tutoría CLI y consumidor del Segundo Cerebro.

- **`modules/core/` (Núcleo del Sistema y Dominio Académico)**:
  - **`domain/`**: Lógica de negocio pura y reglas de dominio (`alineador_curricular.py`, `sincronizador.py`). Jamás debe depender de infraestructura externa o adaptadores.
  - **`ports/`**: Interfaces abstractas (Contratos). `llm_base.py` (`LLMAdapterBase`).
  - **`adapters/`**: Implementaciones concretas (`llm_gemini_adapter.py`).
  - **`services/`**: Casos de uso y orquestación (`gestor_llm.py`, `gestor_archivos.py`).

- **`modules/ui/` (Capa de Interfaz de Usuario)**:
  - `formateador.py`: Renderizado universal de Markdown con Rich y limpieza estricta de LaTeX.
  - `interaccion.py`: Menús interactivos multiplataforma con `questionary.select()`.

- **`modules/plugins/` (Sistema de Adaptadores Prácticos / Memoria Técnica)**:
  - Adaptadores específicos por dominio tecnológico (`plugin_cisco.py`, `plugin_nodered.py`, `plugin_web.py`).

- **`tools/` (Herramientas Auxiliares)**:
  - `extraer_silabo.py`, `ingestar_material.py`, `actualizar_plugins.py`.

- **`modules/agents/` (Orquestación de Agentes con CrewAI y Flujo Estricto)**:
  - `orquestador_crew.py`: Orquestador basado en CrewAI con flujo secuencial estricto y dependencias opcionales:
    1. **QA (`qa_agent`)**: Calidad y verificación de pruebas.
    2. **Guardián de la Arquitectura Hexagonal (`arquitecto_agent`)**: Asegura que el dominio puro no dependa de infraestructura externa.
    3. **Auditor de Seguridad Estática (`seguridad_agent`)**: Previene filtración de credenciales y uso inseguro de `subprocess`.
    4. **Dev (`dev_agent`)**: Corrección y aplicación de parches.
    5. **Agente Técnico de Documentación (`docs_agent`)**: Responsable de la precisión de toda la carpeta `docs/` y `README.md`.
    6. **DevOps (`devops_agent`)**: Consolidación en git con Conventional Commits y resiliencia en pre-commit hooks.
  - `herramientas_agentes.py`: Herramientas especializadas con manejo explícito de errores de terminal y pre-commit.

---

## 🔄 Ciclos de Retroalimentación y Memoria Persistente
1. **Cronogramas**: Actualización automática de clases a `"completado"` en `data/schedules/`.
2. **Memoria de Plugins**: Alimentación de memorias persistentes en `data/plugins/`.
3. **Code Snapshots**: Generación de instantáneas con `ml up` para mentoría personalizada.
