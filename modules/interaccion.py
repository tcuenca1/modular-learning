import os
import re
from typing import Dict, List
import questionary
from modules import gestor_archivos


def seleccionar_con_flechas(opciones: List[str]) -> str:
    """
    Permite seleccionar una opción usando la librería multiplataforma questionary.
    """
    seleccion = questionary.select(
        "Selecciona una opción:",
        choices=opciones,
        style=questionary.Style([
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
            ('answer', 'fg:green bold'),
        ])
    ).ask()
    
    if seleccion is None:
        print("\n\n⚠️ Operación cancelada por el usuario.")
        exit(0)
        
    return seleccion


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
    Solicita al usuario los datos de inicio seleccionando la materia interactivamente,
    ofreciendo las próximas clases del cronograma JSON si existen, y pidiendo profundidad.
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

    # Obtener próximas clases pendientes del cronograma JSON si existe
    proximas_clases = gestor_archivos.obtener_proximas_clases(materia)
    tema = ""

    if proximas_clases:
        print("📅 Se encontraron clases pendientes en el cronograma de la asignatura:")
        opciones_clases = [f"📅 [{c.get('fecha', 'Sin fecha')}] {c.get('tema', 'Tema')}" for c in proximas_clases]
        opciones_clases.append("➕ Ingresar un tema manualmente")
        
        eleccion_clase = questionary.select(
            "Selecciona una clase pendiente o ingresa un tema manual:",
            choices=opciones_clases,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('answer', 'fg:green bold'),
            ])
        ).ask()

        if eleccion_clase and "➕" not in eleccion_clase:
            idx = opciones_clases.index(eleccion_clase)
            clase_seleccionada = proximas_clases[idx]
            tema = clase_seleccionada.get("tema", "")
            print(f"🎯 Tema seleccionado del cronograma: \033[1;93m{tema}\033[0m")

    if not tema:
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
