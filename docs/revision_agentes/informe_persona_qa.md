# Informe QA exploratorio (Andrés) - Modular Learning en :8001

Alcance: API y UI en http://localhost:8001 (copia de datos de ejemplo). No se tocó el puerto 8000, ni `.env`, ni `data/`. Pruebas con curl y scripts Python (urllib) y una pestaña propia del navegador integrado.

AVISO de proceso: `GET /api/quiz/generar` lo llamé sin parámetros creyendo que fallaría en validación. Respondió 200 con un quiz completo, así que pudo consumir una llamada a Gemini. No volví a llamar a ningún endpoint de IA. Ver H12.

AVISO de estado: mi prueba de nombre de 20 MB dejó la copia de datos inutilizable (ver H2). La limpié editando `materias.json` dentro de `scratchpad\datos_prueba\config`. Los datos de ejemplo quedaron con asignaturas basura de mis pruebas (XSS, "../../x", "abc\u0000def", "Renombrada", "Física II", "Física 😀 Ñandú", "CON", "..\..\..\evil", "con/barra:y*?", "Carrera N"/"Par N") y la clase "<img onerror>" en programacion-web, y una clase huérfana en la materia inexistente "fantasma".

Resumen de severidades: 1 Alta crítica (H1), 3 Altas (H2, H3, H4), varias Medias, resto Bajas.

---

## H1 [ALTA] Condición de carrera: pérdida de escrituras y 500 con peticiones concurrentes

Dos escrituras simultáneas rompen la persistencia: se pierden datos silenciosamente y algunas devuelven 500 o 400 con errores de SO.

Reproducción (8 hilos, mismo servidor):
```
for i in 0..7 en paralelo:  POST /api/materias  {"nombre":"Carrera <i>"}
```
Observado: 4x `201` y 4x `500 {"detail":"Internal Server Error"}` (texto plano). Tras listar solo existía 1 de las 8 asignaturas creadas, incluidas algunas de las que respondieron 201 (se perdieron).

Con 20 hilos: la mayoría de peticiones fallaron con conexión rechazada/500 (`[-1, 500, ...]`) y solo 1-2 de 20 asignaturas quedaron guardadas.

Altas de clase en paralelo:
```
for i in 0..7 en paralelo:  POST /api/materias/programacion-web/clases  {"tema":"D<i>"}
```
Observado: 4x `201`, 4x `400` con detalle:
`{"detail":"[WinError 32] El proceso no tiene acceso al archivo porque está siendo utilizado por otro proceso: '<ruta-local>"}`
y `[Errno 13] Permission denied: '...datos_prueba\\schedu...'`. Con 20 hilos solo 3 de 20 altas fueron 201.

DELETE doble en paralelo (10 hilos) `/api/materias/concurrente`: 8x `500`, 2x `200`.

Causa probable: el almacén de documentos reescribe el JSON sin bloqueo (lectura-modificación-escritura no atómica; reemplazo de archivo en Windows falla si otro hilo lo tiene abierto).
Impacto: doble clic o dos pestañas pueden perder datos; los mensajes filtran la ruta absoluta del servidor (ver H5).

---

## H2 [ALTA] Sin límite de longitud en nombres: una asignatura de 20 MB bloquea la app y no se puede borrar

```
python: requests POST /api/materias {"nombre":"B"*20_000_000}   -> 201
```
Observado: `201`. Desde ese momento `GET /api/materias` pesa ~60 MB (el nombre se repite 3 veces: `materias`, `catalogo`, y respuesta), la pantalla "Asignaturas" y cualquier vista que liste asignaturas se vuelven lentas o inutilizables.

El borrado es imposible por API porque el slug mide 20.000.000 de caracteres:
```
DELETE /api/materias/<slug de 20M caracteres>   -> 400 "Invalid HTTP request received."
```
(con un prefijo de 5000 caracteres devuelve 404 "Asignatura no encontrada."). Quedó persistente hasta que edité el archivo a mano. Tampoco se puede renombrar (mismo problema en la URL).
Con 20.000 caracteres: `POST /api/materias {"nombre":"AAAA...x20000"}` -> 201 (aceptado sin límite).
Sugerencia: `max_length` en `NuevaMateria`/`RenombrarMateria`/`NuevaClase` (tema, objetivo, contenido), y límite de tamaño de body.

---

## H3 [ALTA] Escaneo de material permite recorrer carpetas arbitrarias fuera de la carpeta de material (path traversal)

```
GET /api/material/escanear?materia=..%2f..%2f
```
Observado `200`: `{"escaneos":[{"materia":"../../","carpeta":"<ruta-local> - ...\\<carpeta-local>\\../../","existe":true,"total":1417,"pendientes":[{"nombre":"Documento.docx","ruta":"C:\\Users\\...\\..\\"...` es decir, lista 1417 archivos de un directorio dos niveles por encima, con rutas absolutas. El parámetro `materia` se concatena con `os.path.join(ruta_material, m)` sin validar contra el catálogo (también en `GET /api/proyectos/escanear?materia=...`, que respondió 200 con candidatos vacíos).
Impacto: divulgación de la estructura de archivos del equipo; combinado con `POST /api/material/sincronizar/stream {"materia":"../../"}` permitiría ingerir (y enviar a la IA) archivos fuera de la carpeta prevista. No lo probé por usar IA.
Relacionado (revisado en código, no ejecutado por consumir IA): `POST /api/proyectos/ingestar` acepta `ruta` arbitraria del servidor (`IngestarProyectoRequest.ruta`) y `POST /api/config` acepta cualquier carpeta existente.

---

## H4 [ALTA/MEDIA] Sin autenticación local, sin validación de Host/Origin y sin cabeceras de seguridad

- `curl -H "Host: evil.com" localhost:8001/api/stats` -> `200` (DNS rebinding posible).
- Ninguna cabecera de seguridad en `/` ni en `/api/*`: faltan `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors`, `Referrer-Policy`. Solo `server: uvicorn` (expone el servidor).
- CORS: ninguna cabecera `Access-Control-*` con `Origin: http://evil.com` (bien: no permisivo). Los preflights devuelven 405 (`allow: PUT`), lo cual en la práctica bloquea escrituras JSON cross-site.
- Pero los POST sin cuerpo (p. ej. `POST /api/proyectos/{id}/actualizar`, `POST /api/tutoria/{id}/finalizar`) y los GET que consumen IA (`GET /api/quiz/generar`) son accionables cross-site (CSRF/`<img src>`), pues no requieren preflight. `GET /api/quiz/generar` con efecto colateral (consume cuota) es especialmente mala idea como GET.
- `/docs`, `/redoc` y `/openapi.json` públicos (200, 44 rutas) y cargan Swagger UI desde cdn.jsdelivr.net sin SRI. `/api/docs` y `/api/openapi.json` dan 404.

---

## H5 [MEDIA] Mensajes de error filtran rutas internas y detalles del SO

Ver H1 (rutas absolutas del scratchpad en 400). Otros endpoints devuelven `str(e)` de excepciones genéricas como 500 (`silabo`, `proyectos`, `guias`, `config`), lo que expone rutas y trazas cortas. `POST /api/config` devuelve la ruta en el mensaje (`"La carpeta de material no existe: Z:\\no\\\\existe"`, doble barra rara), y `GET /api/config` devuelve las rutas absolutas del equipo del usuario (carpeta de OneDrive y Obsidian Vault).

---

## H6 [MEDIA] `PUT /api/materias/{slug}` crea asignaturas si el slug no existe y permite duplicar nombres

```
PUT /api/materias/noexiste   {"nombre":"X"}   -> 200 {"materia":{"slug":"noexiste","nombre":"X"},...}   (esperado 404)
PUT /api/materias/duplicada  {"nombre":"Programacion Web"}  -> 200 {"materia":{"slug":"duplicada","nombre":"Programacion Web"}}
```
El primero crea una asignatura nueva en vez de dar 404. El segundo deja dos asignaturas con el mismo nombre visible (slugs distintos, `programacion-web` y `duplicada`), sin conflicto 409.
También: `PUT` con `"nombre":"   "` -> 400 correcto, pero `POST /api/materias {"nombre":"   "}` -> `201` sin crear nada (silencioso). `POST {"nombre":"!!!???"}` y `{"nombre":"😀"}` -> `201` y no se crea asignatura (slug vacío), sin error.

---

## H7 [MEDIA] Se crean cronogramas/clases de asignaturas inexistentes (datos huérfanos)

```
POST /api/materias/fantasma/clases   {"tema":"X"}   -> 201 (la asignatura "fantasma" no existe)
POST /api/materias/fantasma/parciales {"parciales":[{"nombre":"P1"}]} -> 200
GET  /api/stats  -> aparece "fantasma" con 1 clase
POST /api/silabo/guardar {"materia":"<b>x</b>","datos":{"clases":[...]}}  -> registra la materia
```
Además `GET /api/materias/noexiste/cronograma` y `/clases` devuelven `200 {"clases":[]}` en vez de 404 (no se distingue "vacío" de "no existe"). `DELETE /api/materias/{slug}` de inexistente sí da 404 correcto la primera vez.

---

## H8 [MEDIA] Falta de validación de contenido de clases

```
POST /api/materias/programacion-web/clases {"tema":"   "}                         -> 201 (tema solo espacios)
POST ... {"tema":"<img src=x onerror=alert(1)>","fecha":"no-es-fecha","estado":"inventado"} -> 201
PATCH /api/materias/programacion-web/clases/<id>/estado?estado=lol                  -> 200 {"ok":true,"estado":"lol"}
PUT  .../clases/<id> {"campos":{"tema":""}}                                          -> 200 (tema vacío permitido)
PUT  .../clases/<id> {"campos":{"__proto__":{"a":1},"x":{"y":[1]}}}                  -> 200, los campos arbitrarios se guardan en el JSON
```
Fecha sin formato, estado fuera de catálogo y campos libres se persisten tal cual (el `id` sí queda protegido). Alta con el tema como solo espacios aceptada.
Efecto en la UI: el calendario/Hoy muestra "la clase fue hace 314 días" con fechas válidas, pero un estado "lol" o fecha inválida puede romper filtros.

---

## H9 [MEDIA] Nombres con caracteres peligrosos aceptados tal cual

Aceptados con 201 y mostrados como nombre visible: `<script>alert(1)</script><img src=x onerror=alert(2)>`, `../../etc/passwd`, `..\..\..\evil`, `abc\u0000def` (carácter NUL en el nombre), `con/barra:y*?`, `CON` (nombre reservado de Windows).
- El almacenamiento usa slug saneado (`etc-passwd`, `evil`, `con-barra-y`), así que NO hay escritura fuera de `data/` (path traversal en subidas/guardado no reproducible; bien).
- Pero el nombre bruto se guarda y se muestra, y el cronograma se guarda como `schedules/con_cronograma.json`. Colisión: `"../../x"` renombrado sobre slug `renombrada` coexiste con "Renombrada" en la lista `materias` (la lista `materias` y `catalogo` se desincronizan: `materias` guarda nombres brutos y `catalogo` slugs).
- Dos nombres distintos pueden dar el mismo slug (`"Física 😀 Ñandú"` y `"FISICA 😀 ÑANDÚ"` -> `fisica-nandu`); se deduplican sin avisar (aceptable, pero sin feedback).

## H10 [BAJA] XSS: NO reproducible (positivo)

Los nombres/temas con `<script>`, `<img onerror>` y `<svg onload>` se renderizan como texto en Asignaturas, Hoy y Calendario (React escapa; no hay `dangerouslySetInnerHTML`, y `react-markdown` sin `rehype-raw`). `window.alert` no se invocó, `document.querySelectorAll('img[src="x"]')` = 0.

---

## H11 [BAJA] Validaciones correctas observadas (sin hallazgo)

- Nombre vacío: `422`; sin campo: `422`; JSON malformado: `422`; `null`, número, lista: `422`; `Content-Type: text/plain` o form: `422`; sin cuerpo: `422`.
- Métodos incorrectos: `405` con cabecera `allow`; rutas API desconocidas: `404 {"detail":"Endpoint no encontrado"}`.
- Subidas (`/api/material/ingestar`, `/api/silabo/extraer`) con `.exe`, sin extensión, `a.pdf.exe`, `../../../evil.sh`: `400` claro "Formato no soportado" antes de tocar el LLM. Falta archivo/materia: `422`. (Solo se probó lo que falla antes de la IA; no se probaron archivos vacíos ni enormes con extensión válida por ir a Gemini. Nota de código: `ingestar` llama a `agregar_materia(materia)` ANTES de procesar, por lo que un fallo posterior dejaría una asignatura huérfana, y `shutil.copyfileobj` no limita el tamaño del archivo.)
- Rutas estáticas: `/..%2f..%2fpyproject.toml`, `/.env`, `/.git/config`, `/%2e%2e/...` devuelven el `index.html` del SPA (974 bytes), sin servir archivos; `/static/../..` -> 404. Sin path traversal estático.
- IDs inexistentes en guías, proyectos, tutoría, tarjetas, quiz: `404` claros en español.
- Doble borrado secuencial: primer `200`, segundo `404` (correcto).

## H12 [MEDIA] `GET /api/quiz/generar` sin parámetros genera contenido (posible llamada a IA) y es un GET con efectos

`GET /api/quiz/generar` -> `200` con `quiz_id` y preguntas (ej. sobre puertos driving/driven). Sin validar entrada, sin autenticación, accionable con un simple `<img src>` desde cualquier web. Si usa Gemini, cualquiera puede quemar la cuota.

## H13 [BAJA] Mensaje engañoso al guardar sílabo manual

`POST /api/silabo/guardar {"materia":"x","datos":{}}` -> `400 "La IA no devolvió un cronograma de clases válido."` aunque el usuario no usó IA en ese paso. Además `POST /api/guias {"materia":"fantasma","temas":["a"],"tiempo_minutos":-5}` -> 400 por tema inexistente pero `tiempo_minutos` negativo no se valida (se verá si pasa el primer chequeo).

## H14 [BAJA] UI: ruta desconocida y estado de error

- `http://localhost:8001/ruta/rara/%3Cscript%3E` redirige silenciosamente a `/` (Hoy); no hay página 404 propia. El servidor responde `200` (HTML del SPA) para cualquier ruta, incluyendo `/.env`.
- Con la API fallando (simulado con fetch devolviendo 500 texto plano a `/api/stats` y `/api/materias`), la vista Calendario muestra "No pude cargar el calendario: Error 500:" (mensaje vacío tras los dos puntos, sin botón de reintentar). No hay pantalla en blanco (bien). Tema oscuro correcto, layout móvil (400 px) correcto.
- Pestaña compartida: una llamada del navegador sin `tabId` se ejecutó en otro agente (tab-1); conviene pasar siempre `tabId`.

## H15 [BAJA] Configuración de plugins acepta claves y rutas arbitrarias

`POST /api/plugins/config {"clave":"../../x","carpeta":"C:\\Windows","materia":"<b>"}` -> `200 {"ok":true,"config":{"carpeta":"C:\\Windows","materia":"<b>"}}` (sin validar clave contra los plugins conocidos ni que la carpeta pertenezca a una ruta permitida). Misma raíz que H3: rutas de servidor controladas por el cliente. `POST /api/config` sí valida existencia de carpeta (400) pero acepta cualquier carpeta existente y NUL bytes dan el mismo 400 correcto.

---

## Resumen de endpoints probados

`/api/materias` (GET/POST/PUT/DELETE, clases, parciales, cronograma), `/api/config`, `/api/plugins`, `/api/stats`, `/api/salud`, `/api/repaso/*`, `/api/guias/*` (solo lectura/404), `/api/proyectos/*`, `/api/material/*` (registrados, escanear, delete inexistente), subidas con extensión inválida, `/api/silabo/guardar`, `/api/tutoria/*` con sesión inexistente, `/api/quiz/evaluar`, `/docs`, `/redoc`, `/openapi.json`, cabeceras, CORS, rutas estáticas, XSS en UI.
No ejecutados por IA: tutoría iniciar con datos válidos, guías generar/clases, ingesta con extensión válida, extracción de sílabo con archivo válido, `sincronizar/stream`, `proyectos/ingestar`.
