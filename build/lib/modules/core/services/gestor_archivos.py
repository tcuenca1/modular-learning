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
        with open(ruta_completa, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"El archivo de prompt '{nombre_archivo}' no se encontró en la carpeta prompts/."
        )
    except Exception as e:
        raise IOError(f"Error al leer el prompt '{nombre_archivo}': {e}")


def leer_material_estudio(ruta_archivo: str) -> str:
    """Lee el contenido de un archivo de material de estudio en formato Markdown (.md)."""
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"El archivo de material de estudio no existe en la ruta: {ruta_archivo}"
        )

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except Exception as e:
        raise IOError(f"Error al leer el material de estudio en '{ruta_archivo}': {e}")


def cargar_materias(
    archivo_materias: str = os.path.join("data", "config", "materias.txt"),
) -> List[str]:
    """Carga la lista de materias desde data/config/materias.txt. Si no existe, lo crea con valores iniciales."""
    materias_iniciales = [
        "Seguridad de la Informacion",
        "Ingenieria de Software II",
        "Programacion Web",
        "Internet de las Cosas",
        "Tecnologias de Conmutacion I",
    ]

    os.makedirs(os.path.dirname(archivo_materias), exist_ok=True)

    if not os.path.exists(archivo_materias):
        try:
            with open(archivo_materias, "w", encoding="utf-8") as f:
                f.write("\n".join(materias_iniciales))
        except Exception:
            pass
        return materias_iniciales

    try:
        with open(archivo_materias, "r", encoding="utf-8") as f:
            materias = [line.strip() for line in f if line.strip()]
        return materias if materias else materias_iniciales
    except Exception:
        return materias_iniciales


def agregar_materia(
    nueva_materia: str, archivo_materias: str = os.path.join("data", "config", "materias.txt")
) -> None:
    """Añade una nueva materia a data/config/materias.txt si no existe."""
    nueva_materia = nueva_materia.strip()
    if not nueva_materia:
        return
    materias = cargar_materias(archivo_materias)
    if nueva_materia not in materias:
        materias.append(nueva_materia)
        try:
            os.makedirs(os.path.dirname(archivo_materias), exist_ok=True)
            with open(archivo_materias, "w", encoding="utf-8") as f:
                f.write("\n".join(materias))
        except Exception as e:
            print(f"⚠️ No se pudo guardar la nueva materia en disco: {e}")


def obtener_proximas_clases(materia: str) -> List[Dict[str, Any]]:
    """
    Lee el archivo cronograma.json correspondiente a la materia en data/schedules/,
    filtra las clases con estado 'pendiente' y devuelve las primeras 5.
    Utiliza coincidencia robusta (exacta, slug y búsqueda difusa).
    """
    carpeta_data = os.path.join("data", "schedules")
    if not os.path.exists(carpeta_data):
        return []

    materia_slug = (
        "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
        .strip()
        .replace(" ", "_")
        .upper()
    )
    materia_upper = materia.upper().replace(" ", "_")

    posibles_nombres = [
        f"{materia}_cronograma.json",
        f"{materia_slug}_cronograma.json",
        f"{materia_upper}_cronograma.json",
        f"{materia_slug.lower()}_cronograma.json",
    ]

    ruta_archivo = None
    for nombre in posibles_nombres:
        ruta_prueba = os.path.join(carpeta_data, nombre)
        if os.path.exists(ruta_prueba):
            ruta_archivo = ruta_prueba
            break

    if not ruta_archivo:
        try:
            archivos_data = os.listdir(carpeta_data)
            for arch in archivos_data:
                if arch.endswith("_cronograma.json"):
                    if materia_slug.replace("_", "") in arch.upper().replace("_", ""):
                        ruta_archivo = os.path.join(carpeta_data, arch)
                        break
        except Exception:
            pass

    if not ruta_archivo:
        return []

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            clases = data
        elif isinstance(data, dict):
            clases = data.get("clases", data.get("cronograma", []))
        else:
            clases = []

        if not isinstance(clases, list):
            return []

        pendientes = [c for c in clases if c.get("estado", "").lower() == "pendiente"]
        for c in pendientes:
            if "subtemas_adicionales" not in c:
                c["subtemas_adicionales"] = []
            if "materiales_asociados" not in c:
                c["materiales_asociados"] = []
        return pendientes[:5]
    except Exception as e:
        print(f"⚠️ Error al leer el cronograma de {materia}: {e}")
        return []


def obtener_detalle_clase(materia: str, tema: str) -> dict:
    """
    Busca en el cronograma de la materia la clase cuyo tema coincida con el tema indicado
    y retorna su diccionario con 'subtemas_adicionales' y 'materiales_asociados' garantizados.
    """
    carpeta_data = os.path.join("data", "schedules")
    if not os.path.exists(carpeta_data):
        return {"subtemas_adicionales": [], "materiales_asociados": []}

    materia_slug = (
        "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
        .strip()
        .replace(" ", "_")
        .upper()
    )
    materia_upper = materia.upper().replace(" ", "_")

    posibles_nombres = [
        f"{materia}_cronograma.json",
        f"{materia_slug}_cronograma.json",
        f"{materia_upper}_cronograma.json",
        f"{materia_slug.lower()}_cronograma.json",
    ]

    ruta_archivo = None
    for nombre in posibles_nombres:
        ruta_prueba = os.path.join(carpeta_data, nombre)
        if os.path.exists(ruta_prueba):
            ruta_archivo = ruta_prueba
            break

    if not ruta_archivo:
        try:
            for arch in os.listdir(carpeta_data):
                if arch.endswith("_cronograma.json"):
                    if materia_slug.replace("_", "") in arch.upper().replace("_", ""):
                        ruta_archivo = os.path.join(carpeta_data, arch)
                        break
        except Exception:
            pass

    if not ruta_archivo or not os.path.exists(ruta_archivo):
        return {"subtemas_adicionales": [], "materiales_asociados": []}

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            clases = data
        elif isinstance(data, dict):
            clases = data.get("clases", data.get("cronograma", []))
        else:
            clases = []

        tema_buscado = tema.strip().lower()
        for clase in clases:
            tema_clase = clase.get("tema", "").strip().lower()
            if (
                tema_buscado in tema_clase
                or tema_clase in tema_buscado
                or tema_buscado == tema_clase
            ):
                if "subtemas_adicionales" not in clase:
                    clase["subtemas_adicionales"] = []
                if "materiales_asociados" not in clase:
                    clase["materiales_asociados"] = []
                return clase
    except Exception:
        pass

    return {"subtemas_adicionales": [], "materiales_asociados": []}


def marcar_clase_completada(materia: str, tema_exacto: str) -> bool:
    """
    Busca el archivo cronograma.json de la materia en data/schedules/ y marca la clase cuyo tema
    coincida con tema_exacto como 'completado'.
    """
    carpeta_data = os.path.join("data", "schedules")
    if not os.path.exists(carpeta_data):
        return False

    materia_slug = (
        "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in materia)
        .strip()
        .replace(" ", "_")
        .upper()
    )
    materia_upper = materia.upper().replace(" ", "_")

    posibles_nombres = [
        f"{materia}_cronograma.json",
        f"{materia_slug}_cronograma.json",
        f"{materia_upper}_cronograma.json",
        f"{materia_slug.lower()}_cronograma.json",
    ]

    ruta_archivo = None
    for nombre in posibles_nombres:
        ruta_prueba = os.path.join(carpeta_data, nombre)
        if os.path.exists(ruta_prueba):
            ruta_archivo = ruta_prueba
            break

    if not ruta_archivo:
        try:
            for arch in os.listdir(carpeta_data):
                if arch.endswith("_cronograma.json"):
                    if materia_slug.replace("_", "") in arch.upper().replace("_", ""):
                        ruta_archivo = os.path.join(carpeta_data, arch)
                        break
        except Exception:
            pass

    if not ruta_archivo or not os.path.exists(ruta_archivo):
        return False

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            clases = data
            es_lista = True
        elif isinstance(data, dict):
            clases = data.get("clases", data.get("cronograma", []))
            es_lista = False
        else:
            return False

        if not isinstance(clases, list):
            return False

        actualizado = False
        tema_buscado = tema_exacto.strip().lower()

        for clase in clases:
            tema_clase = clase.get("tema", "").strip().lower()
            if (
                tema_buscado in tema_clase
                or tema_clase in tema_buscado
                or tema_buscado == tema_clase
            ):
                clase["estado"] = "completado"
                actualizado = True

        if actualizado:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                if es_lista:
                    json.dump(clases, f, indent=4, ensure_ascii=False)
                else:
                    data["clases"] = clases
                    json.dump(data, f, indent=4, ensure_ascii=False)
            return True

        return False
    except Exception as e:
        print(f"⚠️ Error al actualizar el estado de la clase en cronograma: {e}")
        return False


def _obtener_ruta_registro() -> str:
    return os.path.join("data", "config", "registro_materiales.json")


def verificar_material_ingestado(nombre_archivo: str) -> bool:
    """Verifica si un archivo de material ya fue procesado e ingestado previamente."""
    ruta = _obtener_ruta_registro()
    if not os.path.exists(ruta):
        return False
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            registro = json.load(f)
        if isinstance(registro, list):
            return any(
                item.get("nombre", "").lower() == nombre_archivo.lower() for item in registro
            )
        elif isinstance(registro, dict):
            return nombre_archivo in registro or nombre_archivo.lower() in [
                k.lower() for k in registro.keys()
            ]
        return False
    except Exception:
        return False


def registrar_material(nombre_archivo: str, materia: str) -> None:
    """Registra un nuevo material ingestado en el archivo JSON de tracking ubicado en data/config/."""
    ruta = _obtener_ruta_registro()
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    registro = []
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = json.load(f)
                if isinstance(contenido, list):
                    registro = contenido
                elif isinstance(contenido, dict):
                    registro = [
                        {"nombre": k, "materia": v.get("materia", ""), "fecha": v.get("fecha", "")}
                        for k, v in contenido.items()
                    ]
        except Exception:
            registro = []

    nombre_lower = nombre_archivo.lower()
    registro = [r for r in registro if r.get("nombre", "").lower() != nombre_lower]

    registro.append(
        {
            "nombre": nombre_archivo,
            "materia": materia,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(registro, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ No se pudo guardar el registro de material: {e}")


def guardar_resumen_obsidian(materia: str, tema: str, contenido: str, ruta_boveda: str) -> bool:
    """
    Crea un archivo .md dentro de la bóveda de Obsidian y un archivo índice central
    para asegurar que Obsidian genere la constelación (grafo de conexiones).
    """
    try:
        carpeta_materia = os.path.join(ruta_boveda, materia)
        os.makedirs(carpeta_materia, exist_ok=True)

        tema_sanitizado = (
            "".join(c if c.isalnum() or c in (" ", "_", "-") else "" for c in tema)
            .strip()
            .replace(" ", "_")
        )
        if not tema_sanitizado:
            tema_sanitizado = "resumen_sesion"

        nombre_archivo = f"{tema_sanitizado}.md"
        ruta_archivo = os.path.join(carpeta_materia, nombre_archivo)

        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        materia_sin_espacios = materia.lower().replace(" ", "_")

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
        contenido_final = (
            frontmatter
            + contenido
            + f"\n\n---\n*Nota generada por Sistema de Tutoría CLI.*\nConexión raíz: [[{materia}]]\n"
        )

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_final)

        ruta_indice = os.path.join(ruta_boveda, f"{materia}.md")
        link_tag = f"[[{tema_sanitizado}]]"

        if not os.path.exists(ruta_indice):
            with open(ruta_indice, "w", encoding="utf-8") as idx_file:
                idx_file.write(
                    f"---\nmateria: {materia}\ntipo: indice_asignatura\ntags: [{materia_sin_espacios}, indice]\n---\n# 📚 Asignatura: {materia}\n\n## 🕸️ Grafo de Constelación de Temas\n- {link_tag}\n"
                )
        else:
            with open(ruta_indice, "r", encoding="utf-8") as idx_file:
                idx_content = idx_file.read()
            if link_tag not in idx_content:
                with open(ruta_indice, "w", encoding="utf-8") as idx_file:
                    idx_file.write(idx_content + f"\n- {link_tag}")

        return True

    except Exception as e:
        print(f"❌ Error al guardar el resumen en Obsidian: {e}")
        return False
