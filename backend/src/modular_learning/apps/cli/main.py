"""Punto de entrada principal para la interfaz de línea de comandos (CLI) de Modular Learning."""

from __future__ import annotations

import sys

import typer
from rich.console import Console

app = typer.Typer(add_completion=False, help="Modular Learning CLI (ml)")
console = Console()

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@app.command("init")
def cmd_init() -> None:
    """Inicia la sesión de tutoría interactiva personalizada."""
    from modular_learning.apps.cli.commands import init

    init.run()


@app.command("es")
def cmd_es() -> None:
    """Extraer cronogramas de sílabos (archivos o carpetas)."""
    from modular_learning.apps.cli.commands import es

    es.run()


@app.command("im")
def cmd_im() -> None:
    """Ingestar material de estudio multimodal hacia Obsidian."""
    from modular_learning.apps.cli.commands import im

    im.run()


@app.command("quiz")
def cmd_quiz() -> None:
    """Motor de Recuerdo Activo (Quiz interactivo de temas completados)."""
    from modular_learning.apps.cli.commands import quiz

    quiz.run()


@app.command("stats")
def cmd_stats() -> None:
    """Muestra el Dashboard visual de telemetría y progreso académico."""
    from modular_learning.apps.cli.commands import stats

    stats.run()


@app.command("up")
def cmd_up() -> None:
    """Actualiza e inspecciona los plugins prácticos y flujos (Cisco, Web, Node-RED, Todos)."""
    from modular_learning.apps.cli.commands import up

    up.run()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Modular Learning CLI (ml)."""
    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]🎓 Modular Learning CLI (ml)[/bold cyan]")
        console.print("Usa [bold yellow]ml --help[/bold yellow] para ver los comandos disponibles.")


if __name__ == "__main__":
    app()
