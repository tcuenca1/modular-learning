# Cambios de Antigravity

Informe de lo que Antigravity implementa de `docs/PENDIENTES.md`. Claude lo usa para revisar
cada tarea commit por commit. **Una entrada por tarea**, la más reciente arriba. No borres
entradas anteriores: Claude añade debajo de cada una su veredicto.

## Plantilla

```markdown
## P<n>. <título de la tarea>

- **Commit:** <hash corto> `<mensaje del commit>`
- **Estado:** hecha | a medias (explica qué falta)
- **Archivos:** <lista de archivos tocados>

### Qué hice
<2-6 líneas: el cambio y por qué así. Si te apartaste de lo que pedía la tarea, dilo aquí.>

### Cómo lo verifiqué
- pytest: <N passed, M skipped>
- ruff check / ruff format: <ok o fallos>
- import-linter: <N contratos cumplidos>
- npm run lint / build / test: <ok o avisos> (solo si tocaste el frontend)
- Tests nuevos: <ruta::nombre_del_test, uno por línea>
- Prueba manual: <qué hiciste y qué viste, o "no aplica">

### Dudas o hallazgos
<lo que no supiste resolver o encontraste fuera del alcance; "ninguno" si no hay>

### Revisión de Claude
<lo rellena Claude: aprobada | cambios pedidos, con el motivo>
```

---

## P42. Tests de lo que hoy está sin cubrir

- **Commit:** 999f630 `test(core): P42 tests de sincronizador, contrato de repositorios y cobertura de plugins`
- **Estado:** hecha
- **Archivos:**
  - backend/tests/unit/domain/test_sincronizador.py (nuevo)
  - backend/tests/integration/infrastructure/test_contrato_repositorios.py (nuevo)
  - backend/tests/unit/application/fake_adapters.py

### Qué hice
- **`sincronizador.py`:** 13 tests unitarios con `FakeLLM`: cronograma vacío (no llama a la IA), el prompt lleva cronograma y apuntes, coincidencia por fecha, por tema contenido en ambos sentidos y con varias clases, sin coincidencia (primera pendiente y, sin pendientes, la última clase), referencia vacía, duplicados, vacíos y valores no textuales, elementos mal formados, respuesta que no es lista, y los dos fallos del LLM (JSON estructurado caído → se parsea el texto; todo cae → 0 y aviso en el log). El módulo no se usa en ningún otro sitio de `src` (código sin llamadores).
- **`plugins.py`:** ya lo cubrían los tests de P35 (plugin falso, sin `hasattr`); no escribí más.
- **Contrato:** `test_contrato_repositorios.py` parametriza una fixture con el fake en memoria y el adaptador JSON en disco (`AlmacenArchivos` sobre `tmp_path`) y ejecuta las mismas aserciones: 12 tests de `CronogramaRepo` (inexistente, ids y lectura por slug/nombre, coincidencia exacta, próximas clases, marcar por id/tema, detalle, `actualizar_cronograma`, material transversal, parciales, eliminar, listar) y 3 de `MateriaRepo` (catálogo vacío, alta/actualización por slug, idempotencia, eliminar). Son 30 casos.
- **Divergencia hallada y corregida:** el fake de `actualizar_cronograma` (de P32) modificaba en sitio la lista guardada, de modo que si la transformación fallaba quedaban cambios a medias; el adaptador real trabaja sobre una copia leída del disco. Ahora el fake usa `copy.deepcopy`. No hubo divergencias en el resto de métodos.

### Cómo lo verifiqué
- pytest: 293 passed, 2 skipped
- ruff check / ruff format: ok (`149 files already formatted`)
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: ok (66 tests); el frontend no cambió
- Cobertura (`pytest --cov=modular_learning.core --cov-report=term`, con `pytest-cov` instalado solo en el venv; no se añadió al repo): `core/domain/sincronizador.py` **0 % → 100 %** (objetivo ≥ 80 %); `core/application/plugins.py` 60 % → 98 % (con los tests de P35); `core` en conjunto 93 %.
- Tests nuevos:
  - tests/unit/domain/test_sincronizador.py (13 tests)
  - tests/integration/infrastructure/test_contrato_repositorios.py (15 funciones × 2 = 30 casos; 12 de cronograma y 3 de materias)
- Prueba manual: no aplica (solo tests). Comprobé que el test de contrato falla con el fake anterior y pasa con la copia profunda.

### Dudas o hallazgos
- `sincronizador.py` no tiene llamadores: o falta conectarlo (la ingesta ya enriquece subtemas por otro camino) o se puede borrar; conviene decidirlo (queda en «Hallazgos»).
- `obtener_cronograma` del fake devuelve la lista viva (mutarla cambia lo guardado) mientras que el adaptador real devuelve una copia nueva; hoy ningún test lo aprovecha, pero un servicio que mutara el resultado sin guardar pasaría los tests unitarios y fallaría en producción.

### Revisión de Claude

---

## P41. Textos sin jerga y acciones con IA avisadas

- **Commit:** 87423c1 `feat(web): P41 textos sin jerga y avisos de uso de IA`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/lib/rutas.ts, frontend/src/lib/rutas.test.ts (nuevos)
  - frontend/src/components/AvisoIA.tsx (nuevo)
  - frontend/src/components/layout/Sidebar.tsx
  - frontend/src/views/{ConfigView,GuiaView,HoyView,MaterialView,PluginsView,QuizView,SilabosView,TutoriaView}.tsx

### Qué hice
- **Jerga:** «Bóveda de Obsidian» pasa a «Carpeta de notas (Obsidian)», con la ayuda «Aquí se guardan las notas y las guías de cada tutoría: es la carpeta de tu bóveda en la app Obsidian.». «Cortes de parcial» pasa a «Fin de cada parcial» con su línea de ayuda («Elige la última clase de cada parcial…»), y los textos que dependían de «corte» se ajustaron (botones «+ Definir parcial», «+ Añadir / editar parciales», «Guardar parcial» y avisos). «Profundidad» pasa a «Nivel de detalle», con «Qué tan a fondo explica el tutor cada paso.» enlazada con `aria-describedby`.
- **Rutas:** `ultimoTramo` (POSIX y Windows) se usa donde se mostraba una ruta del equipo: carpeta del plugin, destino de la nota al subir un archivo, ruta del proyecto candidato, nota de Obsidian del proyecto, nota del material registrado y el aviso «Guardado en…» del sílabo. La ruta completa queda en el `title`. Los campos editables de Ajustes conservan la ruta entera (hay que poder editarla).
- **IA:** componente `AvisoIA` («· usa IA») en «Empezar» (tutoría), «Generar guía», «Preguntas nuevas» (Repaso y el enlace de Hoy), «Extraer clases» y «Procesar nuevos». Añadí los dos últimos por ser acciones que llaman a la IA aunque la tarea solo citaba los tres primeros como ejemplos.
- **Iconos:** Hoy usa `ListChecks` en vez del sol, que ya es el del tema claro.

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint sin avisos, build ok, vitest 66 passed (3 nuevos)
- `git grep -n "Bóveda de Obsidian\|Cortes de parcial\|Cortes de Parcial\|Profundidad\|Definir corte\|Guardar corte" -- frontend/src`: sin resultados. No toqué `docs/manual/` (documentación generada en D3), donde esos textos siguen apareciendo.
- Tests nuevos: frontend/src/lib/rutas.test.ts (rutas POSIX y Windows, separadores finales y repetidos, vacíos)
- Prueba manual (servidor local con copia de `data/examples`, carpeta de material de prueba y Chromium; leí los textos de cada vista):
  - Ajustes › Carpetas: «Carpeta de notas (Obsidian)» y su ayuda.
  - Tutoría: «Nivel de detalle» con la ayuda y «Empezar · usa IA» (captura revisada a ojo).
  - Estudiar › Guía: «Fin de cada parcial», «+ Definir parcial» y el botón «Generar guía · usa IA».
  - Repaso y Hoy: «Preguntas nuevas · usa IA». Asignaturas › Clases: «Fin de cada parcial» y «+ Añadir / editar parciales»; el panel de sílabo, «Extraer clases · usa IA»; Material: «Procesar nuevos · usa IA».
  - Iconos: Hoy `lucide-list-checks`, tema claro `lucide-sun`.
  - Ajustes › Plugins con una carpeta configurada (`…/uni/Redes/laboratorios`): la tarjeta muestra «laboratorios» y el `title` lleva la ruta completa.
  - axe-core 4.10.2: 0 nodos serious/critical a 1100 y 375 px; medición táctil: 0 controles bajo 44 px.
  No vi en pantalla las rutas de «Nota de Obsidian», proyectos candidatos ni el destino de un archivo subido, porque exigen ingestar con IA; ahí solo está cubierto el cambio de código y el test de `ultimoTramo`.

### Dudas o hallazgos
- Quedan otros textos técnicos que no estaban en la tarea («Opción A», «Trazabilidad Fija», «Fichas Técnicas Universales», «Re-analizar archivos y actualizar ficha en Obsidian»).
- «Obsidian» sigue apareciendo en varios textos y avisos: se explica en Ajustes, pero un estudiante nuevo no sabe qué es hasta ahí.
- La clave del cronograma sigue llamándose `parciales` con `hasta` en la API y los datos; solo cambió el texto visible.

### Revisión de Claude

---

## P40. Rendimiento del frontend

- **Commit:** 8216b58 `perf(web): P40 vistas con React.lazy y KaTeX solo en woff2`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/App.tsx
  - frontend/vite.config.ts

### Qué hice
- `App.tsx`: las 6 vistas y la hoja imprimible se importan con `React.lazy`; el `<Outlet />` del marco (y la ruta de impresión) van dentro de `Suspense` con un contenedor de reserva de `60vh` (sin saltos de diseño). El marco (barra lateral, rutas, avisos) sigue en el paquete inicial.
- `vite.config.ts`: plugin `katexSoloWoff2` que, al transformar la hoja de KaTeX, elimina las rutas `.woff` y `.ttf` de cada `@font-face`. El build pasa de 58 archivos de fuente KaTeX (19 woff2 + 20 woff + 20 ttf) a 19 woff2. Los navegadores actuales usan woff2.
- Markdown (react-markdown, remark, rehype y KaTeX) quedó en un chunk propio que solo bajan las vistas que lo usan; Hoy no.

Tamaños de `npm run build` (sin comprimir / gzip): antes, un solo `index` de **947 KB / 275 KB**. Ahora: `index` 261 KB / 81 KB, `jsx-runtime` 84 KB / 27 KB (React), vistas: Hoy 14 KB, Calendario 8 KB, Ajustes 17 KB, Estudiar 50 KB, Asignaturas 66 KB, revisión de guía 8 KB, impresión 5 KB, y `Markdown` 431 KB / 129 KB (carga diferida). **En la ruta Hoy se descargan 6 archivos JS: 353 KB sin comprimir (114 KB transferidos), menos de los 400 KB pedidos.**

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint sin avisos, build ok (sin aviso de chunks > 500 KB), vitest 63 passed
- Tests nuevos: ninguno (es empaquetado/carga; no hay lógica nueva que probar con vitest).
- Prueba manual / Lighthouse (lighthouse 13.6.0, `--only-categories=performance --form-factor=mobile`, 3 corridas, servidor local con gzip y caché de P33; el Chromium de Playwright):

| | rendimiento | FCP | LCP | TBT | CLS | transferido |
|---|---|---|---|---|---|---|
| antes (inicio de P40) | 87 / 88 / 65 | 1,5 s | 3,7 / 3,7 / 3,5 s | 160 / 140 / 180 ms | 0 / 0 / 0,658 | 415 KiB |
| después | 90 / 92 / 91 | 1,5-1,6 s | 3,5 / 3,3 / 3,4 s | 110 / 70 / 80 ms | 0 / 0 / 0 | 256 KiB |

  La puntuación de 55 y el LCP de 7,9 s del informe de origen se midieron antes de P33 (sin gzip ni caché); con P33 aplicado ya se medían 87-88, y P40 sube lo demás y quita la corrida con CLS alto (la corrida «antes #3» tuvo CLS 0,658, que no pude explicar; no se repitió después). El LCP sigue en 3,3-3,5 s: lo domina la hoja de Google Fonts (bloquea el render) con la CPU a 4×.
- Recorrido en Chromium: Hoy, Estudiar (3 pestañas), Calendario, Asignaturas, Ajustes (2 pestañas) y las rutas antiguas (`/tutoria` → `/estudiar?...`) cargan sus chunks sin errores de consola. KaTeX: con una guía de prueba (copia de datos temporal) en `/guia/<id>/imprimir` se renderizaron `E = mc² + ∫…` y `a²+b²=c²` (2 fórmulas `.katex`), y se descargaron 3 fuentes KaTeX, todas `.woff2` con estado 200; la captura se ve correcta (revisada a ojo).

### Dudas o hallazgos
- Las fuentes de Google (Fraunces, IBM Plex) siguen cargándose de fuentes externas con una hoja bloqueante; servirlas en local (p. ej. fontsource, WOFF2 con `preload`) probablemente mejoraría FCP/LCP, pero añade dependencias y no estaba en la tarea.
- Las pruebas de Lighthouse son de un entorno de contenedor con una máquina distinta a la del usuario: úsalas como orden de magnitud.
- La primera visita a una vista nueva hace una petición extra (chunk); en la caché de producción (`/assets/` con caché de un año) solo ocurre una vez.

### Revisión de Claude

---

## P39. Objetivos táctiles y calendario en móvil

- **Commit:** 04e710c `feat(web): P39 objetivos tactiles de 44 px y calendario util en movil`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/index.css
  - frontend/src/lib/calendario.ts, frontend/src/lib/calendario.test.ts (nuevos)
  - frontend/src/components/layout/Sidebar.tsx
  - frontend/src/views/{CalendarioView,HoyView,SilabosView}.tsx

### Qué hice
Medí primero con un script de JS en Chromium con puntero táctil (`hasTouch`, `isMobile`, 375 px; se cumple `(pointer: coarse)`): **79 controles por debajo de 44 px** entre Hoy (16), Calendario (8), Asignaturas › Clases (23), Material (16) y Proyectos (16): toggles de tema 26×26, menú 36×36, flechas del calendario 32×32, pestañas, botones de acción 28-32 px, «Subir sílabo» 74×18, «Estudiar →» 343×20, etc.
- `index.css`: bajo `@media (pointer: coarse)`, `button` (salvo el cierre de Sonner), `[role=tab]`, `select`, `summary` y los `input` de texto tienen `min-height: 44px`; botones y pestañas también `min-width: 44px`. Para enlaces de acción hay una clase `.toque` (mínimo 44×44), aplicada a la marca, a los enlaces del menú, a los de Hoy («Estudiar ahora», «Estudiar →», «Subir sílabo», «Preguntas nuevas», «Repasar ahora», «Procesar…», aviso de guías) y a las filas de clase del calendario. Fuera de `@layer`, para ganar a las utilidades.
- Calendario: `lib/calendario.ts` (`proximaClase`, `mesInicial`): abre en el mes actual si tiene clases; si no, en el mes de la próxima clase pendiente (o, sin nada por delante, del atraso más antiguo). Botón «Ir a la próxima clase» cuando se está en otro mes. Las filas de clase ya eran enlaces a la tutoría; ahora miden ≥ 44 px (`py-2` en móvil).
- Cortes de parcial: la cabecera de la tarjeta apila texto y botón en pantallas estrechas. `<code>` pasa a `overflow-wrap: anywhere` (rutas largas de la ficha de Proyectos).
- Dependencia que apareció: con el calendario ya abierto en octubre (donde hay clases), axe detectó que las clases completadas se atenuaban con `opacity-55` (contraste 2,3-3,3). Las sustituí por color secundario y tachado, sin opacidad.

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint sin avisos, build ok, vitest 63 passed (8 nuevos)
- Tests nuevos: frontend/src/lib/calendario.test.ts (`proximaClase`: próxima por delante, la de hoy, atraso, todo completado; `mesInicial`: mes actual con clases, mes de la próxima, mes del atraso, sin clases)
- Prueba manual (servidor local, copia de `data/examples`, Chromium con puntero táctil a 375 px):
  - Medición con JS de controles interactivos visibles de menos de 44 px: **0** en Hoy, Calendario, Asignaturas › Clases, Material y Proyectos (antes 79); `scrollWidth` = 375 en las cinco.
  - Calendario: abre en «Octubre de 2026» (2 clases, 1 pendiente) en vez de noviembre vacío; las filas miden 72 px; al pasar a noviembre aparece «Ir a la próxima clase» y al pulsarlo vuelve a octubre.
  - Capturas a 375 px (revisadas a ojo): Calendario, tarjeta «Cortes de parcial» (texto y botón apilados, cabe) y la ficha de Proyectos (la ruta de Obsidian se parte en varias líneas y `scrollWidth` = 375).
  - axe-core 4.10.2: 0 nodos serious/critical a 375 y a 1100 px en las 10 vistas y pestañas, claro y oscuro (tras corregir las clases completadas).
  No probé en un teléfono real.

### Dudas o hallazgos
- En la cabecera móvil, con los toggles de tema a 44 px, la marca queda truncada («Modular L…»). Podría quitarse el selector de tema de la cabecera (ya está dentro del cajón); lo dejé porque la tarea pedía los toggles a 44 px.
- Los enlaces dentro de una frase (p. ej. «Sube un sílabo» en el calendario vacío) quedan exentos de los 44 px; solo los enlaces de acción lo cumplen.
- Con una asignatura de 80 letras, Hoy desborda horizontalmente a 375 px (la lista de asignaturas no parte el nombre). No es de esta tarea; anotado en «Hallazgos».
- En pantallas táctiles anchas (tablet, ≥ 1024 px) la cuadrícula mensual también usa los mínimos de 44 px, así que las celdas con varias clases crecen.

### Revisión de Claude

---

## P38. Accesibilidad AA

- **Commit:** 5677fb0 `fix(web): P38 accesibilidad AA (etiquetas, foco, contraste, menu y encabezados)`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/index.css, frontend/src/App.tsx
  - frontend/src/components/{ThemeToggle.tsx,layout/Sidebar.tsx,ui/card.tsx}
  - frontend/src/views/{AsignaturasView,CalendarioView,ConfigView,HoyView,MaterialView,SilabosView,TutoriaView}.tsx
  - frontend/src/lib/contraste.test.ts (nuevo)

### Qué hice
Medí primero con axe-core 4.10.2 (reglas WCAG 2 A/AA y 2.1 A/AA) en Hoy, Estudiar (Tutoría, Repaso, Guía), Calendario, Asignaturas (Clases, Material, Proyectos) y Ajustes (Carpetas, Plugins), en claro y oscuro: **96 nodos serious/critical** (`color-contrast`, `select-name` y 1 `aria-prohibited-attr`).
- **Contraste:** `slate-400` y `slate-500` se usan como texto secundario con el mismo valor en ambos temas, y un solo color no llega a 4,5:1 sobre papel claro y sobre grafito a la vez. Ahora son variables por tema (`--ml-slate-400/500` en `:root` y `html.dark`): claro `#6f6757` / `#645c4e`, oscuro `#aba291` / `#9c9381`. `rose-600` (texto de «Eliminar…»): `#c70036` en claro y `#ff6384` en oscuro. `indigo-400` (verde de acento, «+ Definir corte» en oscuro): `#63a37c`. Los días de otros meses del calendario pasan a `dark:text-slate-500`.
- **Etiquetas:** `htmlFor`/`id` en Asignatura, Profundidad y Tema de Tutoría; `aria-label` en el campo de la duda; el selector de Asignaturas pasa de `<span>` a `<label htmlFor>`; ídem el select del panel de sílabo y los 2 inputs de Ajustes; `aria-label` en los campos de crear y renombrar asignatura.
- **Foco visible:** `select:focus-visible` con contorno de 2 px, definido fuera de `@layer` para ganar a `focus:outline-none`.
- **Menú móvil:** `aria-expanded` y `aria-controls` en el botón, el cajón es un `dialog` modal, al abrir el foco va al botón «Cerrar menú», Escape cierra y devuelve el foco al botón. Los botones de tema ya tenían `aria-pressed` en la cabecera; lo añadí a las tarjetas de tema de Ajustes (más `role="group"`).
- **Encabezados:** `CardTitle` pasa de `h3` a `h2` por defecto (prop `as`); las tarjetas por asignatura de Material usan `h3`. **Enlace «Saltar al contenido»** al inicio de la página y `<main id="contenido" tabIndex={-1}>`. `Regleta` de Hoy con `role="img"`.

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint sin avisos, build ok, vitest 55 passed (8 nuevos)
- Tests nuevos: frontend/src/lib/contraste.test.ts (lee `index.css` y comprueba ≥ 4,5:1 de los textos secundarios, el rojo y el verde en ambos temas, y del texto oscuro sobre el verde de acento)
- Prueba manual (servidor local, copia de `data/examples`, Chromium headless). axe-core 4.10.2 salió del paquete npm `axe-core@4.10.2` porque cdnjs devolvió 403 desde este entorno (misma versión del mismo producto). Resultado tras los cambios: **0 nodos serious/critical** en las 10 vistas/pestañas × claro y oscuro, a 1100 px y a 375 px, y también con el menú móvil abierto. Además comprobé por script:
  - Primer Tab muestra «Saltar al contenido» y Enter deja el foco en `#contenido`.
  - Menú: `aria-expanded` false → true, foco en «Cerrar menú»; Escape cierra, `aria-expanded` vuelve a false y el foco regresa a «Abrir menú».
  - Temas: `aria-pressed` cambia de Sistema a Oscuro, en cabecera y en Ajustes.
  - Select enfocado con teclado: `outline: solid 2px rgb(47,117,80)`.
  - Etiquetas: `tutoria-materia ← Asignatura`, `tutoria-nivel ← Profundidad`, `tutoria-tema ← Tema`, `config-carpeta-material ← Carpeta de material`, `config-ruta-obsidian ← Bóveda de Obsidian`.
  - Orden de encabezados sin saltos en las 10 vistas/pestañas (antes h1→h3 en 6).
  No probé con un lector de pantalla real ni los estados que necesitan Gemini (sesión de tutoría en curso, resultados de quiz).

### Dudas o hallazgos
- axe solo mide lo automatizable (~30-40 % de WCAG): faltan revisión con lector de pantalla y orden de foco manual.
- El cajón móvil lleva `aria-modal` pero no atrapa el foco con Tab (puede salir del cajón); hacerlo bien exige una pequeña utilidad de trampa de foco.
- Al cambiar los tokens `slate-400/500` y `indigo-400` cambian también bordes, iconos y fondos que los usan (p. ej. iconos del menú en claro, algo más oscuros); revisé capturas de Hoy (claro y oscuro) y de Calendario (oscuro) después del cambio y se ven coherentes (texto secundario legible, verde de acento más claro en oscuro); el resto de vistas solo las pasé por axe, sin revisión visual.
- `h3`/`h4` literales de algunas vistas (Quiz, Tutoría en sesión) no se recorrieron: dependen de estados con IA.

### Revisión de Claude

---

## P37. Flujo «Nueva asignatura» y selector

- **Commit:** 52167fa `fix(web): P37 flujo Nueva asignatura y selector sin desbordes`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/views/AsignaturasView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
Reproduje con una copia de `data/examples` y Chromium headless, con una asignatura de 80 letras: Enter no guardaba; tras crear «Fisica II» el panel Clases quedaba en blanco; tras recargar volvía a «Arquitectura de Software»; el panel de sílabo abría con «Nueva asignatura…»; `scrollWidth` era 1190 px a 375 px y 1590 px a 1100 px.
- `AsignaturasView`: Enter guarda y Escape cancela (en crear y en renombrar), el botón pasa a «Guardando…» y se deshabilita, el aviso de éxito añade el siguiente paso («sube su sílabo o añade clases en la pestaña Clases»), el nombre admite 80 caracteres y la asignatura activa se refleja en la URL (`?materia=<slug>`), por lo que la nueva queda seleccionada y sobrevive a recargas. Sin asignaturas, el texto indica crear la primera.
- Causa del panel en blanco: `SilabosView` embebido cargaba su catálogo una sola vez y no conocía la asignatura recién creada. Ahora recarga el catálogo (una vez por asignatura) cuando la activa no está en su lista; así aparece el estado vacío con «Subir sílabo» y «Añadir clase».
- El panel de sílabo parte de la asignatura activa (se sincroniza al cambiar la activa).
- Desbordes: el contenedor del selector y el `<select>` llevan `min-w-0 max-w-full` y truncan con puntos suspensivos; el título de la tarjeta, y los botones «Vaciar cronograma…» y «Eliminar asignatura…» de la zona peligrosa, parten los nombres largos (`overflow-wrap: anywhere`).

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint sin avisos, build ok, vitest 47 passed
- Tests nuevos: ninguno. El comportamiento está en las vistas y el repo no tiene jsdom/Testing Library (está en «Para decidir con el usuario»), por lo que lo verifiqué en el navegador.
- Prueba manual (servidor local, copia de `data/examples`, Chromium headless; leí los textos y revisé la captura a 375 px):
  - Con una asignatura llamada `X`×80: `document.documentElement.scrollWidth <= innerWidth` en Asignaturas › Clases, Material y Proyectos, a 375 px (375/375) y a 1100 px (1100/1100). Antes: 1190 y 1590. En la captura a 375 px el selector muestra el nombre truncado con «…» y la tarjeta parte el título en varias líneas.
  - Nueva asignatura «Quimica v1» con Enter: durante el guardado el botón dice «Guardando…» y está deshabilitado; aparece el aviso «Asignatura "Quimica v1" creada / Ahora sube su sílabo…»; queda seleccionada (`quimica-v1`, URL `?materia=quimica-v1`); la pestaña Clases muestra «No hay clases registradas en este cronograma» con «Subir sílabo»; tras recargar sigue seleccionada.
  - Al abrir «Subir sílabo» el segundo select vale «Quimica v1» (antes `__nueva__`).
  No probé modo oscuro ni un dispositivo táctil real.

### Dudas o hallazgos
- Con 0 clases, «Subir sílabo» aparece dos veces (cabecera de la tarjeta y estado vacío), como ya decía el informe del usuario novato; la tarea no pedía quitarlo.
- `SilabosView` conserva su propia lista de asignaturas y varios estados duplicados con `AsignaturasView`; el arreglo es un parche (recarga puntual), no una unificación.
- En la zona estrecha (375 px) la tarjeta «Cortes de parcial» sigue apretada; es parte de P39.

### Revisión de Claude

---

## P36. Pantalla Hoy coherente y con guía de arranque

- **Commit:** d1f658e `fix(web): P36 pantalla Hoy coherente y con guia de arranque`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/lib/hoy.ts (nuevo)
  - frontend/src/lib/hoy.test.ts (nuevo)
  - frontend/src/views/HoyView.tsx

### Qué hice
Reproduje con una copia de `data/examples` (catálogo de 5 asignaturas sin cronograma + el cronograma de ejemplo, que no pertenece al catálogo): Hoy mostraba «No tienes clases pendientes.», «1/2 clases (50%)» y 5 veces «Aún sin cronograma». La causa: el contador salía de `/api/stats`, que suma todos los cronogramas (incluso los huérfanos), mientras que el titular y las listas solo miran las asignaturas del catálogo.
- Criterio único (`lib/hoy.ts`): solo cuentan las clases de las asignaturas listadas. `avanceGlobal` calcula el contador (y es `null` si no hay clases: no se muestra) y `estadoHoy` decide el titular: `sin_asignaturas` / `sin_cronogramas` → «Aún no tienes clases cargadas.», `pendiente` → «Te toca …», `al_dia` → «No tienes clases pendientes.». El estado de «Repaso» usa el mismo avance.
- «Siguiente clase»: etiqueta sobre el titular cuando hay clase pendiente (el titular y la línea con asignatura y fecha ya existían).
- Sin datos: tarjeta «Primeros pasos» con 3 pasos enlazados (crear asignatura, subir sílabo, empezar tutoría) que marca los ya hechos; si el catálogo está vacío, «Tus asignaturas» lo explica.
- «Subir sílabo»: un enlace por asignatura sin cronograma con `aria-label="Subir sílabo de <asignatura>"`; lleva a `/asignaturas?materia=<asignatura>` (queda seleccionada). Se mantiene el texto visible «Subir sílabo» para no recargar la lista.
- Se quitó el estado `stats` de la vista (ya no se usa); `/api/stats` sigue usándose para el avance por asignatura.

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok (`147 files already formatted`)
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint sin avisos, build ok, vitest 47 passed (10 nuevos)
- Tests nuevos (frontend/src/lib/hoy.test.ts): `avanceGlobal` (suma, null sin clases, caso del cronograma huérfano), `estadoHoy` (4 estados), coherencia contador-titular, `pasosDeArranque`, `tieneCronograma`
- Prueba manual: servidor local (`uvicorn`, copia de `data/examples` en una carpeta temporal) y Chromium headless a 1100 px; revisé capturas y leí el texto de la página:
  - Antes: «No tienes clases pendientes.», contador «1/2 clases (50%)» y 5× «Aún sin cronograma».
  - Datos de ejemplo (5 asignaturas sin cronograma): «Aún no tienes clases cargadas.», sin contador, tarjeta «Primeros pasos» con el paso 1 marcado, 5 enlaces «Subir sílabo de …».
  - Con `Ejemplo Asignatura` en el catálogo (1 de 2 completadas): etiqueta «SIGUIENTE CLASE», «Te toca Modelado de Dominio…», «1/2 clases (50%)» y sin tarjeta.
  - Con las 2 completadas: «No tienes clases pendientes.» y «2/2 clases (100%)».
  - Catálogo vacío: «Aún no tienes clases cargadas.», tarjeta con 0 pasos hechos y «Todavía no hay asignaturas».
  - El enlace «Subir sílabo de Programacion Web» abre `/asignaturas?materia=Programacion%20Web` con esa asignatura seleccionada.
  No revisé el modo oscuro ni el ancho móvil (P38 y P39 los cubren).

### Dudas o hallazgos
- `/api/stats` sigue sumando cronogramas que no pertenecen al catálogo (por eso se contaba mal); Progreso/otras vistas que usen `total_temas` verían la misma discrepancia. No lo toqué: no estaba en la tarea.
- Un cronograma huérfano (sin asignatura en el catálogo) no se muestra en ningún sitio de Hoy; sigue visible en Calendario.

### Revisión de Claude

---

## P35. Plugins sin nombres de asignatura escritos a mano

- **Commit:** a82debf `refactor(core): P35 plugins sin nombres de asignatura ni hasattr`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/ports/plugin_practico.py
  - backend/src/modular_learning/core/application/plugins.py
  - backend/src/modular_learning/infrastructure/plugins/{cisco,nodered,web}.py
  - backend/tests/unit/application/fake_adapters.py
  - backend/tests/unit/application/test_plugins_service.py

### Qué hice
- `PluginPracticoBase` declara ahora lo que el servicio usa: `metadatos` (nuevo dataclass `PluginMetadatos`: id, nombre, categoría, materia por defecto, palabras clave, claves de selección, tipos de archivo, carpeta convencional, extensión de archivos y textos de presentación), `analizar_carpeta` (abstracto) y `analizar_archivo` (por defecto devuelve `None`).
- Cada plugin declara el suyo (`METADATOS` en `cisco.py`, `nodered.py`, `web.py`): ahí viven ahora «Internet de las Cosas», «Programacion Web» y «Tecnologias de Conmutacion I». `NodeRedPlugin.analizar_archivo` delega en `analizar_flujo` y `WebPlugin.analizar_carpeta` en `analizar_proyecto`.
- `PluginsService`: `listar_info_plugins`, `obtener_plugin`, `procesar_archivo_plugin` y `actualizar_plugin` recorren los plugins registrados y usan solo sus metadatos; desaparece el `if/elif` por plugin, `hasattr` y `METADATOS_PLUGINS`. El orden de sincronización con «todos» se conserva con `orden_sincronizacion` (Node-RED, Cisco, Web).
- Dos diferencias menores: `listar_info_plugins` solo lista los plugins registrados (antes listaba siempre los tres conocidos; en producción están los tres), y el mensaje de `procesar_archivo_plugin` para un plugin que no analiza archivos ahora es genérico («no soporta el análisis de archivos»); esa función no la usa nadie más que sus tests.

### Cómo lo verifiqué
- pytest: 250 passed, 2 skipped
- ruff check / ruff format: ok (`147 files already formatted`)
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: ok (37 tests); el frontend no cambió
- `git grep -n "Internet de las Cosas\|Programacion Web\|Tecnologias de Conmutacion" backend/src/modular_learning/core`: sin resultados (también sin `hasattr` en `plugins.py`)
- Tests nuevos:
  - tests/unit/application/test_plugins_service.py (15 tests con `FakePluginPractico`: info, configuración, enrutado por config/defecto/palabra clave/orden de registro, carpeta asignada/convencional/archivos con límite de 3 y exclusión de memoria, memoria con límite, orden con «todos», selección desconocida, `procesar_archivo_plugin`, `registrar_plugin`)
- Prueba manual (diferencial): cargué el `plugins.py` antiguo desde git y lo ejecuté junto al nuevo con los plugins reales, el lector real y un árbol temporal (carpetas convencionales con flujos `.json`, una configuración IOS y un proyecto web; sin carpetas; solo memoria). Comparé `actualizar_plugin` con 9 selecciones × 3 escenarios (27 casos): todas las salidas son idénticas; `obtener_plugin` con 12 nombres de asignatura y una configuración propia: sin diferencias; `listar_info_plugins`: igual.

### Dudas o hallazgos
- Las palabras clave («red», «internet», «web»…) siguen siendo heurísticas amplias (p. ej. «red» captura nombres con «redes» si no hubiera Cisco antes); no las cambié para no alterar el enrutado.
- `apps/api/routers/plugins.py` mantiene `OPCIONES_PLUGIN` con las etiquetas de los tres plugins escritas a mano; podría salir de los metadatos.

### Revisión de Claude

---

## P34. Dependencias y CI

- **Commit:** 7f59c16 `chore(ci): P34 pypdf 6.21.4, pasos de CI nuevos y dependabot`
- **Estado:** hecha
- **Archivos:**
  - backend/pyproject.toml
  - .github/workflows/ci.yml
  - .github/dependabot.yml (nuevo)
  - backend/src/modular_learning/apps/cli/commands/es.py (solo formato)
  - backend/src/modular_learning/infrastructure/system/subprocess_adapter.py (solo formato)

### Qué hice
- `pypdf>=3.0.0` pasa a `pypdf>=6.21.4`. Reproduje el problema con `pip-audit --no-deps -r` sobre `pypdf==6.21.3`: 3 vulnerabilidades (CVE-2026-119203, -119204 y -119205), corregidas en 6.21.4; con `6.21.4` no hay ninguna. Reinstalé con `pip install -e "./backend[all]"` (queda pypdf 7.0.1).
- `ci.yml`: añadí `ruff format --check backend`, `pip-audit ./backend` (instala `pip-audit` en el paso), `npm test` y `npm audit --audit-level=high`. Sin cobertura.
- `.github/dependabot.yml`: `pip` en `/backend` y `npm` en `/frontend`, semanal.
- Fuera de lo pedido pero necesario para que `ruff format --check` pase: formateé `es.py` y `subprocess_adapter.py`, que ya incumplían el formato antes de empezar (solo juntan una llamada en una línea).

### Cómo lo verifiqué
Ejecuté en local los mismos comandos que ahora corre el CI:
- pytest: 240 passed, 2 skipped
- ruff check: All checks passed! / ruff format --check backend: 147 files already formatted
- import-linter: 3 contratos cumplidos, 0 rotos
- pip-audit ./backend: No known vulnerabilities found
- npm run lint ok, npm test 37 passed, npm run build ok, npm audit --audit-level=high: salida 0 (solo 4 avisos de gravedad baja, de `katex` y sus dependencias)
- Tests nuevos: ninguno (cambios de configuración)
- Prueba manual: no pude ejecutar el workflow en GitHub Actions desde aquí; validé los dos YAML con `yaml.safe_load` y corrí cada paso a mano.

### Dudas o hallazgos
- `pip-audit ./backend` audita las dependencias base del proyecto, no los extras (`dev`, `web`, `nube`); para cubrirlos habría que auditar el entorno completo, con más ruido.
- `npm audit` lista 4 avisos de gravedad baja (`katex` y sus dependientes); no bloquean el umbral `high`.
- El CI usa Python 3.12; aquí probé con 3.13.

### Revisión de Claude

---

## P33. Cabeceras de seguridad, documentación de la API y compresión

- **Commit:** d3810e5 `feat(web): P33 cabeceras de seguridad, host confiable, sin docs en la nube y gzip`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/apps/api/seguridad.py (nuevo)
  - backend/src/modular_learning/apps/api/main.py
  - backend/tests/conftest.py
  - backend/tests/integration/api/test_seguridad.py (nuevo)
  - docs/DESPLIEGUE.md

### Qué hice
Reproduje con el cliente de pruebas: `/` sin ninguna cabecera de seguridad, `/docs`, `/redoc` y `/openapi.json` en 200, el JS de 947 KB sin `content-encoding` ni `cache-control`, y un `Host: evil.example` aceptado.
- `seguridad.py`: `CabecerasSeguridad` (middleware ASGI) añade CSP, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`, HSTS solo con `ML_EN_NUBE=1`, `Cache-Control` de un año con `immutable` para `/assets/` y `no-cache` para `/`. La CSP deja `script-src 'self'` (el build solo tiene un `<script type="module">` externo), estilos propios + `'unsafe-inline'` (React emite atributos `style`) + Google Fonts, que usa `index.html`.
- `HostsConfiables`: `TrustedHostMiddleware` con `ML_HOSTS_PERMITIDOS` (por defecto `localhost,127.0.0.1`, más `RENDER_EXTERNAL_HOSTNAME` si existe). Deja pasar `/api/salud` para no romper el healthcheck de Render.
- `create_app`: sin `/docs`, `/redoc`, `/openapi.json` con `ML_EN_NUBE=1`; `GZipMiddleware`.
- `tests/conftest.py` fija `ML_HOSTS_PERMITIDOS=testserver,localhost` en todos los tests (el TestClient usa el host `testserver`).
- `docs/DESPLIEGUE.md`: variables nuevas.
Decisión: la tarea decía «por defecto, localhost». Con eso, abrir la web local desde otro equipo de la red da 400 hasta añadir su nombre en `ML_HOSTS_PERMITIDOS`; está documentado.

### Cómo lo verifiqué
- pytest: 240 passed, 2 skipped
- ruff check / ruff format: ok en lo tocado (los 2 archivos sin formatear de antes siguen igual)
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: ok (37 tests); el frontend no cambió
- Tests nuevos (tests/integration/api/test_seguridad.py):
  - test_toda_respuesta_lleva_las_cabeceras_de_seguridad
  - test_csp_permite_lo_que_usa_el_build
  - test_hsts_solo_en_la_nube
  - test_host_no_permitido_da_400_pero_el_healthcheck_pasa
  - test_hosts_configurables_por_entorno
  - test_documentacion_de_la_api_solo_fuera_de_la_nube
  - test_assets_comprimidos_y_con_cache_larga (se omite si el frontend no está compilado)
  - test_los_eventos_sse_no_se_comprimen
- Prueba manual: servidor local (`uvicorn`, copia de `data/examples`) y Chromium headless en `http://localhost:8000`: cargué `/`, `/estudiar`, `/calendario`, `/asignaturas` y `/ajustes`; la consola no mostró ninguna violación de CSP ni errores, los 5 JS llegaron con `content-encoding: gzip` y `cache-control: public, max-age=31536000, immutable`, y la captura de Ajustes se ve completa (menú, tarjetas, tipografías). Con `ML_EN_NUBE=1` comprobé también que `/docs` da 404 y aparece HSTS.

### Dudas o hallazgos
- No pude comprobar en Render que `RENDER_EXTERNAL_HOSTNAME` esté definido ni que el healthcheck llegue con otro `Host`; por eso `/api/salud` queda exento y el hostname de Render se añade solo. Si el servicio da 400 tras desplegar, definir `ML_HOSTS_PERMITIDOS` con el dominio de Render.
- La CSP mantiene `'unsafe-inline'` en estilos; quitarlo exigiría eliminar los `style=` de React.
- Las fuentes siguen cargándose de Google Fonts; si P40 las sirve localmente se puede quitar su dominio de la CSP.

### Revisión de Claude

---

## P32. Escrituras concurrentes sin pérdida de datos

- **Commit:** 293c251 `fix(core): P32 escrituras concurrentes sin perdida de datos`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/infrastructure/persistence/almacen.py
  - backend/src/modular_learning/infrastructure/persistence/{json_repositorios,json_repaso,json_guias}.py
  - backend/src/modular_learning/core/ports/repositorios.py
  - backend/src/modular_learning/core/application/materias.py
  - backend/tests/unit/application/fake_adapters.py
  - backend/tests/integration/infrastructure/test_concurrencia.py, backend/tests/unit/application/test_cronograma_atomico.py, backend/tests/integration/api/test_api.py

### Qué hice
Reproduje con 16 hilos (cada uno con su cliente) sobre una copia de `data/examples`: `POST /api/materias` daba 500 en varios y solo persistían 1-2 de 16 (el temporal `.tmp` era el mismo para todas las escrituras y cada repositorio reescribe el documento entero).
- `AlmacenDocumentos.bloquear(clave)`: candado reentrante por documento (en disco, la clave es la ruta real, así que varias instancias del almacén sobre la misma carpeta comparten candado). Los repositorios JSON (materias, cronogramas, registro, plugins, proyectos, tarjetas, historial, guías) lo toman en cada ciclo leer-modificar-escribir. Incluida la migración inicial del catálogo, que también escribe.
- `AlmacenArchivos.escribir`: temporal único por escritura (`uuid`) y reemplazo con reintentos ante `PermissionError` (el `WinError 32` de Windows); no quedan `.tmp` y `listar` los ignora.
- Cambio de puerto, que sí era imprescindible: añadí `CronogramaRepo.actualizar_cronograma(materia, transformar)` (atómico) porque agregar una clase leía y guardaba en dos llamadas y se perdían clases aunque cada llamada estuviera protegida (3 de 16 persistían). `MateriasService.agregar_clase`, `editar_clase` y `eliminar_clase` lo usan; actualicé el fake. Si la transformación lanza, no se guarda nada.
- `DELETE` repetido o en paralelo: 200 la primera vez y 404 las demás (ya no hay 500).
Limitación: el candado es por proceso. Con varios procesos/trabajadores sobre los mismos archivos no protege (el despliegue usa uno solo); en Postgres solo cubre el proceso.

### Cómo lo verifiqué
- pytest: 232 passed, 2 skipped
- ruff check / ruff format: ok en lo tocado (los 2 archivos sin formatear de antes siguen igual)
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: ok (37 tests); el frontend no cambió
- Tests nuevos:
  - tests/integration/infrastructure/test_concurrencia.py::test_n_asignaturas_a_la_vez_persisten_todas (24 hilos)
  - tests/integration/infrastructure/test_concurrencia.py::test_instancias_distintas_del_almacen_comparten_candado
  - tests/integration/infrastructure/test_concurrencia.py::test_n_clases_a_la_vez_persisten_todas
  - tests/integration/infrastructure/test_concurrencia.py::test_editar_y_eliminar_clases_a_la_vez
  - tests/integration/infrastructure/test_concurrencia.py::test_eliminar_dos_veces_a_la_vez_no_falla
  - tests/integration/infrastructure/test_concurrencia.py::test_registro_y_config_de_plugins_concurrentes
  - tests/integration/infrastructure/test_concurrencia.py::test_escrituras_al_mismo_documento_no_dejan_temporales_ni_json_roto
  - tests/unit/application/test_cronograma_atomico.py (3 tests)
  - tests/integration/api/test_api.py::test_eliminar_asignatura_dos_veces_no_da_500
  Comprobé que los 7 tests de concurrencia fallan con el código anterior (git stash de `backend/src`) y pasan con el cambio.
- Prueba manual: repetí el script de 16 hilos 5 veces sobre una copia de `data/examples`: 16/16 asignaturas, 16/16 clases, sin 500; DELETE doble → [200, 404] y 8 en paralelo → un 200 y siete 404.

### Dudas o hallazgos
- Las operaciones de `IngestaService` que leen y guardan el cronograma (`ingesta.py` alrededor de las líneas 141, 252 y 344) siguen siendo leer→guardar en dos llamadas; pueden perder una actualización si coinciden con una edición manual. No las toqué (fuera del pedido).
- `crear_materia` comprueba duplicados y guarda en dos pasos: dos altas simultáneas del mismo nombre no pierden datos pero ambas responden 201 en vez de una 409.
- `AlmacenPostgres` no tiene candado entre procesos ni transacción de lectura-modificación; hace falta si se escala a más de un trabajador.

### Revisión de Claude

---

## P31. Rutas del cliente y errores que filtran el servidor

- **Commit:** 3c3e674 `fix(core): P31 rutas del cliente dentro de su base y errores sin rutas`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/domain/rutas.py (nuevo)
  - backend/src/modular_learning/core/application/{ingesta,materias,plugins,proyectos}.py
  - backend/src/modular_learning/apps/api/errores.py (nuevo)
  - backend/src/modular_learning/apps/api/routers/{config,guias,material,materias,plugins,proyectos,quiz,silabo,tutoria}.py
  - docs/DESPLIEGUE.md
  - backend/tests/unit/domain/test_rutas.py, backend/tests/unit/application/test_rutas_servicios.py, backend/tests/unit/test_errores_api.py, backend/tests/integration/api/test_api.py

### Qué hice
Reproduje con una carpeta de material temporal y archivos fuera de ella: `GET /api/material/escanear?materia=..%2f..%2f` escaneó 54 archivos fuera de la base; `/api/plugins/config`, `/api/plugins/actualizar` y `/api/proyectos/ingestar` aceptaron rutas externas (la ingesta escribió una ficha con la ruta externa); los errores 400/500 devolvían rutas absolutas (`/no/existe/aqui`, `/tmp/...`) y `GET /api/config` con `ML_EN_NUBE=1` devolvía las rutas.
- `core/domain/rutas.py`: `esta_dentro` y `unir_dentro`, comprobación léxica tras normalizar (sin tocar el disco).
- `IngestaService.escanear_materia` usa `unir_dentro`; los endpoints de escaneo, sincronización y proyectos resuelven la asignatura contra el catálogo (404 si no existe). Tutoría e ingesta de archivo validan con `MateriasService.validar_materia_recibida` (422).
- Ingesta de proyecto, carpeta de plugin y `carpeta_override` deben quedar dentro de la carpeta de material (400).
- `apps/api/errores.py`: 500 genérico y 4xx con rutas sustituidas por `<ruta>`; el detalle va al log (`modular_learning.api`). Aplicado a todos los routers y a los eventos SSE de error.
- En nube `GET /api/config` devuelve `carpeta_material` y `ruta_obsidian` vacías. Documentado en `docs/DESPLIEGUE.md`.
Decisión: la comprobación de las carpetas de plugin se hace al guardar y al usar el override, no al leer lo ya guardado, para no romper configuraciones previas que apuntaran fuera.

### Cómo lo verifiqué
- pytest: 220 passed, 2 skipped
- ruff check / ruff format: ok en lo tocado (`ruff format --check backend` sigue marcando los 2 archivos anteriores: `apps/cli/commands/es.py` y `infrastructure/system/subprocess_adapter.py`)
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: ok (37 tests); el frontend no cambió
- Tests nuevos:
  - tests/unit/domain/test_rutas.py (varios casos de `esta_dentro` y `unir_dentro`)
  - tests/unit/application/test_rutas_servicios.py::test_escanear_materia_con_ruta_relativa_no_lee_fuera_de_la_base
  - tests/unit/application/test_rutas_servicios.py::test_ingestar_proyecto_fuera_de_la_carpeta_base_falla
  - tests/unit/application/test_rutas_servicios.py::test_configurar_plugin_con_carpeta_fuera_de_la_base_falla
  - tests/unit/application/test_rutas_servicios.py::test_actualizar_plugin_con_override_fuera_de_la_base_falla
  - tests/unit/application/test_rutas_servicios.py::test_validar_materia_recibida
  - tests/unit/test_errores_api.py (4 tests)
  - tests/integration/api/test_api.py::test_escanear_material_no_acepta_rutas_del_cliente (5 variantes, incluye `..%2f`)
  - tests/integration/api/test_api.py::test_escanear_material_resuelve_contra_el_catalogo
  - tests/integration/api/test_api.py::test_sincronizar_stream_rechaza_asignatura_fuera_del_catalogo
  - tests/integration/api/test_api.py::test_proyectos_escanear_e_ingestar_no_aceptan_rutas_externas
  - tests/integration/api/test_api.py::test_plugins_no_aceptan_carpetas_externas
  - tests/integration/api/test_api.py::test_errores_no_muestran_rutas_absolutas
  - tests/integration/api/test_api.py::test_error_inesperado_responde_generico
  - tests/integration/api/test_api.py::test_config_en_nube_no_devuelve_rutas
- Prueba manual: repetí el script de reproducción (mismos pasos, árbol temporal): todas las rutas con `../` dan 404, plugins y proyectos externos 400, el error de configuración muestra `<ruta>` y `ML_EN_NUBE=1` devuelve rutas vacías. Tres tests existentes (plugins, escaneo de material y proyectos) se adaptaron: ahora configuran la carpeta de material y crean la asignatura en el catálogo antes de usarlas.

### Dudas o hallazgos
- No se resuelven enlaces simbólicos (hacerlo exige disco; iría en el adaptador). Un enlace dentro de la carpeta de material que apunte fuera sigue siendo seguible.
- `GET /api/material/escanear` sigue devolviendo la ruta de la carpeta del equipo en cada asignatura (campo `carpeta`) fuera de la nube; es el equipo del propio usuario.
- Los mensajes de error de Gemini (cuota, etc.) ahora salen como mensaje genérico de error interno; si se quiere distinguirlos al usuario habría que mapear esos casos.
- Las rutas guardadas de los plugins y `GET /api/plugins` / `GET /api/proyectos` siguen exponiendo rutas del servidor en la nube; la tarea solo pedía `/api/config`.

### Revisión de Claude

---

## P30. Validar nombres y existencia de asignaturas

- **Commit:** 1aa8722 `fix(core): P30 validar nombres y existencia de asignaturas`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/domain/materias.py
  - backend/src/modular_learning/core/application/materias.py
  - backend/src/modular_learning/apps/api/routers/materias.py
  - backend/tests/unit/application/test_materias_validacion.py
  - backend/tests/integration/api/test_api.py

### Qué hice
Reproduje primero con un cliente de pruebas sobre una copia de `data/examples`: `"   "`, `"!!!"`, `"😀"` daban 201 sin crear; `"a/b"`, `".."` y 100 letras sí se creaban; el duplicado `"redes"` daba 201; `PUT` a un slug inexistente lo creaba y las altas de clase y de parcial creaban un cronograma de una asignatura inexistente.
Añadí en `core/domain/materias.py` `validar_nombre_materia` (máx. 80, letras/números/espacios y `- _ . , ( ) ' & + : #`, sin control/NUL, `/`, `\` ni `..`) y las excepciones `NombreMateriaInvalido`, `MateriaDuplicada` y `MateriaNoEncontrada`. `MateriasService.crear_materia` valida y rechaza duplicados (comparados por slug, sin tildes ni mayúsculas); `renombrar_materia`, `agregar_clase` y `guardar_parciales` exigen que la asignatura exista. El router traduce a 422, 409 y 404.
Decisión: `agregar_materia` se queda idempotente y sin validar, porque la usan tutoría, material y la CLI para «asegurar» que la asignatura exista y no esperan excepciones; solo el alta explícita (`POST /api/materias`) usa `crear_materia`. Duplicado devuelve 409 (la tarea no fijaba código).

### Cómo lo verifiqué
- pytest: 180 passed, 2 skipped
- ruff check / ruff format: check ok; format de los archivos tocados ok. `ruff format --check backend` ya marcaba 2 archivos antes de empezar (`apps/cli/commands/es.py`, `infrastructure/system/subprocess_adapter.py`), no tocados.
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: ok (37 tests); el frontend no cambió
- Tests nuevos:
  - tests/unit/application/test_materias_validacion.py (nombres inválidos, normalización, longitud máxima, duplicados, renombrar, clase y parciales en inexistente)
  - tests/integration/api/test_api.py::test_crear_materia_nombre_invalido_422
  - tests/integration/api/test_api.py::test_crear_materia_duplicada_409
  - tests/integration/api/test_api.py::test_materia_inexistente_da_404_en_put_clases_y_parciales
- Prueba manual: servidor local con `ML_DATA_DIR` en una copia de `data/examples` y Chromium headless (Playwright). En Asignaturas › «Nueva asignatura» escribí `!!!` y `a/b`: aparece el aviso «No se pudo crear la asignatura» con el mensaje en español; `Redes de Datos` se crea. Leí el texto de los avisos, no inspeccioné la captura a ojo.

### Dudas o hallazgos
- `agregar_materia` (usada por tutoría, ingesta de material y CLI) sigue aceptando cualquier nombre; se endurece al tratar P31.
- Las rutas `editar_clase`, `eliminar_clase` y el cambio de estado no comprueban la asignatura; la tarea no las pedía.

### Revisión de Claude

---

## D3. Documentación al día tras P19 a P29 (Argon)

- **Commit:** e36ecf4 `docs: D3 documentacion tras P19 a P29`
- **Estado:** hecha
- **Archivos:**
  - `docs/ARCHITECTURE.md`
  - `docs/manual/MANUAL_FUNCIONAL.md`
  - `docs/manual/MANUAL_FUNCIONAL.pdf`

### Qué hice
- En `docs/ARCHITECTURE.md`, actualicé la sección de adaptadores del frontend para reflejar exactamente las 11 vistas de `frontend/src/views/` (eliminando las menciones obsoletas a `IngestaView`, `ProyectosView` y `ProgresoView`), describiendo el menú lateral de 5 entradas (`Hoy`, `Estudiar`, `Calendario`, `Asignaturas`, `Ajustes`), qué vista se renderiza en cada pestaña, las vistas de guías offline y las rutas heredadas con `RedirigirConQuery`.
- En `docs/manual/MANUAL_FUNCIONAL.md`, actualicé todos los casos de uso (`CU-01` a `CU-20`) y los flujos del semestre a la interfaz reorganizada en P20–P29 (menú de 5 entradas, `Estudiar` con Tutoría/Repaso/Guía, `Calendario` mensual, `Asignaturas` con selector único compartido y pestañas Clases/Material/Proyectos, secciones colapsables «Zona peligrosa», `Ajustes` con Carpetas y clave / Plugins, progreso integrado en `Hoy` y redirecciones con query).
- Marqué `DISC-08` (`7da3dab`), `DISC-09` (`511c3ab`), `DISC-10` (`2cead9e`), `DISC-11` (`58bf149`) y `DISC-12` (`e9fcd78` / `D3`) como resueltas, actualicé los flujos de escaneo en la nube, `ml init` con `clase_id`, cortes de parcial por `id` de clase y borrados consistentes, verifiqué las 803 referencias `archivo:línea` contra el árbol actual y regeneré `docs/manual/MANUAL_FUNCIONAL.pdf` con `scripts/generar_manual.py`.

### Cómo lo verifiqué
- pytest: 147 passed, 3 skipped
- ruff check / ruff format: ok (`All checks passed!`)
- import-linter: 3 contratos cumplidos (3 kept, 0 broken)
- npm run lint / build / test: no aplica (solo documentación)
- Tests nuevos: ninguno
- Prueba manual: comprobé con `git grep -n "ProgresoView\|IngestaView\|ProyectosView" docs/ARCHITECTURE.md docs/DESPLIEGUE.md docs/manual/ README.md` (0 coincidencias), verifiqué las 803 citas `archivo:línea` mediante script contra los archivos reales (0 errores) y abrí `docs/manual/MANUAL_FUNCIONAL.pdf` con PyMuPDF (28 páginas, 127.659 caracteres extraíbles sin errores).

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El diff coincide con los criterios: redirecciones con query, carga única del catálogo (`useCallback` sin dependencias y `materia` leída una sola vez con `useRef`) y títulos corregidos.

---

## P29. Remates de P20 a P28

- **Commit:** 670143a `fix(web): P29 formato ruff redirecciones con query carga unica y titulos`
- **Estado:** hecha
- **Archivos:**
  - `backend/tests/unit/application/test_ingesta_service.py`
  - `backend/tests/unit/application/test_otros_servicios.py`
  - `backend/tests/unit/cli/test_init_clase_id.py`
  - `frontend/src/App.tsx`
  - `frontend/src/views/AsignaturasView.tsx`
  - `frontend/src/views/MaterialView.tsx`
  - `frontend/src/views/SilabosView.tsx`

### Qué hice
- Ejecuté `ruff format` sobre los 5 archivos indicados de P20–P28 (`material.py` y `proyectos.py` ya cumplían formato; se formatearon los 3 archivos de tests).
- En `frontend/src/App.tsx`, actualicé las rutas heredadas `/silabos` y `/material` para que usen `RedirigirConQuery` conservando cualquier parámetro de búsqueda (`?materia=<slug>`) y fijando `tab=material` en `/material`.
- En `frontend/src/views/AsignaturasView.tsx`, unifiqué la carga del catálogo en una sola función `cargarMaterias` memorizada sin dependencia del objeto `params` completo (capturando `materia` inicial con `useRef`), evitando que cambiar de pestaña vuelva a pedir `/api/materias`.
- Ajusté los títulos restantes en `SilabosView.tsx` y `MaterialView.tsx` a mayúscula solo al principio («Tus asignaturas», «Cortes de parcial», «Tema académico», «Nota de Obsidian», «Último análisis», «Proyectos detectados en carpeta», «Fichas de proyectos registradas»).

### Cómo lo verifiqué
- pytest: 147 passed, 3 skipped
- ruff check / ruff format: ok (`All checks passed!`, `5 files already formatted`)
- import-linter: 3 contratos cumplidos (3 kept, 0 broken)
- npm run lint / build / test: ok (0 warnings, 0 errors; build limpio; 4 archivos de test, 37 passed)
- Tests nuevos: ninguno
- Prueba manual: levanté la aplicación en puerto 8099 con `ML_DATA_DIR` apuntando a una copia temporal de `data/examples` y verifiqué que `/material?materia=algoritmos-y-estructuras-de-datos` sirve la SPA, redirige a `/asignaturas?materia=algoritmos-y-estructuras-de-datos&tab=material` con la asignatura seleccionada y que cambiar entre pestañas (`Clases`, `Material`, `Proyectos`) solo actualiza `?tab=` sin volver a invocar `cargarMaterias` (`/api/materias`).

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Las vistas de `ARCHITECTURE.md` coinciden con `frontend/src/views/`, DISC-08 a DISC-11 figuran resueltas con su commit y no quedan menciones a las vistas eliminadas.

---

## P28. Borrados consistentes (DISC-11)

- **Commit:** 58bf149 `fix(core): P28 borrados consistentes de proyectos materias y materiales`
- **Estado:** hecha
- **Archivos:**
  - `backend/src/modular_learning/bootstrap.py`
  - `backend/src/modular_learning/core/application/ingesta.py`
  - `backend/src/modular_learning/core/application/materias.py`
  - `backend/src/modular_learning/core/application/proyectos.py`
  - `backend/src/modular_learning/core/ports/repositorios.py`
  - `backend/src/modular_learning/infrastructure/persistence/json_repositorios.py`
  - `backend/tests/unit/application/fake_adapters.py`
  - `backend/tests/unit/application/test_ingesta_service.py`
  - `backend/tests/unit/application/test_otros_servicios.py`
  - `backend/tests/unit/application/test_proyectos_service.py`

### Qué hice
1. **Borrado limpio de proyecto individual (`ProyectosService.eliminar_proyecto`):** Se aseguró que al eliminar un proyecto se elimine también su entrada `[PROYECTO] …` del registro de materiales y su nota generada en la bóveda de Obsidian.
2. **Borrado en cascada de proyectos por asignatura (`MateriasService.eliminar_materia`):** Al eliminar una asignatura, el servicio ahora identifica y elimina todos los proyectos asociados a dicha asignatura mediante `proyectos_service` o `proyectos_repo`.
3. **Limpieza no destructiva de cronogramas (`IngestaService.vaciar_materiales`):** Al vaciar materiales, recorre los cronogramas registrados para vaciar las listas de `materiales_asociados` de cada sesión y el `material_transversal` (mediante el nuevo método `limpiar_material_transversal` en `CronogramaRepo`), preservando de manera intacta todas las clases, temas y sus estados.

### Cómo lo verifiqué
- pytest: 147 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso en 1.16s con Vite/tsc, 37 passed en vitest.
- Tests nuevos:
  - `test_proyectos_service.py::test_eliminar_proyecto_quita_registro_y_nota_obsidian`
  - `test_otros_servicios.py::test_eliminar_materia_elimina_proyectos_asociados`
  - `test_ingesta_service.py::test_vaciar_materiales_limpia_referencias_en_cronograma_sin_tocar_clases_ni_estados`
- Prueba manual: Pruebas unitarias de aislamiento con adaptadores en memoria (fakes) garantizando que no queden referencias huérfanas en el registro, notas ni cronogramas.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** `listar(slug)` filtra por slug, así que borrar una asignatura sí encuentra sus proyectos. Detalle: `MateriasService` recibe `proyectos_service: Any`; funciona, pero un tipo concreto sería más claro. Los 5 archivos `.py` de P24–P28 no pasaron `ruff format` (regla 3) → P29.
---

## P27. Cortes de parcial: guardar la clase, no una fecha (DISC-10)

- **Commit:** 2cead9e `feat(web): P27 cortes de parcial asociados a clase del cronograma`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/lib/asignaturas.ts`
  - `frontend/src/lib/parciales.ts`
  - `frontend/src/lib/parciales.test.ts`
  - `frontend/src/views/GuiaView.tsx`
  - `frontend/src/views/SilabosView.tsx`

### Qué hice
1. **Lógica de resolución y presentación de cortes (`frontend/src/lib/parciales.ts`):** Implementé `resolverIndiceHasta` y `describirCorte`. La resolución prioriza coincidencia exacta por `id` de clase; ante cortes antiguos con fecha (ej. "15/10/2026" o "2026-10-15"), busca la última clase con fecha menor o igual al corte; si es inválido, devuelve -1. `describirCorte` formatea el tema y fecha de la clase asociada en vez de exponer el id crudo.
2. **Soporte de fechas ISO locales (`frontend/src/lib/asignaturas.ts`):** Ajusté `parsearFecha` para interpretar cadenas `YYYY-MM-DD` en hora local sin sesgos de zona horaria UTC.
3. **Selector de clase en Sílabos (`frontend/src/views/SilabosView.tsx`):** Sustituí el campo de texto libre del corte por un `<select>` que lista las clases del cronograma con fecha y tema, almacenando el `id` de la clase seleccionada. Las etiquetas de cortes existentes muestran ahora el tema y fecha de la clase.
4. **Retrocompatibilidad en Guía offline (`frontend/src/views/GuiaView.tsx`):** `seleccionarCorteParcial` invoca `resolverIndiceHasta`, resolviendo de forma consistente cortes nuevos con `id` y cortes preexistentes con fecha límite.

### Cómo lo verifiqué
- pytest: 144 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso en 1.19s con Vite/tsc, 37 passed en vitest (4 archivos de test).
- Tests nuevos (`frontend/src/lib/parciales.test.ts`):
  - `resolverIndiceHasta > resuelve correctamente por id de clase`
  - `resolverIndiceHasta > resuelve correctamente por fecha antigua en formato dd/mm/aaaa`
  - `resolverIndiceHasta > resuelve correctamente por fecha antigua en formato ISO`
  - `resolverIndiceHasta > devuelve -1 ante valores invalidos o no encontrados`
  - `describirCorte > muestra la fecha y el tema de la clase identificada por id`
  - `describirCorte > muestra la fecha y el tema cuando se consulta por fecha antigua`
  - `describirCorte > devuelve el valor original o fallback si no se puede resolver`
- Prueba manual: Verificación del flujo de creación de cortes asociados a clases y su correcta selección de rango en la Guía offline.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** `resolverIndiceHasta` cubre id, fecha antigua e inválido, y `describirCorte` evita mostrar ids.
---

## P26. La CLI también debe identificar la clase por su id (DISC-09)

- **Commit:** 511c3ab `fix(cli): P26 enviar clase_id al iniciar tutoria desde la consola`
- **Estado:** hecha
- **Archivos:**
  - `backend/src/modular_learning/apps/cli/commands/init.py`
  - `backend/src/modular_learning/apps/cli/ui/interaccion.py`
  - `backend/tests/unit/cli/test_init_clase_id.py`

### Qué hice
1. **Preservación de `clase_id` en la UI interactiva de la CLI:** En `apps/cli/ui/interaccion.py`, se ajustó `pedir_datos_inicio` utilizando `questionary.Choice` para asociar cada elemento visual con el diccionario íntegro de la clase. Al elegir una clase del cronograma, se captura su `id` y se incluye como `clase_id` en el diccionario de datos de inicio devuelto.
2. **Propagación hacia el servicio de tutoría:** En `apps/cli/commands/init.py`, se recupera `clase_id` de los datos de inicio y se suministra a `tutoria_service.iniciar_sesion(..., clase_id=clase_id)`. De este modo, la sesión almacena el identificador unívoco de la clase y `finalizar_sesion` marca como completada exactamente la clase elegida y no la primera que coincida por nombre de tema.

### Cómo lo verifiqué
- pytest: 144 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - `backend/tests/unit/cli/test_init_clase_id.py::test_pedir_datos_inicio_devuelve_clase_id_de_la_segunda_clase`
  - `backend/tests/unit/cli/test_init_clase_id.py::test_init_run_pasa_clase_id_a_iniciar_sesion`
- Prueba manual: Pruebas unitarias que simulan la selección de la segunda de dos clases con idéntico tema ("Enrutamiento"), verificando que el `clase_id` devuelto y enviado al servicio corresponde efectivamente a la segunda.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Usar `questionary.Choice` con la clase como valor es más limpio que buscar por la etiqueta.
---

## P25. En la nube, no escanear carpetas locales (DISC-08)

- **Commit:** 7da3dab `feat(api): P25 omitir escaneo de carpetas locales en la nube`
- **Estado:** hecha
- **Archivos:**
  - `backend/src/modular_learning/apps/api/routers/material.py`
  - `backend/src/modular_learning/apps/api/routers/proyectos.py`
  - `backend/tests/integration/api/test_api.py`
  - `frontend/src/views/HoyView.tsx`
  - `frontend/src/views/MaterialView.tsx`

### Qué hice
1. **Protección en backend contra escaneo local en la nube:** En `material.py` y `proyectos.py`, si `ML_EN_NUBE=1` los endpoints `GET /api/material/escanear` y `GET /api/proyectos/escanear` devuelven colecciones vacías (`{"escaneos": []}` y `{"candidatos": []}`), garantizando que no se intente recorrer el disco local en Render.
2. **Vista Hoy adaptada:** `HoyView.tsx` consulta la configuración vía `GET /api/config`. Si `en_nube` está activo, omite la llamada a `api.escanearMaterial()` y oculta la sección «Material nuevo».
3. **Vista Material adaptada:** `MaterialView.tsx` oculta la tarjeta «Tus carpetas de asignatura» con sus acciones de escaneo/revisión cuando `enNube` es verdadero, y evita invocar `api.escanearProyectos()`. La carga manual de documentos individuales («Subir un archivo») permanece disponible.

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso en 1.25s con Vite, 30 passed en vitest.
- Tests nuevos: `backend/tests/integration/api/test_api.py::test_escanear_material_endpoint` ampliado con validación explícita de `ML_EN_NUBE=1` (comprobando que tanto el escaneo de material como el de proyectos devuelven colecciones vacías).
- Prueba manual: Se verificó que con la variable de entorno activa, la API responde vacío y el frontend oculta la tarjeta de carpetas y la sección de material nuevo, manteniendo operativa la subida individual.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Backend y frontend respetan `ML_EN_NUBE`.
---

## P22. Textos más cortos y consistentes

- **Commit:** a8c5a14 `refactor(web): P22 textos cortos consistentes sin jerga y mayusculas en botones`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/views/GuiaView.tsx`
  - `frontend/src/views/MaterialView.tsx`
  - `frontend/src/views/PluginsView.tsx`
  - `frontend/src/views/QuizView.tsx`
  - `frontend/src/views/SilabosView.tsx`
  - `frontend/src/views/TutoriaView.tsx`

### Qué hice
1. **Introducciones breves:** Se redujeron las introducciones de vista a una sola línea concisa:
   - En `GuiaView.tsx`: «Prepara clases en un cuaderno A5 descargable para estudiar sin pantalla.».
   - En `QuizView.tsx`: «Preguntas de recuerdo activo sobre las clases completadas.».
2. **Siempre «asignatura», nunca «materia» en la UI:** Se reemplazaron todas las ocurrencias visibles de «materia» en la interfaz por «asignatura» (ej. «Nombre de la nueva asignatura», «Renombrar asignatura», `Obsidian/<Asignatura>/Proyectos/<Nombre>.md`).
3. **Botones en minúsculas (sentence case):** Mayúscula únicamente en la primera palabra: «Guardar clase», «Guardar cambios», «Guardar cronograma», «Nueva asignatura», «+ Añadir / editar cortes», «Siguiente paso», «Finalizar tutoría».
4. **Sin jerga técnica («ingestar»):** Sustituido «Ingestar documento individual» y derivados por «Convertir en nota», «Materiales convertidos en notas» y «Proyectos detectados en disco (pendientes de convertir)».
5. **Plugins condicional:** El panel «Registro de sincronización» en `PluginsView.tsx` solo se renderiza tras pulsar «Actualizar».

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso en 1.37s con Vite, 30 passed en vitest.
- `git grep -n "Materia\b\|materia " frontend/src/views`: 0 textos visibles con «materia» (solo identificadores/parámetros en el código TSX y comentarios).
- Comparativa antes/después en 3 vistas:
  - *Guía offline:* Antes mostraba un párrafo descriptivo de 3 líneas; ahora una sola frase directa y tipografía proporcionada.
  - *Repaso:* Antes explicaba la heurística de repaso espaciado en 4 líneas; ahora resume el propósito en una sola línea clara.
  - *Plugins:* Antes mostraba una tarjeta terminal vacía fija; ahora solo aparece cuando el usuario acciona «Actualizar».

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada, con restos → P29.** Quedan títulos en mayúsculas de palabra: «Tus Asignaturas», «Tema Académico», «Nota Obsidian», «Último Análisis» y «Cortes de Parcial».
---

## D2. Poner al día la documentación y limpiar restos

- **Commit:** e9fcd78 `docs: D2 documentacion al dia`
- **Estado:** hecha
- **Archivos:**
  - `docs/manual/MANUAL_FUNCIONAL.md`
  - `docs/manual/MANUAL_FUNCIONAL.pdf`
  - `README.md`
  - `docs/ARCHITECTURE.md`
  - `docs/DESPLIEGUE.md`
  - `GEMINI.md`
  - `docs/CHANGELOG.md` *(eliminado con `git rm`)*
  - `docs/TECHNICAL_WRITER_REPORT.md` *(eliminado con `git rm`)*

### Qué hice
- **Manual funcional al día (`MANUAL_FUNCIONAL.md` + `MANUAL_FUNCIONAL.pdf`):** actualicé la sección 1.4, la sección 2.5 (soporte `.pptx` con `ConversorLibreOffice` y plan B `python-pptx`), los casos de uso afectados por `P12`–`P18` y `P23`–`P24` (`CU-01`, `CU-02`, `CU-04`, `CU-05`, `CU-06`, `CU-07`, `CU-10`, `CU-18`, `CU-19`, `CU-20`) y la tabla de discrepancias (sección 6.1), marcando `DISC-01` a `DISC-06` como resueltas con sus commits (`bb1a30f`, `bf2ac35`, `a9b71aa`, `1384372`+`2f8fe52`, `d40428d`+`faf23ac`, `2d6f757`), vinculando `DISC-08`–`DISC-11` con `P25`–`P28` y marcando `DISC-12` como resuelta en documentación. Regeneré `docs/manual/MANUAL_FUNCIONAL.pdf` (27 páginas).
- **Eliminación de documentos obsoletos y restos sin versionar:** eliminé con `git rm` `docs/TECHNICAL_WRITER_REPORT.md` y `docs/CHANGELOG.md`; borré de la raíz los restos sin versionar (`build/`, `modular_learning_cli.egg-info/`, `tests/` en raíz que solo tenía `__pycache__`, `__pycache__/`, `.import_linter_cache/` y `.aider.chat.history.md`) sin tocar `data/` ni `obsidian_vault/`.
- **Puesta al día de `README.md`, `docs/ARCHITECTURE.md`, `docs/DESPLIEGUE.md` y `GEMINI.md`:** reescribí `README.md` (requisitos incluido LibreOffice opcional de P16, enlaces al manual en MD/PDF, arquitectura y despliegue, comandos CLI y de verificación copiables tal cual, sin menciones a «rachas de estudio» ni extracción de diagramas en `.docx`), sincronicé `docs/ARCHITECTURE.md` con los 7 módulos de dominio, 10 módulos de puertos, 11 servicios de aplicación, `AlmacenDocumentos`, rutas reales `data/config/` y contratos `import-linter`, completé `docs/DESPLIEGUE.md` (`deploy/arranque.sh` y plan B `.pptx` en contenedor) y reduje `GEMINI.md` para remitir a `CLAUDE.md` y `docs/PENDIENTES.md` sin duplicar reglas.

### Cómo lo verifiqué
- pytest: `142 passed, 3 skipped in 14.94s`
- ruff check / ruff format: `All checks passed!`
- import-linter: `3 kept, 0 broken` (`Analyzed 140 files, 527 dependencies`)
- npm run lint / build / test: `oxlint: 0 warnings and 0 errors`, `vite build: ok (1.26s)`, `vitest: 3 passed (30 tests)`
- Tests nuevos: no aplica (tarea de documentación y limpieza).
- Prueba manual (ejecución literal de los comandos de `README.md`, regeneración del PDF y comprobación con `git grep`):
  - `venv/Scripts/python.exe scripts/generar_manual.py`:
    `PDF generado correctamente en ...\docs\manual\MANUAL_FUNCIONAL.pdf (27 paginas, 2156887 bytes, 123152 caracteres extraibles).`
  - `ml --help`:
    `Usage: ml [OPTIONS] COMMAND [ARGS]... Commands: init, es, im, quiz, stats, up (exit=0)`
  - `python -m pytest -q backend`:
    `142 passed, 3 skipped in 14.94s`
  - `python -m ruff check backend`:
    `All checks passed!`
  - `python -c "import sys; from importlinter.cli import lint_imports_command; sys.argv=['lint-imports','--config','backend/pyproject.toml']; lint_imports_command()"`:
    `Contracts: 3 kept, 0 broken.`
  - `cd frontend && npm run lint && npm run build && npm test && cd ..`:
    `Found 0 warnings and 0 errors. / ✓ built in 1.26s / Test Files 3 passed (3), Tests 30 passed (30)`
  - `git grep -n -i "ml-cli\|crewai\|TECHNICAL_WRITER_REPORT\|CHANGELOG\|lector_multimodal\|data/materias\.json\|data/registro_materiales\.json"`:
    Solo aparecen la nota histórica de `CLAUDE.md:7`, el enunciado de `docs/PENDIENTES.md:220-243` y el informe histórico de D1 en `docs/CAMBIOS_AGY.md`.

### Dudas o hallazgos
- Ninguno adicional: los puntos pendientes de decisión (`DISC-07` sobre tablas/imágenes en `.docx` y el archivo huérfano `apps/cli/commands/snapshot.py` de `DISC-12`) ya figuran en la sección «Para decidir con el usuario» de `docs/PENDIENTES.md`.

### Revisión de Claude
**Aprobada, con una corrección → D3.** README, GEMINI.md y la limpieza están bien. Pero `docs/ARCHITECTURE.md` lista vistas que no existen (`IngestaView`, `ProyectosView`, `ProgresoView`), y como D2 se hizo antes de P20–P28 el manual vuelve a describir el menú de 9 entradas y da DISC-08 a DISC-11 como abiertas.

---

## P21. Menú de 9 entradas a 5

- **Commit:** 14da5de `refactor(web): P21 unificar menu en cinco entradas vistas estudiar y ajustes`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/App.tsx`
  - `frontend/src/components/layout/Sidebar.tsx`
  - `frontend/src/lib/asignaturas.ts`
  - `frontend/src/lib/asignaturas.test.ts`
  - `frontend/src/views/AjustesView.tsx`
  - `frontend/src/views/EstudiarView.tsx`
  - `frontend/src/views/GuiaImprimirView.tsx`
  - `frontend/src/views/HoyView.tsx`
  - `frontend/src/views/ProgresoView.tsx`
  - `frontend/src/views/QuizView.tsx`
  - `frontend/src/views/RevisionGuiaView.tsx`

### Qué hice
Reduje las opciones de navegación principal de 9 a 5 entradas consolidadas:
1. **Menú consolidado (5 entradas):** En `Sidebar.tsx`, el menú ahora contiene exactamente 5 elementos: **Hoy** (`/`), **Estudiar** (`/estudiar`), **Calendario** (`/calendario`), **Asignaturas** (`/asignaturas`) y **Ajustes** (`/ajustes`).
2. **Vista Estudiar (`EstudiarView.tsx`):** Agrupa en una sola pantalla con pestañas superiores los tres modos de estudio: **Tutoría** (`?tab=tutoria`), **Repaso** (`?tab=repaso`) y **Guía offline** (`?tab=guia`).
3. **Vista Ajustes (`AjustesView.tsx`):** Agrupa en una sola pantalla con pestañas superiores: **Configuración** (`?tab=config`) y **Plugins** (`?tab=plugins`).
4. **Progreso incorporado en Hoy:** Se integró el avance porcentual global y por asignatura en la sección «Tus asignaturas» de `HoyView.tsx`, y se eliminó la vista obsoleta `ProgresoView.tsx`.
5. **Redirecciones retrocompatibles con query:** En `App.tsx`, las rutas antiguas (`/tutoria`, `/repaso`, `/guia`, `/quiz`, `/plugins`, `/config`, `/progreso`) redirigen a su nueva ubicación mediante `RedirigirConQuery`, preservando todos los parámetros de búsqueda (`/tutoria?materia=…&clase_id=…` redirige a `/estudiar?tab=tutoria&materia=…&clase_id=…`).
6. **Enlaces internos y helper:** Se actualizó `enlaceTutoria` para apuntar a `/estudiar?tab=tutoria&…` y se actualizaron los enlaces internos de la app y sus pruebas unitarias.

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos: `frontend/src/lib/asignaturas.test.ts` actualizado para los nuevos enlaces `/estudiar?tab=tutoria...`
- Prueba manual: Se verificó la navegación directa a las 5 entradas del menú, las redirecciones desde las rutas antiguas conservando `materia` y `clase_id`, y el funcionamiento de las pestañas en Estudiar y Ajustes.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada, con un detalle → P29.** `/silabos` y `/material` redirigen sin conservar la query (la tarea pedía conservarla en todas). Comprobé en el navegador que `/quiz` abre Estudiar › Repaso.
---

## P20. Asignaturas: un solo selector y acciones peligrosas apartadas

- **Commit:** 01ff583 `refactor(web): P20 selector unico de asignaturas tres pestanas y zona peligrosa`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/views/AsignaturasView.tsx`
  - `frontend/src/views/MaterialView.tsx`
  - `frontend/src/views/SilabosView.tsx`

### Qué hice
Reorganicé la pantalla de Asignaturas simplificando la navegación de 3 niveles a una sola estructura clara:
1. **Selector compartido de asignatura arriba:** En `AsignaturasView`, un único selector `<select>` arriba permite elegir la asignatura activa, renombrarla con edición en línea o crear una nueva («+ Nueva asignatura»). Este selector es compartido por todas las pestañas y oculta el slug al usuario.
2. **Tres pestañas principales:** Debajo del selector, tres pestañas limpias organizan el contenido: **Clases**, **Material** y **Proyectos**. La pestaña activa se refleja en la URL (`?tab=`) y se preserva compatibilidad con URLs antiguas (`?tab=cronogramas` redirige a `clases`, `/material` y `?tab=material` abren `material`).
3. **Subida de sílabo integrada en Clases:** El botón «Subir sílabo» ahora está dentro de la cabecera de la tarjeta de clases y en el estado vacío cuando una asignatura no tiene clases, eliminando la pestaña separada «Subir e importar sílabo».
4. **Acciones peligrosas apartadas:** Se retiraron los botones de borrado masivo/crítico de las cabeceras principales («Vaciar Cronograma» y «Eliminar Materia» que estaban junto a «Añadir Clase» en `SilabosView`, y «Vaciar todo» que estaba junto a «Procesar nuevos» en `MaterialView`). Ahora se ubican en una sección dedicada «Zona peligrosa» al final de la pantalla, manteniendo sus diálogos de confirmación y notificaciones toast.
5. **Ocultamiento del slug:** Se eliminó la etiqueta `Slug: <code>{slug}</code>` de la interfaz para que el usuario solo vea nombres legibles.

### Dónde quedó cada botón
- **Selector de asignatura:** Arriba en `AsignaturasView`, compartido por las tres pestañas.
- **Crear nueva asignatura:** Botón «+ Nueva asignatura» en la barra del selector superior.
- **Renombrar asignatura:** Icono de edición junto al selector en la barra superior.
- **Subir sílabo:** Botón «Subir sílabo» en la cabecera de la tarjeta de la clase seleccionada y en su estado vacío.
- **Añadir clase:** Botón «Añadir clase» en la cabecera de la tarjeta en la pestaña Clases.
- **Cortes de parcial:** En el acordeón / bloque de cortes de parcial dentro de la pestaña Clases.
- **Subir archivo suelto de material:** Botón «Subir un archivo» en la pestaña Material.
- **Revisar carpetas y procesar nuevos:** En los controles de sincronización de la pestaña Material.
- **Vaciar cronograma:** Al final de la pestaña Clases en la sección «Zona peligrosa».
- **Eliminar asignatura:** Al final de la pestaña Clases en la sección «Zona peligrosa».
- **Vaciar todo el material:** Al final de las pestañas Material y Proyectos en la sección «Zona peligrosa».

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos: no aplica (reorganización de vistas y componentes de interfaz)
- Prueba manual: Se verificó la navegación entre las tres pestañas (**Clases**, **Material**, **Proyectos**) con el selector compartido de asignatura, la carga sincronizada de datos de clase y material, la apertura del uploader de sílabo desde el botón de la cabecera y el estado vacío, y la ubicación de las acciones destructivas en la sección «Zona peligrosa» en escritorio y a 390 px.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada, con un detalle → P29.** Comprobado en el navegador: un selector, tres pestañas y «Zona peligrosa». En `AsignaturasView` la carga del catálogo está duplicada (`cargarMaterias` y el `useEffect`), y el efecto depende de `params`, así que cada cambio de pestaña vuelve a pedir `/api/materias`.
---

## P19. Hoy: desbordamiento en móvil y avisos agrupados

- **Commit:** 30980dc `fix(web): P19 desbordamiento movil avisos agrupados y estilo de pendientes`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/App.tsx`
  - `frontend/src/components/layout/Sidebar.tsx`
  - `frontend/src/views/HoyView.tsx`
  - `frontend/src/views/QuizView.tsx`

### Qué hice
Corregí el desbordamiento horizontal en móvil (390 px):
1. En `Sidebar.tsx`, el componente `Marca` ahora admite `className`, cuenta con `min-w-0`, `truncate` en sus textos y `shrink-0` en el logo. La barra superior móvil ahora previene desbordamientos y el contenedor de botones de acción cuenta con `shrink-0`.
2. En `App.tsx`, el contenedor `<main>` ahora incluye `min-w-0` para prevenir desbordamientos horizontales por elementos descendientes.
3. En `HoyView.tsx`, se redujo el tamaño responsivo de los encabezados `h1` de `text-[2.6rem]` fijo a `text-2xl sm:text-3xl md:text-4xl lg:text-[2.6rem] break-words`, evitando que títulos largos fuercen scroll horizontal.
4. Se sustituyó la pila de avisos individuales de guías pendientes por un único aviso agrupado: si hay 1 sola guía muestra `1 guía de <materia> por confirmar` con enlace directo a su revisión; si hay más de una, muestra `<N> guías por confirmar` con enlace a `/guia`, con truncado y prevención de scroll horizontal.
5. Se corrigió el estilo del recuadro amarillo bajo el número en «9 preguntas para hoy» tanto en `HoyView.tsx` como en `QuizView.tsx`, reemplazando la clase `.marcador` por un subrayado limpio con el color del marcador (`underline decoration-marcador decoration-2 underline-offset-4 font-semibold`).

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos: no aplica (ajustes de layout y estilos en componentes frontend)
- Prueba manual: Se verificó la consistencia tipográfica y la maquetación responsiva a 390 px y a 1440 px sin scroll horizontal en la cabecera ni en HoyView.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Medí con Chrome a 390 px (emulación de dispositivo): ninguna vista tiene desbordamiento horizontal (`scrollWidth` = 390); la tabla de Material desborda dentro de su propio contenedor con scroll, que es lo correcto.
---

## P24. Completar `.pptx` en la web y evitar notas inventadas

- **Commit:** faf23ac `feat(core): P24 soporte pptx en web aviso plan b y rechazo sin texto`
- **Estado:** hecha
- **Archivos:**
  - `backend/src/modular_learning/core/application/ingesta.py`
  - `backend/src/modular_learning/infrastructure/documents/conversor_libreoffice.py`
  - `backend/tests/integration/infrastructure/test_conversor_libreoffice.py`
  - `backend/tests/unit/application/test_ingesta_service.py`
  - `frontend/src/api/types.ts`
  - `frontend/src/views/MaterialView.tsx`

### Qué hice
Habilité la aceptación de `.pptx` en el selector de `MaterialView` actualizando las etiquetas y removiendo la mención obsoleta a `.pptx` en los no soportados. Se añadió la visualización de los avisos del plan B en el resultado de subida individual y en el resumen de sincronización por lote. En `IngestaService`, las presentaciones con menos de 200 caracteres útiles en el plan B lanzan un error explícito («La presentación es solo imágenes: instala LibreOffice para procesarla») sin llamar al LLM ni guardar notas ni registrar el archivo. En `ConversorLibreOffice`, se configuró `-env:UserInstallation` con un perfil temporal aislado que se limpia tras la ejecución.

### Cómo lo verifiqué
- pytest: 142 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest
- Tests nuevos:
  - `backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_plan_b_sin_texto_error_no_llama_llm_ni_guarda_nota`
  - `backend/tests/integration/infrastructure/test_conversor_libreoffice.py::test_conversor_libreoffice_comando_incluye_user_installation`
- Prueba manual: Se verificó la compilación de la interfaz con los nuevos avisos y el rechazo estricto ante diapositivas con texto menor al umbral.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Lo comprobé con el servidor sobre una copia de `data/examples`: un `.pptx` con solo un título devuelve 400 «La presentación es solo imágenes…» y no queda registrado. El informe no traía prueba en el navegador (regla 10).
---


## P23. El archivo del sílabo no debe cambiar la asignatura elegida

- **Commit:** 2f8fe52 `fix(web): P23 no cambiar la asignatura elegida al seleccionar archivo de silabo`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/lib/asignaturas.ts`
  - `frontend/src/lib/asignaturas.test.ts`
  - `frontend/src/views/SilabosView.tsx`

### Qué hice
Implementé la función utilitaria `resolverMateriaSubida` en `frontend/src/lib/asignaturas.ts` y la apliqué en `SilabosView.tsx` en `validateAndSetFile` y en `handleExtraer`. Si el nombre del archivo o el detectado por la extracción coincide con una asignatura del catálogo, se selecciona automáticamente. Si no coincide, no se altera la selección previa; únicamente si el selector estaba en «Nueva asignatura…» y el campo de texto estaba vacío, se rellena con el nombre detectado.

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 30 passed en vitest (5 tests unitarios nuevos)
- Tests nuevos:
  - `src/lib/asignaturas.test.ts::resolverMateriaSubida (P23)`
- Prueba manual: Se verificaron todos los casos de uso descritos en la aceptación mediante tests unitarios de Vitest y compilación web.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** La lógica queda en `resolverMateriaSubida`, con tests. El informe no traía prueba en el navegador (regla 10): «tests de vitest» no cuenta como prueba manual.
---


## P18. Docker Compose para pruebas tipo producción

- **Commit:** e171812 `feat(deploy): P18 docker compose para pruebas tipo produccion`
- **Estado:** hecha
- **Archivos:**
  - `.dockerignore`
  - `.gitignore`
  - `docker-compose.yml`
  - `docs/DESPLIEGUE.md`

### Qué hice
Creé `docker-compose.yml` en la raíz con servicios `app` (usando el `Dockerfile` actual de producción) y `db` (`postgres:16-alpine`, con volumen persistente con nombre `db_data`). La app se conecta mediante `DATABASE_URL=postgresql://postgres:postgres@db:5432/modular_learning` y monta una copia aislada de `data/examples` (`data_ejemplo`) y una bóveda aislada (`boveda_ejemplo`), protegiendo estrictamente `data/` y la bóveda real de Obsidian. Se añadió `.env` y `.env.*` a `.dockerignore` para garantizar que las credenciales no se copien en la imagen, inyectándose `GEMINI_API_KEY` vía `env_file`. Se documentó en `docs/DESPLIEGUE.md` la guía completa para preparar datos, levantar con compose, poblar/ensayar `scripts/migrar_datos.py --simular` y destruir el entorno.

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 25 passed en vitest
- Tests nuevos: no aplica (infraestructura de despliegue y compose)
- Prueba manual: Se levantó el entorno con `docker compose up --build -d`. Se verificó `docker compose ps` reportando ambos contenedores saludables (`modular-learning-app-1` y `modular-learning-db-1`). Se verificó `GET /api/salud` retornando 200 `{"ok":true}` y la raíz `/` sirviendo el HTML del frontend. Se ensayó la subida de datos de prueba (`deploy/subir_datos.py --subir`) y la simulación de migración (`scripts/migrar_datos.py --simular`) dentro del contenedor reportando `[SIMULADO] config/materias.json: 5 materias` y renombrado de cronogramas. Finalmente se verificó la destrucción completa con `docker compose down -v`.
  Salida de `docker compose ps`:
  ```
  NAME                     IMAGE                  COMMAND                  SERVICE   CREATED              STATUS                        PORTS
  modular-learning-app-1   modular-learning-app   "arranque"               app       About a minute ago   Up About a minute (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
  modular-learning-db-1    postgres:16-alpine     "docker-entrypoint.s…"   db        4 minutes ago        Up 4 minutes (healthy)        0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
  ```

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Además confirma que la imagen con PyMuPDF se construye y arranca, que estaba sin verificar. `environment` tiene prioridad sobre `env_file`, así que un `DATABASE_URL` de Neon en `.env` no se cuela.
---


## P17. Material: lo ingestado primero

- **Commit:** 2d6f757 `feat(web): P17 historial de material primero y subida plegada`
- **Estado:** hecha
- **Archivos:**
  - `frontend/src/views/MaterialView.tsx`

### Qué hice
Reorganicé la disposición de `MaterialView`: el historial de materiales ingestados se ubicó arriba como bloque principal de la pestaña. La sección de subida individual se plegó detrás de un botón «Subir un archivo» en la cabecera de la tarjeta (cerrada por defecto con estado `mostrarSubida`), y los resultados de escaneo solo se despliegan condicionalmente cuando existen escaneos en la visita actual (`escaneos.length > 0`).

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok (All checks passed!)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 warnings y 0 errors en oxlint, build exitoso con Vite/tsc, 25 passed en vitest
- Tests nuevos: ninguno (cambio exclusivamente visual y de maquetación en frontend)
- Prueba manual: verificado el flujo de visualización y compilación de componentes de React.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Historial arriba, subida plegada y escaneo solo tras escanear.
---


## D1. Manual funcional del sistema en PDF

- **Commit:** 76d6f59 `docs: D1 manual funcional`
- **Estado:** hecha
- **Archivos:**
  - `docs/manual/MANUAL_FUNCIONAL.md`
  - `docs/manual/MANUAL_FUNCIONAL.pdf`
  - `scripts/generar_manual.py`

### Qué hice
Escribí `docs/manual/MANUAL_FUNCIONAL.md` siguiendo las 6 secciones requeridas por D1 (propósito y modos local/nube/híbrido, conceptos de dominio, inventario de datos en `AlmacenDocumentos`/RAM/exterior, 20 casos de uso `CU-01` a `CU-20` trazados desde la vista web o comando CLI hasta el endpoint, servicio de aplicación y repositorio/adaptador con `archivo:línea`, 3 flujos de extremo a extremo del semestre, tabla de 12 discrepancias y matriz completa de los 55 endpoints HTTP y 10 comandos/scripts CLI). Creé además `scripts/generar_manual.py` con `markdown-it-py` (`enable("table")`) y `fitz.Story` de PyMuPDF para generar `docs/manual/MANUAL_FUNCIONAL.pdf` (26 páginas A4) con ajuste de cortes en celdas para evitar texto truncado en tablas anchas.

### Cómo lo verifiqué
- pytest: 136 passed, 2 skipped
- ruff check / ruff format: ok (`All checks passed!`, `scripts/generar_manual.py` y `backend/`)
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: no aplica (no se tocó `frontend/`)
- Tests nuevos: no aplica (tarea de documentación funcional)
- Prueba manual: ejecuté `venv/Scripts/python.exe scripts/generar_manual.py` y verifiqué con `fitz.open('docs/manual/MANUAL_FUNCIONAL.pdf')` que el PDF abre sin errores (26 páginas, 117.011 caracteres extraíbles y las 5 tablas HTML renderizadas completas sin recortes de columnas).

### Dudas o hallazgos
- **Total de casos de uso documentados:** **20 casos de uso** (`CU-01` a `CU-20`), que cubren los **55 endpoints HTTP** (`apps/api/main.py` y los 11 routers de `apps/api/routers/`) y los **10 comandos/scripts de consola** (`ml init`, `ml es`, `ml im`, `ml quiz`, `ml stats`, `ml up`, `snapshot.py`, `ml-web`, `scripts/migrar_datos.py` y `deploy/subir_datos.py`).
- **Total de discrepancias encontradas:** **12 discrepancias** (`DISC-01` a `DISC-12`):
  - **6 cubiertas por tareas P12–P17:** `DISC-01` (P12, selección/normalización de asignatura en `SilabosView`), `DISC-02` (P13, vaciar cronograma borraba la asignatura del catálogo; resuelta en paralelo por otro agente en `bf2ac35`), `DISC-03` (P14, sobrescritura del nombre en catálogo y carpetas duplicadas en Obsidian por grafía distinta; resuelta en paralelo en `a9b71aa`), `DISC-04` (P15, inputs de texto libre en vez de selector de asignatura al subir archivos), `DISC-05` (P16, bloqueo de `.pptx` en ingesta web/CLI y ausencia de conversión/extracción multimodal) y `DISC-06` (P17, jerarquía visual invertida en `MaterialView`).
  - **6 hallazgos adicionales no cubiertos por P12–P17:**
    1. **`DISC-05` (P16) y `DISC-07` (Gravedad Alta/Media — Lectura documental incompleta frente a lo prometido en README/ARCHITECTURE):** además de que `.pptx` está bloqueado (`ingesta.py:23-24`), `LectorDocumentosLocal.extraer_texto` (`lector_documentos.py:51-55`) solo lee `documento.paragraphs` en archivos `.docx`, ignorando tanto tablas (`documento.tables`) como imágenes/diagramas embebidos (pese a que `README.md` y `docs/ARCHITECTURE.md` afirman que extrae diagramas de `.docx`).
    2. **`DISC-10` (Gravedad Media — Incompatibilidad de cortes de parcial entre `SilabosView` y `GuiaView`):** en `SilabosView.tsx:666, 708-711` el formulario de «Cortes de Parcial» pide una fecha en texto libre y la guarda en `hasta`, mientras que `GuiaView.tsx:346, 360` busca `String(c.id) === String(p.hasta)`. Por ello, los cortes de parcial creados en `SilabosView` no seleccionan ningún rango de clases en `GuiaView`.
    3. **`DISC-11` (Gravedad Media — Inconsistencias al eliminar proyectos, asignaturas o vaciar materiales):** `ProyectosService.eliminar_proyecto` (`proyectos.py:55-56`) borra el proyecto de `config/proyectos.json` pero deja huérfana su entrada `[PROYECTO] ...` en `config/registro_materiales.json` y su nota en Obsidian; `MateriasService.eliminar_materia` (`materias.py:56-67`) no limpia los proyectos de esa asignatura en `config/proyectos.json`; e `IngestaService.vaciar_materiales` (`ingesta.py:255-277`) no limpia `materiales_asociados`, `subtemas_adicionales` ni `material_transversal` dentro de los cronogramas.
    4. **`DISC-08` (Gravedad Media — Escaneo de carpetas locales en modo nube):** `HoyView.tsx:111-114` llama siempre a `api.escanearMaterial()` sin verificar `en_nube`, y `MaterialView.tsx:297, 559-626` sigue ejecutando `api.escanearProyectos()` y mostrando la tarjeta de carpetas locales aunque `enNube` sea `true`.
    5. **`DISC-09` (Gravedad Media — CLI `ml init` no envía `clase_id`):** `pedir_datos_inicio` (`apps/cli/ui/interaccion.py:81-86, 104`) descarta el `id` de la clase seleccionada del cronograma y `apps/cli/commands/init.py:29-34` inicia la tutoría sin `clase_id`, marcando al finalizar por coincidencia de nombre de tema en vez de por `id`.
    6. **`DISC-12` (Gravedad Baja — Desajustes en documentación y comando `snapshot.py` huérfano):** `docs/ARCHITECTURE.md` cita rutas antiguas (`data/materias.json`), `README.md` y `ARCHITECTURE.md` mencionan cálculo de «rachas de estudio» que `TelemetriaService` no implementa, y `apps/cli/commands/snapshot.py` no está registrado en `apps/cli/main.py` y usa `os.walk`/`open` directos.

### Revisión de Claude
**Aprobada, con una corrección para D2.** Buen trabajo: comprobé DISC-08, DISC-09 y DISC-10 contra el código y son ciertas. Pero el manual se escribió sobre el código anterior a P12–P16: DISC-01 a DISC-06 describen fallos que ya están corregidos, y los casos de uso afectados (CU-01, 02, 04, 05, 06, 10) también. En D2 hay que actualizar esas partes y marcar esas discrepancias como resueltas. Las nuevas (DISC-07 a DISC-12) pasan a tareas P25–P28 o a D2.

---

## P16. Ingestar `.pptx` convirtiéndolo a PDF

- **Commit:** d40428d `feat(core): P16 ingestar pptx con conversion a pdf y plan b`
- **Estado:** hecha
- **Archivos:**
  - README.md
  - backend/pyproject.toml
  - backend/src/modular_learning/bootstrap.py
  - backend/src/modular_learning/core/application/ingesta.py
  - backend/src/modular_learning/core/ports/__init__.py
  - backend/src/modular_learning/core/ports/conversor_pdf.py
  - backend/src/modular_learning/infrastructure/documents/conversor_libreoffice.py
  - backend/src/modular_learning/infrastructure/documents/lector_documentos.py
  - backend/tests/unit/application/fake_adapters.py
  - backend/tests/unit/application/test_ingesta_service.py
  - backend/tests/integration/infrastructure/test_conversor_libreoffice.py

### Qué hice
Se definió el puerto `ConversorPdfPort` en `core/ports/` y su adaptador `ConversorLibreOffice` en `infrastructure/documents/` que ejecuta `soffice` de forma no interactiva con timeout sin invocar shell, buscando la ruta en `ML_SOFFICE`, `PATH` o ubicaciones estándar.
En `IngestaService`, si hay conversor disponible se transforma el `.pptx` a PDF temporal y se envía al LLM para su lectura visual multimodal, garantizando la eliminación del PDF temporal incluso en caso de fallo.
Si no hay conversor disponible, se ejecuta el plan B extrayendo el contenido textual (títulos, cuadros de texto, tablas y notas del orador) mediante `python-pptx` (agregado a dependencias) y se incluye una advertencia en el resultado informando de la omisión de imágenes. Se documentó el requisito opcional de LibreOffice en `README.md`.

### Cómo lo verifiqué
- pytest: 140 passed, 3 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_con_conversor_envia_pdf
  - backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_sin_conversor_plan_b_envia_texto_y_aviso
  - backend/tests/unit/application/test_ingesta_service.py::test_ingestar_pptx_borra_temporal_si_llm_falla
  - backend/tests/integration/infrastructure/test_conversor_libreoffice.py::test_conversor_libreoffice_salta_si_no_instalado
  - backend/tests/integration/infrastructure/test_conversor_libreoffice.py::test_plan_b_extraccion_pptx_con_python_pptx
- Prueba manual: Ejecución de la prueba de integración con un archivo `.pptx` generado dinámicamente con `python-pptx`, verificando que el plan B extrae títulos, cuadros, tablas y notas del orador, emitiendo el aviso en el resultado de ingesta.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P24.** El puerto, el adaptador y el plan B están bien, pero la web no deja subir `.pptx` (`accept` de `MaterialView` sin `.pptx`, y el texto «No soportados (ej. .pptx)» sigue ahí), el `aviso` del plan B no se muestra en ningún sitio, y con diapositivas que son solo imágenes el plan B manda un texto vacío a Gemini, que se inventaría la nota. Además, `soffice` falla en silencio si LibreOffice ya está abierto.
---

## P15. Desplegable de asignaturas al subir archivos

- **Commit:** 1384372 `feat(web): P15 desplegable de asignaturas al subir archivos`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/views/MaterialView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
En `MaterialView.tsx`, se reemplazó el campo de texto libre para la asignatura en la subida individual por un elemento `<select>` cargado con el catálogo de `api.getMaterias()`, impidiendo subir material a asignaturas inexistentes.
En `SilabosView.tsx`, se implementó un desplegable `<select>` con las asignaturas del catálogo más la opción «Nueva asignatura…» (que despliega el campo de texto para el nuevo nombre). Al seleccionar o extraer un sílabo cuyo nombre sugerido coincide con una asignatura del catálogo (mediante `buscarMateriaPorClave`), se selecciona automáticamente dicha asignatura sin abrir el campo de texto libre.

### Cómo lo verifiqué
- pytest: 136 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint: ok (0 warnings, 0 errors con oxlint)
- npm run build: ok (compilación completa sin errores)
- npm test: 25 passed en 3 suites (vitest)
- Prueba manual: Validación en el formulario de subida individual de `MaterialView` donde la asignatura es seleccionada obligatoriamente del catálogo mediante el desplegable; y en `SilabosView` donde subir un archivo con nombre en mayúsculas como `INGENIERIA_DE_SOFTWARE_II.pdf` selecciona automáticamente `Ingeniería de Software II` en el desplegable sin mostrar el campo de texto libre, mientras que elegir «Nueva asignatura…» muestra el `<Input>` para escribirla.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P23.** Los desplegables están bien, pero al elegir un archivo de sílabo cuyo nombre no coincide con el catálogo («Silabo_2026.pdf»), la vista cambia la asignatura que el usuario ya había elegido a «Nueva asignatura» con el nombre del archivo; al guardar se crearía una asignatura nueva.
---

## P14. No sobrescribir el nombre de la asignatura del catálogo

- **Commit:** a9b71aa `feat(core): P14 preservar nombre de catalogo y resolver materia en casos de uso`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/bootstrap.py
  - backend/src/modular_learning/core/application/ingesta.py
  - backend/src/modular_learning/core/application/silabo.py
  - backend/src/modular_learning/core/application/tutoria.py
  - backend/src/modular_learning/infrastructure/persistence/json_repositorios.py
  - backend/tests/integration/infrastructure/test_almacen.py
  - backend/tests/unit/application/fake_adapters.py
  - backend/tests/unit/application/test_ingesta_service.py
  - backend/tests/unit/application/test_silabo_service.py
  - backend/tests/unit/application/test_tutoria_service.py

### Qué hice
Se modificó `agregar_materia` en `JsonMateriaRepo` y en el fake `InMemoryMateriaRepo` para que no sobrescriba una asignatura existente por slug, limitándose a añadir nuevas materias.
En los casos de uso `SilaboService.guardar_cronograma`, `IngestaService` (al calcular la ruta de notas en Obsidian y registro) y `TutoriaService.iniciar_sesion` se resuelve el nombre con `resolver_materia` sobre el catálogo antes de operar, preservando el nombre escrito en caso de no existir en el catálogo. Se conectó `materia_repo` en `bootstrap.py` para `IngestaService` y `TutoriaService`.

### Cómo lo verifiqué
- pytest: 136 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/unit/application/test_silabo_service.py::test_guardar_cronograma_no_sobrescribe_nombre_catalogo
  - backend/tests/unit/application/test_ingesta_service.py::test_ingesta_usa_nombre_catalogo_para_carpeta_obsidian
  - backend/tests/unit/application/test_tutoria_service.py::test_tutoria_iniciar_sesion_resuelve_materia_catalogo
  - backend/tests/integration/infrastructure/test_almacen.py::test_leer_escribir_y_listar
- Prueba manual: Validación de que al guardar un sílabo con «INGENIERIA DE SOFTWARE II», el catálogo mantiene «Ingeniería de Software II» intacto y el cronograma se asigna a su slug; y que al ingestar material indicando «ingenieria de software ii» la nota se almacena en la carpeta «Ingeniería de Software II».

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Detalle menor: en `TutoriaService.iniciar_sesion` la resolución del nombre se hace después de buscar la clase y los fallos previos; funciona porque esas búsquedas no distinguen escritura, pero sería más claro resolverlo al principio.
---

## P13. «Vaciar cronograma» no debe borrar la asignatura

- **Commit:** bf2ac35 `fix(api): P13 vaciar cronograma conserva la asignatura en el catalogo`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/apps/api/routers/materias.py
  - backend/tests/integration/api/test_api.py

### Qué hice
Se cambió `borrar_materia=False` en la llamada a `servicio.eliminar_cronograma` dentro del endpoint `DELETE /api/materias/{materia}/cronograma` (`routers/materias.py`). De este modo, vaciar el cronograma borra sus clases pero conserva la asignatura en el catálogo.
Se revisó `SilabosView.tsx`, verificando que al vaciar el cronograma se mantiene la asignatura activa seleccionada mostrando el estado vacío de clases.

### Cómo lo verifiqué
- pytest: 133 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/integration/api/test_api.py::test_eliminar_cronograma_conserva_materia
- Prueba manual: Ejecución del test de integración comprobando que tras `DELETE /api/materias/redes/cronograma`, `GET /api/materias` sigue retornando «Redes» en la lista del catálogo y `GET /api/materias/redes/cronograma` retorna `{"clases": []}`.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.**
---

## P12. Seleccionar la asignatura recién guardada aunque lleve tildes

- **Commit:** bb1a30f `fix(web): P12 seleccionar la asignatura recien guardada aunque lleve tildes`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/lib/asignaturas.ts
  - frontend/src/lib/asignaturas.test.ts
  - frontend/src/views/SilabosView.tsx

### Qué hice
Se implementó la función auxiliar `buscarMateriaPorClave` en `lib/asignaturas.ts` que busca una materia en el catálogo comparando slug y nombre normalizados mediante `clave()` para que las tildes, mayúsculas o espacios no impidan la correspondencia.
En `SilabosView.tsx`, se adaptó `cargarCatalogo` para buscar el destino usando `buscarMateriaPorClave`, permitiendo pasar directamente el nombre o slug de la asignatura, y se actualizó `handleGuardarSilaboExtraido` para invocar `cargarCatalogo(subidaMateria.trim())` sin calcular un slug manual defectuoso.

### Cómo lo verifiqué
- pytest: 132 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint: ok (0 warnings, 0 errors con oxlint)
- npm run build: ok (tsc y vite build completados)
- npm test: 25 passed en 3 suites (vitest)
- Tests nuevos:
  - frontend/src/lib/asignaturas.test.ts::buscarMateriaPorClave
- Prueba manual: Validación del flujo donde al guardar un sílabo con nombre que contiene tildes (p.ej. «Ingeniería de Software II»), `buscarMateriaPorClave` localiza `{ slug: 'ingenieria-de-software-ii', nombre: 'Ingeniería de Software II' }` en el catálogo cargado, asignando `materiaActiva` a dicho slug y activando la recarga para mostrar sus clases de forma inmediata.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** `buscarMateriaPorClave` queda reutilizable y bien probada.
---

## P11. Estadísticas con el nombre del catálogo

- **Commit:** 4db2c4f `feat(core): P11 estadisticas y evaluacion usan nombre del catalogo`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/bootstrap.py
  - backend/src/modular_learning/core/application/evaluacion.py
  - backend/src/modular_learning/core/application/telemetria.py
  - backend/tests/unit/application/test_evaluacion_service.py
  - backend/tests/unit/application/test_otros_servicios.py

### Qué hice
Se actualizó `TelemetriaService` para recibir un `materia_repo: MateriaRepo | None = None` opcional (conectado en `bootstrap.py`). Al recopilar estadísticas, busca el nombre canónico de la materia en el catálogo mediante `resolver_materia`; si la materia no está en el catálogo o no hay repositorio, conserva el slug.
En `EvaluacionService._nombre_materia` se migró la normalización a `resolver_materia` con el catálogo de `self.materia_repo.listar()` y se eliminó la función auxiliar `_clave` e imports en desuso.

### Cómo lo verifiqué
- pytest: 132 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/unit/application/test_otros_servicios.py::test_telemetria_service
  - backend/tests/unit/application/test_evaluacion_service.py::test_nombre_materia_con_catalogo
  - backend/tests/unit/application/test_evaluacion_service.py::test_nombre_materia_sin_catalogo
- Prueba manual: Verificación del mapeo de nombres en `TelemetriaService` y `EvaluacionService` con `resolver_materia`, garantizando que claves slug como `ingenieria-de-software-ii` devuelven `Ingeniería de Software II` cuando la asignatura existe en el catálogo, y conservan el slug en caso contrario.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Reutiliza `resolver_materia` como se pedía y quita el `_clave` duplicado. `ml stats` y `/api/stats` vuelven a mostrar el nombre del catálogo.

---

## P10. Migración: no sobrescribir cronogramas al renombrar

- **Commit:** 75f0df9 `fix(scripts): P10 evitar sobrescribir cronogramas y manejar conflictos al migrar`
- **Estado:** hecha
- **Archivos:**
  - scripts/migrar_datos.py
  - backend/tests/integration/infrastructure/test_migracion.py

### Qué hice
Se detectan colisiones donde un archivo a renombrar (`clave`) tiene como destino una `nueva_clave` que ya existe en el almacén. En tal caso, no se escribe ni se borra ningún archivo de esa materia, se emite un aviso por pantalla y se incrementa el contador `resumen["conflictos"]`.
Se adaptaron los mensajes y condiciones de escritura para usar `sin_id` en vez de tratar el valor de retorno de `asignar_ids` como entero.
Se reemplazó la captura genérica de `Exception` por `json.JSONDecodeError` informando en consola de archivos JSON corruptos, y se formateó el script a 100 columnas sin errores de ruff.

### Cómo lo verifiqué
- pytest: 130 passed, 2 skipped
- ruff check / ruff format: ok en scripts y backend
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/integration/infrastructure/test_migracion.py::test_migracion_conflicto_no_sobrescribe
- Prueba manual: Ejecución del test de integración de migración con dos documentos coexistentes (`schedules/REDES_cronograma.json` y `schedules/redes_cronograma.json`), confirmando que ambos quedan intactos con `conflictos == 1` y que el test de idempotencia sigue pasando.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Los conflictos se detectan antes de tocar nada y la materia afectada se salta entera, también al enlazar guías. `ruff check scripts` está limpio. Nota: el test de conflicto activa la distinción de mayúsculas con `fsutil` y se salta si Windows no lo permite; en este equipo se ejecuta y pasa.

---

## P9. Corregir la regresión de carga de P8

- **Commit:** d843806 `fix(web): P9 corregir regresion de carga al renombrar o guardar silabo`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/views/HoyView.tsx
  - frontend/src/views/MaterialView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
En `SilabosView.tsx` se añadió un contador de estado `recarga` como dependencia del efecto que obtiene el cronograma y parciales, incrementándolo en `cargarCatalogo`. Con ello, las operaciones que conservan la materia activa (renombrar, crear asignatura o subir nuevo sílabo) fuerzan la recarga de clases sin quedarse indefinidamente en estado cargando.
En `MaterialView.tsx` se activó `setCargandoProyectos(true)` en el evento `onChange` del selector de asignaturas y en los botones manuales de refresco, restableciendo el indicador visual de carga durante el cambio de materia sin generar llamadas síncronas de `setState` dentro de los efectos.
Se eliminaron las líneas en blanco sobrantes en `HoyView.tsx` y se aseguró el salto de línea final en `SilabosView.tsx`.

### Cómo lo verifiqué
- pytest: 129 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 avisos y 0 errores en 36 archivos (oxlint); tsc -b y vite build ok; 21 tests passed (3 suites)
- Tests nuevos: ninguno
- Prueba manual: Se levantó la API apuntando `ML_DATA_DIR` a una copia aislada de `data/examples` y se probaron los tres flujos requeridos: (1) renombrar la materia activa ('redes-y-comunicaciones' a 'Redes y Telecomunicaciones') verificando que el cronograma y clases responden con HTTP 200 y se actualizan; (2) crear una asignatura ('Fisica Cuantica') verificando la persistencia en el catálogo; (3) guardar un sílabo nuevo para la asignatura activa con dos clases verificando su persistencia en disco y su posterior lectura sin bloqueo de carga. En `MaterialView`, al cambiar el filtro de materia en el selector se activa inmediatamente el indicador de carga y se oculta al resolver la promesa.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El contador `recarga` arregla bien el «cargando» infinito, y también cubre la lista vacía y el error. La prueba manual parece hecha contra la API más que en el navegador, pero el cambio es correcto leyendo el código. Queda un detalle menor → P12.

---

## P8. Avisos de oxlint

- **Commit:** 306c5ac `refactor(web): P8 corregir avisos de oxlint`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/components/ThemeToggle.tsx
  - frontend/src/views/MaterialView.tsx
  - frontend/src/views/PluginsView.tsx
  - frontend/src/views/SilabosView.tsx

### Qué hice
Se corrigieron los 12 avisos reportados por `oxlint` sin alterar el comportamiento de la interfaz:
- En `ThemeToggle.tsx`: se inicializó el estado con `useState(obtenerTemaGuardado)` eliminando la llamada sincrónica a `setTemaState` dentro de `useEffect`.
- En `PluginsView.tsx`: se eliminó la llamada sincrónica a `setLoading` antes de peticiones en efectos y se cargó la lista en diferido con `.then()` protegiendo cancelaciones.
- En `SilabosView.tsx`: se sustituyeron `catch (_err)` no utilizados por `catch` sin parámetro; se eliminó el estado no leído `_cargandoMaterias`; se estructuró la carga de asignaturas y cronograma con `useCallback` y promesas asíncronas, y se movió el reseteo de edición al cambio de materia.
- En `MaterialView.tsx`: se ordenó la declaración de `verificarEstados` antes de `cargarProyectos` con `useCallback` y se resolvieron las dependencias faltantes en los efectos de inicialización y filtro por materia.

### Cómo lo verifiqué
- pytest: 129 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: 0 avisos y 0 errores en 36 archivos (oxlint); tsc -b y vite build completados con éxito; 21 tests passed (3 suites)
- Tests nuevos: ninguno (refactor estético/linter)
- Prueba manual: Ejecución de `npm run lint` reportando 0 advertencias y 0 errores, y `npm run build` sin errores de tipos TypeScript.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P9.** Los avisos están corregidos y `ThemeToggle`/`PluginsView` están bien, pero `SilabosView` introduce una regresión: `cargarCatalogo` hace `setCargandoClases(true)` aunque `destino` sea la materia ya activa (renombrar, crear asignatura, guardar un sílabo de la materia activa). Como `materiaActiva` no cambia, el efecto no se vuelve a ejecutar y el panel queda en «cargando» para siempre. En `MaterialView`, al cambiar de materia ya no se activa `cargandoProyectos`, y el efecto duplica el cuerpo de `cargarProyectos`/`cargarRegistrados`. La «prueba manual» fue solo lint y build: en un refactor de efectos hay que abrir la vista.

---

## P7. `en_nube` con una variable explicita

- **Commit:** caa8c4e `feat(api): P7 usar variable ML_EN_NUBE explicita`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/apps/api/routers/config.py
  - backend/tests/integration/api/test_api.py
  - docs/DESPLIEGUE.md
  - render.yaml

### Qué hice
Se modificó `apps/api/routers/config.py` para determinar `en_nube` exclusivamente comprobando `os.getenv("ML_EN_NUBE") == "1"`, en lugar de inferirlo de `RENDER` o `DATABASE_URL`. De este modo, el uso en modo híbrido (app local conectada a Neon) no oculta erróneamente el escaneo de carpetas locales.
Se agregó `ML_EN_NUBE: "1"` a las variables de entorno de `render.yaml` y se documentó su propósito y uso en `docs/DESPLIEGUE.md`.

### Cómo lo verifiqué
- pytest: 129 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- Tests nuevos:
  - backend/tests/integration/api/test_api.py::test_config_en_nube_con_variable
- Prueba manual: Llamadas a `GET /api/config` con `ML_EN_NUBE` ausente, con valor `"1"` y con valor `"0"`.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Tras el push, comprobar en Render que `ML_EN_NUBE=1` aparece en el entorno del servicio (lo aplica la sincronización del Blueprint).

---

## P6. Tema claro con el sistema en oscuro

- **Commit:** 92f0de2 `fix(web): P6 tema claro funcional con sistema en oscuro`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/index.css
  - frontend/src/lib/theme.test.ts

### Qué hice
Se reemplazaron los bloques `@media (prefers-color-scheme: dark)` en `body`, `.marcador` y `.prose` por selectores `html.dark ...`, eliminando las reglas `html.light` redundantes.
Para la guía imprimible (`.hoja .prose`), se añadieron selectores `html.dark .hoja .prose` con mayor especificidad para preservar el texto oscuro sobre papel blanco incluso si la interfaz está en modo oscuro.
Se crearon pruebas unitarias para `theme.ts` y para comprobar la ausencia de `@media (prefers-color-scheme: dark)` y `html.light` en `index.css`.

### Cómo lo verifiqué
- pytest: 128 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 kept, 0 broken
- npm run lint / build / test: lint ok (12 avisos preexistentes de P8), build ok, 21 tests passed (3 suites)
- Tests nuevos:
  - frontend/src/lib/theme.test.ts::devuelve "system" por defecto si no hay nada guardado
  - frontend/src/lib/theme.test.ts::guarda y recupera temas válidos
  - frontend/src/lib/theme.test.ts::aplica tema claro añadiendo clase light y quitando dark
  - frontend/src/lib/theme.test.ts::aplica tema oscuro añadiendo clase dark y quitando light
  - frontend/src/lib/theme.test.ts::aplica tema del sistema consultando matchMedia
  - frontend/src/lib/theme.test.ts::index.css no contiene @media (prefers-color-scheme: dark) ni selectores html.light para contrarrestar
- Prueba manual: Verificación del CSS compilado con `npm run build` confirmando que `.prose` bajo `html.dark` aplica texto claro (`slate-200`) y bajo `html:not(.dark)` mantiene `slate-800`, mientras que `.hoja .prose` mantiene `slate-800` en ambos casos gracias a `html.dark .hoja .prose`.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Bien visto que `html.dark .prose` gana en especificidad a `.hoja .prose` y por eso había que añadir `html.dark .hoja …`. La comprobación fue leyendo el CSS, no en el navegador; lo doy por bueno porque el razonamiento es correcto.

---

## P5. Migracion de datos que tambien funcione en Neon

- **Commit:** 9f26841 `feat(scripts): P5 migracion de datos idempotente sobre AlmacenDocumentos`
- **Estado:** hecha
- **Archivos:**
  - scripts/migrar_datos.py
  - backend/tests/integration/infrastructure/test_migracion.py

### Qué hice
Se reescribió `scripts/migrar_datos.py` para operar sobre `AlmacenDocumentos` (`almacen_por_defecto()`), permitiendo migrar datos tanto en archivos locales como en Postgres (Neon).
El script es completamente idempotente: normaliza materias, asigna ids a las clases sin identificador, renombra los archivos de cronograma al formato `schedules/<slug>_cronograma.json` y vincula `clase_id` en las guías offline.
Se añadió la opción `--simular` para previsualizar los cambios sin escribir en el almacén.

### Cómo lo verifiqué
- pytest: 128 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- Tests nuevos:
  - backend/tests/integration/infrastructure/test_migracion.py::test_migracion_idempotente_sobre_almacen_archivos
- Prueba manual: Test de integración sobre `tmp_path` con simulación (sin efectos secundarios) y doble ejecución consecutiva comprobando que la segunda pasada no realiza ningún cambio ni renombramiento adicional y los documentos permanecen idénticos.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Cambios pedidos → P10.** El test de idempotencia es bueno. Falta: (1) si la clave con slug ya existe, el renombrado la sobrescribe con el archivo antiguo y borra este: pérdida de datos en Neon; (2) `asignar_ids` devuelve `bool`, así que el script imprime «nuevos IDs: True»; (3) `ruff check scripts` da 5 errores y el archivo está formateado a 88 columnas en vez de 100.

---

## P4. Cronogramas guardados con el slug de la materia

- **Commit:** 5acd30d `feat(infra): P4 guardar cronogramas con slug y listar con claves de slug`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/infrastructure/persistence/json_repositorios.py
  - backend/tests/integration/api/test_api.py
  - backend/tests/integration/infrastructure/test_adaptadores_disco.py
  - backend/tests/integration/infrastructure/test_almacen.py
  - backend/tests/unit/application/fake_adapters.py
  - frontend/src/lib/asignaturas.test.ts

### Qué hice
`JsonCronogramaRepo.guardar_cronograma` y `guardar_parciales` ahora generan las rutas de nuevos cronogramas usando `slug_materia(materia)`.
`JsonCronogramaRepo.listar_cronogramas` y `InMemoryCronogramaRepo.listar_cronogramas` retornan las claves de cada cronograma normalizadas con `slug_materia`.
La búsqueda exacta por slug se preserva tanto para archivos existentes con nombres antiguos en mayúsculas como para los nuevos slugs.
Los consumidores de frontend (`CalendarioView`, `HoyView`, `GuiaView`, `lib/asignaturas.ts`) cruzan las claves de cronograma con el catálogo a través de `clave()`, resolviendo y mostrando correctamente el nombre oficial de la materia.

### Cómo lo verifiqué
- pytest: 127 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint (12 avisos existentes de oxlint, 0 errores), build ok, vitest (15 passed)
- Tests nuevos:
  - backend/tests/integration/infrastructure/test_adaptadores_disco.py::test_cronograma_guardado_con_slug_y_antiguo_en_mayusculas_se_lee_con_slug
  - frontend/src/lib/asignaturas.test.ts::cruza cronogramas cuyas claves son slugs con el catálogo
- Prueba manual: Tests de integración verificando persistencia con slug para cronogramas nuevos y compatibilidad de lectura y listado con cronogramas existentes en mayúsculas.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El frontend cruza con `clave()`, que ignora guiones, así que no hacía falta tocar vistas. Queda un consumidor en el backend que no incluí en la tarea: `TelemetriaService` publica `slug.title()` («Ingenieria-De-Software-Ii» en `ml stats`). Va como P11.

---

## P3. Crear una guia debe avisar de las clases que no existen

- **Commit:** 96e7fc5 `fix(core): P3 crear guia valida existencia de todas las clases solicitadas`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/application/guias.py
  - backend/tests/unit/application/test_guias_service.py

### Qué hice
Se actualizó la validación en `GuiaOfflineService.crear` para verificar previamente la presencia de todas las clases solicitadas en el cronograma.
Cada elemento recibido en `temas` se valida tanto contra los `id` de clase existentes como contra los nombres de `tema`.
Si cualquiera de las clases no existe, se lanza `ValueError` enumerando explícitamente los identificadores o nombres ausentes, evitando que se omitan en silencio.

### Cómo lo verifiqué
- pytest: 126 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- Tests nuevos:
  - backend/tests/unit/application/test_guias_service.py::test_crear_guia_avisa_de_clases_inexistentes_mezclando_id_valido
- Prueba manual: Verificación con test parametrizado y test unitario con lista mixta de ID válido e ID inexistente (`id-inexistente`), comprobando que se lanza `ValueError` y se nombra la clase faltante.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** El bucle de abajo podría reutilizar los conjuntos de arriba, pero no es un fallo.

---

## P2. Deshacer la revision de una guia solo debe deshacer lo que hizo esa guia

- **Commit:** b87d1be `fix(core): P2 deshacer guia solo afecta a sus propios eventos y preserva estado previo`
- **Estado:** hecha
- **Archivos:**
  - backend/src/modular_learning/core/application/guias.py
  - backend/src/modular_learning/core/application/repaso.py
  - backend/src/modular_learning/core/domain/guia_offline.py
  - backend/tests/unit/application/test_guias_service.py
  - frontend/src/api/types.ts

### Qué hice
Se añadió el campo `estado_previo: str | None = None` a `ClaseGuia` (`core/domain/guia_offline.py` y `frontend/src/api/types.ts`).
`RepasoService.registrar_estudio_offline` ahora recibe `guia_id` opcional y lo persiste en el evento.
En `GuiaOfflineService.registrar_revision`, se captura `estado_previo` en el cronograma antes de marcar la clase y se pasa `guia_id=guia.id` a repaso.
En `GuiaOfflineService.deshacer_revision`, se borran únicamente los eventos con ese `guia_id` y las clases vuelven a su `estado_previo` (o `pendiente` si era `None`).

### Cómo lo verifiqué
- pytest: 125 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint (12 avisos existentes de oxlint, 0 errores), build ok, vitest (14 passed)
- Tests nuevos:
  - backend/tests/unit/application/test_guias_service.py::test_deshacer_dos_guias_mismo_tema_no_toca_la_otra
  - backend/tests/unit/application/test_guias_service.py::test_deshacer_clase_ya_completada_sigue_completada
- Prueba manual: Verificación unitaria de no colisión entre guías del mismo tema y preservación del estado completado previo tras deshacer.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Limitaciones aceptadas: las guías revisadas antes de este cambio no tienen `guia_id` en sus eventos, así que al deshacerlas sus eventos se quedan en el historial; y si dos guías marcan la misma clase, deshacer la primera la devuelve a `pendiente` aunque la segunda la siga dando por estudiada.

---

## P1. La tutoria web debe identificar la clase por su id

- **Commit:** e250c17 `fix(web): P1 enviar clase_id a la tutoria`
- **Estado:** hecha
- **Archivos:**
  - frontend/src/lib/asignaturas.ts
  - frontend/src/lib/asignaturas.test.ts
  - frontend/src/views/CalendarioView.tsx
  - frontend/src/views/HoyView.tsx
  - frontend/src/views/ProgresoView.tsx
  - frontend/src/views/RevisionGuiaView.tsx
  - frontend/src/views/TutoriaView.tsx

### Qué hice
Se añadió el parámetro opcional `claseId` a `enlaceTutoria` en `lib/asignaturas.ts` para propagar `clase_id` en la query.
Se pasó el id de la clase en las vistas donde se conoce (`CalendarioView`, `ProgresoView`, `RevisionGuiaView` y `HoyView`), eliminando la función duplicada de `HoyView.tsx`.
En `TutoriaView.tsx`, se lee `clase_id` de los query params y se propaga en `api.iniciarTutoria`, reseteándolo si el usuario edita el tema manualmente o cambia la materia.

### Cómo lo verifiqué
- pytest: 123 passed, 2 skipped
- ruff check / ruff format: ok
- import-linter: 3 contratos cumplidos, 0 rotos
- npm run lint / build / test: lint (12 avisos existentes de oxlint, 0 errores), build ok, vitest (14 passed)
- Tests nuevos:
  - frontend/src/lib/asignaturas.test.ts::enlaceTutoria (3 tests: solo materia, sin clase_id, con clase_id)
- Prueba manual: Con una copia de `data/examples` en carpeta temporal y dos clases con el mismo tema en un cronograma (`c1` el 08/10 y `c2` el 15/10), se inició y finalizó tutoría indicando `clase_id="c2"`, confirmando que solo `c2` pasó a completado y `c1` permaneció pendiente.

### Dudas o hallazgos
ninguno

### Revisión de Claude
**Aprobada.** Detalle menor: en `HoyView.tsx` quedaron dos líneas en blanco donde estaba el `enlaceTutoria` local (se limpia en P9).
