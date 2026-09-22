import os
from typing import Dict


def pedir_datos_inicio() -> Dict[str, str]:
    """
    Solicita al usuario los datos iniciales de la sesión de tutoría:
    Materia, Tema de hoy, y opcionalmente la ruta del material de apoyo (.md).
    Retorna un diccionario con estos datos.
    """
    print("=" * 65)
    print(" 🎓 SISTEMA DE TUTORÍA PERSONALIZADO - CLI (ECUADOR) 🇪🇨")
    print("=" * 65)
    
    materia = input("📚 Ingresa la materia (ej. Cálculo II, Estructura de Datos): ").strip()
    while not materia:
        print("⚠️ La materia no puede estar vacía.")
        materia = input("📚 Ingresa la materia: ").strip()

    tema = input("🎯 Ingresa el tema de hoy: ").strip()
    while not tema:
        print("⚠️ El tema no puede estar vacío.")
        tema = input("🎯 Ingresa el tema de hoy: ").strip()

    ruta_material = input("📄 (Opcional) Ingresa la ruta del archivo de material de apoyo (.md) o presiona ENTER: ").strip()
    # Limpiar comillas si se arrastró el archivo
    ruta_material = ruta_material.strip('"').strip("'")
    if ruta_material and not os.path.exists(ruta_material):
        print("⚠️ El archivo especificado no existe. Se continuará sin material de apoyo.")
        ruta_material = ""

    return {
        "materia": materia,
        "tema": tema,
        "material": ruta_material
    }


def mostrar_mensaje(mensaje: str, tipo: str = "info") -> None:
    """
    Muestra mensajes en consola con formato y colores básicos según el tipo.
    Tipos soportados: 'info', 'exito', 'error', 'ia'.
    """
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
    """
    Pausa el flujo de estudio tras mostrar una explicación.
    Muestra el input para que el usuario confirme avance o escriba una duda.
    Retorna la respuesta del usuario (vacío si dio ENTER).
    """
    print("-" * 65)
    respuesta = input("👉 Presiona ENTER si entendiste para pasar al siguiente tema, o escribe tu duda/pregunta: ").strip()
    return respuesta
