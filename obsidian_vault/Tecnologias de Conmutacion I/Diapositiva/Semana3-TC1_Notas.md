---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-28
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Configuración de un [[Switch]] [[Ethernet]]

---

## Contenido a tratar
* Configuración de funcionalidades comunes con los routers.
* Configuración y funcionamiento de un [[Switch]] [[LAN]].

## Objetivos de la clase
* Configurar unas determinadas funcionalidades de un [[Switch]] que se configuran exactamente igual que algunas funcionalidades en los [[Router]]s Cisco.
* Configurar varias funcionalidades que son únicas de los [[Switch]]es y que no se usan en los [[Router]]s, o se configuran de forma distinta a como se hace en los [[Router]]s Cisco.

> **Diagrama detectado:** Ilustración conceptual sobre la implementación de redes basadas en [[Switch]]es mediante el uso de protocolos y tecnologías del [[Modelo TCP/IP]], garantizando tolerancia a fallos, escalabilidad, calidad de servicio y seguridad de las comunicaciones.

---

## Proteger la [[CLI]] de un [[Switch]]

De manera predeterminada no es necesario que un usuario en la consola suministre una contraseña para entrar en el modo de usuario o en el modo `enable`, ya que cualquiera con acceso físico a la consola del [[Switch]] o del [[Router]] podría restablecer las contraseñas en menos de 5 minutos usando los procedimientos que Cisco publica.

> **Diagrama detectado:** Esquema ilustrando que para alcanzar el modo `enable` mediante `vty` ([[Telnet]] o [[SSH]]), el [[Switch]] debe estar configurado con:
> - Una [[Dirección IP]]
> - Seguridad de inicio de sesión en las líneas `vty`
> - Una contraseña `enable`

---

## Configuración de una seguridad sencilla mediante contraseña

> **Captura de código:** Configuración básica de contraseñas y un nombre de host en la [[CLI]]:
> ```text
> Switch> enable
> Switch# configure terminal
> Switch(config)# enable secret cisco
> Switch(config)# hostname Emma
> Emma(config)# line console 0
> Emma(config-line)# password faith
> Emma(config-line)# login
> Emma(config-line)# exit
> Emma(config-line)# line vty 0 15
> Emma(config-line)# password love
> Emma(config-line)# login
> Emma(config-line)# end
> Emma#
> ```

---

## Mostrar la configuración actual del [[Switch]]

> **Captura de código:** Resultado del comando `show running-config` en la [[CLI]] mostrando el resumen de la configuración del [[Switch]], incluyendo la versión, nombre de host y el cifrado de la contraseña de enable.

---

## Cifrado de la contraseña

El cifrado y el comando `service password-encryption`

> **Captura de código:** Ejemplo de uso de `service password-encryption` para cifrar las contraseñas en texto claro dentro del archivo de configuración del [[Switch3]].

---

## Cifrado de la contraseña (desactivación)

El cifrado y el comando `no service password-encryption`

> **Captura de código:** Ejemplo de uso de `no service password-encryption` para deshabilitar el cifrado de contraseñas en texto plano en [[Switch3]].

---

## Las dos contraseñas del modo `enable`

* **Comando `enable password contraseña`:** Por defecto esta contraseña se muestra como de sólo texto en el archivo de configuración.
* **Comando `enable secret contraseña`:** Esta contraseña aparece como un valor de hash MD5 oculto en el archivo de configuración.
* Si se utilizan los dos comandos, la contraseña establecida con el comando `enable secret` define la contraseña que será requerida.

---

## Las dos contraseñas del modo `enable` (Ejemplos)

> **Captura de código:** Comandos de ayuda e interacción en la [[CLI]] para configurar `enable secret` y el uso posterior de `no enable secret`.

---

## Ajustes de consola y `vty`

Banners y su uso:
* Message of the Day (MOTD)
* Login
* Exec

---

## Configuración de banners

> **Captura de código:** Ejemplos de comandos para configurar banners en [[Switch1]]:
> ```text
> SW1(config)# banner #
> Enter TEXT message. End with the character '#'.
> Switch down for maintenance at 11PM Today #
> SW1(config)# banner login #
> Enter TEXT message. End with the character '#'.
> Unauthorized Access Prohibited!!!! #
> SW1(config)# banner exec Z
> Enter TEXT message. End with the character 'Z'.
> Company picnic at the park on Saturday
> Don't tell outsiders!
> Z
> ```

---

## Configuración de banners - resultado

> **Captura de código:** Salida en consola que muestra el despliegue secuencial de los banners configurados (MOTD, Login y Exec) al acceder al dispositivo [[SW1]].

---

## Los comandos `logging synchronous` y `exec-timeout`

Definición de los intervalos de inactividad de consola y cuándo visualizar los mensajes:

> **Captura de código:** Configuración aplicada en la línea de consola:
> ```text
> line console 0
> exec-timeout 0 0
> logging synchronous
> ```

---

## Configuración y funcionamiento de un [[Switch]] [[LAN]]

* Configuración de la dirección IP de un [[Switch]].
* Configuración de la interfaz (velocidad y modo dúplex).
* Configuración [[VLAN]].

---

## Configuración de la dirección IP de un [[Switch]]

Configuración estática de la dirección IP de un [[Switch]]:

> **Captura de código:** Comandos para configurar la [[VLAN 1]] de forma estática y definir la puerta de enlace predeterminada:
> ```text
> Emma# configure terminal
> Emma(config)# interface vlan 1
> Emma(config-if)# ip address 192.168.1.200 255.255.255.0
> Emma(config-if)# no shutdown
> Emma(config-if)# exit
> Emma(config)# ip default-gateway 192.168.1.1
> ```

---

## Configuración de la dirección IP de un [[Switch]] con DHCP

Configuración dinámica de la dirección IP de un [[Switch]] con [[DHCP]]:

> **Captura de código:** Comandos para solicitar una dirección IP por [[DHCP]] en la interfaz de gestión:
> ```text
> Emma# configure terminal
> Emma(config)# interface vlan 1
> Emma(config-if)# ip address dhcp
> Emma(config-if)# no shutdown
> Emma(config-if)# end
> ```

---

## Configuración dinámica de la dirección IP con [[DHCP]] - Resultados

> **Captura de código:** Salida de los comandos `show dhcp lease` y `show interface vlan 1` que verifican la asignación exitosa de la dirección IP dinámica.

---

## Configuración de las interfaces de un [[Switch]]

Configuración básica de una interfaz:

> **Captura de código:** Configuración de velocidad, modo dúplex y descripción para interfaces individuales y rangos:
> ```text
> Emma# configure terminal
> Emma(config)# interface FastEthernet 0/1
> Emma(config-if)# duplex full
> Emma(config-if)# speed 100
> Emma(config-if)# description Server1 connects here
> Emma(config-if)# exit
> Emma(config)# interface range FastEthernet 0/11 - 20
> Emma(config-if-range)# description end-users connect_here
> Emma(config-if-range)# end
> ```

---

## Configuración de las interfaces de un [[Switch]] - Resultados

> **Captura de código:** Salida del comando `show interfaces status` que muestra el estado operativo, velocidad, modo dúplex y asignación de VLAN para cada puerto del [[Switch]].

---

## Configuración [[VLAN]]

Red con un [[Switch]] y dos [[VLAN]]s:

> **Diagrama detectado:** Topología de red que muestra un [[Switch]] central (`SW1`) conectado a terminales mediante puertos FastEthernet, divididos en dos dominios de difusión o [[VLAN]]s distintas ([[VLAN 1]] y [[VLAN 2]]).

---

## Configuración [[VLAN]] (Verificación inicial)

Configuración de [[VLAN]]s y asignación de interfaces a las mismas:

> **Captura de código:** Salida del comando `show vlan brief` antes de crear nuevas [[VLAN]]s, mostrando todas las interfaces asignadas por defecto a la [[VLAN 1]].

---

## Configuración [[VLAN]] (Creación y asignación)

> **Captura de código:** Creación de una [[VLAN]] personalizada y asignación de puertos por rango:
> ```text
> SW1# configure terminal
> SW1(config)# vlan 2
> SW1(config-vlan)# name Freds-vlan
> SW1(config-vlan)# exit
> SW1(config)# interface range fastethernet 0/13 - 14
> SW1(config-if)# switchport access vlan 2
> SW1(config-if)# exit
> ```

---

## Configuración [[VLAN]] (Verificación de puertos)

> **Captura de código:** Salida de `show running-config` visualizando el modo de acceso y la asignación de la [[VLAN 2]] en los puertos `Fa0/13` y `Fa0/14`.

---

## Configuración [[VLAN]] (Resumen final)

> **Captura de código:** Salida final de `show vlan brief` comprobando que `Freds-vlan` ([[VLAN 2]]) se encuentra activa y contiene correctamente asignadas las interfaces `Fa0/13` y `Fa0/14`.

---

## Información [[DOCENTE]]

* Perfil Personal:
  * Ingeniero de Sistemas
  * Magister en Telecomunicaciones
  * Docente en Universidad Técnica de Machala
* Contacto:
  * Teléfono: [ID_OMITIDO]
  * Correo: [DOCENTE]@utmachala.edu.ec