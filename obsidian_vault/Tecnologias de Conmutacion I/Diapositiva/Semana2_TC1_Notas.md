---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-28
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

# [[Tecnologias de Conmutacion I]] - Funcionamiento de los switches [[Cisco]] LAN

---

## Contenido a tratar:
* Acceso a la [[CLI]] del switch [[Cisco]].
* Configuración del software [[Cisco IOS]].

## Objetivos de la clase:
* Examinar los switches [[Cisco]] y cómo acceder a la interfaz de línea de comandos ([[CLI]]) desde la que es posible enviar instrucciones al switch.
* Explicar cómo se indica al switch los diferentes parámetros operacionales utilizando la [[CLI]].

> **Diagrama detectado:** Ilustración conceptual de redes basadas en switches interconectadas con el [[modelo TCP/IP]], destacando tolerancia a fallos, escalabilidad, calidad de servicio y seguridad.

---

## Switches [[Cisco]] Catalyst y el switch 2960

> **Diagrama detectado:** Apilamiento físico de múltiples modelos de [[Cisco Catalyst]] [[Switch 2960]] mostrando sus paneles frontales con puertos [[Fast Ethernet]] y [[Gigabit Ethernet]].

---

## Switches [[Cisco]]

* Para redes de sucursales de empresas.
* Es un switch de nivel de acceso.
* Velocidades de envío entre 16 Gbps a 32 Gbps.
* Administración basada en la web y [[CLI]] (Interfaz de línea de comandos) de [[Cisco]].
* Funciones LAN avanzadas ([[QoS]], [[ACL]]).
* Conectividad [[Fast Ethernet]] y [[Gigabit Ethernet]].
* Hasta 48 puertos 10/100 o puertos 10/100/1000 (No PoE).

---

## Secuencia de arranque de un switch

> **Diagrama detectado:** Gráfico escalonado que detalla los 5 pasos del arranque de un switch:
> 1. Ejecutar **POST** (Pruebas de diagnóstico de hardware).
> 2. Cargar el cargador de arranque (**Bootloader**).
> 3. Inicializar **CPU**.
> 4. Iniciar sistema de archivos.
> 5. Cargar [[Cisco IOS]] y tomar el control.

---

## Indicadores LED de un switch

> **Diagrama detectado:** Panel frontal de un switch [[Cisco]] destacando el botón **MODE** y los indicadores LED: **SYST**, **RPS**, **STAT**, **DUPLX**, **SPEED** y **PoE**.

* **LED del sistema (SYST):** muestra si el sistema recibe alimentación y funciona correctamente.
* **LED de fuente de alimentación redundante (RPS):** muestra el estado de [[RPS]].
* **LED de estado del puerto (STAT):** cuando está verde, indica que el modo de estado del puerto está seleccionado (valor predeterminado).
* **LED de modo dúplex del puerto:** indica que se seleccionó el modo [[dúplex]].
* **LED de velocidad del puerto (SPEED):** indica que se ha seleccionado el modo de velocidad del puerto.
* **LED de alimentación a través de Ethernet (PoE):** presente si el switch es compatible con [[PoE]].

El botón **Modo** se utiliza para moverse entre los diferentes modos: STAT, DUPLX, SPEED y PoE.

---

## Acceso a la [[CLI]] del [[Cisco IOS]]

> **Diagrama detectado:** Topología de conexión que muestra un PC conectado al puerto de consola de un switch [[Switch 2960]] mediante un cable de consola (**Console Cable** con conectores Serial/USB a RJ-45/USB) para entrar al *User Mode*, así como acceso remoto mediante red [[TCP/IP]] usando [[Telnet]] y [[SSH]].

---

## Acceso a la [[CLI]] del [[Cisco IOS]] (Cont.)

> **Diagrama detectado:** Tres esquemas de conexión física de consola a un switch:
> 1. **SW1:** Conexión mediante cable *Rollover* desde puerto Serie del PC a puerto *RJ-45 Console*.
> 2. **SW2:** Conexión mediante cable *Rollover* con conversor USB a puerto USB del PC.
> 3. **SW3:** Conexión directa mediante cable USB desde puerto USB del PC a puerto *USB Console* del switch.

---

## Acceso a la [[CLI]] desde la consola

> **Diagrama detectado:** Captura de pantalla de un emulador de terminal (**Tera Term**) configurando los parámetros del puerto serie (Baud rate: 9600, Data: 8 bit, Parity: none, Stop: 1 bit, Flow control: none) y mostrando la ejecución del comando `show mac address-table dynamic` en la [[CLI]].

---

## Seguridad de la contraseña para acceder a la [[CLI]]

Configuración de contraseña CLI: consola y [[Telnet]]

| Access From | Password Type | Sample Configuration |
| :--- | :--- | :--- |
| Console | Console password | `line console 0`<br>`login`<br>`password [ID_OMITIDO]` |
| [[Telnet]] | vty password | `line vty 0 15`<br>`login`<br>`password [ID_OMITIDO]` |

---

## Modos de usuario y enable (privilegiado)

> **Diagrama detectado:** Diagrama de estados dentro de un switch que ilustra la transición mediante comandos entre el *User Mode* y el *Enable Mode* (Privilegiado), accedidos mediante [[Console]], [[Telnet]] o [[SSH]].

---

## Funcionalidades de ayuda de la [[CLI]]

> **Diagrama detectado:** Tabla listando las opciones de ayuda contextual en el software [[Cisco IOS]]: `?`, `help`, `command ?`, `com?`, `command parm?`, `command parm<Tab>`, y `command parm1 ?`.

---

## Configuración del software [[Cisco IOS]]

El modo de configuración [[CLI]] frente a los modos Exec.

> **Diagrama detectado:** Mapa de navegación entre los modos de ejecución y configuración: Modo Usuario $\rightarrow$ (comando `enable`) $\rightarrow$ Modo Enable (Privilegiado) $\rightarrow$ (comando `configure terminal`) $\rightarrow$ Modo Configuración $\rightarrow$ (comandos `end` o `Ctrl+Z`) $\rightarrow$ retorno al Modo Enable.

---

## Submodos de configuración y contextos

Navegación entre los diferentes modos de configuración.

> **Diagrama detectado:** Bloque de código de ejemplo en la [[CLI]]:
> ```text
> Switch#configure terminal
> Switch(config)#hostname [ESTUDIANTE]
> [ESTUDIANTE](config)#line console 0
> [ESTUDIANTE](config-line)#password [ID_OMITIDO]
> [ESTUDIANTE](config-line)#interface FastEthernet 0/1
> [ESTUDIANTE](config-if)#speed 100
> [ESTUDIANTE](config-if)#exit
> [ESTUDIANTE](config)#
> ```

---

## Submodos de configuración y contextos (cont.)

Modos comunes de configuración de un switch.

| Prompt | Name of Mode | Context-setting Command(s) to Reach This Mode |
| :--- | :--- | :--- |
| `hostname(config)#` | Global | None—first mode after `configure terminal` |
| `hostname(config-line)#` | Line | `line console 0`<br>`line vty 0 15` |
| `hostname(config-if)#` | Interface | `interface type number` |

---

## Submodos de configuración y contextos (cont.)

> **Diagrama detectado:** Diagrama de flujo detallado sobre la navegación de entrada y salida entre el *Enable Mode*, el *Global Config Mode*, y los submodos específicos: *Interface Mode*, *VLAN Mode*, *Console Line Mode* y *VTY Line Mode* utilizando comandos como `interface type/number`, `vlan x`, `line console 0`, `line vty 0 15`, `exit`, y `end` o `Ctrl+Z`.

---

## Almacenamiento de los archivos de configuración del switch

Tipos de memoria de un switch [[Cisco]]:
* **RAM:** (*Working Memory and Running Configuration*)
* **Flash:** (*[[Cisco IOS]] Software*)
* **ROM:** (*Bootstrap Program*)
* **NVRAM:** (*Startup Configuration*)

---

## Almacenamiento de los archivos de configuración del switch (Cont.)

Nombres y objetivos de los dos archivos de configuración de [[Cisco IOS]] principales:
* **Startup-config:** Almacena la configuración inicial que se utiliza siempre que el switch recarga el [[Cisco IOS]] (ubicado en la **NVRAM**).
* **Running-config:** Almacena los comandos de configuración actualmente utilizados. Este archivo cambia dinámicamente cuando alguien introduce comandos en el modo de configuración (ubicado en la **RAM**).

---

## Almacenamiento de los archivos de configuración del switch (Cont.)

> **Diagrama detectado:** Bloque de comandos y salidas de consola demostrando que los cambios realizados en el modo de configuración modifican el *running-config* inmediatamente, pero no afectan al *startup-config* hasta que se guarden explícitamente.

---

## Copia de archivos de configuración

> **Diagrama detectado:** Diagrama de transferencia de archivos entre el servidor **TFTP**, la **RAM** (*running-config*) y la **NVRAM** (*startup-config*), indicando las distintas variantes del comando `copy` (ej. `copy running-config startup-config`, `copy startup-config running-config`, etc.).