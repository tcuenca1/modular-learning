import os
import google.generativeai as genai
from modules.core.domain.ports.llm_port import LLMPort


class LLMGeminiAdapter(LLMPort):
    def __init__(self, api_key: str | None = None):
        # Asegurar obtención estricta de la clave API desde variables de entorno si no se provee
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "La clave API de Gemini (GEMINI_API_KEY) no está configurada en las variables de entorno."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error al generar respuesta con Gemini: {str(e)}")
