import sys
import os
import json
import warnings

# Suprimir todas las advertencias (incluyendo FutureWarning de google.generativeai)
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai


def procesar_archivo(ruta_archivo: str) -> None:
    # 1. Cargar el .env desde la raíz del proyecto (un nivel arriba de tools/)
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_raiz = os.path.dirname(ruta_script)
    load_dotenv(os.path.join(ruta_raiz, '.env'))
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "tu_api_key_de_google_gemini_aqui":
        print("\n[ERROR] Debes configurar tu GEMINI_API_KEY real en el archivo .env de la raíz del proyecto.")
        return

    # 2. Configurar la IA
    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    print(f"\nSubiendo archivo a Gemini: {os.path.basename(ruta_archivo)}")
    
    archivo_gemini = None
    try:
        # Detectar el tipo MIME según la extensión (.pdf, .md, .txt)
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
            
        print("Archivo subido con éxito. Analizando el contenido...")
    except Exception as e:
        print(f"\n[ERROR] Fallo al subir el archivo (verifica que tu API Key sea válida): {e}")
        return

    # 3. Prompt Estructurado
    prompt = """
    Eres un experto en extracción de datos. Analiza este documento (puede ser un sílabo en PDF o notas en Markdown/Texto).
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
        # Generar contenido forzando el formato JSON
        respuesta = modelo.generate_content(
            [archivo_gemini, prompt],
            generation_config={"response_mime_type": "application/json"}
        )
        
        datos = json.loads(respuesta.text)
        
        # 4. Guardar el JSON resultante
        ruta_salida = os.path.splitext(ruta_archivo)[0] + "_cronograma.json"
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
            
        print(f"\n========================================")
        print(f"[EXITO] Se extrajeron {len(datos)} clases válidas.")
        print(f"Archivo guardado en: {ruta_salida}")
        print(f"========================================")
        
    except json.JSONDecodeError:
        print("\n[ERROR] La IA no devolvió un JSON válido.")
    except Exception as e:
        print(f"\n[ERROR] Fallo en la extracción y parseo: {e}")
    finally:
        # 5. Limpieza obligatoria: Borrar el archivo de los servidores de Google
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
