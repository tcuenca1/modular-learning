import sys
import os
import json
import warnings

# Forzar codificación UTF-8 en stdout para evitar errores de encoding en Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Suprimir todas las advertencias de deprecación
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
from pypdf import PdfReader

# Importar core desde modules
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_script)
sys.path.append(ruta_raiz)

from modules.core import gestor_llm


def extraer_texto_local(ruta_archivo: str) -> str:
    """Extrae el texto de un archivo local (PDF, Markdown o TXT)."""
    ext = os.path.splitext(ruta_archivo)[1].lower()
    
    if ext == '.pdf':
        print(f"[PDF] Procesando archivo: {os.path.basename(ruta_archivo)}")
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
        print(f"[TEXTO] Procesando archivo: {os.path.basename(ruta_archivo)}")
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
        print(f"[OK] Sección 4.2 delimitada con éxito ({len(texto_recortado)} caracteres).")
        return texto_recortado
    else:
        print("[AVISO] No se encontró la sección 4.2 exacta. Se analizará el segmento optimizado.")
        if len(texto) > 30000:
            return texto[:30000]
        return texto


def procesar_archivo_individual(ruta_archivo: str) -> None:
    """Procesa un archivo individual de sílabo y guarda el cronograma en data/schedules/."""
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_raiz = os.path.dirname(ruta_script)
        ruta_env = os.path.join(ruta_raiz, '.env')
        
        if os.path.exists(ruta_env):
            load_dotenv(ruta_env, override=True)
        else:
            load_dotenv(override=True)

        llm = gestor_llm.obtener_llm()

        try:
            contenido_bruto = extraer_texto_local(ruta_archivo)
            if not contenido_bruto.strip():
                print(f"\n[AVISO] El archivo {os.path.basename(ruta_archivo)} está vacío. Omitiendo...")
                return
            
            contenido_texto = delimitar_seccion_temas(contenido_bruto)
        except Exception as e:
            print(f"\n[ERROR] No se pudo procesar el archivo {os.path.basename(ruta_archivo)}: {e}")
            return

        nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
        nombre_sugerido = nombre_base.replace("SYLLABUS", "").replace("syllabus", "").replace("-", "").strip()
        if not nombre_sugerido:
            nombre_sugerido = nombre_base

        print(f"[MATERIA] Asignatura detectada del archivo: {nombre_sugerido}")
        nombre_materia = input(f"-> Presiona ENTER para aceptar '{nombre_sugerido}' o escribe otro nombre: ").strip()
        if not nombre_materia:
            nombre_materia = nombre_sugerido

        ruta_prompt = os.path.join(ruta_raiz, "prompts", "04_extraccion_silabo.md")
        try:
            with open(ruta_prompt, 'r', encoding='utf-8') as f:
                prompt_base = f.read()
        except Exception:
            prompt_base = "Extrae el cronograma de clases en JSON."

        prompt_completo = (
            f"{prompt_base}\n\n"
            f"Contenido de la Sección 4.2 del Sílabo ({nombre_materia}):\n"
            f"----------------------------------------\n"
            f"{contenido_texto}\n"
            f"----------------------------------------"
        )

        try:
            print("[IA] Analizando y estructurando cronograma mediante puerto LLM...")
            datos = llm.generar_json_estructurado(prompt_completo)
            
            carpeta_schedules = os.path.join(ruta_raiz, "data", "schedules")
            os.makedirs(carpeta_schedules, exist_ok=True)
            
            materia_slug = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in nombre_materia).strip().replace(' ', '_')
            ruta_salida = os.path.join(carpeta_schedules, f"{materia_slug}_cronograma.json")
            
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
                
            print(f"\n[EXITO] Se extrajeron {len(datos)} clases para '{nombre_materia}'.")
            print(f"Guardado en: {os.path.abspath(ruta_salida)}\n")
            
        except json.JSONDecodeError:
            print(f"\n[ERROR] La respuesta de la IA para {nombre_materia} no tiene un formato JSON válido.")
        except Exception as e:
            print(f"\n[ERROR] Fallo en la generación o parseo para {nombre_materia}: {e}")

    except Exception as err:
        print(f"\n[ERROR] {err}")


def procesar_ruta(ruta: str) -> None:
    """Procesa un archivo individual o escanea una carpeta completa en busca de sílabos."""
    ruta = ruta.strip('"').strip("'")
    if not os.path.exists(ruta):
        print(f"[ERROR] La ruta especificada no existe: {ruta}")
        return

    if os.path.isdir(ruta):
        print(f"[CARPETA] Analizando carpeta de sílabos:\n   {ruta}")
        archivos = [
            os.path.join(ruta, f) for f in os.listdir(ruta)
            if os.path.isfile(os.path.join(ruta, f)) and f.lower().endswith(('.pdf', '.md', '.txt'))
        ]
        if not archivos:
            print("[AVISO] No se encontraron archivos PDF, MD o TXT en la carpeta especificada.")
            return
        
        print(f"[LOTE] Se encontraron {len(archivos)} archivos. Iniciando procesamiento...")
        for idx, archivo in enumerate(archivos, 1):
            print(f"\n" + "=" * 50)
            print(f" ARCHIVO {idx} DE {len(archivos)}")
            print("=" * 50)
            procesar_archivo_individual(archivo)
    else:
        procesar_archivo_individual(ruta)


def run():
    if len(sys.argv) > 1:
        procesar_ruta(sys.argv[1])
    else:
        print("=" * 50)
        print(" EXTRACTOR MASIVO DE CRONOGRAMAS DE SÍLABOS (LLM PORT)")
        print("=" * 50)
        ruta_input = input("-> Ingresa la ruta de un archivo o carpeta con sílabos: ").strip()
        if ruta_input:
            procesar_ruta(ruta_input)
        else:
            print("[ERROR] Ruta no válida.")
        input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    run()
