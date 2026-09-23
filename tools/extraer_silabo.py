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
    """Extrae el texto de un archivo local (PDF, Markdown o TXT)."""
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
    """Delimita el texto extraído para analizar únicamente la Sección 4.2."""
    inicio_clave = "4.2 Estructura de la unidad didáctica por temas"
    fin_clave = "4.3 Distribución de horas en unidades y temas"
    
    texto_lower = texto.lower()
    pos_inicio = texto_lower.find(inicio_clave.lower())
    
    if pos_inicio == -1:
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
        print("⚠️ No se encontró la sección 4.2 exacta. Se analizará el segmento optimizado.")
        if len(texto) > 30000:
            return texto[:30000]
        return texto


def procesar_archivo(ruta_archivo: str) -> None:
    """Procesa un sílabo y guarda el cronograma JSON estructurado en data/cronogramas/."""
    try:
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

        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel('gemini-3.5-flash-lite')

        print(f"\nLeyendo archivo local: {os.path.basename(ruta_archivo)}")
        
        try:
            contenido_bruto = extraer_texto_local(ruta_archivo)
            if not contenido_bruto.strip():
                print("\n[ERROR] El archivo extraído está vacío.")
                return
            
            contenido_texto = delimitar_seccion_temas(contenido_bruto)
            print(f"✅ Texto optimizado ({len(contenido_texto)} caracteres). Analizando con Gemini...")
        except Exception as e:
            print(f"\n[ERROR] No se pudo leer el archivo: {e}")
            return

        # Pedir nombre de la materia para el archivo cronograma
        nombre_materia = input("📚 Ingresa el nombre exacto de la asignatura para este cronograma: ").strip()
        if not nombre_materia:
            nombre_materia = os.path.splitext(os.path.basename(ruta_archivo))[0]

        ruta_prompt = os.path.join(ruta_raiz, "prompts", "04_extraccion_silabo.md")
        try:
            with open(ruta_prompt, 'r', encoding='utf-8') as f:
                prompt_base = f.read()
        except Exception:
            prompt_base = "Extrae el cronograma de clases en JSON."

        prompt_completo = (
            f"{prompt_base}\n\n"
            f"Contenido de la Sección 4.2 del Sílabo:\n"
            f"----------------------------------------\n"
            f"{contenido_texto}\n"
            f"----------------------------------------"
        )

        try:
            respuesta = modelo.generate_content(
                prompt_completo,
                generation_config={"response_mime_type": "application/json"}
            )
            
            datos = json.loads(respuesta.text)
            
            # Guardar en data/cronogramas/
            carpeta_cronogramas = os.path.join(ruta_raiz, "data", "cronogramas")
            os.makedirs(carpeta_cronogramas, exist_ok=True)
            
            materia_slug = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in nombre_materia).strip().replace(' ', '_')
            ruta_salida = os.path.join(carpeta_cronogramas, f"{materia_slug}_cronograma.json")
            
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
                
            print(f"\n========================================")
            print(f"[ÉXITO] Se extrajeron {len(datos)} clases válidas.")
            print(f"Cronograma guardado en: {os.path.abspath(ruta_salida)}")
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
