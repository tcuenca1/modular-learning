# Guía de Instalación - Markdown-Learn

Markdown-Learn se distribuye como un paquete Python modular y portable, permitiendo una instalación ligera para usuarios finales o una instalación completa para desarrollo y agentes autónomos.

## Prerrequisitos

- Python 3.10 o superior.
- `pip` actualizado.

---

## Modos de Instalación

### 1. Versión Ligera (Usuarios Finales)
Ideal para la gestión de notas, comandos CLI y exportación sin requerir dependencias pesadas de IA o frameworks de agentes:
```bash
pip install .
```

### 2. Entorno de Desarrollo y Agentes (Desarrolladores)
Instala todas las dependencias del núcleo junto con el ecosistema de CrewAI, orquestadores y herramientas de desarrollo:
```bash
pip install -e ".[dev]"
```

---

## Configuración de Variables de Entorno

Para utilizar las funciones avanzadas de IA y los agentes autónomos, configura tu clave de API de Gemini:

```bash
export GEMINI_API_KEY="tu-api-key-aqui"
```
