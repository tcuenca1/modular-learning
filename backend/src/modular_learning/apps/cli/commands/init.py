"""Comando CLI: `ml init` - Sesión interactiva de tutoría personalizada."""

from __future__ import annotations

import sys
import uuid

from modular_learning import bootstrap
from modular_learning.apps.cli.ui import interaccion
from modular_learning.apps.cli.ui.spinner import spinner


def run(container: bootstrap.Container | None = None) -> None:
    """Ejecuta el flujo interactivo de tutoría como adaptador delgado."""
    cont = container or bootstrap.get_container()
    tutoria_service = cont.tutoria_service

    try:
        # 1. Recopilar datos interactivos del estudiante
        datos = interaccion.pedir_datos_inicio(cont.materias_service)
        materia = datos["materia"]
        tema = datos["tema"]
        nivel_profundidad = datos["nivel_profundidad"]
        clase_id = datos.get("clase_id")

        sesion_id = uuid.uuid4().hex

        # 2. Iniciar sesión y roadmap con el servicio
        with spinner("Generando ruta de aprendizaje personalizada con IA..."):
            sesion = tutoria_service.iniciar_sesion(
                sesion_id=sesion_id,
                materia=materia,
                tema=tema,
                nivel_profundidad=nivel_profundidad,
                clase_id=clase_id,
            )

        print("\n" + "=" * 65)
        print(f" 🗺️ ROADMAP GENERADO: {len(sesion.pasos)} Pasos para dominar '{tema}'")
        print("=" * 65)
        for idx, p in enumerate(sesion.pasos, 1):
            print(f"  {idx}. \033[1;96m{p.get('titulo')}\033[0m: {p.get('descripcion')}")
        print("=" * 65 + "\n")

        # 3. Recorrer cada paso del roadmap
        for i, paso in enumerate(sesion.pasos):
            titulo_paso = paso.get("titulo", f"Paso {i + 1}")
            print(f"\n📖 [Paso {i + 1}/{len(sesion.pasos)}]: \033[1;94m{titulo_paso}\033[0m")
            print("-" * 65)

            with spinner(f"El tutor está elaborando la explicación para '{titulo_paso}'..."):
                explicacion = tutoria_service.explicar_paso(sesion, i)

            interaccion.mostrar_mensaje(explicacion, tipo="ia")

            # Ciclo de resolución de dudas
            while True:
                duda = interaccion.pausa_estudio()
                if not duda:
                    break
                with spinner("El tutor está resolviendo tu duda..."):
                    respuesta_duda = tutoria_service.responder_duda(sesion, i, duda)
                interaccion.mostrar_mensaje(respuesta_duda, tipo="ia")

        # 4. Finalización y guardado en Obsidian
        print("\n" + "=" * 65)
        print(" 📝 Generando guía de repaso activo y consolidando notas...")
        print("=" * 65)

        with spinner("Sintetizando guía final y registrando clase completada..."):
            resultado = tutoria_service.finalizar_sesion(sesion)

        if resultado.get("guardado_obsidian"):
            interaccion.mostrar_mensaje(
                f"¡Guía de estudio guardada exitosamente en Obsidian bajo la materia '{materia}'!",
                tipo="exito",
            )
        else:
            interaccion.mostrar_mensaje(
                "La guía se generó, pero hubo una advertencia al persistir en la bóveda.",
                tipo="info",
            )

        print("\n" + "=" * 65)
        print(" 🎉 ¡Sesión de estudio completada con éxito!")
        print("=" * 65 + "\n")

    except KeyboardInterrupt:
        print("\n\n\033[1;33m⚠️ Sesión cancelada por el usuario. ¡Hasta pronto!\033[0m")
        sys.exit(0)
    except Exception as e:
        interaccion.mostrar_mensaje(f"Error en la sesión de tutoría: {e}", tipo="error")
        sys.exit(1)


def main() -> None:
    run()


if __name__ == "__main__":
    main()
