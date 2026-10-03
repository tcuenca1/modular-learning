---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] - Modelos de calidad del software

> **Diagrama detectado:** Fondo azul oscuro con elementos abstractos de interfaz gráfica corporativa, incluyendo iconos de seguridad con un escudo y una marca de verificación, paneles flotantes con código fuente simulado, gráficos de barras y líneas estadísticas, y lupas de análisis de datos.

---

## 1. Información General y Objetivos

* **Asignatura:** [[Ingenieria de Software II]]
* **Semana:** 1 · Clase 2
* **Tema:** [[Modelos de calidad del software]]: Garvin · McCall · [[ISO/IEC 9126]] · evolución de los modelos
* **Docente:** [DOCENTE]
* **Correo:** [ID_OMITIDO]
* **Institución:** Universidad Técnica de Machala · Tecnologías de la Información

### Objetivo e Indicador de Evaluación

* **OBJETIVO:** Comparar modelos de calidad del software mediante sus dimensiones, factores y características aplicables a la evaluación de [[producto software]].
* **INDICADOR:** Diferenciar modelos de calidad del software mediante sus dimensiones, factores, características y posibilidades de aplicación.
* **Pregunta guía:** ¿Todos los modelos evaluarían la calidad del mismo producto de igual manera?

---

## 2. De «calidad» a «modelo de calidad»

En la clase anterior concluimos que la [[calidad]] es **multidimensional**.

* **Concepto:** ¿Qué entendemos por calidad?
* **Perspectiva:** ¿Quién la observa?
* **Modelo:** ¿Cómo organizamos sus dimensiones?
* **Evaluación:** ¿Cómo la valoramos?

> Un modelo convierte una idea amplia de calidad en una estructura susceptible de análisis.

---

## 3. Garvin: Perspectivas de la calidad

La calidad cambia según el punto de vista desde el que se juzga el producto. David Garvin propone cinco perspectivas:

1. **Trascendente:** Excelencia reconocible.
2. **Producto:** Atributos medibles.
3. **Usuario:** Adecuación al uso.
4. **Producción:** Conformidad con requisitos.
5. **Valor:** Calidad frente al costo.

---

## 4. McCall: Factores de calidad del software

[[Modelo de McCall]] organiza los factores en tres grandes grupos orientados al [[ciclo de vida del software]]:

* **Operación del producto (Uso actual):**
  * Corrección
  * Confiabilidad
  * Eficiencia
  * Integridad
  * Usabilidad
* **Revisión del producto (Cambio interno):**
  * Mantenibilidad
  * Flexibilidad
  * Testabilidad
* **Transición del producto (Cambio de entorno):**
  * Portabilidad
  * Reusabilidad
  * Interoperabilidad

---

## 5. ISO/IEC 9126: Un antecedente clave

Estudiado como parte de la evolución histórica de los [[modelo de calidad|modelos de calidad]], estructurado en características fundamentales:

* **Funcionalidad:** Funciones adecuadas.
* **Fiabilidad:** Comportamiento estable.
* **Usabilidad:** Facilidad de uso.
* **Eficiencia:** Recursos y rendimiento.
* **Mantenibilidad:** Facilidad de cambio.
* **Portabilidad:** Adaptación a entornos.

---

## 6. Evolución de los modelos de calidad

> La evolución no elimina la idea anterior: reorganiza, amplía y precisa qué entendemos por calidad.

* **Garvin:** Perspectivas.
* **McCall:** Factores.
* **[[ISO/IEC 9126]]:** Características.
* **Modelos actuales:** Mayor cobertura y contexto.

---

## 7. Comparación estructurada de los enfoques

| Modelo | Unidad de análisis | Fortaleza didáctica / Orientación | Limitación / Contexto | Pregunta central |
| :--- | :--- | :--- | :--- | :--- |
| **Garvin** | Perspectiva | Comprender puntos de vista / Amplía el punto de vista | No es específico de software | ¿Desde dónde juzgo? |
| **McCall** | Factor | Relacionar atributos software / Orientación al producto software | Modelo histórico | ¿Qué factor observo? |
| **[[ISO/IEC 9126]]** | Característica | Estructurar la calidad / Estructura sistemática | Antecedente de modelos posteriores | ¿Qué característica evalúo? |

*Nota: No existe comparación útil sin considerar propósito, contexto y evidencia disponible.*

---

## 8. Caso de Estudio: Plataforma de comercio electrónico

### Evidencias disponibles
* Cumple las funciones de compra y pago.
* Usuarios reportan dificultad para localizar productos.
* El tiempo de respuesta aumenta en campañas masivas.
* El código presenta alta dependencia entre módulos.
* La solución debe migrarse a una nueva infraestructura.

### Reto
¿Qué aspectos de calidad resaltaría cada modelo? *(No busques «el mejor» todavía: identifica qué permite observar cada uno).*

---

## 9. Discusión y Árbol de decisión conceptual

1. ¿Qué modelo ofrece una lectura más cercana al usuario?
2. ¿Cuál permite organizar mejor atributos propios del [[producto software]]?
3. ¿Qué información del caso queda fuera de algún modelo?
4. ¿La selección del modelo depende del propósito de evaluación?

### Árbol de decisión para la selección de modelo:
* **¿Cuál es el propósito principal de la evaluación?**
  * Comprender diferentes puntos de vista $\rightarrow$ **Garvin**
  * Analizar factores del producto software $\rightarrow$ **McCall**
  * Organizar características de calidad $\rightarrow$ **[[ISO/IEC 9126]]**

---

## 10. Síntesis y Cierre

* **GARVIN:** Perspectivas (*¿Desde quién o desde qué lógica?*).
* **McCALL:** Factores (*¿Qué cualidad del software?*).
* **ISO/IEC 9126:** Características (*¿Cómo estructurar la evaluación?*).

> **Idea de salida:** Comparar modelos es reconocer qué organizan, qué priorizan y para qué sirven. La selección debe justificarse por propósito, contexto y evidencia disponible.