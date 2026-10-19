"""Servicio de aplicación para la gestión de plugins prácticos interactivos."""

from __future__ import annotations

import os

from modular_learning import settings
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.plugin_practico import PluginPracticoBase


class PluginsService:
    """Caso de uso para el enrutamiento, análisis y sincronización de adaptadores prácticos."""

    def __init__(
        self,
        plugins: dict[str, PluginPracticoBase] | None = None,
        ajustes_port: AjustesPort | None = None,
        carpeta_plugins: str | None = None,
    ):
        self._plugins = dict(plugins or {})
        self.ajustes_port = ajustes_port
        self._carpeta_plugins = carpeta_plugins

    @property
    def carpeta_plugins(self) -> str:
        return self._carpeta_plugins or str(settings.ruta_plugins_memoria())

    def registrar_plugin(self, clave: str, plugin: PluginPracticoBase) -> None:
        """Registra un plugin práctico en el catálogo de plugins activos."""
        self._plugins[clave.lower().strip()] = plugin

    def obtener_plugin(self, materia: str) -> PluginPracticoBase | None:
        """
        Factory / Enrutador de plugins.
        Evalúa el nombre de la asignatura y retorna el adaptador práctico registrado correspondiente.
        """
        materia_lower = materia.lower()

        # Coincidencias para Cisco / Redes / Conmutación
        if any(
            kw in materia_lower
            for kw in ["redes", "conmutacion", "cisco", "routing", "packet tracer"]
        ):
            return self._plugins.get("cisco")

        # Coincidencias para IoT / Node-RED / Internet de las Cosas
        if any(kw in materia_lower for kw in ["iot", "internet", "node", "red"]):
            return self._plugins.get("nodered")

        # Coincidencias para Desarrollo y Programación Web
        if any(
            kw in materia_lower
            for kw in ["web", "programacion", "frontend", "backend", "javascript", "html", "css"]
        ):
            return self._plugins.get("web")

        return None

    def procesar_archivo_plugin(self, ruta: str, tipo_plugin: str) -> str:
        """
        Procesa un archivo de plugin según su tipo (ej. 'iot', 'nodered').
        Analiza el flujo JSON y retorna el texto procesado.
        """
        tipo_lower = tipo_plugin.lower().strip()
        if tipo_lower in ["iot", "nodered"]:
            plugin = self._plugins.get("nodered")
            if plugin and hasattr(plugin, "analizar_flujo"):
                return plugin.analizar_flujo(ruta)
            return "⚠️ Error: El adaptador NodeRed no está disponible o no soporta el análisis de flujos."
        return f"⚠️ Error: Tipo de plugin no soportado para procesamiento de flujos: {tipo_plugin}"

    def actualizar_plugin(self, seleccion: str) -> str:
        """
        Busca dinámicamente y procesa archivos de flujos o proyectos para la selección de plugin indicada
        ('Cisco (Actividades)', 'Web (Proyectos)', 'Node-RED (Flujos JSON)', 'Todos').
        """
        seleccion_lower = seleccion.lower()
        resultados = []

        ruta_base_uni = (
            self.ajustes_port.carpeta_material() if self.ajustes_port else "C:/Universidad"
        )
        ruta_boveda = (
            self.ajustes_port.ruta_boveda() if self.ajustes_port else "obsidian_vault"
        )

        rutas_busqueda = [
            os.path.join(ruta_base_uni, "Internet de las Cosas"),
            os.path.join(ruta_boveda, "Internet de las Cosas"),
            self.carpeta_plugins,
        ]

        if "node-red" in seleccion_lower or "todos" in seleccion_lower:
            nodered_plugin = self._plugins.get("nodered")
            if nodered_plugin:
                archivos_json = []
                for base in rutas_busqueda:
                    if os.path.exists(base):
                        for root, _, files in os.walk(base):
                            for f in files:
                                if f.endswith(".json") and "memoria" not in f.lower():
                                    archivos_json.append(os.path.join(root, f))

                if archivos_json and hasattr(nodered_plugin, "analizar_flujo"):
                    for arch in archivos_json[:3]:
                        res = nodered_plugin.analizar_flujo(arch)
                        resultados.append(f"### [Node-RED] Archivo: {arch}\n{res}")
                else:
                    memoria = nodered_plugin.cargar_contexto_reciente()
                    resultados.append(
                        f"### [Node-RED] Sin flujos JSON nuevos en rutas automáticas.\nMemoria actual:\n{memoria or 'Sin registros.'}"
                    )

        if "cisco" in seleccion_lower or "todos" in seleccion_lower:
            cisco_plugin = self._plugins.get("cisco")
            if cisco_plugin:
                contexto_cisco = cisco_plugin.cargar_contexto_reciente()
                resultados.append(
                    f"### [Cisco] Sincronización de Redes y Packet Tracer\nContexto activo:\n{contexto_cisco[:500] or 'Sin actividades registradas.'}"
                )

        if "web" in seleccion_lower or "todos" in seleccion_lower:
            web_plugin = self._plugins.get("web")
            if web_plugin:
                try:
                    ruta_web = os.path.join(ruta_base_uni, "Programacion Web")
                    if not os.path.exists(ruta_web):
                        ruta_web = os.path.join(ruta_boveda, "Programacion Web")
                    proyectos = []
                    if os.path.exists(ruta_web):
                        for root, _, files in os.walk(ruta_web):
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


_instancia_por_defecto: PluginsService | None = None


def configurar_servicio_defecto(servicio: PluginsService) -> None:
    global _instancia_por_defecto
    _instancia_por_defecto = servicio


def obtener_plugin(materia: str) -> PluginPracticoBase | None:
    if _instancia_por_defecto is None:
        return None
    return _instancia_por_defecto.obtener_plugin(materia)


def procesar_archivo_plugin(ruta: str, tipo_plugin: str) -> str:
    if _instancia_por_defecto is None:
        return f"⚠️ PluginsService no inicializado para procesar {tipo_plugin}"
    return _instancia_por_defecto.procesar_archivo_plugin(ruta, tipo_plugin)


def actualizar_plugin(seleccion: str) -> str:
    if _instancia_por_defecto is None:
        return f"⚠️ PluginsService no inicializado para actualizar {seleccion}"
    return _instancia_por_defecto.actualizar_plugin(seleccion)


__all__ = [
    "PluginsService",
    "actualizar_plugin",
    "configurar_servicio_defecto",
    "obtener_plugin",
    "procesar_archivo_plugin",
]
