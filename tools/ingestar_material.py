import sys
import os
import time
import json
import warnings
import mimetypes
import tempfile

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


def convertir_a_pdf_si_es_necesario(ruta_archivo: str) -> str:
    """
    Convierte archivos .docx o .pptx a PDF temporal para que Gemini pueda procesarlos óptimamente.
    Retorna la ruta del archivo PDF (o la misma ruta si ya es PDF u otro formato).
    """
    ext = os.path.splitext(ruta_archivo)[1].lower()
    if ext == '.pdf':
        return ruta_archivo

    temp_dir = tempfile.gettempdir()
    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    ruta_pdf = os.path.join(temp_dir, f"{nombre_base}.pdf")

    if ext == '.docx':
        try:
            with Halo(text='Convirtiendo documento Word (.docx) a PDF...', spinner='line') as spinner:
                import docx2pdf
                docx2pdf.convert(ruta_archivo, ruta_pdf)
                spinner.succeed("Conversión de Word a PDF completada.")
                return ruta_pdf
        except Exception as e:
            print(f"⚠️ Error al convertir .docx a PDF: {e}. Procesando archivo original...")
            return ruta_archivo

    elif ext == '.pptx':
        try:
            with Halo(text='Convirtiendo presentación PowerPoint (.pptx) a PDF...', spinner='line') as spinner:
                import comtypes.client
                powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
                powerpoint.Visible = 1
                deck = powerpoint.Presentations.Open(os.path.abspath(ruta_archivo), ReadOnly=True, WithWindow=False)
                deck.SaveAs(os.path.abspath(ruta_pdf), 32)
                deck.Close()
                powerpoint.Quit()
                spinner.succeed("Conversión de PowerPoint a PDF completada.")
                return ruta_pdf
        except Exception as e:
            print(f"⚠️ Error al convertir .pptx a PDF: {e}. Asegúrate de tener PowerPoint instalado. Procesando archivo original...")
            return ruta_archivo

    return ruta_archivo


def clasificar_tipo_material(ruta_archivo: str, ruta_raiz_lote: str) -> str:
    """
    Clasifica automáticamente el tipo de material basándose en su ubicación relativa dentro de la carpeta:
    - Raíz de la carpeta -> 'actividad'
    - Subcarpeta que contiene 'MATERIAL DE ESTUDIO' -> 'diapositiva'
    - Subcarpeta que contiene 'MATERIAL ADICIONAL' -> 'lectura'
    - Cualquier otro caso -> 'material_complementario'
    """
    rel_path = os.path.relpath(ruta_archivo, ruta_raiz_lote)
    partes = rel_path.split(os.sep)
    
    if len(partes) == 1:
        return "actividad"
    
    ruta_upper = rel_path.upper()
    if "MATERIAL DE ESTUDIO" in ruta_upper:
        return "diapositiva"
    elif "MATERIAL ADICIONAL" in ruta_upper:
        return "lectura"
    else:
        return "material_complementario"


def ingestar_material(ruta_entrada: str) -> None:
    """
    Procesa archivos individuales o lotes completos de directorios (Batch Processing) 
    con clasificación automática, conversión a PDF, anonimización de datos y organización estructurada en Obsidian.
    """
    ruta_entrada = ruta_entrada.strip('"').strip("'")
    if not os.path.exists(ruta_entrada):
        print(f"❌ Error: La ruta no existe en el sistema: {ruta_entrada}")
        return

    load_dotenv(os.path.join(ruta_raiz, '.env'), override=True)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error crítico: No se encontró GEMINI_API_KEY en el archivo .env.")
        return

    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('gemini-3.5-flash-lite')

    # Asegurar que existan las carpetas de materias en obsidian_vault/
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

    # Recopilar archivos a procesar (Individual o Lote mediante os.walk)
    archivos_a_procesar = []
    if os.path.isdir(ruta_entrada):
        print(f"📁 Escaneando directorio raíz para procesamiento por lote (Batch):\n   {ruta_entrada}")
        for root, dirs, files in os.walk(ruta_entrada):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx', '.pptx')):
                    archivos_a_procesar.append(os.path.join(root, file))
        ruta_raiz_lote = ruta_entrada
    else:
        archivos_a_procesar = [ruta_entrada]
        ruta_raiz_lote = os.path.dirname(ruta_entrada)

    if not archivos_a_procesar:
        print("⚠️ No se encontraron archivos soportados (.pdf, .docx, .pptx) para procesar.")
        return

    print(f"🚀 Total de archivos detectados para ingesta: {len(archivos_a_procesar)}")

    contador_exito = 0
    contador_saltados = 0
    contador_fallidos = 0

    # Cargar prompt desde prompts/05_ingesta_material.md
    try:
        prompt_template = gestor_archivos.leer_prompt("05_ingesta_material.md")
    except Exception:
        prompt_template = "Actúa como un extractor de conocimiento experto y transcribe este documento en Markdown."

    for idx, archivo_path in enumerate(archivos_a_procesar, 1):
        nombre_archivo_original = os.path.basename(archivo_path)
        print(f"\n" + "-" * 60)
        print(f"[{idx}/{len(archivos_a_procesar)}] Procesando: {nombre_archivo_original}")
        print("-" * 60)

        # Verificar si el material ya fue ingestado previamente
        if gestor_archivos.verificar_material_ingestado(nombre_archivo_original):
            print(f"ℹ️ El archivo '{nombre_archivo_original}' ya consta en el registro de ingesta.")
            if len(archivos_a_procesar) == 1:
                reprocesar = questionary.confirm("¿Desea forzar el reprocesamiento de este material?").ask()
                if not reprocesar:
                    print("Saltando archivo...")
                    contador_saltados += 1
                    continue
            else:
                print("⏭️ Omitiendo automáticamente por lote (ya procesado).")
                contador_saltados += 1
                continue

        # Clasificación automática de tipo según ubicación en árbol de carpetas
        tipo_input = clasificar_tipo_material(archivo_path, ruta_raiz_lote)
        print(f"📂 Tipo clasificado automáticamente: '{tipo_input}'")

        # Conversión a PDF si es Word o PowerPoint
        ruta_para_procesar = convertir_a_pdf_si_es_necesario(archivo_path)
        ext = os.path.splitext(ruta_para_procesar)[1].lower()

        if ext == '.pdf':
            mime_type = 'application/pdf'
        else:
            mime_type = mimetypes.guess_type(ruta_para_procesar)[0] or 'text/plain'

        try:
            with open(ruta_para_procesar, "rb") as f:
                datos_binarios = f.read()
                
            documento_inline = {
                "mime_type": mime_type,
                "data": datos_binarios
            }
        except Exception as e:
            print(f"❌ Error al leer el archivo localmente: {e}")
            contador_fallidos += 1
            continue

        materia_slug = materia_input.lower().replace(' ', '_')
        fecha_actual = time.strftime('%Y-%m-%d')

        # Regla estricta de privacidad y anonimización
        regla_privacidad = (
            "\n\n[REGLA ESTRICTA DE PRIVACIDAD Y ANONIMIZACIÓN]:\n"
            "Oculta o anonimiza cualquier nombre de estudiante, profesor, número de identificación institucional, "
            "correos electrónicos o datos personales que aparezcan en el documento. Reemplázalos por etiquetas "
            "genéricas como [ESTUDIANTE], [DOCENTE] o [ID_OMITIDO]."
        )

        prompt = (
            prompt_template
            .replace("{materia}", materia_input)
            .replace("{tipo}", tipo_input)
            .replace("{fecha}", fecha_actual)
            .replace("{materia_slug}", materia_slug)
            + regla_privacidad
        )

        max_reintentos = 3
        intento_gen = 0
        exito_archivo = False

        while intento_gen < max_reintentos:
            try:
                with Halo(text=f'Extrayendo conocimiento con Gemini (Privacidad Activa)...', spinner='line') as spinner_gen:
                    respuesta = modelo.generate_content([documento_inline, prompt])
                    spinner_gen.succeed("Contenido procesado y anonimizado correctamente.")
                
                contenido_md = respuesta.text
                
                # Organización estructurada en el Vault: obsidian_vault/{Materia}/{Tipo.capitalize()}/
                tipo_carpeta = tipo_input.capitalize()
                carpeta_salida = os.path.join(vault_path, materia_input, tipo_carpeta)
                os.makedirs(carpeta_salida, exist_ok=True)
                
                nombre_base = os.path.splitext(nombre_archivo_original)[0]
                nombre_archivo_salida = f"{nombre_base.replace(' ', '_')}_Notas.md"
                ruta_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
                
                with open(ruta_salida, 'w', encoding='utf-8') as f:
                    f.write(contenido_md)
                    
                print(f"[ÉXITO] Guardado en: {os.path.abspath(ruta_salida)}")
                
                # Registrar material en tracking
                gestor_archivos.registrar_material(nombre_archivo_original, materia_input)
                contador_exito += 1
                exito_archivo = True
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

        if not exito_archivo:
            contador_fallidos += 1

    # Resumen final de procesamiento por lote
    print("\n" + "=" * 60)
    print(" 📊 RESUMEN DE PROCESAMIENTO POR LOTE (BATCH INGESTION)")
    print("=" * 60)
    print(f"   Total de archivos evaluados : {len(archivos_a_procesar)}")
    print(f"   Procesados con éxito        : {contador_exito}")
    print(f"   Omitidos (ya procesados)    : {contador_saltados}")
    print(f"   Fallidos                    : {contador_fallidos}")
    print("=" * 60)
    
    input("\nPresiona ENTER para salir...")


def run():
    if len(sys.argv) > 1:
        ingestar_material(sys.argv[1])
    else:
        print("=" * 60)
        print(" INGESTA MASIVA DE MATERIAL DE ESTUDIO (BATCH / PDF / WORD / PPT)")
        print("=" * 60)
        ruta = input("👉 Ingresa la ruta del archivo o carpeta raíz con materiales: ").strip()
        if ruta:
            ingestar_material(ruta)
        else:
            print("❌ Ruta no válida.")
            input("Presiona ENTER para salir...")


if __name__ == "__main__":
    run()
