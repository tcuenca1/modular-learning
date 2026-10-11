import os
import subprocess


def ejecutar_comando(comando: list[str]) -> str | None:
    """
    Ejecuta un comando de forma segura utilizando subprocess,
    incluyendo check=True y manejo de excepciones específicas.
    """
    try:
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        # Manejo seguro del error sin silenciarlo totalmente ni exponer secretos
        print(f"Error al ejecutar el comando: {e}")
        return None


def obtener_api_key() -> str:
    """
    Obtiene la API key exclusivamente de las variables de entorno,
    evitando credenciales hardcodeadas.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno GEMINI_API_KEY no está configurada.")
    return api_key
