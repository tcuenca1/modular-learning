---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] - Evaluación de la calidad del producto software

**Universidad Técnica de Machala** · Tecnologías de la Información  
**Semana 2** · Clase 1  
**[DOCENTE]**  
[ID_OMITIDO]  

---

> **Diagrama detectado:** Interfaz gráfica institucional con fondo azul oscuro, elementos abstractos de redes de datos, engranajes en cubos 3D, una lupa sobre una marca de verificación y un escudo con un check que simboliza la ciberseguridad y la [[Calidad del Software]].

---

## 1. Objetivo e indicador de evaluación

* **OBJETIVO:** Analizar las características de calidad del producto software mediante criterios asociados con requisitos y atributos de calidad.
* **INDICADOR:** Relaciona requisitos, atributos, criterios y evidencias para la evaluación de la calidad de un producto software.

> *Pregunta guía:* ¿Cuál de los productos tiene mayor calidad y con qué evidencia podría demostrarse?

---

## 2. Caso inicial · Dos productos, dos perfiles

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

> *Pregunta:* ¿Cuál tiene mayor calidad? No respondas todavía: primero define qué criterio usarías.

---

## 3. Calidad del producto software

Evaluar un producto exige observar características relevantes y contrastarlas con requisitos, criterios definidos y evidencias objetivas.

1. **Requisitos:** Qué debe lograr
2. **Atributos:** Qué cualidad observar
3. **Criterios:** Cómo juzgar
4. **Evidencias:** Qué dato lo demuestra

---

## 4. Características y atributos de calidad

* **Adecuación funcional:** Cumplimiento de funciones
* **Rendimiento:** Tiempo y uso de recursos
* **Fiabilidad:** Continuidad y tolerancia a fallos
* **Usabilidad:** Eficacia y facilidad de uso
* **Seguridad:** Protección frente a riesgos
* **Mantenibilidad:** Facilidad de análisis y cambio

> **Nota:** Un atributo es útil para evaluar solo cuando puede vincularse con un criterio y una evidencia.

---

## 5. Requisitos funcionales y requisitos de calidad

* **REQUISITOS FUNCIONALES:** Describen servicios, comportamientos o funciones que el sistema debe proporcionar.
  * *Ejemplo:* «El sistema permitirá registrar una matrícula».
* **REQUISITOS DE CALIDAD:** Establecen condiciones o niveles esperados sobre cómo debe comportarse el producto.
  * *Ejemplo:* «La operación deberá completarse en $\le 3$ segundos».

> **Principio:** Cumplir la función no demuestra, por sí solo, que el producto posea la calidad requerida.

---

## 6. Del requisito al criterio de evaluación

1. **Requisito:** Respuesta $\le 3$ s
2. **Atributo:** [[Rendimiento]]
3. **Criterio:** $95\%$ de operaciones $\le 3$ s
4. **Evidencia:** Prueba de rendimiento

> **Principio:** La evaluación se fortalece cuando cada juicio puede rastrearse hasta una evidencia.

---

## 7. Evidencias de calidad · ¿Qué puede demostrar un juicio?

* **Pruebas:** Resultados reproducibles
* **Métricas:** Valores cuantitativos
* **Registros:** Fallos e incidencias
* **Revisiones:** Hallazgos documentados

> *Ejemplo comparativo:* «Parece rápido» es una opinión. «El $97\%$ de las transacciones responde en menos de 3 segundos» es evidencia utilizable.

---

## 8. Cadena de evaluación de la calidad

1. **REQUISITO:** Qué se espera
2. **ATRIBUTO:** Qué cualidad representa
3. **CRITERIO:** Qué condición permite juzgar
4. **EVIDENCIA:** Qué demuestra el resultado
5. **DECISIÓN:** Qué concluimos

> **Principio:** Sin trazabilidad entre estos elementos, una evaluación puede ser subjetiva o difícil de defender.

---

## 9. Actividad · Matriz requisito–atributo–criterio–evidencia

| Requisito | Atributo | Criterio | Evidencia | Conclusión |
| :--- | :--- | :--- | :--- | :--- |
| Respuesta rápida | | | | |
| Facilidad de uso | | | | |
| Disponibilidad | | | | |

> **Producto:** Una conclusión sustentada sobre la calidad del producto a partir de la matriz.

---

## 10. Volvamos al caso inicial

Ahora responde con evidencia:
1. ¿Qué requisitos de calidad están implícitos en el caso?
2. ¿Qué atributos se ven comprometidos en cada producto?
3. ¿Qué criterios usarías para compararlos?
4. ¿Qué evidencia adicional necesitarías antes de decidir?

> **Regla:** La respuesta final debe evitar «me parece» y utilizar criterios verificables.

---

## 11. Síntesis · evaluar no es opinar

* **Requisito:** Define expectativa
* **Atributo:** Representa calidad
* **Criterio:** Permite juzgar
* **Evidencia:** Sustenta la decisión

> **Conclusión técnica:** Una evaluación de calidad defendible conecta lo que se exige con lo que se observa y con la evidencia que lo demuestra.

---

## 12. Comprobación rápida

Un requisito indica: *«El sistema debe estar disponible el $99,9\%$ del mes»*.

* ¿Cuál es el atributo de calidad relacionado?
* ¿Cuál sería el criterio de evaluación?
* ¿Qué evidencia necesitarías?
* ¿Qué conclusión podrías emitir si la disponibilidad real fuera $98,7\%$?

> **Instrucción:** Responde siguiendo la cadena: `requisito` $\rightarrow$ `atributo` $\rightarrow$ `criterio` $\rightarrow$ `evidencia` $\rightarrow$ `decisión`.

---

## 13. Cierre · conclusión técnica

**Completa:**
> «No puedo afirmar que un producto tiene calidad únicamente porque __________. Para evaluarlo necesito relacionar __________ con __________ y demostrarlo mediante __________.»

* **Criterio de salida:** La respuesta debe incluir requisitos, atributos, criterios y evidencias.
* **Siguiente clase:** Criterios y evidencias para profundizar la evaluación del producto software.

---

## 14. Calidad del producto · una visión multidimensional

Un producto puede cumplir unas características y fallar en otras:

* **Funcionalidad:** ¿Hace lo requerido?
* **Rendimiento:** ¿Lo hace a tiempo?
* **Fiabilidad:** ¿Continúa funcionando?
* **Usabilidad:** ¿Puede utilizarse eficazmente?
* **Seguridad:** ¿Protege lo necesario?
* **Mantenibilidad:** ¿Puede modificarse?

---

## 15. Característica, atributo y métrica · no son lo mismo

* **Característica:** Dimensión general *(Ej.: Rendimiento)*
* **Atributo:** Propiedad observable *(Ej.: Tiempo de respuesta)*
* **Métrica:** Forma de cuantificar *(Ej.: Segundos/operación)*

> **Principio:** Distinguir estos niveles evita evaluar conceptos abstractos sin una forma concreta de observación.

---

## 16. ¿Qué hace que un criterio sea evaluable?

* **CRITERIO DÉBIL:** *«El sistema debe responder rápidamente.»*
  * No define umbral.
  * No indica condiciones.
  * Permite interpretaciones distintas.
* **CRITERIO VERIFICABLE:** *«El $95\%$ de operaciones deberá responder en $\le 3$ s bajo carga nominal.»*
  * Define proporción.
  * Define umbral.
  * Define contexto.

---

## 17. La importancia del atributo depende del contexto

* **Banca:** Seguridad · [[Fiabilidad]]
* **Videojuego casual:** Usabilidad · [[Rendimiento]]
* **Sistema clínico:** [[Fiabilidad]] · seguridad
* **Portal informativo:** Usabilidad · compatibilidad

> **Principio:** Evaluar calidad también implica priorizar las consecuencias del incumplimiento.

---

## 18. Evidencia pertinente, suficiente y reproducible

* **Pertinente:** Responde al atributo evaluado
* **Suficiente:** Sostiene la conclusión
* **Reproducible:** Puede obtenerse nuevamente
* **Trazable:** Se vincula con requisito y criterio

> **Principio:** Una evidencia existente no necesariamente es evidencia suficiente.

---

## 19. Mini caso · sistema de matrícula universitaria

### EVIDENCIAS DISPONIBLES
* $100\%$ de funciones críticas ejecutan correctamente.
* $92\%$ de transacciones responden en $\le 3$ s.
* Disponibilidad mensual: $99,4\%$.
* $18\%$ de usuarios nuevos requiere ayuda.
* $0$ incidentes de pérdida de datos registrados.

### RETO
Construye 3 relaciones: `requisito` $\rightarrow$ `atributo` $\rightarrow$ `criterio` $\rightarrow$ `evidencia`.  
Después emite una conclusión provisional.

---

## 20. Errores frecuentes al evaluar calidad

1. Confundir cumplimiento funcional con calidad total.
2. Elegir métricas porque son fáciles de obtener.
3. Definir criterios después de conocer el resultado.
4. Usar evidencia que no corresponde al atributo.
5. Emitir una conclusión global ocultando fallos críticos.

---

## 21. Taller ampliado · matriz de trazabilidad de calidad

**Producto a evaluar:** Sistema de matrícula universitaria

* Defina 4 requisitos de calidad verificables.
* Asocie cada requisito con una característica o atributo.
* Establezca el criterio antes de observar el resultado.
* Determine qué evidencia debería recolectarse.
* Emita una conclusión por requisito y una conclusión global condicionada.

> **Producto esperado:** Matriz completa + defensa técnica de 3 minutos.

---

## 22. Criterios para valorar la actividad

* **Trazabilidad:** Requisito, atributo, criterio y evidencia están conectados.
* **Verificabilidad:** Los criterios permiten decidir cumplimiento.
* **Pertinencia:** La evidencia realmente demuestra el atributo.
* **Argumentación:** La conclusión se deriva de resultados y riesgos.

> **Nota:** La calidad de la respuesta se evalúa por coherencia, no por cantidad de texto.

---

## 23. Cierre ampliado · de la percepción a la evidencia

Completa la cadena con un ejemplo propio:  
`REQUISITO` $\rightarrow$ `ATRIBUTO` $\rightarrow$ `CRITERIO` $\rightarrow$ `EVIDENCIA` $\rightarrow$ `DECISIÓN`

> ¿Qué elemento, si estuviera mal definido, haría más débil tu conclusión y por qué?

* **Puente a Clase 2:** Valoración cualitativa y cuantitativa sustentada en evidencias.