# Markdown-Learn CLI & Agents System

Sistema modular y portable de gestión de apuntes en Markdown potenciado por Inteligencia Artificial y agentes autónomos (CrewAI).

---

## 📦 Sistema de Instalación y Dependencias Opcionales

Markdown-Learn ofrece un empaquetado modular y portátil que separa el núcleo ligero de gestión de apuntes del entorno completo de agentes autónomos.

### 1. Usuarios Finales (Versión Ligera)
Para la gestión estándar de notas, comandos de la CLI, tests y exportación sin dependencias pesadas de IA:
```bash
pip install .
```

### 2. Desarrolladores y Entorno de Agentes
Para habilitar el orquestador inteligente, agentes autónomos (CrewAI) y el ecosistema completo de desarrollo:
```bash
pip install -e ".[dev]"
```

---

## 🖥️ CLI Reference

La interfaz de línea de comandos (`ml`) proporciona los siguientes comandos principales:

- `ml init`: Inicializa la estructura de directorios y configuración por defecto para Markdown-Learn en el directorio actual.
- `ml es`: Exporta los apuntes a diferentes formatos (HTML, PDF, etc.).
- `ml im`: Importa notas y recursos externos al repositorio de Markdown.
- `ml up`: Actualiza el índice y los metadatos de los documentos locales.
- `ml quiz`: Genera cuestionarios interactivos basados en los apuntes utilizando modelos de lenguaje.
- `ml stats`: Muestra estadísticas detalladas sobre el progreso de estudio, cantidad de apuntes y etiquetas.
- `ml dev`: Ejecuta el orquestador de agentes y utilidades de desarrollo (requiere `.[dev]`).

---

## 🚀 Uso Rápido

```bash
# Inicializar entorno
ml init

# Ver estadísticas
ml stats
```
