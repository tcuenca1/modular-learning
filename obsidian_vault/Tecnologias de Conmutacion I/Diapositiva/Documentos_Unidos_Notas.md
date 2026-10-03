---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Funcionamiento de los [[Switch Cisco LAN]]

---

## Contenido a tratar y Objetivos de la clase

**Contenido a tratar:**
- Acceso a la [[CLI]] del switch [[Cisco]].
- Configuración del software [[Cisco IOS]].

**Objetivos de la clase:**
- Examinar los [[Switch Cisco Catalyst|switches Cisco]] y cómo acceder a la interfaz de línea de comandos ([[CLI]]) desde la que es posible enviar instrucciones al switch.
- Explicar cómo se indica al switch los diferentes parámetros operacionales utilizando la [[CLI]].

> **Diagrama detectado:** Ilustración conceptual que representa la implementación de redes basadas en switches mediante protocolos y tecnologías del [[Modelo TCP/IP]], garantizando tolerancia a fallos, escalabilidad, calidad de servicio ([[QoS]]) y seguridad en las comunicaciones.

---

## [[Switch Cisco Catalyst]] y el [[Switch 2960]]

> **Imagen detectada:** Vista frontal física de varios modelos de switches [[Cisco Catalyst]] apilados, mostrando sus puertos [[Fast Ethernet]] / [[Gigabit Ethernet]] y puertos de consola.

### Características de los Switches [[Cisco]] (Nivel de Acceso)
- Diseñados para redes de sucursales de empresas.
- Funcionan como switches de nivel de acceso ([[Capa 2 del Modelo OSI]]).
- Velocidades de envío entre 16 Gbps y 32 Gbps.
- Administración basada en Web y [[CLI]] de [[Cisco]].
- Funciones LAN avanzadas ([[QoS]], [[ACL]]).
- Conectividad [[Fast Ethernet]] y [[Gigabit Ethernet]].
- Hasta 48 puertos 10/100 o puertos 10/100/1000 (Sin PoE).

---

## Secuencia de Arranque de un Switch

> **Diagrama detectado:** Pirámide escalonada que muestra los 5 pasos del arranque de un switch:
> 1. **Ejecutar POST:** El switch realiza pruebas de diagnóstico para verificar la funcionalidad del hardware.
> 2. **Cargar el cargador de arranque:** Carga el software del cargador de arranque para los siguientes pasos de inicialización.
> 3. **Inicializar CPU:** Inicializa los registros de la CPU para la operación eficiente.
> 4. **Iniciar sistema de archivos:** El switch inicia el sistema de archivos en la placa del sistema.
> 5. **Cargar IOS:** El switch carga la imagen de software [[Cisco IOS]] y toma el control.

---

## Indicadores LED de un Switch

- **LED del sistema (SYST):** Muestra si el sistema recibe alimentación y funciona correctamente.
- **LED de fuente de alimentación redundante (RPS):** Muestra el estado de RPS.
- **LED de estado del puerto (STAT):** Cuando está verde, indica que el modo de estado del puerto está seleccionado (valor predeterminado). El estado se entiende por la luz de cada puerto.
- **LED de modo dúplex del puerto (DUPLX):** Si es verde, indica que se seleccionó el modo dúplex.
- **LED de velocidad del puerto (SPEED):** Si está verde, indica que se seleccionó el modo de velocidad.
- **LED de alimentación a través de Ethernet (PoE):** Presente si el switch es compatible con [[PoE]]. Indica el estado de energía de los puertos.
- *Nota:* El botón **MODE** se utiliza para alternar entre los modos: STAT, DUPLX, SPEED y PoE.

---

## Acceso a la [[CLI]] del [[Cisco IOS]]

> **Diagrama detectado:** Esquema de conexión física y lógica para acceder a la [[CLI]] de un switch [[Cisco 2960]]:
> - Conexión local mediante **Cable de Consola** (Serial o USB a puerto RJ-45 o USB de consola) accediendo al **User Mode**.
> - Conexión remota a través de una red [[TCP/IP Network]] utilizando protocolos como [[Telnet]] y [[SSH]].

### Tipos de Conexión de Consola
1. **Cable Rollover** desde puerto serial de PC a puerto **RJ-45 Console** del switch (SW1).
2. **Cable Rollover + Conversor USB + Cable USB** conectado al puerto USB de consola o puerto serie virtual (SW2).
3. **Cable USB directo** desde puerto USB de PC a puerto **USB Console** del switch (SW3).

---

## Configuración y Seguridad de la Consola y [[Telnet]]

### Configuración del Terminal (ej. [[Tera Term]])
- Puerto: COM1, Baud rate: 9600, Data: 8 bit, Parity: none, Stop: 1 bit, Flow control: none.

### Tabla de Configuración de Contraseñas de Acceso
| Access From | Password Type | Sample Configuration |
| :--- | :--- | :--- |
| **Console** | Console password | `line console 0`<br>`login`<br>`password <contraseña>` |
| **Telnet** | vty password | `line vty 0 15`<br>`login`<br>`password <contraseña>` |

---

## Modos de Usuario y [[Privileged EXEC Mode|Enable (Privilegiado)]]

> **Diagrama detectado:** Diagrama de transiciones entre modos de ejecución:
> - Las conexiones de consola, [[Telnet]] y [[SSH]] aterrizan inicialmente en el **User Mode** (Modo Usuario).
> - Mediante el comando `enable` se transiciona al **Enable Mode** (Modo Privilegiado).
> - Mediante el comando `disable` se retorna del modo privilegiado al modo usuario.

---

## Funcionalidades de Ayuda de la [[CLI]] y Navegación de Modos

### Ayuda sobre Comandos ([[Cisco IOS]])
- `?` : Muestra la lista de comandos disponibles.
- `help` : Descripción general del sistema de ayuda.
- `command ?` : Muestra los subcomandos o argumentos válidos.
- `com?` : Autocompleta o muestra comandos que inicien con "com".
- `command parm?` : Ayuda en línea para parámetros específicos.
- `command parm <Tab>` : Autocompleta el comando o parámetro.

### Modos de Configuración Comunes
- **Global Config Mode:** `hostname(config)#` (Se accede con `configure terminal`).
- **Line Config Mode:** `hostname(config-line)#` (Se accede con `line console 0` o `line vty 0 15`).
- **Interface Config Mode:** `hostname(config-if)#` (Se accede con `interface type number`).
- Para salir a niveles superiores se usa `exit`, y para regresar directamente al modo privilegiado se usa `end` o `Ctrl+Z`.

---

## Almacenamiento y Archivos de Configuración

> **Diagrama detectado:** Gráfico de los tipos de memoria de un switch [[Cisco]]:
> - **RAM:** *Working Memory and Running Configuration* (Memoria de trabajo y configuración en ejecución).
> - **Flash:** Almacena el software *[[Cisco IOS]]*.
> - **ROM:** Almacena el programa de arranque (*Bootstrap Program*).
> - **NVRAM:** Almacena la configuración de inicio (*Startup Configuration*).

### Archivos Principales
- **Startup-config:** Almacena la configuración inicial que se utiliza siempre que el switch recarga el [[Cisco IOS]] (**NVRAM**).
- **Running-config:** Almacena los comandos de configuración actualmente utilizados. Cambia dinámicamente al introducir comandos en el modo de configuración (**RAM**).

---

## Copia de Archivos de Configuración

> **Diagrama detectado:** Flujo de comandos para respaldo y transferencia de configuraciones:
> - `copy running-config startup-config` (de RAM a NVRAM).
> - `copy startup-config running-config` (de NVRAM a RAM).
> - Comandos de transferencia remota con servidor [[TFTP]]: `copy tftp running-config`, `copy running-config tftp`, `copy tftp startup-config`, `copy startup-config tftp`.

---

## Configuración de Seguridad y Ajustes Adicionales

### Proteger la CLI y Contraseñas
- **Enable Secret vs Enable Password:**
  - `enable password <contraseña>`: Se muestra en texto plano por defecto.
  - `enable secret <contraseña>`: Se almacena como un valor de hash [[MD5]] oculto y seguro. Si se usan ambos, `enable secret` tiene prioridad.
- **Cifrado de contraseñas:**
  - `service password-encryption`: Cifra todas las contraseñas en texto plano del archivo de configuración.
  - `no service password-encryption`: Desactiva el cifrado.

### Banners
- `banner motd # Mensaje del día #`
- `banner login # Mensaje de inicio de sesión #`
- `banner exec # Mensaje de modo EXEC #`

### Comandos de Línea Útiles
- `logging synchronous`: Evita que los mensajes de consola interrumpan el comando que se está escribiendo.
- `exec-timeout 0 0`: Desactiva el cierre de sesión por inactividad.

---

## Configuración de un Switch LAN

### Configuración de Dirección IP (Interfaz [[VLAN]] 1)
- **Estática:**
  ```text
  configure terminal
  interface vlan 1
  ip address 192.168.1.200 255.255.255.0
  no shutdown
  exit
  ip default-gateway 192.168.1.1
  ```
- **Dinámica ([[DHCP]]):**
  ```text
  configure terminal
  interface vlan 1
  ip address dhcp
  no shutdown
  end
  ```
  *(Se verifica con el comando `show dhcp lease` o `show interface vlan 1`)*.

### Configuración de Interfaces Físicas
```text
configure terminal
interface FastEthernet 0/1
duplex full
speed 100
description Server1 connects here
exit
interface range FastEthernet 0/11 - 20
description end-users connect_here
end
```
*(Verificación mediante `show interfaces status`)*.

### Configuración de [[VLAN]]s
```text
configure terminal
vlan 2
name Freds-vlan
exit
interface range fastethernet 0/13 - 14
switchport access vlan 2
switchport mode access
end
```
*(Verificación con `show vlan brief`)*.

---

## Conceptos de Conmutación LAN Ethernet

### Evolución Histórica: Hubs, Puentes y Switches
- **Hub (Capa 1):** Comparte el mismo dominio de colisión y ancho de banda en una red basada en bus o estrella repetidora.
- **Bridge / Puente (Capa 2):** Divide el segmento en dominios de colisión separados, reduciendo las colisiones.
- **Switch (Capa 2):** Cada puerto es un dominio de colisión independiente de alta velocidad (ej. 100 Mbps o más), operando con conmutación basada en hardware y direcciones MAC.

### Lógica de Conmutación del Switch
1. **Decidir envío o filtrado:** Envía la trama por el puerto adecuado o la descarta basándose en la dirección MAC de destino y la tabla MAC.
2. **Aprendizaje de direcciones MAC:** Examina y registra la dirección MAC de origen de cada trama entrante y el puerto por el que ingresó.
3. **Prevención de bucles:** Crea un entorno libre de bucles en Capa 2 utilizando [[STP (Spanning Tree Protocol)|STP]].

### Inundación de Tramas ([[Flooding]]) y Temporizadores
- Si el switch no conoce la dirección MAC de destino (Unidifusión desconocida), realiza una **inundación** enviando la trama por todas las interfaces excepto por la que ingresó.
- Utiliza un **temporizador de inactividad** (*aging timer*) para eliminar entradas de la tabla MAC que dejen de recibir tráfico tras un tiempo determinado.

### Métodos de Procesamiento Interno
- **Store-and-Forward (Almacenamiento y envío):** Recibe la trama completa, verifica el CRC ([[FCS]]) antes de reenviarla. Garantiza la integridad pero introduce mayor latencia.
- **Cut-Through (Corte):** Comienza a reencaminar la trama tan pronto como lee la dirección MAC de destino. Reduce la latencia pero puede propagar tramas dañadas.

---

## Terminología de Diseño LAN (Arquitectura de 3 Capas de Cisco)

> **Diagrama detectado:** Modelo jerárquico de diseño de red compuesto por tres capas:
> 1. **Capa de Acceso (*Access*):** Proporciona conectividad y acceso a los dispositivos de usuario final (Workgroup Access).
> 2. **Capa de Distribución (*Distribution*):** Agrega los switches de acceso y provee políticas de conectividad (Policy-based Connectivity).
> 3. **Capa de Núcleo (*Core*):** Conecta los bloques de distribución con conmutación de alta velocidad (*High-Speed Switching*).