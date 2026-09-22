import os
from typing import Optional, List
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


def configurar_ia() -> genai.GenerativeModel:
    """
    Configura y retorna el modelo de Google Gemini utilizando la API key del entorno.
    Lanza ValueError si la clave no está configurada.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Error crítico: No se encontró la variable 'GEMINI_API_KEY' en el archivo .env."
        )
    
    genai.configure(api_key=api_key)
    # Inicializar el modelo recomendado para texto y contexto largo
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model


def consultar_gemini(prompt: str, contexto_previo: Optional[List[dict]] = None) -> str:
    """
    Envía un prompt a la API de Gemini y retorna la respuesta generada en texto.
    Permite mantener un historial de conversación si se provee contexto_previo.
    """
    try:
        model = configurar_ia()
        
        if contexto_previo:
            # Iniciar una sesión de chat con el historial previo provisto
            chat = model.start_chat(history=contexto_previo)
            response = chat.send_message(prompt)
            return response.text
        else:
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        raise RuntimeError(f"Ocurrió un error al consultar la API de Google Gemini: {e}")


def leer_archivo_texto(ruta_archivo: str) -> str:
    """
    Lee y retorna el contenido de texto plano de un archivo (ideal para cargar prompts o plantillas).
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo especificado no se encontró en la ruta: {ruta_archivo}")
    except Exception as e:
        raise IOError(f"Error al leer el archivo {ruta_archivo}: {e}")
