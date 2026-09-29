---
materia: [[Ingenieria de Software II]]
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# A systematic literature review of open source software quality assessment models

**Autores:** [ESTUDIANTE], [DOCENTE], [ESTUDIANTE], [ESTUDIANTE], [ESTUDIANTE]  
**Institución:** [[Covenant University]], [[Atilim University]], [[Pontificia Universidad Católica de Valparaíso]]

---

## Abstract

Muchos modelos de evaluación de calidad de [[Software Libre y Código Abierto|Open Source Software (OSS)]] están disponibles en la literatura, sin embargo, existe poca o nula adopción de estos modelos en la práctica. El objetivo de este estudio es realizar una revisión sistemática de la literatura ([[Revisión Sistemática de la Literatura]]) para investigar las propiedades de los modelos existentes de evaluación de calidad de OSS, clasificándolos con respecto a sus características de calidad, la metodología utilizada para la evaluación y su dominio de aplicación.

> **Diagrama detectado:** Encabezado del artículo científico publicado en SpringerPlus (2016), indicando el título de la revisión sistemática sobre modelos de calidad de OSS, autores, filiaciones y resumen estructurado con antecedentes, resultados y conclusiones.

---

## Background

Previo a la aparición de los modelos de calidad para [[Software Libre y Código Abierto|OSS]], ya existían modelos clásicos como [[McCall]], [[Dromey]] y [[ISO 9126]]. Sin embargo, estos modelos no consideraban atributos únicos del [[Software Libre y Código Abierto|OSS]] como la **comunidad** (un conjunto de usuarios y desarrolladores formados alrededor del OSS que contribuyen al software).

### Evolución de Estándares
* [[ISO 9126]]: Define 6 características de calidad interna y externa (funcionalidad, confiabilidad, usabilidad, eficiencia, mantenibilidad y portabilidad).
* [[ISO 25010]]: Reemplazó a la [[ISO 9126]] en 2010. Divide la calidad en:
  * **Calidad del producto:** Adecuación funcional, confiabilidad, eficiencia de rendimiento, operabilidad, seguridad, compatibilidad, mantenibilidad y transferibilidad.
  * **Calidad en uso:** Eficacia, eficiencia, satisfacción, seguridad y usabilidad.

### Características de Calidad Relacionadas con la Comunidad
* **Capacidad de mantenimiento (*Maintenance Capacity*):** Número de contribuidores y el tiempo que están dispuestos a aportar (observable en registros de versiones, listas de correo, foros y sistemas de seguimiento de errores o *bug reports*).
* **Sostenibilidad (*Sustainability*):** Capacidad de la comunidad para crecer atrayendo nuevos contribuidores.
* **Madurez de procesos (*Process Maturity*):** Adopción de prácticas estándar de desarrollo (revisión por pares, *test suites*, lanzamientos planificados).

---

## Methods

Se aplicaron las directrices de [[Kitchenham]] para revisiones sistemáticas.

### Preguntas de Investigación (RQ)
1. **RQ1:** ¿Cuáles son las características clave de calidad poseídas por los modelos de evaluación de OSS?
2. **RQ2:** ¿Qué métodos de selección emplean estos modelos de evaluación?
3. **RQ3:** ¿Cuál es el dominio de aplicación de los modelos de evaluación de OSS?

### Estrategia de Búsqueda y Selección
* **Cadena de búsqueda:** `(Open Source Software OR libre OR OSS or FLOSS or FOSS) AND (model OR quality model OR measurement model OR evaluation model)`
* Fuentes consultadas: [[Scopus]], [[IEEE Xplore]], [[ACM Digital Library]], [[ScienceDirect]], [[Springer]] y [[Google Search]].
* Rango temporal: 2003 a 2015.
* Se seleccionaron **19 estudios primarios** tras aplicar los criterios de inclusión/exclusión y evaluación de calidad (QA1 a QA4).

---

## Results

### Clasificación de Modelos según RQ1 (Características de Calidad)
Los modelos se clasifican en cinco categorías:
1. **Modelos de un solo atributo (*Single-attribute models*):** Miden una sola característica (ej. [[QSOS]], modelos de Mathieu y Wray, Sudhaman y Thangavel, [[OS-UMM]]).
2. **Modelos de categoría redonda (*Rounded category models*):** Poseen al menos una característica en cada categoría (producto, calidad en uso y comunidad), ej. [[OSMM]], [[Open BRR]], [[SQO-OSS]], [[EFFORT]], Müller, Sohn et al.
3. **Modelos de atributos exclusivos de comunidad (*Community-only attribute model*):** Solo miden características comunitarias (ej. modelo de Kuwata et al.).
4. **Modelos sin atributos comunitarios (*Non-community attribute model*).**
5. **Modelos sin calidad en uso (*Non-quality in use models*).**

> **Diagrama detectado:** Gráficos de distribución de frecuencia (Figuras 1, 2 y 3) que muestran la presencia de características de calidad del producto (destacando la mantenibilidad con un 55%), características de calidad en uso (destacando la usabilidad con un 50%) y características de la comunidad (destacando la capacidad de mantenimiento con un 45%).

### Métodos de Selección (RQ2)
* **Modelo (*Model*):** Representación de sistemas basada en estructuras jerárquicas (**32%** - el más popular).
* **Proceso (*Process*):** Serie de acciones o funciones (**21%**).
* **Otros (*Other*):** Directrices (**16%**).
* **Framework:** **11%**.
* **Basado en herramientas (*Tool-based*):** **10%**.
* **Minería de datos (*Data mining*):** **10%** (incluye redes neuronales artificiales, razonamiento basado en casos, análisis envolvente de datos - DEA, y lógica difusa).

> **Diagrama detectado:** Gráfico circular (Figura 4) que ilustra la proporción de los métodos de selección empleados en los modelos de evaluación de OSS analizados.

### Dominio de Aplicación (RQ3)
* **No especificado:** **47%** (la gran mayoría son independientes del dominio).
* **Software dominado por datos (*Data-dominant software*):** **26%** (sistemas empresariales como [[ERP]], [[CRM]], software de diseño/ingeniería y sistemas de visualización/transacciones).
* **Software de sistema (*Systems software*):** **16%** (sistemas operativos, redes, drivers, middleware).
* **Software dominado por computación (*Computation-dominant software*):** **11%** (investigación de operaciones, software científico, inteligencia artificial).

> **Diagrama detectado:** Gráfico circular (Figura 5) que muestra la distribución de los dominios de aplicación de los modelos analizados en la literatura.

---

## Summary and Discussion

* **Hallazgos principales:**
  * Ningún modelo existente evalúa todos los criterios bajo producto, calidad en uso y comunidad simultáneamente.
  * Los atributos de satisfacción y seguridad de la calidad en uso **nunca** son considerados en los modelos actuales de OSS.
  * Existe una fuerte inclinación hacia enfoques no automatizados, lo que hace que la aplicación de los modelos sea laboriosa y lenta.
* **Implicaciones para la práctica y futuras investigaciones:**
  * Se debe desplazar el foco desde construir modelos ultra-completos hacia modelos centrados en **características esenciales**: mantenibilidad, usabilidad y capacidad de mantenimiento de la comunidad.
  * Es necesario incorporar métodos de selección automatizables y técnicas de **Toma de Decisiones Multicriterio ([[MCDM]])** como [[AHP]], [[TOPSIS]] o [[DEA]].

---

## Conclusiones

El estudio analizó 19 artículos sobre modelos de evaluación de calidad de [[Software Libre y Código Abierto|OSS]] publicados entre 2003 y 2015. Se concluye que la **mantenibilidad** (producto), la **usabilidad** (calidad en uso) y la **capacidad de mantenimiento** (comunidad) son los pilares fundamentales que deben guiar el desarrollo de futuros modelos de evaluación de software libre.