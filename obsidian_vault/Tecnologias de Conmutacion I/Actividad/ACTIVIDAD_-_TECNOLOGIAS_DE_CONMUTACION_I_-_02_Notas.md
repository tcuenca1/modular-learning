---
materia: Tecnologias de Conmutacion I
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [tecnologias_de_conmutacion_i, actividad, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Taller Intraclase: Configuración Inicial de un Switch [[Cisco]] 2960 en [[Cisco Packet Tracer]]

**Estudiantes:** [ESTUDIANTE], [ESTUDIANTE]

## Objetivos
- Acceder a la [[CLI]] del switch [[Cisco Catalyst]] 2960.
- Configurar nombre de host y contraseñas para el acceso seguro.
- Explorar los modos de operación del [[CLI]]: usuario, privilegiado y configuración global.
- Guardar configuraciones y verificar archivos de configuración `running-config` y `startup-config`.

## Materiales
- [[Cisco Packet Tracer]]
- 1 Switch [[Cisco]] 2960
- 1 PC (con cable de consola)

---

## Parte 1: Acceso a la [[CLI]] del Switch

1. Abrir [[Cisco Packet Tracer]].
2. Arrastrar un Switch 2960 al área de trabajo.
3. Arrastrar una PC y conéctala al switch por puerto consola:
   - Usar un cable consola azul: conecta desde RS-232 de la PC al puerto consola del switch.
4. Dar clic en la PC → pestaña Desktop → abre Terminal.
5. Aceptar los valores por defecto y aparecerá el prompt [[CLI]].

> **Captura de pantalla detectada:** Ventana de configuración del Terminal en la [[CLI]] de [[Cisco Packet Tracer]] mostrando el texto inicial de arranque del sistema operativo [[Cisco IOS]] (Version 15.0) y la petición `Press RETURN to get started!`.

---

## Parte 2: Configuración Básica del Switch

1. En la terminal, aparecerá:
   ```text
   Switch>
   ```
2. Ingresar al modo privilegiado:
   ```text
   enable
   ```
3. Ingresar al modo de configuración global:
   ```text
   configure terminal
   ```
4. Cambiar el nombre del switch:
   ```text
   hostname SW1
   ```
5. Configurar una contraseña para el modo privilegiado:
   ```text
   enable secret cisco123
   ```
6. Configurar una contraseña para consola:
   ```text
   line console 0
   password consola123
   login
   exit
   ```
7. Configurar una contraseña para [[Telnet]] ([[VLAN|vty lines]]):
   ```text
   line vty 0 4
   password telnet123
   login
   exit
   ```

> **Captura de pantalla detectada:** Consola interactiva del switch `SW1` mostrando la ejecución secuencial de los comandos de configuración básica para habilitar contraseñas secretas, de consola y de [[Telnet]].

---

## Parte 3: Verificación de los Modos y Ayuda de Comandos

1. Usar `?` para listar comandos posibles:
   ```text
   SW1# ?
   ```
2. Observar el cambio de modo con los distintos niveles:
   - `SW1>` → modo usuario

> **Captura de pantalla detectada:** Salida del comando `SW1?>` en la consola mostrando la lista completa de comandos ejecutables disponibles en el modo de usuario (EXEC commands) como `connect`, `disable`, `enable`, `exit`, `ping`, `show`, `telnet`, etc.

   - `SW1#` → modo privilegiado

> **Captura de pantalla detectada:** Salida del comando `SW1#?` en la consola mostrando la lista extendida de comandos privilegiados disponibles como `clear`, `clock`, `configure`, `copy`, `debug`, `reload`, `write`, entre otros.

   - `SW1(config)#` → modo configuración global

> **Captura de pantalla detectada:** Salida del comando `SW1(config)#?` detallando las opciones de configuración global tales como `aaa`, `banner`, `hostname`, `interface`, `ip`, `line`, `vlan`, etc.

   - `SW1(config-line)#` → configuración específica de línea

> **Captura de pantalla detectada:** Salida del comando `SW1(config-line)#?` mostrando los comandos de configuración de línea de terminal ([[CLI]]) como `exec-timeout`, `logging`, `password`, `transport`.

---

## Parte 4: Almacenamiento y Archivos de Configuración

1. Guardar la configuración en la [[NVRAM]]:
   ```text
   copy running-config startup-config
   ```
2. Verificar los archivos:
   ```text
   show running-config
   show startup-config
   ```

> **Captura de pantalla detectada:** Consola mostrando la ejecución del comando `copy running-config startup-config` con el mensaje resultante `[OK]` y fragmentos de las salidas de los comandos `show startup-config` y `show running-config` detallando la versión de [[Cisco IOS]] 15.0, el hostname `SW1`, la encriptación del `enable secret` y las interfaces `FastEthernet0/1` y `FastEthernet0/2`.