import os
import json
from datetime import datetime
from typing import List, Dict, Any


def leer_prompt(nombre_archivo: str) -> str:
    """
    Lee un archivo de instrucciones desde la carpeta 'prompts/' 
    utilizando codificación UTF-8.
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
    """Lee el contenido de un archivo de material de estudio en formato Markdown (.md)."""
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo de material de estudio no existe en la ruta: {ruta_archivo}")
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        raise IOError(f"Error al leer el material de estudio en '{ruta_archivo}': {e}")


def cargar_materias(archivo_materias: str = os.path.join("data", "materias.txt")) -> List[str]:
    """Carga la lista de materias desde data/materias.txt. Si no existe, lo crea con valores iniciales."""
    materias_iniciales = ["Seguridad de la Informacion", "IoT"]
    
    os.makedirs(os.path.dirname(archivo_materias), exist_ok=True)
    
    if not os.path.exists(archivo_materias):
        try:
            with open(archivo_materias, 'w', encoding='utf-8') as f:
                f.write("\n".join(materias_iniciales))
        except Exception:
            pass
        return materias_iniciales

    try:
        with open(archivo_materias, 'r', encoding='utf-8') as f:
            materias = [line.strip() for line in f if line.strip()]
        return materias if materias else materias_iniciales
    except Exception:
        return materias_iniciales


def agregar_materia(nueva_materia: str, archivo_materias: str = os.path.join("data", "materias.txt")) -> None:
    """Añade una nueva materia a data/materias.txt si no existe."""
    nueva_materia = nueva_materia.strip()
    if not nueva_materia:
        return
    materias = cargar_materias(archivo_materias)
    if nueva_materia not in materias:
        materias.append(nueva_materia)
        try:
            os.makedirs(os.path.dirname(archivo_materias), exist_ok=True)
            with open(archivo_materias, 'w', encoding='utf-8') as f:
                f.write("\n".join(materias))
        except Exception as e:
            print(f"⚠️ No se pudo guardar la nueva materia en disco: {e}")


def obtener_proximas_clases(materia: str) -> List[Dict[str, Any]]:
    """
    Lee el archivo cronograma.json correspondiente a la materia en data/cronogramas/,
    filtra las clases con estado 'pendiente' y devuelve las primeras 5.
    """
    carpeta_cronogramas = os.path.join("data", "cronogramas")
    if not os.path.exists(carpeta_cronogramas):
        return []

    materia_slug = "".join(c if c.isalnum() or c in (' ', '_', '-') else '' for c in materia).strip().replace(' ', '_')
    posibles_nombres = [
        f"{materia}_cronograma.json",
        f"{materia_slug}_cronograma.json"
    ]

    ruta_archivo = None
    for nombre in posibles_nombres:
        ruta_prueba = os.path.join(carpeta_cronogramas, nombre)
        if os.path.exists(ruta_prueba):
            ruta_archivo = ruta_prueba
            break

    if not ruta_archivo:
        return []

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            clases = json.load(f)
        
        if not isinstance(clases, list):
            return []

        pendientes = [c for c in clases if c.get("estado", "").lower() == "pendiente"]
        return pendientes[:5]
    except Exception as e:
        print(f"⚠️ Error al leer el cronograma de {materia}: {e}")
        return []


def guardar_resumen_obsidian(
    materia: str,
    tema: str,
    contenido: str,
    ruta_boveda: str
) -> bool:
    """
    Crea un archivo .md dentro de la bóveda de Obsidian y un archivo índice central
    para asegurar que Obsidian genere la constelación (grafo de conexiones).
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
tags: [{materia_sin_espacios}, repaso, tutor_ia]
---

# Sesión de Estudio: {tema}
> **Asignatura principal:** [[{materia}]]

---

"""
        contenido_final = frontmatter + contenido + f"\n\n---\n*Nota generada por Sistema de Tutoría CLI.*\nConexión raíz: [[{materia}]]\n"
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_final)
            
        ruta_indice = os.path.join(ruta_boveda, f"{materia}.md")
        link_tag = f"[[{tema_sanitizado}]]"
        
        if not os.path.exists(ruta_indice):
            with open(ruta_indice, 'w', encoding='utf-8') as idx_file:
                idx_file.write(f"---\nmateria: {materia}\ntipo: indice_asignatura\ntags: [{materia_sin_espacios}, indice]\n---\n# 📚 Asignatura: {materia}\n\n## 🕸️ Grafo de Constelación de Temas\n- {link_tag}\n")
        else:
            with open(ruta_indice, 'r', encoding='utf-8') as idx_file:
                idx_content = idx_file.read()
            if link_tag not in idx_content:
                with open(ruta_indice, 'w', encoding='utf-8') as idx_file:
                    idx_file.write(idx_content + f"\n- {link_tag}")

        return True
        
    except Exception as e:
        print(f"❌ Error al guardar el resumen en Obsidian: {e}")
        return False
