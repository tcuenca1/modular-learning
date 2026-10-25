"""Servicio de aplicación de telemetría y dashboard de avance académico."""

from __future__ import annotations

from typing import Any

from modular_learning.core.ports.plugin_practico import PluginPracticoBase
from modular_learning.core.ports.repositorios import CronogramaRepo


class TelemetriaService:
    """Caso de uso para el cálculo de progreso global, por materia y plugins activos."""

    def __init__(
        self,
        cronograma_repo: CronogramaRepo,
        plugins: dict[str, PluginPracticoBase] | None = None,
    ):
        self.cronograma_repo = cronograma_repo
        self.plugins = dict(plugins or {})

    def _contar_plugins_activos(self) -> int:
        """Un plugin está activo cuando ya acumuló memoria de contexto técnico."""
        activos = 0
        for plugin in self.plugins.values():
            try:
                if plugin.cargar_contexto_reciente():
                    activos += 1
            except Exception:
                continue
        return activos

    def obtener_estadisticas(self) -> dict[str, Any]:
        """Calcula estadísticas de avance académico y estado de módulos."""
        total_temas = 0
        temas_completados = 0
        materias_stats: dict[str, dict[str, Any]] = {}

        for materia, clases in self.cronograma_repo.listar_cronogramas().items():
            m_total = len(clases)
            m_completados = sum(
                1 for c in clases if str(c.get("estado", "")).lower() == "completado"
            )
            total_temas += m_total
            temas_completados += m_completados
            materias_stats[materia.title()] = {
                "total": m_total,
                "completados": m_completados,
                "porcentaje": (m_completados / m_total * 100) if m_total > 0 else 0,
            }

        porcentaje_global = (temas_completados / total_temas * 100) if total_temas > 0 else 0

        return {
            "total_temas": total_temas,
            "temas_completados": temas_completados,
            "porcentaje_global": porcentaje_global,
            "materias": materias_stats,
            "plugins_activos": self._contar_plugins_activos(),
        }


__all__ = ["TelemetriaService"]
