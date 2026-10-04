import json
import os
import time
import warnings
from typing import Any

import google.generativeai as genai
from dotenv import load_dotenv
from halo import Halo

from modules.core.ports.llm_base import LLMAdapterBase

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()


class LLM_GeminiAdapter(LLMAdapterBase):
    """Adaptador concreto para Google Gemini (gemini-3.5-flash-lite)."""

    def __init__(self):
        self.modelo_nombre = "gemini-3.5-flash-lite"
        self._configurar()

    def _configurar(self) -> genai.GenerativeModel:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "tu_api_key_de_google_gemini_aqui":
            raise ValueError(
                "Error crítico: Debes configurar tu GEMINI_API_KEY real en el archivo .env (actualmente tiene el valor por defecto o está vacía)."
            )
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(self.modelo_nombre)

    def generar_texto(
        self, prompt: str, contexto_previo: list[dict] | None = None, formato_json: bool = False
    ) -> str:
        try:
            model = self._configurar()
            max_reintentos = 3
            intento = 0
            gen_config = {"response_mime_type": "application/json"} if formato_json else None

            while intento < max_reintentos:
                try:
                    with Halo(text="Consultando a Gemini...", spinner="line"):
                        if contexto_previo:
                            chat = model.start_chat(history=contexto_previo)
                            response = chat.send_message(prompt, generation_config=gen_config)
                            return response.text
                        else:
                            response = model.generate_content(prompt, generation_config=gen_config)
                            return response.text
                except Exception as e:
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        intento += 1
                        tiempo_espera = 20 * intento
                        print(
                            f"⚠️ Límite de tasa (Rate Limit 429) alcanzado. Esperando {tiempo_espera}s..."
                        )
                        with Halo(
                            text=f"Esperando {tiempo_espera}s por Rate Limit...", spinner="line"
                        ):
                            time.sleep(tiempo_espera)
                    else:
                        raise e
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini.")
        except Exception as e:
            raise RuntimeError(f"Ocurrió un error al consultar la API de Google Gemini: {e}")

    def generar_texto_con_archivo(self, archivo_inline: dict, prompt: str) -> str:
        try:
            model = self._configurar()
            max_reintentos = 3
            intento = 0

            while intento < max_reintentos:
                try:
                    with Halo(text="Analizando documento con Gemini...", spinner="line"):
                        response = model.generate_content([archivo_inline, prompt])
                        return response.text
                except Exception as e:
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        intento += 1
                        tiempo_espera = 20 * intento
                        print(
                            f"⚠️ Límite de tasa (Rate Limit 429) alcanzado. Esperando {tiempo_espera}s..."
                        )
                        with Halo(
                            text=f"Esperando {tiempo_espera}s por Rate Limit...", spinner="line"
                        ):
                            time.sleep(tiempo_espera)
                    else:
                        raise e
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini.")
        except Exception as e:
            raise RuntimeError(f"Error al procesar archivo con Gemini: {e}")

    def generar_json_estructurado(self, prompt: str) -> dict[str, Any]:
        try:
            model = self._configurar()
            max_reintentos = 3
            intento = 0

            while intento < max_reintentos:
                try:
                    with Halo(text="Generando estructura JSON con Gemini...", spinner="line"):
                        response = model.generate_content(
                            prompt, generation_config={"response_mime_type": "application/json"}
                        )
                        return json.loads(response.text)
                except Exception as e:
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        intento += 1
                        tiempo_espera = 20 * intento
                        print(
                            f"⚠️ Límite de tasa (Rate Limit 429) alcanzado. Esperando {tiempo_espera}s..."
                        )
                        with Halo(
                            text=f"Esperando {tiempo_espera}s por Rate Limit...", spinner="line"
                        ):
                            time.sleep(tiempo_espera)
                    else:
                        raise e
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini.")
        except Exception as e:
            raise RuntimeError(f"Error al obtener JSON estructurado de Gemini: {e}")

    def generar_respuesta_stream(self, prompt: str, contexto_previo: list[dict] | None = None):
        try:
            model = self._configurar()
            max_reintentos = 3
            intento = 0

            while intento < max_reintentos:
                try:
                    if contexto_previo:
                        chat = model.start_chat(history=contexto_previo)
                        response = chat.send_message(prompt, stream=True)
                    else:
                        response = model.generate_content(prompt, stream=True)

                    for chunk in response:
                        if chunk.text:
                            yield chunk.text
                    return
                except Exception as e:
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        intento += 1
                        tiempo_espera = 20 * intento
                        print(
                            f"⚠️ Límite de tasa (Rate Limit 429) alcanzado. Esperando {tiempo_espera}s..."
                        )
                        with Halo(
                            text=f"Esperando {tiempo_espera}s por Rate Limit...", spinner="line"
                        ):
                            time.sleep(tiempo_espera)
                    else:
                        raise e
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini en streaming.")
        except Exception as e:
            raise RuntimeError(f"Error en streaming con la API de Google Gemini: {e}")


LLMGeminiAdapter = LLM_GeminiAdapter
