"""Comando CLI: `ml quiz` - Motor de Recuerdo Activo y evaluación formativa."""

from __future__ import annotations

import questionary
from rich.console import Console

from modular_learning import bootstrap
from modular_learning.apps.cli.ui.spinner import spinner

console = Console()


def run(container: bootstrap.Container | None = None) -> None:
    """Ejecuta el quiz interactivo de recuerdo activo como adaptador fino."""
    cont = container or bootstrap.get_container()
    evaluacion_service = cont.evaluacion_service

    console.print("\n[bold cyan]🧠 [Motor de Recuerdo Activo - Quiz Académico][/bold cyan]\n")

    try:
        with spinner("Generando preguntas de repaso activo basadas en tus avances..."):
            preguntas = evaluacion_service.generar_quiz()
    except Exception as e:
        console.print(f"[red]❌ Error al generar el quiz: {e}[/red]")
        return

    if not preguntas:
        console.print("[yellow]⚠️ No hay preguntas disponibles o no se encontraron temas completados.[/yellow]")
        return

    puntuacion = 0
    total = len(preguntas)

    for idx, p in enumerate(preguntas, 1):
        enunciado = p.get("enunciado", "Pregunta")
        console.print(f"[bold yellow]Pregunta {idx}/{total}:[/bold yellow] {enunciado}")
        opciones = p.get("opciones", [])
        respuesta_correcta = p.get("respuesta_correcta", "")

        try:
            seleccion = questionary.select(
                "Elige tu respuesta:",
                choices=opciones,
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
            console.print("\n[yellow]⚠️ Quiz cancelado por el usuario.[/yellow]")
            return

        if seleccion.strip().lower() == respuesta_correcta.strip().lower():
            console.print("[green]✔ ¡Correcto![/green]\n")
            puntuacion += 1
        else:
            console.print(
                f"[red]✖ Incorrecto. La respuesta correcta era: {respuesta_correcta}[/red]\n"
            )

    pct = (puntuacion / total) * 100 if total > 0 else 0
    console.print("=" * 50)
    console.print(
        f" [bold]📊 Puntuación final: {puntuacion} de {total} ({pct:.0f}%)[/bold]"
    )
    console.print("=" * 50 + "\n")


if __name__ == "__main__":
    run()
