"""Servicio de aplicación de telemetría y dashboard de avance académico."""

from __future__ import annotations

import json
import os
from typing import Any

from modular_learning import settings
from modular_learning.core.ports.repositorios import CronogramaRepo


class TelemetriaService:
    """Caso de uso para el cálculo de progreso global, por materia y plugins activos."""

    def __init__(
        self,
        cronograma_repo: CronogramaRepo | None = None,
        carpeta_schedules: str | None = None,
        carpeta_plugins: str | None = None,
    ):
        self.cronograma_repo = cronograma_repo
        self._carpeta_schedules = carpeta_schedules
        self._carpeta_plugins = carpeta_plugins

    @property
    def carpeta_schedules(self) -> str:
        return self._carpeta_schedules or str(settings.ruta_cronogramas())

    @property
    def carpeta_plugins(self) -> str:
        return self._carpeta_plugins or str(settings.ruta_plugins_memoria())

    def obtener_estadisticas(self) -> dict[str, Any]:
        """Calcula estadísticas de avance académico y estado de módulos."""
        total_temas = 0
        temas_completados = 0
        materias_stats: dict[str, dict[str, Any]] = {}

        if os.path.exists(self.carpeta_schedules):
            for arch in os.listdir(self.carpeta_schedules):
                if arch.endswith("_cronograma.json"):
                    materia_nombre = arch.replace("_cronograma.json", "").replace("_", " ").title()
                    ruta = os.path.join(self.carpeta_schedules, arch)
                    try:
                        with open(ruta, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            clases = data.get("clases", []) if isinstance(data, dict) else data
                            if not isinstance(clases, list):
                                continue
                            m_total = len(clases)
                            m_completados = sum(
                                1 for c in clases if c.get("estado", "").lower() == "completado"
                            )

                            total_temas += m_total
                            temas_completados += m_completados
                            materias_stats[materia_nombre] = {
                                "total": m_total,
                                "completados": m_completados,
                                "porcentaje": (
                                    (m_completados / m_total * 100) if m_total > 0 else 0
                                ),
                            }
                    except Exception:
                        continue

        plugins_activos = 0
        if os.path.exists(self.carpeta_plugins):
            plugins_activos = len([f for f in os.listdir(self.carpeta_plugins) if f.endswith(".json")])

        porcentaje_global = (temas_completados / total_temas * 100) if total_temas > 0 else 0

        return {
            "total_temas": total_temas,
            "temas_completados": temas_completados,
            "porcentaje_global": porcentaje_global,
            "materias": materias_stats,
            "plugins_activos": plugins_activos,
        }


_instancia_por_defecto: TelemetriaService | None = None


def configurar_servicio_defecto(servicio: TelemetriaService) -> None:
    global _instancia_por_defecto
    _instancia_por_defecto = servicio


def obtener_estadisticas() -> dict[str, Any]:
    global _instancia_por_defecto
    if _instancia_por_defecto is None:
        _instancia_por_defecto = TelemetriaService()
    return _instancia_por_defecto.obtener_estadisticas()


__all__ = ["TelemetriaService", "configurar_servicio_defecto", "obtener_estadisticas"]
