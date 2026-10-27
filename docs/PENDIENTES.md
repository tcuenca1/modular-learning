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

- **Clases con el mismo tema reciben el mismo contenido (bug).** La guía offline y la tutoría
  buscan el detalle de la clase por su tema (`CronogramaRepo.obtener_detalle_clase(materia,
  tema)`), y el repositorio devuelve la primera clase que coincide. Si dos clases de días
  distintos comparten tema, ambas se generan con el objetivo y contenido de la primera. Además,
  `GuiaOfflineService.crear` agrupa las clases elegidas por tema. Arreglo: identificar la clase
  por su posición o fecha en el cronograma (no por el tema) en guías, tutoría y
  `marcar_clase_completada`, que hoy marca todas las clases con ese tema.

## Datos que introduce el usuario

- **Todo debe poder deshacerse.** Si el usuario se equivoca al añadir algo, debe poder
  eliminarlo o corregirlo. Materia y cronograma van a la par: eliminar una materia elimina su
  cronograma y viceversa (con confirmación). Revisar todos los puntos de entrada: materias,
  cronogramas y sus clases (editar, borrar, cambiar estado), material ingestado (registro y
  nota), guías offline, revisión de una guía (deshacer la confirmación), tarjetas de repaso y
  ajustes.
- **Normalizar los nombres de las materias.** Hoy conviven "Ingenieria de Software II" en el
  catálogo, "INGENIERIA_DE_SOFTWARE_II" en el archivo del cronograma y "Ingenieria De Software
  Ii" en las estadísticas, y la web los cruza con `clave()`. Definir un identificador único
  por materia (slug) y un nombre para mostrar, aplicarlo al crear y migrar los datos actuales.

## Plugins prácticos

Hoy Node-RED analiza los `.json` de flujos de una carpeta; Cisco extrae líneas con palabras
clave de las notas de la bóveda. Estrategias por plugin, a decidir:

- **Cisco Packet Tracer.** Los `.pkt`/`.pka` son binarios cifrados y no hay forma fiable de
  leerlos fuera de Packet Tracer. Opciones:
  1. *Configuraciones exportadas* (recomendada): por cada actividad, guardar en una carpeta el
     `show running-config` de cada equipo (texto). El plugin extrae VLAN, interfaces,
     enrutamiento, ACL… y el tutor razona sobre la configuración real.
  2. *Enunciado de la actividad*: el PDF o captura de las instrucciones, ingerido como material.
  3. *Registro de comandos*: un `.txt` por actividad con los comandos usados; el más simple,
     pero pierde la topología.
- **Programación (web y otras).** Asociar a la asignatura la carpeta de proyectos. El plugin
  lee lo que describe el proyecto sin mandar todo el código: `README`, `package.json` /
  `pyproject.toml`, estructura de carpetas, rutas y modelos principales, y el `git log` si es
  un repositorio. Ignorar `node_modules`, `dist`, `.venv` y secretos (`.env`). El tutor puede
  así explicar con ejemplos del propio proyecto y detectar qué temas del sílabo ya se aplican.
- **Node-RED.** Mantener la lectura de flujos `.json` y añadir el resumen por flujo (nodos,
  tópicos MQTT, funciones) para elegir cuál usar en una tutoría.
- **General.** Cada plugin declara qué carpeta lee y qué extrae, configurable por asignatura
  en lugar de rutas fijas (Cisco hoy lee `obsidian_vault/Tecnologias de Conmutacion I`).

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
