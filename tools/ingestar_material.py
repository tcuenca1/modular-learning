import sys
import os
import time
import json
import warnings
import mimetypes

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
import questionary

# Importar core desde modules
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_raiz = os.path.dirname(ruta_script)
sys.path.append(ruta_raiz)

from modules.core import gestor_archivos

def ingestar_material(ruta_archivo: str) -> None:
    """
    Sube un archivo (PDF, imágenes) a Gemini (gemini-3.5-flash-lite) mediante Inline Data,
    extrae texto y describe imágenes semánticamente con Wikilinks para Obsidian.
    """
    ruta_archivo = ruta_archivo.strip('"').strip("'")
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo no existe en la ruta: {ruta_archivo}")
        return

    load_dotenv(os.path.join(ruta_raiz, '.env'), override=True)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error crítico: No se encontró GEMINI_API_KEY en el archivo .env.")
        return

    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('gemini-3.5-flash-lite')

    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    ext = os.path.splitext(ruta_archivo)[1].lower()

    # Asegurar que existan las 5 carpetas de materias en obsidian_vault/
    materias = gestor_archivos.cargar_materias()
    vault_path = os.path.join(ruta_raiz, "obsidian_vault")
    for mat in materias:
        os.makedirs(os.path.join(vault_path, mat), exist_ok=True)

    opciones_menu = materias + ["[ + ] Añadir nueva asignatura..."]
    
    print("\n📚 Selecciona la asignatura a la que pertenece este material:")
    seleccion = questionary.select(
        "Selecciona una opción:",
        choices=opciones_menu,
        style=questionary.Style([
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
            ('answer', 'fg:green bold'),
        ])
    ).ask()

    if seleccion is None:
        print("\nOperación cancelada.")
        return

    if "[ + ]" in seleccion:
        nueva_mat = input("\n✍️ Ingresa el nombre de la nueva asignatura: ").strip()
        while not nueva_mat:
            print("⚠️ El nombre no puede estar vacío.")
            nueva_mat = input("✍️ Ingresa el nombre de la nueva asignatura: ").strip()
        gestor_archivos.agregar_materia(nueva_mat)
        materia_input = nueva_mat
        os.makedirs(os.path.join(vault_path, materia_input), exist_ok=True)
    else:
        materia_input = seleccion

    print(f"✅ Asignatura seleccionada: {materia_input}")

    tipo_input = input("📄 Tipo de material (diapositiva / actividad / lectura) [diapositiva]: ").strip().lower()
    if not tipo_input:
        tipo_input = "diapositiva"

    if ext == '.pdf':
        mime_type = 'application/pdf'
    else:
        mime_type = mimetypes.guess_type(ruta_archivo)[0] or 'text/plain'

    try:
        with open(ruta_archivo, "rb") as f:
            datos_binarios = f.read()
            
        documento_inline = {
            "mime_type": mime_type,
            "data": datos_binarios
        }
    except Exception as e:
        print(f"❌ Error al leer el archivo localmente: {e}")
        return

    # Cargar prompt desde prompts/05_ingesta_material.md
    try:
        prompt_template = gestor_archivos.leer_prompt("05_ingesta_material.md")
    except Exception:
        prompt_template = "Actúa como un extractor de conocimiento experto y transcribe este documento en Markdown."

    materia_slug = materia_input.lower().replace(' ', '_')
    fecha_actual = time.strftime('%Y-%m-%d')

    prompt = (
        prompt_template
        .replace("{materia}", materia_input)
        .replace("{tipo}", tipo_input)
        .replace("{fecha}", fecha_actual)
        .replace("{materia_slug}", materia_slug)
    )

    max_reintentos = 3
    intento_gen = 0

    while intento_gen < max_reintentos:
        try:
            with Halo(text='Analizando documento y extrayendo conocimiento visual con Gemini 3.5 Flash Lite...', spinner='line') as spinner_gen:
                respuesta = modelo.generate_content([documento_inline, prompt])
                spinner_gen.succeed("Contenido procesado y extraído correctamente.")
            
            contenido_md = respuesta.text
            
            # Guardar en obsidian_vault/{materia_input}/
            carpeta_salida = os.path.join(vault_path, materia_input)
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
            if "429" in str(e) or "ResourceExhausted" in str(e):
                intento_gen += 1
                tiempo_espera = 20 * intento_gen
                print(f"⚠️ Límite de tasa (Rate Limit 429) alcanzado. Esperando {tiempo_espera}s...")
                with Halo(text=f'Esperando {tiempo_espera}s por Rate Limit...', spinner='line'):
                    time.sleep(tiempo_espera)
            else:
                print(f"\n❌ Error durante la generación: {e}")
                break
    
    input("\nPresiona ENTER para salir...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ingestar_material(sys.argv[1])
    else:
        print("=" * 60)
        print(" INGESTA DE MATERIAL DE ESTUDIO CON GEMINI (VISIÓN Y TEXTO)")
        print("=" * 60)
        ruta = input("👉 Ingresa la ruta del archivo (PDF/Imágenes): ").strip()
        if ruta:
            ingestar_material(ruta)
        else:
            print("❌ Ruta no válida.")
            input("Presiona ENTER para salir...")
