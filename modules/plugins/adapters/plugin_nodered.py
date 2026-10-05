import json
import os

from modules.plugins.ports.base_plugin import PluginPracticoBase


class NodeRedPlugin(PluginPracticoBase):
    """Adaptador práctico para IoT y Node-RED."""

    def __init__(self):
        self.ruta_memoria = os.path.join("data", "plugins", "nodered_memoria.json")

    def guardar_contexto_extraido(self, metadatos: str) -> None:
        metadatos = metadatos.strip()
        if not metadatos:
            return

        historial = []
        os.makedirs(os.path.dirname(self.ruta_memoria), exist_ok=True)
        if os.path.exists(self.ruta_memoria):
            try:
                with open(self.ruta_memoria, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                    if isinstance(contenido, list):
                        historial = contenido
            except Exception:
                historial = []

        historial.append(metadatos)
        historial = historial[-5:]

        try:
            with open(self.ruta_memoria, "w", encoding="utf-8") as f:
                json.dump(historial, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ No se pudo guardar la memoria del plugin Node-RED: {e}")

    def cargar_contexto_reciente(self) -> str:
        if not os.path.exists(self.ruta_memoria):
            return ""
        try:
            with open(self.ruta_memoria, "r", encoding="utf-8") as f:
                historial = json.load(f)
            if isinstance(historial, list) and historial:
                return "\n".join([f"- {item}" for item in historial])
            return ""
        except Exception:
            return ""

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
            instrucciones += f"\n[CONTEXTO TÉCNICO ADICIONAL EXTRAÍDO DE DOCUMENTOS INGESTADOS EN IOT]:\n{contexto_extra}\n"
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

    def analizar_flujo(self, ruta_archivo: str) -> str:
        """
        Recibe la ruta del archivo JSON de un flujo IoT (Node-RED), lo parsea,
        extrae la información útil (nodos, sensores, endpoints) y retorna el texto
        procesado para que el sistema lo maneje como cualquier otro material de estudio.
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

        nodos = []
        if isinstance(data, list):
            nodos = data
        elif isinstance(data, dict):
            if "flows" in data and isinstance(data["flows"], list):
                nodos = data["flows"]
            elif "nodes" in data and isinstance(data["nodes"], list):
                nodos = data["nodes"]
            else:
                nodos = [data]

        total_nodos = len(nodos)
        tipos_nodos = {}
        endpoints_http = []
        sensores_detectados = []

        for nodo in nodos:
            if not isinstance(nodo, dict):
                continue
            tipo = nodo.get("type", "desconocido")
            tipos_nodos[tipo] = tipos_nodos.get(tipo, 0) + 1

            if tipo in ["http in", "http out"]:
                url = nodo.get("url")
                method = nodo.get("method")
                if url:
                    endpoints_http.append(f"- HTTP {method or 'GET'} {url} ({tipo})")

            nombre = nodo.get("name", "")
            topic = nodo.get("topic", "")
            if any(
                kw in tipo.lower() or kw in nombre.lower() or kw in topic.lower()
                for kw in [
                    "sensor",
                    "mqtt",
                    "temperature",
                    "humidity",
                    "esp32",
                    "arduino",
                    "raspberry",
                    "dht",
                    "inject",
                    "function",
                ]
            ):
                sensores_detectados.append(
                    f"- Nodo [{tipo}] '{nombre or 'Sin nombre'}' (Tópico MQTT: {topic or 'N/A'})"
                )

        lineas = [
            "### 🔌 Análisis de Flujo IoT / Node-RED",
            f"- **Archivo fuente:** {ruta_archivo}",
            f"- **Total de nodos:** {total_nodos}",
            "\n#### Tipos de Nodos:",
        ]
        for t, cant in tipos_nodos.items():
            lineas.append(f"- {t}: {cant}")

        if endpoints_http:
            lineas.append("\n#### Endpoints HTTP Configurados:")
            lineas.extend(endpoints_http)

        if sensores_detectados:
            lineas.append("\n#### Sensores y Dispositivos Detectados:")
            lineas.extend(sensores_detectados)

        texto_procesado = "\n".join(lineas)
        self.guardar_contexto_extraido(texto_procesado)
        return texto_procesado
