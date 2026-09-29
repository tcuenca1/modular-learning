---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] - Evaluación cualitativa y cuantitativa de la calidad

---

## 1. Portada y Metadatos
* **Universidad:** Universidad Técnica de Machala · Tecnologías de la Información
* **Asignatura:** [[Ingenieria de Software II]]
* **Sesión:** Semana 2 · Clase 2
* **Tema:** Evaluación cualitativa y cuantitativa de la calidad (Criterios, escalas, evidencias, selección, interpretación)
* **Docente:** [DOCENTE] ([ID_OMITIDO])

> **Diagrama detectado:** Fondo de temática tecnológica en tonos azules oscuros con gráficos abstractos de código fuente, paneles de control con gráficos de barras, barras de progreso con verificación de estados (iconos de check) y una lupa con marca de verificación en la esquina inferior derecha.

---

## 2. Objetivo e Indicador de Evaluación

* **OBJETIVO:** Evaluar la [[Calidad del Software]] mediante criterios cualitativos y cuantitativos sustentados en [[Evidencia Técnica]].
* **INDICADOR:** Valora la calidad del producto software mediante criterios cualitativos y cuantitativos sustentados en evidencias.

> **Pregunta guía:** ¿Puede declararse que un producto es de calidad cuando cumple algunos atributos y falla en otros?

---

## 3. Caso Detonante · Resultados Contradictorios

### Plataforma de servicios digitales
* Disponibilidad mensual: 99,95 %.
* Tiempo medio de respuesta: 1,8 s.
* Tasa de errores en transacciones: 1,9 %.
* Satisfacción de usuarios: 68/100.
* Tiempo medio para corregir defectos: 3,5 días.

> **PROBLEMA:** ¿Alta calidad, calidad aceptable o calidad insuficiente? 
> La respuesta debe poder defenderse con evidencia.

---

## 4. Dos Formas Complementarias de Valorar

### Evaluación Cualitativa
* Describe niveles o condiciones.
* Puede utilizar categorías o rúbricas.
* Interpreta contexto y experiencia.
* Necesita criterios explícitos.

### Evaluación Cuantitativa
* Utiliza medidas y [[Métricas de Software]].
* Permite comparación numérica.
* Requiere escalas y umbrales.
* Necesita interpretación contextual.

> **Regla fundamental:** Cualitativo + cuantitativo + evidencia = juicio técnico más defendible.

---

## 5. Criterios de Evaluación · ¿Qué significa «aceptable»?

* **Criterio:** Regla para juzgar.
* **Umbral:** Valor límite.
* **Escala:** Niveles de valoración.
* **Condición:** Contexto de aplicación.

> **Ejemplo:** «Tiempo de respuesta $\le 3\text{ s}$ en el $95\text{ \%}$ de operaciones bajo carga nominal».

---

## 6. Escalas Cualitativas · Convertir Observaciones en Niveles

* **4 · Excelente:** Cumple plenamente y supera el criterio.
* **3 · Adecuado:** Cumple el criterio esperado.
* **2 · Parcial:** Cumple con limitaciones relevantes.
* **1 · Insuficiente:** No alcanza el criterio mínimo.

> **Nota:** Una escala es útil solo si sus niveles pueden distinguirse mediante evidencia.

---

## 7. Criterios Cuantitativos · Medir para Decidir

* **Rendimiento:** Tiempo de respuesta $\le 3\text{ s}$  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*
* **Fiabilidad:** Tasa de fallos $< 1\text{ \%}$  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*
* **Disponibilidad:** Tiempo operativo $\ge 99,9\text{ \%}$  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*
* **Mantenibilidad:** Tiempo de corrección $\le 8\text{ h}$  *(atributo $\rightarrow$ métrica $\rightarrow$ umbral)*

> **Principio:** El número describe; el criterio permite interpretar.

---

## 8. Evidencia · Fundamento del Juicio de Calidad

* **Pruebas:** Resultados ejecutables.
* **Métricas:** Valores calculados.
* **Registros:** Datos de operación.
* **Encuestas:** Percepción estructurada.

> **Definición de Evidencia Fuerte:** Pertinente al atributo + obtenida mediante un procedimiento definido + interpretable contra un criterio.

---

## 9. Seleccionar Características Evaluables

* **Contexto:** ¿Dónde operará?
* **Riesgo:** ¿Qué puede fallar?
* **Requisitos:** ¿Qué se exige?
* **Usuario:** ¿Quién lo utiliza?
* **Recursos:** ¿Qué podemos medir?

> **Nota de gestión:** Priorizar no significa ignorar la calidad: significa concentrar evidencia donde la decisión es más crítica.

---

## 10. Perfil de Calidad del Producto

| Característica | Resultado | Criterio | Valoración |
| :--- | :--- | :--- | :--- |
| Rendimiento | 1,8 s | $\le 3\text{ s}$ | Adecuado |
| Disponibilidad | 99,95 % | $\ge 99,9\text{ \%}$ | Adecuado |
| Usabilidad | 68/100 | $\ge 80/100$ | Insuficiente |
| Fiabilidad | 1,9 % errores | $< 1\text{ \%}$ | Insuficiente |

> **Pregunta:** ¿Un promedio global sería suficiente para aprobar este producto?

---

## 11. Matriz de Evaluación · Del Dato a la Valoración

| Característica | Criterio | Evidencia | Resultado | Valoración |
| :--- | :--- | :--- | :--- | :--- |
| Rendimiento | $\le 3\text{ s}$ | Prueba de carga | 1,8 s | Adecuado |
| Usabilidad | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* |
| Fiabilidad | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* | *(Pendiente)* |

> **Regla:** Ninguna valoración puede quedar sin criterio ni evidencia.

---

## 12. Interpretar Resultados · Evitar Conclusiones Automáticas

* **Error 1:** Confundir valor con calidad.
* **Error 2:** Usar umbrales sin contexto.
* **Error 3:** Promediar riesgos críticos.
* **Error 4:** Ignorar evidencia contradictoria.

> **Nota:** Interpretar exige explicar qué significa el resultado para ese producto y ese contexto.

---

## 13. Actividad Aplicada · Comité de Evaluación

### Tarea del Equipo
1. Seleccione 4 características de calidad.
2. Defina criterio o umbral para cada una.
3. Asocie la evidencia disponible.
4. Valore cada resultado.
5. Construya un perfil de calidad.
6. Emita una decisión técnica.

### Decisiones Posibles
* **APROBADO**
* **APROBADO CON CONDICIONES**
* **NO APROBADO**

> **Dinámica:** Defender en 2 minutos.

---

## 14. Resultados Contradictorios · ¿Qué Pesa Más?

1. ¿Todos los atributos tienen la misma criticidad?
2. ¿Un atributo excelente compensa otro insuficiente?
3. ¿Cuándo un incumplimiento debe bloquear la aceptación?
4. ¿Qué información adicional cambiaría la decisión?

> **Conclusión:** La calidad es multidimensional; la decisión debe hacer visibles los compromisos y riesgos.

---

## 15. Cómo Redactar un Dictamen Técnico de Calidad

1. Alcance evaluado
2. Criterios utilizados
3. Evidencias obtenidas
4. Resultados relevantes
5. Riesgos e incumplimientos
6. Conclusión técnica

> **Principio de auditoría:** Un dictamen defendible permite rastrear la conclusión hasta criterios y evidencias.

---

## 16. Síntesis · Proceso de Evaluación del Producto

$$\text{Seleccionar características} \rightarrow \text{Definir criterios} \rightarrow \text{Obtener evidencias} \rightarrow \text{Comparar resultados} \rightarrow \text{Interpretar significado} \rightarrow \text{Valorar calidad}$$

> **Flujo clave:** Característica $\rightarrow$ criterio $\rightarrow$ evidencia $\rightarrow$ resultado $\rightarrow$ interpretación $\rightarrow$ valoración.

---

## 17. Comprobación Individual

> **Escenario:** Disponibilidad real $99,6\text{ \%}$ · Requisito $\ge 99,9\text{ \%}$ · Usuarios satisfechos $92/100$.

* ¿Qué resultado es cuantitativo?
* ¿Qué criterio se incumple?
* ¿La alta satisfacción compensa el incumplimiento de disponibilidad?
* Redacta una valoración técnica de 2–3 líneas.

> **Nota:** La conclusión debe mencionar explícitamente criterio, evidencia e implicación.

---

## 18. Cierre · Evidencia Antes que Opinión

### Ticket de Salida
> «Un producto no puede declararse de calidad solo porque __________. Una valoración sustentada requiere __________, __________ y __________.»

* Añade un ejemplo cuantitativo y uno cualitativo que podrían formar parte de una evaluación.
* **Próxima semana:** Defectos y métricas de revisión del software.