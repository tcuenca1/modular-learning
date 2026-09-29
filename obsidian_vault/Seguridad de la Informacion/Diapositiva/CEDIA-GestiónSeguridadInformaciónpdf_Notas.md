---
materia: Seguridad de la Informacion
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [seguridad_de_la_informacion, diapositiva, ingesta_ia]
---

# [[Seguridad de la Informacion]]: Gestión de la Seguridad de la Información

## Prólogo a la versión en castellano
La **Red Nacional Académica de Tecnología Avanzada, [[RENATA]]**, presenta la Escuela Superior de Redes ([[ESR]]) RENATA Colombia, en colaboración con la Rede Nacional de Ensino e Pesquisa ([[RNP]]) Brasil e Instituciones de Educación Superior en Colombia, dentro de su estrategia STAR (Servicios de Tecnología Avanzada RENATA). 

Su objetivo es la formación de alto nivel en competencias [[TIC]] para personal técnico, administrativo y académico en Colombia.

---

## 1. Fundamentos de la Seguridad de la Información

### 1.1 Tendencias en el área de la "gestión de seguridad de información"
La gestión evolucionó desde la norma **ISO-17799** del año 2000 hasta la familia [[ISO 27000]]. 
* **[[ISO 27001]]:2005:** Orientada a establecer, implementar, operar, monitorear, analizar, mantener y mejorar un [[SGSI]] (Sistema de Gestión de Seguridad de la Información), alineada con [[ISO 9001]].
* **Actualización Octubre 2013:** Se actualizaron [[ISO 27001:2013]] (requisitos) e [[ISO 27002:2013]] (Código de Práctica). La versión 2013 cuenta con **114 controles en 14 categorías o dominios**, alineados con [[ISO 31000]] para la gestión del riesgo.

---

### 1.2 ¿Por qué preocuparse por la seguridad?
Problemas comunes:
* Destrucción de la información y otros recursos.
* Modificación o distorsión de información.
* Robo, eliminación o pérdida de información u otros recursos.
* Revelación de información.
* Interrupción de los servicios.

La seguridad de la información protege los datos (impresos, electrónicos, hablados) frente a amenazas para garantizar la **continuidad del negocio**, minimizar riesgos y maximizar el retorno sobre la inversión ([[ROI]]).

---

### 1.3 Definiciones
* **[[Incidente de seguridad]]:** Evento adverso relacionado con la seguridad (ej. ataques de [[Denial of Service|DoS]], robo de información, fuga, acceso no autorizado).
* **Activo:** Cualquier elemento con valor para la organización (bases de datos, software, equipos, servidores, [[Dispositivos de red]], personas, procesos, servicios).
* **Amenaza:** Cualquier evento que explote vulnerabilidades y pueda resultar en daños a un sistema u organización.
* **Vulnerabilidad:** Debilidad o fragilidad de un activo que puede ser explotada por una o más amenazas.
* **Riesgo:** Combinación de la probabilidad de que ocurra un evento y sus consecuencias (impactos) para la organización.
* **Ataque:** Acción que compromete la seguridad de una organización.
* **Impacto:** Resultado evaluado de un evento en particular.

---

### 1.4 Modelos de ataque
Hay cuatro modelos posibles:
1. **Interrupción:** Un activo se destruye o queda indisponible (Ataque contra la **disponibilidad**).
2. **Interceptación:** Un tercero no autorizado accede a un activo (Ataque contra la **confidencialidad**).
3. **Modificación:** Un tercero no autorizado accede y modifica un activo (Ataque contra la **integridad**).
4. **Fabricación:** Una parte no autorizada inserta objetos falsificados (Ataque contra la **autenticidad**).

> **Diagrama detectado:** Figura 1 - Modelos de ataque. Muestra esquemas de flujo normal de información de fuente a destino (a), seguido de flechas divergentes o interrumpidas que ilustran interrupción (b), intercepción (c), modificación (d) y fabricación (e).

---

### 1.5 Formas de ataque
* **Ataques pasivos:** Basados en escuchar y monitorear transmisiones sin alterarlas (difíciles de detectar, prevenibles mediante [[Criptografia]]).
* **Ataques activos:** Involucran modificación de datos, objetos falsos o negación de servicio (difíciles de prevenir totalmente, pero detectables para aplicar recuperación).

---

### 1.6 Arquitectura de seguridad
Según el modelo [[OSI]] (Open Systems Interconnection) y la norma **ISO 7498-2**, los objetivos y requisitos de seguridad son:
* Proteger los datos contra modificaciones no autorizadas.
* Proteger los datos contra pérdida / robo / hurto.
* Proteger los datos contra divulgación no autorizada.
* Asegurar la identidad del remitente correcto.
* Asegurar la identidad del destinatario correcto.

---

### 1.7 Servicios de seguridad
Medidas preventivas (principios básicos) frente a amenazas:
* **Confidencialidad:** Protección contra accesos no autorizados mediante [[Control de acceso]] y [[Criptografia]].
* **Autenticidad:** Garantiza que el origen y destino verifiquen la identidad mutua.
* **Integridad:** Garantía contra ataques activos mediante cambios o remociones no autorizadas.
* **No repudio:** Impide a una fuente o destino negar la transmisión de mensajes.
* **Conformidad:** Cumplimiento de regulaciones internas y externas.
* **Control de acceso:** Limita y controla el acceso lógico/físico mediante identificación, autenticación y autorización.
* **Disponibilidad:** Garantiza que los recursos estén accesibles para entidades autorizadas cuando lo soliciten, protegiéndolos contra caídas de servidores o fallas.

---

### 1.8 Seguridad de la información
> **Diagrama detectado:** Figura 2 - Visión general de la seguridad de la información. Un diagrama de flujo que conecta los **Cambios tecnológicos** y el **Análisis de riesgos** con la **Legislación**, **Normas**, **ISO 27001/27002**, **Política de seguridad** y **Procedimientos**.

---

### 1.9 Preparando a la organización
Cuestiones previas clave:
* ¿Qué hay que proteger? (Activos).
* ¿Contra qué o quién? (Amenazas).
* ¿Cuál es la importancia de cada recurso dentro de los [[Procesos de negocio]]?
* ¿Cuál es el grado de protección deseado y los recursos financieros/humanos disponibles?

---

### 1.10 Requisitos de seguridad
1. **Evaluación/Análisis de riesgos:** Considera estrategias de negocio, amenazas y vulnerabilidades.
2. **Legislación vigente:** Estatutos, reglamentos y cláusulas contractuales.
3. **Conjunto de principios:** Objetivos y requisitos de negocio para el procesamiento de datos.

---

### 1.11 Análisis/evaluación de riesgos
Debe realizarse periódicamente para contemplar cambios en la organización. Compara el riesgo estimado con criterios predefinidos (norma **NTC ISO/IEC 27005:2008**).

---

### 1.12 Selección de controles
Los **controles** (o contramedidas) son medidas adoptadas para hacer frente a las vulnerabilidades y reducir los riesgos (administrativos, técnicos, de gestión o legales). 
* Ejemplos: barreras físicas, tarjetas de visitantes, contraseñas, cerraduras, **controles biométricos**, antivirus, [[Backup|copias de seguridad]].

---

### 1.13 Los controles de seguridad de la información
* **Controles legales fundamentales:** Protección de datos personales, registros de la organización, derechos de propiedad intelectual.
* **Buenas prácticas:** Política de seguridad, asignación de responsabilidades, sensibilización y capacitación, procesamiento correcto en aplicaciones, gestión de vulnerabilidades técnicas, continuidad del negocio, gestión de incidentes.

---

### 1.14 Elementos relevantes para la seguridad de la información
1. Política de seguridad de la información.
2. Seguridad organizacional.
3. Gestión de activos.
4. Seguridad de recursos humanos.
5. Seguridad física y del ambiente.
6. Gestión de operaciones y comunicaciones.
7. Control de acceso.
8. Gestión de incidentes de seguridad.
9. Gestión de la continuidad del negocio.

---

## 2. Código de práctica (ISO/IEC 27002)

### 2.1 Estructura de la norma
La norma **NTC-ISO/IEC 27002:2007** está organizada en capítulos (0 a 15). Los capítulos del 0 al 4 son introductorios; desde el capítulo 5 se denominan **secciones** (11 secciones específicas con un total de 39 categorías principales y **133 controles** estructurados en: *Control*, *Directrices para la implementación* e *Información adicional*).

> **Diagrama detectado:** Figura 3 - Secuencia estructural de la norma. Muestra un esquema radial que vincula la norma **NTC ISO/IEC 27002:2007** con las secciones introductorias (0-4) y las 11 secciones de controles de seguridad (secciones 5 a 15 dispuestas en sentido horario).

* **Sección 4:** Análisis/evaluación y tratamiento de riesgos.
* **Sección 5:** Política de seguridad (Controles 5.1.1 y 5.1.2).
* **Sección 6:** Organizando la seguridad de la información (6.1 Infraestructura de seguridad, 6.2 Partes externas).
* **Sección 7:** Gestión de activos (7.1 Responsabilidad de activos, 7.2 Clasificación de la información).
* **Sección 8:** Seguridad de los recursos humanos (8.1 Antes, 8.2 Durante, 8.3 Finalización/cambio de la contratación).
* **Sección 9:** Seguridad física y del entorno (9.1 Áreas seguras, 9.2 Seguridad de equipos).
* **Sección 10:** Gestión de operaciones y comunicaciones (10 categorías principales: procedimientos operacionales, servicios externalizados, planeación, código malicioso, backups, red, manipulación de medios, intercambio de información, comercio electrónico, monitoreo).
* **Sección 11:** Control de acceso (7 categorías: requisitos de negocio, gestión de accesos de usuarios, responsabilidades de los usuarios, acceso a red, acceso a sistema operativo, acceso a aplicaciones, computación móvil y trabajo remoto).
* **Sección 12:** Adquisición, desarrollo y mantenimiento de sistemas (6 categorías: requisitos, procesamiento correcto, criptografía, archivos de sistema, desarrollo y soporte, vulnerabilidades técnicas).
* **Sección 13:** Gestión de incidentes de seguridad (2 categorías: reportes de eventos y debilidades, gestión de incidentes y mejoras).
* **Sección 14:** Gestión de la continuidad del negocio.
* **Sección 15:** Cumplimiento (3 categorías: requisitos legales, cumplimiento de políticas/normas, auditoría de sistemas).

---

## 3. Sistema de Gestión de Seguridad de la Información ([[SGSI]])

### 3.1 Visión general y alcance
El modelo [[SGSI]] integra la estrategia de la organización basándose en necesidades, objetivos, requisitos de seguridad, procesos y estructura organizacional. Se fundamenta en el ciclo [[PHVA]] (**Planear, Hacer, Verificar, Actuar**).

> **Diagrama detectado:** Figura 25 - Modelo PHVA aplicado al SGSI. Muestra un flujo circular de 4 etapas rodeado por las partes interesadas, expectativas, requisitos de seguridad y la información gestionada.

* **Planear (Establecer el SGSI):** Políticas, objetivos, procesos y procedimientos para la gestión del riesgo.
* **Hacer (Implementar y operar el SGSI):** Ejecución de políticas, controles y procedimientos.
* **Verificar ([[Monitorear]] y analizar críticamente el SGSI):** Evaluación y medición del desempeño frente a objetivos.
* **Actuar (Mantener y mejorar el SGSI):** Acciones correctivas y preventivas basadas en auditorías internas y revisiones directivas.

---

## 4. Política de seguridad de la información
Es el documento formal de más alta jerarquía que establece directrices, límites, responsabilidades y objetivos de los controles de seguridad alineados con el negocio.

> **Diagrama detectado:** Figura 26 - Secuencia y relación de las políticas de seguridad con las etapas de planeación. Una pirámide jerárquica que va desde las *Políticas (Estratégico)*, *Normas*, *Procedimientos (Táctico)*, *Instrucciones* hasta los *Registros / Evidencias (Operacional)*.

* **Etapas para su creación:** Identificar la legislación, identificar recursos críticos, clasificar la información, analizar necesidades/riesgos, preparar propuesta, discusión abierta, aprobación, implementación y mantenimiento periódico.

---

## 5. La gestión del riesgo

### 5.1 Definiciones y cálculo
* **Análisis de riesgos:** Identifica y estima amenazas, vulnerabilidades e impactos.
* **Evaluación de riesgos:** Compara el riesgo estimado con criterios predefinidos de aceptación.
* **Tratamiento del riesgo:** Selección y aplicación de medidas para modificar el riesgo (reducir, retener, evitar o transferir).
* **Cálculo del riesgo:** $\text{Riesgo} = \text{Impacto} \times \text{Probabilidad}$ (con escalas cualitativas o cuantitativas).

---

## 6. Gestión de operaciones y comunicaciones
Garantiza el funcionamiento seguro de los recursos computacionales mediante procedimientos operacionales, protección contra [[Malware|software malicioso]] ([[Antivirus]]), gestión de [[Backup|copias de seguridad]], seguridad de redes, manejo seguro de medios magnéticos y [[Monitoreo]] continuo mediante [[Logs|registros]].

---

## 7. Seguridad de acceso y del entorno
* **Control de acceso lógico:** Identificación ([[Login]]), autenticación (contraseñas, tokens, biometría), atribuciones ([[Control de acceso basado en roles|ACLs]]) y monitoreo.
* **Control de acceso físico y ambiental:** Perímetros de seguridad, controles administrativos (identificación visible, escritorio limpio) y explícitos (cerraduras, cámaras, guardias). Protección contra incendios, fallas eléctricas y ambientales.

---

## 8. Seguridad organizacional
Estructura de gobernanza para asignar responsabilidades (ej. nombramiento de un [[Gestor de seguridad de la información]]), inventario y propiedad de activos, y el manejo seguro de la información con **terceros y clientes** mediante acuerdos específicos y cláusulas contractuales.

---

## 9. Gestión de la continuidad del negocio
Combinación de prevención y recuperación ante desastres. Requiere un **Plan de Continuidad del Negocio ([[PCN]])** y un **Plan de Contingencia** estructurados en fases: actividades preliminares, análisis de impacto, alternativas de recuperación, desarrollo del plan, entrenamiento, pruebas periódicas y actualización.

---

## 10. Conformidad
Verificación del cumplimiento de las políticas internas y de la legislación externa aplicable.
* **Derecho informático en Colombia:**
  * [[Ley 527 de 1999]]: Comercio electrónico y firmas digitales.
  * [[Ley 1273 de 2009]]: Delitos informáticos (protección de la información y de los datos).
  * [[Ley 1266 de 2008]]: Hábeas data (protección de datos personales).
  * [[Ley 1581 de 2012]]: Protección de datos personales.
  * [[Ley 1712 de 2014]]: Ley de transparencia y acceso a la información pública nacional.
* **Otras marcos de referencia:** [[COBIT]] (Gobierno de TI) e [[ITIL]] (Gestión de servicios de TI).