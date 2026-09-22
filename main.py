import os
import re
import warnings
from typing import List, Dict, Any
from dotenv import load_dotenv

from modulos import ai_gemini, gestor_archivos, interaccion

# Suprimir FutureWarning de google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)


def extraer_pasos_roadmap(roadmap_texto: str) -> List[str]:
    """Extrae los pasos o temas de la ruta de sesión del roadmap Markdown generado por Gemini."""
    # Buscar encabezados como ### Paso 1: ..., ### Paso 2: ...
    pasos = re.findall(r"###\s+Paso\s+\d+:\s*(.+)", roadmap_texto, re.IGNORECASE)
    if not pasos:
        # Fallback buscando cualquier encabezado h3
        pasos = re.findall(r"###\s+(.+)", roadmap_texto)
    if not pasos:
        pasos = ["Fundamentos del Tema", "Desarrollo del Núcleo", "Aplicación Práctica y Cierre"]
    return [p.strip() for p in pasos]


def main() -> None:
    load_dotenv()
    ruta_boveda = os.getenv("RUTA_OBSIDIAN", "obsidian_vault")

    try:
        # 1. Recopilar datos de inicio
        datos = interaccion.pedir_datos_inicio()
        materia = datos["materia"]
        tipo_contenido = datos["tipo_contenido"]
        contenido_entrada = datos["contenido_entrada"]
        ruta_material = datos["ruta_material"]
        objetivo_hoy = datos["objetivo_hoy"]
        nivel_profundidad = datos["nivel_profundidad"]

        # 2. Obtener el contenido de estudio (archivo .md o texto directo)
        contenido_texto = contenido_entrada
        if ruta_material:
            interaccion.mostrar_mensaje(f"Leyendo material de apoyo: {ruta_material}", "info")
            try:
                contenido_texto = gestor_archivos.leer_material_estudio(ruta_material)
                interaccion.mostrar_mensaje("Material leído correctamente.", "exito")
            except Exception as e:
                interaccion.mostrar_mensaje(f"Error al leer material ({e}). Usando texto por defecto.", "error")

        if not contenido_texto:
            contenido_texto = f"Estudio general sobre {materia} enfocado en {objetivo_hoy}."

        # 3. Cargar prompt 01_roadmap_aprendizaje.md y generar ruta de sesión
        interaccion.mostrar_mensaje("Analizando contenido y generando Ruta de Sesión...", "info")
        prompt_roadmap_template = gestor_archivos.leer_prompt("01_roadmap_aprendizaje.md")
        
        prompt_roadmap = (
            prompt_roadmap_template
            .replace("[EJ. TEXTO DE LECTURA / INSTRUCCIONES DE TAREA]", tipo_contenido)
            .replace("[INSERTA AQUÍ EL TEXTO, APUNTES O ACTIVIDAD]", contenido_texto)
            .replace("[EJ. ENTENDER EL CONCEPTO / RESOLVER LA ACTIVIDAD]", objetivo_hoy)
        )

        respuesta_roadmap = ai_gemini.consultar_gemini(prompt_roadmap)
        
        print("\n" + "=" * 65)
        print(" 🗺️ RUTA DE SESIÓN ESTABLECIDA:")
        print("=" * 65)
        print(respuesta_roadmap)
        print("=" * 65)

        # Extraer pasos de la sesión
        pasos_sesion = extraer_pasos_roadmap(respuesta_roadmap)

        # Historial de sesión para mantener contexto
        historial_sesion: List[Dict[str, Any]] = [
            {"role": "user", "parts": [prompt_roadmap]},
            {"role": "model", "parts": [respuesta_roadmap]}
        ]

        # 4. Bucle interactivo por cada paso usando prompt 02_explicacion_tema.md
        prompt_explicacion_template = gestor_archivos.leer_prompt("02_explicacion_tema.md")

        for idx, paso in enumerate(pasos_sesion, 1):
            print("\n" + "=" * 65)
            interaccion.mostrar_mensaje(f"Paso {idx}/{len(pasos_sesion)}: {paso}", "info")
            print("=" * 65)

            prompt_explicacion = (
                prompt_explicacion_template
                .replace("[INSERTA EL TEMA AQUÍ]", paso)
                .replace("[ELIGE UNO: BÁSICO (visión general) / INTERMEDIO (conceptos y funcionamiento) / AVANZADO (a profundidad técnica)]", nivel_profundidad)
                .replace("[INSERTA TU ROADMAP, EN QUÉ FASE ESTÁS O BORRA ESTA LÍNEA]", f"Materia: {materia}. Paso actual de la sesión: {paso}")
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
                    prompt_duda = f"Tengo esta duda sobre el paso '{paso}': {duda}. Respóndela técnicamente y de forma clara."
                    
                    respuesta_duda = ai_gemini.consultar_gemini(prompt_duda, contexto_previo=historial_sesion)
                    interaccion.mostrar_mensaje(respuesta_duda, "ia")

                    historial_sesion.append({"role": "user", "parts": [prompt_duda]})
                    historial_sesion.append({"role": "model", "parts": [respuesta_duda]})

        # 5. Generar Guía de Estudio y Autoevaluación con prompt 03_resumen_evaluacion.md
        interaccion.mostrar_mensaje("Generando Guía de Estudio y Autoevaluación definitiva...", "info")
        prompt_resumen_template = gestor_archivos.leer_prompt("03_resumen_evaluacion.md")
        
        prompt_resumen = (
            prompt_resumen_template
            .replace("[INSERTA LA MATERIA]", materia)
            .replace("[INSERTA AQUÍ EL CONTENIDO DE TUS ARCHIVOS .MD]", f"Objetivo: {objetivo_hoy}\nContenido original:\n{contenido_texto}\nPasos cubiertos:\n{', '.join(pasos_sesion)}")
        )

        guia_estudio_markdown = ai_gemini.consultar_gemini(prompt_resumen, contexto_previo=historial_sesion)

        interaccion.mostrar_mensaje(f"Guardando guía de repaso en Obsidian ({ruta_boveda})...", "info")
        exito = gestor_archivos.guardar_resumen_obsidian(materia, f"Repaso_{materia}", guia_estudio_markdown, ruta_boveda)

        if exito:
            interaccion.mostrar_mensaje("¡Guía de estudio guardada exitosamente en tu bóveda de Obsidian!", "exito")
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
