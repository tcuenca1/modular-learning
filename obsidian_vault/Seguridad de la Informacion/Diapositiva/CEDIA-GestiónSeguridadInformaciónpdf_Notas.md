---
materia: Seguridad de la Informacion
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [seguridad_de_la_informacion, diapositiva, ingesta_ia]
---

[[Seguridad de la Informacion]]

# Gestión de la Seguridad de la Información

## Créditos
* **Versión original:** Flávia Estélia Silva Coelho, Luiz Geraldo Segadas de Araújo, Edson Kowask Bezerra
* **Versión adaptada al Ecuador:** A partir de la versión de ESR [[RENATA]] - Colombia.
* **Instituciones participantes:** Red Nacional de Tecnología Avanzada ([[RENATA]]), Universidad Nacional de Colombia, Escola Superior de Redes - RNP Brasil, Red CEDIA.

---

## Tabla de Contenido
1. [[Fundamentos de la Seguridad de la Información]]
2. [[Código de práctica]]
3. [[Sistema de gestión de seguridad de la información]] ([[SGSI]])
4. [[Política de seguridad de la información]]
5. [[La gestión del riesgo]]
6. [[Gestión de operaciones y comunicaciones]]
7. [[Seguridad de acceso y del entorno]]
8. [[Seguridad organizacional]]
9. [[Gestión de la continuidad del negocio]]
10. [[Conformidad]]
11. [[Cuaderno de actividades]]
12. [[Anexo]]

---

## Capítulo 1: Fundamentos de la Seguridad de la Información

### 1.1 Tendencias en el área de la "gestión de seguridad de información"
* Evolución desde la norma **ISO-17799** (año 2000) hasta la familia [[ISO 27000]] (desde 2005).
* **ISO/IEC 27001:2005**: Orientada a establecer, implementar, operar, monitorear, analizar, mantener y mejorar un [[SGSI]] (Sistema de Gestión de Seguridad de la Información), alineada con [[ISO 9001]].
* Actualización de octubre de **2013**:
  * **[[ISO 27001:2013]]**: Cuenta con 114 controles en 14 categorías o dominios (en contraste con los 133 controles y 11 categorías de la edición 2005). Requerimientos de análisis de riesgos alineados con **ISO 31000**.
  * **[[ISO 27002:2013]]**: Código de práctica alineado en número de controles y terminología con [[ISO/IEC 27001]].

### 1.2 ¿Por qué preocuparse por la seguridad?
Problemas comunes:
* Destrucción de la información y otros recursos.
* Modificación o distorsión de información.
* Robo, eliminación o pérdida de información u otros recursos.
* Revelación de información.
* Interrupción de los servicios.

### 1.3 Definiciones
* **[[Seguridad de la Información]]**: Protección de información, sistemas, recursos y demás activos contra desastres, errores y manipulación no autorizada para garantizar la [[continuidad del negocio]], minimizando riesgos y maximizando el retorno sobre la inversión ([[ROI]]) (según [[ISO/IEC 27002]]).
* **Incidente de seguridad**: Evento adverso relacionado con la seguridad (ej. [[Denial of Service|DoS]], robo de información, acceso no autorizado).
* **Activo**: Cualquier elemento que tenga valor para la organización (bases de datos, software, equipos, servidores, [[dispositivos de red]], personas, procesos, servicios).
* **Amenaza**: Cualquier evento que explote vulnerabilidades y cause daños potenciales a un sistema u organización.
* **Vulnerabilidad**: Debilidad o fragilidad de un activo que puede ser explotada por una o más amenazas.
* **Riesgo**: Combinación de la probabilidad de que ocurra un evento y sus consecuencias (impacto) sobre los objetivos de la organización.
* **Ataque**: Acción que compromete la seguridad de una organización.
* **Impacto**: Resultado evaluado de un evento en particular.

### 1.4 Modelos de ataque
Hay cuatro modelos posibles:
1. **Interrupción**: Ataque contra la **disponibilidad** (ej. destrucción de un disco duro).
2. **Interceptación**: Ataque contra la **confidencialidad** (ej. copia no autorizada de archivos).
3. **Modificación**: Ataque contra la **integridad** (ej. alteración de valores en un archivo de datos).
4. **Fabricación**: Ataque contra la **autenticidad** (ej. inserción de registros falsos).

> **Diagrama detectado:** Figura 1 - Modelos de ataque. Muestra esquemas de flujo de información desde una "Fuente de la Información" hasta un "Destino de la Información", ilustrando el flujo normal (a), interrupción cortando la flecha (b), intercepción derivando el flujo hacia abajo (c), modificación alterando el canal (d), y fabricación inyectando datos desde el exterior hacia el canal (e).

### 1.5 Formas de ataque
* **Ataques pasivos:** Basados en escuchar y monitorear transmisiones para obtener información (ej. escuchar una conversación telefónica). Difíciles de detectar, pero prevenibles con [[Criptografía]].
* **Ataques activos:** Involucran modificación de datos, creación de objetos falsos o [[Denial of Service|negación de servicio]]. Difíciles de prevenir por completo, pero detectables para aplicar medidas de recuperación.

### 1.6 Arquitectura de seguridad
Propuesta por el modelo [[OSI]] (Open Systems Interconnection) definido en la norma **ISO 7498-2**:
* Proteger datos contra modificaciones no autorizadas.
* Proteger datos contra pérdida / robo / hurto.
* Proteger datos contra divulgación no autorizada.
* Asegurar la identidad del remitente correcto.
* Asegurar la identidad del destinatario correcto.

### 1.7 Servicios de seguridad
Medidas preventivas (principios básicos):
* **Confidencialidad:** Protección de datos transmitidos contra ataques pasivos (control de acceso y encriptación).
* **Autenticidad:** Garantizar que el origen y destino verifiquen la identidad mutua.
* **Integridad:** Garantía contra ataques activos mediante cambios o remociones no autorizadas.
* **No repudio:** Impide que una fuente o destino niegue la transmisión de mensajes.
* **Conformidad:** Deber de cumplir regulaciones internas y externas.
* **Control de acceso:** Limitar y controlar el acceso lógico/físico mediante identificación, autenticación y autorización.
* **Disponibilidad:** Garantizar que los recursos estén disponibles para entidades autorizadas cuando lo soliciten (protección contra interrupciones o fallas de servidores).

### 1.8 Seguridad de la Información: Visión General
> **Diagrama detectado:** Figura 2 - Visión general de la seguridad de la información. Un diagrama de flujo que conecta "Los cambios tecnológicos" y la "Legislación" con el "Análisis de riesgos", alimentando las normas "ISO 27001/27002", la "Política de seguridad", las "Normas" y los "Procedimientos".

### 1.9 Preparando a la organización
Preguntas clave a responder:
* ¿Qué hay que proteger? (Activos)
* ¿Contra qué o quién? (Amenazas)
* ¿Cuál es la importancia de cada recurso para el **proceso de negocio**?
* ¿Cuál es el grado de protección deseado y los recursos financieros/humanos disponibles?

### 1.10 Requisitos de seguridad
Tres fuentes principales:
1. **Evaluación/análisis de riesgos:** Considera objetivos de negocio, amenazas, vulnerabilidades y probabilidad de ocurrencia.
2. **Legislación vigente:** Estatutos, reglamentos y cláusulas contractuales.
3. **Conjunto de principios:** Objetivos y requisitos de negocio para el procesamiento de datos.

### 1.11 Análisis/evaluación de riesgos
* Los gastos en controles deben equilibrarse frente al impacto de posibles fallas.
* Se debe realizar periódicamente (alineado con **ISO 31000** e **ISO/IEC 27005:2008**).

### 1.12 Selección de controles
* **Control (Contramedida):** Cualquier mecanismo útil para gestionar riesgos (políticas, procedimientos, directrices, prácticas, estructuras organizativas de carácter administrativo, técnico, de gestión o legal).
* Ejemplos: barreras físicas, tarjetas de visitantes, contraseñas, [[biometría]], políticas de seguridad, [[antivirus]], [[backup]], [[control de acceso lógico]].

### 1.13 Los controles de seguridad de la información
* **Controles legales fundamentales:** Protección de datos personales (privacidad), protección de registros de la organización, derechos de propiedad intelectual.
* **Buenas prácticas:** Documento de política de seguridad, asignación de responsabilidades, sensibilización y capacitación, procesamiento correcto en aplicaciones, gestión de vulnerabilidades técnicas, gestión de continuidad del negocio, gestión de incidentes.

### 1.14 Elementos relevantes para la seguridad de la información
Tratados en detalle en [[ISO/IEC 27002:2007]]:
* Política de seguridad de la información.
* Seguridad organizacional.
* Gestión de activos.
* Seguridad de recursos humanos.
* Seguridad física y del ambiente.
* Gestión de operaciones y comunicaciones.
* Control de acceso.
* Gestión de incidentes de seguridad de la información.
* Gestión de la continuidad del negocio.

---

## Capítulo 2: Código de práctica

### 2.1 Estructura de la norma
* La norma **NTC-ISO/IEC 27002:2007** sirve como guía práctica para procedimientos y controles.
* Organizada en capítulos de 0 a 15:
  * Capítulos 0-4: Introducción, objetivo, términos, estructura y análisis/tratamiento de riesgos.
  * Capítulos 5-15 (Secciones): 11 secciones específicas con 39 categorías principales de seguridad y 133 controles en total.

> **Diagrama detectado:** Figura 3 - Secuencia estructural de la norma. Un diagrama radial que conecta la norma "NTC ISO/IEC 27002:2007" en el centro con las 11 secciones de controles (desde "5. Política de Seguridad" hasta "15. Conformidad") y las secciones introductorias (0 a 4).

### Secciones principales de la norma (Resumen de controles):
* **Sección 4:** Análisis/evaluación y tratamiento de los riesgos.
* **Sección 5:** Política de seguridad (Control 5.1.1 Documento de política, 5.1.2 Análisis crítico).
* **Sección 6:** Organizando la seguridad de la información (Infraestructura 6.1 y Partes externas 6.2).
* **Sección 7:** Gestión de activos (Responsabilidad de activos 7.1 y Clasificación de información 7.2).
* **Sección 8:** Seguridad de recursos humanos (Antes, durante y finalización de la contratación).
* **Sección 9:** Seguridad física y del entorno (Áreas seguras 9.1 y Seguridad de equipos 9.2).
* **Sección 10:** Gestión de operaciones y comunicaciones (Incluye procedimientos operacionales, gestión de servicios externalizados, protección contra [[malware]], **copias de seguridad / backup**, seguridad de red, manipulación de medios, intercambio de información, comercio electrónico y monitoreo con [[Logs]]).
* **Sección 11:** Control de acceso (Requisitos de negocio 11.1, Gestión de accesos de usuarios 11.2, Responsabilidades de usuarios 11.3, Control de acceso a redes 11.4, Sistemas operativos 11.5, Aplicaciones 11.6, Computación móvil y trabajo remoto 11.7).
* **Sección 12:** Adquisición, desarrollo y mantenimiento de sistemas de información (Requisitos de seguridad, procesamiento correcto, **controles criptográficos**, seguridad en desarrollo).
* **Sección 13:** Gestión de incidentes de seguridad de la información (Reportes de eventos y debilidades, respuesta y recolección de evidencias).
* **Sección 14:** Gestión de la continuidad del negocio (Inclusión de seguridad en la continuidad, análisis de riesgos, planes de continuidad y pruebas).
* **Sección 15:** Conformidad (Cumplimiento de requisitos legales, propiedad intelectual, protección de datos personales, criptografía, auditoría de sistemas de información).

---

## Capítulo 3: Sistema de gestión de seguridad de la información (SGSI)

### 3.1 Visión general y alcance
* El [[SGSI]] integra la estrategia de la organización con sus necesidades, objetivos, requisitos de seguridad y procesos. Basado en **ISO/IEC 27001:2005**.

### 3.2 Modelo PHVA ([[Ciclo PHVA]])
La norma adopta el ciclo **Planear, Hacer, Verificar, Actuar**:
1. **Planear (Establecer el SGSI):** Establecer políticas, objetivos, procesos y procedimientos de gestión del riesgo.
2. **Hacer (Implementar y operar el SGSI):** Implementar y operar políticas, controles y procesos.
3. **Verificar (Monitorear y analizar críticamente):** Evaluar y medir el desempeño frente a la política y objetivos.
4. **Actuar (Mantener y mejorar):** Tomar acciones correctivas y preventivas basadas en auditorías y revisiones por la dirección.

> **Diagrama detectado:** Figura 25 - Modelo PHVA. Muestra las cuatro fases circulares (Planear - Establecer el SGSI, Hacer - Implementar y operar el SGSI, Verificar - Hacer seguimiento y revisar el SGSI, Actuar - Mantener y mejorar el SGSI) interactuando con las "Partes Interesadas", "Expectativas y requisitos de seguridad de la información" y la "Seguridad de Información gestionada".

### 3.5 Requisitos generales de la documentación y [[Declaración de Aplicabilidad]]
* **Declaración de Aplicabilidad (SoA):** Documento formal que lista los controles aplicados y su justificación, controles no aplicados y sus justificaciones, y controles no aplicables al entorno de la organización.
* Documentación obligatoria requerida para auditoría: Política y objetivos del SGSI, alcance, procedimientos y controles, metodología de evaluación de riesgos, informe de riesgos, plan de tratamiento de riesgos, procedimientos operacionales, registros requeridos.

---

## Capítulo 4: Política de seguridad de la información

### 4.1 Definición y Alcance
* Conjunto de lineamientos, normas y procedimientos que determinan las reglas a seguir para garantizar la seguridad de la información conforme a los requisitos legales y de negocio. Representa un documento formal con valor jurídico.
* Debe cubrir la definición, objetivos, alcance, compromiso de los líderes, objetivos de control, responsabilidades y referencias a documentos de respaldo (políticas específicas de contraseñas, backups, etc.).

### 4.2 Diagrama y Arquitectura
> **Diagrama detectado:** Figura 26 - Secuencia y relación de las políticas de seguridad con las etapas de planeación. Una pirámide jerárquica que va desde las "Políticas (Directrices - Por qué)" en la cúspide (nivel estratégico), pasando por "Normas (Qué)", "Procedimientos (Cómo)", "Instrucciones (Detalles)" (nivel táctico/operacional), hasta los "Registros" y "Evidencias" en la base.

---

## Capítulo 5: La gestión del riesgo

### 5.1 Definiciones y Proceso
* **Análisis de riesgos:** Identifica y estima los riesgos (amenazas, vulnerabilidades, impactos).
* **Evaluación de riesgos:** Compara el riesgo estimado con criterios predefinidos para determinar su importancia.
* **Tratamiento del riesgo:** Selección y aplicación de medidas para modificar el riesgo (reducir, retener, evitar, transferir).
* **Cálculo del riesgo:** $\text{Riesgo} = \text{Impacto} \times \text{Probabilidad}$.
* **Evaluación cualitativa:** Usa calificadores descriptivos (Alto, Medio, Bajo).
* **Evaluación cuantitativa:** Usa valores numéricos financieros (ej. probabilidad en porcentaje, impacto monetario).

---

## Capítulo 6: Gestión de operaciones y comunicaciones

* **Procedimientos operacionales:** Documentación y control de cambios en sistemas operativos y aplicaciones.
* **Protección contra [[malware]]:** Uso de [[antivirus]], control de licencias, prohibición de software no autorizado.
* **Copias de seguridad ([[Backup]]):** Generación regular y probada de respaldos para garantizar integridad y disponibilidad.
* **Manipulación de medios y documentos:** Clasificación, control de acceso, desecho seguro (trituración/incineración) y transporte seguro.
* **Gestión de seguridad de red:** Separación de responsabilidades de red, uso de [[firewalls]], cifrado y control de acceso remoto.
* **Monitoreo:** Uso de [[Logs]] de operaciones, fallas y auditoría debidamente protegidos.

---

## Capítulo 7: Seguridad de acceso y del entorno

* **Política de control de acceso:** Definida según la clasificación de información y requisitos de negocio.
* **Control de acceso lógico:** Funciones de identificación (ej. [[login]]), autenticación (contraseñas, [[biometría]], [[Smart Cards]], tokens), atribuciones ([[ACL]]) y monitoreo.
* **Controles de acceso físico:** Controles administrativos (identificación visible, manejo de visitantes) y controles explícitos (cerraduras, cámaras de video, guardias).
* **Controles ambientales:** Protección contra incendios (extintores, detectores de humo), fallas eléctricas ([[UPS]], generadores), amenazas de agua y control de temperatura/ventilación.
* **Seguridad de recursos humanos:** Selección estricta (antecedentes, referencias), acuerdos de confidencialidad y procedimientos de desvinculación (devolución de activos y revocación de accesos).

---

## Capítulo 8: Seguridad organizacional

* **Infraestructura organizacional:** Asignación formal de responsabilidades (ej. Gestor de Seguridad de la Información) y creación de comités multidisciplinarios de coordinación.
* **Tratamiento de activos:** Inventario de activos ([[hardware]], software, datos, personas) y asignación de propietarios responsables de su seguridad.
* **Seguridad de la información de terceros:** Tratamiento diferenciado para proveedores y clientes, establecimiento de acuerdos de nivel de servicio ([[SLA]]) y acuerdos de confidencialidad ([[NDA]]).

---

## Capítulo 9: Gestión de la continuidad del negocio

* **[[Continuidad del negocio]] y Recuperación de desastres:** Combinación de prevención y recuperación para evitar la indisponibilidad de procesos críticos.
* **Plan de Continuidad del Negocio (PCN / BCP):** Estructura que incluye responsabilidades, activación del plan, procedimientos de emergencia, recuperación y pruebas periódicas (integrales, parciales o simuladas).
* **Gestión de incidentes de seguridad:** Notificación de eventos adversos, análisis de causas, planes de contingencia y recolección de evidencias conforme a la legislación (ej. normativa de entidades de control financiero o ciberseguridad como [[ColCERT]]).

---

## Capítulo 10: Conformidad

### 10.1 Legislación y Derecho Informático en Colombia
* Importancia de cumplir con las leyes nacionales e internacionales para evitar sanciones civiles, penales o administrativas.
* **Marco normativo clave en Colombia:**
  * **Derechos de Autor:** [[Ley 23 de 1982]], [[Ley 44 de 1993]].
  * **Comercio Electrónico y Firmas Digitales:** [[Ley 527 de 1999]].
  * **Protección de Datos Personales ([[Habeas Data]]):** [[Ley 1266 de 2008]], [[Ley 1581 de 2012]], [[Decreto 1377 de 2013]].
  * **Delitos Informáticos:** [[Ley 1273 de 2009]] (modifica el Código Penal tipificando accesos abusivos, interceptación de datos, daños informáticos, uso de software malicioso, violación de datos personales y suplantación de sitios web).
  * **Tecnologías de la Información y las Comunicaciones (TIC):** [[Ley 1341 de 2009]].
  * **Acceso a la Información Pública:** [[Ley 1712 de 2014]] (Ley de transparencia).

### 10.19 Auditoría de sistemas de información
* Protección de herramientas de auditoría (acceso controlado y almacenamiento aislado).
* Realización basada en acuerdos formales con la dirección, limitándose a modo de lectura cuando sea necesario, asegurando la confidencialidad y documentación completa del proceso.

### 10.21 Otras normas y marcos de referencia
* **[[COBIT]]** (Control Objectives for Information Technologies): Marco de gobierno de TI para optimizar inversiones y maximizar el [[ROI]].
* **[[ITIL]]** (Information Technology Infrastructure Library): Librería de buenas prácticas para la gestión de servicios de TI (incluye [[SLA]] y [[OLA]]).