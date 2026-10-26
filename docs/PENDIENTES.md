# Pendientes

Trabajo acordado que queda para más adelante. Al terminar uno, se borra de aquí (el detalle
queda en el commit).

## Guía offline

- **Fase 2: cortes de parcial.** Definir por asignatura qué clases entran en cada parcial
  ("Parcial 1 hasta la clase 8") para generar la guía de todo un parcial. Los cronogramas
  actuales no traen esa información: el prompt `04_extraccion_silabo.md` descarta las clases
  de examen. Más adelante, que la extracción del sílabo capture también las evaluaciones.
- **Fase 2: reparto según el tiempo disponible.** Indicar cuánto tiempo hay ("4 horas") y
  ajustar la extensión de cada clase a ese presupuesto, en lugar de depender solo del número
  de clases.
- **Quitar el recuadro «Mis dudas» del PDF.** La guía se lee en el teléfono, no se imprime ni
  se escribe sobre ella; las dudas se anotan al confirmar la guía en la app.
- **Descarga directa del PDF.** Hoy se genera con «Guardar como PDF» del navegador, que
  funciona pero no se siente como una descarga. Generarlo en el servidor (por ejemplo con
  Playwright/Chromium detrás de un puerto `ExportadorPdfPort`) y servirlo como archivo.

## Frontend

- **Tests del frontend.** No hay ninguno. Empezar por la lógica pura de `lib/` (`clave`,
  `parsearFecha`, `clasesConFecha`, `materiasConCronograma`, `extensionPara`) y seguir con
  las vistas que tienen flujo propio (repaso, guía offline, confirmación).
- **Selector de tema claro/oscuro.** Ahora el tema sigue al sistema operativo
  (`prefers-color-scheme`). Para el despliegue, añadir un selector claro / oscuro / sistema
  que se recuerde por usuario.
