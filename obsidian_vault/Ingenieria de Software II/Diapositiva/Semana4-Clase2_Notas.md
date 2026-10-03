---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-10-01
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] · Unidad I
## Ejecución de una [[Revisión Técnica Formal]]

> **Diagrama detectado:** Iconografía institucional de seguridad de software con un escudo con marca de verificación en la esquina superior derecha, esquemas de bases de datos/redes estilizados en segundo plano, paneles de edición de código y gráficos de barras de progreso con marcas de verificación.

**Planificación** · **Roles** · **Criterios** · **Listas de comprobación** · **Registro** · **Resultados** · **Seguimiento**

**Semana 4 · Clase 2**

¿Cuántos defectos pueden demostrarse técnicamente y cuáles son únicamente opiniones?

[DOCENTE]  
[ID_OMITIDO]

Universidad Técnica de Machala · Tecnologías de la Información

---

## Objetivo e indicador de evaluación

### OBJETIVO
Ejecutar una [[Revisión Técnica Formal]] mediante [[Roles]], [[Criterios]] y evidencias aplicados a un [[Artefacto de Software]].

### INDICADOR
Ejecuta una [[Revisión Técnica Formal]] mediante [[Criterios]], [[Roles]], [[Listas de Comprobación]] y evidencias sobre un [[Artefacto de Software]].

---

## Artefacto deliberadamente defectuoso

### Especificación de requisito — Sistema de compras
> *"El sistema deberá procesar rápidamente las compras de todos los usuarios y, cuando sea necesario, solicitar una validación adicional. Si el pago falla varias veces, se bloqueará temporalmente la cuenta."*

- No corrijas todavía.
- Marca únicamente aquello que puedas justificar como defecto o riesgo verificable.

---

## Defecto demostrado vs. opinión

### OPINIÓN
- “Está mal redactado.”
- “Yo lo haría diferente.”
- “No me parece claro.”

### HALLAZGO TÉCNICO
- Ubicación exacta
- Criterio incumplido
- Evidencia observable
- Impacto o riesgo

---

## Planificación de la revisión

- **Propósito:** ¿qué queremos detectar o verificar?
- **Alcance:** ¿qué parte del artefacto se revisará?
- **Participantes:** ¿qué competencias necesitamos?
- **Criterios:** ¿contra qué se evaluará el artefacto?
- **Tiempo:** preparación, reunión y consolidación.
- **Salida:** ¿qué evidencia debe quedar al finalizar?

---

## Roles y responsabilidades

### AUTOR
Aclara el artefacto; no dirige la evaluación.

### MODERADOR
Conduce el procedimiento y mantiene el foco.

### REVISOR
Busca defectos aplicando [[Criterios]] definidos.

### REGISTRADOR
Documenta hallazgos, estado y evidencia.

> **Pregunta clave:** ¿qué riesgo existe si el autor también actúa como moderador?

---

## Criterios de entrada

- Artefacto identificado y versión conocida.
- Alcance de revisión definido.
- Información de contexto disponible.
- [[Criterios]] o [[Lista de Comprobación]] preparados.
- Participantes y roles asignados.
- Tiempo suficiente para preparación y reunión.

---

## Construcción de una lista de comprobación

- [ ] ¿El requisito utiliza términos inequívocos y medibles?
- [ ] ¿Define condiciones, entradas, salidas y excepciones necesarias?
- [ ] ¿Puede diseñarse una prueba objetiva para verificarlo?
- [ ] ¿Es consistente con otros requisitos y restricciones?
- [ ] ¿Se identifica su origen o necesidad relacionada?

---

## Preparación individual

Antes de la reunión, cada revisor trabaja de forma independiente.

- Aplicar la [[Lista de Comprobación]].
- Marcar ubicación exacta del posible defecto.
- Relacionar el hallazgo con un criterio.
- Evitar diseñar la solución durante esta fase.

*Preparación individual $\neq$ reunión anticipada.*

---

## Formato mínimo de un hallazgo

| ID | Ubicación | Criterio | Descripción | Evidencia/impacto | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| D-01 | Línea 1 | Claridad | Uso de “rápidamente” sin umbral medible. | No permite construir criterio de aceptación objetivo. | Abierto |

> Observe que el registro no dice “redacción mala”: identifica el término, el criterio incumplido y su consecuencia.

---

## Simulación · hallazgos iniciales

- “rápidamente” $\rightarrow$ criterio de desempeño no cuantificado.
- “todos los usuarios” $\rightarrow$ alcance potencialmente indeterminado.
- “cuando sea necesario” $\rightarrow$ condición de activación no especificada.
- “varias veces” $\rightarrow$ umbral de bloqueo indefinido.
- “temporalmente” $\rightarrow$ duración del bloqueo no definida.

---

## Reunión de revisión · propósito

- Presentar hallazgos preparados.
- Eliminar duplicados.
- Solicitar aclaraciones breves.
- Determinar si existe evidencia suficiente.
- Registrar defectos aceptados y observaciones pendientes.
- Posponer la solución detallada para la fase de corrección.

*Detectar $\neq$ corregir. Mezclar ambas actividades reduce el foco de la revisión.*

---

## Protocolo de la reunión

1. **Abrir** (Objetivo y alcance)
2. **Presentar** (Hallazgos)
3. **Contrastar** (Criterio y evidencia)
4. **Registrar** (Defectos válidos)
5. **Cerrar** (Acciones y responsables)

> *El moderador protege el proceso; el criterio protege la objetividad.*

---

## ¿Qué hacer cuando no hay consenso?

- Revisar el criterio aplicable.
- Solicitar evidencia adicional.
- Separar defecto de preferencia de diseño.
- Registrar como pendiente si no puede resolverse.
- Escalar cuando dependa de una decisión externa.

---

## Clasificación de resultados

- **DEFECTO:** Existe criterio incumplido y evidencia.
- **OBSERVACIÓN:** Requiere aclaración o mejora, sin defecto plenamente demostrado.
- **DUPLICADO:** Ya está representado por otro hallazgo.
- **DESCARTADO:** Existe incumplimiento sustentable (sin fundamento).

> El registro debe conservar por qué un hallazgo cambió de estado.

---

## Consolidación de defectos

| Hallazgo | Revisor | Resultado | ID consolidado |
| :--- | :--- | :--- | :--- |
| “rápidamente” no es medible | R1 | Defecto | D-01 |
| No existe tiempo máximo | R2 | Duplicado | D-01 |
| No me gusta “usuarios” | R3 | Descartado | — |

---

## Resultados de la revisión

- Número de defectos confirmados.
- Distribución por criterio o tipo.
- Observaciones pendientes.
- Hallazgos descartados o duplicados.
- Esfuerzo empleado.
- Responsables y fecha de corrección/seguimiento.

---

## Criterios de salida

- Todos los hallazgos fueron clasificados.
- Los defectos confirmados tienen identificación y evidencia.
- Duplicados fueron consolidados.
- Acciones de corrección tienen responsable.
- Pendientes y decisiones externas quedaron registradas.
- Se definió mecanismo de seguimiento.

---

## Corrección y seguimiento

$$\text{Defecto} \rightarrow \text{acción} \rightarrow \text{corrección} \rightarrow \text{verificación} \rightarrow \text{cierre}$$

- Registrar quién corrige y cuándo.
- Conservar vínculo entre defecto y cambio.
- Verificar el resultado.
- Reabrir si la evidencia de cierre es insuficiente.

---

## Registro de seguimiento

| ID | Defecto | Responsable | Estado | Evidencia de cierre |
| :--- | :--- | :--- | :--- | :--- |
| D-01 | “rápidamente” sin umbral medible | Autor | Verificado | Requisito actualizado: $\le 2\text{ s}$ |

> La evidencia de cierre debe ser verificable por alguien distinto del responsable de la corrección.

---

## Simulación formal · organización del equipo

- 1 autor del artefacto.
- 1 moderador.
- 1 registrador.
- 1–2 revisores.
- Lista de comprobación común.
- Registro de revisión obligatorio.

> **Restricción:** ningún defecto puede registrarse sin criterio y evidencia.

---

## Producto del equipo · registro de revisión

- Identificación del artefacto y versión.
- Objetivo, alcance y criterios de entrada.
- Roles y participantes.
- Lista de comprobación aplicada.
- Hallazgos individuales y defectos consolidados.
- Resultado final, acciones y seguimiento.

> El documento es la evidencia de que la revisión fue ejecutada, no solamente discutida.

---

## Rúbrica rápida de ejecución

- **Planificación:** Define alcance, criterios y condiciones.
- **Roles:** Cumple responsabilidades durante la revisión.
- **Criterios:** Aplica lista de comprobación de forma consistente.
- **Evidencias:** Sustenta técnicamente los defectos.
- **Registro:** Consolida resultados y seguimiento.

---

## ¿Fue eficaz la revisión?

- ¿Los criterios facilitaron la detección?
- ¿Los roles redujeron o aumentaron la discusión improductiva?
- ¿Cuántos hallazgos resultaron duplicados o descartados?
- ¿Qué tipo de defecto fue más difícil de identificar?
- ¿Qué modificarías en la lista de comprobación?

> La eficacia del proceso se mejora aprendiendo de sus resultados.

---

## Errores que invalidan una revisión formal

- Asignar roles pero no respetar sus responsabilidades.
- Registrar opiniones como defectos.
- Corregir mientras todavía se intenta detectar.
- Contar duplicados como defectos distintos.
- Finalizar sin responsables ni seguimiento.
- Modificar el artefacto sin conservar trazabilidad.

> Formalidad no es llenar formatos: es hacer el proceso verificable y repetible.

---

## Conclusión del proceso

$$\text{PLANIFICAR} \rightarrow \text{PREPARAR} \rightarrow \text{REVISAR} \rightarrow \text{CONSOLIDAR} \rightarrow \text{CORREGIR} \rightarrow \text{VERIFICAR}$$

- Roles definen responsabilidades.
- Criterios orientan la detección.
- Listas de comprobación operacionalizan criterios.
- Registros convierten hallazgos en evidencia.
- Seguimiento demuestra el cierre.

> Una [[Revisión Técnica Formal]] debe dejar rastros verificables de lo que ocurrió.

---

## Comprobación rápida

- ¿Qué diferencia un defecto demostrado de una opinión?
- ¿Qué función cumple la preparación individual?
- ¿Por qué se consolidan los hallazgos?
- ¿Cuándo puede cerrarse la reunión de revisión?
- ¿Qué evidencia permite cerrar definitivamente un defecto?