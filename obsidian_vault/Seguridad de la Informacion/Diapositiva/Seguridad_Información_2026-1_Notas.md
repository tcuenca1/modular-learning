---
materia: Seguridad de la Informacion
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [seguridad_de_la_informacion, diapositiva, ingesta_ia]
---

# [[Seguridad de la Informacion]]

---

## UNIVERSIDAD TÉCNICA DE MACHALA
### FACULTAD DE INGENIERÍA CIVIL
#### CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN

**Profesores:** [DOCENTE], Mg.  
**Asignatura:** Seguridad de la Información

---

## INTRODUCCIÓN

### CLASE #1
- Asistencia
- Horario de tutorías
- Comunicación oficial a través de correo electrónico
- Políticas generales:
  - Respeto, Puntualidad, Responsabilidad, Disciplina, Honestidad Académica.

- CPE: 16 horas
- Aula virtual
- Semestre: 6to
  - Syllabus
  - Parámetros de evaluación, etc.

---

### UNIDAD I: FUNDAMENTOS Y RIESGOS DE SEGURIDAD DE LA INFORMACIÓN

**Tema:** Introducción a la Seguridad de la Información.  
**Objetivo:** Identificar conceptos relacionados con la seguridad de la información para la fundamentación de la asignatura.

---

## ¿Por qué preocuparse por la seguridad de la información?

> **Imagen detectada:** Icono de interrogación rojo con una figura en 3D reflexionando junto al signo de interrogación.

**Problemas comunes:**
- Destrucción de la información y otros recursos.
- Modificación o distorsión de información.
- Robo, eliminación o pérdida de información u otros recursos.
- La revelación de información.
- La interrupción de los servicios.

---

## Definiciones

> **Imagen detectada:** Ilustración de una persona interactuando con un icono de carpeta digital protegida por un candado y un archivo con forma de llave.

* **La seguridad de la información** incluye la protección de: información, sistemas, recursos y demás activos contra: desastres, errores (intencionales o no) y manipulación no autorizada, para reducir la probabilidad y el impacto de los incidentes de seguridad.

* De acuerdo con la norma **[[ISO/IEC 27002]]:2007**, la seguridad de la información es la protección de la información contra los diversos tipos de amenazas para garantizar la **continuidad del negocio**, minimizando los riesgos y maximizando el retorno sobre la inversión y las oportunidades de negocio.
* La seguridad de la información se obtiene como resultado de la implementación de un conjunto de **controles**, que comprenden políticas, procesos, procedimientos, estructuras organizacionales y funciones de hardware y software.

---

## Otros conceptos relacionados...

> **Imagen detectada:** Ilustración de un personaje con capucha (hacker) corriendo con una bolsa de dinero y un ordenador portátil que muestra una alerta de seguridad.

1. **Incidente de seguridad:** corresponde a cualquier evento adverso relacionado con la seguridad, por ejemplo, ataques de denegación de servicio (**[[DoS]]**), robo de información, fuga y la obtención de un acceso no autorizado a la información.

2. **Activo:** cualquier elemento que tenga valor para la organización y su negocio. Algunos ejemplos: bases de datos, software, equipos (computadores, notebooks), servidores, dispositivos de red (**[[routers]]**, **[[switches]]**, etc), personas, procesos y servicios.

> **Diagrama detectado:** Esquema radial de "Activos de Información" ubicando en el centro al activo y conectándolo con: Datos/Información, Personal, Red de comunicaciones, Ubicación física, Servicios, Hardware y Software.

3. **Amenaza:** cualquier evento que explote vulnerabilidades. Causa potencial de un incidente no deseado, que puede resultar en daños a un sistema u organización.

> **Imagen detectada:** Ilustración de una persona frente a un ordenador portátil rodeada de iconos flotantes de amenazas (virus, calaveras, maletines, etc.).

4. **Vulnerabilidad:** cualquier debilidad que puede ser explotada y ponga en peligro la seguridad de los sistemas y datos.
   - Fragilidad de un activo o grupo de activos que pueden ser explotados por una o más amenazas.
   - Las configuraciones incorrectas en el equipo o en la seguridad también permiten la creación de vulnerabilidades.

5. **Riesgo:** combinación de la probabilidad (oportunidad de que la amenaza se materialice) de que ocurra un evento y sus consecuencias para la organización. Algo que puede ocurrir y sus efectos sobre los objetivos de la organización.

---

## Diferencias entre seguridad de la información, seguridad informática y ciberseguridad

| Enfoque | Objetivo | Ejemplo |
| :--- | :--- | :--- |
| **Seguridad de la información** | Protege toda la información (activos), sin importar el formato. | Garantizar la confidencialidad, integridad y disponibilidad de la información. | Proteger documentos impresos, bases de datos, grabaciones, correos electrónicos, etc. |
| **Seguridad informática** | Se centra en proteger los sistemas informáticos (hardware, software, redes internas). | Evitar accesos no autorizados, fallos técnicos o pérdida de datos en los sistemas. | Antivirus, firewalls, control de acceso a servidores. |
| **[[Ciberseguridad]]** | Protege los sistemas y datos que están conectados a internet. | Defender contra amenazas externas como hackers, **[[malware]]**, **[[phishing]]**, etc. | Seguridad en redes sociales, banca en línea, comercio electrónico. |

> **Diagrama detectado:** Gráfico de conjuntos de Venn donde un óvalo grande ("Seguridad de la Información") contiene parcialmente a un círculo gris ("Seguridad informática") y se intersecta con un círculo celeste ("[[Ciberseguridad]]").

---

### SEGURIDAD DE LA INFORMACIÓN VS SEGURIDAD INFORMÁTICA

- **SEGURIDAD DE LA INFORMACIÓN:** Se refiere a la protección de los activos de información fundamentales para el éxito de cualquier organización. $\neq$
- **LA SEGURIDAD INFORMÁTICA:** Se refiere a la protección de las infraestructuras de las tecnologías de la información y comunicación que soportan nuestro negocio.

> **Diagrama detectado:** Tres círculos superpuestos indicando los componentes organizacionales: Tecnología (verde), Personas (rojo) y Procesos (celeste).

---

## CLASE #2
**UNIDAD I: FUNDAMENTOS Y RIESGOS DE SEGURIDAD DE LA INFORMACIÓN**  
**Tema:** Pilares de la seguridad de la información.  
**Objetivo:** Identificar los pilares y servicios de la seguridad de la información.

---

## Pilares de la Seguridad de la Información (CID)

> **Diagrama detectado:** Pirámide tridimensional donde la base tiene los vértices "Confidencialidad" y "Disponibilidad", el vértice superior es "Integridad", y en el triángulo central muestra el texto "Seguridad de la Información".

### Introducción
- Si otra persona entra con su usuario y contraseña, ¿qué pasa?
- Si alguien cambia sus calificaciones sin permiso, ¿qué principio se rompe?
- ¿Qué pasaría si hoy se borran todas las notas de la plataforma académica?

---

### Confidencialidad
> **Imagen detectada:** Teclado de ordenador con una tecla iluminada con la inscripción "Access denied" y cubierto por cadenas con candado.

- La información solo tiene que ser accesible o divulgada a aquellos que están autorizados.
- La pérdida de la confidencialidad se produce cuando hay una violación de la confidencialidad de cierta información (por ejemplo, la contraseña de un usuario o administrador del sistema).
- Comprende la protección de los datos transmitidos contra ataques pasivos, es decir, el acceso no autorizado, que incluirá medidas tales como el control de acceso y encriptación.
  - *Ejemplo:* Mensajes de WhatsApp sin cifrar.

---

### Integridad
> **Imagen detectada:** Ilustración de un personaje junto a cuatro opciones de integridad de datos: Datos duplicados, Datos faltantes, Datos alterados y Datos incorrectos (tachado con una 'X').

- La información debe permanecer correcta (**integridad de datos**) y como el emisor la originó (**integridad de fuente**) sin manipulaciones por terceros.
- Es la garantía contra ataques activos a través de los cambios o de remociones no autorizadas.
- La integridad es también un prerrequisito para otros servicios de seguridad. Por ejemplo, si la integridad de un sistema de control de acceso a un sistema operativo es violada, también se viola la confidencialidad de sus archivos.
- La pérdida de la integridad se produce en un momento en que cierta información está expuesta a la manipulación por personal no autorizado, que hace cambios que no fueron aprobados y no están bajo el control del propietario de la información (corporativo o privado).
  - *Ejemplo:* Transacción bancaria alterada.

---

### Disponibilidad
- La información debe estar siempre accesible para aquellos que estén autorizados.
- La pérdida de la disponibilidad sucede cuando la información deja de estar accesible para aquellos que la necesitan.
- Sería el caso de pérdida de comunicación con un sistema importante para la organización, que ocurrió al caer un servidor o una aplicación crítica para el negocio, que presentó una falla debido a un error causado por motivo interno o externo al equipo o por la acción de personas no autorizadas, con o sin intención maliciosa.
  - *Ejemplo:* Página de matrícula caída.

---

## Servicios de la Seguridad de la Información

### No repudio
> **Imagen detectada:** Dos personas discutiendo sobre un documento con un signo de interrogación a la izquierda y una 'X' roja a la derecha.

- Comprende el servicio que impide a una fuente o destino negar la transmisión de mensajes, es decir, cuando se envía el mensaje dado, el destino puede demostrar que éste fue enviado realmente por determinado origen y viceversa.
- El **no repudio** o irrenunciabilidad es un servicio de seguridad que permite probar la participación de las partes en una comunicación.
  - **No repudio en origen:** El emisor no puede negar que envió porque el destinatario tiene pruebas del envío.
  - **No repudio en destino:** El receptor no puede negar que recibió el mensaje porque el emisor tiene pruebas de la recepción.
- La posesión de un documento y su firma digital asociada será prueba efectiva del contenido y del autor del documento.

---

### Autenticidad
- Está interesada en garantizar que la comunicación sea auténtica, es decir, origen y destino pueden verificar la identidad de la otra parte implicada en la comunicación, con el fin de confirmar que la otra parte es quien dice ser.
- Verificar que no hayan impostores.
- El origen y el destino son normalmente usuarios, dispositivos o procesos.

### Conformidad
- Cumplir y hacer cumplir las regulaciones internas y externas impuestas a las actividades de la organización.
- Estar en conformidad es estar de acuerdo, siguiendo y haciendo cumplir las leyes y reglamentos internos y externos.

### Control de acceso
- Trata de limitar y controlar el acceso lógico / físico a los activos de una organización a través del proceso de identificación, autenticación y autorización, con el fin de proteger los recursos contra el acceso no autorizado.

---

## Ataques a la información
- El ataque es un acto deliberado de tratar de esquivar los controles de seguridad con el objetivo de explotar las vulnerabilidades.
- Para minimizar el impacto negativo provocado por ataques, existen procedimientos y mejores prácticas que facilitan la lucha contra las actividades delictivas y reducen notablemente el campo de acción de los ataques.
- Uno de los pasos más importantes en seguridad, es la **educación**.

### Modelos de ataques
1. **Interrupción:** Cuando un activo se destruye o queda indisponible (o inutilizable), caracterizando un ataque contra la disponibilidad. (*Ejemplo: la destrucción de un disco duro*).
2. **Interceptación:** Cuando se accede a un activo por un tercero no autorizado (persona o programa del computador), caracterizando un ataque contra la confidencialidad. (*Ejemplo: la copia no autorizada de archivos o programas*).
3. **Modificación:** Cuando se accede a un activo por un tercero no autorizado y se modifica, materializando un ataque contra la integridad. (*Ejemplo: cambio de los valores en un archivo de datos*).
4. **Fabricación:** Cuando una parte no autorizada inserta objetos falsificados en un activo, configurando un ataque contra la autenticidad. (*Ejemplo: la adición de registros en un archivo*).

---

### Formas de ataques
- **Ataques pasivos:** Ataques basados en escuchar y monitorear las transmisiones, con el fin de obtener la información que se está transmitiendo. (*Ejemplo: Escuchar una conversación telefónica*). Son difíciles de detectar debido a que no implica cambios en los datos, sin embargo, son posibles de prevenir con el uso de la **[[criptografía]]**.
- **Ataques activos:** Involucran la modificación de datos, la creación de objetos falsos o negación de servicio, y tienen las propiedades opuestas de ataques pasivos. Son difíciles de prevenir debido a la necesidad de una protección completa de todas las instalaciones de comunicaciones y procesamiento, durante todo el tiempo. Es posible detectarlos y aplicar una medida para la recuperación de los perjuicios causados.

---

## NORMATIVA ECUATORIANA
- [Enlace a Guía EGSI](https://www.gobiernoelectronico.gob.ec/egsi/) *(Resumen del Ciclo: Planificar, hacer, verificar, actuar)*
- [Guía para la implementación del EGSI (PDF)](https://www.gobiernoelectronico.gob.ec/wp-content/uploads/2020/04/GUÍA-PARA-LA-IMPLEMENTACIÓN-DEL-EGSI-ABRIL2020.pdf)

---

## CLASE #3
**UNIDAD I: FUNDAMENTOS Y RIESGOS DE SEGURIDAD DE LA INFORMACIÓN.**  
**Tema:** Amenazas y Vulnerabilidades.  
**Objetivo:** Identificar aspectos relacionados com las principales amenazas y vulnerabilidades de la seguridad de la información, reflexionando sobre la ética y la responsabilidad social en este contexto.

- [Enlace de referencia de noticias de seguridad de hospitales](https://www.nbcnews.com/tech/security/hackers-force-hospital-system-take-national-computer-system-offline-rcna98212)
- [Enlace informativo de la BBC](https://www.bbc.com/mundo/articles/cr71x5vgr9go)

---

### ¿Qué consideran más peligroso: una amenaza externa como un hacker o una vulnerabilidad interna como una mala contraseña?

- **Amenaza:** Potencial causa de un incidente no deseado (*ej: hacker, incendio, [[malware]]*).
- **Vulnerabilidad:** Debilidad que puede ser explotada (*ej: contraseñas débiles, mala configuración*).
- **Ataque:** Un ataque es cuando la amenaza se materializa y explota una vulnerabilidad. Es un acto deliberado de tratar de esquivar los controles de seguridad con el objetivo de explotar las vulnerabilidades.
- **Riesgo:** Probabilidad de que una amenaza explote una vulnerabilidad y cause impacto. Combinación de la probabilidad de que ocurra un evento y sus consecuencias para la organización.
- **Impacto:** Consecuencias que afectan la confidencialidad, integridad o disponibilidad.

---

### Tipos de Amenazas
- **Naturales:** Terremotos, inundaciones, incendios.
- **Accidentales:** Errores humanos, borrado involuntario de datos.
- **Intencionales:** **[[Malware]]**, **[[ransomware]]**, **[[phishing]]**.
- **Organizacionales:** Procesos internos deficientes.

#### Amenazas específicas:
- **Ataques de denegación de servicio (**[[DoS]]**):** Ocurren cuando los atacantes impiden que un sistema informático satisfaga solicitudes legítimas sobrecargando las redes y los servidores con tráfico.
- **Ataques de denegación de servicio distribuido (**[[DDoS]]**):** El tráfico entrante que inunda a la víctima proviene de varias fuentes diferentes, lo que hace imposible detener el ataque bloqueando una sola fuente de tráfico.
- **Hombre en el medio (**[[Man-in-the-middle]]**):** Tipo de amenaza donde un atacante intercepta la comunicación entre dos individuos para robar datos, sin que ni el emisor ni el receptor sean conscientes de que dichos datos están siendo robados.
- **[[Malware]]:** Todo tipo de software malicioso o dañino cuyo objetivo sea infectar ordenadores, tabletas o teléfonos móviles.

---

### Tipos de [[Malware]]
- **Virus:** Tipo de malware formado por una parte contagiosa de código que infecta otro software en el sistema donde reside y se propaga una vez que se ejecuta.
- **Gusano (worm):** Programas que realizan copias de sí mismos, utilizando mecanismos de propagación activos (autoenviándose por correo electrónico) o pasivos (infectando archivos y esperando a que este sea compartido con otro usuario).
- **Troyano (trojan):** Se disfraza de software legítimo para engañar a los usuarios y obtener acceso a sus sistemas, abriendo así una puerta trasera para que los atacantes puedan robar información confidencial, acceder remotamente al equipo o realizar otras acciones maliciosas.
- **[[Ransomware]]:** Programas que tienen como objetivo cifrar ficheros o todo el sistema de almacenamiento, informando al usuario de que únicamente mediante el pago de una determinada cantidad de dinero podrá recuperar la información perdida.
- **[[Spyware]]:** Software malicioso que se instala sin consentimiento, con el objetivo de recopilar información personal y actividades del usuario (contraseñas, tarjetas de crédito, historial) y enviarla a terceros.
- **[[Phishing]]:** Engaños para obtener información personal o credenciales de acceso mediante correos electrónicos, sitios web falsos o mensajes de texto.
- **Puerta trasera (backdoor):** Su propósito principal es permitir el control remoto de un dispositivo mediante la recepción de comandos enviados desde el exterior por un atacante.
- **Keylogger:** Tipo de spyware que registra las pulsaciones del teclado del equipo infectado.
- **Adware:** Software no deseado diseñado para mostrar anuncios en el dispositivo de la víctima, generando un beneficio económico.

---

### Tipos de Vulnerabilidades
1. **Técnicas:** Fallos de software, sistemas sin parches, configuraciones inseguras, protocolos obsoletos (Telnet, FTP), aplicaciones web mal diseñadas (inyección SQL, XSS), hash o cifrado débil (MD5, DES).
2. **Humanas:** Contraseñas débiles o reutilizadas ("123456", "admin"), ingeniería social, falta de capacitación, uso indebido de dispositivos (USB infectadas).
3. **Físicas:** Acceso no autorizado a salas de servidores, equipos sin protección contra incendios o inundaciones, dispositivos perdidos o robados, cámaras sin seguridad.
4. **Organizacionales:** No implementar respaldos periódicos, falta de monitoreo y auditorías, gestión deficiente de accesos (empleados retirados con cuentas activas).

---

### Ética y Responsabilidad Social
- La ética profesional ayuda a prevenir amenazas internas.
- La responsabilidad social garantiza la protección de los datos de los usuarios.
- Buenas prácticas: uso de contraseñas seguras, actualizaciones, capacitación.
- La seguridad no depende solo de la tecnología, sino de las decisiones humanas.

---

## CLASE #4
**UNIDAD I: FUNDAMENTOS Y RIESGOS DE SEGURIDAD DE LA INFORMACIÓN**  
**Tema:** Introducción a la Gestión de Riesgos de la Seguridad de la Información  
**Objetivo:** Reconocer los elementos básicos de la gestión de riesgos, incluyendo impacto y probabilidad, a través del análisis de activos.

### Conceptos Básicos
- **Riesgo:** Probabilidad de que una amenaza explote una vulnerabilidad y cause impacto.
- **Riesgo inherente:** Es el riesgo existente y propio de cada actividad, sin la ejecución de ningún control.
- **Riesgo residual:** El riesgo que permanece tras el tratamiento del riesgo.
- **Gestión de riesgos:** Es el proceso sistemático de identificar, analizar, evaluar y tratar los riesgos que afectan a los activos de información de una organización, con el objetivo de garantizar los principios de Confidencialidad, Integridad y Disponibilidad (**[[CIA]]**).

---

### Proceso para la Gestión del Riesgo
1. Establecimiento del contexto
2. Valoración del riesgo
3. Tratamiento del riesgo
4. Aceptación del riesgo
5. Comunicación del riesgo
6. Monitoreo y revisión del riesgo

---

## CLASE #5
**UNIDAD I: FUNDAMENTOS Y RIESGOS DE SEGURIDAD DE LA INFORMACIÓN**  
**Tema:** Tratamiento y Controles de Riesgos  
**Objetivo:** Aplicar técnicas de tratamiento de riesgos y selección de controles utilizando la matriz de riesgos.

### Tratamiento del Riesgo
El tratamiento de los riesgos consiste en tomar decisiones frente a los diferentes riesgos existentes de acuerdo a la estrategia de la institución. Existen cuatro opciones disponibles:
1. **Reducción del riesgo (mitigar):** Reducir mediante la selección de controles de manera que el riesgo residual sea aceptable.
2. **Evitación del riesgo:** Evitar la actividad o la acción que da origen al riesgo particular.
3. **Transferencia del riesgo:** Pasar la responsabilidad o el impacto a otra parte (por ejemplo, seguros o contratos).
4. **Aceptación del riesgo:** Aceptar los riesgos con conocimiento y objetividad si satisfacen los criterios de la institución.

---

## CLASE #6
**UNIDAD I: FUNDAMENTOS Y RIESGOS DE SEGURIDAD DE LA INFORMACIÓN**  
**Tema:** Aceptación y Comunicación de Riesgos.  
**Objetivo:** Desarrollar un plan de tratamiento de riesgos para su aceptación y comunicación.

- **Monitoreo y revisión de los factores de riesgo:** Los riesgos no son estáticos; las amenazas, vulnerabilidades, probabilidades y consecuencias cambian constantemente, requiriendo supervisión continua sobre activos nuevos, nuevas amenazas y cambios en los niveles de riesgo.

---

## CLASE #7
**UNIDAD II: METODOLOGÍAS, POLÍTICAS Y ESTÁNDARES**  
**Tema:** Metodologías y Mejores Prácticas.  
**Objetivo:** Identificar metodologías y buenas prácticas aplicables a la seguridad de la información.

- **Estándar:** Un conjunto de reglas formales y documentadas (*Ej: "Realizar un Sistema de Gestión de Seguridad de la Información"*).
- **Buena Práctica:** Una técnica o método que ha demostrado funcionar bien (*Ej: "Realizar copias de seguridad diarias"*).

### Familia [[ISO/IEC 27000]]
- **[[ISO/IEC 27001]]**: Norma principal de la serie que especifica los requisitos para implantar, mantener y certificar un [[Sistema de Gestión de Seguridad de la Información (SGSI)]].
- **[[ISO/IEC 27002]]**: Código de prácticas que describe los objetivos de control y controles recomendados (no es certificable).
- **[[NIST Cybersecurity Framework (NIST CSF)]]:** Marco de ciberseguridad organizado en cinco funciones principales: *Identify* (Identificar), *Protect* (Proteger), *Detect* (Detectar), *Respond* (Responder) y *Recover* (Recuperar).

---

## CLASE #8
**UNIDAD II: METODOLOGÍAS, POLÍTICAS Y ESTÁNDARES**  
**Tema:** Políticas de Seguridad.  
**Objetivo:** Identificar aspectos introductorios relacionados con las políticas de seguridad de la información.

- **Política de seguridad de la información:** Es un conjunto de lineamientos basados en normas y procedimientos que determinan las reglas a seguir para garantizar la seguridad de la información, de acuerdo con el tipo de negocio y los requisitos legales, contractuales, regulatorios y normativos.
- **Estructura jerárquica de la documentación de un SGSI:**
  - Políticas (Directrices - El "por qué")
  - Normas (Reglas básicas - El "qué")
  - Procedimientos (Actividades detalladas - El "cómo")
  - Instrucciones (Detalles de operaciones)
  - Registros / Evidencias

---

## CLASE #9 y #10
**UNIDAD II: METODOLOGÍAS, POLÍTICAS Y ESTÁNDARES**  
**Tema:** Desarrollo y Mantenimiento de Políticas  
**Objetivo:** Desarrollar políticas de seguridad de la información que integren principios éticos, ley de protección de datos y buenas prácticas normativas, enfatizando su comunicación y capacitación diferenciada según roles.

---

## CLASE #11
**UNIDAD II: METODOLOGÍAS, POLÍTICAS Y ESTÁNDARES**  
**Tema:** Sistema de gestión de seguridad de la Información ([[SGSI]]) - Parte 1. Ciclo de Deming.  
**Objetivo:** Identificar la estructura del SGSI según la norma [[ISO/IEC 27001]], aplicando el ciclo de Deming (**[[PHVA]]** / **[[PDCA]]**).

- **Planificar (Plan):** Establecer el SGSI, políticas, objetivos, procesos y procedimientos.
- **Hacer (Do):** Implementar y operar las políticas, controles, procesos y procedimientos del SGSI.
- **Verificar (Check):** Monitorear y analizar críticamente el desempeño del SGSI frente a las políticas y objetivos mediante auditorías.
- **Actuar (Act):** Tomar acciones correctivas y preventivas para lograr la mejora continua del SGSI.

---

## CLASE #12 y #13
**UNIDAD II: METODOLOGÍAS, POLÍTICAS Y ESTÁNDARES**  
**Tema:** Sistema de gestión de seguridad de la Información ([[SGSI]]) - Partes 2 y 3.  
**Objetivo:** Identificar el contexto organizacional (cláusula 4 de ISO 27001 mediante [[FODA]] y [[PESTEL]]), las partes interesadas, el liderazgo (cláusula 5), la planificación, el soporte (cláusula 7) y los controles operativos.

---

## CLASE #14 y #15
**UNIDAD III: MARCO LEGAL PARA LA PROTECCIÓN DE DATOS**  
**Tema:** Ley Orgánica de Protección de Datos de Ecuador ([[LOPDP]]) - Partes 1 y 2.  
**Objetivo:** Identificar los principios fundamentales, derechos de los titulares, categorías especiales de datos y las obligaciones del responsable y encargado del tratamiento de datos personales en el marco jurídico ecuatoriano.

- **Principios de Protección de Datos (LOPDP):** Juridicidad, lealtad, transparencia, finalidad, pertinencia, proporcionalidad, confidencialidad, calidad, conservación, seguridad, responsabilidad, aplicación favorable.
- **Derechos de los titulares:** Derecho a la información, acceso, rectificación y actualización, eliminación, oposición, portabilidad, suspensión del tratamiento, no ser objeto de decisiones automatizadas, consulta, educación digital.
- **Obligaciones del Responsable del tratamiento:** Cumplir principios, informar de manera clara, garantizar derechos de los titulares, obtener consentimiento cuando sea necesario, implementar medidas de seguridad, registrar incidentes y notificar vulneraciones, celebrar contratos con encargados, designar un [[Delegado de Protección de Datos (DPO)]] cuando aplique, etc.

---

## CLASE #16
**UNIDAD III: MARCO LEGAL PARA LA PROTECCIÓN DE DATOS**  
**Tema:** Ley Orgánica de Protección de Datos de Ecuador (Parte 2).  
**Objetivo:** Identificar las obligaciones del encargado del tratamiento de datos personales en la legislación ecuatoriana y cierre del contenido del semestre.

> **Imagen detectada:** Sello oficial de la Universidad Técnica de Machala junto al mensaje final de agradecimiento ("¡Gracias!").