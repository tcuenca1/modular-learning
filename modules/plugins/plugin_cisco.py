from modules.plugins.base_plugin import PluginPracticoBase


class CiscoPlugin(PluginPracticoBase):
    """Adaptador práctico para Redes, Conmutación y Cisco Packet Tracer."""

    def obtener_instrucciones_ia(self) -> str:
        return (
            "[ADAPTADOR PRÁCTICO: CISCO PACKET TRACER / REDES]\n"
            "Reglas estrictas de mentoría:\n"
            "1. Enfócate en la configuración real de equipos mediante la CLI de Cisco IOS.\n"
            "2. Detalla paso a paso los modos de comando (User EXEC '> baz', Privileged EXEC '#', Global Configuration '(config)#', Interface '(config-if)#').\n"
            "3. Explica los protocolos de red involucrados (OSPF, VLANs, STP, ACLs, etc.) con topologías lógicas claras.\n"
            "4. Proporciona comandos exactos y funcionales adaptados para simulaciones en Cisco Packet Tracer.\n"
        )

    def generar_ejercicio_base(self, tema: str) -> str:
        return (
            f"### 🌐 Ejercicio Práctico de Redes (Cisco Packet Tracer)\n"
            f"- **Tema:** {tema}\n"
            f"- **Topología sugerida:** 2 Routers, 2 Switches y PCs en subredes distintas.\n"
            f"- **Boilerplate de configuración inicial (Router 0):**\n"
            f"```text\n"
            f"enable\n"
            f"configure terminal\n"
            f"hostname R1\n"
            f"interface GigabitEthernet0/0\n"
            f" ip address 192.168.1.1 255.255.255.0\n"
            f" no shutdown\n"
            f"```\n"
        )
