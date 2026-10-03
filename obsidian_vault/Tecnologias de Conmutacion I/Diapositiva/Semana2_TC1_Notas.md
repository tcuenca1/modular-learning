---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

# [[Tecnologias de Conmutacion I]] - Funcionamiento de los [[Switch|switches]] [[Cisco]] [[LAN]]

## Contenido a tratar y Objetivos de la clase

- Acceso a la [[CLI]] del [[Switch|switch]] [[Cisco]].
- Configuración del software [[Cisco IOS]].

**Objetivos de la clase:**
- Examinar los [[Switch|switches]] [[Cisco]] y cómo acceder a la interfaz de línea de comandos ([[CLI]]) desde la que es posible enviar instrucciones al [[Switch|switch]].
- Explicar cómo se indica al [[Switch|switch]] los diferentes parámetros operacionales utilizando la [[CLI]].

> **Diagrama detectado:** Ilustración conceptual que muestra una red basada en [[Switch|switches]], mediante el uso de protocolos y tecnologías del modelo [[TCP/IP]], garantizando la tolerancia a fallos, la escalabilidad, la calidad de servicio y seguridad de las comunicaciones.

---

## [[Switch|Switches]] [[Cisco]] [[Catalyst]] y el [[Switch|switch]] 2960

> **Imagen detectada:** Vista frontal de múltiples modelos de [[Switch|switches]] [[Cisco Catalyst]] apilados, mostrando la disposición de los puertos físicos de red, paneles de LED y puertos de consola.

---

## [[Switch|Switches]] [[Cisco]]

- Para redes de sucursales de empresas.
- Es un [[Switch|switch]] de nivel de acceso.
- Velocidades de envío entre 16 Gbps a 32 Gbps.
- Administración basada en la web y [[CLI]] (Interfaz de línea de comandos) de [[Cisco]].
- Funciones [[LAN]] avanzadas ([[QoS]], [[ACL]]).
- Conectividad [[Fast Ethernet]] y [[Gigabit Ethernet]].
- Hasta 48 puertos 10/100 o puertos 10/100/1000 (No [[PoE]]).

---

## Secuencia de arranque de un [[Switch|switch]]

> **Diagrama de flujo detectado:** Pasos de inicialización del [[Switch|switch]] representados en una estructura de escalera ascendente:
> 1. **Ejecutar [[POST]]:** El [[Switch|switch]] realiza pruebas de diagnóstico para verificar la funcionalidad del hardware.
> 2. **Cargar el cargador de arranque:** El [[Switch|switch]] carga el software del cargador de arranque para los siguientes pasos de inicialización.
> 3. **Inicializar [[CPU]]:** El [[Switch|switch]] inicializa los registros de la [[CPU]] para la operación eficiente.
> 4. **Iniciar sistema de archivos:** El [[Switch|switch]] inicia el sistema de archivos en la placa del sistema.
> 5. **Cargar [[Cisco IOS|IOS]]:** El [[Switch|switch]] carga la imagen de software [[Cisco IOS|IOS]] y toma de control.

---

## Indicadores [[LED]] de un [[Switch|switch]]

- **[[LED]] del sistema (**[[SYST]]**):** muestra si el sistema recibe alimentación y funciona correctamente.
- **[[LED]] de fuente de alimentación redundante (**[[RPS]]**):** muestra el estado de [[RPS]].
- **[[LED]] de estado del puerto (**[[STAT]]**):** cuando está verde, indica que el modo de estado del puerto está seleccionado, que es el valor predeterminado. El estado del puerto puede ser entendido por la luz asociada a cada puerto.
- **[[LED]] de modo dúplex del puerto:** cuando el [[LED]] es de color verde, indica que se seleccionó el modo dúplex del puerto. El dúplex de puerto se puede entender por la luz asociada a cada puerto.
- **[[LED]] de velocidad del puerto (**[[SPEED]]**):** cuando está verde, indica que se ha seleccionado el modo de velocidad del puerto. La velocidad del puerto se puede entender por la luz asociada a cada puerto.
- **[[LED]] de alimentación a través de Ethernet (**[[PoE]]**):** Presente si el [[Switch|switch]] es compatible con [[PoE]]. Indica el estado [[PoE]] de los puertos del [[Switch|switch]].

El botón **Mode** se utiliza para moverse entre los diferentes modos: **[[STAT]]**, **DUPLX**, **[[SPEED]]** y **[[PoE]]**.

---

## Acceso a la [[CLI]] del [[Cisco IOS]]

> **Diagrama detectado:** Esquema de conexión al [[Switch|switch]] 2960 mediante un cable de consola conectado a un puerto Serial o USB de una computadora, o de forma remota a través de una red [[TCP/IP]] utilizando [[Telnet]] y [[SSH]]. Muestra la transición al modo de usuario (*User Mode*).

---

## Acceso a la [[CLI]] del [[Cisco IOS]] (Cont.)

> **Diagrama detectado:** Tres tipos de conexiones de consola a un [[Switch|switch]]:
> - **SW1:** Conexión mediante cable de consola rollover conectado al puerto serial de la PC.
> - **SW2:** Conexión mediante cable rollover con conversor USB y cable USB a puerto USB de la PC.
> - **SW3:** Conexión directa mediante cable USB consola al puerto USB de la PC.

---

## Acceso a la [[CLI]] desde la consola

> **Captura de pantalla detectada:** Ventana de configuración de un emulador de terminal (como Tera Term) mostrando los parámetros del puerto serie (Baud rate: 9600, Data: 8 bit, Parity: none, Stop: 1 bit, Flow control: none) junto con una sesión de consola activa ejecutando el comando `show mac address-table dynamic`.

---

## Seguridad de la contraseña para acceder a la [[CLI]]

| Access From | Password Type | Sample Configuration |
| :--- | :--- | :--- |
| Console | Console password | `line console 0`<br>`login`<br>`password` |
| Telnet | vty password | `line vty 0 15`<br>`login`<br>`password` |

---

## Modos de usuario y enable (privilegiado)

> **Diagrama detectado:** Flujo de navegación entre el *User Mode* y el *Enable Mode* (Modo Privilegiado) mediante el comando `enable` y el comando de retorno `disable`, accesibles desde la consola, [[Telnet]] o [[SSH]].

---

## Funcionalidades de ayuda de la [[CLI]]

> **Tabla de comandos de ayuda:**
> - `?`
> - `help`
> - `command ?`
> - `com?`
> - `command parm?`
> - `command parm<Tab>`
> - `command parm1 ?`

---

## Configuración del software [[Cisco IOS]]

> **Diagrama detectado:** Mapa de navegación entre el Modo Usuario, Modo Enable (Privilegiado) y Modo Configuración utilizando los comandos `enable`, `disable`, `configure terminal`, y `end` o `Ctrl+Z`.

---

## Submodos de configuración y contextos

> **Captura de código / Terminal detectada:**
> ```text
> Switch#configure terminal
> Switch(config)#hostname [ESTUDIANTE]
> [ESTUDIANTE](config)#line console 0
> [ESTUDIANTE](config-line)#password hope
> [ESTUDIANTE](config-line)#interface FastEthernet 0/1
> [ESTUDIANTE](config-if)#speed 100
> [ESTUDIANTE](config-if)#exit
> [ESTUDIANTE](config)#
> ```

---

## Submodos de configuración y contextos (cont.)

| Prompt | Name of Mode | Context-setting Command(s) to Reach This Mode |
| :--- | :--- | :--- |
| `hostname(config)#` | Global | None—first mode after `configure terminal` |
| `hostname(config-line)#` | Line | `line console 0`<br>`line vty 0 15` |
| `hostname(config-if)#` | Interface | `interface type number` |

---

## Submodos de configuración y contextos (cont.)

> **Diagrama detectado:** Mapa ampliado de navegación de entrada y salida desde el *Enable Mode* hacia el Modo Configuración Global, y sus submodos derivados: *Interface Mode*, *[[VLAN]] Mode*, *Console Line Mode* y *VTY Line Mode* utilizando comandos como `interface type/number`, `vlan x`, `line console 0`, `line vty 0 15` y retornando con `exit` o `End / Ctrl+Z`.

---

## Almacenamiento de los archivos de configuración del switch

> **Diagrama detectado:** Representación de los tipos de memoria física en un [[Switch|switch]] [[Cisco]]:
> - **[[RAM]]:** Working Memory and Running Configuration.
> - **Flash:** [[Cisco IOS|Cisco IOS Software]].
> - **[[ROM]]:** Bootstrap Program.
> - **[[NVRAM]]:** Startup Configuration.

---

## Almacenamiento de los archivos de configuración del switch (Cont.)

Nombres y objetivos de los dos archivos de configuración de [[Cisco IOS]] principales:

- **Startup-config:** Almacena la configuración inicial que se utiliza siempre que el [[Switch|switch]] recarga el [[Cisco IOS]] - **[[NVRAM]]**.
- **Running-config:** Almacena los comandos de configuración actualmente utilizados. Este archivo cambia dinámicamente cuando alguien introduce comandos en el modo de configuración - **[[RAM]]**.

---

## Almacenamiento de los archivos de configuración del switch (Cont.)

> **Captura de código / Terminal detectada:** Ejemplos de uso de los comandos `show running-config` y `show startup-config` antes y después de aplicar cambios temporales en el hostname mediante `configure terminal`.

---

## Copia de archivos de configuración

> **Diagrama detectado:** Esquema de transferencia y respaldo de archivos de configuración entre un servidor [[TFTP]], la memoria [[RAM]] (*Running-config*) y la [[NVRAM]] (*Startup-config*) utilizando comandos de tipo `copy running-config startup-config`, `copy startup-config running-config`, `copy tftp running-config`, entre otros.