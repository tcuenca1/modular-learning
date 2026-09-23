import os
import sys
import msvcrt
import re
from typing import Dict, List
from modules import gestor_archivos


def seleccionar_con_flechas(opciones: List[str]) -> str:
    """
    Permite seleccionar una opción usando las teclas de flecha Arriba/Abajo y Enter en la terminal (Windows).
    """
    os.system('')  # Activar secuencias ANSI en Windows
    idx = 0
    n = len(opciones)
    
    print("Usa las flechas [↑] [↓] para moverte y [ENTER] para seleccionar:")
    # Imprimir por primera vez
    for i, op in enumerate(opciones):
        if i == idx:
            sys.stdout.write(f"  > \033[1;96m{op}\033[0m\n")
        else:
            sys.stdout.write(f"    {op}\n")
    sys.stdout.flush()

    while True:
        key = msvcrt.getch()
        if key == b'\xe0':  # Tecla especial
            sub_key = msvcrt.getch()
            # Borrar las n líneas anteriores
            sys.stdout.write(f"\033[{n}A")
            if sub_key == b'H':  # Arriba
                idx = (idx - 1) % n
            elif sub_key == b'P':  # Abajo
                idx = (idx + 1) % n
            
            # Redibujar menú
            for i, op in enumerate(opciones):
                sys.stdout.write("\033[K")
                if i == idx:
                    sys.stdout.write(f"  > \033[1;96m{op}\033[0m\n")
                else:
                    sys.stdout.write(f"    {op}\n")
            sys.stdout.flush()
        elif key == b'\r':  # Enter
            # Borrar menú para dejar limpia la selección
            sys.stdout.write(f"\033[{n}A")
            for _ in range(n):
                sys.stdout.write("\033[K\n")
            sys.stdout.write(f"\033[{n}A")
            sys.stdout.flush()
            return opciones[idx]


def imprimir_markdown_bonito(texto: str) -> None:
    """Formatea texto Markdown con colores y estilos atractivos para la consola."""
    os.system('')
    lineas = texto.split('\n')
    for linea in lineas:
        if linea.startswith('# '):
            print(f"\n\033[1;95m{linea[2:].upper()}\033[0m")
        elif linea.startswith('## '):
            print(f"\n\033[1;94m{linea[3:]}\033[0m")
        elif linea.startswith('### '):
            print(f"\n\033[1;96m  🔹 {linea[4:]}\033[0m")
        elif linea.startswith('- ') or linea.startswith('* '):
            linea_fmt = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', linea[2:])
            print(f"    • {linea_fmt}")
        else:
            linea_fmt = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', linea)
            print(f"    {linea_fmt}")
    print()


def pedir_datos_inicio() -> Dict[str, str]:
    """
    Solicita al usuario los datos de inicio seleccionando la materia interactivamente con flechas
    y pidiendo el tema de estudio.
    """
    print("=" * 65)
    print(" 🎓 SISTEMA DE TUTORÍA PERSONALIZADO - CLI (ECUADOR) 🇪🇨")
    print("=" * 65)
    
    materias = gestor_archivos.cargar_materias()
    opciones_menu = materias + ["[ + ] Añadir nueva asignatura..."]
    
    print("\n📚 Selecciona la asignatura para la sesión de hoy:")
    seleccion = seleccionar_con_flechas(opciones_menu)
    
    if "[ + ]" in seleccion:
        nueva_mat = input("\n✍️ Ingresa el nombre de la nueva asignatura: ").strip()
        while not nueva_mat:
            print("⚠️ El nombre no puede estar vacío.")
            nueva_mat = input("✍️ Ingresa el nombre de la nueva asignatura: ").strip()
        gestor_archivos.agregar_materia(nueva_mat)
        materia = nueva_mat
    else:
        materia = seleccion

    print(f"✅ Asignatura seleccionada: \033[1;92m{materia}\033[0m\n")

    tema = input("🎯 Ingresa el tema específico que deseas estudiar hoy: ").strip()
    while not tema:
        print("⚠️ El tema no puede estar vacío.")
        tema = input("🎯 Ingresa el tema específico que deseas estudiar hoy: ").strip()

    print("\n[Nivel de profundidad para las explicaciones]")
    print("  1. BÁSICO (Visión general, analogías)")
    print("  2. INTERMEDIO (Conceptos, funcionamiento lógico)")
    print("  3. AVANZADO (Arquitectura, rigor técnico profundo)")
    opcion_profundidad = input("👉 Elige el nivel de profundidad (1/2/3) [Por defecto: 2 Intermedio]: ").strip()
    
    niveles_map = {"1": "BÁSICO", "2": "INTERMEDIO", "3": "AVANZADO"}
    nivel_profundidad = niveles_map.get(opcion_profundidad, "INTERMEDIO")

    return {
        "materia": materia,
        "tema": tema,
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
        imprimir_markdown_bonito(mensaje)
        print("=" * 63 + "\n")
    else:
        print(f"• {mensaje}")


def pausa_estudio() -> str:
    """Pausa el flujo para comprobar comprensión o plantear dudas."""
    print("-" * 65)
    respuesta = input("👉 Presiona ENTER si entendiste para pasar al siguiente paso, o escribe tu duda/pregunta: ").strip()
    return respuesta
