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
    PluginMetadatos,
    PluginPracticoBase,
)


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
        """Retorna información detallada de todos los plugins registrados con su estado actual."""
        configs = self.obtener_configuraciones()
        resultado: list[dict[str, Any]] = []

        for p_id, plugin in self._plugins.items():
            meta = plugin.metadatos
            conf = configs.get(p_id, {})
            carpeta_conf = conf.get("carpeta") or ""

            resultado.append(
                {
                    "id": p_id,
                    "nombre": meta.nombre,
                    "opcion_key": meta.opcion_key,
                    "categoria": meta.categoria,
                    "descripcion": meta.descripcion,
                    "carpeta": carpeta_conf,
                    "carpeta_existe": self._existe_carpeta(carpeta_conf),
                    "materia": conf.get("materia") or meta.materia_defecto,
                    "contexto_reciente": plugin.cargar_contexto_reciente(),
                }
            )

        return resultado

    def obtener_plugin(self, materia: str) -> PluginPracticoBase | None:
        """
        Factory / Enrutador de plugins.
        Primero busca coincidencia exacta o por slug en las materias configuradas por plugin.
        Si no hay coincidencia, usa la materia por defecto y las palabras clave de cada plugin.
        """
        materia_slug = slug_materia(materia)
        configs = self.obtener_configuraciones()

        # 1. Coincidencia explícita con materia configurada en cada plugin
        for p_id, conf in configs.items():
            conf_materia = conf.get("materia")
            if conf_materia and slug_materia(conf_materia) == materia_slug:
                return self._plugins.get(p_id)

        # 2. Coincidencia con la materia por defecto que declara cada plugin
        for plugin in self._plugins.values():
            if slug_materia(plugin.metadatos.materia_defecto) == materia_slug:
                return plugin

        # 3. Heurística por palabras clave que declara cada plugin
        materia_lower = materia.lower()
        for plugin in self._plugins.values():
            if any(kw in materia_lower for kw in plugin.metadatos.palabras_clave):
                return plugin

        return None

    def procesar_archivo_plugin(self, ruta: str, tipo_plugin: str) -> str:
        """Procesa un archivo específico con el plugin que declara ese tipo."""
        tipo_lower = tipo_plugin.lower().strip()
        for plugin in self._plugins.values():
            meta = plugin.metadatos
            if tipo_lower in meta.tipos_archivo:
                resultado = plugin.analizar_archivo(ruta)
                if resultado is not None:
                    return resultado
                return f"⚠️ Error: El adaptador {meta.etiqueta} no soporta el análisis de archivos."
        return f"⚠️ Error: Tipo de plugin no soportado para procesamiento: {tipo_plugin}"

    def actualizar_plugin(self, seleccion: str, carpeta_override: str | None = None) -> str:
        """
        Escanea y procesa configuraciones o proyectos según la selección: 'todos', la clave de
        un plugin o etiquetas como 'Cisco (Actividades)'.
        Usa la carpeta configurada si existe, o busca en rutas convencionales.
        """
        self._exigir_carpeta_permitida(carpeta_override)
        seleccion_lower = seleccion.lower()
        configs = self.obtener_configuraciones()

        ruta_base_uni = (
            self.ajustes_port.carpeta_material() if self.ajustes_port else "C:/Universidad"
        )
        ruta_boveda = self.ajustes_port.ruta_boveda() if self.ajustes_port else "obsidian_vault"

        seleccionados = sorted(
            (
                (p_id, plugin)
                for p_id, plugin in self._plugins.items()
                if "todos" in seleccion_lower
                or any(clave in seleccion_lower for clave in plugin.metadatos.claves_seleccion)
            ),
            key=lambda par: par[1].metadatos.orden_sincronizacion,
        )
        resultados: list[str] = []
        for p_id, plugin in seleccionados:
            carpeta = carpeta_override or configs.get(p_id, {}).get("carpeta")
            resultados.extend(self._sincronizar_plugin(plugin, carpeta, ruta_base_uni, ruta_boveda))

        if not resultados:
            return (
                f"⚠️ No se encontró contenido ni rutas configuradas para la selección: {seleccion}"
            )

        return "\n\n".join(resultados)

    def _sincronizar_plugin(
        self,
        plugin: PluginPracticoBase,
        carpeta: str | None,
        ruta_base_uni: str,
        ruta_boveda: str,
    ) -> list[str]:
        """Secciones de resultado de un plugin: carpeta asignada, convencional o su memoria."""
        meta = plugin.metadatos
        if self._existe_carpeta(carpeta):
            res = plugin.analizar_carpeta(carpeta or "")
            return [f"### [{meta.etiqueta}] {meta.titulo_carpeta_asignada}: `{carpeta}`\n{res}"]

        if meta.extension_archivos:
            secciones = self._analizar_archivos_convencionales(
                plugin, meta, [ruta_base_uni, ruta_boveda]
            )
            if secciones:
                return secciones
        else:
            convencional = os.path.join(ruta_base_uni, meta.carpeta_convencional)
            if meta.carpeta_convencional and self._existe_carpeta(convencional):
                res = plugin.analizar_carpeta(convencional)
                titulo = f"### [{meta.etiqueta}] {meta.titulo_carpeta_convencional}"
                return [f"{titulo}: `{convencional}`\n{res}"]

        contexto = plugin.cargar_contexto_reciente()
        if meta.limite_contexto is not None:
            contexto = contexto[: meta.limite_contexto]
        titulo = f"### [{meta.etiqueta}] {meta.titulo_sincronizacion}"
        return [f"{titulo}\nContexto activo:\n{contexto or meta.texto_sin_contexto}"]

    def _analizar_archivos_convencionales(
        self, plugin: PluginPracticoBase, meta: PluginMetadatos, raices: list[str]
    ) -> list[str]:
        """Analiza (hasta 3) archivos del plugin hallados en sus carpetas convencionales."""
        carpetas = [os.path.join(raiz, meta.carpeta_convencional) for raiz in raices]
        carpetas.append(self.carpeta_plugins or "")
        archivos = [
            ruta
            for carpeta in carpetas
            for ruta in self._listar_archivos(carpeta)
            if ruta.endswith(meta.extension_archivos or "")
            and "memoria" not in os.path.basename(ruta).lower()
        ]
        secciones: list[str] = []
        for arch in archivos[:3]:
            res = plugin.analizar_archivo(arch)
            if res is not None:
                secciones.append(f"### [{meta.etiqueta}] Archivo: {arch}\n{res}")
        return secciones


__all__ = ["PluginsService"]
