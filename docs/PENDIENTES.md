# Pendientes

Trabajo acordado que queda para más adelante. Al terminar uno, se borra de aquí (el detalle
queda en el commit).

## Guía offline y tutoría

- **La tutoría web no identifica la clase por su id.** El backend ya acepta `clase_id`
  (`POST /api/tutoria` y `TutoriaService.iniciar_sesion`), pero `enlaceTutoria` y
  `TutoriaView` solo envían el tema, así que se usa la primera clase pendiente con ese tema.
  Pasar el id en el enlace desde Hoy, Asignaturas y la revisión de la guía.
- **Extracción de evaluaciones del sílabo.** Los cortes de parcial ya se definen a mano; falta
  que el prompt `04_extraccion_silabo.md` capture las evaluaciones en lugar de descartarlas.
- **Deshacer la revisión de una guía es demasiado amplio.** `deshacer_revision` borra del
  historial los eventos de tipo "guia" con el mismo tema (aunque sean de otra guía) y deja como
  pendientes clases que quizá ya estaban completadas antes de la guía. Guardar en el evento el
  id de la guía y el estado previo de cada clase.
- **`crear` ya no avisa de clases que faltan.** Si alguna de las clases elegidas no está en el
  cronograma, se ignora en silencio; solo falla si no se encuentra ninguna.

## Datos que introduce el usuario

- **Terminar la normalización de nombres.** El catálogo ya usa slug + nombre y el registro de
  material guarda slugs, pero los archivos de cronograma siguen como
  `INGENIERIA_DE_SOFTWARE_II_cronograma.json` y `listar_cronogramas` devuelve esos nombres.
  Renombrar los documentos a `<slug>_cronograma.json` y devolver el slug.
- **Migrar los datos de Neon.** `scripts/migrar_datos.py` solo actúa sobre `data/` local. En
  la nube los cronogramas reciben ids solo cuando se vuelven a guardar; hasta entonces la web
  identifica sus clases por el tema. Migrar a través de `AlmacenDocumentos`.

## Despliegue (Render + Neon)

- **Medir la caché de `AlmacenPostgres`.** Ya hay caché de lectura en memoria; falta medir la
  recarga antes y después. `listar` sigue consultando Neon cada vez.
- **`en_nube` se activa con `DATABASE_URL`.** Con el modo híbrido (app local contra Neon) se
  ocultaría el escaneo de carpetas. Decidirlo con una variable explícita.
- **Material nuevo en la nube.** Hoy solo se avisa en Configuración y Material. Siguen
  pendientes las opciones: modo híbrido con ajustes por equipo o lectura de OneDrive con
  Microsoft Graph.

## Frontend

- **Tema claro con el sistema en oscuro.** `index.css` aún tiene bloques
  `@media (prefers-color-scheme: dark)` (por ejemplo, el de `.prose`) sin su contrapartida para
  `html.light`: con el sistema en oscuro y la app en claro, las notas salen en texto claro
  sobre fondo claro. Pasarlos a la variante `dark:` / `html.dark`.
- **Avisos de oxlint.** `npm run lint` da 12 avisos en `MaterialView`, `SilabosView`,
  `PluginsView` y `ThemeToggle` (dependencias de efectos y `setState` dentro de efectos).
- **Tests de las vistas.** La lógica de `lib/` ya tiene tests; faltan las vistas con flujo
  propio (repaso, guía offline, confirmación).
