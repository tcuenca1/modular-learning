# 🏛️ Arquitectura y Diseño de Sistema - Modular Learning CLI (`ml-cli`)

El sistema es una aplicación de consola (CLI) desarrollada en Python, diseñada para la gestión académica y procesamiento de conocimiento estructurado aplicando el **Principio de Responsabilidad Única (SoC)** y **Arquitectura Hexagonal (Puertos y Adaptadores)**.

---

## 🧩 Estructura de Capas y Módulos (Arquitectura Hexagonal)

- **`cli.py` & `main.py`**:
  - `cli.py`: Enrutador nativo multiplataforma basado en `entry_points` (`ml = cli:app`).
  - `main.py`: Orquestador principal del ciclo de vida de la aplicación CLI y gestión de procesos.

- **`modules/core/` (Núcleo del Sistema y Dominio Académico)**:
  - **`domain/`**: Lógica de negocio pura y reglas de dominio (`alineador_curricular.py`, `sincronizador.py`). Independiente de infraestructura externa o adaptadores.
  - **`ports/`**: Interfaces abstractas (Contratos).
  - **`adapters/`**: Implementaciones concretas de infraestructura y persistencia (incluyendo `llm_gemini_adapter.py` actualizado al moderno SDK `google.genai`).
  - **`services/`**: Casos de uso y orquestación (`gestor_archivos.py`).

- **`modules/ui/` (Capa de Interfaz de Usuario)**:
  - `formateador.py`: Renderizado y formateo universal de texto con Rich.
  - `interaccion.py`: Menús interactivos multiplataforma con `questionary.select()`.

- **`modules/plugins/` (Sistema de Adaptadores y Memoria Técnica)**:
  - Adaptadores específicos por dominio tecnológico (`plugin_cisco.py`, `plugin_nodered.py`, `plugin_web.py`).

- **`tools/` (Herramientas Auxiliares)**:
  - `extraer_silabo.py`, `ingestar_material.py`, `actualizar_plugins.py`.

---

## 🔄 Ciclos de Procesamiento y Memoria Persistente
1. **Cronogramas**: Gestión y actualización automática de estados de clases en `data/schedules/`.
2. **Memoria de Plugins**: Persistencia de datos y registros en `data/plugins/`.
