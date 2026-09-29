---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

[[Ingenieria de Software II]]

---

## 1. Presentación del Módulo

> **Diagrama detectado:** Ilustración de bienvenida con iconos representativos de las fases de desarrollo de software: Análisis y modelado, Diseño y arquitectura, Implementación y pruebas, y Despliegue y mantenimiento, acompañados de una laptop mostrando código y herramientas de desarrollo.

* **Módulo:** [[Ingenieria de Software II]]
* **Objetivo:** Construir soluciones robustas, escalables y de alta calidad aplicando diseño, arquitectura y buenas prácticas.
* **Temas principales:** 
  * [[UML]] (Diagramas)
  * [[Patrones de Diseño]]
  * [[Arquitectura de Software]]
  * Pruebas y Calidad
  * [[DevOps]]
  * Despliegue
* **Docente:** [DOCENTE]
* **Contacto:** [ID_OMITIDO]

---

## 2. Encuadre de la Asignatura

* La comunicación profesor-estudiante únicamente por vía email: [ID_OMITIDO]
* Las justificaciones de inasistencias, por vía email.
* **Tutorías:** Presencial: Conforme Horario.
* Asistencia al inicio de clase (se pide puntualidad).
* Dispositivos de comunicación en modo silencio.
* Participación activa durante la clase.
* Respeto: Profesor-Estudiante, Estudiante-Profesor y entre Estudiantes.
* En caso de existir suspensión de clases, se coordinará el reajuste entre Profesor-Estudiante.
* **EVEA** (Entorno Virtual de Aprendizaje)
* **Syllabus:** Contenido y Sistema de Evaluación.
* Grupos Clase – Equipos Proyectos.
* Diagnóstico: Preguntas.

---

## 3. Semana 1 · Clase 1: Fundamentos y modelos de calidad del software

* **Conceptos clave:** Concepto de [[Calidad de Software]], perspectivas, proceso y producto, requisitos.
* **Docente:** [DOCENTE]
* **Institución:** Universidad Técnica de Machala · Tecnologías de la Información

---

## 4. Objetivo e indicador de evaluación

* **Objetivo:** Analizar los fundamentos de la [[Calidad de Software]] mediante sus conceptos, perspectivas y relación con el proceso y producto software.
* **Indicador:** Distingue criterios de calidad del software considerando las características del proceso, producto y requisitos establecidos.
* **Pregunta guía:** ¿Un software que funciona correctamente puede considerarse de alta calidad?

---

## 5. Caso · «Funciona, pero…»

### Sistema de matrículas universitarias
* Registra matrículas y genera comprobantes sin errores funcionales.
* En horas pico tarda 25–40 segundos por operación.
* En móvil algunos controles quedan fuera de pantalla.
* Los usuarios nuevos necesitan ayuda para completar el proceso.
* Una modificación pequeña obliga a cambiar varios módulos.

> **Desafío:** ¿Es un software de calidad? Sustenta tu respuesta con al menos 3 criterios.

---

## 6. ¿Qué se entiende por [[Calidad de Software]]?

La calidad no es una propiedad única: surge del grado en que un producto satisface necesidades, requisitos y expectativas dentro de un contexto de uso.

1. **Conformidad:** ¿Cumple lo especificado?
2. **Adecuación:** ¿Resuelve la necesidad real?
3. **Experiencia:** ¿Puede usarse eficazmente?
4. **Evolución:** ¿Puede mantenerse y cambiar?

> **Idea clave:** «Funcionar» es necesario, pero no suficiente.

---

## 7. Calidad desde diferentes perspectivas

* **Usuario:** Utilidad, facilidad, confianza, respuesta.
* **Cliente:** Valor, cumplimiento, costo, riesgo.
* **Desarrollo:** Corrección, mantenibilidad, [[Testabilidad]].
* **Operación:** Disponibilidad, rendimiento, seguridad.

> Una misma solución puede ser «buena» desde una perspectiva y deficiente desde otra.

---

## 8. Calidad del proceso $\neq$ calidad del producto

* **Calidad del Proceso:**
  * Métodos y prácticas
  * Revisiones y controles
  * Trazabilidad
  * Gestión de cambios
* **Calidad del Producto:**
  * Comportamiento observable
  * Atributos de calidad
  * Defectos y fallos
  * Adecuación al uso

> Un buen proceso aumenta la probabilidad de obtener un buen producto, pero no lo garantiza por sí solo.

---

## 9. Requisitos y calidad: la conexión crítica

La evaluación de calidad necesita una referencia: ¿contra qué afirmamos que algo es «bueno»?

$$\text{Necesidad} \rightarrow \text{Requisito} \rightarrow \text{Criterio} \rightarrow \text{Evidencia} \rightarrow \text{Decisión de calidad}$$

* **Necesidad:** Problema o expectativa.
* **Requisito:** Condición verificable.
* **Criterio:** Cómo juzgar cumplimiento.
* **Evidencia:** Dato que sustenta la decisión.

---

## 10. Actividad colaborativa · Matriz de calidad

En equipos, vuelvan al caso de matrículas y completen la siguiente matriz:

| Perspectiva | Problema observado | Criterio de calidad | Evidencia necesaria |
| :--- | :--- | :--- | :--- |
| **Usuario** | | | |
| **Cliente** | | | |
| **Desarrollo** | | | |
| **Operación** | | | |

* **Producto:** una conclusión de 3–4 líneas que responda si el sistema puede considerarse de calidad.

---

## 11. Discusión · Calidad multidimensional

1. ¿Puede un producto cumplir todos sus requisitos funcionales y aun así tener baja calidad?
2. ¿Qué perspectiva debería prevalecer cuando existen criterios contradictorios?
3. ¿Qué ocurre si los requisitos de calidad nunca fueron explicitados?
4. ¿Cómo evitar decisiones de calidad basadas únicamente en opinión?

---

## 12. Síntesis conceptual

> **Diagrama detectado:** Mapa conceptual central que interconecta **Calidad del Software** con cuatro pilares fundamentales: **Perspectivas** (usuario, cliente, desarrollo, operación), **Proceso** (prácticas, control, trazabilidad), **Producto** (atributos, comportamiento, defectos) y **Requisitos** (necesidades, criterios, evidencia).

* La calidad emerge de la relación entre estos cuatro elementos.

---

## 13. Comprobación rápida

Selecciona la afirmación más sólida:
* A. Un software es de calidad cuando no presenta errores funcionales.
* B. La calidad depende exclusivamente de la satisfacción del usuario.
* **C. La calidad debe valorarse con criterios relacionados con producto, proceso, requisitos y contexto.** *(Respuesta sólida)*
* D. Un proceso certificado garantiza automáticamente un producto de alta calidad.

> *Justifica tu elección en una frase.*

---

## 14. ¿Funcionalidad = calidad? · Descomponiendo el supuesto

* **Funciona:** Ejecuta las funciones previstas.
* **Pero es lento:** La respuesta afecta la experiencia y operación.
* **Pero es difícil de usar:** El usuario puede no alcanzar su objetivo.
* **Pero es difícil de cambiar:** El costo futuro y el riesgo aumentan.

> **Conclusión:** La corrección funcional es una dimensión, no la totalidad de la calidad.

---

## 15. Calidad interna, externa y en uso

* **Interna:** Estructura del producto (Acoplamiento, complejidad, facilidad de cambio).
* **Externa:** Comportamiento observable (Rendimiento, fallos, respuesta del sistema).
* **En Uso:** Resultado para el usuario (Eficacia, satisfacción, logro de objetivos).

> Un sistema puede verse bien internamente y aun fracasar en el contexto de uso —o al contrario.

---

## 16. De una expectativa vaga a un criterio verificable

| Expectativa | Requisito verificable | Evidencia |
| :--- | :--- | :--- |
| “Debe ser rápido” | 95 % de operaciones < 2 s | Prueba de carga |
| “Debe ser fácil” | $\ge 90$ % completa sin ayuda | Prueba con usuarios |
| “Debe ser estable” | Disponibilidad $\ge 99,5$ % | Registro operativo |

> La calidad necesita criterios observables y evidencia reproducible.

---

## 17. El costo de descubrir tarde un problema de calidad

$$\text{1. Requisito ambiguo} \rightarrow \text{2. Diseño condicionado} \rightarrow \text{3. Código implementado} \rightarrow \text{4. Despliegue} \rightarrow \text{5. Fallo percibido}$$

> **Idea:** Calidad también implica prevenir, no únicamente detectar defectos al final.

---

## 18. Perspectivas en conflicto · Decisión de calidad

* **Cliente:** “La fecha comprometida no puede moverse”.
* **Usuario:** “En móvil no puedo completar el proceso”.
* **Desarrollo:** “El cambio rápido incrementará la [[Deuda Técnica]]”.
* **Operación:** “La plataforma se degrada en horas pico”.

> ¿Quién tiene razón? $\rightarrow$ La decisión necesita propósito, riesgo, criterios y evidencia. No se trata de elegir una voz; se trata de justificar prioridades.

---

## 19. Proceso y producto · Cuatro escenarios posibles

| | **Producto Favorable** | **Producto Débil** |
| :--- | :--- | :--- |
| **Buen Proceso** | Buen proceso + buen producto<br>*(Resultado sostenible y repetible)* | Buen proceso + producto débil<br>*(Revisar requisitos, criterios o contexto)* |
| **Proceso Débil** | Proceso débil + buen producto<br>*(Éxito frágil o difícil de reproducir)* | Proceso débil + producto débil<br>*(Riesgo alto y retrabajo probable)* |

---

## 20. Evidencia de calidad · ¿Qué dato aceptarías?

* “El sistema es rápido” $\rightarrow$ Tiempos de respuesta bajo carga definida.
* “Es fácil de usar” $\rightarrow$ Tasa de éxito, tiempo de tarea, errores, observación.
* “Es mantenible” $\rightarrow$ Impacto de cambios, complejidad, tiempo de modificación.
* “Es confiable” $\rightarrow$ Fallos observados, disponibilidad, recuperación.

> Una afirmación de calidad sin evidencia es una hipótesis, no una conclusión.

---

## 21. Mini-caso · Sistema de pagos universitarios

* Los pagos se registran correctamente cuando la operación finaliza.
* En alta demanda, algunas respuestas superan 15 segundos.
* Usuarios repiten el pago al no recibir confirmación inmediata.
* Los registros de auditoría no permiten reconstruir todos los eventos.
* Una actualización menor exige detener el servicio durante dos horas.

> **Reto:** Formula 4 criterios y define qué evidencia necesitarías para cada uno.

---

## 22. Taller ampliado · Dictamen de calidad

1. **Decisión provisional:** ¿alta, aceptable, insuficiente o indeterminada?
2. **Cuatro criterios:** al menos uno por perspectiva relevante.
3. **Evidencia:** dato concreto que permitiría confirmar o rechazar cada criterio.
4. **Riesgo:** consecuencia de aceptar el sistema sin corregir.
5. **Prioridad:** qué atender primero y por qué.

> **Producto:** Dictamen técnico de máximo 1 página + defensa oral de 3 minutos.

---

## 23. Cierre ampliado · Cinco ideas que deben quedar

* Funcionar correctamente no agota el concepto de calidad.
* La calidad cambia según perspectiva y contexto de uso.
* Proceso y producto están relacionados, pero no son equivalentes.
* Los requisitos convierten necesidades en referencias evaluables.
* Una decisión de calidad exige criterios y evidencia.

> **Puente:** ¿Cómo organizar estas dimensiones en modelos de calidad evaluables?