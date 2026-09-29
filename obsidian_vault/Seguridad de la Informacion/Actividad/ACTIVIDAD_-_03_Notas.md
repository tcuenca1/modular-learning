---
materia: Seguridad de la Informacion
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [seguridad_de_la_informacion, actividad, ingesta_ia]
---

# [[Seguridad de la Informacion]]

**Tema:** Amenazas y Vulnerabilidades  
**Asignatura:** Seguridad de la Información  
**Estudiantes:** [ESTUDIANTE], [ESTUDIANTE]  

## Objetivo
Que los estudiantes comprendan cómo identificar amenazas y vulnerabilidades en un sistema [[Windows]] utilizando [[Nmap]] en modo local (`localhost`), analizando los servicios expuestos y reflexionando sobre las medidas de seguridad necesarias.

## Recursos Necesarios
- Una máquina con [[Windows]] 10/11.
- Instalación de [[Nmap]] para [[Windows]] (incluye [[Zenmap]] opcional).
- Acceso a [[PowerShell]] o [[CMD]].
- Opcional: habilitar [[IIS]] o instalar [[XAMPP]] para simular servicios adicionales.

---

## Procedimiento de la Práctica

### 1. Instalación de [[Nmap]] (15 min)
- Descargar [[Nmap]] desde [nmap.org/download.html](https://nmap.org/download.html).
- Instalar [[Nmap]] en [[Windows]] (con opción de [[Zenmap]] si se desea usar interfaz gráfica).
- Abrir [[PowerShell]] o [[CMD]] para verificar que funciona ejecutando: `nmap -v localhost`

> **Captura de pantalla detectada (Página 3):** Ventana de instalación de Nmap indicando la ruta de destino seleccionada ("Program Files (x86)\Nmap"), el espacio requerido (89.6 MB) y el espacio disponible (259.8 GB).

### 2. Escaneo básico de `localhost` (10 min)
- Ejecutar en [[PowerShell]]:
  `nmap -v localhost`
- Observar los puertos abiertos (ej: 135, 445, 3389).
- Anotar qué servicios están asociados a esos puertos.

> **Captura de pantalla detectada (Página 3):** Consola de comandos (CMD) mostrando la ejecución de `nmap` con los resultados del escaneo en `localhost` (`127.0.0.1`), indicando los puertos descubiertos (135/tcp, 445/tcp, 3000/tcp, 5432/tcp, 7070/tcp) y el estado de los mismos.

Los puertos que se lograron identificar en el escaneo de `nmap` fueron:
- Puerto `135/tcp`: `msrpc`.
- Puerto `445/tcp`: `microsoft-ds`.
- Puerto `3000/tcp`: `ppp`.
- Puerto `5432/tcp`: [[PostgreSQL]].
- Puerto `7070/tcp`: `realserver`.

---

### 3. Escaneo con detección de servicios (10 min)
- Ejecutar:
  `nmap -sV localhost`
- Revisar la versión de los servicios detectados.
- Ejemplo: puerto 80 ([[IIS]]/[[Apache]]) si está instalado, puerto 3389 ([[RDP]]) si está habilitado.

> **Captura de pantalla detectada (Página 4):** Consola de comandos ejecutando `nmap -sV localhost` y mostrando las versiones detalladas de los servicios detectados en los puertos abiertos del sistema local.

Los puertos que se lograron identificar en el escaneo de `nmap` fueron:
- Puerto `135/tcp`: Ejecuta la versión Microsoft Windows RPC.
- Puerto `445/tcp`: Se identifica como `microsoft-ds` sin versión exacta confirmada.
- Puerto `3000/tcp`: Se identifica como `ppp` sin versión exacta confirmada.
- Puerto `5432/tcp`: Ejecuta [[PostgreSQL]] DB configurado en idioma Español.
- Puerto `7070/tcp`: Se identifica como `realserver` sin versión exacta confirmada.

---

### 4. Opcional: Simulación de servicios adicionales (10 min)
- Instalar [[XAMPP]] o habilitar [[IIS]] para abrir el puerto 80.
- Repetir el escaneo con `nmap -sV localhost`.
- Comparar resultados y discutir riesgos.

> **Captura de pantalla detectada (Página 5):** Interfaz gráfica de [[Internet Information Services (IIS)]] en Windows mostrando la activación de servicios World Wide Web y Servidor FTP, junto con una captura de consola ejecutando `nmap -sV localhost` donde ahora aparece el puerto 80 (`http` - Microsoft IIS httpd 10.0).

---

## Análisis de Resultados y Mitigación

| Puerto y Servicio detectado | Amenaza Potencial | Vulnerabilidad Relacionada | Medidas de Mitigación |
| :--- | :--- | :--- | :--- |
| **80** (Microsoft [[IIS]] httpd 10.0) | Acceso no autorizado a directorios web, o ataques web a las aplicaciones alojadas. | Servidor web expuesto con configuraciones por defecto o vulnerabilidades en los scripts habilitados. | Detener el servicio [[IIS]] desde `services.msc` cuando no se use y bloquear conexiones externas al puerto 80 mediante el [[Firewall]]. |
| **135** (Microsoft Windows [[RPC]]) | Enumeración del sistema para extraer perfiles de red y servicios. | Exposición del asignador de puertos (Endpoint Mapper) a redes externas. | Configurar el [[Firewall]] local de [[Windows]] para denegar tráfico entrante del exterior al puerto. |
| **445** (`microsoft-ds` / [[SMB]]) | Ejecución remota de código y propagación de [[malware]] (ej. [[Ransomware]]). | Fallos críticos a nivel de protocolo por falta de instalación de parches en el sistema operativo. | Instalar las últimas actualizaciones de Windows Update y bloquear las conexiones entrantes en el [[Firewall]]. |
| **3000** (`ppp?` / Posible entorno web) | Exposición de código fuente, [[API]]s o bases de datos de prueba sin protección. | Interfaces de desarrollo corriendo sin autenticación o con configuraciones por defecto. | Configurar la aplicación de desarrollo para escuchar solo en `localhost` o cerrar el proceso al terminar. |
| **5432** ([[PostgreSQL]]) | Extracción, alteración o borrado de la información en la base de datos. | Uso de credenciales débiles contra el usuario administrador o exposición a cualquier IP. | Modificar `pg_hba.conf` para permitir únicamente conexiones locales (`127.0.0.1`) y usar contraseñas fuertes. |
| **7070** (`realserver?` / Acceso remoto) | Toma de control remoto del equipo por atacantes externos. | Uso de software de escritorio remoto de terceros mal configurado o vulnerable. | Verificar el proceso asociado usando `netstat -ano`. Si es un software de acceso, configurar listas de control de acceso ([[ACL]]) o cerrarlo cuando no se use. |

---

## Informe de la Práctica
Cada estudiante debe entregar un informe con:
- Captura de pantalla de los resultados de [[Nmap]].
- Lista de puertos y servicios encontrados en `localhost`.
- Análisis de amenazas y vulnerabilidades.
- Medidas de mitigación sugeridas.