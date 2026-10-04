# Arquitectura de Markdown-Learn

Markdown-Learn está diseñado bajo una arquitectura modular, separando la interfaz de línea de comandos (CLI), el núcleo de procesamiento de Markdown y el subsistema de agentes inteligentes basado en CrewAI.

## 1. Carga Perezosa (Lazy Loading) del Orquestador

Para garantizar que los usuarios que instalan la versión ligera (`pip install .`) no sufran errores por dependencias faltantes de CrewAI, el orquestador dentro de `cli.py` se carga mediante **Lazy Loading** (importación diferida).

Si se invoca un comando de agentes sin haber instalado `.[dev]`, el sistema captura la excepción `ImportError` y muestra un mensaje claro indicando que se debe ejecutar `pip install -e ".[dev]"`.

## 2. Flujo de los Agentes Autónomos

El sistema de agentes colabora mediante un flujo estructurado de roles especializados:

- **Arquitecto (Lead Architect):** Diseña la estructura conceptual, la taxonomía y las relaciones lógicas entre los apuntes y módulos de estudio.
- **Desarrollador (Content Developer):** Redacta, expande y formatea el contenido técnico en Markdown siguiendo las directrices del Arquitecto.
- **Seguridad (Security Auditor):** Revisa el contenido y los scripts generados para asegurar el cumplimiento de buenas prácticas, evitando exposición de secretos o vulnerabilidades.
- **Validador (QA Specialist):** Comprueba la precisión técnica, genera tests y cuestionarios (`ml quiz`) basados en el material producido.
