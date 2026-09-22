import os
from typing import Dict


def pedir_datos_inicio() -> Dict[str, str]:
    """
    Solicita al usuario los datos requeridos por los prompts de IA:
    Materia/Tema, Nivel actual, Tiempo disponible, Objetivo final, 
    Nivel de profundidad y opcionalmente material de apoyo.
    """
    print("=" * 65)
    print(" 🎓 SISTEMA DE TUTORÍA PERSONALIZADO - CLI (ECUADOR) 🇪🇨")
    print("=" * 65)
    
    materia = input("📚 Ingresa la materia o tema principal a aprender: ").strip()
    while not materia:
        print("⚠️ Este campo no puede estar vacío.")
        materia = input("📚 Ingresa la materia o tema principal: ").strip()

    nivel_actual = input("🌱 Ingresa tu nivel actual (ej. Principiante absoluto / Con nociones básicas): ").strip()
    if not nivel_actual:
        nivel_actual = "Principiante absoluto"

    tiempo_disponible = input("⏱️ Tiempo disponible (ej. 10 horas a la semana durante 2 meses): ").strip()
    if not tiempo_disponible:
        tiempo_disponible = "Flexible"

    objetivo_final = input("🎯 Objetivo final real (ej. Aprobar examen / Crear un proyecto / Dominar bases): ").strip()
    if not objetivo_final:
        objetivo_final = "Dominar el tema"

    print("\n[Niveles de profundidad para las explicaciones]")
    print("  1. BÁSICO (Visión general, analogías)")
    print("  2. INTERMEDIO (Conceptos, funcionamiento lógico)")
    print("  3. AVANZADO (Arquitectura, rigor técnico profundo)")
    opcion_profundidad = input("👉 Elige el nivel de profundidad (1/2/3) [Por defecto: 2 Intermedio]: ").strip()
    
    niveles_map = {"1": "BÁSICO", "2": "INTERMEDIO", "3": "AVANZADO"}
    nivel_profundidad = niveles_map.get(opcion_profundidad, "INTERMEDIO")

    ruta_material = input("\n📄 (Opcional) Ruta del archivo de material de apoyo (.md) o presiona ENTER: ").strip()
    ruta_material = ruta_material.strip('"').strip("'")
    if ruta_material and not os.path.exists(ruta_material):
        print("⚠️ El archivo especificado no existe. Se continuará sin material de apoyo.")
        ruta_material = ""

    return {
        "materia": materia,
        "nivel_actual": nivel_actual,
        "tiempo_disponible": tiempo_disponible,
        "objetivo_final": objetivo_final,
        "nivel_profundidad": nivel_profundidad,
        "material": ruta_material
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
    respuesta = input("👉 Presiona ENTER si entendiste para pasar al siguiente tema, o escribe tu duda/pregunta: ").strip()
    return respuesta
