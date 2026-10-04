# 🎓 Modular Learning CLI (`ml`)

Plataforma de tutoría académica y gestión de conocimiento basada en consola (CLI) conectada a Google Gemini (`gemini-3.5-flash-lite`), diseñada bajo Arquitectura Hexagonal y Principio de Responsabilidad Única (SoC), con exportación automática a Obsidian y orquestación autónoma mediante agentes de IA.

---

## 📦 Sistema de Empaquetado Portátil y Dependencias

Para garantizar una portabilidad total y un inicio ligero, las dependencias pesadas de desarrollo y agentes están aisladas en grupos opcionales:

### 1. Usuario Final (Versión Ligera)
Ideal para estudiantes que solo requieren la CLI de tutoría, ingesta y quizzes:
```bash
pip install .
```

### 2. Desarrolladores y Entorno de Agentes (CrewAI & QA)
Para contribuidores y agentes autónomos que ejecutan pruebas, linter y auditorías de agentes:
```bash
pip install -e ".[dev]"
```

---

## 🚀 Guía de Instalación Rápida

1. Clona el repositorio y sitúate en la raíz.
2. Configura tu archivo `.env` basándote en `.env.example`:
   ```env
   GEMINI_API_KEY=tu_clave_api_de_google_gemini
   RUTA_OBSIDIAN="C:\Users\TuUsuario\Documents\Obsidian Vault"
   RUTA_BASE_UNIVERSIDAD="C:\Universidad"
   ```
3. Instala el paquete en modo editable:
   ```bash
   pip install -e .
   ```

---

## 🛠️ CLI Reference (Comandos Disponibles)

El comando global `ml` ofrece los siguientes subcomandos:

- **`ml init`**
  - **Descripción**: Inicia la sesión de tutoría interactiva personalizada guiada por el tutor IA.
  - **Uso**: `ml init`
- **`ml es`**
  - **Descripción**: Extrae cronogramas de sílabos (PDFs o archivos locales) y genera cronogramas estructurados en JSON.
  - **Uso**: `ml es "ruta/al/silabo.pdf"`
- **`ml im`**
  - **Descripción**: Ingesta masiva y automatizada de material de estudio multimodal (PDFs, PPTx, DOCx) hacia Obsidian con anonimización estricta.
  - **Uso**: `ml im`
- **`ml up`**
  - **Descripción**: Actualiza el contexto técnico y code snapshots de proyectos de desarrollo local en los plugins prácticos.
  - **Uso**: `ml up`
- **`ml quiz`**
  - **Descripción**: Ejecuta el Motor de Recuerdo Activo (quiz interactivo de temas completados).
  - **Uso**: `ml quiz`
- **`ml stats`**
  - **Descripción**: Muestra un Dashboard visual interactivo con telemetría, progreso global y desglose por asignatura.
  - **Uso**: `ml stats`
- **`ml dev`**
  - **Descripción**: Inicia el entorno de desarrollo y auditoría con agentes autónomos (CrewAI con Lazy Loading). Requiere `[dev]`.
  - **Uso**: `ml dev`
- **`ml --help`**
  - **Descripción**: Muestra el panel de ayuda y comandos disponibles.
  - **Uso**: `ml --help`

---

## 🏛️ Arquitectura del Sistema

Consulta [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) para más detalles sobre la Arquitectura Hexagonal, puertos, adaptadores y el funcionamiento del orquestador de agentes.
