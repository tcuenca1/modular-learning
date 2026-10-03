---
materia: Seguridad de la Informacion
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [seguridad_de_la_informacion, diapositiva, ingesta_ia]
---

[[Seguridad de la Informacion]]

# Universidad Técnica de Machala
## Facultad de Ingeniería Civil
### Carrera de Tecnologías de la Información

**Asignatura:** Seguridad de la Información  
**Profesores:** [DOCENTE]  

---

## Introducción (Clase #1)
- Asistencia y Horario de tutorías.
- Comunicación oficial a través de correo electrónico.
- Políticas generales:
  - Respeto, Puntualidad, Responsabilidad, Disciplina, [[Honestidad Académica]].

### Parámetros de la Asignatura
- CPE: 16 horas.
- Aula virtual.
- Semestre: 6to.
- Syllabus y parámetros de evaluación.

---

## Unidad I: Fundamentos y Riesgos de Seguridad de la Información

### ¿Por qué preocuparse por la seguridad de la información?
Problemas comunes:
- Destrucción de la información y otros recursos.
- Modificación o distorsion de información.
- Robo, eliminación o pérdida de información u otros recursos.
- La revelación de información.
- La interrupción de los servicios.

### Definiciones
> **Imagen detectada:** Ilustración de una persona interactuando con una carpeta de archivos digital protegida por un icono de llave y candado.

- **Seguridad de la información:** Incluye la protección de información, sistemas, recursos y demás activos contra desastres, errores (intencionales o no) y manipulación no autorizada, para reducir la probabilidad y el impacto de los incidentes de seguridad.
- Según la norma [[ISO/IEC 27002]], es la protección de la información contra diversos tipos de amenazas para garantizar la [[continuidad del negocio]], minimizando riesgos y maximizando el retorno sobre la inversión. Se obtiene implementando controles como políticas, procesos, procedimientos, estructuras organizacionales y funciones de [[hardware]] y [[software]].

### Conceptos Relacionados
1. **Incidente de seguridad:** Evento adverso relacionado con la seguridad, por ejemplo, ataques de denegación de servicio ([[DoS]]), robo de información, fuga y acceso no autorizado.
   > **Imagen detectada:** Gráfico tipo caricatura de un atacante encapuchado corriendo con una bolsa de dinero desde una laptop con un icono de seguridad.
2. **Activo:** Cualquier elemento que tenga valor para la organización y su negocio (bases de datos, [[software]], computadores, servidores, dispositivos de red como [[router|routers]] y [[switch|switches]], personas, procesos y servicios).
   > **Diagrama detectado:** Esquema de "Activos de Información" relacionando datos, personal, redes de comunicación, ubicación física, servicios, hardware y software alrededor de un nodo central "ACTIVO".
3. **Amenaza:** Cualquier evento que explote [[vulnerabilidad|vulnerabilidades]]. Causa potencial de un incidente no deseado que puede resultar en daños.
   > **Imagen detectada:** Icono de un hacker trabajando en una laptop rodeado de símbolos flotantes de malware, virus y fallas de seguridad.
4. **Vulnerabilidad:** Debilidad que puede ser explotada y pone en peligro la seguridad de los sistemas y datos (fragilidad de un activo o configuraciones incorrectas).
5. **Riesgo:** Combinación de la probabilidad de que una amenaza se materialice y sus consecuencias para la organización.

---

## Diferencias: Seguridad de la Información vs Seguridad Informática vs [[Ciberseguridad]]

| Enfoque | Enfoque Principal | Objetivo | Ejemplo |
| :--- | :--- | :--- | :--- |
| **Seguridad de la información** | Protege toda la información (activos), sin importar el formato. | Garantizar [[Confidencialidad, Integridad y Disponibilidad|CID]] (Confidencialidad, Integridad y Disponibilidad). | Proteger documentos impresos, bases de datos, grabaciones, correos. |
| **Seguridad informática** | Se centra en proteger los sistemas informáticos (hardware, software, redes internas). | Evitar accesos no autorizados, fallos técnicos o pérdida de datos. | [[Antivirus]], [[firewall|firewalls]], control de acceso a servidores. |
| **[[Ciberseguridad]]** | Protege sistemas y datos conectados a Internet. | Defender contra amenazas externas como hackers, [[malware]], [[phishing]]. | Seguridad en redes sociales, banca en línea, comercio electrónico. |

> **Diagrama detectado:** Diagrama de Venn que muestra tres conjuntos: un óvalo grande azul que abarca todo representando la *Seguridad de la Información*, dentro del cual se intersectan un círculo gris (Seguridad Informática) y un círculo cian (Ciberseguridad).

---

## Pilares de la Seguridad de la Información (CID)

> **Diagrama detectado:** Pirámide triangular verde y azul que muestra los pilares de la seguridad de la información con "Integridad" en la cúspide, y "Confidencialidad" y "Disponibilidad" en la base.

1. **Confidencialidad:** La información solo debe ser accesible o divulgada a aquellos autorizados. Protege los datos transmitidos contra ataques pasivos mediante el [[control de acceso]] y la [[encriptación]] (Ej: mensajes de [[WhatsApp]] sin cifrar).
2. **Integridad:** La información debe permanecer correcta (integridad de datos) y como el emisor la originó (integridad de fuente) sin manipulaciones. Es la garantía contra ataques activos (Ej: transacción bancaria alterada).
3. **Disponibilidad:** La información debe estar siempre accesible para aquellos autorizados (Ej: página de matrícula caída).

---

## Servicios de la Seguridad de la Información
- **No repudio (Irrenunciabilidad):** Impide que una fuente o destino niegue la transmisión o recepción de mensajes. Se divide en *no repudio en origen* y *no repudio en destino*. La [[firma digital]] es una prueba efectiva.
- **Autenticidad:** Garantiza que el origen y el destino puedan verificar la identidad de la otra parte, evitando impostores.
- **Conformidad:** Cumplir y hacer cumplir regulaciones internas y externas (leyes y reglamentos).
- **Control de acceso:** Limitar y controlar el acceso lógico o físico mediante identificación, autenticación y autorización.

---

## Ataques a la Información
Un ataque es un acto deliberado de tratar de esquivar los controles de seguridad para explotar vulnerabilidades. Uno de los pasos más importantes para mitigarlos es la **educación**.

### Modelos de Ataques
1. **Interrupción:** Destrucción o indisponibilidad de un activo (ataque contra la disponibilidad, ej: destrucción de un disco duro).
2. **Interceptación:** Acceso a un activo por un tercero no autorizado (ataque contra la confidencialidad, ej: copia no autorizada de archivos).
3. **Modificación:** Acceso y alteración de un activo (ataque contra la integridad, ej: cambio de valores en un archivo).
4. **Fabricación:** Inserción de objetos falsificados en un activo (ataque contra la autenticidad, ej: adición de registros falsos).

### Formas de Ataques
- **Ataques pasivos:** Basados en escuchar y monitorear transmisiones (difíciles de detectar, prevenibles con [[criptografía]]).
- **Ataques activos:** Involucran modificación de datos, creación de objetos falsos o [[DoS]] (difíciles de prevenir totalmente, pero detectables y recuperables).

---

## Normativa Ecuatoriana y Referencias
- [[EGSI]] (Esquema Gubernamental de Seguridad de la Información): Ciclo PHVA (Planificar, Hacer, Verificar, Actuar).

---

## Amenazas y Vulnerabilidades (Clase #3)

- **Amenaza:** Potencial causa de un incidente no deseado (hacker, incendio, malware).
- **Vulnerabilidad:** Debilidad que puede ser explotada (contraseñas débiles, mala configuración).
- **Ataque:** Cuando la amenaza explota una vulnerabilidad.
- **Riesgo:** Probabilidad de que una amenaza explote una vulnerabilidad y cause un impacto.
- **Impacto:** Consecuencias que afectan la confidencialidad, integridad o disponibilidad.

### Tipos de Amenazas
- **Naturales:** Terremotos, inundaciones, incendios.
- **Accidentales:** Errores humanos, borrado involuntario.
- **Intencionales:** Malware, ransomware, phishing.
- **Organizacionales:** Procesos internos deficientes.

### Tipos de Amenazas Específicas
- **[[DoS]] (Denegación de Servicio):** Sobrecargar redes y servidores con tráfico para inhabilitar solicitudes legítimas.
- **[[DDoS]] (Denegación de Servicio Distribuido):** DoS proveniente de múltiples fuentes distribuidas (Botnets).
- **[[Man-in-the-Middle (MitM)|Hombre en el medio (Man-in-the-middle)]]:** Interceptación de comunicación entre dos partes para robar datos de forma invisible.
- **[[Malware]]:** Software malicioso (Virus, Gusano, Troyano, [[Ransomware]], [[Spyware]], [[Adware]], [[Keylogger]], [[Puerta trasera (Backdoor)|Backdoor]]).
- **[[Phishing]]:** Engaños mediante correos o sitios falsos para robar credenciales.

### Tipos de Vulnerabilidades
- **Técnicas:** Software sin parches, configuraciones inseguras, protocolos obsoletos ([[Telnet]], [[FTP]]), aplicaciones mal diseñadas ([[SQL Injection]], [[XSS]]), cifrado débil ([[MD5]], [[DES]]).
- **Humanas:** Contraseñas débiles, ingeniería social, falta de capacitación, uso de USBs infectadas.
- **Físicas:** Acceso no autorizado a salas de servidores, falta de protección contra incendios, equipos robados.
- **Organizacionales:** Falta de respaldos, monitoreo deficiente, gestión de accesos desactualizada (empleados dados de baja con credenciales activas).

---

## Gestión de Riesgos de la Seguridad de la Información (Clase #4)

- **Riesgo inherente:** Riesgo propio de la actividad sin la aplicación de controles.
- **Riesgo residual:** Riesgo remanente tras el tratamiento.

### Proceso de Gestión de Riesgo (ISO 27005 / Metodología)
1. **Establecimiento del contexto:** Consideraciones generales, criterios básicos, alcance, límites y estructura organizacional del [[SGRSI]].
2. **Valoración del riesgo:** Identificación de activos (primarios y de soporte), amenazas, vulnerabilidades, controles existentes, valoración de consecuencias (Confidencialidad, Integridad, Disponibilidad) y estimación del nivel de riesgo.
3. **Tratamiento del riesgo:** Selección de controles.
4. **Aceptación del riesgo.**
5. **Comunicación del riesgo.**
6. **Monitoreo y revisión del riesgo.**

---

## Tratamiento y Controles de Riesgos (Clase #5)

### Opciones de Tratamiento del Riesgo
1. **Reducción (Mitigar):** Aplicar controles para disminuir la probabilidad o impacto y llevar el riesgo a un nivel residual aceptable.
2. **Evitación:** Eliminar la actividad que genera el riesgo si este es demasiado alto y no rentable de mitigar.
3. **Transferencia:** Pasar el riesgo a un tercero (ej: mediante seguros o contratos de externalización).
4. **Aceptación:** Asumir el riesgo de manera consciente si está dentro del umbral de tolerancia.

---

## Metodologías, Políticas y Estándares (Clase #7 - #13)

- **Estándar:** Reglas formales y documentadas (ej: establecer un SGSI).
- **Buena Práctica:** Técnica o método probado (ej: backups diarios).

### La Familia [[ISO/IEC 27000]]
- **[[ISO/IEC 27001]]:** Norma principal con los requisitos obligatorios para implementar, mantener y mejorar un [[SGSI]] (Sistema de Gestión de Seguridad de la Información). Es **certificable**. Utiliza el ciclo [[PHVA]] (Plan-Do-Check-Act).
- **[[ISO/IEC 27002]]:** Código de prácticas que ofrece un catálogo de controles de seguridad recomendados. Es una guía de **cómo** aplicar los controles. **No es certificable**.
- **[[ISO/IEC 27003]]:** Guía de implementación del SGSI.
- **[[ISO/IEC 27004]]:** Métricas y medición de la eficacia del SGSI.
- **[[ISO/IEC 27005]]:** Directrices para la gestión del riesgo de seguridad de la información.
- **[[ISO/IEC 27032]]:** Guías relativas a la [[ciberseguridad]].

### NIST Cybersecurity Framework ([[NIST CSF]])
Marco desarrollado por el [[NIST]] organizado en 5 funciones principales:
1. **Identify (Identificar):** Reconocer activos, riesgos y vulnerabilidades.
2. **Protect (Proteger):** Implementar salvaguardas y controles de acceso.
3. **Detect (Detectar):** Monitoreo continuo y detección de incidentes.
4. **Respond (Responder):** Acciones para contener incidentes.
5. **Recover (Recuperar):** Restaurar servicios y resiliencia.
*Es flexible y no requiere certificación.*

---

## Políticas de Seguridad de la Información (Clase #8 - #10)

Conjunto de lineamientos basados en normas y procedimientos que determinan las reglas para garantizar la seguridad de la información.
- **Estructura jerárquica:** Leyes -> Políticas (Estratégico) -> Normas / Qué (Táctico) -> Procedimientos / Cómo -> Instrucciones (Operacional) -> Registros / Evidencias.
- **Características:** Estructuradas, claras, aprobadas por la alta dirección, de aplicación obligatoria para todo el personal y proveedores.
- **Elementos clave:** Propósito, alcance, objetivos, definiciones, principios ([[CID]], [[LOPDP]]), roles y responsabilidades, clasificación de la información, control de accesos, gestión de incidentes, cumplimiento y sanciones, formación, revisión y mejora continua.

---

## Sistema de Gestión de Seguridad de la Información (SGSI) - Ciclo PHVA (Clase #11 - #13)

> **Diagrama detectado:** Esquema circular del ciclo PDCA (Planificar, Hacer, Verificar, Actuar) rodeado por las interacciones con las "Partes Interesadas" y los requisitos/expectativas de seguridad de la información.

- **Planificar (Plan):** Establecer el SGSI, políticas, objetivos, análisis de riesgos y declaración de aplicabilidad (SOA).
- **Hacer (Do):** Implementar y operar los controles, políticas y planes de tratamiento de riesgos.
- **Verificar (Check):** Monitorear, medir procesos, realizar auditorías internas y revisión por la dirección.
- **Actuar (Act):** Tomar acciones correctivas y preventivas para la mejora continua del SGSI.

---

## Marco Legal para la Protección de Datos: LOPDP Ecuador (Clase #14 - #16)

- **Definición ([[LOPDP]]):** Ley Orgánica de Protección de Datos Personales de Ecuador, que garantiza el derecho fundamental de las personas a controlar su información personal.
- **Derechos de los titulares:** Derecho a la información, acceso, rectificación y actualización, eliminación, oposición, portabilidad, suspensión del tratamiento, a no ser objeto de decisiones automatizadas, consulta y educación digital.
- **Categorías especiales (Art. 25-32):** Datos sensibles, de niños y adolescentes, de salud, y de personas con discapacidad (su tratamiento está prohibido salvo excepciones específicas como consentimiento explícito).
- **Responsable del tratamiento:** Persona natural o jurídica que decide sobre la finalidad y el tratamiento de los datos.
- **Obligaciones del responsable:** Cumplir principios de licitud, lealtad y transparencia, informar al titular, garantizar derechos, obtener consentimiento, implementar medidas de seguridad, registrar incidentes, celebrar contratos con encargados, designar un [[Delegado de Protección de Datos (DPO)|Delegado de Protección de Datos (DPO)]] cuando aplique, y limitar el tiempo de conservación.