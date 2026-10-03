import os
import json
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
