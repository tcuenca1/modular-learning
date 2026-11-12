"""Adaptador concreto para Google Gemini utilizando el SDK moderno google.genai."""

from __future__ import annotations

import json
import os
import re
import time
import warnings
from collections.abc import Callable
from typing import Any, TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import types

from modular_learning.core.ports.llm import LLMAdapterBase, LLMNoDisponible

warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

T = TypeVar("T")

# Fallos del servidor o de red que suelen desaparecer solos (503 «alta demanda», cortes de red…)
_PATRON_TRANSITORIO = re.compile(
    r"\b(500|502|503|504)\b|UNAVAILABLE|INTERNAL|DEADLINE_EXCEEDED|overloaded|"
    r"ConnectError|ReadTimeout|ConnectTimeout|RemoteProtocolError|ReadError|ConnectionReset",
    re.IGNORECASE,
)
# Segundos de espera antes de cada reintento de un fallo pasajero
ESPERAS_REINTENTO = (1.5, 3.0, 6.0)


class LLM_GeminiAdapter(LLMAdapterBase):
    """Adaptador concreto para Google Gemini desacoplado de dependencias de UI (sin spinners de consola)."""

    def __init__(self):
        self.modelo_nombre = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
        # Modelo al que pasar si el principal sigue saturado tras los reintentos (opcional)
        self.modelo_respaldo = os.getenv("GEMINI_MODELO_RESPALDO", "").strip()
        self._esperas = ESPERAS_REINTENTO
        # El cliente se crea en la primera llamada: sin clave la app arranca igual y solo
        # fallan las funciones que consultan a Gemini, con un mensaje claro
        self._cliente: genai.Client | None = None

    def _configurar(self) -> genai.Client:
        if self._cliente is not None:
            return self._cliente

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Falta la variable de entorno GEMINI_API_KEY en el archivo .env.")
        self._cliente = genai.Client(api_key=api_key)
        return self._cliente

    @staticmethod
    def _sanitizar_claves_json(dato: Any) -> Any:
        """Limpia saltos de línea, espacios y comillas residuales en las claves del JSON devuelto por el LLM."""
        if isinstance(dato, dict):
            limpio: dict[str, Any] = {}
            for k, v in dato.items():
                clave_limpia = str(k).strip().strip('"').strip("'").strip()
                limpio[clave_limpia] = LLM_GeminiAdapter._sanitizar_claves_json(v)
            return limpio
        if isinstance(dato, list):
            return [LLM_GeminiAdapter._sanitizar_claves_json(item) for item in dato]
        return dato

    @staticmethod
    def _parsear_json(texto: str) -> Any:
        """Extrae el primer JSON válido (objeto o arreglo) de la respuesta del modelo sanitizando claves."""
        limpio = texto.strip()

        # Limpiar bloques de código markdown si están presentes
        if "```json" in limpio:
            partes = limpio.split("```json")
            if len(partes) > 1:
                limpio = partes[1].split("```")[0]
        elif "```" in limpio:
            partes = limpio.split("```")
            if len(partes) > 1:
                limpio = partes[1].split("```")[0]

        limpio = limpio.strip()

        try:
            objeto = json.loads(limpio)
            return LLM_GeminiAdapter._sanitizar_claves_json(objeto)
        except json.JSONDecodeError:
            pass

        decoder = json.JSONDecoder()
        for i, caracter in enumerate(limpio):
            if caracter in "[{":
                try:
                    objeto, _ = decoder.raw_decode(limpio[i:])
                    return LLM_GeminiAdapter._sanitizar_claves_json(objeto)
                except json.JSONDecodeError:
                    continue

        raise json.JSONDecodeError("La respuesta no contiene JSON válido", limpio, 0)

    def _normalizar_historial(self, contexto_previo: list[Any] | None) -> list[types.Content]:
        """Convierte historiales en formato diccionario estándar a objetos types.Content de google.genai."""
        if not contexto_previo:
            return []
        historial_normalizado: list[types.Content] = []
        for item in contexto_previo:
            if isinstance(item, types.Content):
                historial_normalizado.append(item)
            elif isinstance(item, dict):
                rol = item.get("role", "user")
                partes_raw = item.get("parts", [])
                if not partes_raw and "content" in item:
                    content_val = item["content"]
                    partes_raw = [content_val] if isinstance(content_val, str) else content_val

                partes: list[types.Part] = []
                for p in partes_raw:
                    if isinstance(p, types.Part):
                        partes.append(p)
                    elif isinstance(p, str):
                        partes.append(types.Part.from_text(text=p))
                    elif isinstance(p, dict):
                        if "text" in p:
                            partes.append(types.Part.from_text(text=p["text"]))
                        else:
                            partes.append(types.Part(**p))
                    else:
                        partes.append(types.Part.from_text(text=str(p)))
                historial_normalizado.append(types.Content(role=rol, parts=partes))
        return historial_normalizado

    # ------------------------------------------------------------------ reintentos
    def _modelos(self) -> list[str]:
        """El modelo principal y, si está configurado (GEMINI_MODELO_RESPALDO), uno de respaldo."""
        modelos = [self.modelo_nombre]
        if self.modelo_respaldo and self.modelo_respaldo != self.modelo_nombre:
            modelos.append(self.modelo_respaldo)
        return modelos

    @staticmethod
    def _es_limite(e: Exception) -> bool:
        return "429" in str(e) or "ResourceExhausted" in str(e) or "RESOURCE_EXHAUSTED" in str(e)

    @staticmethod
    def _es_transitorio(e: Exception) -> bool:
        """Errores del servidor o de red que suelen desaparecer solos (p. ej. 503 «alta demanda»)."""
        texto = f"{type(e).__name__} {e}"
        return bool(_PATRON_TRANSITORIO.search(texto))

    def _llamar(self, operacion: Callable[[str], T]) -> T:
        """
        Ejecuta `operacion(modelo)` reintentando los fallos pasajeros con espera creciente y, si
        siguen, con el modelo de respaldo. Un error que no es pasajero (clave inválida, petición
        rechazada) se propaga de inmediato; si se agotan los reintentos, LLMNoDisponible.
        """
        ultimo: Exception | None = None
        for modelo in self._modelos():
            transitorios = limites = 0
            while True:
                try:
                    return operacion(modelo)
                except Exception as e:
                    if self._es_limite(e) and limites < 3:
                        limites += 1
                        print(f"⚠️ Límite de tasa (429). Esperando {20 * limites}s…")
                        time.sleep(20 * limites)
                    elif self._es_transitorio(e) and transitorios < len(self._esperas):
                        time.sleep(self._esperas[transitorios])
                        transitorios += 1
                    elif self._es_limite(e) or self._es_transitorio(e):
                        ultimo = e
                        break  # prueba con el modelo de respaldo, si hay
                    else:
                        raise
        raise LLMNoDisponible() from ultimo

    # ------------------------------------------------------------------ generación
    def generar_texto(
        self, prompt: str, contexto_previo: list[dict] | None = None, formato_json: bool = False
    ) -> str:
        config = (
            types.GenerateContentConfig(response_mime_type="application/json")
            if formato_json
            else None
        )

        def operacion(modelo: str) -> str:
            client = self._configurar()
            if contexto_previo:
                historial = self._normalizar_historial(contexto_previo)
                chat = client.chats.create(model=modelo, history=historial)
                return chat.send_message(prompt, config=config).text
            return client.models.generate_content(model=modelo, contents=prompt, config=config).text

        try:
            return self._llamar(operacion)
        except LLMNoDisponible:
            raise
        except Exception as e:
            raise RuntimeError(f"Ocurrió un error al consultar la API de Google Gemini: {e}") from e

    def generar_texto_con_archivo(self, archivo_inline: dict, prompt: str) -> str:
        def operacion(modelo: str) -> str:
            client = self._configurar()
            mime = archivo_inline.get("mime_type", "application/pdf")
            ruta = archivo_inline.get("path")
            file_bytes = archivo_inline.get("data")
            if file_bytes is None and ruta:
                with open(ruta, "rb") as f:
                    file_bytes = f.read()
            file_bytes = file_bytes or b""

            if ruta and os.path.exists(ruta) and len(file_bytes) > 4_000_000:
                contents = [client.files.upload(file=ruta), prompt]
            else:
                contents = [types.Part.from_bytes(data=file_bytes, mime_type=mime), prompt]
            return client.models.generate_content(model=modelo, contents=contents).text

        try:
            return self._llamar(operacion)
        except LLMNoDisponible:
            raise
        except Exception as e:
            raise RuntimeError(f"Error al procesar archivo con Gemini: {e}") from e

    def generar_json_estructurado(self, prompt: str) -> dict[str, Any]:
        config = types.GenerateContentConfig(response_mime_type="application/json")

        def operacion(modelo: str) -> Any:
            client = self._configurar()
            response = client.models.generate_content(model=modelo, contents=prompt, config=config)
            return self._parsear_json(response.text)

        try:
            return self._llamar(operacion)
        except LLMNoDisponible:
            raise
        except Exception as e:
            raise RuntimeError(f"Error al obtener JSON estructurado de Gemini: {e}") from e

    def generar_respuesta_stream(self, prompt: str, contexto_previo: list[dict] | None = None):
        """
        Texto en streaming. Si Gemini falla ANTES de emitir nada se reintenta con espera creciente
        (y con el modelo de respaldo); si falla a mitad no se puede reintentar sin repetir texto,
        así que se avisa con LLMNoDisponible para que la interfaz ofrezca reintentar el paso.
        """
        try:
            client = self._configurar()
        except Exception as e:
            raise RuntimeError(f"Error en streaming con la API de Google Gemini: {e}") from e

        ultimo: Exception | None = None
        for modelo in self._modelos():
            transitorios = limites = 0
            while True:
                emitido = False
                try:
                    if contexto_previo:
                        historial = self._normalizar_historial(contexto_previo)
                        chat = client.chats.create(model=modelo, history=historial)
                        respuesta = chat.send_message_stream(prompt)
                    else:
                        respuesta = client.models.generate_content_stream(
                            model=modelo, contents=prompt
                        )
                    for chunk in respuesta:
                        if chunk.text:
                            emitido = True
                            yield chunk.text
                    return
                except Exception as e:
                    recuperable = self._es_limite(e) or self._es_transitorio(e)
                    if not recuperable:
                        raise RuntimeError(
                            f"Error en streaming con la API de Google Gemini: {e}"
                        ) from e
                    if emitido:
                        raise LLMNoDisponible(
                            "La explicación se interrumpió porque el servicio de IA falló. "
                            "Pulsa «Reintentar» para generarla de nuevo."
                        ) from e
                    if self._es_limite(e) and limites < 3:
                        limites += 1
                        time.sleep(20 * limites)
                    elif not self._es_limite(e) and transitorios < len(self._esperas):
                        time.sleep(self._esperas[transitorios])
                        transitorios += 1
                    else:
                        ultimo = e
                        break
        raise LLMNoDisponible() from ultimo


LLMGeminiAdapter = LLM_GeminiAdapter

__all__ = ["LLMGeminiAdapter", "LLM_GeminiAdapter"]
