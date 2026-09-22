import os
import re
import warnings
from typing import List, Dict, Any
from dotenv import load_dotenv

from modulos import ai_gemini, gestor_archivos, interaccion

# Suprimir FutureWarning de google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)


def extraer_fases_roadmap(roadmap_texto: str) -> List[str]:
    """Extrae las fases o temas principales del roadmap Markdown generado por Gemini."""
    # Buscar coincidencias de encabezados FASE
    fases = re.findall(r"###\s+FASE\s+\d+:\s*(.+)", roadmap_texto, re.IGNORECASE)
    if not fases:
        # Fallback buscando encabezados h3
        fases = re.findall(r"###\s+(.+)", roadmap_texto)
    if not fases:
        fases = ["Fundamentos Iniciales", "Desarrollo Core y Práctica", "Avanzado y Buenas Prácticas"]
    return [f.strip() for f in fases]


def main() -> None:
    load_dotenv()
    ruta_boveda = os.getenv("RUTA_OBSIDIAN", "obsidian_vault")

    try:
        # 1. Recopilar datos iniciales según los prompts
        datos = interaccion.pedir_datos_inicio()
        materia = datos["materia"]
        nivel_actual = datos["nivel_actual"]
        tiempo_disponible = datos["tiempo_disponible"]
        objetivo_final = datos["objetivo_final"]
        nivel_profundidad = datos["nivel_profundidad"]
        ruta_material = datos["material"]

        # 2. Leer material de apoyo si existe
        contenido_material = ""
        if ruta_material:
            interaccion.mostrar_mensaje(f"Leyendo material de apoyo: {ruta_material}", "info")
            try:
                contenido_material = gestor_archivos.leer_material_estudio(ruta_material)
                interaccion.mostrar_mensaje("Material de apoyo cargado correctamente.", "exito")
            except Exception as e:
                interaccion.mostrar_mensaje(f"Error al leer material ({e}). Continuando sin él.", "error")

        # 3. Cargar prompt de Roadmap y rellenar variables
        interaccion.mostrar_mensaje("Generando Roadmap de Aprendizaje personalizado...", "info")
        prompt_roadmap_template = gestor_archivos.leer_prompt("01_roadmap_aprendizaje.md")
        
        prompt_roadmap = (
            prompt_roadmap_template
            .replace("[INSERTA EL TEMA]", materia)
            .replace("[EJ. PRINCIPIANTE ABSOLUTO / TENGO NOCIONES BASICAS DE...]", nivel_actual)
            .replace("[EJ. 10 HORAS A LA SEMANA DURANTE 3 MESES]", tiempo_disponible)
            .replace("[EJ. CONSEGUIR EMPLEO / CREAR UN SAAS / APROBAR EXAMEN]", objetivo_final)
        )
        if contenido_material:
            prompt_roadmap += f"\n\nMaterial de referencia:\n{contenido_material[:4000]}"

        respuesta_roadmap = ai_gemini.consultar_gemini(prompt_roadmap)
        
        print("\n" + "=" * 65)
        print(" 🗺️ ROADMAP DE APRENDIZAJE GENERADO:")
        print("=" * 65)
        print(respuesta_roadmap)
        print("=" * 65)

        # Extraer fases/subtemas para la tutoría interactiva
        subtemas = extraer_fases_roadmap(respuesta_roadmap)
        
        # Historial de sesión para mantener contexto
        historial_sesion: List[Dict[str, Any]] = [
            {"role": "user", "parts": [prompt_roadmap]},
            {"role": "model", "parts": [respuesta_roadmap]}
        ]

        # 4. Bucle interactivo por cada subtema/fase usando el prompt 02_explicacion_tema.md
        prompt_explicacion_template = gestor_archivos.leer_prompt("02_explicacion_tema.md")

        for idx, subtema in enumerate(subtemas, 1):
            print("\n" + "=" * 65)
            interaccion.mostrar_mensaje(f"Estudiando Fase {idx}/{len(subtemas)}: {subtema}", "info")
            print("=" * 65)

            prompt_explicacion = (
                prompt_explicacion_template
                .replace("[INSERTA EL TEMA AQUÍ]", subtema)
                .replace("[ELIGE UNO: BÁSICO (visión general) / INTERMEDIO (conceptos y funcionamiento) / AVANZADO (a profundidad técnica)]", nivel_profundidad)
                .replace("[INSERTA TU ROADMAP, EN QUÉ FASE ESTÁS O BORRA ESTA LÍNEA]", f"Materia principal: {materia}. Fase actual: {subtema}")
            )
            if contenido_material:
                prompt_explicacion += f"\n\nContexto del material:\n{contenido_material[:3000]}"

            interaccion.mostrar_mensaje("Generando explicación del tutor...", "info")
            explicacion = ai_gemini.consultar_gemini(prompt_explicacion, contexto_previo=historial_sesion)
            interaccion.mostrar_mensaje(explicacion, "ia")

            historial_sesion.append({"role": "user", "parts": [prompt_explicacion]})
            historial_sesion.append({"role": "model", "parts": [explicacion]})

            # Pausa interactiva para dudas
            while True:
                duda = interaccion.pausa_estudio()
                if not duda or duda.lower() in ['s', 'si', 'sí', 'ok', 'continuar']:
                    interaccion.mostrar_mensaje("¡Excelente! Avanzando a la siguiente fase.", "exito")
                    break
                else:
                    interaccion.mostrar_mensaje("Consultando tu duda con el mentor técnico...", "info")
                    prompt_duda = f"Tengo esta duda sobre '{subtema}': {duda}. Por favor respóndela técnicamente y de forma didáctica."
                    
                    respuesta_duda = ai_gemini.consultar_gemini(prompt_duda, contexto_previo=historial_sesion)
                    interaccion.mostrar_mensaje(respuesta_duda, "ia")

                    historial_sesion.append({"role": "user", "parts": [prompt_duda]})
                    historial_sesion.append({"role": "model", "parts": [respuesta_duda]})

        # 5. Generar resumen final y guardar en Obsidian
        interaccion.mostrar_mensaje("Generando resumen final consolidado de la sesión...", "info")
        prompt_resumen = (
            f"Actúa como un asistente técnico experto.\n"
            f"Basado en toda la sesión de mentoría sobre '{materia}' y las fases estudiadas ({', '.join(subtemas)}), "
            f"genera un resumen técnico completo en Markdown listo para Obsidian, incluyendo conceptos clave, ejemplos y preguntas de repaso."
        )
        
        resumen_markdown = ai_gemini.consultar_gemini(prompt_resumen, contexto_previo=historial_sesion)

        interaccion.mostrar_mensaje(f"Guardando resumen en Obsidian ({ruta_boveda})...", "info")
        exito = gestor_archivos.guardar_resumen_obsidian(materia, f"Roadmap_{materia}", resumen_markdown, ruta_boveda)

        if exito:
            interaccion.mostrar_mensaje("¡Resumen guardado exitosamente en tu bóveda de Obsidian!", "exito")
        else:
            interaccion.mostrar_mensaje("No se pudo guardar el archivo en Obsidian.", "error")

        print("\n" + "=" * 65)
        print(" 🎉 ¡Sesión de aprendizaje completada con éxito!")
        print("=" * 65 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️ Sesión cancelada por el usuario. ¡Hasta pronto!")
    except Exception as e:
        interaccion.mostrar_mensaje(f"Ocurrió un error en el sistema: {e}", "error")


if __name__ == "__main__":
    main()
