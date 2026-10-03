from typing import Optional
from modules.plugins.ports.base_plugin import PluginPracticoBase
from modules.plugins.adapters.plugin_cisco import CiscoPlugin
from modules.plugins.adapters.plugin_nodered import NodeRedPlugin
from modules.plugins.adapters.plugin_web import WebPlugin


def obtener_plugin(materia: str) -> Optional[PluginPracticoBase]:
    """
    Factory / Enrutador de plugins. 
    Evalúa el nombre de la asignatura y retorna el adaptador práctico correspondiente (Hexagonal).
    """
    materia_lower = materia.lower()
    
    # Coincidencias para Cisco / Redes / Conmutación
    if any(kw in materia_lower for kw in ["redes", "conmutacion", "cisco", "routing", "packet tracer"]):
        return CiscoPlugin()
        
    # Coincidencias para IoT / Node-RED / Internet de las Cosas
    if any(kw in materia_lower for kw in ["iot", "internet", "node", "red"]):
        return NodeRedPlugin()

    # Coincidencias para Desarrollo y Programación Web
    if any(kw in materia_lower for kw in ["web", "programacion", "frontend", "backend", "javascript", "html", "css"]):
        return WebPlugin()
        
    return None
