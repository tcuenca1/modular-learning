"""Comando CLI: `ml up` - Actualización e inspección de plugins prácticos."""

from __future__ import annotations

import questionary
from rich.console import Console
from rich.panel import Panel

from modular_learning import bootstrap
from modular_learning.apps.cli.ui.spinner import spinner

console = Console()


def run(container: bootstrap.Container | None = None) -> None:
    """Actualiza e inspecciona los plugins prácticos y flujos como adaptador fino."""
    cont = container or bootstrap.get_container()
    plugins_service = cont.plugins_service

    console.print("\n[bold cyan]🔌 [Gestor de Plugins Prácticos y Flujos][/bold cyan]\n")

    try:
        seleccion = questionary.select(
            "¿Qué plugin de materia deseas actualizar?",
            choices=["Cisco (Actividades)", "Web (Proyectos)", "Node-RED (Flujos JSON)", "Todos"],
            style=questionary.Style(
                [
                    ("pointer", "fg:cyan bold"),
                    ("highlighted", "fg:cyan bold"),
                    ("answer", "fg:green bold"),
                ]
            ),
        ).ask()
    except (KeyboardInterrupt, EOFError):
        seleccion = None

    if seleccion is None:
        console.print("\n[yellow]⚠️ Operación cancelada por el usuario.[/yellow]")
        return

    console.print(f"\n[italic]Ejecutando actualización para:[/italic] {seleccion}...\n")

    try:
        with spinner(f"Actualizando e indexando componentes para '{seleccion}'..."):
            resultado_texto = plugins_service.actualizar_plugin(seleccion)
    except Exception as e:
        console.print(f"[red]❌ Error al actualizar plugin: {e}[/red]")
        return

    console.print(
        Panel(resultado_texto, title=f"Actualización de Plugin: {seleccion}", border_style="green")
    )
    console.print("[bold green]✔ Operación de actualización de plugin finalizada.[/bold green]\n")


if __name__ == "__main__":
    run()
