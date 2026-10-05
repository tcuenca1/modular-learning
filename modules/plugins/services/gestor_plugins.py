import os

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


def actualizar_plugin(seleccion: str) -> str:
    """
    Busca dinámicamente y procesa archivos de flujos o proyectos para la selección de plugin indicada
    ('Cisco (Actividades)', 'Web (Proyectos)', 'Node-RED (Flujos JSON)', 'Todos').
    """
    seleccion_lower = seleccion.lower()
    resultados = []
    ruta_base_uni = os.getenv("RUTA_BASE_UNIVERSIDAD", "C:/Universidad")

    rutas_busqueda = [
        os.path.join(ruta_base_uni, "Internet de las Cosas"),
        os.path.join("obsidian_vault", "Internet de las Cosas"),
        os.path.join("data", "plugins"),
    ]

    if "node-red" in seleccion_lower or "todos" in seleccion_lower:
        nodered_plugin = NodeRedPlugin()
        archivos_json = []
        for base in rutas_busqueda:
            if os.path.exists(base):
                for root, dirs, files in os.walk(base):
                    for f in files:
                        if f.endswith(".json") and "memoria" not in f.lower():
                            archivos_json.append(os.path.join(root, f))

        if archivos_json:
            for arch in archivos_json[:3]:
                res = nodered_plugin.analizar_flujo(arch)
                resultados.append(f"### [Node-RED] Archivo: {arch}\n{res}")
        else:
            memoria = nodered_plugin.cargar_contexto_reciente()
            resultados.append(
                f"### [Node-RED] Sin flujos JSON nuevos en rutas automáticas.\nMemoria actual:\n{memoria or 'Sin registros.'}"
            )

    if "cisco" in seleccion_lower or "todos" in seleccion_lower:
        cisco_plugin = CiscoPlugin()
        contexto_cisco = cisco_plugin.cargar_contexto_reciente()
        resultados.append(
            f"### [Cisco] Sincronización de Redes y Packet Tracer\nContexto activo:\n{contexto_cisco[:500] or 'Sin actividades registradas.'}"
        )

    if "web" in seleccion_lower or "todos" in seleccion_lower:
        web_plugin = WebPlugin()
        try:
            ruta_web = os.path.join(ruta_base_uni, "Programacion Web")
            if not os.path.exists(ruta_web):
                ruta_web = os.path.join("obsidian_vault", "Programacion Web")
            proyectos = []
            if os.path.exists(ruta_web):
                for root, dirs, files in os.walk(ruta_web):
                    for f in files:
                        if f.endswith((".js", ".html", ".css", ".md")):
                            proyectos.append(os.path.join(root, f))
            if proyectos:
                web_plugin.guardar_contexto_extraido(
                    f"Proyectos detectados: {len(proyectos)} archivos en {ruta_web}"
                )
            contexto_web = web_plugin.cargar_contexto_reciente()
            resultados.append(
                f"### [Web] Sincronización de Programación Web\nContexto activo:\n{contexto_web or 'Sin proyectos web registrados.'}"
            )
        except Exception as e:
            resultados.append(f"### [Web] Advertencia al escanear proyectos web: {e}")

    if not resultados:
        return f"⚠️ No se encontró contenido ni rutas para la selección: {seleccion}"

    return "\n\n".join(resultados)
