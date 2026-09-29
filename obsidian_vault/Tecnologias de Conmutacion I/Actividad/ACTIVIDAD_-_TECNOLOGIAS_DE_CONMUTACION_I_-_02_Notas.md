---
materia: Tecnologias de Conmutacion I
tipo: actividad
fecha_procesamiento: 2026-09-28
tags: [tecnologias_de_conmutacion_i, actividad, ingesta_ia]
---

[[Tecnologias de Conmutacion I]]

# Taller Intraclase: Configuración Inicial de un Switch Cisco 2960 en [[Cisco Packet Tracer]]

**Estudiantes:** [ESTUDIANTE 1], [ESTUDIANTE 2]

## Objetivos
* Acceder a la [[CLI]] del switch [[Cisco Catalyst 2960]].
* Configurar nombre de host y contraseñas para el acceso seguro.
* Explorar los modos de operación del [[CLI]]: usuario, privilegiado y configuración global.
* Guardar configuraciones y verificar archivos de configuración `running-config` y `startup-config`.

## Materiales
* [[Cisco Packet Tracer]]
* 1 Switch Cisco 2960
* 1 PC (con cable de consola)

---

## Parte 1: Acceso a la CLI del Switch

1. Abrir [[Cisco Packet Tracer]].
2. Arrastrar un Switch 2960 al área de trabajo.
3. Arrastrar una PC y conéctala al switch por puerto consola:
   * Usar un cable consola azul: conecta desde RS-232 de la PC al puerto consola del switch.
4. Dar clic en la PC → pestaña Desktop → abre Terminal.
5. Aceptar los valores por defecto y aparecerá el prompt [[CLI]].

> **Captura de pantalla detectada (Página 1):** Muestra el entorno de [[Cisco Packet Tracer]] con una PC conectada a un switch mediante un enlace de consola azul (`RS-232` al puerto `Console`). Debajo se observa la ventana de la terminal interactiva mostrando la secuencia de arranque (*boot*) del [[Cisco Catalyst 2960]] con la línea final "Press RETURN to get started!".

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
7. Configurar una contraseña para [[Telnet]] (vty lines):
   ```text
   line vty 0 4
   password telnet123
   login
   exit
   ```

> **Captura de pantalla detectada (Página 2):** Se visualiza la terminal de comandos ejecutando exitosamente la configuración básica: asignación del nombre de host (`hostname SW1`), habilitación de la contraseña secreta (`enable secret`), y configuración de las líneas de acceso por consola (`line console 0`) y [[Telnet]] (`line vty 0 4`) con sus respectivas contraseñas y comandos `login`.

---

## Parte 3: Verificación de los Modos y Ayuda de Comandos

1. Usar `?` para listar comandos posibles:
   ```text
   SW1# ?
   ```
2. Observar el cambio de modo con los distintos niveles:
   * `SW1>` → modo usuario
   * `SW1#` → modo privilegiado

> **Captura de pantalla detectada (Página 3):** Despliegue de la ayuda de comandos utilizando el signo de interrogación (`?`) tanto en el modo usuario (`SW1>`) como en el modo privilegiado (`SW1#`), listando los comandos ejecutables disponibles para cada nivel de privilegios.

> **Captura de pantalla detectada (Página 4):** Continuación de la ayuda interactiva en el [[CLI]], mostrando el menú de comandos para el modo de configuración global (`SW1(config)#`) y para la configuración específica de línea (`SW1(config-line)#`).

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

> **Captura de pantalla detectada (Página 5):** Salida de comandos en la terminal donde se ejecuta la copia de seguridad de la configuración actual hacia la memoria no volátil (`copy running-config startup-config`), seguida de las verificaciones mediante `show running-config` y `show startup-config`, donde se aprecia la contraseña cifrada (`enable secret 5 ...`), el nombre del equipo (`hostname SW1`) y las interfaces configuradas.