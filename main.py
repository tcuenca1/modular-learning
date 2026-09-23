import os
import json
import warnings
from typing import List, Dict, Any
from dotenv import load_dotenv

from modules import ai_gemini, gestor_archivos, interaccion

# Suprimir FutureWarning de google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)


def main() -> None:
    load_dotenv()
    ruta_boveda = os.getenv("RUTA_OBSIDIAN", "obsidian_vault")

    try:
        # 1. Recopilar datos de inicio (Asignatura con questionary y Tema)
        datos = interaccion.pedir_datos_inicio()
        materia = datos["materia"]
        tema = datos["tema"]
        nivel_profundidad = datos["nivel_profundidad"]

        # 2. Cargar prompt 01_roadmap_aprendizaje.md y generar ruta de sesión estructurada (JSON)
        interaccion.mostrar_mensaje(f"Generando Roadmap JSON para el tema: '{tema}'...", "info")
        prompt_roadmap_template = gestor_archivos.leer_prompt("01_roadmap_aprendizaje.md")
        
        prompt_roadmap = (
            prompt_roadmap_template
            .replace("[INSERTA AQUÍ EL TEMA]", tema)
            .replace("[EJ. ENTENDER LAS BASES / DOMINAR EL FUNCIONAMIENTO TÉCNICO]", f"Estudiar y dominar a fondo el tema dentro de la asignatura {materia}")
        )

        # Usar Structured Outputs (JSON) nativo de Gemini
        data_roadmap = ai_gemini.consultar_gemini_json(prompt_roadmap)
        pasos_sesion = data_roadmap.get("pasos", [])

        if not pasos_sesion:
            raise ValueError("El JSON del roadmap no contiene la clave 'pasos' esperada.")

        print("\n" + "=" * 65)
        print(" 🗺️ RUTA DE SESIÓN ESTABLECIDA (JSON STRUCTURED OUTPUT):")
        print("=" * 65)
        for idx, p in enumerate(pasos_sesion, 1):
            print(f"  {idx}. {p.get('titulo', 'Paso')}: {p.get('descripcion', '')}")
        print("=" * 65)

        # Historial de sesión para mantener contexto
        historial_sesion: List[Dict[str, Any]] = [
            {"role": "user", "parts": [prompt_roadmap]},
            {"role": "model", "parts": [json.dumps(data_roadmap, ensure_ascii=False)]}
        ]

        # 3. Bucle interactivo por cada paso usando prompt 02_explicacion_tema.md
        prompt_explicacion_template = gestor_archivos.leer_prompt("02_explicacion_tema.md")

        for idx, paso_obj in enumerate(pasos_sesion, 1):
            titulo_paso = paso_obj.get("titulo", f"Paso {idx}")
            desc_paso = paso_obj.get("descripcion", "")
            
            print("\n" + "=" * 65)
            interaccion.mostrar_mensaje(f"Paso {idx}/{len(pasos_sesion)}: {titulo_paso}", "info")
            print("=" * 65)

            prompt_explicacion = (
                prompt_explicacion_template
                .replace("[INSERTA EL TEMA AQUÍ]", f"{titulo_paso}: {desc_paso}")
                .replace("[ELIGE UNO: BÁSICO (visión general) / INTERMEDIO (conceptos y funcionamiento) / AVANZADO (a profundidad técnica)]", nivel_profundidad)
                .replace("[INSERTA TU ROADMAP, EN QUÉ FASE ESTÁS O BORRA ESTA LÍNEA]", f"Asignatura: {materia}. Tema principal: {tema}. Paso actual: {titulo_paso}")
            )

            interaccion.mostrar_mensaje("El tutor está explicando el paso...", "info")
            explicacion = ai_gemini.consultar_gemini(prompt_explicacion, contexto_previo=historial_sesion)
            interaccion.mostrar_mensaje(explicacion, "ia")

            historial_sesion.append({"role": "user", "parts": [prompt_explicacion]})
            historial_sesion.append({"role": "model", "parts": [explicacion]})

            # Pausa interactiva para dudas
            while True:
                duda = interaccion.pausa_estudio()
                if not duda or duda.lower() in ['s', 'si', 'sí', 'ok', 'continuar']:
                    interaccion.mostrar_mensaje("¡Entendido! Pasando al siguiente paso.", "exito")
                    break
                else:
                    interaccion.mostrar_mensaje("Consultando tu duda con el tutor...", "info")
                    prompt_duda = f"Tengo esta duda sobre el paso '{titulo_paso}': {duda}. Respóndela técnicamente y de forma clara."
                    
                    respuesta_duda = ai_gemini.consultar_gemini(prompt_duda, contexto_previo=historial_sesion)
                    interaccion.mostrar_mensaje(respuesta_duda, "ia")

                    historial_sesion.append({"role": "user", "parts": [prompt_duda]})
                    historial_sesion.append({"role": "model", "parts": [respuesta_duda]})

        # 4. Generar Guía de Estudio y Autoevaluación con prompt 03_resumen_evaluacion.md
        interaccion.mostrar_mensaje("Generando Guía de Estudio y Autoevaluación definitiva...", "info")
        prompt_resumen_template = gestor_archivos.leer_prompt("03_resumen_evaluacion.md")
        
        nombres_pasos = [p.get("titulo", "") for p in pasos_sesion]
        prompt_resumen = (
            prompt_resumen_template
            .replace("[INSERTA LA MATERIA]", materia)
            .replace("[INSERTA AQUÍ EL CONTENIDO DE TUS ARCHIVOS .MD]", f"Tema de estudio: {tema}\nPasos cubiertos:\n{', '.join(nombres_pasos)}")
        )

        guia_estudio_markdown = ai_gemini.consultar_gemini(prompt_resumen, contexto_previo=historial_sesion)

        interaccion.mostrar_mensaje(f"Guardando guía de repaso en Obsidian ({ruta_boveda})...", "info")
        exito = gestor_archivos.guardar_resumen_obsidian(materia, tema, guia_estudio_markdown, ruta_boveda)

        if exito:
            interaccion.mostrar_mensaje(f"¡Guía de estudio guardada exitosamente en tu bóveda de Obsidian bajo la asignatura '{materia}'!", "exito")
        else:
            interaccion.mostrar_mensaje("No se pudo guardar el archivo en Obsidian.", "error")

        print("\n" + "=" * 65)
        print(" 🎉 ¡Sesión de estudio y autoevaluación completada con éxito!")
        print("=" * 65 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️ Sesión cancelada por el usuario. ¡Hasta pronto!")
    except Exception as e:
        interaccion.mostrar_mensaje(f"Ocurrió un error en el sistema: {e}", "error")


if __name__ == "__main__":
    main()
