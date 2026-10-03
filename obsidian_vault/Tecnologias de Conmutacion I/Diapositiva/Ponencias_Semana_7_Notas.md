---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

# [[Tecnologias de Conmutacion I]]

## VLANs y troncales seguros

* Deshabilitar administrativamente la interfaz no utilizada, con el subcomando de interfaz `shutdown`.
* Prevenir la negociación del `trunking` cuando el puerto está habilitado mediante el subcomando de interfaz `switchport nonegotiate` para deshabilitar la negociación, o el subcomando de interfaz `switchport mode access` para configurar estáticamente la interfaz como interfaz de acceso.
* Asignar el puerto a una [[VLAN]] no utilizada, llamada a veces [[VLAN]] de aparcamiento.

---

## Configuración y verificación de [[VTP]]

* Configuración del switch antes del ejemplo

> **Diagrama detectado:** Topología de red que muestra dos switches, **SW1** y **SW2**, conectados entre sí mediante un enlace troncal (`Trunk`) a través de sus interfaces `Gi0/1` (en SW1) y `Gi0/2` (en SW2). 
> - **SW1:** VLANs: 1, 2, 3, 1002-1005 | VTP Mode: Server | VTP Domain: `<null>` | VTP Password: `<null>` | VTP Revision: 5 | IP Address: 192.168.1.105
> - **SW2:** VLANs: 1, 1002-1005 | VTP Mode: Server | VTP Domain: `<null>` | VTP Password: `<null>` | Revision: 1 | IP Address: 192.168.1.106

---

## Configuración y verificación de [[VTP]]

* Configuración básica de cliente y servidor [[VTP]]

> **Captura de código detectada:** Consola de comandos de **SW1** configurando el servidor VTP:
> ```text
> SW1#configure terminal
> Enter configuration commands, one per line. End with CNTL/Z.
> SW1(config)#vtp mode server
> Setting device to VTP SERVER mode
> SW1(config)#vtp domain Freds-domain
> Changing VTP domain name from NULL to Freds-domain
> SW1(config)#vtp password Freds-password
> Setting device VLAN database password to Freds-password
> SW1(config)#vtp pruning
> Pruning switched on
> SW1(config)#^Z
> ```

---

## Configuración y verificación de [[VTP]]

* Configuración básica de cliente y servidor [[VTP]]

> **Captura de código detectada:** Consola de comandos de **SW2** configurando el cliente VTP:
> ```text
> SW2#configure terminal
> Enter configuration commands, one per line. End with CNTL/Z.
> SW2(config)#vtp mode client
> Setting device to VTP CLIENT mode.
> SW2(config)#vtp domain Freds-domain
> Domain name already set to Freds-domain.
> SW2(config)#vtp password Freds-password
> Setting device VLAN database password to Freds-password
> SW2(config)#^Z
> ```

---

## Configuración y verificación de [[VTP]]

* Configuración básica de cliente y servidor [[VTP]]

> **Captura de código detectada:** Salida del comando de verificación `show vtp status` en **SW2**:
> ```text
> SW2#show vtp status
> VTP Version                     : 2
> Configuration Revision          : 5
> Maximum VLANs supported locally : 255
> Number of existing VLANs        : 7
> VTP Operating Mode              : Client
> VTP Domain Name                 : Freds-domain
> VTP Pruning Mode                : Enabled
> VTP V2 Mode                     : Disabled
> VTP Traps Generation            : Disabled
> MD5 digest                      : 0x22 0x07 0xF2 0x3A 0xF1 0x28 0xA0 0x5D
> Configuration last modified by 192.168.1.105 at 3-1-93 00:28:35
> ```

---

## Configuración y verificación de [[VTP]]

* Configuración básica de cliente y servidor [[VTP]]

> **Captura de código detectada:** Salida del comando de verificación `show vlan brief` en **SW2**:
> ```text
> SW2#show vlan brief
> 
> VLAN Name                 Status    Ports
> ---- -------------------- --------- -------------------------------
> 1    default              active    Fa0/1, Fa0/2, Fa0/3, Fa0/4
>                                     Fa0/5, Fa0/6, Fa0/7, Fa0/8
>                                     Fa0/9, Fa0/10, Fa0/11, Fa0/12
>                                     Fa0/13, Fa0/14, Fa0/15, Fa0/16
>                                     Fa0/17, Fa0/18, Fa0/19, Fa0/20
>                                     Fa0/21, Fa0/22, Fa0/23, Fa0/24
>                                     Gi0/1
> 2    Freds-vlan           active    
> 3    VLAN0003             active    
> 1002 fddi-default         act/unsup 
> 1003 token-ring-default   act/unsup 
> 1004 fddinet-default      act/unsup 
> 1005 trnet-default        act/unsup 
> ```

---

## Configuración y verificación de [[VTP]]

* Configuración básica de cliente y servidor [[VTP]]

> **Captura de código detectada:** Salida combinada de verificación en **SW1**:
> ```text
> SW1#show vtp status
> VTP Version                     : 2
> Configuration Revision          : 5
> Maximum VLANs supported locally : 255
> Number of existing VLANs        : 7
> VTP Operating Mode              : Server
> VTP Domain Name                 : Freds-domain
> VTP Pruning Mode                : Enabled
> VTP V2 Mode                     : Disabled
> VTP Traps Generation            : Disabled
> MD5 digest                      : 0x22 0x07 0xF2 0x3A 0xF1 0x28 0xA0 0x5D
> Configuration last modified by 192.168.1.105 at 3-1-93 00:28:35
> Local updater ID is 192.168.1.105 on interface Vl1 (lowest numbered VLAN interface found)
> SW1#show vtp password
> VTP Password: Freds-password
> ```

---

## Configuración y verificación de [[VTP]]

* Dónde almacenan los clientes y servidores [[VTP]] la configuración relativa a la [[VLAN]]

| Configuration Commands | Where Stored | How to View |
| :--- | :--- | :--- |
| `vtp domain` | `vlan.dat` | `show vtp status` |
| `vtp mode` | `vlan.dat` | `show vtp status` |
| `vtp password` | `vlan.dat` | `show vtp password` |
| `vtp pruning` | `vlan.dat` | `show vtp status` |
| `vlan vlan-id` | `vlan.dat` | `show vlan [brief]` |
| `name vlan-name` | `vlan.dat` | `show vlan [brief]` |
| `switchport access vlan vlan-id` | `running-config` | `show running-config`, `show interfaces switchport` |
| `switchport voice vlan vlan-id` | `running-config` | `show running-config`, `show interfaces switchport` |

---

> **Imagen detectada:** Logotipo de certificación [[CCNA]] Routing & Switching de Cisco Systems.