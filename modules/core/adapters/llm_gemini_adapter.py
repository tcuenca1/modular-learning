import json
import os
import time
import warnings
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from halo import Halo

from modules.core.ports.llm_base import LLMAdapterBase

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()


class LLM_GeminiAdapter(LLMAdapterBase):
    """Adaptador concreto para Google Gemini utilizando el SDK moderno `google.genai`."""

    def __init__(self):
        self.modelo_nombre = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
        self._cliente: genai.Client | None = None
        self._configurar()

    def _configurar(self) -> genai.Client:
        if self._cliente is not None:
            return self._cliente

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable de entorno GEMINI_API_KEY en el archivo .env.")
        self._cliente = genai.Client(api_key=api_key)
        return self._cliente

    def generar_texto(
        self, prompt: str, contexto_previo: list[dict] | None = None, formato_json: bool = False
    ) -> str:
        try:
            client = self._configurar()
            max_reintentos = 3
            intento = 0

            config = (
                types.GenerateContentConfig(response_mime_type="application/json")
                if formato_json
                else None
            )

            while intento < max_reintentos:
                try:
                    with Halo(text="Consultando a Gemini...", spinner="line"):
                        if contexto_previo:
                            chat = client.chats.create(
                                model=self.modelo_nombre, history=contexto_previo
                            )
                            response = chat.send_message(prompt, config=config)
                            return response.text
                        else:
                            response = client.models.generate_content(
                                model=self.modelo_nombre, contents=prompt, config=config
                            )
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
                        raise
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini.")
        except Exception as e:
            raise RuntimeError(f"Ocurrió un error al consultar la API de Google Gemini: {e}")

    def generar_texto_con_archivo(self, archivo_inline: dict, prompt: str) -> str:
        try:
            client = self._configurar()
            max_reintentos = 3
            intento = 0

            while intento < max_reintentos:
                try:
                    with Halo(text="Analizando documento con Gemini...", spinner="line"):
                        mime = archivo_inline.get("mime_type", "application/pdf")
                        file_bytes = archivo_inline.get("data", b"")
                        ruta = archivo_inline.get("path")

                        if ruta and os.path.exists(ruta) and len(file_bytes) > 4_000_000:
                            uploaded_file = client.files.upload(file=ruta)
                            contents = [uploaded_file, prompt]
                        else:
                            parte_archivo = types.Part.from_bytes(data=file_bytes, mime_type=mime)
                            contents = [parte_archivo, prompt]

                        response = client.models.generate_content(
                            model=self.modelo_nombre, contents=contents
                        )
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
                        raise
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini.")
        except Exception as e:
            raise RuntimeError(f"Error al procesar archivo con Gemini: {e}")

    def generar_json_estructurado(self, prompt: str) -> dict[str, Any]:
        try:
            client = self._configurar()
            max_reintentos = 3
            intento = 0

            config = types.GenerateContentConfig(response_mime_type="application/json")

            while intento < max_reintentos:
                try:
                    with Halo(text="Generando estructura JSON con Gemini...", spinner="line"):
                        response = client.models.generate_content(
                            model=self.modelo_nombre, contents=prompt, config=config
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
                        raise
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini.")
        except Exception as e:
            raise RuntimeError(f"Error al obtener JSON estructurado de Gemini: {e}")

    def generar_respuesta_stream(self, prompt: str, contexto_previo: list[dict] | None = None):
        try:
            client = self._configurar()
            max_reintentos = 3
            intento = 0

            while intento < max_reintentos:
                try:
                    if contexto_previo:
                        chat = client.chats.create(
                            model=self.modelo_nombre, history=contexto_previo
                        )
                        response = chat.send_message_stream(prompt)
                    else:
                        response = client.models.generate_content_stream(
                            model=self.modelo_nombre, contents=prompt
                        )

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
                        raise
            raise RuntimeError("Se agotaron los reintentos por Rate Limit con Gemini en streaming.")
        except Exception as e:
            raise RuntimeError(f"Error en streaming con la API de Google Gemini: {e}")


LLMGeminiAdapter = LLM_GeminiAdapter
