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
- **Descarga directa del PDF.** Hoy se genera con «Guardar como PDF» del navegador, que
  funciona pero no se siente como una descarga. Generarlo en el servidor (por ejemplo con
  Playwright/Chromium detrás de un puerto `ExportadorPdfPort`) y servirlo como archivo.

## Despliegue (Render + Neon)

- **Recarga lenta en la nube.** Con el servidor despierto, una recarga normal tarda 2–3 s en
  mostrar todo. Cada lectura es un viaje a Neon y una pantalla como Hoy hace muchas (además,
  buscar un cronograma lista todos antes de leer uno). Solución prevista: caché en memoria en
  `AlmacenPostgres` (leer una vez, escribir en caché y en Postgres a la vez; es seguro con un
  solo servidor) y medir antes y después. Aparte, el primer acceso tras 15 min sin uso tarda
  30–60 s porque Render y Neon se duermen en el plan gratuito; eso no se arregla con código.
- **Material nuevo en la nube.** El servidor de Render no ve las carpetas de este equipo: en la
  nube la carpeta de material es `/app/data/material` (vacía) y Configuración rechaza rutas
  como `C:\Users\…\OneDrive…\6. SEXTO` porque valida que existan en el servidor. Hoy solo
  funciona subir archivos sueltos desde Material. Opciones a decidir:
  - **Modo híbrido:** ejecutar la app local con la misma `DATABASE_URL` para ingerir desde las
    carpetas y la bóveda de Obsidian de este equipo, y que la nube vea el resultado. Requiere
    que los ajustes (rutas) sean de cada equipo y no se compartan en Postgres.
  - **Leer de OneDrive** con Microsoft Graph, ya que el material está allí.
  - Como mínimo, en la nube ocultar el escaneo de carpetas y explicar por qué, en lugar de
    mostrar una ruta del servidor.

## Frontend

- **Tests del frontend.** No hay ninguno. Empezar por la lógica pura de `lib/` (`clave`,
  `parsearFecha`, `clasesConFecha`, `materiasConCronograma`, `extensionPara`) y seguir con
  las vistas que tienen flujo propio (repaso, guía offline, confirmación).
- **Selector de tema claro/oscuro.** Ahora el tema sigue al sistema operativo
  (`prefers-color-scheme`). Para el despliegue, añadir un selector claro / oscuro / sistema
  que se recuerde por usuario.
