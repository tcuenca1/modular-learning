import os
import json
from modules.plugins.ports.base_plugin import PluginPracticoBase


class CiscoPlugin(PluginPracticoBase):
    """Adaptador práctico para Redes, Conmutación y Cisco Packet Tracer."""

    def __init__(self):
        self.ruta_memoria = os.path.join("data", "plugins", "cisco_memoria.json")

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
            print(f"⚠️ No se pudo guardar la memoria del plugin Cisco: {e}")

    def cargar_contexto_reciente(self) -> str:
        if not os.path.exists(self.ruta_memoria):
            self._sincronizar_desde_vault()

        try:
            if os.path.exists(self.ruta_memoria):
                with open(self.ruta_memoria, "r", encoding="utf-8") as f:
                    historial = json.load(f)
                if isinstance(historial, list) and historial:
                    return "\n".join([f"- {item}" for item in historial])
        except Exception:
            pass
        return ""

    def _sincronizar_desde_vault(self) -> None:
        """Lee el contexto actual almacenado en el Vault de Obsidian para Tecnologias de Conmutacion I."""
        vault_materia = os.path.join("obsidian_vault", "Tecnologias de Conmutacion I")
        if not os.path.exists(vault_materia):
            return

        elementos_tecnicos = []
        keywords_redes = [
            "switch",
            "router",
            "cli",
            "vlan",
            "stp",
            "ospf",
            "mac",
            "ip",
            "packet tracer",
            "ethernet",
            "interfaz",
            "puerto",
            "puente",
        ]

        try:
            for root, dirs, files in os.walk(vault_materia):
                for file in files:
                    if file.endswith(".md"):
                        ruta_md = os.path.join(root, file)
                        try:
                            with open(ruta_md, "r", encoding="utf-8") as md_file:
                                lineas = md_file.readlines()
                            for linea in lineas:
                                linea_clean = linea.strip()
                                if (
                                    any(kw in linea_clean.lower() for kw in keywords_redes)
                                    and len(linea_clean) > 20
                                    and not linea_clean.startswith("#")
                                ):
                                    limpia = linea_clean.lstrip("-*# >").strip()
                                    if limpia and limpia not in elementos_tecnicos:
                                        elementos_tecnicos.append(limpia)
                        except Exception:
                            pass

            if elementos_tecnicos:
                resumen_inicial = elementos_tecnicos[:5]
                self.guardar_contexto_extraido(" | ".join(resumen_inicial))
        except Exception as e:
            print(f"⚠️ Error al sincronizar memoria de Cisco desde el Vault: {e}")

    def obtener_instrucciones_ia(self) -> str:
        contexto_extra = self.cargar_contexto_reciente()
        instrucciones = (
            "[ADAPTADOR PRÁCTICO: CISCO PACKET TRACER / REDES]\n"
            "Reglas estrictas de mentoría:\n"
            "1. Enfócate en la configuración real de equipos mediante la CLI de Cisco IOS.\n"
            "2. Detalla paso a paso los modos de comando (User EXEC '>', Privileged EXEC '#', Global Configuration '(config)#', Interface '(config-if)#').\n"
            "3. Explica los protocolos de red involucrados (OSPF, VLANs, STP, ACLs, etc.) con topologías lógicas claras.\n"
            "4. Proporciona comandos exactos y funcionales adaptados para simulaciones en Cisco Packet Tracer.\n"
        )
        if contexto_extra:
            instrucciones += f"\n[CONTEXTO TÉCNICO ADICIONAL EXTRAÍDO DEL VAULT DE TECNOLOGÍAS DE CONMUTACIÓN I]:\n{contexto_extra}\n"
        return instrucciones

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
