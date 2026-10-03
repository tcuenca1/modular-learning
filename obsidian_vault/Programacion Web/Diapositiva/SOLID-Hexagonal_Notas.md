---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [programacion_web, diapositiva, ingesta_ia]
---

# [[Programacion Web]]: Arquitectura Hexagonal y Principios [[SOLID]]

## Entendiendo el Código a través de la Cocina
Un enfoque práctico con [[Node.js]] y [[Express]]

> **Imagen detectada (Página 1):** Portada de la presentación con el título principal "Arquitectura Hexagonal y Principios SOLID" y un subtítulo que indica un enfoque práctico con Node.js y Express. A la derecha se muestra una ilustración 3D de una barra de cocina metálica con una campana extractora y un cuchillo. A la izquierda, un bloque de código mostrando una ruta básica de Express: `app.get('/6A/mensaje', (req, res) => { ... });`.

---

## El Plano del Restaurante: Separación de Responsabilidades
Cómo organizamos nuestro directorio `src/` para evitar el caos.

- `dominio/Mensaje.js`
- `aplicacion/ObtenerMensaje.js`, `MensajePuerto.js`
- `infraestructura/MensajeHttpAdapter.js`, `MensajeMemoriaAdapter.js`

> **Diagrama detectado (Página 2):** Estructura visual de carpetas en [[Arquitectura Hexagonal]] comparada con una cocina:
> 1. **El Libro de Recetas (Dominio):** La verdad fundamental. No sabe ni le importa dónde está el restaurante.
> 2. **La Cocina & El Chef (Aplicación):** El flujo central. Reciben órdenes y preparan, pero nunca hablan directamente con el cliente.
> 3. **Comedor y Despensa (Infraestructura):** El mundo exterior. Meseros hablan con clientes, despensa entrega ingredientes brutos.

---

## S — [[Single Responsibility Principle (SRP)]]
*Una clase debe tener una sola razón para cambiar. El Chef no toma pedidos.*

> **Diagrama detectado (Página 3):** 
> - **Caos (Incorrecto):** Una clase `MensajeService` que maneja tanto la lógica de negocio como la respuesta HTTP (`res.json`). Ilustración superior de un chef estresado intentando cocinar mientras atiende y toma notas.
> - **Orden (Correcto):** Separación en clases independientes como `ObtenerMensaje` (lógica) y `MensajeHttpAdapter` (transporte). Ilustración inferior de un mesero tomando pedidos ordenadamente separado del chef en su cocina.

---

## O — [[Open/Closed Principle (OCP)]]
*Abierto para extensión, cerrado para modificación. El Menú Extensible.*

> **Diagrama detectado (Página 4):** Código que muestra la creación de nuevas implementaciones (`MensajeSaludo` y `MensajeBienvenida`) que extienden el comportamiento sin modificar el caso de uso central. A la derecha, la metáfora de un menú de restaurante al que se le añade una página de "Especial del Día".

---

## L — [[Liskov Substitution Principle (LSP)]]
*Cualquier implementación debe poder sustituir a otra. El Chef Sustituto.*

> **Diagrama detectado (Página 5):** Esquema de inyección donde `ObtenerMensaje` recibe un `mensajePuerto` y puede trabajar indistintamente con `MensajeSaludo` o `MensajeBienvenida` porque ambas implementan el método `obtener()`. A la derecha, un chef señala hacia la cocina indicando un reemplazo fluido ("¡Salsa!").

---

## I — [[Interface Segregation Principle (ISP)]]
*No obligues a depender de métodos innecesarios. Estaciones Especializadas.*

> **Diagrama detectado (Página 6):** 
> - **Incorrecto:** Una interfaz o clase `MensajePuerto` masiva con métodos como `obtener()`, `guardar()`, `eliminar()`, `enviarCorreo()`, `imprimir()`. Ilustración de una estación de cocina caótica con una licuadora, tostadora, panel de advertencias y hasta una motosierra.
> - **Correcto:** Interfaces segregadas y pequeñas (`ObtenerMensajePuerto` y `GuardarMensajePuerto`). Ilustración de un tablero ordenado con herramientas específicas y precisas ("Usa solo la herramienta que necesitas").

---

## D — [[Dependency Inversion Principle (DIP)]]
*Depende de abstracciones, no de detalles. Proveedores Intercambiables.*

> **Diagrama detectado (Página 7):**
> - **Bad Pattern:** Dependencia directa de una base de datos concreta (`const mysql = new MySQL();`). Ilustración de un camión de reparto atado al chef.
> - **Hexagonal Pattern:** Uso de interfaces/contratos de ingredientes. Ilustración de múltiples camiones intercambiables (`MySQL`, `PostgreSQL`, `Memoria DB`) adaptándose al contrato dictado por el núcleo.

---

## La Gran Apertura: Conectando las Piezas en `app.js`
*Inyección de Dependencias: Asignando al equipo a sus estaciones antes de abrir.*

1. `const mensajeRepositorio = new MensajeMemoriaAdapter();`
2. `const obtenerMensaje = new ObtenerMensaje(mensajeRepositorio);`
3. `const mensajeHttp = new MensajeHttpAdapter(obtenerMensaje);`

> **Diagrama detectado (Página 8):** Rompecabezas de arquitectura conectando las piezas: Chef/Caso de Uso, Despensa/Memoria DB y Mesero/HTTP Adapter. `app.js` actúa como el Gerente del restaurante que conecta manualmente los adaptadores al núcleo.

---

## El Viaje de la Orden: Flujo de la Arquitectura
*Cómo viaja la petición HTTP a través de nuestras capas aisladas.*

1. **Comedor (Externa / Infraestructura):** Petición HTTP GET $\rightarrow$ [[Express]] $\rightarrow$ `MensajeHttpAdapter`. *(Metáfora: Cliente pide al Mesero).*
2. **La Estación de Mando (Puertos):** Adaptador llama al Caso de Uso (`ObtenerMensaje`). *(Metáfora: Mesero deja el ticket de la orden en la cocina).*
3. **La Cocina (Dominio / Aplicación):** Caso de Uso pide datos a través de `MensajePuerto`. *(Metáfora: Chef lee la receta y pide los ingredientes exactos).*
4. **La Despensa (Infraestructura de Datos):** `MensajeMemoriaAdapter` retorna 'Hola Mundo'. *(Metáfora: Ayudante trae los ingredientes. El plato se cocina y viaja de regreso al cliente).*

---

## Matriz de Diagnóstico: [[SOLID]] en la Arquitectura Hexagonal
*El resumen definitivo para el arquitecto de software.*

| Principio | El Síntoma del Caos (Si lo ignoramos) | La Solución Hexagonal | El Equivalente en el Restaurante |
| :--- | :--- | :--- | :--- |
| **[S] [[Single Responsibility Principle (SRP)|SRP]]** | Cambiar la base de datos rompe la respuesta web HTTP. | Cada clase tiene una sola responsabilidad concreta. | El mesero intenta cocinar y servir al mismo tiempo. |
| **[O] [[Open/Closed Principle (OCP)|OCP]]** | Hay que reescribir el caso de uso para un nuevo mensaje. | Se agregan nuevas implementaciones sin tocar la lógica central. | Hay que reescribir todo el menú para añadir un postre. |
| **[L] [[Liskov Substitution Principle (LSP)|LSP]]** | El caso de uso falla si cambiamos el tipo de mensaje. | Una implementación del puerto reemplaza a otra perfectamente. | El Chef entra en pánico si le cambian al ayudante de cocina. |
| **[I] [[Interface Segregation Principle (ISP)|ISP]]** | Adaptadores obligados a implementar métodos vacíos o inútiles. | Los puertos son pequeños, específicos y modulares. | Usar una licuadora industrial para cortar un tomate. |
| **[D] [[Dependency Inversion Principle (DIP)|DIP]]** | El caso de uso depende directamente de [[MySQL]] o Express. | El caso de uso dicta el puerto; la infraestructura se adapta a él. | El Chef se niega a cocinar si el tomate no es de una granja específica. |

---

## Tu Primer Turno como Arquitecto en Jefe
*Prueba la flexibilidad de tu nuevo sistema.*

> **Imagen detectada (Página 11):** Consola ejecutándose en el puerto 3000 con la respuesta HTTP 200 OK retornando `{'mensaje': 'Hola Mundo'}`. A la derecha, una libreta tipo "Misión del Día" con un checklist:
> - [ ] Aplica OCP: Crea una nueva implementación `MensajeDespedida` que retorne "Hasta luego".
> - [ ] Aplica LSP: Comprueba que `ObtenerMensaje` funciona con esta nueva clase sin modificar su código interno.
> - [ ] Aplica DIP: Crea un nuevo adaptador de salida que obtenga el mensaje desde un arreglo en memoria, reemplazando al actual.
> - [ ] Valida: Prueba el endpoint desde tu navegador o [[Postman]]. ¿Se rompió algo? (Pista: ¡No debería!).