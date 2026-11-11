# Informe de accesibilidad (WCAG 2.2 AA) - persona Lucia (baja vision, teclado)

App: http://localhost:8001 (datos de ejemplo). axe-core 4.10.2 cargado sin problemas desde cdnjs (sin bloqueo CSP). Vistas probadas en modo Claro y Oscuro: Hoy, Estudiar (Tutoria, Repaso, Guia offline), Calendario, Asignaturas (Clases, Material, Proyectos), Ajustes (Configuracion, Plugins). Nota: el tema "Sistema" inicial resulto ser oscuro, por eso la primera pasada ya mostraba fallos en Hoy y Calendario.

## Lo que esta bien
- `lang="es"`, titulo de pagina, un unico h1 por vista, landmarks (header, nav, main, aside).
- Todos los botones/enlaces tienen nombre accesible, salvo los campos citados abajo.
- Zoom 200 % (640x360) y 1280x720: sin scroll horizontal ni elementos fuera de pantalla en ninguna vista (1.4.4, 1.4.10 OK).
- Botones de tema, pestañas y enlaces muestran foco nativo (outline auto).

## Hallazgos

### A1. Selects sin etiqueta asociada - CRITICO (axe select-name)
WCAG 1.3.1, 3.3.2, 4.1.2. Estudiar > Tutoria: selects "Asignatura" y "Profundidad" (2 nodos); Asignaturas > Clases/Material/Proyectos: select de asignatura (1 nodo). El texto visible esta en un elemento aparte y `select.labels.length = 0`. Un lector de pantalla solo anuncia "cuadro combinado" sin nombre. Reproducir: ir a /estudiar, ejecutar axe, o tabular hasta el select. Arreglo: `<label htmlFor>` o `aria-label`.

### A2. Campos de texto sin nombre accesible - ALTO
WCAG 1.3.1, 4.1.2, 3.3.2. Estudiar > Tutoria: input "Tema" (solo placeholder, 1 nodo) y 2 inputs en Ajustes (sin label ni aria-label). axe no lo marca como violacion en todos los casos porque el placeholder cuenta como nombre, pero el placeholder desaparece al escribir. Arreglo: label visible o aria-label.

### A3. Contraste insuficiente del texto secundario - SERIO (axe color-contrast)
WCAG 1.4.3 (minimo 4.5:1; el texto es de 11-14 px).
- Modo claro: #9c9381 sobre #fdfcf8 / #f9f7f1 = 2.83-2.96:1. Aparece en: "Puede ser cualquier tema..." (11 px), "Esta asignatura no tiene clases pendientes", "Sube el silabo oficial...", y en Ajustes > Plugins todos los subtitulos de ruta ("Ruta convencional (boveda de notas)", nombres de asignatura; 6 nodos). Boton rojo #ec003f sobre #f7f2ec = 4.21:1.
- Modo oscuro: #756d5e sobre #151412 = 3.59:1 y sobre #1f1d1a = 3.28:1. Aparece en pestañas inactivas (Repaso, Guia offline, Material, Proyectos, Plugins; 2-3 nodos por vista), "Nada pendiente hoy", "1/2 clases (50%)", Calendario ("No hay clases en este mes", leyenda "Completada"), "Cortes de parcial", "Contexto tecnico activo", botones con icono "Configurar carpeta". Tambien "+ Definir corte" #4f8e67 sobre #1f1d1a = 4.32:1 y boton rojo #ec003f sobre #1b1213 = 3.91:1.
- Total aprox.: 2-7 nodos por vista segun tema (Ajustes > Plugins es la peor: 6-7).
Reproducir: activar tema (Claro/Oscuro) y ejecutar axe en cada vista. Arreglo: oscurecer #9c9381 hasta >= 4.5:1 sobre el crema (aprox. #6f6858) y aclarar #756d5e en oscuro (aprox. #9a917f).

### A4. Orden de encabezados saltado - MODERADO (axe heading-order)
WCAG 1.3.1 (buena practica 2.4.6). h1 va directo a h3 en Estudiar ("Que vas a estudiar"), Asignaturas (nombres de asignatura), Ajustes (Cisco Packet Tracer, etc.). Hoy tiene h1, h2, h3 correcto. Arreglo: usar h2 o cambiar el nivel.

### A5. Select sin indicador de foco visible - ALTO
WCAG 2.4.7, 2.4.11 (foco visible/no oculto). Los `<select>` usan `focus:outline-none focus:ring-1 ...`, pero con el select enfocado (`:focus-visible` verdadero) el estilo computado muestra `outline: none` y `box-shadow: none`: no hay anillo. El input de texto si lo tiene (box-shadow). Reproducir: en /estudiar, tabular hasta "Asignatura" y observar. Arreglo: restaurar outline o ring visible con contraste 3:1.

### A6. Menu movil sin semantica ni cierre con Escape - ALTO
WCAG 4.1.2, 2.1.1, 2.1.2 (menu), 2.4.3. A anchos < 1024 px, el boton "Abrir menu" no tiene `aria-expanded`, el panel no es `role="dialog"` ni `aria-modal`, el foco no se mueve al panel y Escape no lo cierra (probado: tras Escape el panel sigue abierto). No se detecto trampa de foco pero tampoco contencion. Reproducir: ventana estrecha, foco en "Abrir menu", Enter, Escape.

### A7. Sin enlace "Saltar al contenido" y navegacion duplicada - MEDIO
WCAG 2.4.1 (bloques). En cada pagina hay que tabular logo, Claro, Oscuro, Sistema, Abrir menu, y en escritorio ademas toda la barra lateral antes del contenido (hay dos `aside` y dos enlaces del logo / selectores de tema duplicados en el DOM, uno oculto segun el ancho). No hay enlace de salto ni `id` en main. En Hoy hay 5 enlaces "Subir silabo" con el mismo nombre (WCAG 2.4.4: el contexto de cada uno no es identificable solo por el enlace; añadir aria-label con la asignatura).

### A8. Controles de tema sin estado - MEDIO
WCAG 4.1.2. Botones Claro/Oscuro/Sistema (iconos con nombre) no exponen `aria-pressed`; no se anuncia cual esta activo.

### A9. Pestañas: roles parciales - MEDIO
WCAG 4.1.2 / 1.3.1. Los botones tienen `role="tab"` y `aria-selected`, pero la tabulacion recorre todas las pestañas (no hay roving tabindex ni flechas) y no se confirmo `role="tablist"`/`tabpanel`. Revisar patron ARIA de pestañas.

### A10. Objetivos pequeños - BAJO
WCAG 2.5.8 (24 px). En Hoy, 13 controles miden < 24 px en ancho o alto (iconos/enlaces cortos). El resto de vistas, 0.

## Teclado
- Se alcanzan todos los controles con Tab; no hay trampas de foco; el orden es logico (logo, tema, menu, pestañas, formulario).
- Escape no cierra el menu movil (A6). No se probaron dialogos que invoquen a la IA (instruccion).

## Resumen de violaciones axe (por regla)
| Regla | Impacto | Nodos (por vista) |
|---|---|---|
| select-name | critico | 2 en Estudiar>Tutoria, 1 en cada pestaña de Asignaturas |
| color-contrast | serio | 1-7 por vista; en las 10 vistas oscuras y 8 de las claras |
| heading-order | moderado | 1 en Estudiar>Tutoria, Asignaturas (3 pestañas), Ajustes (2 pestañas) |

Hoy, Calendario, Estudiar>Repaso y Guia offline en modo claro: sin violaciones; Ajustes>Configuracion claro solo heading-order.

## Zoom
1280x720 y 640x360: sin desbordamiento horizontal (scrollWidth = innerWidth) en las 5 vistas; viewport restablecido a desktop.
