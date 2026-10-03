---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] - Evaluación de la calidad del producto software

---

## 1. Información General y Portada

**Universidad:** Universidad Técnica de Machala  
**Facultad / Unidad:** Tecnologías de la Información  
**Asignatura:** [[Ingenieria de Software II]]  
**Semana:** 2 · Clase 1  
**Tema:** Evaluación de la calidad del producto software (Requisitos, atributos, criterios y evidencias de calidad)  
**Docente:** [DOCENTE] ([ID_OMITIDO])  

> **Diagrama detectado:** Ilustración de fondo de temática tecnológica con tonos azules oscuros, un escudo digital con un visto bueno (Check), gráficos de barras estadísticos, fragmentos de código de programación y una lupa examinando datos.

---

## 2. Objetivo e Indicador de Evaluación

* **OBJETIVO:** Analizar las características de calidad del producto software mediante criterios asociados con requisitos y atributos de calidad.
* **INDICADOR:** Relaciona requisitos, atributos, criterios y evidencias para la evaluación de la [[Calidad del Software]].
* **Pregunta guía:** ¿Cuál de los productos tiene mayor calidad y con qué evidencia podría demostrarse?

---

## 3. Caso Inicial · Dos productos, dos perfiles

### PRODUCTO A
* Cumple todas las funciones solicitadas.
* Respuesta promedio: 8 segundos.
* Interfaz confusa para usuarios nuevos.
* Pocos fallos registrados.

### PRODUCTO B
* Cumple todas las funciones solicitadas.
* Respuesta promedio: 2 segundos.
* Interfaz fácil de aprender.
* Mayor número de fallos intermitentes.

> **Pregunta de análisis:** ¿Cuál tiene mayor calidad? No respondas todavía: primero define qué criterio usarías.

---

## 4. Calidad del Producto Software

Evaluar un producto exige observar características relevantes y contrastarlas con requisitos, criterios definidos y evidencias objetivas.

1. **Requisitos:** Qué debe lograr.
2. **Atributos:** Qué cualidad observar.
3. **Criterios:** Cómo juzgar.
4. **Evidencias:** Qué dato lo demuestra.

---

## 5. Características y Atributos de Calidad

* **Adecuación funcional:** Cumplimiento de funciones.
* **Rendimiento:** Tiempo y uso de recursos.
* **Fiabilidad:** Continuidad y tolerancia a fallos.
* **Usabilidad:** Eficacia y facilidad de uso.
* **Seguridad:** Protección frente a riesgos.
* **Mantenibilidad:** Facilidad de análisis y cambio.

> *Nota:* Un atributo es útil para evaluar solo cuando puede vincularse con un criterio y una evidencia.

---

## 6. Requisitos Funcionales y Requisitos de Calidad

* **REQUISITOS FUNCIONALES:** Describen servicios, comportamientos o funciones que el sistema debe proporcionar.
  * *Ejemplo:* «El sistema permitirá registrar una matrícula».
* **REQUISITOS DE CALIDAD:** Establecen condiciones o niveles esperados sobre cómo debe comportarse el producto.
  * *Ejemplo:* «La operación deberá completarse en $\le 3$ segundos».

> *Principio clave:* Cumplir la función no demuestra, por sí solo, que el producto posea la calidad requerida.

---

## 7. Del Requisito al Criterio de Evaluación

1. **Requisito:** Respuesta $\le 3\text{ s}$
2. **Atributo:** [[Rendimiento]]
3. **Criterio:** $95\text{ \%}$ de operaciones $\le 3\text{ s}$
4. **Evidencia:** [[Prueba de rendimiento]]

> *Principio clave:* La evaluación se fortalece cuando cada juicio puede rastrearse hasta una evidencia.

---

## 8. Evidencias de Calidad · ¿Qué puede demostrar un juicio?

* **Pruebas:** Resultados reproducibles.
* **Métricas:** Valores cuantitativos.
* **Registros:** Fallos e incidencias.
* **Revisiones:** Hallazgos documentados.

> *Ejemplo comparativo:* «Parece rápido» es una opinión. «El $97\text{ \%}$ de las transacciones responde en menos de $3$ segundos» es evidencia utilizable.

---

## 9. Cadena de Evaluación de la Calidad

* **REQUISITO:** Qué se espera.
* **ATRIBUTO:** Qué cualidad representa.
* **CRITERIO:** Qué condición permite juzgar.
* **EVIDENCIA:** Qué demuestra el resultado.
* **DECISIÓN:** Qué concluimos.

> *Principio clave:* Sin trazabilidad entre estos elementos, una evaluación puede ser subjetiva o difícil de defender.

---

## 10. Actividad · Matriz Requisito – Atributo – Criterio – Evidencia

| Requisito | Atributo | Criterio | Evidencia | Conclusión |
| :--- | :--- | :--- | :--- | :--- |
| Respuesta rápida | | | | |
| Facilidad de uso | | | | |
| Disponibilidad | | | | |

> **Objetivo de la actividad:** Generar una conclusión sustentada sobre la calidad del producto a partir de la matriz.

---

## 11. Volvamos al Caso Inicial

Ahora responde con evidencia:
1. ¿Qué requisitos de calidad están implícitos en el caso?
2. ¿Qué atributos se ven comprometidos en cada producto?
3. ¿Qué criterios usarías para compararlos?
4. ¿Qué evidencia adicional necesitarías antes de decidir?

> *Regla:* La respuesta final debe evitar «me parece» y utilizar criterios verificables.

---

## 12. Síntesis · Evaluar no es opinar

* **Requisito:** Define expectativa.
* **Atributo:** Representa calidad.
* **Criterio:** Permite juzgar.
* **Evidencia:** Sustenta la decisión.

> *Conclusión:* Una evaluación de calidad defendible conecta lo que se exige con lo que se observa y con la evidencia que lo demuestra.

---

## 13. Comprobación Rápida

* **Premisa:** Un requisito indica: «El sistema debe estar disponible el $99,9\text{ \%}$ del mes».
  * ¿Cuál es el atributo de calidad relacionado?
  * ¿Cuál sería el criterio de evaluación?
  * ¿Qué evidencia necesitarías?
  * ¿Qué conclusión podrías emitir si la disponibilidad real fuera $98,7\text{ \%}$?

> *Formato de respuesta:* Sigue la cadena: $\text{requisito} \to \text{atributo} \to \text{criterio} \to \text{evidencia} \to \text{decisión}$.

---

## 14. Cierre · Conclusión Técnica

**Completa la frase:**
> «No puedo afirmar que un producto tiene calidad únicamente porque __________. Para evaluarlo necesito relacionar __________ con __________ y demostrarlo mediante __________.»

* **Criterio de salida:** La respuesta debe incluir requisitos, atributos, criterios y evidencias.
* **Siguiente clase:** Criterios y evidencias para profundizar la evaluación del producto software.

---

## 15. Calidad del Producto · Una Visión Multidimensional

Un producto puede cumplir unas características y fallar en otras:
* **Funcionalidad:** ¿Hace lo requerido?
* **Rendimiento:** ¿Lo hace a tiempo?
* **Fiabilidad:** ¿Continúa funcionando?
* **Usabilidad:** ¿Puede utilizarse eficazmente?
* **Seguridad:** ¿Protege lo necesario?
* **Mantenibilidad:** ¿Puede modificarse?

---

## 16. Característica, Atributo y Métrica · No son lo mismo

* **Característica:** Dimensión general (Ej.: Rendimiento).
* **Atributo:** Propiedad observable (Ej.: Tiempo de respuesta).
* **Métrica:** Forma de cuantificar (Ej.: Segundos/operación).

> *Principio:* Distinguir estos niveles evita evaluar conceptos abstractos sin una forma concreta de observación.

---

## 17. ¿Qué hace que un criterio sea evaluable?

* **CRITERIO DÉBIL:**
  * *Ejemplo:* «El sistema debe responder rápidamente.»
  * Características: No define umbral, no indica condiciones, permite interpretaciones distintas.
* **CRITERIO VERIFICABLE:**
  * *Ejemplo:* «El $95\text{ \%}$ de operaciones deberá responder en $\le 3\text{ s}$ bajo carga nominal.»
  * Características: Define proporción, define umbral, define contexto.

---

## 18. La importancia del atributo depende del contexto

* **Banca:** [[Seguridad]] · [[Fiabilidad]]
* **Videojuego casual:** [[Usabilidad]] · [[Rendimiento]]
* **Sistema clínico:** [[Fiabilidad]] · [[Seguridad]]
* **Portal informativo:** [[Usabilidad]] · [[Compatibilidad]]

> *Principio:* Evaluar calidad también implica priorizar las consecuencias del incumplimiento.

---

## 19. Evidencia Pertinente, Suficiente y Reproducible

* **Pertinente:** Responde al atributo evaluado.
* **Suficiente:** Sostiene la conclusión.
* **Reproducible:** Puede obtenerse nuevamente.
* **Trazable:** Se vincula con requisito y criterio.

> *Nota:* Una evidencia existente no necesariamente es evidencia suficiente.

---

## 20. Mini Caso · Sistema de Matrícula Universitaria

### EVIDENCIAS DISPONIBLES:
* $100\text{ \%}$ de funciones críticas ejecutan correctamente.
* $92\text{ \%}$ de transacciones responden en $\le 3\text{ s}$.
* Disponibilidad mensual: $99,4\text{ \%}$.
* $18\text{ \%}$ de usuarios nuevos requiere ayuda.
* $0$ incidentes de pérdida de datos registrados.

### RETO:
Construye $3$ relaciones: $\text{requisito} \to \text{atributo} \to \text{criterio} \to \text{evidencia}$. Después emite una conclusión provisional.

---

## 21. Errores Frecuentes al Evaluar Calidad

1. Confundir cumplimiento funcional con calidad total.
2. Elegir métricas porque son fáciles de obtener.
3. Definir criterios después de conocer el resultado.
4. Usar evidencia que no corresponde al atributo.
5. Emitir una conclusión global ocultando fallos críticos.

---

## 22. Taller Ampliado · Matriz de Trazabilidad de Calidad

* **Producto a evaluar:** Sistema de matrícula universitaria.
* **Instrucciones:**
  1. Defina $4$ requisitos de calidad verificables.
  2. Asocie cada requisito con una característica o atributo.
  3. Establezca el criterio antes de observar el resultado.
  4. Determine qué evidencia debería recolectarse.
  5. Emita una conclusión por requisito y una conclusión global condicionada.
* **Producto esperado:** Matriz completa + defensa técnica de 3 minutos.

---

## 23. Criterios para Valorar la Actividad

* **Trazabilidad:** Requisito, atributo, criterio y evidencia están conectados.
* **Verificabilidad:** Los criterios permiten decidir cumplimiento.
* **Pertinencia:** La evidencia realmente demuestra el atributo.
* **Argumentación:** La conclusión se deriva de resultados y riesgos.

> *Nota:* La calidad de la respuesta se evalúa por coherencia, no por cantidad de texto.

---

## 24. Cierre Ampliado · De la Percepción a la Evidencia

* **Actividad:** Completa la cadena con un ejemplo propio:
  $$\text{REQUISITO} \to \text{ATRIBUTO} \to \text{CRITERIO} \to \text{EVIDENCIA} \to \text{DECISIÓN}$$
* **Pregunta de reflexión:** ¿Qué elemento, si estuviera mal definido, haría más débil tu conclusión y por qué?
* **Puente a Clase 2:** Valoración cualitativa y cuantitativa sustentada en evidencias.