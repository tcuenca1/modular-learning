# Pendientes

Trabajo acordado que queda para más adelante. Al terminar uno, se borra de aquí (el detalle
queda en el commit).

## Reglas para quien implemente

Lee `CLAUDE.md` antes de empezar. Además:

1. **Una tarea, un commit.** Rama `main`. El mensaje empieza con el tipo y lleva el id de la
   tarea: `fix(web): P1 enviar clase_id a la tutoria`. Sin tildes, en español.
2. **Solo lo que pide la tarea.** Nada de funcionalidades, refactors ni renombrados extra. Si
   ves otro problema, anótalo al final de este archivo en «Hallazgos» en vez de arreglarlo.
3. **Antes de cada commit, todo en verde** (desde la raíz):
   ```bash
   venv/Scripts/python.exe -m pytest -q backend
   venv/Scripts/ruff.exe check backend
   venv/Scripts/ruff.exe format <archivos .py tocados>     # solo los tocados
   venv/Scripts/python.exe -c "import sys; from importlinter.cli import lint_imports_command; sys.argv=['lint-imports','--config','backend/pyproject.toml']; lint_imports_command()"
   cd frontend && npm run lint && npm run build && npm test
   ```
   `lint-imports.exe` falla en silencio: usa la línea de arriba.
4. **El núcleo no accede al disco.** En `core/` no puede haber `open`, `os.walk`, `os.listdir`,
   `os.remove`, `os.stat`, `os.path.isdir/isfile/exists`, `print` ni `settings`
   (`os.path.join/splitext/basename` sí). Si hace falta el disco, se añade un método a un
   puerto, se implementa en `infrastructure/` y se añade al fake de
   `backend/tests/unit/application/fake_adapters.py`.
5. **Cada tarea trae su test** y lo nombra en el commit. Los tests unitarios usan los fakes,
   nunca `tmp_path` ni el LLM real.
6. **No toques `data/`** (son los datos reales del usuario) **ni `.env`**. Para probar a mano,
   copia `data/examples` a otra carpeta y apunta `ML_DATA_DIR` a ella. No hagas push.
7. **No marques nada como hecho si no cumple todos sus criterios.** Si la dejas a medias,
   escribe debajo qué falta. **No borres tareas de este archivo:** las borra Claude cuando
   aprueba la revisión.
8. **Informe en `docs/CAMBIOS_AGY.md`.** Por cada tarea añade una entrada con la plantilla de
   ese archivo (commit, archivos, qué hiciste, cómo lo verificaste con la salida real de los
   comandos, dudas). Va en un commit aparte justo después del de la tarea:
   `docs: P1 informe en CAMBIOS_AGY`.
9. **Documentación:** si la tarea cambia un comportamiento descrito en `README.md`,
   `docs/DESPLIEGUE.md` o `CLAUDE.md`, actualiza ese párrafo en el mismo commit de la tarea.
   No reescribas `docs/ARCHITECTURE.md` ni añadas documentos nuevos (salvo las tareas D1 y D2).
10. **Prueba manual de verdad.** Si la tarea cambia efectos, estado o carga de datos de una
    vista, ábrela en el navegador y describe qué hiciste y qué viste. `lint` y `build` no
    cuentan como prueba manual.

## Tareas (en orden de prioridad)

### P23. El archivo del sílabo no debe cambiar la asignatura elegida

**Hazla antes de P19** (toca `SilabosView`, que P20 reorganiza). En
`frontend/src/views/SilabosView.tsx`, al elegir un archivo, si su nombre no coincide con el
catálogo se cambia el desplegable a «Nueva asignatura…» con el nombre del archivo, aunque el
usuario ya hubiera elegido una asignatura. Con «Silabo_2026.pdf» se acabaría creando la
asignatura «Silabo 2026».

- Si el nombre del archivo coincide con una asignatura del catálogo, se selecciona esa.
- Si no coincide, **no se toca** la selección. Solo si el desplegable ya estaba en «Nueva
  asignatura…» y el campo de texto está vacío, se rellena con el nombre del archivo.
- Lo mismo con el nombre que devuelve la extracción (`res.materia`).

**Aceptación:** prueba en el navegador (regla 10): elegir «Programación Web» y luego un archivo
llamado `Silabo_2026.pdf` mantiene «Programación Web»; elegir un archivo
`PROGRAMACION_WEB.pdf` con «Nueva asignatura…» selecciona «Programación Web».

### P24. Completar `.pptx` en la web y evitar notas inventadas

**Hazla antes de P19.** Completa P16:

- `MaterialView`: el selector de archivo acepta `.pptx` y la etiqueta lo menciona; quita el texto
  «No soportados (ej. .pptx)» si ya no aplica.
- El `aviso` que devuelve la ingesta (plan B) se muestra al usuario: en el resultado de la subida
  individual y en el resumen del lote.
- **Presentación sin texto:** si el plan B extrae menos de ~200 caracteres útiles (sin contar
  las marcas «--- Diapositiva N ---»), **no se llama a Gemini ni se escribe la nota**: el
  resultado es un error claro («La presentación es solo imágenes: instala LibreOffice para
  procesarla») y el archivo no se registra como ingestado.
- `ConversorLibreOffice`: lanza `soffice` con un perfil propio
  (`-env:UserInstallation=file:///<tmp>/perfil`) para que funcione aunque LibreOffice esté
  abierto, y borra ese perfil temporal al terminar.

**Aceptación:** tests unitarios con fakes: plan B con texto vacío no llama al LLM ni escribe en
la bóveda; plan B con texto sí, y devuelve el aviso. Test del adaptador comprobando que el
comando incluye `-env:UserInstallation` (sin ejecutar `soffice`). Prueba en el navegador de la
subida de un `.pptx` con una copia de `data/examples` y una bóveda de prueba.

### P19. Hoy: desbordamiento en móvil y avisos agrupados

Hazla después de P18. En las capturas (390 px de ancho) la vista Hoy se sale por la derecha: los
avisos de guías y la cabecera quedan cortados. Además, la vista empieza con un aviso amarillo por
cada guía pendiente de confirmar (hoy hay 6, con duplicados y dos de una asignatura que ya no
está en el catálogo) antes de lo importante.

- Corrige el desbordamiento horizontal en móvil en Hoy (y revisa la barra superior de móvil del
  layout). Ninguna vista debe tener scroll horizontal a 390 px.
- Sustituye la pila de avisos por una sola línea: «N guías por confirmar →» que lleva a la lista
  de guías. Con una sola guía, puede seguir mostrando su asignatura.
- En el número de «9 preguntas para hoy» se ve un recuadro amarillo extraño debajo del número
  (en Hoy y en Repaso): corrige el estilo para que el resaltado se vea como subrayado o quítalo.

**Aceptación:** capturas o prueba en el navegador a 390 px y a 1440 px (regla 10), con varias
guías pendientes en una copia de `data/examples`. `npm run lint` sin avisos.

### P20. Asignaturas: un solo selector y acciones peligrosas apartadas

Hazla después de P15 y P17 (tocan los mismos archivos). Hoy Asignaturas tiene tres niveles de
navegación seguidos (pestañas Cronogramas/Material → «Gestionar / Subir sílabo» → chips de
asignatura) y Material tiene además sus propias pestañas. Los botones que borran están al lado
de los normales.

- Estructura: arriba, el selector de asignatura (uno solo, compartido); debajo, tres pestañas:
  **Clases**, **Material** y **Proyectos**. «Subir sílabo» es un botón dentro de Clases (y el
  estado vacío de una asignatura sin clases lo ofrece directamente). La pestaña se refleja en la
  URL (`?tab=`) y las URL antiguas siguen funcionando.
- Acciones de borrado (vaciar cronograma, eliminar asignatura, vaciar todo el material) en un
  menú «⋯» o en una sección «Zona peligrosa» al final, nunca junto al botón principal. Siguen
  pidiendo confirmación.
- No mostrar el slug al usuario.
- Solo reorganizar: sin cambios de API ni de lógica de datos.

**Aceptación:** prueba en el navegador (regla 10) de cada acción que había antes (todas siguen
accesibles), en escritorio y a 390 px. Lista en el informe dónde quedó cada botón.

### P21. Menú de 9 entradas a 5

Hazla después de P20. Menú actual: Hoy, Calendario, Tutoría, Repaso, Guía offline, Progreso,
Asignaturas, Plugins, Configuración.

- **Hoy** incorpora el resumen de Progreso (avance por asignatura); la vista Progreso se elimina.
- **Estudiar** agrupa Tutoría, Repaso y Guía offline como tres pestañas o modos de una misma
  pantalla.
- **Calendario** y **Asignaturas** se quedan.
- **Ajustes** agrupa Configuración y Plugins.
- Todas las rutas antiguas (`/tutoria`, `/repaso`, `/guia`, `/progreso`, `/plugins`, `/config`)
  redirigen a su nuevo sitio conservando la query (`/tutoria?materia=…&clase_id=…` debe seguir
  funcionando: lo usan los enlaces de P1).
- Actualiza los enlaces internos.

**Aceptación:** prueba en el navegador (regla 10) de todas las rutas antiguas y de los enlaces
«Estudiar» de Hoy y Calendario. `npm run lint`, `npm run build` y `npm test` en verde.

### P22. Textos más cortos y consistentes

Hazla al final de la interfaz (después de P21).

- Las introducciones de cada vista, una sola línea (Guía offline y Repaso tienen párrafos de tres
  líneas); lo demás, en un icono de ayuda o en el estado vacío.
- Siempre «asignatura», nunca «materia», en la interfaz.
- Botones con mayúscula solo en la primera palabra («Añadir clase», no «Añadir Clase»).
- Sin jerga: «Ingestar documento individual» → «Convertir en nota» (revisa «ingestar» en toda la
  interfaz).
- Plugins: el «Registro de sincronización» solo aparece después de pulsar «Actualizar».

**Aceptación:** `git grep -n "Materia\b\|materia " frontend/src/views` sin textos visibles con
«materia»; capturas antes y después de 3 vistas en el informe. `npm run lint` sin avisos.

### P25. En la nube, no escanear carpetas locales (DISC-08 del manual)

`HoyView` llama a `api.escanearMaterial()` siempre y muestra «Material nuevo» aunque la app esté
en Render; `MaterialView` muestra la tarjeta «Tus carpetas de asignatura» y llama a
`api.escanearProyectos()` también en la nube.

- Con `en_nube` (de `GET /api/config`), Hoy no escanea ni muestra «Material nuevo», y Material
  oculta la tarjeta de carpetas y no llama a los escaneos. La subida de archivos sigue
  disponible.
- En el backend, los endpoints de escaneo responden vacío (o 409 con un mensaje claro) si
  `ML_EN_NUBE=1`, para que no dependa solo del frontend.

**Aceptación:** test de API con `ML_EN_NUBE=1` y sin ella; prueba en el navegador con la
variable puesta.

### P26. La CLI también debe identificar la clase por su id (DISC-09)

`ml init` (`apps/cli/ui/interaccion.py` y `apps/cli/commands/init.py`) descarta el `id` de la
clase elegida y llama a `iniciar_sesion` sin `clase_id`, así que al cerrar se marca la primera
clase con ese tema (el mismo fallo que P1 corrigió en la web).

- `pedir_datos_inicio` devuelve también `clase_id` cuando se eligió una clase del cronograma, y
  `init` lo pasa a `iniciar_sesion`.

**Aceptación:** test de la CLI (con `typer.testing.CliRunner` y servicios falsos, o un test de
la función) en el que, con dos clases del mismo tema, elegir la segunda manda su `clase_id`.

### P27. Cortes de parcial: guardar la clase, no una fecha (DISC-10)

`SilabosView` guarda en `hasta` una fecha escrita a mano («15/10/2026»), pero `GuiaView` compara
`hasta` con el `id` de la clase, así que un corte creado desde Sílabos nunca selecciona nada.

- En el formulario de cortes, `hasta` se elige con un desplegable de las clases del cronograma
  (mostrando fecha y tema) y se guarda el `id` de la clase.
- Los cortes antiguos con fecha siguen funcionando: si `hasta` no es un id, `GuiaView` usa la
  última clase con fecha menor o igual a esa fecha.
- La lista de cortes muestra el tema y la fecha de la clase, no el id.

**Aceptación:** tests de vitest para la función que resuelve `hasta` (id, fecha antigua y valor
inválido) y prueba en el navegador: crear un corte en Sílabos y usarlo en Guía offline.

### P28. Borrados consistentes (DISC-11)

- `ProyectosService.eliminar_proyecto` también quita su entrada `[PROYECTO] …` del registro de
  materiales y su nota en la bóveda (como hace `vaciar_proyectos`).
- `MateriasService.eliminar_materia` también elimina los proyectos de esa asignatura.
- `IngestaService.vaciar_materiales` limpia las referencias a materiales dentro de los
  cronogramas (`materiales_asociados` y `material_transversal`), sin tocar clases ni estados.

**Aceptación:** un test unitario con fakes por cada punto.

## Documentación funcional (tarea aparte, no toca código)

### D2. Poner al día la documentación y limpiar restos

Hazla **después de D1**: el manual te da el inventario de lo que existe de verdad.

- **Manual al día:** D1 se escribió sobre el código anterior a P12–P18. Actualiza los casos de
  uso afectados y marca DISC-01 a DISC-06 como resueltas (con el commit que las resolvió). Cada
  vez que se apruebe una tarea que cambie un flujo, el manual se actualiza (lo pedirá Claude).
- **DISC-12:** corrige en `docs/ARCHITECTURE.md` y `README.md` la ruta de `materias.json` y
  `registro_materiales.json` (están en `data/config/`) y quita las «rachas de estudio», que no
  existen. Regenera el PDF con `scripts/generar_manual.py`.

- **Borrar** (están obsoletos): `docs/TECHNICAL_WRITER_REPORT.md` (informe de octubre que aún
  llama al proyecto `ml-cli`) y `docs/CHANGELOG.md` (habla de agentes CrewAI que ya no existen;
  el historial de git hace de changelog). Quita los enlaces que apunten a ellos.
- **`README.md`**: que describa el sistema actual: qué es, requisitos (incluido LibreOffice si
  P16 ya está hecha), instalación con `backend/` y `frontend/`, arranque local, comandos de la
  CLI y enlaces a `docs/manual/`, `docs/ARCHITECTURE.md` y `docs/DESPLIEGUE.md`. Corto: el
  detalle va en el manual.
- **`docs/ARCHITECTURE.md`**: comprobar cada afirmación contra el código (capas, puertos,
  adaptadores, almacén de documentos, contratos de import-linter) y corregir lo que no
  coincida. Sin inventar: si algo no está en el código, no va.
- **`docs/DESPLIEGUE.md`**: comprobar contra `render.yaml`, `Dockerfile` y `deploy/`.
- **`GEMINI.md`**: reducirlo a «sigue `CLAUDE.md` y las reglas de `docs/PENDIENTES.md`» más los
  pasos de trabajo (tarea → verificación → commit → informe → detenerse), sin copiar las
  reglas, para que no se desincronicen.
- **No toques** `CLAUDE.md` ni `docs/PENDIENTES.md` (salvo «Hallazgos»): son las
  instrucciones de trabajo y las mantiene Claude. Si ves algo mal en ellos, anótalo en
  «Hallazgos».
- **Restos sin versionar** en la raíz (están ignorados por git, solo ocupan disco): borra
  `build/`, `modular_learning_cli.egg-info/`, `tests/` de la raíz (solo tiene `__pycache__`;
  los tests están en `backend/tests/`), `__pycache__/`, `.import_linter_cache/` y
  `.aider.chat.history.md`. **No borres `obsidian_vault/`** ni nada de `data/`: lo decide el
  usuario.

**Aceptación:** ningún documento menciona `ml-cli`, CrewAI ni rutas que no existan (compruébalo
con `git grep`). Todos los comandos del README funcionan copiándolos tal cual (pégalos con su
salida en el informe). Commit `docs: D2 documentacion al dia` y su informe aparte.

## Para decidir con el usuario (no implementar)

- **Material nuevo en la nube:** modo híbrido con ajustes por equipo, o leer de OneDrive con
  Microsoft Graph.
- **Medir la caché de `AlmacenPostgres`:** hay que medir la recarga en Render antes y después;
  `listar` sigue consultando Neon en cada llamada.
- **Extracción de evaluaciones del sílabo:** que `04_extraccion_silabo.md` capture los parciales
  en lugar de descartarlos, para no tener que definir a mano los cortes.
- **Tests de las vistas** (repaso, guía offline, confirmación): hace falta elegir la
  herramienta (Testing Library + jsdom).

- **Imágenes en `.docx` (DISC-07):** hoy solo se envía el texto de los párrafos (sin tablas ni
  imágenes). Opciones: convertir `.docx` a PDF con el mismo conversor de P16, o extraer tablas.
- **`apps/cli/commands/snapshot.py` (DISC-12):** no está registrado en la CLI y hace I/O fuera
  de los puertos. ¿Se borra o se integra como comando?

## Hallazgos

*(Anota aquí lo que encuentres fuera del alcance de tu tarea.)*
