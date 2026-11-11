# Informe persona Mateo (móvil 375x812) - http://localhost:8001

Nota de contexto: los datos de ejemplo estaban contaminados por pruebas de otros agentes (asignaturas "<script>...", "../../etc/passwd", "abc\0def", una con 20000 letras "AAAA..."). Algunos hallazgos se agravan por eso, pero el fallo de layout es real.

## Hallazgos priorizados

### P1 (alto) - Selector de asignatura sin límite de ancho rompe /asignaturas
- Reproducir: abrir /asignaturas a 375px. Con un nombre largo en la lista, el `<select>` mide 163.962 px y `document.documentElement.scrollWidth` = 164.030 (innerWidth 375). Medido igual en pestañas Clases, Material y Proyectos.
- Incluso con nombres normales, el select sobresale del tarjeta: se ve cortado en el borde derecho (screenshot: "Arquitectura de Software" cortado en x=375, sin flecha visible).
- Sin overflow en Hoy, Estudiar, Calendario y Ajustes (scrollWidth = 375).
- Mejora: `w-full max-w-full min-w-0` en el select y `truncate`; limitar longitud del nombre de asignatura al crearla (backend y UI).

### P2 (medio) - Objetivos táctiles menores de 44 px (casi todo)
Medidas en px (ancho x alto), vistas principales:
- Cabecera (todas las vistas): selector de tema Claro/Oscuro/Sistema 26x26 (x3), Abrir menú 36x36, logo/enlace 190x37. Cerrar menú 28x28. Toggle de tema duplicado dentro del cajón (26x26).
- Menú lateral: ítems 231x34 (aceptable en ancho, bajos en alto).
- Hoy: "Ir a Asignaturas" 113x22, "Subir sílabo" 74x18 (x5, enlaces en línea, muy difíciles de pulsar), "Preguntas nuevas" 137x34, "Procesar 25 archivos" 157x34.
- Estudiar: pestañas Tutoría 69x32, Repaso 71x32, Guía offline 96x32; selects/inputs 294x36; botón "Empezar" 294x36.
- Calendario: Mes anterior 32x32, Mes siguiente 32x32, Hoy 50x30.
- Asignaturas: pestañas Clases 42x32, Material 51x32, Proyectos 62x32; lápiz 32x32 y otro botón 28x28; Subir sílabo 109x32; Añadir clase 113x32; "+ Añadir / editar cortes" 151x28; "Vaciar cronograma" 286x32; "Eliminar asignatura" 293x32 (acción destructiva con poco margen, riesgo de toque erróneo).
- Ajustes: pestañas Configuración 113x32, Plugins 70x32; inputs 294x36; Guardar 124x36.
- Mejora: mínimo 44x44 en móvil (padding o `min-h-11`), sobre todo toggles de tema, flechas del calendario y enlaces "Subir sílabo".

### P3 (medio) - Calendario: no se puede "buscar" y arranca vacío
- Reproducir: Menú > Calendario. Muestra "Noviembre de 2026 - Sin clases este mes." Solo en octubre aparecen 2 clases (1 y 8 de oct). Hay que pulsar "Mes anterior" a ciegas (las 7 meses anteriores comprobados estaban vacíos salvo octubre).
- No hay campo de búsqueda ni salto a "próxima clase". Es una agenda en lista, legible (sin tabla ni desbordamiento), pero las filas de clase no parecen pulsables (no hay botones en la lista, solo 3 botones en toda la vista).
- Mejora: buscador por título/asignatura, enlace "ir a la próxima clase", y filas tocables hacia la tutoría.

### P3 (medio) - "Qué toca estudiar hoy" poco útil e incoherente
- Hoy dice "No tienes clases pendientes." y lista 5 asignaturas todas con "Aún sin cronograma. Subir sílabo", pero el contador marca "1/2 clases (50%)". Contradicción (el calendario sí tiene 2 clases en octubre en "ejemplo-asignatura", que no aparece en Hoy).
- Hoy es largo (altura 1137 px, ~1,4 pantallas) y repite 5 veces "Subir sílabo". Debajo hay "Repaso: Nada pendiente hoy", "Preguntas nuevas", "Material nuevo / Procesar 25 archivos", que obligan a hacer scroll. Un estudiante ve el resumen útil solo tras bajar.
- Mejora: lo accionable arriba (una tarjeta "Siguiente clase" con botón Estudiar), y colapsar asignaturas sin cronograma en una sola línea.

### P4 (bajo) - Texto cortado en código en línea (Asignaturas > Proyectos)
- El fragmento `Obsidian/<Asignatura>/Proyectos/<Nombre>.md` queda cortado en el borde derecho de la tarjeta en 375px (screenshot). Aplicar `break-all`/`overflow-wrap:anywhere` al `<code>`.
- Tarjeta "Cortes de parcial": título envuelto en 2 líneas ("Cortes de / parcial") y descripción en columna muy estrecha (7 líneas) porque el botón "+ Añadir / editar cortes" ocupa la mitad del ancho; apilar en vertical en móvil.

### P4 (bajo) - Tema
- Existe selector de tema (Claro/Oscuro/Sistema) y modo oscuro funciona y se ve bien y legible en Hoy, Calendario y Ajustes (contraste correcto, sin elementos ilegibles). Comportamiento raro: tras recargar, el tema volvió a Claro aunque había elegido Oscuro; probablemente por la clave `ml_theme` de localStorage compartida con otras pestañas/agentes del mismo origen, no confirmado como bug.
- El selector de tema aparece dos veces (cabecera y pie del menú) ocupando espacio de cabecera en 375px.

### Positivo
- Menú hamburguesa con cajón lateral claro, cierra con X, 5 secciones fáciles de entender (Hoy, Estudiar, Calendario, Asignaturas, Ajustes).
- Sin desbordamiento horizontal en Hoy, Estudiar, Calendario, Ajustes. Sin tablas ilegibles encontradas.
- Tipografía legible, buen contraste en ambos temas, calendario móvil en formato lista.

## Secciones recorridas
Hoy, Estudiar (Tutoría/Repaso/Guía offline; solo vista, sin llamar a la IA), Calendario, Asignaturas (Clases, Material, Proyectos), Ajustes (Configuración; pestaña Plugins no abierta).

## Mejoras recomendadas (orden)
1. Arreglar ancho del select de asignatura y limitar longitud de nombres.
2. Objetivos táctiles de 44px (tema, calendario, pestañas, enlaces "Subir sílabo", botones destructivos separados).
3. Hoy: "Siguiente clase" arriba y coherencia del contador.
4. Calendario: búsqueda y atajo a la próxima clase.
5. Ajustar `<code>` y tarjeta de cortes para 375px.
