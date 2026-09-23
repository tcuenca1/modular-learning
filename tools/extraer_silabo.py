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
    # Localizar y cargar el archivo .env ubicado en la raíz del proyecto (un nivel arriba de tools/)
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.dirname(ruta_script)
    ruta_env = os.path.join(ruta_raiz, '.env')
    
    if os.path.exists(ruta_env):
        load_dotenv(ruta_env)
    else:
        load_dotenv()  # Fallback a búsqueda estándar

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"\n[ERROR] No se encontró la variable 'GEMINI_API_KEY' en el archivo .env ubicado en: {ruta_raiz}")
        return

    # Configurar la API de Google Generative AI
    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    print(f"\nSubiendo archivo a la API de Gemini: {os.path.basename(ruta_archivo)}")
    
    archivo_gemini = None
    try:
        # Detectar tipo MIME según la extensión
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
        print(f"\n[ERROR] Fallo al subir el archivo a la API (verifique su GEMINI_API_KEY en el .env): {e}")
        return

    # Prompt estructurado profesional
    prompt = """
    Eres un experto en extracción de datos académicos. Analiza este documento (puede ser un sílabo o notas).
    Busca la tabla, cronograma o sección de contenidos de clases.
    
    Reglas de Extracción:
    1. Extrae cada clase y estructura los datos.
    2. Identifica la 'fecha', el 'tema' principal, el 'objetivo' y haz un resumen directo del 'contenido'.
    3. EXCLUYE las clases que sean sobre presentación de proyectos, revisiones, evaluaciones o exámenes.
    4. Agrega a cada registro la clave "estado" con el valor "pendiente".
    
    Devuelve ÚNICAMENTE un arreglo JSON válido con esta estructura exacta:
    [
      {
        "fecha": "DD/MM/YYYY",
        "tema": "Nombre",
        "objetivo": "Objetivo",
        "contenido": "Resumen",
        "estado": "pendiente"
      }
    ]
    """

    try:
        respuesta = modelo.generate_content(
            [archivo_gemini, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        datos = json.loads(respuesta.text)
        
        # Guardar el JSON resultante junto al archivo original
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
        # Limpieza obligatoria: Borrar el archivo de los servidores de Google
        if archivo_gemini is not None:
            try:
                genai.delete_file(archivo_gemini.name)
                print("Archivo temporal eliminado de la nube de Google.")
            except Exception as del_err:
                print(f"⚠️ No se pudo eliminar el archivo remoto: {del_err}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        procesar_archivo(sys.argv[1])
    else:
        print("ERROR: Debes proporcionar la ruta de un archivo (PDF, MD o TXT).")
