---
materia: Ingenieria de Software II
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, actividad, ingesta_ia]
---

# [[Ingenieria de Software II]] - Actividad CAA-3

## Información General

- **Universidad:** [[Universidad Técnica de Machala]]
- **Facultad:** [[Facultad de Ingeniería Civil]]
- **Carrera:** [[Tecnologías de la Información]]
- **Asignatura:** [[Ingeniería de Software II]] - 2026– E2
- **Actividad:** CAA - 3
- **Fecha:** 26/09/2026
- **Semestre:** Sexto
- **Paralelo:** A
- **Unidad I:** Calidad del Software y Técnicas de Revisión
- **Tema:** Defectos y métricas de revisión del software

---

## Problema

Análisis forense de defectos. A partir de un caso de software, identificar errores, defectos y fallos; establecer su origen, propagación e impacto. Calcular métricas de revisión considerando cantidad y densidad de defectos, tasa de detección, eficacia de eliminación y esfuerzo de revisión. Interpretar técnicamente los resultados.

**Debe entregar:**
- Matriz defecto–origen–propagación–impacto
- Hoja de cálculo de métricas
- Reporte técnico de interpretación

---

## Objetivo

Aplicar [[métricas de revisión]] mediante datos de defectos y esfuerzo para la valoración de la eficacia del proceso de revisión.

---

## Tipo de Actividad

- **Lugar:** Extraclase
- **Alcance:** Grupal
- **Forma:** Resolución de problemas, ejercicios

---

## Roles y Responsabilidades de los Participantes en la Tarea

| Nombre Estudiante | Rol | Descripción |
| :--- | :--- | :--- |
| [ESTUDIANTE 1] | Estudiantes | Realizadores de la actividad |
| [ESTUDIANTE 2] | Estudiantes | Realizadores de la actividad |
| [ESTUDIANTE 3] | Estudiantes | Realizadores de la actividad |
| [ESTUDIANTE 4] | Estudiantes | Realizadores de la actividad |

---

## Análisis Forense de Defectos

### Caso de software: Fallo del software del Ariane 5, Vuelo 501

El vuelo 501 del Ariane 5 presentó un fallo relacionado con el software del sistema de referencia inercial. El sistema utilizaba un módulo de software desarrollado originalmente para el Ariane 4, pero determinadas condiciones de operación del Ariane 5 no habían sido consideradas adecuadamente. Durante el vuelo, una variable alcanzó un valor que excedió el rango permitido para el tipo de dato utilizado en una conversión. Esto produjo un desbordamiento numérico y posteriormente una excepción que no fue manejada correctamente por el software.

Como consecuencia, el sistema de referencia inercial dejó de funcionar correctamente y transmitió información errónea al sistema de control. Esto provocó que el sistema de control reaccionara de forma incorrecta y se perdiera el control del vehículo, ocasionando la destrucción del Ariane 5 y de su carga.

El caso permite realizar un análisis forense del defecto considerando su origen, propagación, fallo e impacto, relacionando el problema inicial del software con las consecuencias observadas durante la ejecución del sistema [1], [2].

### Matriz Defecto–Origen–Propagación–Impacto

| Componente | Descripción Técnica en el Ariane 5 |
| :--- | :--- |
| **1. Error Humano (Origen)** | Reutilización directa de código legado (Ariane 4) sin actualizar las especificaciones ni reevaluar el rango operacional para las mayores aceleraciones horizontales del Ariane 5. |
| **2. Defecto (Bug en el código/diseño)** | Conversión de un valor de punto flotante de 64 bits (`float64`) a un entero con signo de 16 bits (`int16`) sin incluir validación ni protección contra desbordamiento (`overflow`). |
| **3. Propagación** | El valor superó los 32,768 (límite de 16 bits), provocando un error de hardware (`operand error`). La computadora de respaldo, que ejecutaba exactamente el mismo software con el mismo defecto, falló de forma idéntica un milisegundo después. |
| **4. Fallo Operacional (Failure)** | El Sistema de Referencia Inercial (SRI) se deshabilitó y envió datos de diagnóstico erróneos (interpretados como datos de vuelo válidos) al ordenador de a bordo (*On-Board Computer*). |
| **5. Impacto Final** | El ordenador corrigió la trayectoria basándose en datos falsos, provocando un ángulo de ataque extremo (más de 20 grados), sobreesfuerzo estructural, separación de los propulsores y auto-destrucción del cohete a 37 segundos del lanzamiento. |

---

## Hoja de Cálculo de Métricas

| Parámetro | Valor | Unidad |
| :--- | :---: | :--- |
| Tamaño del subsistema (documento de diseño) | 15 | páginas |
| Tamaño del subsistema (código) | 0,1 | [[KLOC]] |
| Defectos críticos (diseño heredado) | 1 | defectos |
| Defectos menores / secundarios | 2 | defectos |
| Total de defectos identificados post-mortem ($D$) | 3 | defectos |
| Esfuerzo de revisión ($ER$) | 12 | horas-hombre |
| Defectos encontrados en revisión ($E$) | 0 | defectos |
| Defectos encontrados en pruebas/producción ($P$) | 3 | defectos |

| Métrica | Resultado | Unidad | Formula aplicada |
| :--- | :---: | :--- | :--- |
| [[Densidad de defectos]] (por página de diseño) | 0,2 | defectos/página | $D \div \text{páginas} = 3 \div 15$ |
| [[Densidad de defectos]] (por [[KLOC]]) | 30 | defectos/[[KLOC]] | $D \div \text{KLOC} = 3 \div 0.1$ |
| Tasa de detección en revisión ([[DDR]]) | 0 | defectos/hora | $E \div ER = 0 \div 12$ |
| Eficiencia en la eliminación de defectos ([[DRE]]) | 0 | % | $E \div (E + P) = 0 \div (0 + 3)$ |

---

## Reporte Técnico de Interpretación

El colapso del Ariane 5 se originó al reutilizar software del Ariane 4 sin adaptar sus especificaciones a las mayores aceleraciones del nuevo cohete. Una conversión de datos de 64 a 16 bits, carente de validación, generó un desbordamiento numérico que apagó el sistema de referencia inercial. Al fallar, este componente envió datos de error que el ordenador de a bordo interpretó como desviaciones reales de la trayectoria, ejecutando una corrección extrema que destruyó el vehículo. La redundancia fue inútil, ya que la computadora de respaldo colapsó un milisegundo después por ejecutar exactamente el mismo código defectuoso.

Las métricas del proyecto evidencian un grave fallo en el control de calidad previo al lanzamiento. Presentar una [[densidad de defectos]] de 30 defectos por [[KLOC]] en un sistema de misión crítica demuestra que el componente heredado no fue auditado adecuadamente. El esfuerzo de revisión fue ineficaz y la eficiencia en la eliminación de defectos fue del 0%, lo que indica que las pruebas solo replicaron escenarios del Ariane 4 en lugar de someter el software a las exigencias físicas reales del Ariane 5.

Para evitar futuros colapsos, la industria no debe asumir como confiable ningún software heredado sin antes recertificarlo bajo las nuevas condiciones operativas. Es imperativo implementar un manejo de excepciones robusto para evitar que un error aritmético local bloquee el sistema central o transmita diagnósticos que puedan confundirse con telemetría. Asimismo, los sistemas críticos deben emplear redundancia diversificada, utilizando arquitecturas de software desarrolladas de forma independiente para que un mismo error lógico no neutralice también a los sistemas de respaldo.

---

## Referencias Bibliográficas

[1] G. Le Lann, “An analysis of the Ariane 5 flight 501 failure—A system engineering perspective,” in *Proc. 1997 Workshop on Engineering of Computer-Based Systems (ECBS '97)*, Monterey, CA, USA, 1997, doi: 10.1109/ECBS.1997.581900. Disponible en: [ResearchGate Publication](https://www.researchgate.net/publication/3687017_An_analysis_of_the_Ariane_5_flight_501_failure-a_system_engineeringperspective)

[2] Proyecto [[SWEBOK]], “Caso Ariane 5,” 2002. Disponible en: [INAOEP Document](https://ccc.inaoep.mx/~balderas/documents/misc/ariane-5-swebook-2002.pdf)