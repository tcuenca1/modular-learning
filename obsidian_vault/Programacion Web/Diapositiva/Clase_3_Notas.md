---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [programacion_web, diapositiva, ingesta_ia]
---

[[Programacion Web]]

# Construyendo Software que no se Derrumba
## Entendiendo el Acoplamiento, la Cohesión y los Principios [[SOLID]] (sin escribir una sola línea de código)

> **Diagrama detectado:** Ilustración isométrica de un cubo construido con bloques de tipo LEGO de colores. Varios bloques en la esquina superior izquierda se están desprendiendo en una explosión controlada, mostrando herramientas de medición como un calibrador pie de rey y planos técnicos alrededor.
---

## La trampa de la Deuda Técnica

### El Camino Rápido
> **Diagrama detectado:** Una torre hecha de ladrillos desgastados y rústicos, completamente sujeta por múltiples capas de cinta adhesiva gris. Muestra símbolos de advertencia y líneas de tensión estructural rota.

Entregar rápido tiene un costo. La deuda técnica ocurre cuando elegimos la solución más rápida en lugar de la más efectiva. A corto plazo, ganamos tiempo. A largo plazo, cada cambio amenaza con derrumbar el sistema entero.

### El Camino Sostenible
> **Diagrama detectado:** Una torre alta, estilizada y perfectamente estructurada compuesta de bloques modulares azules con diseño tecnológico, con planos detallados a los costados que muestran medidas exactas.

Construir con piezas bien diseñadas toma más tiempo inicial, pero permite escalar, modificar y mantener el sistema sin miedo a romperlo.
---

## Los 4 síntomas de un diseño enfermo

1. **Rigidez**
   > **Diagrama detectado:** Un bloque de cemento gris macizo, pesado, atravesado por barras de metal dobladas y marcas de medición técnica.
   > El sistema es difícil de cambiar porque un pequeño ajuste requiere modificar docenas de otras piezas.

2. **Fragilidad**
   > **Diagrama detectado:** Un panel de vidrio grueso que se ha agrietado en múltiples direcciones tras un impacto en un punto específico.
   > Al cambiar algo en un lugar, el sistema se rompe en sitios que aparentemente no tenían relación.

3. **Inmovilidad**
   > **Diagrama detectado:** Un barco de papel frágil atado fuertemente a una gran ancla de hierro oxidada mediante cadenas pesadas.
   > Imposible reutilizar partes del código en otros proyectos (quería el plátano, pero me traje el gorila y la selva entera).

4. **Viscosidad**
   > **Diagrama detectado:** Un engranaje mecánico metálico cubierto por una sustancia verde viscosa y tóxica que gotea.
   > Es más fácil hacer hacks temporales que hacer las cosas bien respetando la arquitectura original.
---

## Las dos fuerzas fundamentales de la arquitectura

### [[Cohesión]] (La fuerza interna)
> **Diagrama detectado:** Un núcleo electromagnético circular rodeado de bobinas de cobre densas que irradian un brillo solar intenso y energía electromagnética controlada en su interior.
> Mide qué tan relacionadas están las piezas funcionales dentro de un mismo módulo. *(El grado en que los elementos permanecen juntos por un propósito común)*.

### [[Acoplamiento]] (La fuerza externa)
> **Diagrama detectado:** Dos gabinetes mecánicos industriales complejos conectados caóticamente entre sí por un haz masivo de tuberías de metal y cables azules entrelazados.
> Mide el nivel de interdependencia entre diferentes módulos. (Si el componente A cambia, qué tan fuerte golpea al componente B?).
---

## El mapa del tesoro del programador

> **Diagrama detectado:** Una matriz de 2x2 sobre un plano azul de ingeniería técnica con flechas de ejes indicando [[Cohesión]] (eje Y: Baja a Alta) y [[Acoplamiento]] (eje X: Bajo a Alto).
> - **Cuadrante Superior Izquierdo (Alta Cohesión, Bajo Acoplamiento):** El Estado Ideal. Módulos independientes, enfocados en una sola tarea, fáciles de mantener y reutilizar (representado con bloques LEGO limpios y conectados por un cable USB).
> - **Cuadrante Superior Derecho (Alta Cohesión, Alto Acoplamiento):** Tareas bien definidas, pero demasiado dependientes unas de otras (bloques LEGO asegurados con cadenas pesadas y un candado).
> - **Cuadrante Inferior Izquierdo (Baja Cohesión, Bajo Acoplamiento):** Módulos independientes, pero internamente caóticos y sin un propósito claro (montones de bloques LEGO multicolores mezclados sin orden).
> - **Cuadrante Inferior Derecho (Baja Cohesión, Alto Acoplamiento):** [[Código Espagueti]]. El caos total. El efecto dominó está garantizado (una masa fundida de bloques LEGO destruidos rodeados de cadenas y señales de peligro).
---

## La Caja de Herramientas: Los Principios [[SOLID]]

Para alcanzar la Alta [[Cohesión]] y el Bajo [[Acoplamiento]], los ingenieros utilizan cinco de diseño. No son leyes inmutables, son herramientas para dar forma a nuestras piezas de software para que encajen de manera perfecta, predecible y segura.

> **Diagrama detectado:** Sobre una mesa de trabajo metálica pulida, se muestran en fila cinco herramientas y objetos modulares: un cuchillo de chef azul, un cartucho de videojuego rojo, pilas recargables, un control remoto verde y un contacto de pared eléctrico naranja.
---

## [S] [[Principio de Responsabilidad Única]]
Una clase debe tener una sola razón para cambiar.

> **Diagrama detectado:** Comparación visual dividida en dos zonas:
> - **Izquierda (Baja Cohesión):** Un fondo de advertencia con rayas de peligro amarillas y negras, mostrando una navaja suiza sobrecargada con múltiples herramientas desplegadas de forma caótica (sierras, tijeras, destornilladores, secador de pelo, motosierra, pistola láser).
> - **Derecha (Alta Cohesión):** Un fondo azul limpio que muestra un único cuchillo de chef profesional azul, elegante y perfectamente afilado.

No significa que un módulo haga una sola acción, sino que responda a un único propósito de negocio. Si una pieza procesa pagos, guarda en base de datos y envía emails, un cambio en la factura romperá el envío de correos. Separa las responsabilidades.
---

## [O] [[Principio Abierto / Cerrado]]
El software debe estar abierto a la extensión, pero cerrado a la modificación.

> **Diagrama detectado:** Una consola de videojuegos de diseño futurista gris donde se inserta limpiamente un cartucho dorado superior, mientras una mano con un destornillador y una gran marca roja en "X" tacha la opción de desarmar el dispositivo por la fuerza.

Puedes agregar nuevas funcionalidades (nuevos cartuchos) tanpa tener que desarmar el código base que ya funciona. Si quieres añadir Pagos con PayPal a un sistema que ya usa Tarjetas, no edites el archivo original; crea una nueva extensión que se conecte al sistema.
---

## [L] [[Principio de Sustitución de Liskov]]
Las piezas hijas deben poder reemplazar a sus piezas padre sin romper el sistema.

> **Diagrama detectado:** Un control remoto inalámbrico futurista con la tapa del compartimento de baterías abierta, mostrando dos baterías cilíndricas (una naranja y una verde brillante) siendo insertadas de manera intercambiable.

Si tu sistema espera una Batería, cualquier marca de batería debería funcionar sin que el control remoto tenga que reprogramarse para entenderla. Si una nueva pieza hija lanza errores inesperados cuando intentas usarla, estás violando este principio.
---

## [I] [[Principio de Segregación de Interfaces]]
Es mejor tener muchas interfaces pequeñas y específicas que una interfaz gigante y general.

> **Diagrama detectado:** Comparativa entre dos controles remotos:
> - **Interfaces Gigantes:** Un control remoto masivo, saturado de cientos de botones diminutos, interruptores y antenas múltiples.
> - **Interfaces Segregadas:** Un control remoto minimalista, estilizado, con solo los botones esenciales distribuidos de forma ergonómica.

Ningún componente debe verse obligado a depender de métodos (botones) que no utiliza. En lugar de crear un contrato masivo para todo el sistema, divídelo en contratos pequeños que entreguen exactamente lo que cada cliente necesita.
---

## [D] [[Principio de Inversión de Dependencias]]
Depende de abstracciones, no de implementaciones concretas.

> **Diagrama detectado:** Una lámpara de escritorio articulada de color azul cuyo cable termina en un enchufe estándar conectado firmemente a una toma de corriente de pared, etiquetado visualmente como **Abstracción (El Contrato)**.

El sistema principal no debe depender de detalles de bajo nivel (como una base de datos específica o un framework). Ambos deben depender de contratos (enchufes). Si mañana cambias de lámpara o de proveedor eléctrico, el enchufe estándar asegura que nada explote.
---

## El lado oscuro de [[SOLID]]: La Sobre-ingeniería

> **Diagrama detectado:** Una enorme grúa de construcción industrial amarilla y pesada sobre un terreno de tierra, sosteniendo mediante un gancho gigante un simple martillo de carpintero que intenta clavar un único clavo en una tabla de madera.

Aplicar [[SOLID]] sin criterio es tan destructivo como ignorarlo. Crear abstracciones para problemas que aún no existen (por si acaso) resulta en un laberinto de código. Single Responsibility no significa una clase por cada verbo. No construyas una grúa industrial para clavar un clavo.
---

## ¿Cuándo abstraer? La Regla de Tres

1. **Haz que funcione (La Primera Vez)**
   > **Diagrama detectado:** Un icono de un engranaje técnico simple dentro de un recuadro azul.
   > Escribe el código directamente. Resuelve el problema actual sin anticipar estructuras futuras que quizás nunca necesites.

2. **Cópialo sin culpa (La Segunda Vez)**
   > **Diagrama detectado:** Dos iconos de engranajes superpuestos sobre documentos de papel duplicados.
   > Si el requerimiento se repite con una pequeña variación, duplica el código. Aún no tienes suficiente evidencia para crear un patrón general.

3. **Refactoriza con [[SOLID]] (La Tercera Vez)**
   > **Diagrama detectado:** Un conjunto de engranajes entrelazados de colores azul y verde brillante en alta resolución.
   > Al tercer uso, el patrón es real. Ahora sí, abre la caja de herramientas [[SOLID]] y extrae la abstracción. La extensión ya no es una hipótesis, es una realidad probada.
---

## Síntesis: El Ecosistema Equilibrado

> **Diagrama detectado:** Una interfaz de aplicación web modular montada sobre bloques LEGO gigantescos, mostrando una perfecta alineación superior y conexiones modulares laterales delimitadas por cotas técnicas de diseño.

- **El Objetivo:** Alta cohesión (piezas sólidas) y Bajo acoplamiento (conexiones limpias).
- **Las Herramientas:** Los principios [[SOLID]] son el vocabulario y las técnicas para esculpir estas piezas.
- **La Sabiduría:** Las abstracciones deben ganarse, no adivinarse. Usa [[SOLID]] para curar el dolor del código, no para anticipar futuros.
- **El Resultado:** Software web preparado para el cambio, resistente a las fallas, y un placer para el próximo desarrollador.