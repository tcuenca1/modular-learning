# Informe de usabilidad - Camila (novata, primer uso) - puerto 8001

Nota de contexto: la ventana del navegador medía ~736 px de ancho, así que vi el diseño "móvil" (menú hamburguesa). No pulsé ninguna acción con IA (Extraer clases, Preguntas nuevas, Empezar, Procesar nuevos).

## Tabla de tareas

| # | Tarea | Logrado | Pasos | Fricción |
|---|-------|---------|-------|----------|
| 1 | Entender de qué trata la app | Parcial | 0 (solo mirar) | Título "No tienes clases pendientes." + lista de asignaturas "Aún sin cronograma". "Cuaderno de estudio" no explica que hay IA, tutoría ni Obsidian. Entendí "planificador de clases"; el resto no. Además "1/2 clases (50%)" contradice "Aún sin cronograma" en las 5 asignaturas. |
| 2 | Qué clase toca a continuación | No (sin datos) | 1 (Hoy) + 1 (Calendario) | Hoy dice "No tienes clases pendientes" y Calendario "No hay clases en este mes". Correcto pero sin camino claro; no distingue "no hay sílabo" de "ya terminé". El Calendario es una página casi vacía con una leyenda minúscula y de bajo contraste ("Pendiente: abre la tutoría / Completada"). |
| 3 | Crear "Física II" | Sí, pero con dudas | ~7 (menú, Asignaturas, Nueva asignatura, escribir, Enter sin efecto, Guardar x2) | Enter no guarda. Mi primer clic en Guardar no hizo nada visible (el layout se movió) y tuve que repetirlo. Tras guardar: página en blanco bajo las pestañas y scroll horizontal. No hubo mensaje de éxito. |
| 4 | Dónde subir sílabo y apuntes | Sí | Sílabo: 3. Apuntes: 4 | Sílabo: botón "Subir sílabo" (aparece duplicado en la misma pantalla). Apuntes: pestaña "Material" > "Subir un archivo". Nada me dice que "Material" = apuntes. |
| 5 | Dónde repasar con preguntas | Sí | 3 (menú, Estudiar, Repaso) | "Estudiar > Repaso" es claro. No se ve de qué asignatura saldrán las preguntas. Esperaría que "Preguntas nuevas" genere preguntas con IA y gaste cuota. |
| 6 | Modo oscuro y Ajustes | Sí | Oscuro: 1. Ajustes: 2 | Selector de tema visible siempre arriba. Ajustes en el menú. Ver hallazgos sobre persistencia. |

## Hallazgos priorizados

### Alta
1. **Un nombre de asignatura largo rompe el diseño.** En el selector hay asignaturas de prueba con nombres de cientos de caracteres. El `<select>` se desborda y la página tiene scroll horizontal; el selector se corta en el borde. Repro: abrir /asignaturas con una asignatura de nombre larguísimo creada. Si es dato de otro tester, igual es un caso real (un usuario puede pegar texto largo). Faltan límite de longitud y truncado.
2. **Tras crear una asignatura la pantalla queda vacía.** Repro: Asignaturas > Nueva asignatura > escribir "Física II" > Guardar. Se selecciona Física II, pero debajo de las pestañas Clases/Material/Proyectos no hay nada (ni estado vacío ni "Subir sílabo") y hay scroll horizontal. Tras recargar vuelve a mostrar Arquitectura de Software, no la nueva. No hay confirmación de éxito (toast) que yo viera.
3. **Enter no envía el formulario de nueva asignatura** y el primer clic en "Guardar" no tuvo efecto visible. Se sintió roto; un usuario real pensaría que no funcionó y quizá la duplicaría.
4. **No hay onboarding ni explicación en la pantalla inicial.** Con datos vacíos, Hoy no dice qué hace la app (tutor con IA, notas en Obsidian). Un estado vacío debería ser una guía paso a paso: 1) crea asignatura, 2) sube sílabo, 3) sube apuntes, 4) estudia.
5. **Datos incoherentes en Hoy:** "1/2 clases (50%)" mientras todas las asignaturas dicen "Aún sin cronograma". Pierde confianza en la app desde el primer segundo.

### Media
6. **Fuga de ruta personal/jerga:** en Material se lee "Detecta materiales ... en <carpeta-local>/." y en Ajustes aparece una ruta de OneDrive con nombre de usuario y universidad. Es dato de ejemplo mezclado con el real, pero para un usuario nuevo es confuso ("¿qué es SEXTO?").
7. **Jerga sin explicar:** "Cortes de parcial", "Bóveda de Obsidian", "Procesar nuevos", "Revisar carpetas", "Profundidad: Intermedia: detalle técnico y ejemplos", "Guía offline", "Plugins", "Proyectos". Camila no sabe qué es Obsidian ni qué es una "bóveda".
8. **Botón "Subir sílabo" duplicado** en la misma vista (cabecera y estado vacío) y "Añadir clase" deshabilitado/atenuado sin explicar por qué.
9. **El panel de subir sílabo pregunta "Asignatura: Nueva asignatura…" por defecto** aunque estoy dentro de Arquitectura de Software; hay que cambiarlo a mano o se crea otra asignatura. Debería preseleccionar la actual.
10. **Tema inestable:** durante mi sesión el tema alternó entre oscuro y claro entre cargas sin que yo lo cambiara (probable por compartir navegador con otros agentes, pero conviene revisar que el tema persista y que dos pestañas no se pisen). Además, el icono de sol se usa para "Hoy" en el menú y para "Tema claro": ambiguo.
11. **Calendario vacío** casi sin contenido: no sugiere "sube un sílabo para ver fechas". La leyenda inferior es diminuta y de bajo contraste.
12. **Repaso:** no indica de qué asignatura/clases; el botón no avisa de que usa IA/cuota.

### Baja
13. Tabla de Material cortada a la derecha ("Nota de Obsidian") en pantalla estrecha; requiere scroll horizontal.
14. Texto "Tres preguntas nuevas de tus clases. Al terminar verás qué fallaste y por qué." en gris tenue, poco legible en oscuro.
15. Botones del selector de tema sin texto visible (solo iconos; sí tienen etiqueta accesible). Falta tooltip.
16. Consola: sin errores ni avisos durante toda la sesión (positivo).
17. En `<option>` se ven nombres de prueba tipo `<script>...`, `../../etc/passwd` (se escapan bien, no se ejecutó nada, pero la lista de ejemplo está contaminada).

## 3 mejoras recomendadas
1. **Onboarding en el estado vacío de Hoy:** tarjeta de 3 pasos (Crear asignatura > Subir sílabo > Subir apuntes) con botones directos, una frase que explique la app en una línea y corregir el contador "1/2 clases".
2. **Arreglar el flujo "Nueva asignatura":** que Enter guarde, mostrar confirmación, seleccionar la nueva asignatura y mostrar un estado vacío con "Subir sílabo"/"Añadir clase"; limitar longitud del nombre y truncar con elipsis en el selector para evitar el scroll horizontal.
3. **Reducir jerga y contextualizar acciones:** glosario breve o texto de ayuda para Obsidian/bóveda/parcial; etiquetar acciones con IA ("usa IA, gasta cuota") y preseleccionar la asignatura actual en el panel de sílabo.
