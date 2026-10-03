import os
import sys

# Asegurar que el directorio raíz del proyecto esté en el path para ejecución global correcta
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def app():
    """Enrutador principal CLI para Modular Learning CLI (ml)."""
    try:
        if len(sys.argv) < 2:
            mostrar_ayuda()
            return

        comando = sys.argv[1].lower()
        args_restantes = sys.argv[2:]

        if comando == "init":
            from main import main as run_main

            run_main()
        elif comando == "es":
            from tools import extraer_silabo

            sys.argv = [sys.argv[0]] + args_restantes
            extraer_silabo.run()
        elif comando == "im":
            from tools import ingestar_material

            sys.argv = [sys.argv[0]] + args_restantes
            ingestar_material.run()
        elif comando == "up":
            from tools import actualizar_plugins

            sys.argv = [sys.argv[0]] + args_restantes
            actualizar_plugins.run()
        elif comando == "quiz":
            import questionary
            from rich.console import Console

            from modules.core.services import motor_evaluacion

            console = Console()

            console.print(
                "\n[bold cyan]🧠 [Motor de Recuerdo Activo - Quiz Académico][/bold cyan]\n"
            )
            preguntas = motor_evaluacion.generar_quiz()

            puntuacion = 0
            total = len(preguntas)

            for idx, p in enumerate(preguntas, 1):
                console.print(
                    f"[bold yellow]Pregunta {idx}/{total}:[/bold yellow] {p.get('enunciado')}"
                )
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
        elif comando == "stats":
            from rich.console import Console
            from rich.panel import Panel
            from rich.progress import BarColumn, Progress, TextColumn
            from rich.table import Table

            from modules.core.services import telemetria

            console = Console()
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
                progress.add_task(
                    "[cyan]Avance General", total=max(total, 1), completed=completados
                )

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
        elif comando == "dev":
            from rich.console import Console

            console = Console()
            try:
                from modules.agents.orquestador_crew import crew

                console.print("[bold green]Iniciando entorno de desarrollo con CrewAI...[/]")
                crew.kickoff()
            except ImportError:
                console.print("[bold red]Faltan dependencias de desarrollo.[/]")
                console.print(
                    "Para usar los agentes, instala la CLI con: [yellow]pip install -e .[dev][/]"
                )
                sys.exit(1)
        elif comando in ["help", "--help", "-h"]:
            mostrar_ayuda()
        else:
            print(f"❌ Comando desconocido: '{comando}'\n")
            mostrar_ayuda()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Proceso cancelado por el usuario.\033[0m")
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"\n\033[1;31m❌ [Error] Archivo no encontrado: {e}\033[0m")
        print(
            "\033[1;33m💡 [Sugerencia] Revisa el archivo .env, la ruta de la bóveda o los archivos de configuración requeridos.\033[0m"
        )
        sys.exit(1)
    except ConnectionError as e:
        print(f"\n\033[1;31m❌ [Error] Error de conexión: {e}\033[0m")
        print(
            "\033[1;33m💡 [Sugerencia] Verifica tu conexión a internet o el estado del servicio de red.\033[0m"
        )
        sys.exit(1)
    except Exception as e:
        print(f"\n\033[1;31m❌ [Error Inesperado] {e}\033[0m")
        print(
            "\033[1;33m💡 [Sugerencia] Revisa el archivo .env o la configuración inicial del sistema.\033[0m"
        )
        sys.exit(1)


def mostrar_ayuda():
    """Imprime un panel de ayuda estilizado con las opciones disponibles."""
    print("=" * 65)
    print(" [EDU] MODULAR LEARNING CLI (ml) - PANEL DE AYUDA")
    print("=" * 65)
    print(" Comandos disponibles:")
    print("   ml init    -> Inicia la sesión de tutoría interactiva personalizada.")
    print("   ml es      -> Extraer cronogramas de sílabos (archivos o carpetas).")
    print("   ml im      -> Ingestar material de estudio multimodal hacia Obsidian.")
    print("   ml up      -> Actualiza el contexto técnico de proyectos de código en plugins.")
    print("   ml quiz    -> Motor de Recuerdo Activo (Quiz interactivo de temas completados).")
    print("   ml stats   -> Muestra el Dashboard visual de telemetría y progreso académico.")
    print("   ml dev     -> Inicia el entorno de desarrollo y auditoría con agentes (CrewAI).")
    print("   ml --help  -> Muestra este panel de ayuda.")
    print("=" * 65)


def main():
    """Punto de entrada principal compatible con pipx / setuptools."""
    app()


if __name__ == "__main__":
    main()
