from modules.plugins.base_plugin import PluginPracticoBase


class NodeRedPlugin(PluginPracticoBase):
    """Adaptador práctico para IoT y Node-RED."""

    def obtener_instrucciones_ia(self) -> str:
        return (
            "[ADAPTADOR PRÁCTICO: INTERNET DE LAS COSAS (IoT) / NODE-RED]\n"
            "Reglas estrictas de mentoría:\n"
            "1. Enfócate en la construcción de flujos visuales basados en nodos (Inject, Debug, MQTT, Function, Dashboard).\n"
            "2. Explica detalladamente cómo viaja el `msg.payload` (formato JSON) entre los nodos.\n"
            "3. Evita escribir código nativo en Node.js a menos que sea estrictamente necesario dentro de un nodo `function`.\n"
            "4. Proporciona ejemplos de tópicos MQTT y estructuras de datos para dispositivos IoT simulados.\n"
        )

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
