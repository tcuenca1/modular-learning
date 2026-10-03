---
materia: Seguridad de la Informacion
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [seguridad_de_la_informacion, diapositiva, ingesta_ia]
---

# [[Seguridad de la Informacion]] - Guía para la Gestión de Riesgos de Seguridad de la Información

> **Diagrama detectado:** Portada institucional con elementos gráficos isométricos en tonos azules oscuros que representan seguridad digital, incluyendo un dispositivo móvil mostrando campos de contraseña con asteriscos, un icono de nube y cubos de datos interconectados.

---

## Contenido

1. Introducción
2. Conceptos Básicos
3. Proceso para la Gestión del Riesgo de la [[Seguridad de la Informacion]]
4. Establecimiento del Contexto
5. Valoración del Riesgo de la [[Seguridad de la Informacion]]
   - Análisis del Riesgo
   - Evaluación del Riesgo
6. Tratamiento del Riesgo de la [[Seguridad de la Informacion]]
7. Aceptación del Riesgo de la [[Seguridad de la Informacion]]
8. Comunicación de los Riesgos de la [[Seguridad de la Informacion]]
9. Monitoreo y Revisión del Riesgo de la [[Seguridad de la Informacion]]
10. Glosario de Términos

---

## Introducción

La revolución digital ha generado que las organizaciones a nivel mundial tomen mayor atención a la información, actor principal de este proceso de cambio. Este proceso ha permitido establecer nuevas alianzas y acortar distancias entre naciones, donde el internet cumple un papel fundamental en la comunicación.

En términos de gestión de riesgos de [[Seguridad de la Informacion]], el activo a proteger es la información, tanto digital (contenida en los [[Sistema de información|sistemas de información]]) como aquella contenida en cualquier otro medio como por ejemplo el papel. Debemos tener presente que la gestión debe ocuparse de todo el ciclo de vida de la información.

Es necesario un enfoque sistemático para la gestión del riesgo en la [[Seguridad de la Informacion]] para identificar las necesidades de la organización con respecto a los requisitos de seguridad y para crear un eficaz **[[SGSI]]** (Sistema de Gestión de la Seguridad de la Información).

> *"La gestión del riesgo analiza lo que puede suceder y cuáles pueden ser las posibles consecuencias, antes de decidir lo que se debe hacer y cuando hacerlo, con el fin de reducir el riesgo hasta un nivel aceptable".*

---

## Conceptos Básicos

La información es el activo principal, pero también debemos considerar: infraestructura informática, equipos auxiliares, redes de comunicaciones, instalaciones y personas.

Cuando hablamos de [[Seguridad de la Informacion]] hablamos de protegerla de riesgos que puedan afectar a una o varias de sus tres propiedades principales (Tríada CIA):

- **Confidencialidad:** La información solo tiene que ser accesible o divulgada a aquellos que están autorizados.
- **Integridad:** La información debe permanecer correcta (integridad de datos) y como el emisor la originó (integridad de fuente) sin manipulaciones por terceros.
- **Disponibilidad:** La información debe estar siempre accesible para aquellos que estén autorizados.

> **Diagrama detectado:** Figura No. 1 - Principios de la S.I. (Tríada CIA: Confidencialidad, Integridad, Disponibilidad rodeando al núcleo de Información). Fuente: `https://infosegur.wordpress.com/tag/disponibilidad/`

### Definiciones Clave

- **Riesgo:** Posibilidad de que una [[Amenaza]] concreta pueda explotar una [[Vulnerabilidad]] para causar una pérdida o daño en un activo de información.
- **[[Amenaza]]:** Causa potencial de un incidente no deseado, que puede resultar en un daño a un sistema, persona u organización.
- **[[Vulnerabilidad]]:** Debilidad de un activo o control que puede ser explotada por una o más amenazas.
- **[[Impacto]]:** Consecuencia de la materialización de una amenaza sobre un activo.
- **Riesgo inherente:** Riesgo existente y propio de cada actividad, sin la ejecución de ningún control.
- **[[Riesgo residual]]:** Riesgo que permanece tras el tratamiento del riesgo.

---

## Proceso para la Gestión del Riesgo de la Seguridad de la Información

El proceso de gestión del riesgo puede ser iterativo. Las actividades clave son:

1. Establecimiento del contexto
2. Valoración del riesgo
3. Tratamiento del riesgo
4. Aceptación del riesgo
5. Comunicación del riesgo
6. Monitoreo y revisión del riesgo

> **Diagrama detectado:** Figura No. 2 - Proceso de gestión del riesgo en la [[Seguridad de la Informacion]] (Fuente: [[ISO27005]]). Muestra el flujo iterativo desde el establecimiento del contexto, análisis del riesgo, estimación, evaluación y decisión de tratamiento mediante controles.

---

## Establecimiento del Contexto

Se deben establecer los criterios básicos que son necesarios para la gestión del riesgo: definir el alcance y los límites, y establecer una organización adecuada para operar el [[SGSI]].

### Criterios Básicos
- **Criterios de identificación del riesgo:** Considerar activos de información con valor de impacto alto.
- **Criterios de evaluación del riesgo:** Determinar el nivel de riesgo de la institución.
- **Criterios de impacto:** Especificados en términos de grado de daño o costos para la organización.
- **Criterios de aceptación del riesgo:** Dependen de las políticas, metas y objetivos de la institución.

---

## Valoración del Riesgo de la Seguridad de la Información

La valoración cuantifica o describe cualitativamente el riesgo y consta de:
1. **[[Análisis de riesgos]]**
   - Identificación del riesgo (Activos, Amenazas, Vulnerabilidades, Controles existentes)
   - Estimación o análisis del riesgo
2. **[[Evaluación de riesgos]]**

### Identificación de Activos
Se dividen en dos clases:
- **Activos primarios:** Actividades y procesos del negocio, Información.
- **Activos de soporte:** [[Hardware]], [[Software]], Redes, Personal, Ubicación, Estructura de la organización.

> *Fórmula de Valoración del Impacto de un Activo (VA):*
> $$VA = \frac{C + I + D}{3}$$
> *(Donde C = Confidencialidad, I = Integridad, D = Disponibilidad)*

---

## Estimación y Evaluación del Riesgo

### Cálculo del Nivel de Riesgo
El nivel de riesgo de cada activo se calcula mediante la fórmula:

$$\text{Nivel de riesgo} = VA(CID) \times \text{Nivel de amenaza} \times \text{Nivel de vulnerabilidad}$$

#### Escala de Niveles de Riesgo:
- **1 - 3:** El riesgo es **BAJO** (Color verde)
- **4 - 8:** El riesgo es **MEDIO** (Color amarillo)
- **9 - 27:** El riesgo es **ALTO** (Color rojo)

---

## Tratamiento del Riesgo de la Seguridad de la Información

Existen cuatro opciones disponibles para el tratamiento del riesgo:
1. **Reducción del riesgo:** Selección de controles ([[Mitigación]]) para disminuir probabilidad e impacto.
2. **Evitación del riesgo:** Retirar la actividad o cambiar las condiciones que originan el riesgo.
3. **Transferencia del riesgo:** Trasladar el riesgo a otra parte ([[Proveedor de servicios de Internet|terceros]], seguros).
4. **Retención / Aceptación del riesgo:** Asumir el riesgo de manera consciente y objetiva.

> **Diagrama detectado:** Figura No. 3 - Actividades para el tratamiento de los riesgos (Fuente: [[ISO27005]]). Muestra las ramificaciones de opciones de tratamiento hacia los riesgos residuales.

---

## Comunicación, Monitoreo y Revisión

- **Comunicación del riesgo:** Actividad bidireccional para intercambiar información entre quienes toman decisiones y las partes involucradas. Se apoya en el **Comité de Seguridad de la Información (CSI)**.
- **Monitoreo y revisión de los factores de riesgo:** Los riesgos no son estáticos. Se debe vigilar la aparición de nuevos activos, modificaciones de valor, nuevas amenazas y cambios en las vulnerabilidades.

---

## Glosario de Términos (Extracto Principal)

- [[Activo de información]]: Cualquier información o elemento relacionado que tenga valor para la institución.
- [[Amenaza]]: Causa potencial de un incidente no deseado.
- [[Análisis de riesgos]]: Proceso para comprender la naturaleza del riesgo y determinar su nivel.
- [[Ataque]]: Intento de destruir, exponer, alterar, deshabilitar o robar un activo.
- [[Confidencialidad]]: Propiedad de que la información no esté disponible o sea divulgada a entidades no autorizadas.
- [[Control]]: Medidas, políticas y procedimientos para mantener los riesgos por debajo del nivel asumido.
- [[Incidente de seguridad de la información]]: Evento inesperado que compromete las operaciones del negocio.
- [[Malware]]: Software diseñado con intenciones dañinas.
- [[Phishing]]: Proceso fraudulento para adquirir información privada.
- [[Resiliencia]]: Capacidad de los activos institucionales para regresar a su forma original.
- [[Riesgo residual]]: Riesgo que permanece tras su tratamiento.
- [[Vulnerabilidad]]: Debilidad de un activo o control explotable por una amenaza.