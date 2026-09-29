---
materia: Tecnologias de Conmutacion I
tipo: actividad
fecha_procesamiento: 2026-09-28
tags: [tecnologias_de_conmutacion_i, actividad, ingesta_ia]
---

# Taller 2 S3

[[Tecnologias de Conmutacion I]]

* **Nombres:** [ESTUDIANTE], [ESTUDIANTE].
* **Fecha:** 22/09/2026

De la topología planteada por el [DOCENTE] configurar lo siguiente:
* Dos [[VLAN]]s 10 y 20
* Cinco host (2 host a la vlan 10; 2 host a la vlan 20 y 1 host a consola)
* Todos los host deben pertenecer a la misma red.
* Comprobar las conexiones entre los hosts que estan en las vlan 10 y vlan 20.

---

## TOPOLOGIA LOGICA (GENERAL)

> **Diagrama detectado:** Captura de Cisco Packet Tracer que muestra una topología de red lógica con un switch central modelo 2960-24TT ([[Switch0]]) conectado a varios dispositivos finales ([[PC-PT]]): 
> - En la parte superior izquierda, la **VLAN 10 (DIRECCIÓN ADMINISTRATIVA)** con los hosts `PC0` y `PC1`.
> - En la parte superior derecha, la **VLAN 20 (DIRECCIÓN COMPRAS PÚBLICAS)** con los hosts `PC2`, `PC3` y un host adicional (`PC4`) conectado al sistema mediante consola.
> - Se observa el enlace entre los equipos y el switch central.

---

## PING DENTRO DE LA RED DE DIRECCION ADMINISTRATIVA (PC0 A PC1)

> **Captura de código detectada:** Consola de comandos de Packet Tracer (`C:\>`) realizando una prueba de conectividad mediante [[Ping]] hacia la dirección IP `192.168.1.21`. Se observan los tiempos de respuesta (Time <1ms, TTL=128) y las estadísticas finales con 0% de pérdida de paquetes (`Packets: Sent = 4, Received = 4, Lost = 0`).

---

## PING DENTRO DE LA RED DE DIRECCION DE COMPRAS PUBLICAS (PC2 A PC3)

> **Captura de código detectada:** Consola de comandos de Packet Tracer (`C:\>`) ejecutando el comando `ping 192.168.1.21`. La respuesta muestra una comunicación exitosa entre los dispositivos de la VLAN 20, con tiempos de respuesta menores a 1 ms y 0% de pérdida de paquetes.