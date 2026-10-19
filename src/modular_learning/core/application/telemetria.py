import json
import os


def obtener_estadisticas() -> dict:
    """
    Escanea data/schedules/ para calcular el porcentaje de avance (temas completados vs pendientes)
    y cuenta la cantidad de plugins/memorias activas en data/plugins/.
    """
    carpeta_schedules = os.path.join("data", "schedules")
    total_temas = 0
    temas_completados = 0
    materias_stats = {}

    if os.path.exists(carpeta_schedules):
        for arch in os.listdir(carpeta_schedules):
            if arch.endswith("_cronograma.json"):
                materia_nombre = arch.replace("_cronograma.json", "").replace("_", " ").title()
                ruta = os.path.join(carpeta_schedules, arch)
                try:
                    with open(ruta, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        clases = data.get("clases", [])
                        m_total = len(clases)
                        m_completados = sum(1 for c in clases if c.get("estado") == "completado")

                        total_temas += m_total
                        temas_completados += m_completados
                        materias_stats[materia_nombre] = {
                            "total": m_total,
                            "completados": m_completados,
                            "porcentaje": ((m_completados / m_total * 100) if m_total > 0 else 0),
                        }
                except Exception:
                    continue

    carpeta_plugins = os.path.join("data", "plugins")
    plugins_activos = 0
    if os.path.exists(carpeta_plugins):
        plugins_activos = len([f for f in os.listdir(carpeta_plugins) if f.endswith(".json")])

    porcentaje_global = (temas_completados / total_temas * 100) if total_temas > 0 else 0

    return {
        "total_temas": total_temas,
        "temas_completados": temas_completados,
        "porcentaje_global": porcentaje_global,
        "materias": materias_stats,
        "plugins_activos": plugins_activos,
    }
