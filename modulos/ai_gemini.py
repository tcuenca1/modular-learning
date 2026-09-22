import os
import warnings
from typing import Optional, List
from dotenv import load_dotenv
import google.generativeai as genai

# Suprimir FutureWarning del paquete deprecado google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)

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
            chat = model.start_chat(history=contexto_previo)
            response = chat.send_message(prompt)
            return response.text
        else:
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        raise RuntimeError(f"Ocurrió un error al consultar la API de Google Gemini: {e}")
