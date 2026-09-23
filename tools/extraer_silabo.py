import sys
import os
import json
import warnings

# Suprimir todas las advertencias de deprecación
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader


def extraer_texto_local(ruta_archivo: str) -> str:
    """
    Extrae el texto de un archivo local de forma robusta:
    - Si es PDF, utiliza pypdf para extraer texto de todas las páginas.
    - Si es Markdown o TXT, lo lee como texto plano en UTF-8 (con fallback a latin-1).
    """
    ext = os.path.splitext(ruta_archivo)[1].lower()
    
    if ext == '.pdf':
        print("📄 Procesando archivo PDF localmente...")
        texto_acumulado = []
        try:
            reader = PdfReader(ruta_archivo)
            for pagina in reader.pages:
                t = pagina.extract_text()
                if t:
                    texto_acumulado.append(t)
            return "\n".join(texto_acumulado)
        except Exception as e:
            raise RuntimeError(f"No se pudo extraer texto del PDF con pypdf: {e}")
    else:
        print("📄 Procesando archivo de texto/markdown localmente...")
        # Intentar UTF-8 primero, si falla usar latin-1 para evitar UnicodeDecodeError
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(ruta_archivo, 'r', encoding='latin-1') as f:
                return f.read()


def procesar_archivo(ruta_archivo: str) -> None:
    """
    Procesa un archivo (PDF, Markdown o TXT) extrayendo su texto localmente 
    y enviándolo directamente al modelo de Gemini para obtener el cronograma en JSON.
    (Evita genai.upload_file y su servicio deprecado de descubrimiento $discovery/rest).
    """
    try:
        # 1. Cargar el .env desde la raíz del proyecto (forzando override)
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

        # 2. Configurar la API de Google Generative AI
        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel('gemini-3.5-flash-lite')

        print(f"\nLeyendo archivo local: {os.path.basename(ruta_archivo)}")
        
        try:
            contenido_texto = extraer_texto_local(ruta_archivo)
            if not contenido_texto.strip():
                print("\n[ERROR] El archivo extraído está vacío o no contiene texto legible.")
                return
            print(f"✅ Texto extraído con éxito ({len(contenido_texto)} caracteres). Analizando con Gemini...")
        except Exception as e:
            print(f"\n[ERROR] No se pudo leer el archivo local: {e}")
            return

        # 3. Cargar prompt desde prompts/04_extraccion_silabo.md
        ruta_prompt = os.path.join(ruta_raiz, "prompts", "04_extraccion_silabo.md")
        try:
            with open(ruta_prompt, 'r', encoding='utf-8') as f:
                prompt_base = f.read()
        except Exception:
            prompt_base = "Extrae el cronograma de clases en JSON con fecha, tema, objetivo, contenido y estado pendiente."

        prompt_completo = (
            f"{prompt_base}\n\n"
            f"Contenido del documento a analizar:\n"
            f"----------------------------------------\n"
            f"{contenido_texto}\n"
            f"----------------------------------------"
        )

        try:
            # Enviar directamente como texto al modelo (evita File API / discovery/rest)
            respuesta = modelo.generate_content(
                prompt_completo,
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
            print(f"Respuesta cruda:\n{respuesta.text}")
        except Exception as e:
            print(f"\n[ERROR] Fallo en la generación o parseo: {e}")

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
