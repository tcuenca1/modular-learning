---
materia: Ingenieria de Software II
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, diapositiva, ingesta_ia]
---

[[Ingenieria de Software II]]

---

## Módulo de [[Ingenieria de Software II]]

> **Imagen detectada:** Imagen de portada que muestra el título del módulo, iconos ilustrativos de análisis y modelado, diseño y arquitectura, implementación y pruebas, despliegue y mantenimiento, calidad y mejora continua. Se observa una laptop mostrando código de programación y un entorno de trabajo digital.

*   **[DOCENTE]:** [DOCENTE]
*   **Contacto:** [ID_OMITIDO]

---

## Encuadre de la asignatura

*   La comunicación profesor-estudiante únicamente por vía email: [ID_OMITIDO]
*   Las justificaciones de inasistencias, por vía email.
*   Tutorías: Presencial: Conforme Horario.
*   Asistencia al inicio de clase. (se pide Puntualidad)
*   Dispositivos de comunicación en modo silencio.
*   Participación activa durante la clase.
*   Respeto: Profesor-Estudiante, Estudiante-Profesor y entre Estudiantes.
*   En caso de existir suspensión de clases, se coordinará el reajuste entre Profesor-Estudiante
*   EVEA
*   Syllabus: Contenido. Sistema de Evaluación.
*   Grupos Clase – Equipos Proyectos.
*   Diagnóstico: Preguntas.

---

## Semana 1 · Clase 1
### Fundamentos y modelos de [[Calidad de Software]]

*   Concepto de calidad
*   Perspectivas
*   Proceso y producto
*   Requisitos

---

## Objetivo e indicador de evaluación

*   **OBJETIVO:** Analizar los fundamentos de la calidad del software mediante sus conceptos, perspectivas y relación con el proceso y producto software.
*   **INDICADOR:** Distingue criterios de calidad del software considerando las características del proceso, producto y requisitos establecidos.

> **Pregunta guía:** ¿Un software que funciona correctamente puede considerarse de alta calidad?

---

## Caso · «Funciona, pero…»

### Sistema de matrículas universitarias
*   Registra matrículas y genera comprobantes sin errores funcionales.
*   En horas pico tarda 25–40 segundos por operación.
*   En móvil algunos controles quedan fuera de pantalla.
*   Los usuarios nuevos necesitan ayuda para completar el proceso.
*   Una modificación pequeña obliga a cambiar varios módulos.

> **DESAFÍO:** ¿Es un software de calidad? Sustenta tu respuesta con al menos 3 criterios.

---

## ¿Qué se entiende por [[Calidad de Software]]?

La calidad no es una propiedad única: surge del grado en que un producto satisface necesidades, requisitos y expectativas dentro de un contexto de uso.

*   **Conformidad:** ¿Cumple lo especificado?
*   **Adecuación:** ¿Resuelve la necesidad real?
*   **Experiencia:** ¿Puede usarse eficazmente?
*   **Evolución:** ¿Puede mantenerse y cambiar?

> **Idea clave:** «funcionar» es necesario, pero no suficiente.

---

## Calidad desde diferentes perspectivas

*   **USUARIO:** Utilidad, facilidad, confianza, respuesta.
*   **CLIENTE:** Valor, cumplimiento, costo, riesgo.
*   **DESARROLLO:** Corrección, [[Mantenibilidad]], testabilidad.
*   **OPERACIÓN:** Disponibilidad, rendimiento, seguridad.

> Una misma solución puede ser «buena» desde una perspectiva y deficiente desde otra.

---

## Calidad del proceso $\neq$ calidad del producto

*   **CALIDAD DEL PROCESO:**
    *   Métodos y prácticas
    *   Revisiones y controles
    *   Trazabilidad
    *   Gestión de cambios
*   **CALIDAD DEL PRODUCTO:**
    *   Comportamiento observable
    *   Atributos de calidad
    *   Defectos y fallos
    *   Adecuación al uso

> Un buen proceso aumenta la probabilidad de obtener un buen producto, pero no lo garantiza por sí solo.

---

## Requisitos y calidad: la conexión crítica

La evaluación de calidad necesita una referencia: ¿contra qué afirmamos que algo es «bueno»?

1.  **Necesidad:** Problema o expectativa.
2.  **Requisito:** Condición verificable.
3.  **Criterio:** Cómo juzgar cumplimiento.
4.  **Evidencia:** Dato que sustenta la decisión.

> **Flujo:** Necesidad $\rightarrow$ requisito $\rightarrow$ criterio $\rightarrow$ evidencia $\rightarrow$ decisión de calidad

---

## Actividad colaborativa · Matriz de calidad

En equipos, vuelvan al caso de matrículas y completen:

| Perspectiva | Problema observado | Criterio de calidad | Evidencia necesaria |
| :--- | :--- | :--- | :--- |
| Usuario | | | |
| Cliente | | | |
| Desarrollo | | | |
| Operación | | | |

*   **Producto:** una conclusión de 3–4 líneas que responda si el sistema puede considerarse de calidad.

---

## Discusión · Calidad multidimensional

01. ¿Puede un producto cumplir todos sus requisitos funcionales y aun así tener baja calidad?
02. ¿Qué perspectiva debería prevalecer cuando existen criterios contradictorios?
03. ¿Qué ocurre si los requisitos de calidad nunca fueron explicitados?
04. ¿Cómo evitar decisiones de calidad basadas únicamente en opinión?

---

## Síntesis conceptual

*   **Perspectivas:** usuario · cliente · desarrollo · operación
*   **Proceso:** prácticas · control · trazabilidad
*   **Producto:** atributos · comportamiento · defectos
*   **Requisitos:** necesidades · criterios · evidencia

> La calidad emerge de la relación entre estos cuatro elementos.

---

## Comprobación rápida

Selecciona la afirmación más sólida:
*   A. Un software es de calidad cuando no presenta errores funcionales.
*   B. La calidad depende exclusivamente de la satisfacción del usuario.
*   **C. La calidad debe valorarse con criterios relacionados con producto, proceso, requisitos y contexto.**
*   D. Un proceso certificado garantiza automáticamente un producto de alta calidad.

> Justifica tu elección en una frase.

---

## ¿Funcionalidad = calidad? · descomponiendo el supuesto

*   **Funciona:** Ejecuta las funciones previstas.
*   **Pero es lento:** La respuesta afecta la experiencia y operación.
*   **Pero es difícil de usar:** El usuario puede no alcanzar su objetivo.
*   **Pero es difícil de cambiar:** El costo futuro y el riesgo aumentan.

> **Conclusión:** la corrección funcional es una dimensión, no la totalidad de la calidad.

---

## Calidad interna, externa y en uso

*   **INTERNA:** Estructura del producto (Acoplamiento · complejidad · facilidad de cambio).
*   **EXTERNA:** Comportamiento observable (Rendimiento · fallos · respuesta del sistema).
*   **EN USO:** Resultado para el usuario (Eficacia · satisfacción · logro de objetivos).

> Un sistema puede verse bien internamente y aun fracasar en el contexto de uso —o al contrario.

---

## De una expectativa vaga a un criterio verificable

| Expectativa | Requisito verificable | Evidencia |
| :--- | :--- | :--- |
| “Debe ser rápido” | 95 % de operaciones < 2 s | Prueba de carga |
| “Debe ser fácil” | $\ge$ 90 % completa sin ayuda | Prueba con usuarios |
| “Debe ser estable” | Disponibilidad $\ge$ 99,5 % | Registro operativo |

> La calidad necesita criterios observables y evidencia reproducible.

---

## El costo de descubrir tarde un problema de calidad

1. Requisito ambiguo $\rightarrow$ 2. Diseño condicionado $\rightarrow$ 3. Código implementado $\rightarrow$ 4. Despliegue $\rightarrow$ 5. Fallo percibido

> **Idea:** calidad también implica prevenir, no únicamente detectar defectos al final.

---

## Perspectivas en conflicto · decisión de calidad

*   Cliente: “La fecha comprometida no puede moverse”.
*   Usuario: “En móvil no puedo completar el proceso”.
*   Desarrollo: “El cambio rápido incrementará la deuda técnica”.
*   Operación: “La plataforma se degrada en horas pico”.

> ¿Quién tiene razón? $\rightarrow$ La decisión necesita propósito, riesgo, criterios y evidencia. No se trata de elegir una voz; se trata de justificar prioridades.

---

## Proceso y producto · cuatro escenarios posibles

*   **Buen proceso + buen producto:** Resultado sostenible y repetible.
*   **Buen proceso + producto débil:** Revisar requisitos, criterios o contexto.
*   **Proceso débil + buen producto:** Éxito frágil o difícil de reproducir.
*   **Proceso débil + producto débil:** Riesgo alto y retrabajo probable.

---

## Evidencia de calidad · ¿qué dato aceptarías?

*   “El sistema es rápido” $\rightarrow$ Tiempos de respuesta bajo carga definida.
*   “Es fácil de usar” $\rightarrow$ Tasa de éxito, tiempo de tarea, errores, observación.
*   “Es mantenible” $\rightarrow$ Impacto de cambios, complejidad, tiempo de modificación.
*   “Es confiable” $\rightarrow$ Fallos observados, disponibilidad, recuperación.

> Una afirmación de calidad sin evidencia es una hipótesis, no una conclusión.

---

## Mini-caso · sistema de pagos universitarios

*   Los pagos se registran correctamente cuando la operación finaliza.
*   En alta demanda, algunas respuestas superan 15 segundos.
*   Usuarios repiten el pago al no recibir confirmación inmediata.
*   Los registros de auditoría no permiten reconstruir todos los eventos.
*   Una actualización menor exige detener el servicio durante dos horas.

> **Reto:** formula 4 criterios y define qué evidencia necesitarías para cada uno.

---

## Taller ampliado · dictamen de calidad

*   1. Decisión provisional: ¿alta, aceptable, insuficiente o indeterminada?
*   2. Cuatro criterios: al menos uno por perspectiva relevante.
*   3. Evidencia: dato concreto que permitiría confirmar o rechazar cada criterio.
*   4. Riesgo: consecuencia de aceptar el sistema sin corregir.
*   5. Prioridad: qué atender primero y por qué.

> **Producto:** dictamen técnico de máximo 1 página + defensa oral de 3 minutos.

---

## Cierre ampliado · cinco ideas que deben quedar

*   Funcionar correctamente no agota el concepto de calidad.
*   La calidad cambia según perspectiva y contexto de uso.
*   Proceso y producto están relacionados, pero no son equivalentes.
*   Los requisitos convierten necesidades en referencias evaluables.
*   Una decisión de calidad exige criterios y evidencia.

> **Puente:** ¿cómo organizar estas dimensiones en modelos de calidad evaluables?