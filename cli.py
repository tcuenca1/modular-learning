import os
import sys
import typer
from rich.console import Console

app = typer.Typer(add_completion=False, help="Modular Learning CLI (ml)")
console = Console()

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


@app.command("init")
def cmd_init():
    """Inicia la sesión de tutoría interactiva personalizada."""
    from main import main as run_main

    run_main()


@app.command("es")
def cmd_es():
    """Extraer cronogramas de sílabos (archivos o carpetas)."""
    from tools import extraer_silabo

    extraer_silabo.run()


@app.command("im")
def cmd_im():
    """Ingestar material de estudio multimodal hacia Obsidian."""
    from tools import ingestar_material

    ingestar_material.run()


@app.command("quiz")
def cmd_quiz():
    """Motor de Recuerdo Activo (Quiz interactivo de temas completados)."""
    import questionary
    from modules.core.services import motor_evaluacion

    console.print("\n[bold cyan]🧠 [Motor de Recuerdo Activo - Quiz Académico][/bold cyan]\n")
    preguntas = motor_evaluacion.generar_quiz()
    puntuacion = 0
    total = len(preguntas)
    for idx, p in enumerate(preguntas, 1):
        console.print(f"[bold yellow]Pregunta {idx}/{total}:[/bold yellow] {p.get('enunciado')}")
        opciones = p.get("opciones", [])
        respuesta_correcta = p.get("respuesta_correcta")
        seleccion = questionary.select("Elige tu respuesta:", choices=opciones).ask()
        if seleccion is None:
            print("\n⚠️ Quiz cancelado por el usuario.")
            sys.exit(0)
        if seleccion.strip().lower() == respuesta_correcta.strip().lower():
            console.print("[green]✔ ¡Correcto![/green]\n")
            puntuacion += 1
        else:
            console.print(
                f"[red]✖ Incorrecto. La respuesta correcta era: {respuesta_correcta}[/red]\n"
            )
    console.print("=" * 50)
    console.print(
        f" [bold]📊 Puntuación final: {puntuacion} de {total} ({(puntuacion/total)*100:.0f}%)[/bold]"
    )
    console.print("=" * 50)


@app.command("stats")
def cmd_stats():
    """Muestra el Dashboard visual de telemetría y progreso académico."""
    from rich.panel import Panel
    from rich.progress import BarColumn, Progress, TextColumn
    from rich.table import Table
    from modules.core.services import telemetria

    stats = telemetria.obtener_estadisticas()
    console.print("\n")
    console.print(
        Panel.fit(
            "[bold cyan]📊 TELEMETRÍA Y DASHBOARD DE APRENDIZAJE[/bold cyan]\n[italic]Modular Learning CLI - Estado del Sistema[/italic]",
            border_style="cyan",
        )
    )
    total = stats["total_temas"]
    completados = stats["temas_completados"]
    pct = stats["porcentaje_global"]
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
    for mat, info in stats["materias"].items():
        tabla.add_row(
            mat, str(info["completados"]), str(info["total"]), f"{info['porcentaje']:.1f}%"
        )
    console.print(tabla)
    console.print(
        f"\n[bold green]🔌 Módulos / Plugins Activos en Memoria:[/bold green] {stats['plugins_activos']}\n"
    )


@app.command("up")
def cmd_up():
    """Actualiza e inspecciona los plugins prácticos y flujos (Cisco, Web, Node-RED, Todos)."""
    import questionary
    from rich.panel import Panel
    from modules.plugins.services import gestor_plugins

    console.print("\n[bold cyan]🔌 [Gestor de Plugins Prácticos y Flujos][/bold cyan]\n")
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

    if seleccion is None:
        console.print("\n⚠️ Operación cancelada por el usuario.")
        sys.exit(0)

    console.print(f"\n[italic]Ejecutando actualización para:[/italic] {seleccion}...\n")
    resultado_texto = gestor_plugins.actualizar_plugin(seleccion)

    console.print(
        Panel(resultado_texto, title=f"Actualización de Plugin: {seleccion}", border_style="green")
    )
    console.print("[bold green]✔ Operación de actualización de plugin finalizada.[/bold green]\n")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Modular Learning CLI (ml)."""
    if ctx.invoked_subcommand is None:
        console.print("[bold cyan]🎓 Modular Learning CLI (ml)[/bold cyan]")
        console.print("Usa [bold yellow]ml --help[/bold yellow] para ver los comandos disponibles.")


if __name__ == "__main__":
    app()
