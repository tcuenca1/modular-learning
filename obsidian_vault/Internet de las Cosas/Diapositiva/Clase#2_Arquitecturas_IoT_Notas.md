---
materia: Internet de las Cosas
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [internet_de_las_cosas, diapositiva, ingesta_ia]
---

[[Internet de las Cosas]]

# Arquitecturas de IoT: Conectando el Mundo Digital y Físico

---

## 1. Problema y Objetivo

* **Problema:** Caracterizar arquitecturas [[IoT]].
* **Objetivo:** Comprender los elementos clave y las capas de la arquitectura [[IoT]] para diseñar soluciones eficientes y escalables.

> **Diagrama detectado:** Esquema conceptual que contrasta el mundo físico con el mundo de la información mediante redes de comunicación, dispositivos, pasarelas (*gateways*), cosas físicas y virtuales, y su respectivo mapeo y comunicación.

---

## 2. Definición de las "Cosas" y Arquitecturas del [[IoT]]

* **Arquitectura:** Estructura de un sistema = distribución de elementos = modelos = patrones = estilos = representación.
* **Componentes principales:** Cosas (*Things*) hasta el Usuario (Monitoreo/Control).
* Pueden estar distribuidos o agrupados por:
  * [[Niveles (Levels)]]
  * [[Capas (Layers)]]
  * Bloques
  * Dominios
* **Elementos intermedios:** Redes IP, [[Internet]], equipos de comunicación, [[Fog Computing]], [[Edge Computing]], [[Cloud Computing]], aplicaciones y servicios.

---

## 3. ¿Qué es la Arquitectura [[IoT]]?

Una estructura de capas que organiza los componentes del [[IoT]] para permitir una comunicación fluida y segura.

> *“La arquitectura de IoT se organiza en capas que permiten que los dispositivos se comuniquen de forma fluida y segura. Cada capa tiene un papel esencial, desde capturar datos hasta analizarlos y usarlos para aplicaciones específicas.”*

---

## 4. Modelos de Arquitecturas [[IoT]]

Existen múltiples arquitecturas definidas para el [[IoT]], algunas establecidas por instituciones de renombre y otras aceptadas por la comunidad científica (artículos, libros, congresos), convertidas en estándares:

1. **[[SOA-Based Architecture]]** (Arquitectura basada en Servicios):
   * Interoperabilidad de dispositivos heterogéneos.
   * 4 Capas: *Sensing layer*, *Network layer*, *Service layer*, *Interfaces layer*.
   * Muy usado en [[WSN]] (Wireless Sensor Networks) debido a su nivel de abstracción y diseño modular.
2. **[[API-Oriented Architecture]]**:
   * Web API + REST. Usa JSON (más ligero que XML).
   * Protocolo [[CoAP]] (Constrained Application Protocol) = protocolo REST.
   * 4 Capas: *Sensing layer*, *Network layer*, *REST API layer*, *Application (Web) layer*.
3. **[[oneM2M IoT Standardized Architecture]]**:
   * Creado por el *European Telecommunications Standards Institute* ([[ETSI]]).
   * 3 Capas: *Application layer*, *Services layer*, *Network layer* (Sitio web: `www.onem2m.org`).
4. **[[IoT World Forum (IoTWF) Standardized Architecture]]**:
   * Creado por [[CISCO]], [[IBM]], [[Rockwell]], entre otros.
   * 7 Capas: 
     1. *Physical devices & controllers*
     2. *Connectivity*
     3. *Edge Computing*
     4. *Data Accumulation (Storage)*
     5. *Data Abstraction*
     6. *Application*
     7. *Collaboration & Process*
5. **[[Purdue Model for Control Hierarchy]]**
6. **[[Industrial Internet Reference Architecture (IIRA)]]**
7. **[[Internet of Things-Architecture (IoT-A)]]**
8. **[[Simplified IoT Architecture]]**:
   * Compuesto por el *Core IoT Functional Stack* (Applications, Communications Network, Things: Sensors and Actuators) y el *IoT Data Management and Compute Stack* (Cloud, Fog, Edge), atravesados por la [[Seguridad]].
9. **[[IoT Layered Architecture of ITU-T]]**
10. **[[WSO2 Reference Architecture]]**:
    * 5 Capas: *Client/external communications layer* (Web/Portal, Dashboard, APIs), *Event processing and analytics layer* (incluye almacenamiento), *Aggregation/bus layer* (ESB y message broker), *Communication layer* (MQTT/HTTP/XMPP/CoAP/AMQP), y *Devices Layer*.
11. **[[FOKUS IoT Architecture]]**
12. **[[Domine IoT Architecture (Dixys)]]**:
    * Arquitectura basada en dominios, *Cloud computing*, coexistencia IPv4 / IPv6, y [[WSN]].

---

## 5. Componentes del [[IoT]]

* **[[Sensores y Actuadores]]**
* **Redes de Comunicación**
* **[[Gateway IoT]]**
* **[[Protocolos IoT]]**
* **[[Plataformas IoT]]**
* **Aplicaciones**

### Detalle de Componentes:

* **Sensores:** Convierten una propiedad física en una señal eléctrica.
  * Variables físicas: temperatura, sonido, flujo, presión, distancia, luz, aceleración, humedad, vibración, gas, etc.
  * Pueden ser analógicos o digitales.
* **Actuadores:** Convierten una señal eléctrica en una propiedad física.
  * Ejemplos: luz, movimiento, calor, corriente, sonido.
  * Salidas analógicas (DAC), digitales, PWM. Tecnología [[MEMS]] (Micro-Electro-Mechanical Systems).
* **Procesadores y Dispositivos Restringidos ([[Constrained Devices]]):**
  * Microcontroladores ([[uC]]): PIC, STM32.
  * [[SoC]]: nRF52, ESP32.
  * [[SBC]]: Raspberry Pi (RPI), Beaglebone, Orange Pi.
  * [[PLC]], [[FPGA]].
  * Restricciones: uso de baterías, bajo consumo, poca memoria, latencias, capacidad de procesamiento limitada. Uso de Sistemas Operativos en Tiempo Real ([[RTOS]]).
* **Gateway [[IoT]]:**
  * Puerta de enlace entre la capa de dispositivos y los niveles superiores. Dispositivo físico capaz de encapsular diferentes protocolos (ej. BLE, Zigbee, Lora hacia Wi-Fi, Ethernet, LAN e Internet).
  * Brinda acceso a internet a dispositivos que no lo poseen y maneja interfaces seriales (UART, I2C, SPI).

---

## 6. Redes de Sensores Inalámbricos ([[WSN]])

* **[[WSN]]** (*Wireless Sensor Network*): Compuestas por nodos o **Motes** (*Smart sensors*).
* Utilizan direccionamiento IP ([[IPv4]] o [[IPv6]]) y diversas tecnologías de comunicación inalámbrica (Wi-Fi, Zigbee, BLE, Lora).
* **Patrones de comunicación:**
  * **Event-driven:** Transmite datos solo cuando se detecta un evento o se alcanza un límite definido.
  * **Periodic:** Transmite datos en intervalos de tiempo específicos.

---

## 7. Dónde debe ser procesada la información?

* **[[Edge Computing]] (Borde):** Billones de dispositivos deslocalizados (Sensores, actuadores, máquinas). Procesamiento local inmediato.
* **[[Fog Computing]] (Niebla):** Millones de nodos distribuidos en pasarelas (*gateways*) y redes locales.
* **[[Cloud Computing]] (Nube):** Miles de servidores centralizados para almacenamiento masivo, análisis avanzado y visualización global.

---

## 8. Plataformas [[IoT]]

¿Por qué usar una plataforma [[IoT]]?
* Conectar hardware (sensores y dispositivos).
* Manejar diferentes [[Protocolos de Comunicación]] entre hardware y software.
* Proporcionar [[Seguridad]] y autenticación para dispositivos y usuarios.
* Recopilar, visualizar y analizar datos.
* Integrar con otros servicios [[SaaS]].
* *Ejemplos mostrados en herramientas:* Blynk, Home Assistant, OpenHAB, AWS IoT, Google Cloud Platform (IoT Core, Pub/Sub, BigQuery), Microsoft Azure IoT Hub.

---

## 9. Orquestaciones en [[IoT]]

* **Centralizada:** Control centralizado, fácil monitoreo y gestión.
  * *Limitación:* Vulnerable a puntos únicos de fallo (*single point of failure*).
* **Descentralizada:** Alta resiliencia y escalabilidad.
  * *Limitación:* Requiere mayor capacidad de procesamiento en los dispositivos individuales.

---

## 10. Casos de Estudio para Análisis Arquitectural
*(Pregunta de aplicación planteada en la sesión)*:
¿Qué arquitectura, elementos y orquestación usaría en los siguientes casos?
* Control de tráfico de una ciudad.
* Control de iluminación en el hogar.
* Monitoreo de salud remoto.
* Monitoreo de flotas de vehículos.
* Control de riego en parques y jardines.
* Monitoreo de temperatura y humedad de flores en contenedor.
* Rastreo y gestión de activos.
* Alerta temprana de desastres naturales.
* Control de calidad del agua.