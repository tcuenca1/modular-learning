---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

[[Ingenieria de Software II]]

# Métricas de revisión del software

Defectos · densidad · eficacia · esfuerzo · interpretación

Semana 3 · Clase 2

¿Encontrar más defectos significa necesariamente revisar mejor?

[DOCENTE]  
[ID_OMITIDO]

Universidad Técnica de Machala · Tecnologías de la Información

> **Diagrama detectado:** Ilustración decorativa corporativa que incluye gráficos de barras con tendencia ascendente, listas con iconos de verificación, fragmentos de código de programación resaltados y lupas con marcas de aceptación sobre un fondo azul oscuro con líneas de flujo digitales.

---

## Objetivo e indicador de evaluación

### OBJETIVO
Aplicar métricas de revisión mediante datos de defectos y esfuerzo para la valoración de la eficacia del proceso de revisión.

### INDICADOR
Calcula [[métricas de revisión]] a partir de datos de defectos, tamaño y esfuerzo del proceso de [[software]].

---

## Ruta de aprendizaje

1. **Datos:** ¿Qué observamos?
2. **Defectos:** Número y distribución
3. **Densidad:** Defectos / tamaño
4. **Eficacia:** Capacidad de detección
5. **Esfuerzo:** Costo de revisión

**Meta:** calcular correctamente y evitar conclusiones engañosas.

---

## Caso detonante · dos equipos, resultados contradictorios

### EQUIPO A
- 28 defectos detectados
- 40 páginas revisadas
- 4 horas de revisión
- 2 revisores

### EQUIPO B
- 15 defectos detectados
- 15 páginas revisadas
- 2 horas de revisión
- 2 revisores

**Pregunta:** ¿qué equipo revisó mejor? ¿Qué información falta?

---

## ¿Qué es una métrica de revisión?

- **DATO:** Valor observado: 18 defectos.
- **MEDIDA:** Cuantificación directa de una propiedad.
- **MÉTRICA:** Relación o indicador construido con medidas.
- **INTERPRETACIÓN:** Significado del resultado dentro de un contexto.

*Medir produce números; evaluar exige convertirlos en evidencia para una decisión.*

---

## Número de defectos · útil, pero insuficiente

**Número de defectos detectados = conteo de hallazgos válidos**

- Permite observar volumen de hallazgos.
- Facilita comparar categorías dentro del mismo contexto.
- No considera tamaño del artefacto.
- No demuestra por sí solo eficacia ni calidad.

**Regla:** nunca interpretes el conteo aislado del contexto.

---

## Distribución de defectos

| Categoría | Cantidad | % del total | Pregunta que responde |
| :--- | :---: | :---: | :--- |
| Requisitos | 12 | 40 % | ¿Dónde se originan? |
| Diseño | 9 | 30 % | ¿Dónde se originan? |
| Código | 9 | 30 % | ¿Dónde se originan? |

**Interpretación:** la distribución señala concentración; no explica automáticamente la causa.

---

## Porcentaje de distribución · cálculo básico

$$\text{\% categoría} = (\text{defectos de la categoría} / \text{defectos totales}) \times 100$$

**Ejemplo: requisitos**  
$$(12 / 30) \times 100 = 40\%$$

**Comprueba**  
$$40\% + 30\% + 30\% = 100\%$$

**Pregunta:** ¿qué cambiaría si los 9 defectos de código fueran todos críticos?

---

## Densidad de defectos · normalizar por tamaño

$$\text{Densidad de defectos} = \text{número de defectos} / \text{tamaño del artefacto}$$

- **Requisitos:** defectos por página o requisito.
- **Código:** defectos por KLOC, si esa unidad es pertinente.
- **Modelos:** defectos por elemento o unidad definida.
- Siempre indicar la unidad utilizada.

La densidad permite comparar mejor que el conteo, pero solo entre contextos razonablemente comparables.

---

## Ejercicio · calcular densidad

### ARTEFACTO A
$$24 / 30 = 0,80$$
defectos por página

### ARTEFACTO B
$$18 / 15 = 1,20$$
defectos por página

*B tiene mayor densidad, aunque A tiene mayor número absoluto de defectos.*

---

## Eficacia de detección · ¿qué proporción encontramos?

$$\text{Eficacia de detección} = \text{detectos en revisión} / (\text{detectos} + \text{escapados}) \times 100$$

**Ejemplo: 24 detectados + 6 escapados** $\rightarrow$ $(24 / 30) \times 100 = 80\%$

- Mayor porcentaje sugiere mayor capacidad de detección en ese contexto.
- Debe interpretarse con tipo, severidad y fase de los defectos escapados.

*Un 95% con el 5% crítico escapado puede ser más riesgoso que un porcentaje menor con defectos leves.*

---

## Defectos escapados · la parte que la revisión no vio

- Se descubre en una etapa posterior a la revisión analizada.
- Permite identificar huecos en criterios, experiencia o cobertura.
- Debe rastrearse hacia su origen y naturaleza.
- Su severidad importa tanto como su cantidad.

**Pregunta:** ¿qué patrón de escapes justificaría cambiar una lista de chequeo?

---

## Esfuerzo de revisión

$$\text{Esfuerzo} = \text{suma de horas-persona dedicadas a la revisión}$$

$$\text{3 revisores} \times \text{2 h} = \text{6 horas-persona}$$

- Permite analizar costo de la actividad.
- Debe relacionarse con tamaño, defectos detectados y resultados posteriores.

*Más esfuerzo puede mejorar cobertura, pero también puede reflejar ineficiencia.*

---

## Rendimiento de la revisión · defectos por esfuerzo

$$\text{Rendimiento} = \text{defectos detectados} / \text{horas-persona}$$

$$\text{18 defectos} / \text{6 h-persona} = \text{3 defectos por h-persona}$$

- Ayuda a relacionar hallazgos y esfuerzo.
- No representa por sí sola profundidad, severidad ni eficacia global.

*No conviertas “más defectos por hora” en el objetivo de la revisión.*

---

## Velocidad de revisión · ¿cuánto artefacto se inspecciona?

$$\text{Velocidad} = \text{tamaño revisado} / \text{esfuerzo o tiempo definido}$$

$$\text{40 páginas} / \text{4 horas} = \text{10 páginas por hora}$$

- Una velocidad alta no demuestra mejor revisión.
- Debe contrastarse con densidad, escapes, severidad y objetivo.

*La velocidad es una variable de proceso, no una nota de calidad.*

---

## Comparación integrada · Equipo A vs. Equipo B

| Métrica | Equipo A | Equipo B | Lectura |
| :--- | :---: | :---: | :--- |
| Conteo | 28 | 15 | A detectó más. |
| Densidad | 0,70/pág. | 1,00/pág. | B detectó más por unidad. |
| Esfuerzo | 8 h-p | 4 h-p | A invirtió el doble. |
| Rendimiento | 3,50/h-p | 3,75/h-p | Resultados cercanos. |

**Conclusión provisional:** faltan defectos escapados, severidad y comparabilidad del artefacto.

---

## Cuando aparece información posterior, cambia la interpretación

### EQUIPO A
$$28 / (28 + 2)$$
$$= 93,3\%$$

### EQUIPO B
$$15 / (15 + 10)$$
$$= 60\%$$

*La interpretación cambia cuando incorporamos los defectos que escaparon.*

---

## Riesgos de interpretar métricas aisladamente

- Comparar tamaños o tipos de artefactos incompatibles.
- Ignorar severidad, origen y naturaleza de los defectos.
- Confundir productividad de detección con eficacia.
- Evaluar personas con una métrica diseñada para analizar procesos.
- Optimizar el número y perder de vista la calidad real.

**Principio:** las métricas apoyan decisiones; no sustituyen el juicio técnico.

---

## Caso de aplicación · revisión de requisitos

| Dato | Equipo X | Equipo Y |
| :--- | :---: | :---: |
| Tamaño | 25 páginas | 30 páginas |
| Detectados | 20 | 21 |
| Escapados | 5 | 3 |
| Esfuerzo | 5 h-persona | 7 h-persona |

*Calcula: densidad · eficacia · rendimiento. Luego decide qué revisión parece más efectiva y justifica.*

---

## Solución guiada del caso

| Métrica | Equipo X | Equipo Y | Interpretación |
| :--- | :---: | :---: | :--- |
| Densidad | 0,80/pág. | 0,70/pág. | X halló más por página. |
| Eficacia | 80% | 87,5% | Y dejó escapar menor proporción. |
| Rendimiento | 4/h-p | 3/h-p | X halló más por esfuerzo. |

*La decisión depende de qué atributo del proceso se desea valorar.*

---

## Cómo elaborar un reporte técnico de métricas

1. Contexto: artefacto, técnica, equipo y alcance.
2. Datos de entrada: defectos, tamaño, esfuerzo y escapes.
3. Fórmula y unidad de cada métrica.
4. Resultado calculado.
5. Interpretación técnica y limitaciones.
6. Decisión o acción de mejora propuesta.

*Un indicador es útil cuando conduce a una pregunta o decisión concreta.*

---

## Taller · auditoría de una revisión

- Calcular número y distribución de defectos.
- Calcular densidad de defectos.
- Calcular eficacia de detección.
- Calcular esfuerzo y rendimiento.
- Identificar una conclusión engañosa basada en una sola métrica.
- Emitir una decisión sustentada en al menos tres indicadores.

**Producto:** reporte de 1 página + defensa técnica de 3 minutos.

---

## Criterios de valoración del taller

- **Cálculo:** Fórmulas, sustitución y resultados correctos.
- **Unidades:** Expresa defectos/página, horas-persona, porcentaje, etc.
- **Interpretación:** Explica qué significa y qué no significa cada métrica.
- **Integración:** Contrasta varias métricas antes de decidir.
- **Argumentación:** Sustenta la conclusión con evidencia.

---

## Comprobación rápida

**Datos:** 18 detectados · 2 escapados · 12 páginas · 6 horas-persona

1. Calcula la eficacia de detección.
2. Calcula la densidad de defectos.
3. Calcula el rendimiento de la revisión.
4. Escribe una conclusión que NO exceda lo que los datos permiten afirmar.

**Resultados esperados:** 90% · 1,5 defectos/página · 3 defectos/h-persona.

---

## Cierre · interpretar antes de decidir

- El número de defectos muestra volumen, no eficacia por sí solo.
- La densidad normaliza por tamaño, pero necesita contexto.
- La eficacia incorpora defectos escapados conocidos.
- El esfuerzo permite analizar recursos invertidos.
- La interpretación integrada transforma métricas en decisiones.

**Idea final:** medir $\rightarrow$ contextualizar $\rightarrow$ comparar $\rightarrow$ interpretar $\rightarrow$ decidir.

---

## Ticket de salida

- Define densidad de defectos y escribe su fórmula.
- Explica qué representa la eficacia de detección.
- ¿Qué diferencia existe entre esfuerzo y rendimiento de revisión?
- ¿Por qué dos revisiones no deben compararse solo por número de defectos?
- Propón una decisión que requiera combinar al menos dos métricas.

**Entrega individual:** breve, calculable y argumentada.