import sys
import os
import json
import warnings

# Suprimir todas las advertencias de deprecación
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai


def procesar_archivo(ruta_archivo: str) -> None:
    """
    Procesa un archivo (PDF, Markdown o TXT) subiéndolo a la API de Gemini 
    para extraer un cronograma estructurado en JSON.
    """
    try:
        # Localizar y cargar el archivo .env ubicado en la raíz del proyecto (forzando override)
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_raiz = os.path.dirname(ruta_script)
        ruta_env = os.path.join(ruta_raiz, '.env')
        
        if os.path.exists(ruta_env):
            load_dotenv(ruta_env, override=True)
        else:
            load_dotenv(override=True)

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print(f"\n[ERROR] No se encontró la variable 'GEMINI_API_KEY' en el archivo .env ubicado en: {ruta_raiz}")
            return

        # Configurar la API de Google Generative AI
        genai.configure(api_key=api_key)
        # Usar el mismo modelo consistente con main.py (gemini-3.5-flash-lite)
        modelo = genai.GenerativeModel('gemini-3.5-flash-lite')

        print(f"\nSubiendo archivo a la API de Gemini: {os.path.basename(ruta_archivo)}")
        
        archivo_gemini = None
        try:
            ext = os.path.splitext(ruta_archivo)[1].lower()
            mime_map = {
                '.pdf': 'application/pdf',
                '.md': 'text/markdown',
                '.txt': 'text/plain'
            }
            mime_type = mime_map.get(ext, None)
            
            if mime_type:
                archivo_gemini = genai.upload_file(ruta_archivo, mime_type=mime_type)
            else:
                archivo_gemini = genai.upload_file(ruta_archivo)
                
            print("Archivo subido con éxito. Analizando contenido con Gemini...")
        except Exception as e:
            print(f"\n[ERROR] Fallo al subir el archivo a la API: {e}")
            return

        # Cargar prompt desde prompts/04_extraccion_silabo.md
        ruta_prompt = os.path.join(ruta_raiz, "prompts", "04_extraccion_silabo.md")
        try:
            with open(ruta_prompt, 'r', encoding='utf-8') as f:
                prompt = f.read()
        except Exception:
            prompt = "Extrae el cronograma de clases en JSON."

        try:
            respuesta = modelo.generate_content(
                [archivo_gemini, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            
            datos = json.loads(respuesta.text)
            
            ruta_salida = os.path.splitext(ruta_archivo)[0] + "_cronograma.json"
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
                
            print(f"\n========================================")
            print(f"[ÉXITO] Se extrajeron {len(datos)} clases válidas.")
            print(f"Archivo guardado en: {ruta_salida}")
            print(f"========================================")
            
        except json.JSONDecodeError:
            print("\n[ERROR] La respuesta de la IA no tiene un formato JSON válido.")
        except Exception as e:
            print(f"\n[ERROR] Fallo en la extracción y parseo: {e}")
        finally:
            if archivo_gemini is not None:
                try:
                    genai.delete_file(archivo_gemini.name)
                    print("Archivo temporal eliminado de la nube de Google.")
                except Exception as del_err:
                    print(f"⚠️ No se pudo eliminar el archivo remoto: {del_err}")

    except Exception as err:
        print(f"\n[ERROR CRÍTICO]: {err}")
    finally:
        print("\n" + "=" * 40)
        input("Presiona ENTER para salir...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        procesar_archivo(sys.argv[1])
    else:
        print("=" * 50)
        print(" EXTRACTOR DE CRONOGRAMA DE SÍLABO (GEMINI)")
        print("=" * 50)
        ruta_input = input("👉 Ingresa la ruta del archivo (PDF, MD o TXT): ").strip()
        ruta_input = ruta_input.strip('"').strip("'")
        if ruta_input and os.path.exists(ruta_input):
            procesar_archivo(ruta_input)
        else:
            print("❌ Ruta de archivo no válida o no encontrada.")
            input("Presiona ENTER para salir...")
