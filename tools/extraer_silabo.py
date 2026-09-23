import sys
import os
import json
import warnings
import time

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
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(ruta_archivo, 'r', encoding='latin-1') as f:
                return f.read()


def delimitar_seccion_temas(texto: str) -> str:
    """
    Delimita el texto extraído del PDF para analizar únicamente desde 
    '4.2 Estructura de la unidad didáctica por temas' hasta antes de 
    '4.3 Distribución de horas en unidades y temas'.
    """
    inicio_clave = "4.2 Estructura de la unidad didáctica por temas"
    fin_clave = "4.3 Distribución de horas en unidades y temas"
    
    # Búsqueda insensible a mayúsculas/minúsculas
    texto_lower = texto.lower()
    pos_inicio = texto_lower.find(inicio_clave.lower())
    
    if pos_inicio == -1:
        # Intentar variaciones comunes si el título exacto varía ligeramente
        for variante in ["4.2. estructura", "4.2 estructura", "unidad didáctica por temas", "estructura de la unidad"]:
            pos_inicio = texto_lower.find(variante)
            if pos_inicio != -1:
                break
                
    pos_fin = texto_lower.find(fin_clave.lower())
    if pos_fin == -1:
        for variante in ["4.3.", "4.3 distribución", "5. metodología", "5. sistema", "bibliografía"]:
            pos_fin = texto_lower.find(variante)
            if pos_fin != -1 and pos_fin > pos_inicio:
                break

    if pos_inicio != -1:
        texto_recortado = texto[pos_inicio:]
        if pos_fin != -1 and pos_fin > pos_inicio:
            rel_fin = pos_fin - pos_inicio
            texto_recortado = texto_recortado[:rel_fin]
        print(f"🎯 Sección 4.2 delimitada con éxito ({len(texto_recortado)} caracteres).")
        return texto_recortado
    else:
        print("⚠️ No se encontró la sección 4.2 exacta. Se analizará el documento completo o un segmento optimizado.")
        # Si el texto es muy largo y no se encontró la sección, tomar los primeros 30,000 caracteres para evitar rate limits
        if len(texto) > 30000:
            return texto[:30000]
        return texto


def procesar_archivo(ruta_archivo: str) -> None:
    """
    Procesa un archivo (PDF, Markdown o TXT) extrayendo su texto localmente,
    delimitándolo a la sección 4.2 y enviándolo a Gemini para obtener el cronograma en JSON.
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
            contenido_bruto = extraer_texto_local(ruta_archivo)
            if not contenido_bruto.strip():
                print("\n[ERROR] El archivo extraído está vacío o no contiene texto legible.")
                return
            
            # Delimitar estrictamente a la sección 4.2 requerida
            contenido_texto = delimitar_seccion_temas(contenido_bruto)
            print(f"✅ Texto optimizado para la IA ({len(contenido_texto)} caracteres). Analizando con Gemini...")
        except Exception as e:
            print(f"\n[ERROR] No se pudo leer o procesar el archivo local: {e}")
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
            f"Contenido de la Sección 4.2 del Sílabo:\n"
            f"----------------------------------------\n"
            f"{contenido_texto}\n"
            f"----------------------------------------"
        )

        max_intentos = 3
        for intento in range(max_intentos):
            try:
                print(f"⏳ Consultando a la IA (Intento {intento + 1}/{max_intentos})...")
                respuesta = modelo.generate_content(
                    prompt_completo,
                    generation_config={"response_mime_type": "application/json"}
                )
                
                datos = json.loads(respuesta.text)
                
                ruta_salida = os.path.splitext(ruta_archivo)[0] + "_cronograma.json"
                with open(ruta_salida, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                    
                print(f"\n========================================")
                print(f"[ÉXITO] Se extrajeron {len(datos)} clases válidas de la sección 4.2.")
                print(f"Archivo guardado en: {ruta_salida}")
                print(f"========================================")
                break  # Si tiene éxito, rompe el bucle de reintentos
                
            except json.JSONDecodeError:
                print("\n[ERROR] La respuesta de la IA no tiene un formato JSON válido.")
                print(f"Respuesta cruda:\n{respuesta.text}")
                break # Rompe porque no es un error de cuota, sino de formato
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "Quota exceeded" in error_str:
                    espera = 60
                    print(f"\n⚠️ Límite de la API gratuita alcanzado.")
                    print(f"El sistema se pausará {espera} segundos para enfriar la cuota antes de reintentar...")
                    time.sleep(espera) # Pausa la ejecución sin cerrar el programa
                else:
                    print(f"\n[ERROR] Fallo en la generación: {e}")
                    break # Rompe si es un error distinto a la cuota

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
