import os
from typing import Dict


def pedir_datos_inicio() -> Dict[str, str]:
    """
    Solicita al usuario los datos requeridos por el prompt 01_roadmap_aprendizaje.md:
    Materia, Tipo de contenido, Contenido o texto de entrada, Objetivo de hoy, 
    y el nivel de profundidad para las explicaciones.
    """
    print("=" * 65)
    print(" 🎓 SISTEMA DE TUTORÍA PERSONALIZADO - CLI (ECUADOR) 🇪🇨")
    print("=" * 65)
    
    materia = input("📚 Ingresa la materia o asignatura: ").strip()
    while not materia:
        print("⚠️ La materia no puede estar vacía.")
        materia = input("📚 Ingresa la materia o asignatura: ").strip()

    tipo_contenido = input("📋 Tipo de contenido (ej. Texto de lectura / Instrucciones de tarea): ").strip()
    if not tipo_contenido:
        tipo_contenido = "Texto de lectura"

    print("📄 Introduce el contenido, apuntes o descripción de la actividad (o presiona ENTER para cargar desde archivo):")
    contenido_entrada = input("👉 Contenido de entrada: ").strip()
    
    ruta_material = ""
    if not contenido_entrada:
        ruta_material = input("📁 Ingresa la ruta del archivo de material de apoyo (.md): ").strip()
        ruta_material = ruta_material.strip('"').strip("'")
        if ruta_material and not os.path.exists(ruta_material):
            print("⚠️ Archivo no encontrado. Se solicitará texto por defecto.")
            ruta_material = ""

    objetivo_hoy = input("🎯 ¿Cuál es tu objetivo hoy? (ej. Entender el concepto / Resolver la actividad): ").strip()
    if not objetivo_hoy:
        objetivo_hoy = "Entender el concepto y practicar"

    print("\n[Nivel de profundidad para las explicaciones]")
    print("  1. BÁSICO (Visión general, analogías)")
    print("  2. INTERMEDIO (Conceptos, funcionamiento lógico)")
    print("  3. AVANZADO (Arquitectura, rigor técnico profundo)")
    opcion_profundidad = input("👉 Elige el nivel de profundidad (1/2/3) [Por defecto: 2 Intermedio]: ").strip()
    
    niveles_map = {"1": "BÁSICO", "2": "INTERMEDIO", "3": "AVANZADO"}
    nivel_profundidad = niveles_map.get(opcion_profundidad, "INTERMEDIO")

    return {
        "materia": materia,
        "tipo_contenido": tipo_contenido,
        "contenido_entrada": contenido_entrada,
        "ruta_material": ruta_material,
        "objetivo_hoy": objetivo_hoy,
        "nivel_profundidad": nivel_profundidad
    }


def mostrar_mensaje(mensaje: str, tipo: str = "info") -> None:
    """Muestra mensajes en consola con formato según el tipo."""
    if tipo == "info":
        print(f"ℹ️ [INFO]: {mensaje}")
    elif tipo == "exito":
        print(f"✅ [ÉXITO]: {mensaje}")
    elif tipo == "error":
        print(f"❌ [ERROR]: {mensaje}")
    elif tipo == "ia":
        print("\n" + "🤖" + "=" * 60)
        print(" [TUTOR IA]:")
        print("=" * 61)
        print(f"{mensaje}\n")
        print("=" * 63 + "\n")
    else:
        print(f"• {mensaje}")


def pausa_estudio() -> str:
    """Pausa el flujo para comprobar comprensión o plantear dudas."""
    print("-" * 65)
    respuesta = input("👉 Presiona ENTER si entendiste para pasar al siguiente paso, o escribe tu duda/pregunta: ").strip()
    return respuesta
