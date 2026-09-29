---
materia: Tecnologias de Conmutacion I
tipo: actividad
fecha_procesamiento: 2026-09-28
tags: [tecnologias_de_conmutacion_i, actividad, ingesta_ia]
---

# [[Tecnologias de Conmutacion I]] - Configuración Básica del Switch

## Datos Informativos
* **UNIVERSIDAD:** Universidad Técnica de Machala
* **FACULTAD:** Facultad de Ingeniería Civil
* **LABORATORIO:** Laboratorio de Telecomunicaciones y Redes de Datos
* **NÚMERO DE PRÁCTICA:** 6.5-01
* **NOMBRE DE LA PRÁCTICA:** Configuración Básica del [[Switch]].
* **ESTUDIANTES:** [ESTUDIANTE]

---

## 1. Datos Informativos
* **CARRERA:** Tecnologías de la Información
* **ASIGNATURA:** [[Tecnologias de Conmutacion I|Tecnologías de Conmutación I]]
* **CICLO/NIVEL:** Sexto

---

## 2. Fundamentación
Los [[Switch|switches Cisco]] se pueden configurar con una dirección IP especial, conocida como "**interfaz virtual de switch**" ([[SVI]]). La [[SVI]] o dirección de administración se puede usar para el acceso remoto al switch a fin de ver o configurar parámetros. Si se asigna una dirección IP a la [[SVI]] de la [[VLAN]] 1, de manera predeterminada, todos los puertos en la [[VLAN]] 1 tienen acceso a la dirección IP de administración de [[SVI]].

---

## 3. Resultados de Aprendizaje
Realiza, guarda y verifica las tareas iniciales de configuración de un switch incluyendo la gestión del acceso remoto.

---

## 4. Objetivos Específicos
* Acceder a un [[Switch|switch Cisco]] utilizando los métodos de acceso de consola para la verificación de su configuración predeterminada y la configuración de los parámetros básicos.

---

## 5. Equipos, Materiales e Insumos
* Computadora de escritorio (con Windows 7 o superior).
* Software de simulación de redes [[Cisco PacketTracer]] v5.0 o superior.

---

## 6. Procedimiento

1. Realizar el cableado de red tal como se muestra en la topología.
   * a. Realice el cableado de la conexión de consola tal como se muestra en la topología. En esta instancia, no conecte el cable directo Ethernet de la PC-A.

> **Diagrama detectado:** Topología de red en Packet Tracer que muestra un switch (etiquetado como `S1` / `Switch0`) conectado mediante un cable de consola a una PC (`PC-A` / `PCO`), y un enlace Ethernet adicional entre el switch y la computadora.

   * b. Con Tera Term u otro programa de emulación de terminal, cree una conexión de consola de la PC-A al switch.

> **Pregunta:** ¿Por qué debe usar una conexión de consola para configurar inicialmente el switch? ¿Por qué no es posible conectarse al switch a través de [[Telnet]] o [[SSH]]?  
> **Respuesta:** Porque en su configuración de fábrica no tiene asignada una IP por la cual se pueda acceder con [[Telnet]] o [[SSH]]. Para poder usar esos protocolos se requiere de su configuración por consola.

---

### 2. Verificar la configuración predeterminada del switch

En este paso, examinará la configuración predeterminada del switch, como la configuración actual del switch, la información de [[IOS]], las propiedades de las interfaces, la información de la [[VLAN]] y la memoria flash. No debería haber contraseñas ni direcciones IP configuradas.

* **a. Examine el archivo de configuración activa actual.**
  * ¿Cuántas interfaces FastEthernet tiene el switch? -> Tiene 24 interfaces FastEthernet.
  * ¿Cuántas interfaces GigabitEthernet tiene el switch? -> Tiene 2 interfaces GigabitEthernet.
  * ¿Cuál es el rango de valores que se muestra para las líneas vty? -> Hay dos rangos, el primero de 0 a 4, y el segundo de 5 a 15.

* **b. Examine el archivo de configuración de inicio en la NVRAM.**
  * ¿Por qué aparece el mensaje `(startup-config is not present)`? -> Porque no se ha guardado ningún archivo de configuración inicial, solo se ha trabajado en [[RAM]].

* **c. Examine las características de la SVI para la [[VLAN]] 1.**
  * ¿Hay alguna dirección IP asignada a la [[VLAN]] 1? -> No, por defecto no tiene asignada una IP.
  * ¿Cuál es la dirección MAC de esta SVI? -> `00e0.f9a6.0378` (bia `00e0.f9a6.0378`).
  * ¿Está activa esta interfaz? -> No se encuentra activa, administratively down.

* **d. Examine las propiedades IP de la [[VLAN]] 1 SVI.**
  * ¿Qué resultado ve?
    ```text
    Vlan1 is administratively down, line protocol is down
     Hardware is CPU Interface, address is 00e0.f9a6.0378 (bia 00e0.f9a6.0378)
     MTU 1500 bytes, BW 100000 Kbit, DLY 1000000 usec,
     reliability 255/255, txload 1/255, rxload 1/255
     Encapsulation ARPA, loopback not set
     ARP type: ARPA, ARP Timeout 04:00:00
     Last input 21:40:21, output never, output hang never
     Last clearing of "show interface" counters never
     Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
     Queueing strategy: fifo
     Output queue: 0/40 (size/max)
     5 minute input rate 0 bits/sec, 0 packets/sec
     5 minute output rate 0 bits/sec, 0 packets/sec
     1682 packets input, 530955 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicast)
     ...
    ```

* **e. Conecte el cable Ethernet de la PC-A al puerto 6 en el switch y examine las propiedades IP de la [[VLAN]] 1 SVI.**
  * Aguarde un momento para que el switch y la computadora negocien los parámetros de dúplex y velocidad.
  * ¿Qué resultado ve? -> El indicador de conexión pasó de naranja a verde luego de unos segundos.

* **f. Examine la información de la versión del [[IOS]] de Cisco del switch.**
  * ¿Cuál es la versión del [[IOS]] de Cisco que está ejecutando el switch? -> Version 15.0(2)SE4.
  * ¿Cuál es el nombre del archivo de imagen del sistema? -> `System image file is "flash:c2960-lanbasek9-mz.150-2.SE4.bin"`
  * ¿Cuál es la dirección MAC base de este switch? -> `Base ethernet MAC Address : 00:E0:F9:A6:03:78`

* **g. Examine las propiedades predeterminadas de la interfaz FastEthernet que usa la PC-A.**
  * ¿La interfaz está activa o desactivada? -> `FastEthernet0/6 is up.`
  * ¿Qué haría que una interfaz se active? -> Conectar un cable ethernet hacia un dispositivo final con tarjeta NIC.
  * ¿Cuál es la dirección MAC de la interfaz? -> `0060.2f26.6406` (bia `0060.2f26.6406`).
  * ¿Cuál es la configuración de velocidad y de dúplex de la interfaz? -> Full-duplex, 100Mb/s.

* **h. Examine la configuración [[VLAN]] predeterminada del switch.**
  * ¿Cuál es el nombre predeterminado de la [[VLAN]] 1? -> Su nombre es `default`.
  * ¿Qué puertos hay en esta VLAN? -> Todos los puertos físicos del switch pertenecen a esta VLAN.
  * ¿La [[VLAN]] 1 está activa? -> Sí, se encuentra activa.
  * ¿Qué tipo de VLAN es la VLAN predeterminada? -> Es una [[VLAN]] ethernet.

* **i. Examine la memoria flash.**
  Los archivos poseen una extensión, tal como `.bin`, al final del nombre del archivo. Los directorios no tienen una extensión de archivo.
  * ¿Cuál es el nombre de archivo de la imagen de [[IOS]] de Cisco? -> `c2960-lanbasek9-mz.150-2.SE4.bin`

---

### 3. Configurar los parámetros básicos de los dispositivos de red

| Dispositivo | Interfaz | Dirección IP | Máscara de subred | Gateway predeterminado |
| :--- | :--- | :--- | :--- | :--- |
| S1 | [[VLAN]] 1 | `192.168.1.2` | `255.255.255.0` | `192.168.1.1` |
| PC-A | NIC | `192.168.1.10` | `255.255.255.0` | `192.168.1.1` |

* **a. Configurar los parámetros básicos del switch, incluidos:**
  * Nombre de host: `S1`
  * Contraseña de consola: `cisco`
  * Contraseña de las líneas vty: `cisco`
  * Contraseña enable password: `cisco`
  * Contraseña enable secret: `class`
  * Mensaje MOTD: `Mantenimiento programado para el fin de semana de 08:00 a 14:00`
  * Se debe activar el servicio de encriptación de contraseñas, la dirección IP de administración y el acceso por [[Telnet]].

* **b. Configurar una dirección IP en la PC-A.**
  * Asigne a la computadora la dirección IP y la máscara de subred.

---

### 4. Comprobar la conectividad de extremo a extremo con [[ping]]
* **a.** En el símbolo del sistema de la PC-A, haga [[ping]] a la dirección de administración de [[SVI]] del S1. Debido a que la PC-A debe resolver la dirección MAC del S1 mediante [[ARP]], es posible que se agote el tiempo de espera del primer paquete. Si los resultados del ping siguen siendo incorrectos, resuelva los problemas de configuración de los parámetros básicos del dispositivo. Revise el cableado físico y el direccionamiento lógico, si es necesario.

---

## 7. Resultados Esperados
Se espera la correcta configuración de los dispositivos de la topología de red. Las evidencias son: archivo de configuración, capturas de pantalla de ejecución de comandos, resultados de las verificaciones, configuraciones, pruebas.

> **Captura de código y consola detectada:** Se muestran capturas de comandos ejecutados en el CLI del switch Cisco (`S1`), incluyendo configuración de contraseñas (`enable secret`, `line console 0`, `line vty 0 15`), asignación de IP a la interfaz `vlan 1`, comandos `copy running-config startup-config`, así como trazas de comandos `ping 192.168.1.2` desde la interfaz de comandos de la PC en Packet Tracer evidenciando pérdida inicial por [[ARP]] y posterior éxito en los paquetes subsecuentes.

---

## 8. Bibliografía
* Ariganello, Ernesto (2014). Redes Cisco. México: Alfaomega.