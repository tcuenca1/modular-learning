---
materia: Tecnologias de Conmutacion I
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, diapositiva, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Tecnologías de Conmutación I
## Conmutación LAN Ethernet

**Docente:** [DOCENTE]

---

## Contenido a Tratar
- Encuadre de la asignatura.
- Diagnóstico.
- Conceptos de [[Conmutación LAN]].
- Consideraciones de diseño [[LAN]].

## Objetivos de la Clase
- Entender los procesos básicos utilizados por los [[Switch|switches LAN]] para enviar tramas.
- Describir el razonamiento y la terminología sobre cómo diseñar una [[LAN]] conmutada que funcione bien.

> **Diagrama detectado:** Ilustración conceptual sobre la implementación de redes basadas en [[Switch|switches]] mediante [[Modelo TCP/IP]], garantizando tolerancia a fallos, escalabilidad, calidad de servicio ([[QoS]]) y seguridad de las comunicaciones.

---

## Indicaciones Generales

### Horario de clases:
- Miércoles 6to A: 10:00 a 13:00
- Miércoles 6to B: 07:00 a 10:00

### En clases:
- Se prohíbe realizar otras actividades mientras dure la clase, así como el uso del celular para actividades ajenas a la clase.
- En caso de trabajos repetidos (copia), se anularán todos y se registrará la nota de 0, sin opción a recalificación.
- Las tareas, foros, lecciones, etc. no podrán ser entregadas en fechas posteriores a la señalada (excepto en casos debidamente justificados); de no hacerlo oportunamente, se registrará la nota de 0.
- Las tareas deben contener carátula, ficha, índice, citas y bibliografía en formato IEEE.
- Se prohíbe el consumo de alimentos dentro de laboratorio y aula de clases.
- Prohibido tomar fotos o grabar videos mientras dure la clase.
- Se esperará un máximo de 10 minutos para el ingreso de los estudiantes; luego del tiempo de gracia se procederá a tomar asistencia.
- Respeto al docente y compañeros.

---

## Actividades y Prácticas
- Estas actividades se completan mediante [[Packet Tracer]].
- Están diseñados para emular los laboratorios correspondientes.
- Pueden utilizarse en lugar del laboratorio cuando el acceso a equipos físicos no es posible.
- Estas actividades se realizarán conforme avancen las temáticas.

---

## Prueba de Diagnóstico

### Preguntas
1. ¿Qué es una [[Topología]] de estructura física y lógica?
2. ¿Cuál es la función de una [[Dirección IP]] y cómo se diferencia de una [[Dirección MAC]]?
3. Mencione las capas que tiene el [[Modelo OSI]] y en qué capa se encuentran los [[Switch|switches]].
4. ¿Qué dispositivos se utilizan comúnmente en las capas 1, 2 y 3 del [[Modelo OSI]]?
5. Define qué es un [[Switch]] y qué función cumple en una [[Red de Área Local (LAN)]].

---

## Conceptos de Conmutación [[LAN]] Ethernet

### Conmutación a nivel de Capa 2
> **Diagrama detectado:** Esquema del [[Modelo OSI]] destacando la Capa 2 ([[Capa de Enlace de Datos]]) conectada a un icono de [[Switch]], con características de conmutación basada en hardware, baja latencia, uso de [[Dirección MAC]] y bajo costo.

### Progresión histórica: hubs, puentes y switches
- **Topologías físicas 10BASE2 y 10BASE-T (con un hub):** Muestra el uso de cable coaxial y cable de par trenzado compartido ([[Hub]]).
- **Puentes (Bridges):** El puente crea dos [[Dominio de Colisión|dominios de colisión]] y dos Ethernets compartidas.
- **Switches:** El switch crea cuatro [[Dominio de Colisión|dominios de colisión]] y cuatro segmentos [[Ethernet]].

---

## Lógica de Conmutación

La principal tarea de un [[Switch]] [[LAN]] es recibir tramas [[Ethernet]] y tomar después una decisión: enviar la trama por otro(s) puerto(s) o ignorarla. Para esta misión, los switches llevan a cabo tres acciones:
1. **Decidir cuándo enviar una trama o cuándo filtrar (no enviar) una trama**, basándose en la [[Dirección MAC]] de destino.
2. **Aprender direcciones MAC** examinando la [[Dirección MAC]] de origen de cada trama recibida por el switch.
3. **Crear un entorno libre de bucles (Capa 2)** con otros switches utilizando [[STP (Spanning Tree Protocol)]].

---

## Inundación de Tramas
- El proceso de envío de tramas por todas las interfaces, excepto por la que entró la trama, se denomina **inundación ([[Flooding]])**.
- Los switches mantienen un temporizador para cada entrada de la tabla de direcciones MAC, denominado **temporizador de inactividad**.
- El switch establece el temporizador a 0 para las entradas nuevas.
- Cada vez que el switch recibe otra trama con esa misma [[Dirección MAC]] de origen, el temporizador se restablece a 0.
- El temporizador cuenta ascendentemente, así que el switch puede saber cuáles son las entradas que llevan más tiempo sin recibir una trama procedente de ese dispositivo.

---

## Prevención de Bucles con el Protocolo de Árbol de Extensión
> **Diagrama detectado:** Red con enlaces redundantes pero sin [[STP]], donde se ilustra que una trama entra en un bucle infinito.

---

## Procesamiento Interno en los Switches Cisco

- **Almacenamiento y envío (Store and Forward):** Exige la recepción de la trama completa (hasta aproximadamente 9,200 bytes para tramas gigantes) antes de tomar una decisión con respecto al reenvío, permitiendo verificar errores mediante FCS.
- **Método de corte (Cut-through):** Las tramas pueden comenzar a reenviarse en cuanto se recibe la [[Dirección MAC]] de destino.

---

## Beneficios de la Conmutación [[LAN]]
- Reducción de la cantidad de colisiones.
- Múltiples comunicaciones simultáneas.
- Uplinks de alta velocidad.
- Respuesta de red mejorada.
- Aumento de la productividad del usuario.

---

## Terminología del Diseño de LANs Interdepartamentales o de Campus

> **Diagrama detectado:** Gráfico concéntrico de la arquitectura jerárquica de Cisco indicando tres capas:
> - **Access** (Local and Remote Workgroup Access)
> - **Distribution** (Policy-based Connectivity)
> - **Core** (High-Speed Switching)

### Roles de los switches de campus:
- **Acceso ([[Capa de Acceso]]):** Proporciona un punto de conexión para los dispositivos de usuario final. Bajo circunstancias normales, no envía tramas entre otros dos switches de acceso.
- **Distribución ([[Capa de Distribución]]):** Proporciona un punto de agregación para los switches de acceso, enviando tramas entre switches, pero sin conectar directamente con los dispositivos de usuario final.
- **Núcleo ([[Capa de Núcleo]]):** Switches de distribución agregados a LANs de campus muy grandes, que proporcionan velocidades de envío muy altas.