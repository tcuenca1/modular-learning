---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [programacion_web, diapositiva, ingesta_ia]
---

[[Programacion Web]]

# Construyendo Software que no se Derrumba
## Entendiendo el [[Acoplamiento]], la [[Cohesión]] y los [[Principios SOLID]] (sin escribir una sola línea de código)

> **Diagrama detectado:** Ilustración isométrica de una estructura construida con bloques de LEGO multicolor sobre una cuadrícula técnica. Un sector de la estructura aparece explotando y desarmándose, mientras al lado se muestran herramientas de precisión como un calibrador pie de rey y una regla sobre planos arquitectónicos.

---

## La trampa de la [[Deuda Técnica]]

### El Camino Rápido
> **Diagrama detectado:** Una torre hecha de ladrillos rústicos e irregulares sostenida precariamente por cinta adhesiva gris, con múltiples símbolos de advertencia (!). Un ladrillo superior se está cayendo y genera chispas y grietas en la estructura.

Entregar rápido tiene un costo. La deuda técnica ocurre cuando elegimos la solución más rápida en lugar de la más efectiva. A corto plazo, ganamos tiempo. A largo plazo, cada cambio amenaza con derrumbar el sistema entero.

### El Camino Sostenible
> **Diagrama detectado:** Una torre alta y esbelta construida con bloques modulares de color azul con un diseño limpio e industrial, rodeada de líneas de medición técnica y cotas arquitectónicas.

Construir con piezas bien diseñadas toma más tiempo inicial, pero permite escalar, modificar y mantener el sistema sin miedo a romperlo.

---

## Los 4 síntomas de un [[diseño enfermo]]

### Rigidez
> **Diagrama detectado:** Un bloque de concreto macizo atravesado por barras de metal expuestas, con marcas de cotas de medición.

El sistema es difícil de cambiar porque un pequeño ajuste requiere modificar docenas de otras piezas.

### Fragilidad
> **Diagrama detectado:** Un panel de vidrio transparente que se rompe en múltiples fragmentos y grietas tras un impacto localizado.

Al cambiar algo en un lugar, el sistema se rompe en sitios que aparentemente no tenían relación.

### Inmovilidad
> **Diagrama detectado:** Un ancla de barco oxidada junto a un pequeño bote de papel sobre planos con líneas punteadas.

Imposible reutilizar partes del código en otros proyectos (quería el plátano, pero me traje el gorila y la selva entera).

### Viscosidad
> **Diagrama detectado:** Un engranaje metálico cubierto por una sustancia verde y viscosa que gotea.

Es más fácil hacer hacks temporales que hacer las cosas bien respetando la arquitectura original.

---

## Las dos fuerzas fundamentales de la arquitectura

### Cohesión (La fuerza interna)
> **Diagrama detectado:** Un esquema circular que representa un núcleo energético con múltiples bobinas magnéticas conectadas e irradiando una luz brillante en el centro.

Mide qué tan relacionadas están las piezas funcionales dentro de un mismo módulo. *(El grado en que los elementos permanecen juntos por un propósito común).*

### Acoplamiento (La fuerza externa)
> **Diagrama detectado:** Dos cajas de maquinaria industrial complejas unidas y enredadas con una gran cantidad de tuberías azules y cables entrelazados.

Mide el nivel de interdependencia entre diferentes módulos. (Si el componente A cambia, ¿qué tan fuerte golpea al componente B?).

---

## El mapa del tesoro del programador

> **Diagrama detectado:** Una matriz de 2x2 sobre un fondo de plano técnico con ejes de Coordenadas (Eje Y: [[Cohesión]] de Baja a Alta; Eje X: [[Acoplamiento]] de Bajo a Alto):
> - **Cuadrante Superior Izquierdo (Alta Cohesión, Bajo Acoplamiento):** "El Estado Ideal. Módulos independientes, enfocados en una sola tarea, fáciles de mantener y reutilizar" representado por dos bloques LEGO conectados por un cable USB.
> - **Cuadrante Superior Derecho (Alta Cohesión, Alto Acoplamiento):** "Tareas bien definidas, pero demasiado dependientes unas de otras" representado por bloques de LEGO unidos por cadenas con candados.
> - **Cuadrante Inferior Izquierdo (Baja Cohesión, Bajo Acoplamiento):** "Módulos independientes, pero internamente caóticos y sin un propósito claro" representado por cúmulos de piezas de LEGO multicolores desordenadas.
> - **Cuadrante Inferior Derecho (Baja Cohesión, Alto Acoplamiento):** "Código Espagueti. El caos total. El efecto dominó está garantizado" representado por un montón derretido y enredado de bloques de LEGO rodeado de cadenas y fuego.

---

## La Caja de Herramientas: Los [[Principios SOLID]]

Para alcanzar la [[Alta Cohesión]] y el [[Bajo Acoplamiento]], los ingenieros utilizan cinco de diseño. No son leyes inmutables, son herramientas para dar forma a nuestras piezas de software para que encajen de manera perfecta, predecible y segura.

> **Diagrama detectado:** Una superficie metálica limpia donde se alinean de izquierda a derecha cinco herramientas u objetos analógicos: un cuchillo de cocina azul, un cartucho de videojuego rojo, unas pilas doble A, un control remoto verde y un contacto eléctrico de pared naranja.

---

## [S] [[Principio de Responsabilidad Única]]
Una clase debe tener una sola razón para cambiar.

> **Diagrama detectado:** Imagen dividida en dos contrastes:
> - **Izquierda (Baja Cohesión - Advertencia):** Una navaja suiza sobrecargada con múltiples herramientas desplegadas de forma caótica (secador de pelo, cuchillo, sierra eléctrica, taladro, lupa, destornilladores, etc.) generando chispas.
> - **Derecha (Alta Cohesión):** Un único cuchillo de chef profesional azul, elegante y de hoja afilada.

No significa que un módulo haga una sola acción, sino que responda a un único propósito de negocio. Si una pieza procesa pagos, guarda en base de datos y envía emails, un cambio en la factura romperá el envío de correos. Separa las responsabilidades.

---

## [O] [[Principio Abierto / Cerrado]]
El software debe estar abierto a la extensión, pero cerrado a la modificación.

> **Diagrama detectado:** Una consola de videojuegos gris con un diseño modular donde un cartucho de circuito dorado se inserta limpiamente desde arriba mediante una flecha blanca, mientras un destornillador rojo tachado con una gran "X" roja indica la prohibición de desarmar el núcleo.

Puedes agregar nuevas funcionalidades (nuevos cartuchos) sin tener que desarmar el código base que ya funciona. Si quieres añadir Pagos con PayPal a un sistema que ya usa Tarjetas, no edites el archivo original; crea una nueva extensión que se conecte al sistema.

---

## [L] [[Principio de Sustitución de Liskov]]
Las piezas hijas deben poder reemplazar a sus piezas padre sin romper el sistema.

> **Diagrama detectado:** Un control remoto inalámbrico gris con el compartimento de baterías abierto, mostrando dos opciones de baterías cilíndricas (una naranja y una verde brillante) siendo insertadas de forma intercambiable.

Si tu sistema espera una [[Batería]], cualquier marca de batería debería funcionar sin que el control remoto tenga que reprogramarse para entenderla. Si una nueva pieza hija lanza errores inesperados cuando intentas usarla, estás violando este principio.

---

## [I] [[Principio de Segregación de Interfaces]]
Es mejor tener muchas interfaces pequeñas y específicas que una interfaz gigante y general.

> **Diagrama detectado:** Comparación entre dos dispositivos:
> - **Izquierda (Interfaces Gigantes):** Un control remoto sobrecargado de docenas de botones diminutos, antenas e interruptores complejos con una luz roja encendida.
> - **Derecha (Interfaces Segregadas):** Un control remoto moderno, minimalista y limpio con pocos botones esenciales y una luz azul tenue.

Ningún componente debe verse obligado a depender de métodos (botones) que no utiliza. En lugar de crear un contrato masivo para todo el sistema, divídelo en contratos pequeños que entreguen exactamente lo que cada cliente necesita.

---

## [D] [[Principio de Inversión de Dependencias]]
Depende de abstracciones, no de implementaciones concretas.

> **Diagrama detectado:** Una lámpara de escritorio azul conectada mediante un cable eléctrico con un enchufe estándar que se dispone a conectarse a un tomacorriente de pared, etiquetado como `Abstracción (El Contrato)`.

El sistema principal no debe depender de detalles de bajo nivel (como una base de datos específica o un framework). Ambos deben depender de contratos (enchufes). Si mañana cambias de lámpara o de proveedor eléctrico, el enchufe estándar asegura que nada explote.

---

## El lado oscuro de SOLID: La Sobre-ingeniería

> **Diagrama detectado:** Una grúa de construcción industrial gigante de color amarillo levantando un diminuto martillo de carpintero que intenta clavar un simple clavo sobre una tabla de madera.

Aplicar [[Principios SOLID]] sin criterio es tan destructivo como ignorarlo. Crear abstracciones para problemas que aún no existen (por si acaso) resulta en un laberinto de código. [[Single Responsibility]] no significa una clase por cada verbo. No construyas una grúa industrial para clavar un clavo.

---

## ¿Cuándo abstraer? La Regla de Tres

> **Diagrama detectado:** Flujo secuencial de tres pasos con flechas azules:
> 1. **Haz que funcione (La Primera Vez):** Icono de un engranaje simple. *Texto:* Escribe el código directamente. Resuelve el problema actual sin anticipar estructuras futuras que quizás nunca necesites.
> 2. **Cópialo sin culpa (La Segunda Vez):** Icono de dos documentos con engranajes idénticos. *Texto:* Si el requerimiento se repite con una pequeña variación, duplica el código. Aún no tienes suficiente evidencia para crear un patrón general.
> 3. **Refactoriza con SOLID (La Tercera Vez):** Icono de tres engranajes interconectados de colores verde y azul. *Texto:* Al tercer uso, el patrón es real. Ahora sí, abre la caja de herramientas SOLID y extrae la abstracción. La extensión ya no es una hipótesis, es una realidad probada.

---

## Síntesis: El Ecosistema Equilibrado

> **Diagrama detectado:** Una vista general esquemática de una interfaz web integrada dentro de una estructura modular de bloques de LEGO, señalando la [[ALTA COHESIÓN]] en el panel lateral izquierdo, la [[CONEXIÓN MODULAR]] en los márgenes y la **ALINEACIÓN PERFECTA** en la barra superior.

* **El Objetivo:** Alta cohesión (piezas sólidas) y Bajo acoplamiento (conexiones limpias).
* **Las Herramientas:** Los [[Principios SOLID]] son el vocabulario y las técnicas para esculpir estas piezas.
* **La Sabiduría:** Las abstracciones deben ganarse, no adivinarse. Usa [[Principios SOLID]] para curar el dolor del código, no para anticipar futuros.
* **El Resultado:** Software web preparado para el cambio, resistente a las fallas, y un placer para el próximo desarrollador.