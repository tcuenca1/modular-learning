"""Comando CLI: `ml im` - Ingesta multimodal de material de estudio hacia Obsidian."""

from __future__ import annotations

import questionary

from modular_learning import bootstrap
from modular_learning.apps.cli.ui import formateador
from modular_learning.apps.cli.ui.spinner import spinner


def _procesar_lote_materia(materia: str, ingesta_service) -> None:
    print(f"\n📚 Analizando asignatura: \033[1;92m{materia}\033[0m")
    escaneo = ingesta_service.escanear_materia(materia)

    if not escaneo["existe"]:
        print(f"⚠️ La carpeta '{escaneo['carpeta']}' no existe en disco. Omitiendo...")
        return

    pendientes = escaneo["pendientes"]
    print(
        f"🚀 Archivos totales: {escaneo['total']} | Omitidos: {escaneo['omitidos']} | Nuevos a procesar: {len(pendientes)}"
    )

    if not pendientes:
        print(f"✨ Todos los archivos de '{materia}' ya han sido procesados previamente.")
        return

    for idx, item in enumerate(pendientes, 1):
        print("\n" + "-" * 60)
        print(f"[{idx}/{len(pendientes)}] Ingestando: {item['nombre']} ({item['tipo']})")
        print("-" * 60)

        try:
            with spinner(f"Extrayendo y anonimizando conocimiento para '{item['nombre']}'..."):
                res = ingesta_service.ingestar_archivo(
                    ruta_archivo=item["ruta"],
                    nombre_original=item["nombre"],
                    materia=materia,
                    tipo=item["tipo"],
                )

            formateador.imprimir_markdown_bonito(res.get("contenido_md", ""))

            alineacion = res.get("alineacion", {})
            clase_asig = alineacion.get("clase_asignada", "X")
            afinidad = alineacion.get("peso_afinidad", 0)
            print(f"✅ [✓] Asignado a Clase {clase_asig} (Afinidad: {afinidad}%)")
            print(f"📄 Guardado en: {res['ruta_salida']}")
        except Exception as e:
            print(f"❌ Error al procesar '{item['nombre']}': {e}")


def run(container: bootstrap.Container | None = None) -> None:
    """Punto de entrada interactivo para `ml im`."""
    cont = container or bootstrap.get_container()
    materias_service = cont.materias_service
    ingesta_service = cont.ingesta_service

    materias = materias_service.listar_materias()
    opciones_menu = (
        ["✨ Actualizar todas las materias"] + materias + ["[ + ] Añadir nueva asignatura..."]
    )

    print("\n📚 Selecciona la asignatura o modo de ingesta:")
    try:
        seleccion = questionary.select(
            "Selecciona una opción:",
            choices=opciones_menu,
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
        print("\nOperación cancelada.")
        return

    if "✨ Actualizar todas las materias" in seleccion:
        print("\n🚀 Iniciando actualización global de todas las asignaturas...")
        for mat in materias:
            _procesar_lote_materia(mat, ingesta_service)
        print("\n✨ ¡Actualización global finalizada!")
    elif "[ + ]" in seleccion:
        try:
            nueva_mat = input("\n✍️ Ingresa el nombre de la nueva asignatura: ").strip()
            while not nueva_mat:
                nueva_mat = input("✍️ Ingresa el nombre de la nueva asignatura: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")
            return

        materias_service.agregar_materia(nueva_mat)
        _procesar_lote_materia(nueva_mat, ingesta_service)
    else:
        _procesar_lote_materia(seleccion, ingesta_service)


if __name__ == "__main__":
    run()
