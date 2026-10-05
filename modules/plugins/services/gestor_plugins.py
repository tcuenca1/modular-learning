from modules.plugins.adapters.plugin_cisco import CiscoPlugin
from modules.plugins.adapters.plugin_nodered import NodeRedPlugin
from modules.plugins.adapters.plugin_web import WebPlugin
from modules.plugins.ports.base_plugin import PluginPracticoBase


def obtener_plugin(materia: str) -> PluginPracticoBase | None:
    """
    Factory / Enrutador de plugins.
    Evalúa el nombre de la asignatura y retorna el adaptador práctico correspondiente (Hexagonal).
    """
    materia_lower = materia.lower()

    # Coincidencias para Cisco / Redes / Conmutación
    if any(
        kw in materia_lower for kw in ["redes", "conmutacion", "cisco", "routing", "packet tracer"]
    ):
        return CiscoPlugin()

    # Coincidencias para IoT / Node-RED / Internet de las Cosas
    if any(kw in materia_lower for kw in ["iot", "internet", "node", "red"]):
        return NodeRedPlugin()

    # Coincidencias para Desarrollo y Programación Web
    if any(
        kw in materia_lower
        for kw in ["web", "programacion", "frontend", "backend", "javascript", "html", "css"]
    ):
        return WebPlugin()

    return None


def procesar_archivo_plugin(ruta: str, tipo_plugin: str) -> str:
    """
    Procesa un archivo de plugin según su tipo (ej. 'iot', 'nodered').
    Instancia el adaptador correspondiente, analiza el flujo JSON y retorna el texto procesado.
    """
    tipo_lower = tipo_plugin.lower().strip()
    if tipo_lower in ["iot", "nodered"]:
        plugin = NodeRedPlugin()
        if hasattr(plugin, "analizar_flujo"):
            return plugin.analizar_flujo(ruta)
        return "⚠️ Error: El adaptador NodeRedPlugin no soporta el análisis de flujos."
    else:
        return f"⚠️ Error: Tipo de plugin no soportado para procesamiento de flujos: {tipo_plugin}"
