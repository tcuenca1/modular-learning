"""Adaptador práctico para IoT y Node-RED con análisis granular de flujos."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from modular_learning.core.ports.plugin_practico import PluginMetadatos, PluginPracticoBase
from modular_learning.infrastructure.persistence.almacen import DocumentoJson


def extraer_resumen_funcion_js(codigo: str) -> str:
    """Extrae comentarios o una descripción de una función JavaScript de Node-RED."""
    lineas = codigo.splitlines()
    for linea in lineas[:5]:
        l = linea.strip()
        if l.startswith(("//", "/*")):
            limpio = re.sub(r"^[/\\*]+", "", l).strip()
            if limpio:
                return limpio[:60]
    # Si no hay comentarios, mostrar primeras operaciones
    for linea in lineas[:3]:
        l = linea.strip()
        if l and not l.startswith("//"):
            return l[:60]
    return "procesamiento de payload"


METADATOS = PluginMetadatos(
    id="nodered",
    nombre="Node-RED",
    opcion_key="Node-RED (Flujos JSON)",
    categoria="Internet de las Cosas",
    descripcion=(
        "Lee tus flujos JSON por pestañas: nodos, tópicos MQTT, sensores y endpoints HTTP."
    ),
    materia_defecto="internet-de-las-cosas",
    claves_seleccion=("node-red", "nodered"),
    tipos_archivo=("iot", "nodered"),
    palabras_clave=("iot", "internet", "node", "red"),
    carpeta_convencional="Internet de las Cosas",
    extension_archivos=".json",
    etiqueta="Node-RED",
    texto_sin_contexto="Sin flujos registrados.",
    orden_sincronizacion=0,
)


class NodeRedPlugin(PluginPracticoBase):
    """Adaptador práctico para IoT y Node-RED."""

    @property
    def metadatos(self) -> PluginMetadatos:
        return METADATOS

    def analizar_archivo(self, ruta_archivo: str) -> str | None:
        return self.analizar_flujo(ruta_archivo)

    def __init__(self, memoria: DocumentoJson | None = None):
        self._memoria = memoria or DocumentoJson("plugins/nodered_memoria.json")

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        metadatos = metadatos.strip()
        if not metadatos:
            return

        historial = self._memoria.leer([])
        if not isinstance(historial, list):
            historial = []

        historial.append(metadatos)
        historial = historial[-5:]

        try:
            self._memoria.escribir(historial, sangria=4)
        except Exception as e:
            print(f"⚠️ No se pudo guardar la memoria del plugin Node-RED: {e}")

    def cargar_contexto_reciente(self) -> str:
        try:
            historial = self._memoria.leer([])
        except Exception:
            return ""
        if isinstance(historial, list) and historial:
            return "\n\n".join(historial)
        return ""

    def analizar_flujo(self, ruta_archivo: str) -> str:
        """
        Recibe la ruta del archivo JSON de un flujo IoT (Node-RED), lo parsea de forma granular
        organizado por pestañas/flujos, extrae nodos, sensores, tópicos MQTT, endpoints HTTP y funciones.
        """
        if not os.path.exists(ruta_archivo):
            return f"⚠️ Error: El archivo de flujo no existe: {ruta_archivo}"

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return f"⚠️ Error: El archivo JSON no es un flujo válido de Node-RED: {e}"
        except Exception as e:
            return f"⚠️ Error al leer el archivo de flujo: {e}"

        nodos: list[dict[str, Any]] = []
        if isinstance(data, list):
            nodos = [n for n in data if isinstance(n, dict)]
        elif isinstance(data, dict):
            if "flows" in data and isinstance(data["flows"], list):
                nodos = [n for n in data["flows"] if isinstance(n, dict)]
            elif "nodes" in data and isinstance(data["nodes"], list):
                nodos = [n for n in data["nodes"] if isinstance(n, dict)]
            else:
                nodos = [data]

        total_nodos = len(nodos)
        if not total_nodos:
            return f"⚠️ El archivo `{os.path.basename(ruta_archivo)}` no contiene nodos de Node-RED."

        # Identificar pestañas (tabs) y subflujos
        pestanas: dict[str, str] = {}
        for n in nodos:
            if n.get("type") == "tab":
                pestanas[n.get("id", "")] = n.get("label") or "Pestaña sin título"

        # Agrupar nodos por pestaña (clave z)
        nodos_por_pestana: dict[str, list[dict[str, Any]]] = {}
        for n in nodos:
            if n.get("type") == "tab":
                continue
            z = n.get("z", "")
            nombre_pestana = pestanas.get(z, "Flujo Principal / General")
            if nombre_pestana not in nodos_por_pestana:
                nodos_por_pestana[nombre_pestana] = []
            nodos_por_pestana[nombre_pestana].append(n)

        lineas: list[str] = [
            "### 🔌 Análisis de Flujo IoT / Node-RED",
            f"- **Archivo fuente:** `{ruta_archivo}`",
            f"- **Total de nodos en el lienzo:** {total_nodos}",
            f"- **Pestañas / flujos activos:** {len(nodos_por_pestana)}",
        ]

        for nombre_tab, nodos_tab in nodos_por_pestana.items():
            lineas.append(f"\n#### 📑 Flujo: «{nombre_tab}» ({len(nodos_tab)} nodos)")

            mqtt_in: list[str] = []
            mqtt_out: list[str] = []
            http_endpoints: list[str] = []
            funciones: list[str] = []
            sensores: list[str] = []
            dashboard: list[str] = []
            tipos_cont: dict[str, int] = {}

            for nodo in nodos_tab:
                tipo = nodo.get("type", "desconocido")
                tipos_cont[tipo] = tipos_cont.get(tipo, 0) + 1
                nombre = nodo.get("name", "")
                topic = nodo.get("topic", "")

                if tipo == "mqtt in" and topic:
                    mqtt_in.append(f"`{topic}` ({nombre or 'sin nombre'})")
                elif tipo == "mqtt out" and topic:
                    mqtt_out.append(f"`{topic}` ({nombre or 'sin nombre'})")
                elif tipo in ["http in", "http out", "http response"]:
                    url = nodo.get("url")
                    method = nodo.get("method", "GET").upper()
                    if url:
                        http_endpoints.append(f"`{method} {url}`")
                elif tipo == "function":
                    func_body = nodo.get("func", "")
                    resumen_func = extraer_resumen_funcion_js(func_body)
                    funciones.append(f"«{nombre or 'Función sin nombre'}»: {resumen_func}")
                elif tipo.startswith("ui_"):
                    widget = tipo.replace("ui_", "").capitalize()
                    dashboard.append(f"{widget} ({nombre or 'sin nombre'})")
                elif any(
                    kw in tipo.lower() or kw in nombre.lower()
                    for kw in [
                        "sensor",
                        "dht",
                        "esp32",
                        "arduino",
                        "temperatura",
                        "humedad",
                        "inject",
                    ]
                ):
                    sensores.append(f"[{tipo}] '{nombre or 'Sensor/Generador'}'")

            if mqtt_in:
                lineas.append(f"- **MQTT Subscripción (In):** {', '.join(mqtt_in)}")
            if mqtt_out:
                lineas.append(f"- **MQTT Publicación (Out):** {', '.join(mqtt_out)}")
            if http_endpoints:
                lineas.append(f"- **Endpoints HTTP:** {', '.join(http_endpoints)}")
            if funciones:
                lineas.append("- **Nodos de Función (Lógica JS):**")
                for fn in funciones[:4]:
                    lineas.append(f"  - {fn}")
            if dashboard:
                lineas.append(f"- **Panel Dashboard:** {', '.join(dashboard[:6])}")
            if sensores:
                lineas.append(f"- **Entradas/Sensores detectados:** {', '.join(sensores[:5])}")

            if tipos_cont:
                lineas.append(
                    f"- **Tipos de nodos en el flujo:** {', '.join(f'{t} ({c})' for t, c in tipos_cont.items())}"
                )

        texto_procesado = "\n".join(lineas)
        self.guardar_contexto_extraido(texto_procesado)
        return texto_procesado

    def analizar_carpeta(self, ruta_carpeta: str) -> str:
        """
        Escanea una carpeta en busca de flujos JSON de Node-RED y los analiza.
        """
        if not os.path.isdir(ruta_carpeta):
            return f"⚠️ La carpeta configurada para Node-RED no existe: {ruta_carpeta}"

        archivos_json: list[str] = []
        for root, _, files in os.walk(ruta_carpeta):
            for file in files:
                if (
                    file.lower().endswith(".json")
                    and "memoria" not in file.lower()
                    and "package" not in file.lower()
                ):
                    archivos_json.append(os.path.join(root, file))

        if not archivos_json:
            return f"⚠️ No se encontraron archivos de flujos Node-RED (.json) en {ruta_carpeta}"

        resultados = []
        for arch in archivos_json[:5]:
            resultados.append(self.analizar_flujo(arch))

        texto_final = "\n\n---\n\n".join(resultados)
        return texto_final

    def obtener_instrucciones_ia(self) -> str:
        contexto_extra = self.cargar_contexto_reciente()
        instrucciones = (
            "[ADAPTADOR PRÁCTICO: INTERNET DE LAS COSAS (IoT) / NODE-RED]\n"
            "Reglas estrictas de mentoría:\n"
            "1. Enfócate en la construcción de flujos visuales basados en nodos (Inject, Debug, MQTT, Function, Dashboard).\n"
            "2. Explica detalladamente cómo viaja el `msg.payload` (formato JSON) entre los nodos.\n"
            "3. Evita escribir código nativo en Node.js a menos que sea estrictamente necesario dentro de un nodo `function`.\n"
            "4. Proporciona ejemplos de tópicos MQTT y estructuras de datos para dispositivos IoT simulados.\n"
        )
        if contexto_extra:
            instrucciones += (
                f"\n[FLUJOS REALES Y TÓPICOS MQTT CONFIGURADOS EN NODE-RED]:\n{contexto_extra}\n"
                "DIRECTIVA OBLIGATORIA: Utiliza preferentemente las pestañas, tópicos MQTT y endpoints reales extraídos de sus flujos.\n"
            )
        return instrucciones

    def generar_ejercicio_base(self, tema: str) -> str:
        return (
            f"### 🔌 Ejercicio Práctico de IoT (Node-RED)\n"
            f"- **Tema:** {tema}\n"
            f"- **Estructura del Flujo sugerida:** Nodo `Inject` (generador de datos simulados) -> Nodo `Function` (procesamiento) -> Nodo `Debug` (consola) o `Dashboard` (UI).\n"
            f"- **Boilerplate de Payload JSON inicial:**\n"
            f"```json\n"
            f'{{\n  "device_id": "sensor_iot_01",\n  "temperature": 25.4,\n  "status": "active"\n}}\n'
            f"```\n"
        )


__all__ = ["NodeRedPlugin", "extraer_resumen_funcion_js"]
