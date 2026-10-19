import json
import os
import sys
import warnings
from typing import Any

from dotenv import load_dotenv

from modules.core.services import gestor_archivos, gestor_llm, servicio_config
from modules.plugins.services import gestor_plugins
from modules.ui import interaccion

# Suprimir advertencias de deprecación
warnings.filterwarnings("ignore", category=FutureWarning)


def main() -> None:
    load_dotenv()
    ruta_boveda = servicio_config.ruta_boveda()
    llm = gestor_llm.obtener_llm()

    try:
        # 1. Recopilar datos de inicio (Asignatura con questionary y Tema)
        datos = interaccion.pedir_datos_inicio()
        materia = datos["materia"]
        tema = datos["tema"]
        nivel_profundidad = datos["nivel_profundidad"]

        # Recuperar datos enriquecidos del Segundo Cerebro (Alineador Curricular)
        detalle_clase = gestor_archivos.obtener_detalle_clase(materia, tema)
        materiales_asociados = detalle_clase.get("materiales_asociados", [])
        subtemas_adicionales = detalle_clase.get("subtemas_adicionales", [])

        if materiales_asociados or subtemas_adicionales:
            print("\n" + "🧠" + "=" * 60)
            if materiales_asociados:
                print(
                    f" \033[1;95m[🧠 Segundo Cerebro Activo]\033[0m Contexto inyectado desde: {', '.join(materiales_asociados)}"
                )
            if subtemas_adicionales:
                print(
                    f" \033[1;96m[+]\033[0m Subtemas detectados: {', '.join(subtemas_adicionales)}"
                )
            print("=" * 62 + "\n")

        # 2. Cargar prompt 01_roadmap_aprendizaje.md y generar ruta de sesión estructurada (JSON)
        interaccion.mostrar_mensaje(f"Generando Roadmap JSON para el tema: '{tema}'...", "info")
        prompt_roadmap_template = gestor_archivos.leer_prompt("01_roadmap_aprendizaje.md")

        prompt_roadmap = prompt_roadmap_template.format(
            tema=tema,
            objetivo=f"Estudiar y dominar a fondo el tema dentro de la asignatura {materia}",
        )

        # Usar Structured Outputs (JSON) nativo a través del puerto LLM
        data_roadmap = llm.generar_json_estructurado(prompt_roadmap)

        if isinstance(data_roadmap, dict):
            data_roadmap_dict = {str(k).strip(): v for k, v in data_roadmap.items()}
            pasos_raw = data_roadmap_dict.get("pasos", [])
            if not pasos_raw:
                for k, v in data_roadmap_dict.items():
                    if "paso" in k.lower():
                        pasos_raw = v
                        break
        elif isinstance(data_roadmap, list):
            pasos_raw = data_roadmap
        else:
            pasos_raw = []

        pasos_sesion = []
        if isinstance(pasos_raw, list):
            for p in pasos_raw:
                if isinstance(p, dict):
                    p_limpio = {str(k).strip().lower(): v for k, v in p.items()}
                    titulo = (
                        p_limpio.get("titulo")
                        or p_limpio.get("title")
                        or p_limpio.get("nombre")
                        or p_limpio.get("paso")
                        or "Paso"
                    )
                    descripcion = (
                        p_limpio.get("descripcion")
                        or p_limpio.get("description")
                        or p_limpio.get("detalle")
                        or p_limpio.get("contenido")
                        or ""
                    )
                    pasos_sesion.append({"titulo": str(titulo), "descripcion": str(descripcion)})
                elif isinstance(p, str):
                    pasos_sesion.append({"titulo": p, "descripcion": ""})

        if not pasos_sesion:
            raise ValueError("El JSON del roadmap no contiene una lista de 'pasos' válida.")

        print("\n" + "=" * 65)
        print(" 🗺️ RUTA DE SESIÓN ESTABLECIDA (JSON STRUCTURED OUTPUT):")
        print("=" * 65)
        for idx, p in enumerate(pasos_sesion, 1):
            print(f"  {idx}. {p.get('titulo', 'Paso')}: {p.get('descripcion', '')}")
        print("=" * 65)

        # Historial de sesión para mantener contexto
        historial_sesion: list[dict[str, Any]] = [
            {"role": "user", "parts": [prompt_roadmap]},
            {"role": "model", "parts": [json.dumps(data_roadmap, ensure_ascii=False)]},
        ]

        # 3. Bucle interactivo por cada paso usando prompt 02_explicacion_tema.md
        prompt_explicacion_template = gestor_archivos.leer_prompt("02_explicacion_tema.md")

        for idx, paso_obj in enumerate(pasos_sesion, 1):
            titulo_paso = paso_obj.get("titulo", f"Paso {idx}")
            desc_paso = paso_obj.get("descripcion", "")

            print("\n" + "=" * 65)
            interaccion.mostrar_mensaje(f"Paso {idx}/{len(pasos_sesion)}: {titulo_paso}", "info")
            print("=" * 65)

            prompt_explicacion = prompt_explicacion_template.format(
                tema=f"{titulo_paso}: {desc_paso}",
                nivel_profundidad=nivel_profundidad,
                contexto_roadmap=f"Asignatura: {materia}. Tema principal: {tema}. Paso actual: {titulo_paso}",
            )

            # Inyección y Directiva Estricta de Prompt (Segundo Cerebro)
            if materiales_asociados or subtemas_adicionales:
                lista_materiales_str = (
                    ", ".join(materiales_asociados)
                    if materiales_asociados
                    else "Ninguno específico"
                )
                lista_subtemas_str = (
                    ", ".join(subtemas_adicionales)
                    if subtemas_adicionales
                    else "Ninguno específico"
                )

                bloque_segundo_cerebro = f"""
CONTEXTO DEL SEGUNDO CEREBRO (Material local del estudiante):
- Archivos de referencia: {lista_materiales_str}
- Subtemas clave a integrar: {lista_subtemas_str}

DIRECTIVA OBLIGATORIA: En tu respuesta, DEBES hacer referencia explícitamente a que estás utilizando estos subtemas extraídos de sus propios apuntes. Hazlo de forma natural pero evidente (ej. "Basándome en tu archivo X, profundicemos en Y..."). Integra estos subtemas en tu explicación del tema principal.
"""
                prompt_explicacion += "\n" + bloque_segundo_cerebro

            # Inyectar plugin práctico si existe (Arquitectura Hexagonal / Puertos y Adaptadores)
            plugin = gestor_plugins.obtener_plugin(materia)
            if plugin:
                instrucciones_plugin = plugin.obtener_instrucciones_ia()
                ejercicio_base = plugin.generar_ejercicio_base(titulo_paso)
                prompt_explicacion += f"\n\n{instrucciones_plugin}\n\n{ejercicio_base}"

            interaccion.mostrar_mensaje("El tutor está explicando el paso...", "info")
            print("\n\033[1;36m🤖 [Tutor IA - Streaming en tiempo real]\033[0m")
            explicacion_chunks = []
            for chunk in llm.generar_respuesta_stream(
                prompt_explicacion, contexto_previo=historial_sesion
            ):
                sys.stdout.write(chunk)
                sys.stdout.flush()
                explicacion_chunks.append(chunk)
            print("\n")
            explicacion = "".join(explicacion_chunks)

            historial_sesion.append({"role": "user", "parts": [prompt_explicacion]})
            historial_sesion.append({"role": "model", "parts": [explicacion]})

            # Pausa interactiva para dudas
            while True:
                duda = interaccion.pausa_estudio()
                if not duda or duda.lower() in ["s", "si", "sí", "ok", "continuar"]:
                    interaccion.mostrar_mensaje("¡Entendido! Pasando al siguiente paso.", "exito")
                    break
                else:
                    interaccion.mostrar_mensaje("Consultando tu duda con el tutor...", "info")
                    prompt_duda = f"Tengo esta duda sobre el paso '{titulo_paso}': {duda}. Respóndela técnicamente y de forma clara."

                    respuesta_duda = llm.generar_texto(
                        prompt_duda, contexto_previo=historial_sesion
                    )
                    interaccion.mostrar_mensaje(respuesta_duda, "ia")

                    historial_sesion.append({"role": "user", "parts": [prompt_duda]})
                    historial_sesion.append({"role": "model", "parts": [respuesta_duda]})

        # 4. Generar Guía de Estudio y Autoevaluación con prompt 03_resumen_evaluacion.md
        interaccion.mostrar_mensaje(
            "Generando Guía de Estudio y Autoevaluación definitiva...", "info"
        )
        prompt_resumen_template = gestor_archivos.leer_prompt("03_resumen_evaluacion.md")

        nombres_pasos = [p.get("titulo", "") for p in pasos_sesion]
        prompt_resumen = prompt_resumen_template.format(
            materia=materia,
            contenido_apuntes=f"Tema de estudio: {tema}\nPasos cubiertos:\n{', '.join(nombres_pasos)}",
        )

        guia_estudio_markdown = llm.generar_texto(prompt_resumen, contexto_previo=historial_sesion)

        interaccion.mostrar_mensaje(
            f"Guardando guía de repaso en Obsidian ({ruta_boveda})...", "info"
        )
        exito = gestor_archivos.guardar_resumen_obsidian(
            materia, tema, guia_estudio_markdown, ruta_boveda
        )

        if exito:
            interaccion.mostrar_mensaje(
                f"¡Guía de estudio guardada exitosamente en tu bóveda de Obsidian bajo la asignatura '{materia}'!",
                "exito",
            )
            # Actualizar estado de la clase en el cronograma JSON a completado
            gestor_archivos.marcar_clase_completada(materia, tema)
        else:
            interaccion.mostrar_mensaje("No se pudo guardar el archivo en Obsidian.", "error")

        print("\n" + "=" * 65)
        print(" 🎉 ¡Sesión de estudio y autoevaluación completada con éxito!")
        print("=" * 65 + "\n")

    except KeyboardInterrupt:
        print("\n\n\033[1;33m⚠️ Sesión cancelada por el usuario. ¡Hasta pronto!\033[0m")
        sys.exit(0)
    except FileNotFoundError as e:
        interaccion.mostrar_mensaje(f"Archivo no encontrado: {e}", "error")
        print(
            "\033[1;33m💡 [Sugerencia] Revisa el archivo .env, la ruta de la bóveda de Obsidian o los archivos de configuración requeridos.\033[0m"
        )
        sys.exit(1)
    except ConnectionError as e:
        interaccion.mostrar_mensaje(f"Error de conexión: {e}", "error")
        print(
            "\033[1;33m💡 [Sugerencia] Verifica tu conexión a internet o el estado de la API de Gemini.\033[0m"
        )
        sys.exit(1)
    except Exception as e:
        interaccion.mostrar_mensaje(f"Ocurrió un error en el sistema: {e}", "error")
        print(
            "\033[1;33m💡 [Sugerencia] Revisa el archivo .env y asegúrate de que las dependencias y la configuración sean correctas.\033[0m"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
