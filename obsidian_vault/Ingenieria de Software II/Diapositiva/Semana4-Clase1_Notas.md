---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-10-01
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

# [[Ingenieria de Software II]] · Unidad I
## Revisiones informales y técnicas formales del software
Revisión de software · revisión por pares · walkthrough · inspección · revisiones técnicas formales

**Universidad Técnica de Machala · Tecnologías de la Información**
**Semana 4 · Clase 1**

> **Pregunta orientadora:** ¿Todos los artefactos deberían revisarse utilizando el mismo procedimiento?

---

### Objetivo e indicador de evaluación

**Objetivo:**
Analizar las técnicas de [[Revisión de software]] mediante sus características, procedimientos y niveles de formalidad.

**Indicador:**
Diferencia técnicas de revisión del software según su formalidad, procedimiento, participantes y contexto de aplicación.

---

### Escenario: solo hay tiempo para revisar una vez

* **Documento de requisitos:** 35 páginas y varios cambios recientes.
* **Arquitectura:** se modificó la integración con un sistema externo.
* **Código:** módulo de pagos con una corrección urgente.
* **Equipo:** 5 personas; solo 6 horas disponibles para revisión.
* **Riesgo:** un defecto puede afectar transacciones reales.

---

### ¿Qué es una revisión de software?

> **Revisar** = examinar sistemáticamente un artefacto para detectar problemas y mejorar su calidad.

* Puede realizarse sobre artefactos no ejecutables.
* Busca defectos antes de que se propaguen.
* Puede variar desde una lectura informal hasta una inspección estructurada.
* Su procedimiento depende del riesgo, artefacto, equipo y propósito.

---

### Objetivos de una revisión

| Objetivo | Descripción |
| :--- | :--- |
| **Detectar** | Defectos, omisiones e inconsistencias. |
| **Verificar** | Cumplimiento de criterios y estándares. |
| **Comprender** | Construir entendimiento compartido. |
| **Prevenir** | Evitar propagación a etapas posteriores. |
| **Aprender** | Retroalimentar prácticas y criterios. |

---

### El continuo de formalidad

> INFORMAL ────────────────────────────────────→ FORMAL

1. **Conversación:** Poca estructura.
2. **Pares:** Revisión focalizada.
3. **Walkthrough:** Autor guía.
4. **Inspección:** Roles y proceso definidos.

> *La técnica debe ser proporcional al riesgo, complejidad y propósito.*

---

### Revisión informal

* **Fortalezas:**
  * Rápida de organizar
  * Bajo costo
  * Flexible
  * Retroalimentación inmediata
* **Limitaciones:**
  * Dependencia del revisor
  * Poca trazabilidad
  * Cobertura variable
  * Difícil de repetir

---

### Revisión por pares

* **Participantes:** autor + uno o más colegas técnicamente pertinentes.
* **Objeto:** requisitos, diseño, código, pruebas o documentación.
* **Procedimiento:** lectura, comentarios, discusión y corrección posterior.
* **Formalidad:** variable; puede ir desde comentarios rápidos hasta listas de chequeo.
* **Resultado:** defectos identificados y recomendaciones.

---

### Walkthrough · el autor conduce el recorrido

> Autor ➔ guía el recorrido ➔ participantes preguntan ➔ se registran hallazgos

* El autor explica estructura, decisiones o flujo.
* Los participantes siguen escenarios o ejemplos.
* Se plantean preguntas y alternativas.
* Puede ser útil para transferir conocimiento además de detectar defectos.

---

### Ejemplo de walkthrough · requisito de autenticación

> **Requisito:** “El sistema permitirá acceso seguro mediante usuario y contraseña.”

* **Escenario 1:** credenciales válidas.
* **Escenario 2:** cinco intentos fallidos consecutivos.
* **Escenario 3:** usuario solicita recuperación de contraseña.
* **Escenario 4:** sesión permanece abierta en un equipo compartido.

---

### Inspección · revisión estructurada

> **1. Planificación** ➔ **2. Preparación** ➔ **3. Examen** ➔ **4. Registro** ➔ **5. Corrección** ➔ **6. Seguimiento**

* **La estructura** busca aumentar disciplina, trazabilidad y cobertura de la revisión.
* **Costo:** mayor preparación y coordinación. 
* **Beneficio potencial:** mayor control en artefactos críticos.

---

### Roles en una inspección

* **AUTOR:** Produce y aclara el artefacto.
* **MODERADOR:** Coordina y mantiene el procedimiento.
* **REVISORES:** Buscan defectos con criterios definidos.
* **REGISTRADOR:** Documenta hallazgos y decisiones.

---

### Preparación individual · donde comienza la inspección

* Comprender propósito y alcance del artefacto.
* Aplicar lista de chequeo o criterios.
* Registrar ubicación y naturaleza del posible defecto.
* Evitar corregir extensamente durante la detección.
* Llegar a la reunión con hallazgos concretos.

---

### Lista de chequeo · apoyo, no sustituto del juicio

* ¿El requisito es inequívoco y verificable?
* ¿Existen condiciones límite no especificadas?
* ¿Las interfaces tienen entradas, salidas y errores definidos?
* ¿Las decisiones de diseño respetan restricciones conocidas?
* ¿El artefacto contiene inconsistencias con otros documentos?

---

### Revisión técnica formal (RTF)

* Objetivo y alcance definidos.
* Participantes seleccionados por competencia.
* Preparación previa.
* Criterios o estándares de referencia.
* Hallazgos documentados.
* Seguimiento de acciones.

---

### Comparación de técnicas

| Técnica | Formalidad | Quién conduce | Preparación | Registro | Uso típico |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Informal** | Baja | Variable | Baja | Opcional | Feedback rápido |
| **Pares** | Baja-media | Par/autor | Variable | Variable | Artefactos cotidianos |
| **Walkthrough** | Media | Autor | Media | Recomendable | Comprensión + defectos |
| **Inspección** | Alta | Moderador | Alta | Formal | Artefactos críticos |
| **RTF** | Media-alta | Definido | Alta | Formal | Control técnico |

---

### No existe una técnica universalmente mejor

* **RIESGO:** ¿Qué ocurre si el defecto escapa?
* **COMPLEJIDAD:** ¿Cuánto razonamiento requiere el artefacto?
* **MADUREZ:** ¿Qué experiencia tiene el equipo y el artefacto?
* **COSTO:** ¿Qué esfuerzo de coordinación es razonable?

---

### Matriz técnica de selección

| Artefacto | Riesgo | Técnica | Formalidad | Participantes | Evidencia |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Requisito crítico** | Alto | Inspección | Alta | Autor + moderador + revisores | Registro de defectos |
| **Código menor** | Bajo | Pares | Baja-media | Autor + par | Comentarios/cambios |
| **Diseño nuevo** | Medio-alto | Walkthrough | Media | Autor + equipo | Hallazgos + dudas |

---

### Casos de Estudio

#### Caso 1 · requisito regulatorio crítico
> “Toda modificación de una transacción deberá quedar registrada con usuario, fecha, valor anterior y valor nuevo.”
* **Impacto de un defecto:** alto.
* **Interesados:** desarrollo, seguridad, auditoría.
* **Artefactos relacionados:** requisitos, diseño de datos y código.

#### Caso 2 · cambio pequeño en interfaz
* **Cambio:** etiqueta y ubicación de un botón secundario.
* **No modifica** reglas de negocio ni datos.
* **Impacto potencial:** limitado y fácilmente reversible.
* **Tiempo disponible:** 30 minutos antes de integrar.

#### Caso 3 · arquitectura con integración externa
* **Nueva interfaz** con un sistema legado.
* **Cambios** en autenticación y transformación de datos.
* **Participan** arquitectura, seguridad, base de datos y operación.
* **El error** puede propagarse a varios componentes.

---

### Taller · comité de revisión

1. Identificar artefacto, riesgo y objetivo de revisión.
2. Seleccionar técnica y nivel de formalidad.
3. Definir participantes y roles.
4. Describir procedimiento en 4–6 pasos.
5. Definir qué evidencia quedará registrada.
6. Justificar por qué otra técnica sería menos adecuada.

---

### Errores frecuentes al organizar revisiones

* Revisar sin objetivo ni alcance definido.
* Llegar a la reunión sin preparación.
* Confundir detección de defectos con sesión de rediseño.
* Convertir la revisión en evaluación personal del autor.
* No registrar hallazgos.
* No verificar posteriormente las correcciones.

> *Una buena técnica mal ejecutada puede producir una revisión ineficaz.*

---

### Comprobación rápida

* A. Corrección menor de código entre dos desarrolladores.
* B. Documento crítico con requisitos regulatorios.
* C. Arquitectura nueva que el autor debe explicar al equipo.
* D. Cambio de bajo riesgo que necesita retroalimentación inmediata.

---

### Conclusión

* **Informal** ➔ retroalimentación rápida y bajo costo.
* **Pares** ➔ contraste técnico entre colegas.
* **Walkthrough** ➔ comprensión guiada y discusión del artefacto.
* **Inspección** ➔ procedimiento estructurado, roles y registro.
* **Revisión técnica formal** ➔ control sistemático y trazabilidad.