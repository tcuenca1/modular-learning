import sys
import os
import time
import json
import warnings

# Forzar UTF-8 en stdout
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai
from halo import Halo


def ingestar_material(ruta_archivo: str) -> None:
    """
    Sube un archivo de material de estudio (PDF, diapositiva, DOCX) a Gemini (gemini-1.5-flash),
    extrae texto y describe imágenes semánticamente con Wikilinks y Frontmatter, manejando rate limits (429).
    """
    ruta_archivo = ruta_archivo.strip('"').strip("'")
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo no existe en la ruta: {ruta_archivo}")
        return

    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.dirname(ruta_script)
    load_dotenv(os.path.join(ruta_raiz, '.env'), override=True)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error crítico: No se encontró GEMINI_API_KEY en el archivo .env.")
        return

    genai.configure(api_key=api_key)
    # Usar gemini-1.5-flash para visión y análisis multimodal de imágenes en documentos
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    materia_input = input(f"📚 Ingresa el nombre de la asignatura para este material [{nombre_base}]: ").strip()
    if not materia_input:
        materia_input = nombre_base

    tipo_input = input("📄 Tipo de material (diapositiva / actividad / lectura) [diapositiva]: ").strip().lower()
    if not tipo_input:
        tipo_input = "diapositiva"

    prompt = (
        "Actúa como un extractor de conocimiento experto.\n"
        "Transcribe el contenido de estas diapositivas o documento de forma estructurada usando Markdown limpio.\n\n"
        "REGLA CRÍTICA PARA IMÁGENES: Si detectas diagramas, gráficos, topologías de red o capturas de código, "
        "NO los ignores. Crea un bloque blockquote (>) y describe detalladamente lo que muestra la imagen "
        "(ej. '> **Diagrama detectado:** Topología de red en estrella con un switch central conectado a 3 PCs...').\n\n"
        "REGLA PARA OBSIDIAN: Identifica los conceptos técnicos, nombres de protocolos o tecnologías clave y envuélvelos "
        "en corchetes dobles para crear Wikilinks (ej. [[Protocolo MQTT]], [[VLAN]]). Opcionalmente incluye al inicio un Wikilink a la asignatura principal: "
        f"[[{materia_input}]].\n\n"
        "REGLA DE FORMATO: Añade un YAML Frontmatter al inicio del documento con esta estructura exacta:\n"
        "---\n"
        f"materia: {materia_input}\n"
        f"tipo: {tipo_input}\n"
        f"fecha_procesamiento: {time.strftime('%Y-%m-%d')}\n"
        f"tags: [{materia_input.lower().replace(' ', '_')}, {tipo_input}, ingesta_ia]\n"
        "---\n"
    )

    archivo_gemini = None
    max_reintentos = 3
    intento = 0

    while intento < max_reintentos:
        spinner = Halo(text=f'Subiendo archivo a Gemini (Intento {intento+1}/{max_reintentos})...', spinner='dots')
        try:
            spinner.start()
            archivo_gemini = genai.upload_file(path=ruta_archivo)
            spinner.succeed("Archivo subido con éxito a la File API de Gemini.")
            break
        except Exception as e:
            spinner.fail(f"Fallo al subir el archivo: {e}")
            intento += 1
            if intento < max_reintentos:
                print("⏳ Esperando 10 segundos antes de reintentar...")
                time.sleep(10)
            else:
                print("❌ Se agotaron los reintentos de subida.")
                return

    if not archivo_gemini:
        return

    # Generar contenido con reintento ante Rate Limit (429)
    intento_gen = 0
    while intento_gen < max_reintentos:
        spinner_gen = Halo(text='Analizando documento, texto e imágenes con Gemini 1.5 Flash...', spinner='line')
        try:
            spinner_gen.start()
            respuesta = modelo.generate_content([archivo_gemini, prompt])
            spinner_gen.succeed("Contenido procesado y extraído correctamente.")
            
            contenido_md = respuesta.text
            
            # Guardar en obsidian_vault/{materia}/
            carpeta_salida = os.path.join(ruta_raiz, "obsidian_vault", materia_input)
            os.makedirs(carpeta_salida, exist_ok=True)
            
            nombre_archivo_salida = f"{nombre_base.replace(' ', '_')}_Notas.md"
            ruta_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
            
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(contenido_md)
                
            print(f"\n========================================")
            print(f"[ÉXITO] Material ingestado y convertido a Markdown.")
            print(f"Archivo guardado en: {os.path.abspath(ruta_salida)}")
            print(f"========================================")
            break

        except Exception as e:
            spinner_gen.fail(f"Error durante la generación: {e}")
            if "429" in str(e) or "ResourceExhausted" in str(e):
                intento_gen += 1
                tiempo_espera = 20 * intento_gen
                print(f"⚠️ Límite de tasa (Rate Limit 429) alcanzado. Esperando {tiempo_espera}s antes de reintentar...")
                time.sleep(tiempo_espera)
            else:
                break
    
    # Limpieza obligatoria en la nube de Google
    if archivo_gemini is not None:
        try:
            print("🧹 Eliminando archivo temporal de los servidores de Google...")
            genai.delete_file(archivo_gemini.name)
            print("✅ Archivo temporal borrado de la nube con éxito.")
        except Exception as del_err:
            print(f"⚠️ No se pudo eliminar el archivo remoto: {del_err}")

    input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ingestar_material(sys.argv[1])
    else:
        print("=" * 60)
        print(" INGESTA DE MATERIAL DE ESTUDIO CON GEMINI (VISIÓN Y TEXTO)")
        print("=" * 60)
        ruta = input("👉 Ingresa la ruta del archivo PDF/DOCX/Diapositiva: ").strip()
        if ruta:
            ingestar_material(ruta)
        else:
            print("❌ Ruta no válida.")
            input("Presiona ENTER para salir...")
