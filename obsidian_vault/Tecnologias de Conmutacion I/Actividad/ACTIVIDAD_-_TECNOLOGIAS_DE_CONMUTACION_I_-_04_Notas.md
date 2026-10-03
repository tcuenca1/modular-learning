---
materia: Tecnologias de Conmutacion I
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, actividad, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Taller 2 S3

**Nombres:** [ESTUDIANTE], [ESTUDIANTE].  
**Fecha:** 22/09/2026  

---

De la [[topologia de red]] planteada por el docente configurar lo siguiente:

> **Diagrama detectado:** Topología de red en Cisco Packet Tracer que muestra un switch central (`Switch0`) de modelo `2960-24TT` conectado a múltiples computadoras (`PC0`, `PC1`, `PC2`, `PC3`, `PC4`). Se aprecian dos agrupaciones lógicas enmarcadas en óvalos:
> - **VLAN 10 (DIRECCIÓN ADMINISTRATIVA):** Enmarca a `PC0` y `PC1` conectados al switch.
> - **VLAN 20 (DIRECCIÓN COMPRAS PÚBLICas):** Enmarca a `PC2` y `PC3` conectados al switch, junto con una conexión hacia `PC4` (consola u otro equipo).

- Dos [[VLAN]]s: 10 y 20.
- Cinco host (2 host a la [[VLAN]] 10; 2 host a la [[VLAN]] 20 y 1 host a consola).
- Todos los host deben pertenecer a la misma red.
- Comprobar las conexiones entre los hosts que estan en las [[VLAN]] 10 y [[VLAN]] 20.

---

## TOPOLOGIA LOGICA (GENERAL)

> **Captura de pantalla detectada:** Interfaz general del simulador [[Cisco Packet Tracer]] mostrando el diseño lógico completo del taller con los dispositivos interconectados.

---

## PING DENTRO DE LA RED DE DIRECCION ADMINISTRATIVA (PC0 A PC1)

> **Captura de pantalla detectada:** Consola de línea de comandos de una PC ejecutando el comando `ping 192.168.1.21` (o similar), mostrando respuestas exitosas (`Reply from... bytes=32 time<1ms TTL=128`) y una tasa de pérdida de paquetes del 0%.

---

## PING DENTRO DE LA RED DE DIRECCION DE COMPRAS PUBLICAS (PC2 A PC3)

> **Captura de pantalla detectada:** Consola de línea de comandos ejecutando una prueba de conectividad mediante `ping` entre `PC2` y `PC3`, evidenciando conectividad exitosa sin pérdida de paquetes (`0% loss`).