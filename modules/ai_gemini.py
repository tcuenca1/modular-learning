import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

import os
from typing import Optional, List
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


def configurar_ia() -> genai.GenerativeModel:
    """
    Configura y retorna el modelo de Google Gemini 'gemini-3.5-flash-lite' 
    utilizando la API key del entorno. Lanza ValueError si la clave no está configurada o es el placeholder.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "tu_api_key_de_google_gemini_aqui":
        raise ValueError(
            "Error crítico: Debes configurar tu GEMINI_API_KEY real en el archivo .env (actualmente tiene el valor por defecto o está vacía)."
        )
    
    genai.configure(api_key=api_key)
    # Usar el modelo Gemini 3.5 Flash Lite solicitado
    model = genai.GenerativeModel('gemini-3.5-flash-lite')
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
