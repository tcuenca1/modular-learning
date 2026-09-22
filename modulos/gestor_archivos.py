import os
from datetime import datetime
from typing import Optional


def leer_prompt(nombre_archivo: str) -> str:
    """
    Lee un archivo de instrucciones desde la carpeta 'prompts/' 
    utilizando codificación UTF-8 (soporta archivos .md o .txt).
    """
    ruta_completa = os.path.join("prompts", nombre_archivo)
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo de prompt '{nombre_archivo}' no se encontró en la carpeta prompts/.")
    except Exception as e:
        raise IOError(f"Error al leer el prompt '{nombre_archivo}': {e}")


def leer_material_estudio(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo de material de estudio en formato Markdown (.md).
    Valida obligatoriamente que el archivo exista antes de proceder.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo de material de estudio no existe en la ruta: {ruta_archivo}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        raise IOError(f"Error al leer el material de estudio en '{ruta_archivo}': {e}")


def guardar_resumen_obsidian(
    materia: str,
    tema: str,
    contenido: str,
    ruta_boveda: str
) -> bool:
    """
    Crea un archivo .md dentro de la bóveda de Obsidian especificada en la carpeta de la materia.
    Inyecta YAML Frontmatter con la estructura requerida.
    Retorna True si tuvo éxito, False si falló.
    """
    try:
        carpeta_materia = os.path.join(ruta_boveda, materia)
        os.makedirs(carpeta_materia, exist_ok=True)
        
        tema_sanitizado = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in tema).strip().replace(' ', '_')
        if not tema_sanitizado:
            tema_sanitizado = "resumen_sesion"
            
        nombre_archivo = f"{tema_sanitizado}.md"
        ruta_archivo = os.path.join(carpeta_materia, nombre_archivo)
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        materia_sin_espacios = materia.lower().replace(' ', '_')
        
        frontmatter = f"""---
materia: {materia}
fecha: {fecha_actual}
estado: pendiente_repaso
tags: [{materia_sin_espacios}, repaso]
---

"""
        contenido_final = frontmatter + contenido
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_final)
            
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar el resumen en Obsidian: {e}")
        return False
