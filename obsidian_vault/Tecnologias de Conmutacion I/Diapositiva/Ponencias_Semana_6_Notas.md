---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Configuración del trunking de [[VLAN]]

## Red con dos switches y tres [[VLAN]]s

> **Diagrama detectado:** Topología de red que muestra dos switches ([[SW1]] y [[SW2]]) conectados entre sí mediante un enlace troncal ([[Trunk]]) en los puertos [[GigabitEthernet]] 0/1 ([[Gi0/1]]) y [[GigabitEthernet]] 0/2 ([[Gi0/2]]). Alrededor se distribuyen tres [[VLAN]]s:
> - **[[VLAN]] 2:** Conectada a los puertos Fa0/13 y Fa0/14 de [[SW1]].
> - **[[VLAN]] 3:** Conectada a los puertos Fa0/15, Fa0/16 ([[SW1]]) y Fa0/23, Fa0/24 ([[SW2]]).
> - **[[VLAN]] 1:** Conectada a los puertos Fa0/11, Fa0/12 ([[SW1]]) y Fa0/21, Fa0/22 ([[SW2]]).

---

## Opciones del modo administrativo de trunking con el comando `switchport mode`

| Opciones del comando | Descripción |
| :--- | :--- |
| `access` | Previene el uso del [[trunking]], haciendo que el puerto siempre actúe como un puerto de acceso (no troncal). |
| `trunk` | Utiliza siempre el [[trunking]]. |
| `dynamic desirable` | Inicia y responde a mensajes de negociación para elegir dinámicamente si comenzar a utilizar el [[trunking]], y define la encapsulación de [[trunking]]. |
| `dynamic auto` | Espera pasivamente a recibir mensajes de negociación de troncal, momento en el que el switch responderá y negociará si utilizar el [[trunking]], y si es así, el tipo de [[trunking]]. |

---

## Configuración de trunking y comandos show

> **Captura de código detectada:** Salida del comando `show interfaces gigabit 0/1 switchport` en [[SW1]], mostrando que el estado del [[Switchport]] está habilitado (`Enabled`), el modo administrativo configurado es `dynamic auto`, el modo operativo es `static access`, y la encapsulación administrativa es `dot1q`.

> **Captura de código detectada:** Secuencia de comandos en [[SW1]] para modificar el modo de interfaz a `dynamic desirable`:
> ```text
> SW1# configure terminal
> SW1(config)# interface gigabit 0/1
> SW1(config-if)# switchport mode dynamic desirable
> SW1(config-if)# *Z
> ```
> Se muestran los mensajes de cambio de estado de la línea a `down` y posteriormente a `up`.

> **Captura de código detectada:** Comprobación posterior mediante `show interfaces gigabit 0/1 switchport` y `show interfaces trunk`, donde se confirma que el puerto [[Gi0/1]] se encuentra operando en modo troncal (`Status: trunking`), utilizando encapsulación `802.1q` con la [[VLAN nativa]] [[VLAN|1]], y permitiendo las [[VLAN]]s de la 1 a la 4094.

---

## Modo operativo de trunking esperado basado en los modos administrativos configurados

| Administrative Mode | Access | Dynamic Auto | Trunk | Dynamic Desirable |
| :--- | :--- | :--- | :--- | :--- |
| **access** | Access | Access | Access | Access |
| **dynamic auto** | Access | Access | Trunk | Trunk |
| **trunk** | Access | Trunk | Trunk | Trunk |
| **dynamic desirable** | Access | Trunk | Trunk | Trunk |

---

## Control de las [[VLAN]]s soportadas en un troncal

Por defecto, los switches incluyen a todas las posibles [[VLAN]]s (1-4094) en la lista [[VLAN]] permitida en cada troncal. Sin embargo, se puede limitar las [[VLAN]]s permitidas en el troncal utilizando el siguiente subcomando de interfaz:

`switchport trunk allowed vlan {add | all | except | remove} lista-vlan`

> **Captura de código detectada:** Configuración para eliminar la [[VLAN]] 3 del enlace troncal y comandos de verificación (`show interfaces trunk`):
> ```text
> SW1(config)# vlan 4
> SW1(config-vlan)# vlan 2
> SW1(config-vlan)# shutdown
> SW1(config-vlan)# interface gi0/1
> SW1(config-if)# switchport trunk allowed vlan remove 3
> ```
> La salida de `show interfaces trunk` refleja que las [[VLAN]]s permitidas en el troncal ahora son `1-2, 4-4094`, y las activas son `1, 4`.

---

## [[Trunking]] para los teléfonos IP de Cisco

> **Diagrama detectado:** Conexión típica donde un switch se conecta a través del puerto Fa0/6 mediante un enlace troncal 802.1Q a un teléfono IP de Cisco (asociado a la [[Voice VLAN]] [[VLAN|12]]), y a su vez el teléfono IP se conecta a una PC (asociada a la [[Access VLAN]] [[VLAN|2]]) mediante un enlace que no es troncal (`Not Trunking`).

### Configuración [[VLAN]] de voz y de datos

| Device | Name of the [[VLAN]] | Configured with This Command |
| :--- | :--- | :--- |
| Phone | Voice or auxiliary [[VLAN]] | `switchport voice vlan vlan-id` |
| PC | Data or access [[VLAN]] | `switchport access vlan vlan-id` |