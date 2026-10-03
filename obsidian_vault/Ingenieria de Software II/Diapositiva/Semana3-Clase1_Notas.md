---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] · Unidad I
## Defectos y métricas de revisión del software

> **Contenido de la diapositiva:** Error · defecto · fallo · origen · propagación · impacto  
> **Semana 3 · Clase 1**  
> **¿Por qué un defecto pequeño puede convertirse en un problema grande?**  
> [DOCENTE], [ID_OMITIDO]  
> Universidad Técnica de Machala · Tecnologías de la Información  
> *Nota: Se omitieron datos de contacto personales por privacidad.*

---

## Ruta de aprendizaje de la clase

1. **Problematizar**: ¿Defecto pequeño = impacto pequeño?
2. **Diferenciar**: Error · defecto · [[fallo de software]]
3. **Rastrear**: Origen y propagación
4. **Clasificar**: [[Requisito]] · diseño · código
5. **Evaluar**: Impacto y detección temprana

> **Meta:** Explicar cómo un defecto nace, se propaga y afecta la calidad del producto.

---

## Objetivo e indicador de evaluación

* **OBJETIVO:** Analizar los [[defecto de software|defectos del software]] mediante su clasificación, origen e impacto en los artefactos del proceso de desarrollo.
* **INDICADOR:** Clasifica [[defecto de software|defectos del software]] según su naturaleza, origen, propagación e impacto sobre la calidad del producto.

> **Pregunta guía:** ¿El defecto pertenece únicamente a la etapa donde finalmente fue descubierto?

---

## Caso detonante · «El requisito parecía correcto»

* **[[Requisito]]:** “El sistema bloqueará operaciones sospechosas automáticamente”.
* El diseño interpreta “sospechosa” mediante una única regla fija.
* El código implementa correctamente la regla definida en el diseño.
* Las pruebas cubren únicamente los ejemplos conocidos por el equipo.
* En producción, operaciones legítimas son bloqueadas y generan reclamos.

> **DESAFÍO:** ¿El problema es de requisito, diseño, código, prueba o de todos ellos?

---

## Error, defecto y fallo · no son sinónimos

* **ERROR**
  * Acción o decisión humana incorrecta.
  * *Ej.:* Interpretar mal una necesidad.
* **DEFECTO**
  * Problema incorporado a un artefacto.
  * *Ej.:* Regla incorrecta en requisito, diseño o código.
* **FALLO**
  * Manifestación observable en ejecución.
  * *Ej.:* Resultado incorrecto para una entrada concreta.

> **Cadena causal:** Error humano $\rightarrow$ puede introducir un defecto $\rightarrow$ que bajo ciertas condiciones puede producir un [[fallo de software]].

---

## De la causa al efecto · cadena de propagación

1. Error humano $\rightarrow$
2. Defecto introducido $\rightarrow$
3. Defecto alcanza ejecución $\rightarrow$
4. Condición lo activa $\rightarrow$
5. Fallo observable

> **Pregunta:** ¿Puede existir un defecto durante meses sin producir un fallo? Sí, si nunca se activa.

---

## Clasificación por artefacto de origen

* **REQUISITOS**
  * Ambigüedad
  * Omisión
  * Inconsistencia
  * Criterio no verificable
* **DISEÑO**
  * Responsabilidad incorrecta
  * Interfaz mal definida
  * Decisión arquitectónica débil
  * Modelo de datos inadecuado
* **CÓDIGO**
  * Lógica incorrecta
  * Condición límite
  * Estado no controlado
  * Manejo de error deficiente

> **Nota importante:** Detectar en pruebas $\neq$ originarse en pruebas.

---

## Propagación entre artefactos del desarrollo

$$\text{Necesidad} \rightarrow \text{Requisito} \rightarrow \text{Diseño} \rightarrow \text{Código} \rightarrow \text{Pruebas} \rightarrow \text{Producción}$$

* Un defecto no corregido puede heredarse, transformarse o amplificarse en los artefactos posteriores.
* **Riesgo adicional:** Si prueba y código se derivan de la misma interpretación equivocada, la prueba puede “confirmar” un comportamiento incorrecto.

---

## Clasificación por naturaleza del defecto

* **Funcional:** Resultado o regla incorrecta
* **Interfaz:** Interacción o contrato defectuoso
* **Datos:** Integridad, formato o transformación
* **Rendimiento:** Tiempo, capacidad o recursos
* **Seguridad:** Protección, acceso o exposición
* **Mantenibilidad:** Cambio costoso o riesgoso

> Una misma causa puede producir defectos de distinta naturaleza en diferentes niveles.

---

## Severidad $\neq$ prioridad

* **SEVERIDAD**
  * Impacto técnico o funcional
  * Daño potencial
  * Alcance del fallo
  * Consecuencia para usuario/sistema
* **PRIORIDAD**
  * Urgencia de corrección
  * Valor de negocio
  * Riesgo de exposición
  * Dependencias y fecha de liberación

> No todo defecto severo es el primero que se corrige; la decisión debe justificarse.

---

## Impacto del defecto sobre la calidad del producto

* **Funcional:** Resultado incorrecto
* **Confiabilidad:** Fallos o interrupciones
* **Rendimiento:** Latencia o saturación
* **Seguridad:** Exposición o acceso indebido
* **Usabilidad:** Errores de interacción
* **Mantenibilidad:** Cambio costoso y riesgoso

> $\text{Impacto} = \text{consecuencia observable} + \text{riesgo sobre atributos de calidad}$.

---

## ¿Por qué importa detectar temprano?

* **Requisitos:** Pocos artefactos afectados $\rightarrow \uparrow \text{retrabajo}$
* **Diseño:** Decisiones derivadas $\rightarrow \uparrow \text{retrabajo}$
* **Código:** Implementación y pruebas $\rightarrow \uparrow \text{retrabajo}$
* **Producción:** Usuarios, datos y operación $\rightarrow \uparrow \text{retrabajo}$

> La detección temprana reduce propagación; no significa que todos los defectos tempranos sean baratos ni que exista una razón fija universal.

---

## Revisiones tempranas como barrera de propagación

* **REVISIÓN / ANÁLISIS ESTÁTICO**
  * Examina artefactos sin ejecutar.
  * Puede actuar desde requisitos y diseño.
  * Busca inconsistencias, omisiones y defectos.
* **PRUEBA / OBSERVACIÓN DINÁMICA**
  * Ejecuta el software.
  * Activa condiciones concretas.
  * Observa fallos y comportamiento.

> Ambas son complementarias: detectar defectos y observar fallos son problemas relacionados, pero distintos.

---

## De defectos a métricas de revisión

* **Conteo:** ¿Cuántos defectos detectamos?
* **Distribución:** ¿Dónde y de qué tipo aparecen?
* **Densidad:** ¿Cuántos respecto al tamaño del artefacto?
* **Detección temprana:** ¿Cuántos encontramos antes de etapas posteriores?

> **Advertencia:** Más defectos encontrados puede significar peor artefacto… o una revisión más eficaz.

---

## Una métrica sin contexto puede engañar

* **Equipo A:** 30 defectos detectados
* **Equipo B:** 8 defectos detectados

> **¿Cuál produjo el artefacto de mayor calidad?**
> * Falta conocer tamaño y complejidad.
> * Falta conocer severidad y origen.
> * Falta conocer esfuerzo de revisión y defectos que escaparon.

> **Conclusión:** Medir no elimina la necesidad de interpretar.

---

## Matriz de análisis de defectos

| Artefacto | Defecto | Origen | Propagación | Impacto | Evidencia |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Requisito | Regla ambigua | Análisis | Diseño $\rightarrow$ código | Bloqueo indebido | Casos + registros |

> La matriz obliga a separar el lugar donde vemos el problema del lugar donde realmente se originó.
> **Producto esperado:** clasificación argumentada, no una lista de errores.

---

## Caso aplicado · plataforma de inscripción

* **Requisito:** “El sistema evitará conflictos de horario”.
* **Diseño:** La disponibilidad se consulta una sola vez al iniciar.
* **Código:** Implementa exactamente esa estrategia.
* **Pruebas:** No modifican la disponibilidad durante la inscripción.
* **Producción:** Dos estudiantes reciben combinaciones inconsistentes bajo concurrencia.

> **Reto:** Identifica error, defecto, posible fallo, origen, propagación, impacto y evidencia.

---

## Discusión guiada · preguntas de alto nivel

* ¿Un defecto detectado en código necesariamente nació en código?
* ¿Puede una prueba correcta revelar un defecto originado en requisitos?
* ¿Ausencia de fallos observados implica ausencia de defectos?
* ¿Qué información necesitas para afirmar que una revisión fue eficaz?

> **Regla de discusión:** Toda afirmación debe incluir una razón o evidencia.

---

## Síntesis conceptual

$$\text{ERROR} \rightarrow \text{DEFECTO} \rightarrow \text{PROPAGACIÓN} \rightarrow \text{ACTIVACIÓN} \rightarrow \text{FALLO} \rightarrow \text{IMPACTO}$$

* **Origen:** requisito · diseño · código u otro artefacto.
* **Naturaleza:** funcional · interfaz · datos · rendimiento · seguridad · mantenibilidad.
* **Detección:** revisión temprana o prueba/operación.
* **Medición:** interpretar defectos con tamaño, severidad, fase y contexto.

> **Idea clave:** El lugar de detección no define por sí solo el origen del defecto.

---

## Comprobación rápida

Selecciona la afirmación más sólida:
* A. Todo defecto produce inmediatamente un fallo observable.
* B. El artefacto donde se detecta un defecto determina necesariamente su origen.
* **C. Un defecto puede originarse temprano, propagarse y manifestarse mucho después.** *(Afirmación más sólida)*
* D. Un mayor número de defectos detectados demuestra por sí solo menor calidad.

> Justifica tu elección utilizando los conceptos de origen y propagación.

---

## Cierre · Ticket de salida

1. Diferencia error, defecto y fallo en una sola cadena causal.
2. Da un ejemplo de defecto originado en requisitos y detectado en pruebas.
3. Explica por qué el lugar de detección puede diferir del origen.
4. ¿Por qué una revisión temprana puede reducir el impacto de un defecto?
5. Menciona una métrica de revisión y una limitación de interpretarla sola.

> **Entrega:** Respuesta individual, breve y argumentada.

---

## Próxima clase · métricas y efectividad de revisión

De clasificar defectos $\rightarrow$ a medir la capacidad de detectarlos:
* Densidad y distribución de defectos.
* Defectos detectados vs. defectos escapados.
* Efectividad de la revisión.
* Interpretación responsable de indicadores.

> **Pregunta de enlace:** ¿Cómo saber si una revisión fue realmente efectiva?