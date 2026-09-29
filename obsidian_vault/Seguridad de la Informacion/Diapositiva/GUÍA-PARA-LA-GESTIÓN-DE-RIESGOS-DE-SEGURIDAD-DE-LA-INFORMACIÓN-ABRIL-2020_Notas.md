---
materia: Seguridad de la Informacion
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [seguridad_de_la_informacion, diapositiva, ingesta_ia]
---

[[Seguridad de la Informacion]]

# GUÍA PARA LA GESTIÓN DE RIESGOS DE SEGURIDAD DE LA INFORMACIÓN

> **Imagen detectada (Portada):** Ilustración isométrica en tonos azules donde aparece un personaje con traje y corbata cruzado de brazos junto a un dispositivo móvil vertical que muestra campos de contraseña protegidos por asteriscos (`*****`), líneas de código, iconos de nube, un servidor cúbico y una tarjeta flotante. En la parte inferior se muestran logotipos institucionales del gobierno de turno y del Ministerio correspondiente.

---

## Contenido

1. INTRODUCCIÓN
2. CONCEPTOS BÁSICOS
3. PROCESO PARA LA GESTIÓN DEL RIESGO DE LA SEGURIDAD DE LA INFORMACIÓN
4. ESTABLECIMIENTO DEL CONTEXTO
    - Consideraciones Generales
    - Criterios Básicos
        - Criterios de identificación del riesgo
        - Criterios de evaluación del riesgo
        - Criterios de impacto
        - Criterios de la aceptación del riesgo
    - Alcance y límites
    - Organización para la gestión del riesgo de la seguridad de la información
5. VALORACIÓN DEL RIESGO DE LA SEGURIDAD DE LA INFORMACIÓN
    - Análisis del riesgo
        - Identificación del riesgo
        - Identificación de los activos
        - Identificación de amenazas
        - Identificación de vulnerabilidades
        - Identificación de existencia de controles
        - Estimación o análisis del riesgo
    - Evaluación del riesgo
        - Criterios de probabilidad de ocurrencia de amenazas
        - Criterio de la evaluación de riesgos
6. TRATAMIENTO DEL RIESGO DE LA SEGURIDAD DE LA INFORMACIÓN
    - Reducción del riesgo
    - Evitación del riesgo
    - Transferencia del riesgo
    - Retención/aceptación del riesgo
7. ACEPTACIÓN DEL RIESGO DE LA SEGURIDAD DE LA INFORMACIÓN
8. COMUNICACIÓN DE LOS RIESGOS DE LA SEGURIDAD DE LA INFORMACIÓN
9. MONITOREO Y REVISIÓN DEL RIESGO DE LA SEGURIDAD DE LA INFORMACIÓN
    - Monitoreo y revisión de los factores de riesgo
    - Monitoreo, revisión y mejora de la gestión del riesgo
10. GLOSARIO DE TÉRMINOS

---

## 1. Introducción

La revolución digital ha generado que las organizaciones a nivel mundial tomen mayor atención a la [[Información]], actor principal de este proceso de cambio. Este proceso ha permitido establecer nuevas alianzas y acortar distancias entre naciones, donde el internet cumple un papel fundamental en la comunicación.

En términos de [[Gestion de Riesgos|gestión de riesgos de seguridad de la información]], el activo a proteger es la información, tanto digital (contenida en los [[Sistemas de Informacion]]) como aquella contenida en cualquier otro medio como por ejemplo el papel. Debemos tener presente que la gestión debe ocuparse de todo el ciclo de vida de la información.

Es necesario un enfoque sistemático para la gestión del riesgo en la [[Seguridad de la Informacion]] para identificar las necesidades de la organización con respecto a los requisitos de seguridad de la información y para crear un eficaz [[SGSI|Sistema de Gestión de la Seguridad de la Información (SGSI)]].

Este enfoque debe ser adecuado para el entorno de la institución y, en particular, debería cumplir los lineamientos de toda la gestión del riesgo de la institución.

Los esfuerzos de seguridad deben abordar los riesgos de una manera eficaz y oportuna donde y cuando sean necesarios. La gestión del riesgo de la seguridad de la información debe ser una parte integral de todas las actividades de la gestión de la seguridad de la información y se deben aplicar tanto a la implementación como al funcionamiento continuo de un [[SGSI]].

La gestión del riesgo de la seguridad de la información debe ser un proceso continuo. Tal proceso debe establecer el contexto, evaluar los riesgos, tratar los riesgos utilizando un plan de tratamiento para implementar las recomendaciones y decisiones.

> *"La gestión del riesgo analiza lo que puede suceder y cuáles pueden ser las posibles consecuencias, antes de decidir lo que se debe hacer y cuando hacerlo, con el fin de reducir el riesgo hasta un nivel aceptable."*

---

## 2. Conceptos Básicos

La información es el activo principal, pero también debemos considerar: infraestructura informática, equipos auxiliares, redes de comunicaciones, instalaciones y personas.

Cuando hablamos de [[Seguridad de la Informacion]] hablamos de protegerla de riesgos que puedan afectar a una o varias de sus tres principales propiedades ([[Triada CIA]]):
- **Confidencialidad:** La información solo tiene que ser accesible o divulgada a aquellos que están autorizados.
- **Integridad:** La información debe permanecer correcta (integridad de datos) y como el emisor la originó (integridad de fuente) sin manipulaciones por terceros.
- **Disponibilidad:** La información debe estar siempre accesible para aquellos que estén autorizados.

> **Diagrama detectado (Figura No.1 PRINCIPIOS DE LA S.I.):** Un diagrama piramidal o tridimensional que entrelaza los tres conceptos clave de la seguridad de la información: **CONFIDENCIALIDAD**, **INTEGRIDAD** y **DISPONIBILIDAD** rodeando al núcleo central denominado **INFORMACIÓN**.

Para facilitar el proceso de análisis y valoración de los riesgos es importante entender algunos conceptos básicos:
- **Riesgo:** Posibilidad de que una amenaza concreta pueda explotar una [[Vulnerabilidad]] para causar una pérdida o daño en un activo de información. Suele considerarse como una combinación de la probabilidad de un evento y sus consecuencias.
- **Amenaza:** Causa potencial de un incidente no deseado, que puede resultar en un daño a un sistema, persona u organización.
- **Vulnerabilidad:** Debilidad de un activo o control que puede ser explotada por una o más amenazas.
- **Impacto:** Es la consecuencia de la materialización de una amenaza sobre un activo. El costo para la institución de un incidente de la escala que sea, que puede o no ser medido en términos estrictamente financieros (ejem.: pérdida de reputación, implicaciones legales, entre otros).
- **Riesgo inherente:** Es el riesgo existente y propio de cada actividad, sin la ejecución de ningún control.
- **Riesgo residual:** El riesgo que permanece tras el tratamiento del riesgo.

---

## 3. Proceso para la Gestión del Riesgo de la Seguridad de la Información

El proceso de gestión del riesgo de la seguridad de la información puede ser iterativo para las actividades de valoración del riesgo y/o de tratamiento del riesgo. Un enfoque iterativo para realizar la valoración del riesgo puede incrementar la profundidad y el detalle de la valoración en cada iteración. El enfoque iterativo suministra un buen equilibrio entre la reducción del tiempo y el esfuerzo requerido para identificar los controles, incluso garantizando que los riesgos de impacto alto se valoren de manera correcta.

**Actividades para la gestión del riesgo de la seguridad de la información:**
- Establecimiento del contexto
- Valoración del riesgo
- Tratamiento del riesgo
- Aceptación del riesgo
- Comunicación del riesgo
- Monitoreo y revisión del riesgo

### Tabla de Actividades y Pasos

| ACTIVIDADES | PASO |
| :--- | :--- |
| **Establecimiento del contexto** | 1. Consideraciones Generales - Levantamiento de información inicial<br>2. Establecer criterios básicos para la Gestión del Riesgo<br>3. Definir alcance y límites de la Gestión del Riesgo<br>4. Establecer una organización para la operación del SGRSI |
| **Valoración del Riesgo** | 5. Identificar Activos de Información<br>6. Identificar las amenazas y las vulnerabilidades<br>7. Identificar los controles existentes<br>8. Identificar consecuencias<br>9. Valorar las consecuencias<br>10. Valorar los incidentes<br>11. Determinar el nivel de estimación del riesgo<br>12. Evaluar el riesgo |
| **Tratamiento del Riesgo** | 13. Seleccionar controles |
| **Aceptación del Riesgo** | 14. Aceptar el riesgo |
| **Comunicación del Riesgo** | 15. Comunicar el riesgo |
| **Monitoreo y Revisión del Riesgo** | 16. Monitorear y revisar los riesgos |

> **Diagrama detectado (Figura No. 2 PROCESO DE GESTIÓN DEL RIESGO EN LA SEGURIDAD DE LA INFORMACIÓN - Fuente: ISO27005):** Un diagrama de flujo complejo que conecta los bloques principales: Establecimiento del Contexto, Evaluación del Riesgo (Análisis de Riesgo: Identificación, Estimación, Evaluación), Decisión del Riesgo (Punto 1), Tratamiento del Riesgo, Decisión del Riesgo (Punto 2) y Aceptación del Riesgo, con flujos bidireccionales de Comunicación y Supervisión/Revisión.

---

## 4. Establecimiento del Contexto

### Consideraciones generales
> *"Se debe establecer el contexto para la gestión del riesgo de la seguridad de la información, lo cual implica establecer los criterios básicos que son necesarios para la gestión del riesgo de la seguridad de la información: definir el alcance y los límites, establecer una organización adecuada que opere la gestión del riesgo de la seguridad de la información."*

### Criterios Básicos
Dependiendo del alcance y los objetivos de la gestión del riesgo, se pueden aplicar diferentes enfoques. Es aconsejable seleccionar o desarrollar un enfoque adecuado que aborde:
- **Criterios de identificación del riesgo:** Es recomendable considerar los activos de información con el valor de impacto alto para el proceso de evaluación del riesgo.
- **Criterios de evaluación del riesgo:** Desarrollar criterios con el fin de determinar el riesgo de la seguridad de la información de la institución.
- **Criterios de impacto:** Especificarlos en términos del grado de daño o de los costos para la organización, causados por un evento de seguridad.
- **Criterios de la aceptación del riesgo:** Dependen con frecuencia de las políticas, metas, objetivos de la institución y de las partes interesadas. Las instituciones pueden definir sus propias escalas.

### Alcance y límites
Es necesario definir el alcance del proceso con el fin de garantizar que todos los activos relevantes se toman en consideración. Los ejemplos del alcance pueden ser una [[Aplicacion]] de [[TI]], infraestructura de TI, un proceso del negocio o una parte definida de la institución.
> *"El alcance y los límites de la gestión del riesgo de la seguridad de la información se relacionan con el alcance y los límites del Esquema Gubernamental de Seguridad de la Información – EGSI -"*

### Organización para la gestión del riesgo
Se recomienda establecer y mantener la organización y las responsabilidades en el proceso de gestión del riesgo y la seguridad de la información definidas en el acuerdo ministerial. Esta organización debería ser aprobada por la máxima autoridad de cada institución.

---

## 5. Valoración del Riesgo de la Seguridad de la Información

> *"Los riesgos se deberían identificar, describir cuantitativa o cualitativamente y priorizar frente a los criterios de evaluación del riesgo y los objetivos relevantes para la institución"*

La valoración del riesgo consta de las siguientes actividades:
1. **Análisis del riesgo:**
    - Identificación del riesgo
    - Estimación del riesgo
2. **Evaluación del riesgo**

### Análisis del Riesgo
Consiste en determinar qué puede provocar pérdidas a la institución mediante:
- Identificación de los activos
- Identificación de las amenazas
- Identificación de vulnerabilidades
- Identificación de la existencia de controles

#### Identificación de los Activos
Un activo es todo aquello que tiene valor para la organización y que, por lo tanto, requiere de protección. El [[Sistema de Informacion]] consta de más elementos que sólo hardware y software.
Se debe identificar al propietario de cada activo para asignarle la responsabilidad y rendición de cuentas. Existen dos clases generales de activos:
- **Activos primarios:**
    - Actividades y procesos del negocio.
    - Información.
- **Activos de soporte:**
    - Hardware.
    - Software.
    - Redes.
    - Personal.
    - Ubicación.
    - Estructura de la organización.

> **Tabla de Ejemplo de Identificación de Activos de Información:**
> Muestra registros desde **A1** hasta **A9** abarcando procesos macro de apoyo de tecnologías (Infraestructura, Redes y comunicaciones, Aplicaciones informáticas, Instalaciones, Talento Humano), tipos de activo (Hardware, Redes, Software, Localidad, Personal), nombres de activos (Controladora Wireless, Firewall Fortigate, Switch Core, Switches de Acceso, Antivirus, Servicio de Correo, Datacenter, Personal de soporte, etc.), descripciones y ubicaciones (Data Center, Edificio Matriz).

#### Valoración del Impacto (Pérdida)
Se evalúa en las tres dimensiones de la seguridad: **Confidencialidad (C)**, **Integridad (I)** y **Disponibilidad (D)** usando escalas de **Alto (3)**, **Medio (2)** y **Bajo (1)**.

El cálculo del impacto de un activo ($VA$) se obtiene mediante el promedio de los valores de las tres dimensiones:
$$VA = \frac{C + I + D}{3}$$

#### Identificación de Amenazas y Vulnerabilidades
Se identifican las amenazas y sus orígenes (ej. intrusos en la red, indisponibilidad de servicios, accesos no deseados). Asimismo, se detectan las vulnerabilidades explotables (ej. actualización de firmware de equipo antiguo, ausencia de redundancia, red de datos mixta).

#### Estimación o Análisis del Riesgo
Consiste en utilizar métodos cuantitativos o cualitativos para obtener una cuantificación de los riesgos identificados.

#### Evaluación del Riesgo
Consiste en comparar los riesgos estimados con los criterios de evaluación y aceptación definidos en el establecimiento del contexto.

El nivel de riesgo se calcula mediante la fórmula:
$$\text{Nivel de riesgo} = VA(CID) \times \text{Nivel de amenaza} \times \text{Nivel de vulnerabilidad}$$

**Escala de Nivel de Riesgo:**
- **1 - 3:** El riesgo es **BAJO** (Color verde)
- **4 - 8:** El riesgo es **MEDIO** (Color amarillo)
- **9 - 27:** El riesgo es **ALTO** (Color rojo)

---

## 6. Tratamiento del Riesgo de la Seguridad de la Información

El tratamiento de los riesgos consiste en tomar decisiones frente a los diferentes riesgos existentes de acuerdo con la estrategia de la institución. Se seleccionan controles para reducir, aceptar/retener, evitar o transferir los riesgos.

**Cuatro opciones disponibles para el tratamiento del riesgo:**
1. **Reducción del riesgo:** Mitigar mediante la selección de controles adecuados y justificados para que el riesgo residual sea aceptable.
2. **Evitación del riesgo:** Evitar la actividad o la acción que da origen al riesgo particular (ej. retirar una actividad o cambiar condiciones).
3. **Transferencia del riesgo:** Transferir el riesgo a otra parte que pueda gestionarlo de manera más eficaz (ej. contratos, seguros, migración a la nube).
4. **Retención/aceptación del riesgo:** Asumir el riesgo de manera consciente y objetiva cuando los costos superan el beneficio o cuando el nivel es muy bajo.

---

## 7. Aceptación del Riesgo de la Seguridad de la Información

Se debe tomar la decisión de aceptar los riesgos y las responsabilidades de forma documentada. Se aplica cuando el costo de implementación de un control sobrepasa el valor del activo o cuando el nivel de riesgo es muy bajo. Los criterios de aceptación pueden incluir umbrales múltiples y excepciones aprobadas por la alta dirección.

---

## 8. Comunicación de los Riesgos de la Seguridad de la Información

> *"La información acerca de los riesgos se debe intercambiar y/o compartir entre quienes toman las decisiones y las partes involucradas."*

La comunicación es bidireccional y busca lograr acuerdos, recolectar información, compartir resultados de valoración, evitar brechas por falta de entendimiento y brindar soporte para la toma de decisiones. Frecuentemente se canaliza a través del **Comité de Seguridad de la Información (CSI)**.

---

## 9. Monitoreo y Revisión del Riesgo de la Seguridad de la Información

Los riesgos no son estáticos; las amenazas, vulnerabilidades y consecuencias cambian abruptamente. Las organizaciones deben garantizar el monitoreo continuo de:
- Nuevos activos en el alcance.
- Modificaciones en los valores de los activos.
- Nuevas amenazas internas y externas.
- Incremento o aparición de nuevas vulnerabilidades.
- [[Incidentes de Seguridad de la Informacion]].

El proceso completo debe monitorearse, revisarse y mejorarse continuamente para asegurar su vigencia frente al entorno institucional.

---

## 10. Glosario de Términos

- **[[Activo de Informacion]]:** Cualquier información o elemento relacionado con el tratamiento de la misma que tenga valor para la institución.
- **[[Amenaza]]:** Causa potencial de un incidente no deseado que puede resultar en daño.
- **[[Analisis de Riesgos]]:** Proceso para comprender la naturaleza del riesgo y determinar su nivel.
- **[[Aplicacion]]:** Solución de TI que automatiza un proceso o función del negocio.
- **[[Ataque]]:** Intento de destruir, exponer, alterar, deshabilitar o robar un activo.
- **[[Autenticacion]]:** Provisión de garantía de que una característica afirmada por una entidad es correcta.
- **[[Autenticidad]]:** Propiedad de que una entidad es lo que afirma ser.
- **[[Comite de Seguridad de la Informacion (CSI)]]:** Encargado de gestionar la implementación y mejora continua del EGSI.
- **[[Confidencialidad]]:** Propiedad de que la información no esté disponible o divulgada a no autorizados.
- **[[Control]]:** Medida (política, procedimiento, práctica) que modifica el riesgo manteniéndolo por debajo del nivel asumido.
- **[[Disponibilidad]]:** Propiedad de estar accesible y utilizable por entidades autorizadas cuando se requiera.
- **[[EGSI]]:** Esquema Gubernamental de Seguridad de la Información.
- **[[Impacto]]:** Costo para la institución de un incidente materializado.
- **[[Incidente de Seguridad de la Informacion]]:** Evento inesperado que compromete las operaciones y amenaza la seguridad.
- **[[Integridad]]:** Propiedad de proteger la precisión y completitud de los activos.
- **[[Malware]]:** Software diseñado con intenciones maliciosas.
- **[[Phishing]]:** Proceso fraudulento para adquirir información confidencial haciéndose pasar por una entidad confiable.
- **[[Plan de Continuidad del Negocio]]:** Plan orientado a permitir la continuidad de funciones clave ante eventos imprevistos.
- **[[Propietario del Activo]]:** Responsable de la producción, desarrollo, mantenimiento y seguridad de un activo.
- **[[Resiliencia]]:** Capacidad de los activos institucionales para regresar a su forma original.
- **[[Riesgo]]:** Combinación de la probabilidad de un evento y sus consecuencias sobre un activo.
- **[[Vulnerabilidad]]:** Debilidad de un activo o control susceptible de ser explotada por una amenaza.