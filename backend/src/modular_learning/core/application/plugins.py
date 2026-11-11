"""Servicio de aplicación para la gestión y configuración de plugins prácticos interactivos."""

from __future__ import annotations

import os
from typing import Any

from modular_learning.core.domain.materias import slug_materia
from modular_learning.core.domain.rutas import esta_dentro
from modular_learning.core.ports.config import AjustesPort
from modular_learning.core.ports.documentos import LectorDocumentosPort
from modular_learning.core.ports.plugin_practico import (
    PluginConfigRepoPort,
    PluginPracticoBase,
)

METADATOS_PLUGINS: dict[str, dict[str, str]] = {
    "cisco": {
        "id": "cisco",
        "nombre": "Cisco Packet Tracer",
        "opcion_key": "Cisco (Actividades)",
        "categoria": "Redes y Telecomunicaciones",
        "descripcion": "Extrae topologías, VLANs, interfaces y enrutamiento desde show running-config y comandos IOS.",
        "materia_defecto": "tecnologias-de-conmutacion-i",
    },
    "nodered": {
        "id": "nodered",
        "nombre": "Node-RED",
        "opcion_key": "Node-RED (Flujos JSON)",
        "categoria": "Internet de las Cosas",
        "descripcion": "Lee tus flujos JSON por pestañas: nodos, tópicos MQTT, sensores y endpoints HTTP.",
        "materia_defecto": "internet-de-las-cosas",
    },
    "web": {
        "id": "web",
        "nombre": "Proyectos Web y Software",
        "opcion_key": "Web (Proyectos)",
        "categoria": "Desarrollo de Software",
        "descripcion": "Inspecciona la estructura de tu proyecto: README, dependencias, rutas, modelos y últimos commits.",
        "materia_defecto": "programacion-web",
    },
}


class PluginsService:
    """Caso de uso para el enrutamiento, análisis y sincronización de adaptadores prácticos."""

    def __init__(
        self,
        plugins: dict[str, PluginPracticoBase] | None = None,
        ajustes_port: AjustesPort | None = None,
        carpeta_plugins: str | None = None,
        lector_docs: LectorDocumentosPort | None = None,
        config_repo: PluginConfigRepoPort | None = None,
    ):
        self._plugins = dict(plugins or {})
        self.ajustes_port = ajustes_port
        self.carpeta_plugins = carpeta_plugins
        self.lector_docs = lector_docs
        self.config_repo = config_repo

    @property
    def plugins(self) -> dict[str, PluginPracticoBase]:
        """Catálogo de plugins registrados (copia)."""
        return dict(self._plugins)

    def _listar_archivos(self, carpeta: str | None) -> list[str]:
        if not carpeta or not self.lector_docs:
            return []
        return self.lector_docs.listar_archivos(carpeta) or []

    def _existe_carpeta(self, carpeta: str | None) -> bool:
        if not carpeta or not self.lector_docs:
            return False
        return self.lector_docs.listar_archivos(carpeta, recursivo=False) is not None

    def registrar_plugin(self, clave: str, plugin: PluginPracticoBase) -> None:
        """Registra un plugin práctico en el catálogo de plugins activos."""
        self._plugins[clave.lower().strip()] = plugin

    def obtener_configuraciones(self) -> dict[str, dict[str, Any]]:
        """Retorna las configuraciones de carpetas y materias de los plugins."""
        if not self.config_repo:
            return {}
        return self.config_repo.obtener_configuraciones()

    def _exigir_carpeta_permitida(self, carpeta: str | None) -> None:
        """Una carpeta recibida del cliente debe quedar dentro de la carpeta de material."""
        if not carpeta or not carpeta.strip() or not self.ajustes_port:
            return
        if not esta_dentro(self.ajustes_port.carpeta_material(), carpeta.strip()):
            raise ValueError("La carpeta del plugin debe estar dentro de la carpeta de material.")

    def guardar_configuracion_plugin(
        self, clave: str, carpeta: str | None = None, materia: str | None = None
    ) -> dict[str, Any]:
        """Persiste la carpeta asignada o la materia vinculada a un plugin."""
        clave_norm = clave.lower().strip()
        self._exigir_carpeta_permitida(carpeta)
        if not self.config_repo:
            return {"carpeta": carpeta, "materia": materia}
        return self.config_repo.guardar_configuracion(clave_norm, carpeta, materia)

    def listar_info_plugins(self) -> list[dict[str, Any]]:
        """Retorna información detallada de todos los plugins conocidos con su estado actual."""
        configs = self.obtener_configuraciones()
        resultado: list[dict[str, Any]] = []

        for p_id, meta in METADATOS_PLUGINS.items():
            conf = configs.get(p_id, {})
            carpeta_conf = conf.get("carpeta") or ""
            materia_conf = conf.get("materia") or meta["materia_defecto"]
            carpeta_existe = self._existe_carpeta(carpeta_conf)

            plugin = self._plugins.get(p_id)
            contexto = plugin.cargar_contexto_reciente() if plugin else ""

            resultado.append(
                {
                    "id": p_id,
                    "nombre": meta["nombre"],
                    "opcion_key": meta["opcion_key"],
                    "categoria": meta["categoria"],
                    "descripcion": meta["descripcion"],
                    "carpeta": carpeta_conf,
                    "carpeta_existe": carpeta_existe,
                    "materia": materia_conf,
                    "contexto_reciente": contexto,
                }
            )

        return resultado

    def obtener_plugin(self, materia: str) -> PluginPracticoBase | None:
        """
        Factory / Enrutador de plugins.
        Primero busca coincidencia exacta o por slug en las materias configuradas por plugin.
        Si no hay coincidencia, usa heurística por palabras clave.
        """
        materia_slug = slug_materia(materia)
        configs = self.obtener_configuraciones()

        # 1. Coincidencia explícita con materia configurada en cada plugin
        for p_id, conf in configs.items():
            conf_materia = conf.get("materia")
            if conf_materia and slug_materia(conf_materia) == materia_slug:
                return self._plugins.get(p_id)

        # 2. Coincidencia con materia por defecto de los plugins
        for p_id, meta in METADATOS_PLUGINS.items():
            if slug_materia(meta["materia_defecto"]) == materia_slug:
                return self._plugins.get(p_id)

        # 3. Heurística general por palabras clave
        materia_lower = materia.lower()
        if any(
            kw in materia_lower
            for kw in ["redes", "conmutacion", "cisco", "routing", "packet tracer"]
        ):
            return self._plugins.get("cisco")
        if any(kw in materia_lower for kw in ["iot", "internet", "node", "red"]):
            return self._plugins.get("nodered")
        if any(
            kw in materia_lower
            for kw in ["web", "programacion", "frontend", "backend", "javascript", "html", "css"]
        ):
            return self._plugins.get("web")

        return None

    def procesar_archivo_plugin(self, ruta: str, tipo_plugin: str) -> str:
        """Procesa un archivo específico según el tipo de plugin."""
        tipo_lower = tipo_plugin.lower().strip()
        if tipo_lower in ["iot", "nodered"]:
            plugin = self._plugins.get("nodered")
            if plugin and hasattr(plugin, "analizar_flujo"):
                return plugin.analizar_flujo(ruta)
            return "⚠️ Error: El adaptador Node-RED no está disponible o no soporta el análisis de flujos."
        if tipo_lower in ["cisco", "redes"]:
            plugin = self._plugins.get("cisco")
            if plugin and hasattr(plugin, "analizar_archivo"):
                return plugin.analizar_archivo(ruta)
            return "⚠️ Error: El adaptador Cisco no está disponible o no soporta el análisis de archivos."
        return f"⚠️ Error: Tipo de plugin no soportado para procesamiento: {tipo_plugin}"

    def actualizar_plugin(self, seleccion: str, carpeta_override: str | None = None) -> str:
        """
        Escanea y procesa configuraciones o proyectos según la selección:
        ('cisco', 'web', 'nodered', 'todos', o etiquetas como 'Cisco (Actividades)').
        Usa la carpeta configurada si existe, o busca en rutas convencionales.
        """
        self._exigir_carpeta_permitida(carpeta_override)
        seleccion_lower = seleccion.lower()
        configs = self.obtener_configuraciones()
        resultados: list[str] = []

        ruta_base_uni = (
            self.ajustes_port.carpeta_material() if self.ajustes_port else "C:/Universidad"
        )
        ruta_boveda = self.ajustes_port.ruta_boveda() if self.ajustes_port else "obsidian_vault"

        # --- Node-RED ---
        if (
            "node-red" in seleccion_lower
            or "nodered" in seleccion_lower
            or "todos" in seleccion_lower
        ):
            nodered_plugin = self._plugins.get("nodered")
            if nodered_plugin:
                carpeta_nr = carpeta_override or configs.get("nodered", {}).get("carpeta")
                if self._existe_carpeta(carpeta_nr) and hasattr(nodered_plugin, "analizar_carpeta"):
                    res = nodered_plugin.analizar_carpeta(carpeta_nr)
                    resultados.append(f"### [Node-RED] Carpeta Asignada: `{carpeta_nr}`\n{res}")
                else:
                    rutas_busqueda = [
                        os.path.join(ruta_base_uni, "Internet de las Cosas"),
                        os.path.join(ruta_boveda, "Internet de las Cosas"),
                        self.carpeta_plugins,
                    ]
                    archivos_json = [
                        ruta
                        for base in rutas_busqueda
                        for ruta in self._listar_archivos(base)
                        if ruta.endswith(".json")
                        and "memoria" not in os.path.basename(ruta).lower()
                    ]
                    if archivos_json and hasattr(nodered_plugin, "analizar_flujo"):
                        for arch in archivos_json[:3]:
                            res = nodered_plugin.analizar_flujo(arch)
                            resultados.append(f"### [Node-RED] Archivo: {arch}\n{res}")
                    else:
                        memoria = nodered_plugin.cargar_contexto_reciente()
                        resultados.append(
                            f"### [Node-RED] Sincronización\nContexto activo:\n{memoria or 'Sin flujos registrados.'}"
                        )

        # --- Cisco ---
        if "cisco" in seleccion_lower or "redes" in seleccion_lower or "todos" in seleccion_lower:
            cisco_plugin = self._plugins.get("cisco")
            if cisco_plugin:
                carpeta_cisco = carpeta_override or configs.get("cisco", {}).get("carpeta")
                if self._existe_carpeta(carpeta_cisco) and hasattr(
                    cisco_plugin, "analizar_carpeta"
                ):
                    res = cisco_plugin.analizar_carpeta(carpeta_cisco)
                    resultados.append(f"### [Cisco] Carpeta Asignada: `{carpeta_cisco}`\n{res}")
                else:
                    # Intento de buscar en carpeta de la materia si existe
                    carpeta_materia = os.path.join(ruta_base_uni, "Tecnologias de Conmutacion I")
                    if self._existe_carpeta(carpeta_materia) and hasattr(
                        cisco_plugin, "analizar_carpeta"
                    ):
                        res = cisco_plugin.analizar_carpeta(carpeta_materia)
                        resultados.append(
                            f"### [Cisco] Carpeta de Materia: `{carpeta_materia}`\n{res}"
                        )
                    else:
                        contexto_cisco = cisco_plugin.cargar_contexto_reciente()
                        resultados.append(
                            f"### [Cisco] Sincronización de Redes y Packet Tracer\nContexto activo:\n{contexto_cisco[:1000] or 'Sin actividades registradas.'}"
                        )

        # --- Web / Software ---
        if "web" in seleccion_lower or "todos" in seleccion_lower:
            web_plugin = self._plugins.get("web")
            if web_plugin:
                carpeta_web = carpeta_override or configs.get("web", {}).get("carpeta")
                if self._existe_carpeta(carpeta_web) and hasattr(web_plugin, "analizar_proyecto"):
                    res = web_plugin.analizar_proyecto(carpeta_web)
                    resultados.append(f"### [Web] Proyecto Asignado: `{carpeta_web}`\n{res}")
                else:
                    carpeta_convencional = os.path.join(ruta_base_uni, "Programacion Web")
                    if self._existe_carpeta(carpeta_convencional) and hasattr(
                        web_plugin, "analizar_proyecto"
                    ):
                        res = web_plugin.analizar_proyecto(carpeta_convencional)
                        resultados.append(
                            f"### [Web] Proyecto Convencional: `{carpeta_convencional}`\n{res}"
                        )
                    else:
                        contexto_web = web_plugin.cargar_contexto_reciente()
                        resultados.append(
                            f"### [Web] Sincronización de Programación Web\nContexto activo:\n{contexto_web or 'Sin proyectos web registrados.'}"
                        )

        if not resultados:
            return (
                f"⚠️ No se encontró contenido ni rutas configuradas para la selección: {seleccion}"
            )

        return "\n\n".join(resultados)


__all__ = ["METADATOS_PLUGINS", "PluginsService"]
