---
materia: Internet de las Cosas
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [internet_de_las_cosas, diapositiva, ingesta_ia]
---

[[Internet de las Cosas]]

# Introducción a [[MQTT]]

## MQTT: Message Queuing Telemetry Transport

### History Lesson
El protocolo [[MQTT]] fue inventado en 1999 por Andy Stanford-Clark (IBM) y Arlen Nipper (Arcom, now Cirrus Link). Ellos necesitaba un protocolo para minimal battery loss and minimal bandwidth to connect with oil pipelines via satellite. The two inventors specified several requirements for the future protocol:

- Simple implementation
- Quality of Service data delivery
- Lightweight and bandwidth efficient
- Data agnostic
- Continuous session awareness

> **Diagrama detectado:** Línea de tiempo histórica del protocolo MQTT desde 1999 (Invention por IBM) pasando por hitos como MQTT 3.1 (2010), MQTT 3.1.1 (2014, estándar OASIS), MQTT 5 (2018), HiveMQ 4 (2018) y HiveMQ Open Source Edition / MQTT 5 (2019).

---

> **Diagrama detectado:** Arquitectura Publish/Subscribe de MQTT mostrando un `[[MQTT Client]]` (Sensor de temperatura) publicando en un tópico hacia un `[[MQTT Broker]]` (HiveMQ), el cual reenvía/suscribe los mensajes a múltiples `[[MQTT Client]]` (dispositivos de visualización/actuadores).

## MQTT: Tópicos

- Tópicos $\rightarrow$ similar a carpetas y archivos
- Los campos del tópico se delimitan por slash "/"
- Case sensitive
- Usa UTF-8 strings
- Debe existir al menos un carácter
- `+` matches anything at a given tree level
- `#` matches a whole sub-tree
- Los tópicos se crean en el bróker
- Special `$SYS/` topics:
  - `$SYS/broker/clients/connected`
  - `$SYS/broker/clients/disconnected`
  - `$SYS/broker/clients/total`
  - `$SYS/broker/messages/sent`
  - `$SYS/broker/uptime`

> **Diagrama detectado:** Ejemplo de estructura de un tópico `myhome/groundfloor/livingroom/temperature` con niveles separados por barras (`/`). A la derecha muestra ejemplos de subscripciones usando comodines (`#` y `+`) especificando qué rutas cubre y cuáles no.

---

## MQTT: [[QoS (Quality of Service)]]

- Define los requerimientos de entrega de un mensaje
- Las aplicaciones requieren de diferentes [[QoS (Quality of Service)]], no siempre se requiere la mas alta.

- **QoS 0:** "at most once" $\rightarrow$ fire-and-forget
- **QoS 1:** "at least once" $\rightarrow$ Brokers almacenan los mensajes en disco y retransmiten hasta que llegue a su destino. Se pueden duplicar los mensajes
- **QoS 2:** "exactly once" $\rightarrow$ can be delivered exactly once

- Mensajes pueden ser retenidos en el bróker $\rightarrow$ `retained flag set` $\rightarrow$ `true`
- Este mensaje (el último) será enviado inmediatamente que un cliente se subscriba

> **Diagrama detectado:** Diagrama de flujo de mensajes QoS 2 entre `[[MQTT Client]]` y `[[MQTT Broker]]` mostrando los pasos de intercambio: `PUBLISH QoS 2`, `PUBREC`, `PUBREL` y `PUBCOMP`.

Un excelente punto de partida de estudio de [[MQTT]] puede ser con el siguiente documento [documento].

---

## Brokers y clientes

Existen varios brokers, algunos de ellos corren en la cloud, otros pueden ser instalados en el PC y otros estan disponibles para móviles con sistemas operativo Android. De igual forma existen soluciones para las diferentes plataformas de hardware, como se aprecia en la siguiente figura:

> **Diagrama detectado:** Esquema conceptual dibujado a mano dividiendo el ecosistema en `[[MQTT Broker]]` (Servidor: Online/Cloud con HiveMQ, Local/PC con Mosquitto, y Móvil Android con MQTT Broker App) y `[[MQTT Client]]` (Cliente: Online con HiveMQ ws, Local con MQTT-fx tcp, y Android con MQTT DASH).

El bróker Mosquitto puede correr como un servicio en su PC.

---

## Broker (Cloud) - Hivemq

> **Diagrama detectado:** Esquema a mano que detalla la conexión a un broker en la nube (`broker.hivemq.com`), especificando puertos `ws: 8000` y `tcp: 1883`, conectado a clientes por WebSockets (Hivemq) y TCP (Mqtt.fx), apuntando al tópico de pruebas `Lab7/test`.

---

## Ejercicio #1 - Broker online

Para probar la solución de Hivemq, debemos ingresar en el siguiente [link]

- Luego identificamos el bróker de Hivemq y guárdelo para posterior uso del mismo
- Identifique el puerto usado como websocket
- Presione el boton --> Connect
- Suscribase al tópico --> Utmach/curso
- Use el siguiente mensaje a `{"hello": "Hola soy [ESTUDIANTE]"}` (use su nombre) y publíquelo en el tópico Utmach/curso
- Cree nuevos mensajes y publíquelos en el mismo tópico.

> **Captura de pantalla:** Interfaz web del cliente WebSocket de HiveMQ conectada al broker con el panel de conexión, sección de publicación de tópicos (`Utmach/curso/dixys`), QoS configurado en 0, y el cuadro de mensajes recibidos.

---

## Instalaciones de clientes [[MQTT]]

### Cliente MQTT - [[MQTTX]]

Existen varios clientes [[MQTT]] que pueden ser instalados directamente en su PC, ejemplo: [[MQTTX]], el cual puede ser descargado desde [aqui]

Una vez instalado, podemos crear nuevas conexiones hacia los brokers disponibles. Haremos el mismo ejercicio, conectándonos al broker online de Hivemq, para ello seguimos los siguientes pasos:

- Crear nueva conexion, añadiendo los parametros adecuados como se muestra en la imagen

> **Captura de pantalla:** Ventana de configuración de una nueva conexión en el cliente [[MQTTX]] rellenando campos como Name (`HiveMq`), Client ID, Host (`ws://broker.mqttdashboard.com`), Port (`8000`), y Path (`/mqtt`).

- Presionamos --> connect
- Si todo va bien, debe aparecer en verde dicha conexión
- Ahora podemos crear nuestro topicos y probar

---

- Para crear un topico, debemos presionar Nueva suscripcion y escribir el topico, ejemplo: `Utmach/curso/#` (recuerda que siginifica `#`)

> **Captura de pantalla:** Ventana modal de "New Subscription" en [[MQTTX]] configurando el tópico `Utmach/curso/#` con QoS 0.

- Listo, ahora ya podemos escuchar en dicho topico
- Probemos enviando algun json al mismo

---

> **Captura de pantalla:** Panel principal de [[MQTTX]] mostrando la recepción y envío exitoso de mensajes JSON en el tópico suscrito.

### Cliente MQTT - Mqtt.fx

En el siguiente [link] podemos descargar el instalador del cliente Mqtt.fx

- Descargamos la version ejecutable y procedemos a instalarlo
- El procedimiento es el mismo, debemos crear una conexion al broker deseado, indicando las credenciales correspondientes. Note que hivemq es un websocket y debe seleccionar el protocolo ws y el puerto 8000
- Para el caso de brokers tcp el puerto es 1883
- en la rueda dentada, podemos crear las conexiones y se abre una ventana como esta

---

> **Captura de pantalla:** Ventana de configuración "Edit Connection Profiles" en Mqtt.fx, pestaña General, especificando Broker Address (`broker.hivemq.com`), Broker Port (`1883`) y Client ID.

- Luego poedmos presionar Connect --> debe salir en verde la conexion activa
- En Subscribe --> escribimos el topico y nos ponemos a la escucha
- EN publish publicamos sobre el topico deseado

> **Captura de pantallas:** Múltiples capturas del cliente Mqtt.fx mostrando las pestañas de **Subscribe** (con el tópico activo `Utmach/curso/#`) y **Publish** (enviando el mensaje `Hola again`).

---

## Instalación broker [[MQTT]]

### Instalación de Mosquitto

Uno de los brokers mas populares es Mosquitto, el mismo puede correr sobre varias plataformas de hardware. Aqui veremos como instalarlo en su PC de Windows, para linux o raspberry pi existen varios tutoriales en la web que pueden seguir :)

Instalación en Windows, pasos a seguir:

- Descargar e instalar mosquitto desde [aqui] (`mosquitto-2.0.15-install-windows-x64.exe`)
- Dicha instalacion crea un servicio en windows

> **Captura de pantalla:** Asistente de instalación de Eclipse Mosquitto (Choose Components) con las opciones de instalación marcadas (Files, Visual Studio Runtime, Service).

- Ahora debemos iniciar dicho servicio, para esto debemos escribir la palabra servicio en el bbuscador de windows y nos aparace como se ve en la estas imagenes

---

> **Captura de pantalla:** Panel de Servicios de Windows localizando y mostrando las propiedades del servicio "Eclipse Mosquitto MQTT v5/v3.1.1 broker" configurado en modo de inicio Automático y en ejecución.

- Una vez inicializado el servicio, no tenemos que hacer nada mas, para acceder a el, debemos como siempre indicar la ip:puerto, ejemplo `127.0.0.1` y puerto `1883`. Esto lo veremos en la proxima imagen cuando hagamos una conexion nueva desde algun cliente [[MQTT]], por ejemplo [[MQTTX]]

> **Captura de pantalla:** Configuración de una nueva conexión en [[MQTTX]] apuntando al broker local Mosquitto (`mqtt://127.0.0.1` en el puerto `1883`).

- Se nos crea dicha conexion y damos clic en Connect, si todo va bien sale un mensaje de Connected
- Ahora podemos probar dicho broker, enviando mensajes a algun topico

---

> **Captura de pantalla:** Interfaz de [[MQTTX]] conectada con éxito al bróker local `Mosquitto local` demostrando la publicación y recepción de un mensaje JSON.

---

## Ejercicio propuesto

### Filtros con tópicos

**Ejercicio #3 - Filtros a través de tópicos**

1. Usar el árbol de la figura como ejemplo para crear tópicos de sensores y actuadores de una empresa.
2. Crear diferentes criterios de filtros en la suscripción:
   a) Leer todos, Leer de un solo dispositivos, leer todos los sensores de un tipo pero de todos los dispositivos, etc.
   b) Simule el envío de las variables de sensores, creando el json correspondiente
   c) Utilice el bróker y cliente de su preferencia
   d) Capture pantalla de los mensajes recibidos

> **Diagrama detectado:** Jerarquía de red IoT en árbol donde la raíz es el "Edificio", ramificándose en "Planta1", "Planta2", "Planta3", con nodos intermedios de salas ("Sala1", "Sala2") que contienen dispositivos (Arduino, Raspberry Pi) asociados a variables específicas como Temperatura o Ruido.

---

Obra publicada con [[Licencia Creative Commons Reconocimiento Compartir igual 4.0]]