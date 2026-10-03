---
materia: Tecnologias de Conmutacion I
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, actividad, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Packet Tracer - Exploración de Modo Lógico y Físico

**Estudiante:** [ESTUDIANTE]

## Objetivos
* Parte 1: Investigar la Barra de Herramientas Inferior
* Parte 2: Investigar Dispositivos en un Armario de Cableado
* Parte 3: Conectar Dispositivos Finales a Dispositivos de Red
* Parte 4: Instalar un Router de Respaldo
* Parte 5: Configurar un Nombre de Host
* Parte 6: Explora el resto de la Red

---

## Aspectos básicos / Situación

El modelo de red de esta actividad [[Packet Tracer]] Physical Mode (PTPM) incorpora muchas de las tecnologías de [[Cisco Networking Academy]], y representa una versión simplificada de la forma en que podría verse una red de pequeña o mediana empresa.

La mayoría de los dispositivos de la sucursal de Seward y del Centro de Datos de Warrenton ya están implementados y configurados, por lo tanto, usted acaba de ser contratado para revisar los dispositivos y redes implementados, donde no es importante que comprenda todo lo que vea y haga en esta actividad. Siéntase libre de explorar la red por usted mismo, y responda las preguntas lo mejor que pueda.

---

## Instrucciones

### Parte 1: Investigar la Barra de Herramientas Inferior

La barra de herramientas de iconos en la esquina inferior izquierda tiene varias categorías de componentes de red. Debería ver categorías que corresponden a Dispositivos de Red, Dispositivos Finales, y Componentes. La cuarta categoría (con el icono del rayo) es Conexiones y representa los medios de red compatibles con [[Packet Tracer]]. Las dos últimas categorías son Miscelánea y Conexión multiusuario.

> **Diagrama detectado:** Captura parcial de la barra de herramientas inferior de [[Packet Tracer]] mostrando los iconos de categorías de dispositivos de red, dispositivos finales, conexiones (icono de rayo), y los menús de búsqueda de dispositivos.

¿Cuáles son las subcategorías de [[Dispositivos de Red]]?
Las subcategorías que hay son [[Routers]], [[Switches]], [[Hubs]], [[Wireless Devices]], [[Security]] y [[WAN Emulation]].

---

### Parte 2: Investigar Dispositivos en un Armario de Cableado

* **a.** Si fuiste a explorar, vuelve a modo Físico e Intercity ahora. En la barra azul superior, haga clic en **Físico** y, a continuación, utilice los botones Panel de Navegación o Nivel Atrás para desplazarse a **Intercity**.
* **b.** Haga clic en **Seward** y, a continuación, haga clic en la **Sucursal**.
* **c.** Haga clic en el **Armario de Cableado de la Sucursal**. Observe que el armario de cableado tiene un **Rack**, un **Tablero de Cables**, una **Mesa** y un **Estante**.

El **Rack** contiene dispositivos que se pueden montar en rack. Si amplía el rack (herramienta de zoom o Ctrl+rueda de desplazamiento), puede ver que los dispositivos están atornillados (montados) en el rack. Debajo del dispositivo de distribución de energía, encontrará un router. Los [[routers]] conectan redes diferentes.

* **d.** Debajo del router hay dos switches. Estos [[switches]] proporcionan conexiones por cable para conectarse a otros dispositivos. Observe que los dispositivos tienen un nombre asignado por el administrador de red.

¿Qué dispositivos utilizan una conexión por cable para conectarse al switch `ALS2`?
Lo utilizan los dispositivos `WebServer` y `Access_Point`.

* **e.** Debajo de los switches del Rack se encuentra un punto de acceso inalámbrico denominado `Access_Point`. Los puntos de acceso inalámbricos utilizan una conexión inalámbrica para conectarse a otros dispositivos. Cambie al modo Lógico. ¿Qué dispositivo está conectado a `Access_Point`?
Está conectada la `Laptop_1`.

* **f.** Cambie al modo Físico. Deberías estar de vuelta en el Armario de Cableado de la Sucursal. ¿Dónde se encuentra físicamente el dispositivo conectado a `Access_Point`?
Está físicamente conectado al router `ALS2`.

> **Diagrama detectado:** Vista de un armario de cableado informático con un rack de servidores y equipos de red (arriba a la izquierda) junto a una representación en modo lógico de la topología local que incluye `Power Distribution Device`, `Edge_Router`, `ALS2`, `Access_Point`, `WebServer`, `Laptop_1` y `PC_1` (arriba a la derecha).

---

### Parte 3: Conectar Dispositivos Finales a Dispositivos de Red

Los dispositivos se pueden conectar de varias maneras. Para la conectividad de red, los dispositivos normalmente se conectan mediante un **cable directo de cobre** o de forma inalámbrica. Para la conectividad de administración, los dispositivos normalmente se conectan mediante un **cable de consola** o un **cable USB**.

* **a.** Investigue el **Tablero de Cables**. Incluye dos cables de Consola, diez cables directos de cobre, cuatro cables de Fibra, dos cables Coaxiales y dos cables USB. Observe que las representaciones de cable en modo Físico son más representativas de sus homólogos del mundo real. Cambie al modo Lógico. Observe que las representaciones de cable son diferentes en este modo.
* **b.** Cambie al modo Físico. Haga clic en un cable directo de cobre del Tablero de Cables.
* **c.** Mueva el ratón sobre los puertos de `PC_1` hasta que vea la ventana emergente `FastEthernet0`. El otro puerto `RS232` es para conectar cables de Consola.
* **d.** Con el cable directo de cobre todavía seleccionado, haga clic en el puerto `FastEthernet0` para conectar el cable. Ahora el puerto debe estar resaltado en verde.
* **e.** Conecte el otro extremo del cable al switch `ALS2` haciendo clic en un puerto Fast Ethernet vacío. El cable ahora debería colgar entre la `PC_1` y el puerto de `ALS2`.
* **f.** Las PCs y los portátiles también se pueden conectar a dispositivos de red mediante un cable de consola o un cable USB. Esta conexión proporciona acceso de administración. Haga clic en un cable de Consola del Tablero de Cables.
* **g.** Haga clic en el puerto `RS232` en `PC_1`. Ahora el puerto debe estar resaltado en verde.
* **h.** Pase el ratón sobre el `Edge_Router` y busque el puerto de Consola. Puede hacer clic con el botón derecho en > **Inspeccionar Frente** para ampliar y facilitar la búsqueda del puerto.
* **i.** Haga clic en el puerto de consola en `Edge_Router` para conectar el cable de Consola. El cable ahora debería colgar entre `PC_1` y el puerto de Consola en el `Edge_Router`.

> **Diagrama detectado:** Vista del rack físico de red mostrando cables conectados colgando entre los dispositivos y el panel de distribución dentro del armario de cableado.

---

### Parte 4: Instalar un Router de Respaldo

A los modelos más nuevos de dispositivos de red se puede acceder a través de un puerto USB para la configuración de la administración. Esto es necesario porque los portátiles y los PC más recientes normalmente no incluyen un puerto RS232 para las conexiones de cables de consola.

* **a.** Investigue el **Estante**. Esto incluye un inventario de dispositivos de la Sucursal de Seward que no están instalados actualmente.
* **b.** Haga clic y arrastre `Backup_Router` a un lugar vacío en el **Rack**.
* **c.** Algunos dispositivos no se encienden automáticamente cuando se instalan en el Rack. Haga clic en `Backup_Router > Inspeccionar parte trasera`. Busque el botón de encendido y encienda el router.
* **d.** En el Tablero de Cables, elija un cable USB. Vuelva a la vista trasera de `Backup_Router` y encuentre el puerto de consola USB en el extremo izquierdo. Haga clic en el puerto para conectar el cable USB. Ahora el puerto debe estar resaltado en verde.
* **e.** Conecte el otro extremo del cable USB a cualquiera de los puertos USB de la `Laptop_1`. El cable no colgará como lo hicieron los cables para las conexiones a `PC_1`.

> **Diagrama detectado:** Vista detallada del armario de red tras la instalación del router de respaldo (`Backup_Router`) montado en el rack con su respectivo cableado conectado a la laptop de administración.

---

### Parte 5: Configuración de un Nombre de Host

Los administradores de red suelen asignar un nombre a los dispositivos de red. Para hacer esto, utilizará la conexión de consola al `Backup_Router`.

* **a.** Haga clic en `Laptop_1` > pestaña de **Desktop** > **Terminal**.
* **b.** La configuración de la Terminal ya está definida con la configuración de puerto necesaria. Haga clic en **Aceptar**.
* **c.** Ahora está en la línea de comandos para `Backup_Router` y debería ver lo siguiente:

```text
<output omitted>
cisco ISR4331/K9 (1RU) processor with 1795999K/6147K bytes of memory. 
Processor board ID FLM232010G0
3 Gigabit Ethernet interfaces
2 Serial interfaces
32768K bytes of non-volatile configuration memory.
4194304K bytes of physical memory.
3207167K bytes of flash memory at bootflash:.
0K bytes of WebUI ODM Files at webui:.

--- System Configuration Dialog ---

Would you like to enter the initial configuration dialog? [yes/no]: no
```

* **d.** Responda `no` a la pregunta y luego presione **ENTRAR** para obtener el símbolo del sistema Router.

```text
Press RETURN to get started!

<ENTER>
Router>
```

* **e.** Introduzca los siguientes comandos para nombrar al router `Edge_Router_Backup`:

```text
Router> enable
Router# configure terminal
Enter configuration commands, one per line. End with CNTL/Z. 
Router(config)# hostname Edge_Router_Backup 
Edge_Router_Backup(config)# end
Edge_Router_Backup#
```

Observe que el nombre de host cambió de `Router` a `Edge_Router_Backup`.

* **f.** Cierre la ventana de `Laptop_1` y vuelva al Armario de Cableado de la Sucursal.
* **g.** Observe que el nombre para mostrar de `Backup_Router` no ha cambiado. Haga clic en `Backup_Router` > pestaña **Config**. En Configuración global, observe que [[Packet Tracer]] mantiene dos nombres para el dispositivo: un **nombre para mostrar** y un **nombre de host**.

> **Diagrama detectado:** Captura de pantalla simultánea de la interfaz gráfica de configuración de [[Packet Tracer]] y la ventana de terminal de comandos abierta desde `Laptop_1` mostrando la ejecución de comandos CLI en el `Backup_Router`.

---

### Parte 6: Explora el resto de la Red

Tómese un tiempo para explorar el resto de la red. Familiarícese con las representaciones de red en los modos Lógico y Físico. En el modo Físico, vaya a otras áreas, como el **Centro de Datos de Wellington** y el **hogar de Teleworker**. Por ahora, vea lo que puede descubrir por su cuenta. No se preocupe por romper nada. Siempre puede cerrar [[Packet Tracer]] y abrir una copia nueva para empezar a explorar de nuevo.