import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path para ejecución global correcta
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def app():
    """Enrutador principal CLI para Modular Learning CLI (ml)."""
    if len(sys.argv) < 2:
        mostrar_ayuda()
        return

    comando = sys.argv[1].lower()
    args_restantes = sys.argv[2:]
    
    if comando == "init":
        from main import main as run_main
        run_main()
    elif comando == "es":
        from tools import extraer_silabo
        sys.argv = [sys.argv[0]] + args_restantes
        extraer_silabo.run()
    elif comando == "im":
        from tools import ingestar_material
        sys.argv = [sys.argv[0]] + args_restantes
        ingestar_material.run()
    elif comando in ["help", "--help", "-h"]:
        mostrar_ayuda()
    else:
        print(f"❌ Comando desconocido: '{comando}'\n")
        mostrar_ayuda()
        sys.exit(1)

def mostrar_ayuda():
    """Imprime un panel de ayuda estilizado con las opciones disponibles."""
    print("=" * 65)
    print(" [EDU] MODULAR LEARNING CLI (ml) - PANEL DE AYUDA")
    print("=" * 65)
    print(" Comandos disponibles:")
    print("   ml init    -> Inicia la sesión de tutoría interactiva personalizada.")
    print("   ml es      -> Extraer cronogramas de sílabos (archivos o carpetas).")
    print("   ml im      -> Ingestar material de estudio multimodal hacia Obsidian.")
    print("   ml --help  -> Muestra este panel de ayuda.")
    print("=" * 65)

if __name__ == "__main__":
    app()
