---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

[[Ingenieria de Software II]]

# Métricas de revisión del software

Defectos · densidad · eficacia · esfuerzo · interpretación

**Semana 3 · Clase 2**

¿Encontrar más defectos significa necesariamente revisar mejor?

[DOCENTE]  
[ID_OMITIDO]

Universidad Técnica de Machala · Tecnologías de la Información  
01

---

> **Diagrama detectado:** Interfaz gráfica que muestra un tablero analítico con gráficos de barras, líneas de tendencia ascendente, listas con iconos de verificación y un escudo con un check (símbolo de seguridad o calidad). Representa el análisis de métricas y control de calidad en el desarrollo de software.

---

## Objetivo e indicador de evaluación

### OBJETIVO
Aplicar [[Métricas de revisión]] mediante datos de defectos y esfuerzo para la valoración de la [[Eficacia de revisión]] del proceso de revisión.

### INDICADOR
Calcula [[Métricas de revisión]] a partir de datos de defectos, tamaño y esfuerzo del proceso de [[Software]].

Universidad Técnica de Machala · Tecnologías de la Información  
02

---

## Ruta de aprendizaje

1. **Datos**  
   ¿Qué observamos?
2. **Defectos**  
   Número y distribución
3. **Densidad**  
   Defectos / tamaño
4. **Eficacia**  
   Capacidad de detección
5. **Esfuerzo**  
   Costo de revisión

**Meta:** calcular correctamente y evitar conclusiones engañosas.

Universidad Técnica de Machala · Tecnologías de la Información  
03

---

## Caso detonante · dos equipos, resultados contradictorios

### EQUIPO A
* 28 defectos detectados
* 40 páginas revisadas
* 4 horas de revisión
* 2 revisores

### EQUIPO B
* 15 defectos detectados
* 15 páginas revisadas
* 2 horas de revisión
* 2 revisores

**Pregunta:** ¿qué equipo revisó mejor? ¿Qué información falta?

Universidad Técnica de Machala · Tecnologías de la Información  
04

---

## ¿Qué es una métrica de revisión?

* **DATO:** Valor observado: 18 defectos.
* **MEDIDA:** Cuantificación directa de una propiedad.
* **MÉTRICA:** Relación o indicador construido con medidas.
* **INTERPRETACIÓN:** Significado del resultado dentro de un contexto.

*Medir produce números; evaluar exige convertirlos en evidencia para una decisión.*

Universidad Técnica de Machala · Tecnologías de la Información  
05

---

## Número de defectos · útil, pero insuficiente

**Número de defectos detectados = conteo de hallazgos válidos**

* Permite observar volumen de hallazgos.
* Facilita comparar categorías dentro del mismo contexto.
* No considera tamaño del artefacto.
* No demuestra por sí solo eficacia ni calidad.

**Regla:** nunca interpretes el conteo aislado del contexto.

Universidad Técnica de Machala · Tecnologías de la Información  
06

---

## Distribución de defectos

| Categoría | Cantidad | % del total | Pregunta que responde |
| :--- | :--- | :--- | :--- |
| Requisitos | 12 | 40 % | ¿Dónde se originan? |
| Diseño | 9 | 30 % | ¿Dónde se originan? |
| Código | 9 | 30 % | ¿Dónde se originan? |

**Interpretación:** la distribución señala concentración; no explica automáticamente la causa.

Universidad Técnica de Machala · Tecnologías de la Información  
07

---

## Porcentaje de distribución · cálculo básico

$$\text{\% categoría} = \left(\frac{\text{defectos de la categoría}}{\text{defectos totales}}\right) \times 100$$

**Ejemplo: requisitos**  
$$\left(\frac{12}{30}\right) \times 100 = 40\,\% $$

**Comprueba**  
$$40\,\% + 30\,\% + 30\,\% = 100\,\%$$

**Pregunta:** ¿qué cambiaría si los 9 defectos de código fueran todos críticos?

Universidad Técnica de Machala · Tecnologías de la Información  
08

---

## Densidad de defectos · normalizar por tamaño

$$\text{Densidad de defectos} = \frac{\text{número de defectos}}{\text{tamaño del artefacto}}$$

* **Requisitos:** defectos por página o requisito.
* **Código:** defectos por [[KLOC]], si esa unidad es pertinente.
* **Modelos:** defectos por elemento o unidad definida.
* Siempre indicar la unidad utilizada.

La densidad permite comparar mejor que el conteo, pero solo entre contextos razonablemente comparables.

Universidad Técnica de Machala · Tecnologías de la Información  
09

---

## Ejercicio · calcular densidad

### ARTEFACTO A
$$24 / 30 = 0,80$$  
**defectos por página**

### ARTEFACTO B
$$18 / 15 = 1,20$$  
**defectos por página**

**B tiene mayor densidad, aunque A tiene mayor número absoluto de defectos.**

Universidad Técnica de Machala · Tecnologías de la Información  
10

---

## Eficacia de detección · ¿qué proporción encontramos?

$$\text{Eficacia de detección} = \frac{\text{detectos en revisión}}{\text{detectos} + \text{escapados}} \times 100$$

**Ejemplo:** 24 detectados + 6 escapados $\rightarrow$ $\frac{24}{30} \times 100 = 80\,\%$

* Mayor porcentaje sugiere mayor capacidad de detección en ese contexto.
* Debe interpretarse con tipo, severidad y fase de los defectos escapados.

**Un 95 % con el 5 % crítico escapado puede ser más riesgoso que un porcentaje menor con defectos leves.**

Universidad Técnica de Machala · Tecnologías de la Información  
11

---

## Defectos escapados · la parte que la revisión no vio

* Se descubre en una etapa posterior a la revisión analizada.
* Permite identificar huecos en criterios, experiencia o cobertura.
* Debe rastrearse hacia su origen y naturaleza.
* Su severidad importa tanto como su cantidad.

**Pregunta:** ¿qué patrón de escapes justificaría cambiar una [[Lista de chequeo]]?

Universidad Técnica de Machala · Tecnologías de la Información  
12

---

## Esfuerzo de revisión

$$\text{Esfuerzo} = \text{suma de horas-persona dedicadas a la revisión}$$

$$3 \text{ revisores} \times 2 \text{ h} = \mathbf{6 \text{ horas-persona}}$$

* Permite analizar costo de la actividad.
* Debe relacionarse con tamaño, defectos detectados y resultados posteriores.

**Más esfuerzo puede mejorar cobertura, pero también puede reflejar ineficiencia.**

Universidad Técnica de Machala · Tecnologías de la Información  
13

---

## Rendimiento de la revisión · defectos por esfuerzo

$$\text{Rendimiento} = \frac{\text{defectos detectados}}{\text{horas-persona}}$$

$$18 \text{ defectos} / 6 \text{ h-persona} = \mathbf{3 \text{ defectos por h-persona}}$$

* Ayuda a relacionar hallazgos y esfuerzo.
* No representa por sí sola profundidad, severidad ni eficacia global.

**No conviertas “más defectos por hora” en el objetivo de la revisión.**

Universidad Técnica de Machala · Tecnologías de la Información  
14

---

## Velocidad de revisión · ¿cuánto artefacto se inspecciona?

$$\text{Velocidad} = \frac{\text{tamaño revisado}}{\text{esfuerzo o tiempo definido}}$$

$$40 \text{ páginas} / 4 \text{ horas} = \mathbf{10 \text{ páginas por hora}}$$

* Una velocidad alta no demuestra mejor revisión.
* Debe contrastarse con densidad, escapes, severidad y objetivo.

**La velocidad es una variable de proceso, no una nota de calidad.**

Universidad Técnica de Machala · Tecnologías de la Información  
15

---

## Comparación integrada · Equipo A vs. Equipo B

| Métrica | Equipo A | Equipo B | Lectura |
| :--- | :--- | :--- | :--- |
| Conteo | 28 | 15 | A detectó más. |
| Densidad | 0,70/pág. | 1,00/pág. | B detectó más por unidad. |
| Esfuerzo | 8 h-p | 4 h-p | A invirtió el doble. |
| Rendimiento | 3,50/h-p | 3,75/h-p | Resultados cercanos. |

**Conclusión provisional:** faltan defectos escapados, severidad y comparabilidad del artefacto.

Universidad Técnica de Machala · Tecnologías de la Información  
16

---

## Cuando aparece información posterior, cambia la interpretación

### EQUIPO A
$$28 / (28 + 2)$$  
$$= \mathbf{93,3\,\%}$$

### EQUIPO B
$$15 / (15 + 10)$$  
$$= \mathbf{60\,\%}$$

**La interpretación cambia cuando incorporamos los defectos que escaparon.**

Universidad Técnica de Machala · Tecnologías de la Información  
17

---

## Riesgos de interpretar métricas aisladamente

* Comparar tamaños o tipos de artefactos incompatibles.
* Ignorar severidad, origen y naturaleza de los defectos.
* Confundir productividad de detección con eficacia.
* Evaluar personas con una métrica diseñada para analizar procesos.
* Optimizar el número y perder de vista la calidad real.

**Principio:** las métricas apoyan decisiones; no sustituyen el juicio técnico.

Universidad Técnica de Machala · Tecnologías de la Información  
18

---

## Caso de aplicación · revisión de requisitos

| Dato | Equipo X | Equipo Y |
| :--- | :--- | :--- |
| Tamaño | 25 páginas | 30 páginas |
| Detectados | 20 | 21 |
| Escapados | 5 | 3 |
| Esfuerzo | 5 h-persona | 7 h-persona |

**Calcula:** densidad · eficacia · rendimiento. Luego decide qué revisión parece más efectiva y justifica.

Universidad Técnica de Machala · Tecnologías de la Información  
19

---

## Solución guiada del caso

| Métrica | Equipo X | Equipo Y | Interpretación |
| :--- | :--- | :--- | :--- |
| Densidad | 0,80/pág. | 0,70/pág. | X halló más por página. |
| Eficacia | 80 % | 87,5 % | Y dejó escapar menor proporción. |
| Rendimiento | 4/h-p | 3/h-p | X halló más por esfuerzo. |

**La decisión depende de qué atributo del proceso se desea valorar.**

Universidad Técnica de Machala · Tecnologías de la Información  
20

---

## Cómo elaborar un reporte técnico de métricas

* 1. Contexto: artefacto, técnica, equipo y alcance.
* 2. Datos de entrada: defectos, tamaño, esfuerzo y escapes.
* 3. Fórmula y unidad de cada métrica.
* 4. Resultado calculado.
* 5. Interpretación técnica y limitaciones.
* 6. Decisión o acción de mejora propuesta.

**Un indicador es útil cuando conduce a una pregunta o decisión concreta.**

Universidad Técnica de Machala · Tecnologías de la Información  
21

---

## Taller · auditoría de una revisión

* Calcular número y distribución de defectos.
* Calcular densidad de defectos.
* Calcular eficacia de detección.
* Calcular esfuerzo y rendimiento.
* Identificar una conclusión engañosa basada en una sola métrica.
* Emitir una decisión sustentada en al menos tres indicadores.

**Producto:** reporte de 1 página + defensa técnica de 3 minutos.

Universidad Técnica de Machala · Tecnologías de la Información  
22

---

## Criterios de valoración del taller

* **Cálculo:** Fórmulas, sustitución y resultados correctos.
* **Unidades:** Expresa defectos/página, horas-persona, porcentaje, etc.
* **Interpretación:** Explica qué significa y qué no significa cada métrica.
* **Integración:** Contrasta varias métricas antes de decidir.
* **Argumentación:** Sustenta la conclusión con evidencia.

Universidad Técnica de Machala · Tecnologías de la Información  
23

---

## Comprobación rápida

**Datos:** 18 detectados · 2 escapados · 12 páginas · 6 horas-persona

* 1. Calcula la eficacia de detección.
* 2. Calcula la densidad de defectos.
* 3. Calcula el rendimiento de la revisión.
* 4. Escribe una conclusión que NO exceda lo que los datos permiten afirmar.

**Resultados esperados:** 90 % · 1,5 defectos/página · 3 defectos/h-persona.

Universidad Técnica de Machala · Tecnologías de la Información  
24

---

## Cierre · interpretar antes de decidir

* El número de defectos muestra volumen, no eficacia por sí solo.
* La densidad normaliza por tamaño, pero necesita contexto.
* La eficacia incorpora defectos escapados conocidos.
* El esfuerzo permite analizar recursos invertidos.
* La interpretación integrada transforma métricas en decisiones.

**Idea final:** medir $\rightarrow$ contextualizar $\rightarrow$ comparar $\rightarrow$ interpretar $\rightarrow$ decidir.

Universidad Técnica de Machala · Tecnologías de la Información  
25

---

## Ticket de salida

* Define densidad de defectos y escribe su fórmula.
* Explica qué representa la eficacia de detección.
* ¿Qué diferencia existe entre esfuerzo y rendimiento de revisión?
* ¿Por qué dos revisiones no deben compararse solo por número de defectos?
* Propón una decisión que requiera combinar al menos dos métricas.

**Entrega individual:** breve, calculable y argumentada.

Universidad Técnica de Machala · Tecnologías de la Información  
26