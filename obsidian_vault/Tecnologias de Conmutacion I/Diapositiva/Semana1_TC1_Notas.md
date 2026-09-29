---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-28
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Tecnologías de Conmutación I
## Conmutación LAN Ethernet
**Docente:** [DOCENTE]

---

## Contenido a Tratar y Objetivos

### Contenido a tratar:
* Encuadre de la asignatura.
* Diagnóstico.
* Conceptos de [[Conmutación]] [[LAN]].
* Consideraciones de diseño [[LAN]].

### Objetivos de la clase:
* Entender los procesos básicos utilizados por los [[Switch|switches LAN]] para enviar tramas.
* Describir el razonamiento y la terminología sobre cómo diseñar una [[LAN]] conmutada que funcione bien.

> **Diagrama detectado:** Ilustración conceptual de redes basadas en switches mediante protocolos y tecnologías del modelo [[Modelo TCP-IP]], destacando la tolerancia a fallos, escalabilidad, calidad de servicio ([[QoS]]) y seguridad.

---

## Indicaciones Generales

### Horario de clases:
* Miércoles 6to A: 10:00 a 13:00
* Miércoles 6to B: 07:00 a 10:00

### En clases:
* Se prohíbe realizar otras actividades mientras dure la clase, así como el uso del celular para actividades ajenas a la clase.
* En caso de trabajos repetidos (copia), se anularán todos y se registrará la nota de 0, sin opción a recalificación.
* Las tareas, foros, lecciones, etc. no podrán ser entregadas en fechas posteriores a la señalada (excepto en casos debidamente justificados); de lo contrario, se registrará la nota de 0.
* Las tareas deben contener carátula, ficha, índice, citas y bibliografía en norma IEEE.
* Se prohíbe el consumo de alimentos dentro de laboratorio y aula de clases.
* Prohibido tomar fotos o grabar vídeos mientras dure la clase.
* Se esperará máximo hasta 10 minutos el ingreso de los estudiantes a las clases; luego del tiempo de gracia se procederá a tomar asistencia.
* Respeto al docente y compañeros.

---

## Actividades y Prácticas

* Estas actividades se completan mediante [[Packet Tracer]].
* Están diseñados para emular los laboratorios correspondientes.
* Pueden utilizarse en lugar del laboratorio cuando el acceso a equipos físicos no es posible.
* Estas actividades se realizarán conforme avancen las temáticas.

---

## Prueba de Diagnóstico

### Preguntas:
1. ¿Qué es una topología de estructura física y lógica?
2. ¿Cuál es la función de una [[Dirección IP]] y cómo se diferencia de una [[Dirección MAC]]?
3. Mencione las capas que tiene el [[Modelo OSI]] y en qué capa se encuentran los [[Switch|switches]].
4. ¿Qué dispositivos se utilizan comúnmente en las capas 1, 2 y 3 del [[Modelo OSI]]?
5. Define qué es un [[Switch]] y qué función cumple en una red de área local ([[LAN]]).

---

## Conceptos de Conmutación LAN Ethernet

### Conmutación a Nivel de Capa 2
> **Diagrama detectado:** Pila del [[Modelo OSI]] resaltando la Capa 2 ([[Capa de Enlace de Datos]]), acompañada de las características de un switch: conmutación basada en hardware, baja latencia, uso de dirección MAC y bajo costo.

---

## Progresión Histórica: Hubs, Puentes y Switches

* **Topologías físicas 10BASE2 y 10BASE-T (con un hub):**
  > **Diagrama detectado:** Comparación esquemática entre un bus único coaxial (10BASE2) y un hub de par trenzado compartido (10BASE-T).
* **El puente (Bridge):** Crea dos dominios de colisión y dos Ethernets compartidas.
  > **Diagrama detectado:** Red dividida por un bridge en dos dominios de colisión separados a 10 Mbps.
* **El switch:** Crea cuatro dominios de colisión y cuatro segmentos Ethernet.
  > **Diagrama detectado:** Esquema de un switch interconectando cuatro equipos finales (Fred, Barney, Wilma, Betty) en dominios de colisión independientes de 100 Mbps cada uno, mediante interfaces FastEthernet (`Fa0/1` a `Fa0/4`).

---

## Lógica de Conmutación

La principal tarea de un switch [[LAN]] es recibir tramas [[Ethernet]] y tomar después una decisión: enviar la trama por otro(s) puerto(s) o ignorarla. Para esta misión, los switches llevan a cabo tres acciones:
1. **Decidir cuándo enviar una trama o cuándo filtrar (no enviar) una trama**, basándose en la [[Dirección MAC]] de destino.
2. **Aprender direcciones MAC** examinando la [[Dirección MAC]] de origen de cada trama recibida por el switch.
3. **Crear un entorno libre de bucles (capa 2)** con otros switches utilizando [[STP]] (*Spanning Tree Protocol*).

*Nota:* La primera tarea es el principal trabajo del switch; las otras dos son funciones de coste operativo.

---

## El Envío frente a la Decisión de Filtrado

> **Diagrama detectado:** Flujo paso a paso de un switch evaluando una trama entrante por la interfaz `F0/1` destinada a una MAC específica (ej. dirección `0200.2222.2222` asociada al puerto `F0/2`), consultando la tabla de direcciones [[MAC Address Table]] y realizando el reenvío hacia el puerto correspondiente mientras filtra el tráfico hacia los puertos inactivos (`F0/3`, `F0/4`).

---

## Aprendizaje de Direcciones MAC por Parte de los Switches

> **Diagrama detectado:** Secuencia en 4 pasos del proceso de aprendizaje dinámico de la tabla MAC en un switch al recibir tramas de difusión desconocida (*unknown unicast*), registrando puertos de entrada asociados a las direcciones MAC de origen (`00-0A`, `00-0D`, etc.).

---

## Inundación de Tramas

* El proceso de envío de tramas por todas las interfaces, excepto por la que entró la trama, se denomina inundación (**flooding**).
* Los switches mantienen un temporizador para cada entrada de la tabla de direcciones MAC, denominado **temporizador de inactividad**.
* El switch establece el temporizador a 0 para las entradas nuevas.
* Cada vez que el switch recibe otra trama con esa misma [[Dirección MAC]] de origen, el temporizador se restablece a 0.
* El temporizador cuenta ascendentemente, así que el switch puede saber cuáles son las entradas que llevan más tiempo sin recibir una trama procedente de ese dispositivo.

---

## Prevención de Bucles con el Protocolo de Árbol de Extensión

> **Diagrama detectado:** Topología de red con enlaces redundantes pero sin [[STP]], donde la ausencia de bloqueo de puertos provoca que una trama entre en un bucle infinito (*broadcast storm*).

---

## Procesamiento Interno en los Switches Cisco

* **Almacenamiento y envío (*Store-and-Forward*):** El switching por almacenamiento y envío exige la recepción de la trama completa (hasta aproximadamente 9,200 bytes para las tramas gigantes) antes de tomar una decisión con respecto al reenvío, verificando el checksum ([[FCS]] / [[CRC]]).
* **Por método de corte (*Cut-Through*):** Las tramas pueden comenzar a reenviarse en cuanto se recibe la [[Dirección MAC]] de destino.

---

## Beneficios de la Conmutación LAN

* Reducción de la cantidad de colisiones.
* Múltiples comunicaciones simultáneas.
* Uplinks de alta velocidad.
* Respuesta de red mejorada.
* Aumento de la productividad del usuario.

---

## Terminología del Diseño de LANs Interdepartamentales o de Campus

### Modelo Jerárquico de 3 Capas de Cisco:
1. **Access (Acceso):** Proporciona un punto de conexión para los dispositivos de usuario final. Bajo circunstancias normales, no envía tramas entre otros dos switches de acceso (*Local and Remote Workgroup Access*).
2. **Distribution (Distribución):** Proporciona un punto de agregación para los switches de acceso, enviando tramas entre switches, pero sin conectar directamente con los dispositivos de usuario final (*Policy-based Connectivity*).
3. **Core (Núcleo):** Switches de distribución agregados a LANs de campus muy grandes, que proporcionan velocidades de envío muy altas (*High-Speed Switching*).

> **Diagrama detectado:** Arquitectura de red de campus dividida en capas de Acceso, Distribución y Núcleo, aplicada a esquemas institucionales como el diseño de la [[LAN]] de campus [[UTMACH]].

---

## Taller

El modelo de red de esta actividad Packet Tracer Physical Mode (PTPM) incorpora muchas de las tecnologías de [[Cisco Networking Academy]], y representa una versión simplificada de la forma en que podría verse una red de pequeña o mediana empresa.

La mayoría de los dispositivos ya están implementados y configurados; por lo tanto, se solicita revisar los dispositivos y redes implementadas.