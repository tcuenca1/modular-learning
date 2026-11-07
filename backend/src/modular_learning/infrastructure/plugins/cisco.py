"""Adaptador práctico para Redes, Conmutación y Cisco Packet Tracer."""

from __future__ import annotations

import os
import re
from typing import Any

from modular_learning.core.ports.plugin_practico import PluginPracticoBase
from modular_learning.infrastructure.persistence.almacen import DocumentoJson


def parsear_configuracion_ios(texto: str) -> dict[str, Any]:
    """
    Parsea una configuración Cisco IOS ('show running-config') o un registro de comandos CLI.
    Extrae hostname, VLANs, interfaces (IP, descripción, modo, vlan), enrutamiento y ACLs.
    """
    lineas = texto.splitlines()
    hostname: str | None = None
    interfaces: list[dict[str, Any]] = []
    vlans: list[dict[str, str]] = []
    enrutamiento: list[str] = []
    acls: list[str] = []
    comandos_cli: list[str] = []

    interfaz_actual: dict[str, Any] | None = None
    vlan_actual: dict[str, str] | None = None
    enrutador_actual: dict[str, Any] | None = None

    for linea_raw in lineas:
        linea = linea_raw.strip()
        if not linea or linea.startswith(("!", "Building configuration")):
            continue

        # Detección de comandos en prompts interactivos (Router# o SW(config)#)
        prompt_match = re.search(
            r"^([A-Za-z0-9_-]+)(?:\([a-z0-9-]+\))?[#>]+\s*(.*)$", linea, re.IGNORECASE
        )
        if prompt_match:
            host_detectado, cmd = prompt_match.groups()
            if not hostname and host_detectado.lower() not in ["router", "switch"]:
                hostname = host_detectado
            if cmd:
                comandos_cli.append(cmd.strip())
                linea = cmd.strip()

        # 1. Hostname
        host_match = re.match(r"^hostname\s+([^\s!]+)", linea, re.IGNORECASE)
        if host_match:
            hostname = host_match.group(1).strip()
            continue

        # 2. VLANs (vlan 10, name Sistemas)
        vlan_match = re.match(r"^vlan\s+(\d+)", linea, re.IGNORECASE)
        if vlan_match:
            if vlan_actual:
                vlans.append(vlan_actual)
            vlan_actual = {"id": vlan_match.group(1), "nombre": f"VLAN {vlan_match.group(1)}"}
            continue
        if vlan_actual and linea.lower().startswith("name "):
            vlan_actual["nombre"] = linea[5:].strip()
            vlans.append(vlan_actual)
            vlan_actual = None
            continue

        # 3. Interfaces
        int_match = re.match(r"^interface\s+([A-Za-z0-9/.-]+)", linea, re.IGNORECASE)
        if int_match:
            if interfaz_actual:
                interfaces.append(interfaz_actual)
            interfaz_actual = {
                "nombre": int_match.group(1),
                "ip": None,
                "descripcion": None,
                "modo": None,
                "vlan": None,
                "trunk_vlans": None,
                "shutdown": False,
            }
            continue

        if interfaz_actual:
            if linea.lower().startswith("ip address "):
                partes = linea.split()
                if len(partes) >= 4:
                    interfaz_actual["ip"] = f"{partes[2]} {partes[3]}"
                elif len(partes) >= 3:
                    interfaz_actual["ip"] = partes[2]
            elif linea.lower().startswith("description "):
                interfaz_actual["descripcion"] = linea[12:].strip()
            elif "switchport mode" in linea.lower():
                modo = "trunk" if "trunk" in linea.lower() else "access"
                interfaz_actual["modo"] = modo
            elif "switchport access vlan" in linea.lower():
                vlan_id = linea.split()[-1]
                interfaz_actual["vlan"] = vlan_id
            elif "switchport trunk allowed vlan" in linea.lower():
                interfaz_actual["trunk_vlans"] = linea.split()[-1]
            elif linea.lower() == "shutdown":
                interfaz_actual["shutdown"] = True
            elif linea.lower() == "no shutdown":
                interfaz_actual["shutdown"] = False
            elif not linea_raw.startswith(" ") and not linea_raw.startswith("\t"):
                # Salida del bloque de interfaz
                interfaces.append(interfaz_actual)
                interfaz_actual = None

        # 4. Enrutamiento
        router_match = re.match(r"^router\s+([A-Za-z0-9_-]+)(?:\s+(\d+))?", linea, re.IGNORECASE)
        if router_match:
            proto, proceso = router_match.groups()
            enrutador_actual = {"proto": proto.upper(), "proceso": proceso or "", "redes": []}
            continue

        if enrutador_actual:
            if linea.lower().startswith("network "):
                enrutador_actual["redes"].append(linea[8:].strip())
            elif linea.lower().startswith("version "):
                enrutador_actual["version"] = linea[8:].strip()
            elif not linea_raw.startswith(" ") and not linea_raw.startswith("\t"):
                redes_str = (
                    ", ".join(enrutador_actual["redes"])
                    if enrutador_actual["redes"]
                    else "sin redes definidas"
                )
                id_str = (
                    f" proceso {enrutador_actual['proceso']}" if enrutador_actual["proceso"] else ""
                )
                enrutamiento.append(f"{enrutador_actual['proto']}{id_str} (redes: {redes_str})")
                enrutador_actual = None

        if linea.lower().startswith("ip route "):
            enrutamiento.append(f"Ruta estática: {linea[9:].strip()}")

        # 5. ACLs
        if linea.lower().startswith("access-list ") or linea.lower().startswith("ip access-list "):
            acls.append(linea)

    # Limpiezas finales de bloques abiertos
    if vlan_actual:
        vlans.append(vlan_actual)
    if interfaz_actual:
        interfaces.append(interfaz_actual)
    if enrutador_actual:
        redes_str = (
            ", ".join(enrutador_actual["redes"])
            if enrutador_actual["redes"]
            else "sin redes definidas"
        )
        id_str = f" proceso {enrutador_actual['proceso']}" if enrutador_actual["proceso"] else ""
        enrutamiento.append(f"{enrutador_actual['proto']}{id_str} (redes: {redes_str})")

    return {
        "hostname": hostname or "Equipo Cisco",
        "vlans": vlans,
        "interfaces": interfaces,
        "enrutamiento": enrutamiento,
        "acls": acls,
        "comandos_cli": comandos_cli[:15],
    }


def formatear_resumen_dispositivo(datos: dict[str, Any]) -> str:
    """Convierte los datos parseados de un equipo en un resumen Markdown conciso."""
    lineas = [f"#### 📟 Equipo: {datos['hostname']}"]

    if datos["vlans"]:
        vlan_items = [f"VLAN {v['id']} ({v['nombre']})" for v in datos["vlans"]]
        lineas.append(f"- **VLANs configuradas:** {', '.join(vlan_items)}")

    if datos["interfaces"]:
        lineas.append("- **Interfaces activas:**")
        for iface in datos["interfaces"]:
            detalles = []
            if iface["ip"]:
                detalles.append(f"IP {iface['ip']}")
            if iface["modo"]:
                detalles.append(f"Modo {iface['modo']}")
            if iface["vlan"]:
                detalles.append(f"VLAN {iface['vlan']}")
            if iface["trunk_vlans"]:
                detalles.append(f"VLANs troncal: {iface['trunk_vlans']}")
            if iface["descripcion"]:
                detalles.append(f"'{iface['descripcion']}'")
            if iface["shutdown"]:
                detalles.append("⚠️ Administrativamente apagada")

            detalle_str = f" ({', '.join(detalles)})" if detalles else ""
            lineas.append(f"  - `{iface['nombre']}`{detalle_str}")

    if datos["enrutamiento"]:
        lineas.append("- **Protocolos de enrutamiento y rutas:**")
        for r in datos["enrutamiento"]:
            lineas.append(f"  - {r}")

    if datos["acls"]:
        lineas.append(
            f"- **Listas de control de acceso (ACLs):** {len(datos['acls'])} reglas detectadas"
        )
        for acl in datos["acls"][:3]:
            lineas.append(f"  - `{acl}`")

    if datos["comandos_cli"]:
        lineas.append(
            f"- **Historial reciente de comandos ejecutados:** {len(datos['comandos_cli'])} comandos"
        )
        for cmd in datos["comandos_cli"][:5]:
            lineas.append(f"  - `{cmd}`")

    return "\n".join(lineas)


class CiscoPlugin(PluginPracticoBase):
    """Adaptador práctico para Redes, Conmutación y Cisco Packet Tracer."""

    def __init__(self, memoria: DocumentoJson | None = None):
        self._memoria = memoria or DocumentoJson("plugins/cisco_memoria.json")

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
            print(f"⚠️ No se pudo guardar la memoria del plugin Cisco: {e}")

    def cargar_contexto_reciente(self) -> str:
        try:
            historial = self._memoria.leer(None)
            if historial is None:
                self._sincronizar_desde_vault()
                historial = self._memoria.leer([])
            if isinstance(historial, list) and historial:
                return "\n\n".join(historial)
        except Exception:
            pass
        return ""

    def analizar_archivo(self, ruta_archivo: str) -> str:
        """Lee un archivo de configuración Cisco IOS o de comandos y extrae su estructura."""
        if not os.path.isfile(ruta_archivo):
            return f"⚠️ Archivo no encontrado: {ruta_archivo}"
        try:
            with open(ruta_archivo, "r", encoding="utf-8", errors="replace") as f:
                contenido = f.read()
        except Exception as e:
            return f"⚠️ Error leyendo {ruta_archivo}: {e}"

        datos = parsear_configuracion_ios(contenido)
        return formatear_resumen_dispositivo(datos)

    def analizar_carpeta(self, ruta_carpeta: str) -> str:
        """
        Escanea la carpeta de actividades de Cisco buscando archivos de configuración (.txt, .cfg, .ios, .log, .md).
        Extrae y resume la topología real de los equipos para el tutor.
        """
        if not os.path.isdir(ruta_carpeta):
            return f"⚠️ La carpeta configurada para Cisco no existe: {ruta_carpeta}"

        archivos_encontrados: list[str] = []
        extensiones_validas = {".txt", ".cfg", ".ios", ".log", ".md", ".conf"}

        for root, _, files in os.walk(ruta_carpeta):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensiones_validas):
                    archivos_encontrados.append(os.path.join(root, file))

        if not archivos_encontrados:
            return f"⚠️ No se encontraron archivos de configuración Cisco (.cfg, .txt, .ios, .log) en {ruta_carpeta}"

        resumenes: list[str] = []
        equipos_detectados: list[str] = []

        for ruta in archivos_encontrados[:8]:  # Limitar a 8 archivos de configuración
            resumen = self.analizar_archivo(ruta)
            if "Equipo:" in resumen:
                resumenes.append(f"**Archivo:** `{os.path.basename(ruta)}`\n{resumen}")
                # Buscar hostname
                m = re.search(r"Equipo:\s+([^\n\r]+)", resumen)
                if m:
                    equipos_detectados.append(m.group(1).strip())

        if not resumenes:
            return f"⚠️ Los archivos encontrados en {ruta_carpeta} no contenían configuraciones Cisco IOS válidas."

        texto_final = (
            f"### 🌐 Topología y Configuraciones Cisco IOS Detectadas\n"
            f"- **Carpeta analizada:** `{ruta_carpeta}`\n"
            f"- **Equipos detectados ({len(equipos_detectados)}):** {', '.join(equipos_detectados) or 'Varios'}\n\n"
            + "\n\n".join(resumenes)
        )
        self.guardar_contexto_extraido(texto_final)
        return texto_final

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
            for root, _, files in os.walk(vault_materia):
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
            instrucciones += (
                f"\n[TOPOLOGÍA Y CONFIGURACIÓN REAL DE TUS PRÁCTICAS EN PACKET TRACER]:\n{contexto_extra}\n"
                "DIRECTIVA: Utiliza preferentemente los nombres de los equipos reales, sus interfaces y sus subredes detectadas arriba.\n"
            )
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


__all__ = ["CiscoPlugin", "formatear_resumen_dispositivo", "parsear_configuracion_ios"]
