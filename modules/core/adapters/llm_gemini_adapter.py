import os
import subprocess
from typing import Optional


class LLMGeminiAdapter:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No se ha proporcionado la API Key de Gemini y no está presente en las variables de entorno."
            )

    def ejecutar_comando(self, comando: list[str]) -> str:
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
            return resultado.stdout
        except subprocess.CalledProcessError as e:
            # Manejo seguro y controlado del error sin filtrar información sensible del sistema
            raise RuntimeError(
                f"Error en la ejecución del proceso externo (código {e.returncode})."
            ) from e
        except (ValueError, OSError) as e:
            raise RuntimeError("Error inesperado al intentar ejecutar el comando.") from e
