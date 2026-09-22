import os
import json
import re
from typing import List, Dict, Any
from dotenv import load_dotenv

from modulos import ai_gemini, gestor_archivos, interaccion


def extraer_json_de_texto(texto: str) -> Dict[str, Any]:
    """Extrae y parsea un objeto JSON de una respuesta de texto de la IA."""
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", texto)
    if match:
        json_str = match.group(1)
    else:
        json_str = texto.strip()
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        match_braces = re.search(r"\{[\s\S]*\}", texto)
        if match_braces:
            try:
                return json.loads(match_braces.group(0))
            except Exception:
                pass
        raise RuntimeError(f"No se pudo parsear el roadmap JSON devuelto por Gemini.\nRespuesta recibida:\n{texto}")


def main() -> None:
    # 1. Cargar variables de entorno
    load_dotenv()
    ruta_boveda = os.getenv("RUTA_OBSIDIAN", "obsidian_vault")

    try:
        # a. Pedir datos iniciales
        datos = interaccion.pedir_datos_inicio()
        materia = datos["materia"]
        tema_principal = datos["tema"]
        ruta_material = datos["material"]

        # b. Leer material de apoyo si existe
        contenido_material = ""
        if ruta_material:
            interaccion.mostrar_mensaje(f"Leyendo material de apoyo desde: {ruta_material}", "info")
            try:
                contenido_material = gestor_archivos.leer_material_estudio(ruta_material)
                interaccion.mostrar_mensaje("Material de apoyo leído con éxito.", "exito")
            except Exception as e:
                interaccion.mostrar_mensaje(f"Error al leer material: {e}. Continuando sin él.", "error")

        # c. Leer prompt 01_roadmap.txt y consultar a Gemini
        interaccion.mostrar_mensaje("Generando ruta de aprendizaje (Roadmap)...", "info")
        prompt_roadmap_base = gestor_archivos.leer_prompt("01_roadmap.txt")
        
        prompt_roadmap_completo = (
            f"{prompt_roadmap_base}\n\n"
            f"Materia: {materia}\n"
            f"Tema Principal: {tema_principal}\n"
        )
        if contenido_material:
            prompt_roadmap_completo += f"\nMaterial de estudio previo:\n{contenido_material[:4000]}...\n"

        respuesta_roadmap_raw = ai_gemini.consultar_gemini(prompt_roadmap_completo)
        data_roadmap = extraer_json_de_texto(respuesta_roadmap_raw)

        subtemas = data_roadmap.get("subtemas", [])
        if not subtemas:
            raise ValueError("El JSON generado por la IA no contiene la lista de 'subtemas'.")

        interaccion.mostrar_mensaje(f"Roadmap generado con {len(subtemas)} subtemas:", "exito")
        for idx, sub in enumerate(subtemas, 1):
            print(f"   {idx}. {sub}")

        # Historial de sesión para el chat y resumen final
        historial_sesion: List[Dict[str, Any]] = []

        # d. y e. Bucle de explicación por cada subtema
        prompt_explicacion_base = gestor_archivos.leer_prompt("02_explicacion.txt")

        for idx, subtema in enumerate(subtemas, 1):
            print("\n" + "=" * 65)
            interaccion.mostrar_mensaje(f"Subtema {idx}/{len(subtemas)}: {subtema}", "info")
            print("=" * 65)

            prompt_subtema = (
                f"{prompt_explicacion_base}\n\n"
                f"Materia: {materia}\n"
                f"Tema Principal: {tema_principal}\n"
                f"Subtema actual: {subtema}\n"
            )
            if contenido_material:
                prompt_subtema += f"\nReferencia del material de estudio:\n{contenido_material[:3000]}...\n"

            interaccion.mostrar_mensaje("Explicando subtema...", "info")
            explicacion = ai_gemini.consultar_gemini(prompt_subtema)
            interaccion.mostrar_mensaje(explicacion, "ia")

            # Registrar en historial
            historial_sesion.append({"role": "user", "parts": [prompt_subtema]})
            historial_sesion.append({"role": "model", "parts": [explicacion]})

            # f. Pausa de estudio e interactividad de dudas
            while True:
                duda_o_confirmacion = interaccion.pausa_estudio()
                
                # Si dio ENTER o dijo sí/continuar
                if not duda_o_confirmacion or duda_o_confirmacion.lower() in ['s', 'si', 'sí', 'ok', 'continuar']:
                    interaccion.mostrar_mensaje("Avanzando al siguiente tema...", "exito")
                    break
                else:
                    # El usuario ingresó una duda/pregunta
                    interaccion.mostrar_mensaje("Consultando tu duda con el tutor...", "info")
                    prompt_duda = f"Tengo la siguiente pregunta sobre el subtema '{subtema}': {duda_o_confirmacion}. Por favor respóndela y aclárala didácticamente."
                    
                    respuesta_duda = ai_gemini.consultar_gemini(prompt_duda, contexto_previo=historial_sesion)
                    interaccion.mostrar_mensaje(respuesta_duda, "ia")

                    historial_sesion.append({"role": "user", "parts": [prompt_duda]})
                    historial_sesion.append({"role": "model", "parts": [respuesta_duda]})

        # g. Fin del bucle: leer '03_resumen.txt' y generar resumen de la sesión
        interaccion.mostrar_mensaje("Generando resumen final de la sesión de estudio...", "info")
        prompt_resumen_base = gestor_archivos.leer_prompt("03_resumen.txt")
        
        prompt_resumen_completo = (
            f"{prompt_resumen_base}\n\n"
            f"Materia: {materia}\n"
            f"Tema Principal: {tema_principal}\n"
            f"Subtemas estudiados: {', '.join(subtemas)}\n\n"
            "Genera el resumen definitivo integrando todo lo conversado en la clase."
        )

        resumen_markdown = ai_gemini.consultar_gemini(prompt_resumen_completo, contexto_previo=historial_sesion)

        # h. Guardar resumen en Obsidian
        interaccion.mostrar_mensaje(f"Guardando resumen en la bóveda de Obsidian ({ruta_boveda})...", "info")
        exito = gestor_archivos.guardar_resumen_obsidian(materia, tema_principal, resumen_markdown, ruta_boveda)

        if exito:
            interaccion.mostrar_mensaje("¡Resumen guardado exitosamente en tu bóveda de Obsidian!", "exito")
        else:
            interaccion.mostrar_mensaje("Hubo un problema al guardar el resumen en Obsidian.", "error")

        print("\n" + "=" * 65)
        print(" 🎉 ¡Tutoría finalizada con éxito! Buen trabajo.")
        print("=" * 65 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️ Sesión interrumpida por el usuario. ¡Hasta pronto!")
    except Exception as e:
        interaccion.mostrar_mensaje(f"Ha ocurrido un error crítico en el sistema: {e}", "error")


if __name__ == "__main__":
    main()
