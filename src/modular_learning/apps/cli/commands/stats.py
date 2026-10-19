"""Comando CLI: `ml stats` - Dashboard de telemetría y progreso académico."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from rich.table import Table

from modular_learning import bootstrap

console = Console()


def run(container: bootstrap.Container | None = None) -> None:
    """Muestra el Dashboard visual de telemetría y progreso académico."""
    cont = container or bootstrap.get_container()
    telemetria_service = cont.telemetria_service

    stats = telemetria_service.obtener_estadisticas()
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]📊 TELEMETRÍA Y DASHBOARD DE APRENDIZAJE[/bold cyan]\n[italic]Modular Learning CLI - Estado del Sistema[/italic]",
            border_style="cyan",
        )
    )

    total = stats.get("total_temas", 0)
    completados = stats.get("temas_completados", 0)
    pct = stats.get("porcentaje_global", 0.0)

    console.print(
        f"\n[bold]Progreso Académico Global:[/bold] {completados}/{total} temas completados ({pct:.1f}%)"
    )

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        progress.add_task("[cyan]Avance General", total=max(total, 1), completed=completados)

    tabla = Table(title="Desglose por Asignatura", border_style="blue")
    tabla.add_column("Asignatura", style="bold magenta")
    tabla.add_column("Completados", justify="center", style="green")
    tabla.add_column("Total Temas", justify="center", style="yellow")
    tabla.add_column("Avance", justify="right", style="cyan")

    materias_dict = stats.get("materias", {})
    for mat, info in materias_dict.items():
        mat_completados = info.get("completados", 0)
        mat_total = info.get("total", 0)
        mat_pct = info.get("porcentaje", 0.0)
        tabla.add_row(
            mat,
            str(mat_completados),
            str(mat_total),
            f"{mat_pct:.1f}%",
        )

    console.print(tabla)
    plugins_activos = stats.get("plugins_activos", 0)
    console.print(
        f"\n[bold green]🔌 Módulos / Plugins Activos en Memoria:[/bold green] {plugins_activos}\n"
    )


if __name__ == "__main__":
    run()
