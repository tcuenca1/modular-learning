---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Configuración de un Switch Ethernet

---

## Contenido a tratar

* Configuración de funcionalidades comunes con los routers.
* Configuración y funcionamiento de un [[Switch]] [[LAN]].

## Objetivos de la clase

* Configurar unas determinadas funcionalidades de un [[Switch]] que se configuran exactamente igual que algunas funcionalidades en los [[Router|routers]] [[Cisco]].
* Configurar varias funcionalidades que son únicas de los [[Switch|switches]] y que no se usan en los [[Router|routers]], o se configuran de forma distinta a como se hace en los [[Router|routers]] [[Cisco]].

> **Imagen detectada:** Ilustración conceptual sobre la implementación de redes basadas en [[Switch|switches]] mediante protocolos y tecnologías del modelo [[TCP/IP]], garantizando tolerancia a fallos, escalabilidad, calidad de servicio y seguridad en las comunicaciones.

---

## Proteger la [[CLI]] de un [[Switch]]

De manera predeterminada no es necesario que un usuario en la consola suministre una contraseña para entrar en el modo de usuario o en el modo enable, ya que cualquiera con acceso físico a la consola del [[Switch]] o del [[Router]] podría restablecer las contraseñas en menos de 5 minutos usando los procedimientos que [[Cisco]] publica.

Para alcanzar el modo enable mediante **vty** ([[Telnet]] o [[SSH]]), el [[Switch]] debe estar configurado con:
* Una dirección [[IP]]
* Seguridad de inicio de sesión en las líneas vty
* Una contraseña enable

---

## Configuración de una seguridad sencilla mediante contraseña

Configuración básica de contraseñas y un nombre de host:

> **Captura de código detectada:** Comandos de consola de [[Cisco]] para habilitar el modo privilegiado, configurar el nombre de host (`hostname Emma`), configurar la contraseña de consola (`line console 0`, `password faith`, `login`) y configurar el acceso remoto vty (`line vty 0 15`, `password love`, `login`).

---

## Mostrar la configuración actual del [[Switch]]

> **Captura de código detectada:** Salida del comando `show running-config` en la cual se muestra la configuración actual del equipo, incluyendo la versión del sistema, nombre de host y las contraseñas cifradas.

---

## Cifrado de la contraseña

El cifrado y el comando `service password-encryption`

> **Captura de código detectada:** Ejemplos de uso del comando `service password-encryption` para aplicar cifrado tipo 7 a las contraseñas en texto claro dentro de la configuración en ejecución.

---

## Cifrado de la contraseña

El cifrado y el comando `no service password-encryption`

> **Captura de código detectada:** Uso del comando `no service password-encryption` para desactivar el cifrado y volver a texto claro o configurar contraseñas específicas en las líneas vty.

---

## Las dos contraseñas del modo enable

* Comando `enable password contraseña`: por defecto esta contraseña se muestra como de sólo texto en el archivo de configuración. (Ejemplo: `enable password cisco123` -> Solo texto).
* Comando `enable secret contraseña`: esta contraseña aparece como un valor de hash [[MD5]] oculto en el archivo de configuración. (Ejemplo: `enable secret miClaveSegura` -> Hash MD5).
* Si se utilizan los dos comandos, la contraseña establecida con el comando `enable secret` define la contraseña que será requerida. (Ejemplo: `enable password cisco123` y `enable secret segura456` -> La contraseña del comando enable secret es requerida).

---

## Las dos contraseñas del modo enable (continuación)

El cifrado y el comando `enable secret`

> **Captura de código detectada:** Ayuda interactiva del comando `enable secret ?` mostrando opciones de cifrado (0 para texto plano, 5 para cifrado [[MD5]]), así como comandos para eliminar el secreto (`no enable secret`).

---

## Ajustes de consola y vty

Banners y su uso:
* Message of the Day ([[MOTD]])
* Login
* Exec

---

## Configuración de banners

> **Captura de código detectada:** Ejemplos de configuración de banners en un [[Switch]]:
> - `banner # ... #` (MOTD)
> - `banner login # ... #` (Acceso no autorizado prohibido)
> - `banner exec Z ... Z` (Mensaje para sesiones ejecutivas)

---

## Configuración de banners - resultado

> **Captura de código detectada:** Pantalla de consola que muestra la salida generada por los banners configurados previamente al acceder a la interfaz del [[Switch]] (`SW1 con0 is now available`, mensajes MOTD, login y exec).

---

## Los comandos `logging synchronous` y `exec-timeout`

Definición de los intervalos de inactividad de consola y cuándo visualizar los mensajes:

> **Captura de código detectada:** Bloque de configuración bajo `line console 0` utilizando `exec-timeout 0 0` y `logging synchronous`.

---

## Configuración y funcionamiento de un [[Switch]] [[LAN]]

* Configuración de la dirección [[IP]] de un [[Switch]].
* Configuración de la interfaz (velocidad y modo dúplex).
* Configuración [[VLAN]].

---

## Configuración de la dirección [[IP]] de un [[Switch]]

Configuración estática de la dirección [[IP]] de un [[Switch]]:

> **Captura de código detectada:** Configuración de la interfaz lógica de gestión mediante `interface vlan 1`, asignación de dirección [[IP]] (`ip address 192.168.1.200 255.255.255.0`), habilitación con `no shutdown` y definición de la puerta de enlace predeterminada (`ip default-gateway 192.168.1.1`).

---

## Configuración de la dirección [[IP]] de un [[Switch]] (Dinámica)

Configuración dinámica de la dirección [[IP]] de un [[Switch]] con [[DHCP]]:

> **Captura de código detectada:** Comandos para solicitar configuración automática mediante `ip address dhcp` en la interfaz vlan 1 y mensajes de confirmación de asignación de dirección [[IP]] mediante [[DHCP]].

---

## Configuración de la dirección [[IP]] de un [[Switch]] (Resultados [[DHCP]])

> **Captura de código detectada:** Salida de los comandos `show dhcp lease` y `show interface vlan 1` detallando la concesión [[IP]], puerta de enlace, máscara de subred y estado operativo de la interfaz virtual de gestión.

---

## Configuración de las interfaces de un [[Switch]]

Configuración básica de una interfaz:

> **Captura de código detectada:** Configuración individual de interfaz (`interface FastEthernet 0/1`, `duplex full`, `speed 100`, `description Server1 connects here`) y configuración por rangos (`interface range FastEthernet 0/11 - 20`, `description end-users connect_here`).

---

## Configuración de las interfaces de un [[Switch]] - resultados

> **Captura de código detectada:** Tabla de estado devuelta por el comando `show interfaces status`, mostrando el nombre, estado de conexión ([[connected]] / [[notconnect]]), [[VLAN]] asignada, modo dúplex y velocidad de cada puerto físico del equipo.

---

## Configuración [[VLAN]]

Red con un [[Switch]] y dos [[VLANs]]:

> **Diagrama detectado:** Topología de red que muestra un [[Switch]] central (`SW1`) conectado a dispositivos finales agrupados en dos dominios virtuales diferentes: [[VLAN1]] (puertos Fa0/11, Fa0/12) y [[VLAN2]] (puertos Fa0/13, Fa0/14).

---

## Configuración [[VLAN]] (Asignación de interfaces)

> **Captura de código detectada:** Resultado del comando `show vlan brief` donde se observa el estado inicial de las interfaces asociadas por defecto a la [[VLAN]] 1, junto con las [[VLAN]] especiales del sistema (fddi, token-ring, etc.).

---

## Configuración [[VLAN]] (Creación y asignación)

> **Captura de código detectada:** Comandos ejecutados en el modo de configuración global para crear una [[VLAN]] (`vlan 2`, `name Freds-vlan`), seleccionar un rango de puertos (`interface range fastethernet 0/13 - 14`) y asignarlos mediante el comando de acceso (`switchport access vlan 2`).

---

## Configuración [[VLAN]] (Verificación de configuración)

> **Captura de código detectada:** Salida del comando `show running-config` verificando los parámetros aplicados a los puertos FastEthernet 0/13 y FastEthernet 0/14 con respecto al acceso a la [[VLAN]] 2 y el modo de puerto de acceso (`switchport mode access`).

---

## Configuración [[VLAN]] (Resumen final)

> **Captura de código detectada:** Salida final del comando `show vlan brief` mostrando de manera explícita que las interfaces `Fa0/13` y `Fa0/14` se encuentran activas y asignadas correctamente a la [[VLAN]] 2 bajo el nombre `Freds-vlan`.

---

## Información Docente

* Perfil Personal:
  * Ingeniero de Sistemas
  * Magister en Telecomunicaciones
  * Docente en Universidad Técnica de Machala ([DOCENTE])

* Contacto:
  * Teléfono: [ID_OMITIDO]
  * Correo electrónico: [ESTUDIANTE] / [DOCENTE]