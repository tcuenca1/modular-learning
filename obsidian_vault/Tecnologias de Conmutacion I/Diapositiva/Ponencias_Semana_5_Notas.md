---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# LANs virtuales

---

## Objetivos

* Entender el significado y el propósito de las [[VLAN]], el trunking VLAN, y el protocolo de trunking VLAN ([[VTP]], VLAN Trunking Protocol).
* Configurar las [[VLAN]] y los troncales en los switches Catalyst de Cisco.
* Configurar y solucionar problemas en las instalaciones [[VTP]].

---

## Conceptos de LANs virtuales

* Red de ejemplo con dos [[VLAN]] utilizando un switch.

> **Diagrama detectado:** Red de ejemplo que muestra un switch conectado a cuatro computadoras distribuidas en dos [[VLAN]]: la computadora [ESTUDIANTE] (Dino) y la computadora [ESTUDIANTE] (Fred) pertenecen a la VLAN1, mientras que la computadora [ESTUDIANTE] (Wilma) y la computadora [ESTUDIANTE] (Betty) pertenecen a la VLAN2.

---

## Conceptos de LANs virtuales

* Razones más comunes para separar hosts en [[VLAN]] diferentes:
  * Crear diseños más flexibles que agrupen a usuarios por departamentos, o por grupos que trabajen juntos, en lugar de por su ubicación física.
  * Segmentar dispositivos en [[LAN]] más pequeñas para reducir la sobrecarga causada por cada host en la [[VLAN]].
  * Reducir la carga de trabajo del Protocolo de árbol de extensión ([[STP]]) limitando una [[VLAN]] a un único acceso al switch.
  * Forzar una mayor seguridad separando los hosts que trabajen con datos sensibles en una [[VLAN]] diferente.
  * Separar tráfico enviado por un teléfono IP del tráfico enviado por PCs conectados a los teléfonos.

---

## Trunking con ISL y 802.1Q

* Trunking de [[VLAN]] entre dos switches.

> **Diagrama detectado:** Topología de trunking entre Switch 1 y Switch 2. Muestra interfaces 0/1, 0/2 en VLAN 1, e interfaces 0/5, 0/6 en VLAN 2, interconectadas mediante un enlace troncal (Trunk) que transporta el tráfico etiquetado con VLAN ID junto con la trama Ethernet.

---

## ISL

* Cabecera ISL.

> **Diagrama detectado:** Estructura de la cabecera ISL de 26 bytes, seguida de la trama Ethernet encapsulada de 4 bytes con CRC. Se desglosan los campos internos: DA, Type, User, SA, LEN, AAAA03, HSA, VLAN, BPDU, INDEX y RES.

---

## IEEE 802.1Q

* Cabecera de trunking 802.1Q.

> **Diagrama detectado:** Comparación de una trama Ethernet estándar (Dest. Address, Source Address, Len./Type, Data, FCS) frente a una trama etiquetada con 802.1Q que añade un campo Tag. El Tag se desglosa en Type (16 Bits, 0x8100), Priority (3 Bits), Flag (1 Bit) y VLAN ID (12 Bits).

---

## Comparación de ISL con 802.1Q

* Comparación entre ISL y 802.1Q:

| Función | ISL | 802.1Q |
| :--- | :--- | :--- |
| Definido por | Cisco | IEEE |
| Inserta otros 4 bytes en la cabecera en vez de encapsular completamente la trama original | No | Sí |
| Soporta rango normal (1-1005) y extendido (1006-4094) de [[VLAN]]s | Sí | Sí |
| Permite múltiples árboles de extensión | Sí | Sí |
| Utiliza [[VLAN nativa]] | No | Sí |

---

## Subredes IP y [[VLAN]]s

* Enrutamiento entre [[VLAN]]s.

> **Diagrama detectado:** Esquema de un switch multicapa (multilayer switch) que enruta tráfico entre la VLAN 1 (Subred IP 10.1.1.0/24 con hosts Dino y Fred), la VLAN 2 (Subred IP 10.1.2.0/24 con host Wilma) y la VLAN 3 (Subred IP 10.1.3.0/24 con host Barney), conectado mediante un enlace troncal a un router a través de la interfaz Fa0/0.

---

## Protocolo de trunking VLAN (VTP, VLAN Trunking Protocol)

* Mecanismo por el cual los switches de Cisco pueden intercambiar información de la [[VLAN]], sin publicar detalles sobre qué interfaces del switch están asignadas a cada [[VLAN]].
* Cada switch utiliza uno de los tres modos de [[VTP]]: servidor, cliente o transparente.
* Se puede añadir la configuración en modo servidor.
* El switch en modo cliente aprende acerca de los cambios en la base de datos de la [[VLAN]], los clientes no se pueden utilizar para configurar la información de la [[VLAN]].
* Los switches de Cisco no pueden deshabilitar [[VTP]], la opción más parecida es utilizar el modo transparente, lo que causa que el switch ignore [[VTP]], con la excepción de reenviar los mensajes [[VTP]].

---

## Operación normal de VTP utilizando los modos servidor y cliente de VTP

* Configuración de los números de revisión de [[VTP]] y el proceso de actualización de [[VTP]].

> **Diagrama detectado:** Flujo de actualización [[VTP]] donde un servidor [[VTP]] procesa la adición de una nueva [[VLAN]] (Rev 3 a Rev 4) y envía anuncios [[VTP]] a los switches clientes, los cuales actualizan su número de revisión y sincronizan la nueva información de la [[VLAN]].

---

## Operación normal de VTP utilizando los modos servidor y cliente de VTP

* Publicaciones de resumen (listan el número de revisión, el nombre de dominio).
* Publicaciones de subconjunto (publica algún subconjunto de la base de datos de [[VLAN]] siempre y cuando algo cambie y se indique con un número de revisión mayor).
* Solicitud de publicación (permite al switch pedir mensajes [[VTP]] a los switches vecinos tan pronto como surge el troncal).

> **Diagrama detectado:** Topología de red jerárquica con múltiples switches interconectados (S0, C1, C2, D1, D2, D3, D4, S1 a S6) ilustrando la propagación de paquetes de actualización [[VTP]].

---

## Tres requisitos para que VTP funcione entre dos switches

* El enlace entre los switches debe trabajar como un troncal VLAN (ISL ó 802.1Q).
* El nombre de dominio [[VTP]] de los switches debe coincidir (considerando mayúsculas y minúsculas).
* Si se configura en al menos uno de los switches, las contraseñas [[VTP]] de los dos switches deben coincidir (considerando mayúsculas y minúsculas).

---

## Cómo evitar VTP empleando el modo transparente de VTP

* Los switches en modo transparente [[VTP]] pueden configurar [[VLAN]]s, sin embargo nunca actualizan sus bases de datos en [[VLAN]] basándose en los mensajes [[VTP]] entrantes y los switches en modo transparente nunca tratan de crear mensajes [[VTP]] para anunciar a otros switches su propia configuración [[VLAN]].
* Los switches en modo transparente se comportan esencialmente como si [[VTP]] no existiera, sólo con una excepción: envían las actualizaciones [[VTP]] recibidas de otros switches, simplemente para ayudar a cualquier switch servidor o cliente [[VTP]] vecino.

---

## Versiones de VTP

* Tres versiones.
* Con VTP v1 un switch en modo transparente podría comprobar primero el nombre de dominio y la contraseña recibidos en una actualización [[VTP]], si ambos parámetros no coinciden, el switch descarta la actualización.
* Con VTP v2 un switch en modo transparente cambia la lógica ignorando el nombre de dominio y contraseña, enviando todas las actualizaciones [[VTP]] recibidas.
* VTP v3 está disponible sólo en los switches de gama alta.

---

## Pruning VTP

* [[VTP Pruning]].

> **Diagrama detectado:** Topología de red que muestra un conjunto de switches (Switch 1 al Switch 6) interconectados, donde el tráfico de broadcast de la VLAN 10 entre los puertos Port 1 y Port 2 es podado (*Pruned*) en los enlaces redundantes innecesarios mediante [[VTP Pruning]].

---

## Creación de VLANs y asignación de VLANs de acceso a una interfaz

* Red con un switch y tres [[VLAN]]s.

> **Diagrama detectado:** Topología de un único switch SW1 con tres [[VLAN]]s configuradas: VLAN 1 (interfaces Fa0/11 y Fa0/12), VLAN 2 (interfaces Fa0/13 y Fa0/14) y VLAN 3 (interfaces Fa0/15 y Fa0/16), cada una con sus respectivas PCs conectadas.

---

## Ejemplo 1 de configuración de VLAN: configuración completa de una VLAN

* Configurando [[VLAN]]s y asignando interfaces a las [[VLAN]]s.

> **Captura de código detectada:**
> ```text
> sw1-2960#configure terminal
> Enter configuration commands, one per line. End with CNTL/Z.
> sw1-2960(config)#vlan 2
> sw1-2960(config-vlan)#name Freds-vlan
> sw1-2960(config-vlan)#exit
> sw1-2960(config)#interface range fastethernet 0/13 - 14
> sw1-2960(config-if)#switchport access vlan 2
> sw1-2960(config-if)#exit
> ```

---

## Ejemplo 2 de configuración de VLAN: la configuración más breve de una VLAN

* Ejemplo corto de configuración de [[VLAN]] (VLAN 3).

> **Captura de código detectada:**
> ```text
> SW1#configure terminal
> Enter configuration commands, one per line. End with CNTL/Z.
> SW1(config)#interface range Fastethernet 0/15 - 16
> SW1(config-if-range)#switchport access vlan 3
> % Access VLAN does not exist. Creating vlan 3
> SW1(config-if-range)#^Z
> ```