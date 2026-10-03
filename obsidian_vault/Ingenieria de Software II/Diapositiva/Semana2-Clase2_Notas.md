---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] - Evaluación cualitativa y cuantitativa de la calidad

---

## 1. Portada

**UNIVERSIDAD TÉCNICA DE MACHALA**
**[[Ingeniería de Software II]]**

* **Semana 2 · Clase 2**
* **Tema:** Evaluación cualitativa y cuantitativa de la calidad
* **Subtemas:** Criterios · escalas · evidencias · selección · interpretación
* **[DOCENTE]:** [ESTUDIANTE]
* **Correo:** [ID_OMITIDO]
* **Institución:** Universidad Técnica de Machala · Tecnologías de la Información

> **Gráfico detectado:** Fondo azul oscuro con temática tecnológica abstracta, que incluye elementos gráficos de código, iconos de verificación, gráficos de barras y líneas de tendencia financiera/analítica.

---

## 2. Objetivo e indicador de evaluación

* **OBJETIVO:** Evaluar la calidad de un producto software mediante criterios cualitativos y cuantitativos sustentados en evidencias.
* **INDICADOR:** Valora la calidad del producto software mediante criterios cualitativos y cuantitativos sustentados en evidencias.

> **Pregunta guía:** ¿Puede declararse que un producto es de calidad cuando cumple algunos atributos y falla en otros?

---

## 3. Caso detonante · Resultados contradictorios

**Plataforma de servicios digitales**
* Disponibilidad mensual: 99,95 %.
* Tiempo medio de respuesta: 1,8 s.
* Tasa de errores en transacciones: 1,9 %.
* Satisfacción de usuarios: 68/100.
* Tiempo medio para corregir defectos: 3,5 días.

> **PROBLEMA:**
> **¿Alta calidad, calidad aceptable o calidad insuficiente?**
> La respuesta debe poder defenderse con evidencia.

---

## 4. Dos formas complementarias de valorar

* **EVALUACIÓN CUALITATIVA**
  * Describe niveles o condiciones.
  * Puede utilizar categorías o rúbricas.
  * Interpreta contexto y experiencia.
  * Necesita criterios explícitos.

* **EVALUACIÓN CUANTITATIVA**
  * Utiliza medidas y métricas.
  * Permite comparación numérica.
  * Requiere escalas y umbrales.
  * Necesita interpretación contextual.

> **Fórmula clave:** $\text{Cualitativo} + \text{cuantitativo} + \text{evidencia} = \text{juicio técnico más defendible.}$

---

## 5. Criterios de evaluación · ¿Qué significa «aceptable»?

* **Criterio:** Regla para juzgar.
* **Umbral:** Valor límite.
* **Escala:** Niveles de valoración.
* **Condición:** Contexto de aplicación.

> **Ejemplo:** «Tiempo de respuesta $\le 3\text{ s}$ en el $95\text{ \%}$ de operaciones bajo carga nominal».

---

## 6. Escalas cualitativas · convertir observaciones en niveles

1. **4 · Excelente:** Cumple plenamente y supera el criterio.
2. **3 · Adecuado:** Cumple el criterio esperado.
3. **2 · Parcial:** Cumple con limitaciones relevantes.
4. **1 · Insuficiente:** No alcanza el criterio mínimo.

> *Una escala es útil solo si sus niveles pueden distinguirse mediante evidencia.*

---

## 7. Criterios cuantitativos · medir para decidir

* **Rendimiento** $\rightarrow$ Tiempo de respuesta $\le 3\text{ s}$  
  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*
* **Fiabilidad** $\rightarrow$ Tasa de fallos $< 1\text{ \%}$  
  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*
* **Disponibilidad** $\rightarrow$ Tiempo operativo $\ge 99,9\text{ \%}$  
  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*
* **Mantenibilidad** $\rightarrow$ Tiempo de corrección $\le 8\text{ h}$  
  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*

> *El número describe; el criterio permite interpretar.*

---

## 8. Evidencia · fundamento del juicio de calidad

* **Pruebas:** Resultados ejecutables.
* **Métricas:** Valores calculados.
* **Registros:** Datos de operación.
* **Encuestas:** Percepción estructurada.

> **Definición:** Evidencia fuerte = pertinente al atributo + obtenida mediante un procedimiento definido + interpretable contra un criterio.

---

## 9. Seleccionar características evaluables

* **Contexto:** ¿Dónde operará?
* **Riesgo:** ¿Qué puede fallar?
* **Requisitos:** ¿Qué se exige?
* **Usuario:** ¿Quién lo utiliza?
* **Recursos:** ¿Qué podemos medir?

> *Priorizar no significa ignorar la calidad: significa concentrar evidencia donde la decisión es más crítica.*

---

## 10. Perfil de calidad del producto

| Característica | Resultado | Criterio | Valoración |
| :--- | :--- | :--- | :--- |
| Rendimiento | $1,8\text{ s}$ | $\le 3\text{ s}$ | Adecuado |
| Disponibilidad | $99,95\text{ \%}$ | $\ge 99,9\text{ \%}$ | Adecuado |
| Usabilidad | $68/100$ | $\ge 80/100$ | Insuficiente |
| Fiabilidad | $1,9\text{ \% errores}$ | $< 1\text{ \%}$ | Insuficiente |

> **Pregunta:** ¿Un promedio global sería suficiente para aprobar este producto?

---

## 11. Matriz de evaluación · del dato a la valoración

| Característica | Criterio | Evidencia | Resultado | Valoración |
| :--- | :--- | :--- | :--- | :--- |
| Rendimiento | $\le 3\text{ s}$ | Prueba de carga | $1,8\text{ s}$ | Adecuado |
| Usabilidad | | | | |
| Fiabilidad | | | | |

> **Regla:** Ninguna valoración puede quedar sin criterio ni evidencia.

---

## 12. Interpretar resultados · evitar conclusiones automáticas

* **Error 1:** Confundir valor con calidad.
* **Error 2:** Usar umbrales sin contexto.
* **Error 3:** Promediar riesgos críticos.
* **Error 4:** Ignorar evidencia contradictoria.

> *Interpretar exige explicar qué significa el resultado para ese producto y ese contexto.*

---

## 13. Actividad aplicada · Comité de evaluación

* **TAREA DEL EQUIPO:**
  1. Seleccione $4$ características de calidad.
  2. Defina criterio o umbral para cada una.
  3. Asocie la evidencia disponible.
  4. Valore cada resultado.
  5. Construya un perfil de calidad.
  6. Emita una decisión técnica.

* **DECISIÓN FINAL:**
  * APROBADO
  * APROBADO CON CONDICIONES
  * NO APROBADO
  * *Defender en 2 minutos.*

---

## 14. Resultados contradictorios · ¿qué pesa más?

1. ¿Todos los atributos tienen la misma criticidad?
2. ¿Un atributo excelente compensa otro insuficiente?
3. ¿Cuándo un incumplimiento debe bloquear la aceptación?
4. ¿Qué información adicional cambiaría la decisión?

> *La calidad es multidimensional; la decisión debe hacer visibles los compromisos y riesgos.*

---

## 15. Cómo redactar un dictamen técnico de calidad

1. **Alcance evaluado**
2. **Criterios utilizados**
3. **Evidencias obtenidas**
4. **Resultados relevantes**
5. **Riesgos e incumplimientos**
6. **Conclusión técnica**

> *Un dictamen defendible permite rastrear la conclusión hasta criterios y evidencias.*

---

## 16. Síntesis · proceso de evaluación del producto

$$\text{Seleccionar características} \rightarrow \text{Definir criterios} \rightarrow \text{Obtener evidencias} \rightarrow \text{Comparar resultados} \rightarrow \text{Interpretar significado} \rightarrow \text{Valorar calidad}$$

> **Flujo resumido:** Característica $\rightarrow$ criterio $\rightarrow$ evidencia $\rightarrow$ resultado $\rightarrow$ interpretación $\rightarrow$ valoración.

---

## 17. Comprobación individual

* **Escenario:** disponibilidad real $99,6\text{ \%}$ · requisito $\ge 99,9\text{ \%}$ · usuarios satisfechos $92/100$.
* ¿Qué resultado es cuantitativo?
* ¿Qué criterio se incumple?
* ¿La alta satisfacción compensa el incumplimiento de disponibilidad?
* Redacta una valoración técnica de $2–3$ líneas.

> *La conclusión debe mencionar explícitamente criterio, evidencia e implicación.*

---

## 18. Cierre · evidencia antes que opinión

* **Ticket de salida:**
  > «Un producto no puede declararse de calidad solo porque __________. Una valoración sustentada requiere __________, __________ y __________».

* Añade un ejemplo cuantitativo y uno cualitativo que podrían formar parte de una evaluación.
* **Próxima semana:** defectos y métricas de revisión del software.