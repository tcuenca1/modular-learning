---
materia: Seguridad de la Informacion
tipo: actividad
fecha_procesamiento: 2026-10-01
tags: [seguridad_de_la_informacion, actividad, ingesta_ia]
---

# [[Seguridad de la Informacion]] - Taller Intraclase N°: 03

**FECHA:** 24/09/2026  
**UNIDAD N°1:** [[Fundamentos y riesgos de seguridad de la información]]  
**TEMA:** [[Amenazas y Vulnerabilidades]]  
**OBJETIVO:** Identificar aspectos relacionados con las principales amenazas y vulnerabilidades de la [[Seguridad de la Informacion]].

---

## TIPO DE ACTIVIDAD

* **LUGAR:** Intraclase
* **ALCANCE:** Individual
* **FORMA:** Taller

---

## ROLES Y RESPONSABILIDADES DE LOS PARTICIPANTES EN LA TAREA:

| NOMBRE ESTUDIANTE | ROL | DESCRIPCIÓN |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |

---

## Análisis de Casos: Amenazas, Vulnerabilidades y Consecuencias

### CASO 1: Ataque de [[Phishing]]

* **La amenaza:** Un ciberdelincuente que ejecuta [[ingeniería social]] mediante correos electrónicos maliciosos diseñados para suplantar la identidad de una autoridad corporativa.
* **La vulnerabilidad explotada:** La falta de capacitación técnica a los empleados, combinada a la ausencia de controles técnicos de validación de correo.
* **Las consecuencias:** El robo de credenciales corporativa, afectando la [[Confidencialidad]] y la [[Integridad]] de los accesos, lo cual permite al atacante escalar privilegios, filtrar datos sensibles o desplegar [[Ransomware]].

---

### CASO 2: Fuga de Datos en la Nube

* **La amenaza:** Acceso no autorizado a repositorios de almacenamiento en la [[Computación en la nube]] (contenedores de Amazon o Azure) por parte de atacantes externos o bots de escaneo que buscan datos expuestos.
* **La vulnerabilidad explotada:** Una mala configuración de seguridad en la arquitectura encargada de gestionar la conexión a la nube, como permisos de acceso públicos o políticas de control de identidad demasiado permisivas sin autenticación.
* **Las consecuencias:** Exposición pública masiva de información confidencial de clientes o de propiedad intelectual, ocasionando impactos legales, multas por incumplimiento de normativas de privacidad y daño reputacional.

---

### CASO 3: Incendio en un Data Center

* **La amenaza:** Un fallo físico o desastre ambiental como un cortocircuito eléctrico o fallas en los sistemas de supresión de incendios.
* **La vulnerabilidad explotada:** Deficiencias en la infraestructura física, fallo en sistemas redundantes de energía ([[UPS]]), falta de cumplimiento de normativas de construcción anti-incendios.
* **Las consecuencias:** Interrupción total de la operación y posible destrucción física de los servidores impactando la [[Disponibilidad]] y la [[Integridad]] de los datos. Si no existen respaldos previos puede haber una pérdida permanente de información crítica.

---

### CASO 4: Empleado Descontento con Altos Privilegios

* **La amenaza:** Es una [[amenaza interna]], específicamente un empleado actual o recientemente desvinculado por motivaciones maliciosas, como espionaje corporativo o lucro personal.
* **La vulnerabilidad explotada:** Falta de segregación de funciones, deficiencias en los controles de monitoreo continuo de registros de actividad, y una tardía revocación de credenciales luego de la salida del personal.
* **Las consecuencias:** Posible sabotaje de sistemas, robo de bases de datos o encriptación de información interna, afectando la [[Confidencialidad]], [[Integridad]] y [[Disponibilidad]]. Mientras mas alto sea el privilegio el daño puede ser más silencioso y difícil de rastrear en el corto plazo.