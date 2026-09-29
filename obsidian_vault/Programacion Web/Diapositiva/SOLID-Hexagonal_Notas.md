---
materia: [[Programacion Web]]
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [programacion_web, diapositiva, ingesta_ia]
---

# Arquitectura Hexagonal y Principios [[SOLID]]
## Entendiendo el Código a través de la Cocina
### Un enfoque práctico con [[Node.js]] y [[Express]]

> **Diagrama detectado:** Captura de la diapositiva de título. A la izquierda, el título principal sobre un fondo oscuro junto con un fragmento de código que configura una ruta de Express (`app.get('/6A/mensaje', (req, res) => { ... })`). A la derecha, una ilustración isométrica de una estación de cocina metálica con una campana extractora y un cuchillo sobre la tabla.

---

## El Plano del Restaurante: Separación de Responsabilidades
Cómo organizamos nuestro directorio `src/` para evitar el caos.

- **`dominio/`** (`Mensaje.js`)
- **`aplicacion/`** (`ObtenerMensaje.js`, `MensajePuerto.js`)
- **`infraestructura/`** (`MensajeHttpAdapter.js`, `MensajeMemoriaAdapter.js`)

> **Diagrama detectado:** Tres columnas que ilustran la división del proyecto. 
> 1. **El Libro de Recetas:** Representa el dominio. La verdad fundamental. No sabe ni le importa dónde está el restaurante.
> 2. **La Cocina & El Chef:** Representa la aplicación. El flujo central. Reciben órdenes y preparan, pero nunca hablan directamente con el cliente.
> 3. **Comedor y Despensa:** Representa la infraestructura. El mundo exterior. Meseros hablan con clientes, despensa entrega ingredientes brutos.

---

## S — [[Single Responsibility Principle (SRP)]]
Una clase debe tener una sola razón para cambiar. El Chef no toma pedidos.

> **Diagrama detectado:** Comparación entre un diseño incorrecto y uno correcto. 
> - **Código incorrecto (Caos):** Muestra una clase `MensajeService` que maneja tanto la lógica de negocio como la respuesta HTTP con `res.json()`. Ilustrado con un chef estresado cocinando mientras atiende llamadas y toma notas.
> - **Código correcto (Orden):** Separa la clase `ObtenerMensaje` (que solo ejecuta y retorna el mensaje) de `MensajeHttpAdapter`. Ilustrado con un mesero tomando pedidos ordenadamente y un chef concentrado únicamente en cocinar en su estación.

---

## O — [[Open/Closed Principle (OCP)]]
Abierto para extensión, cerrado para modificación. El Menú Extensible.

- `class MensajeSaludo { obtener() { return 'Hola Mundo'; } }`
- `class MensajeBienvenida { obtener() { return 'Bienvenido a Programación Web'; } }`

> **Diagrama detectado:** Se ilustra que se agregan nuevas implementaciones sin modificar el caso de uso central. A la derecha, una mano coloca una tarjeta de "Especial del Día" sobre un libro de menú de un restaurante, simbolizando la extensión del menú sin alterar la estructura base del recetario.

---

## L — [[Liskov Substitution Principle (LSP)]]
Cualquier implementación debe poder sustituir a otra. El Chef Sustituto.

- **Constructor:** `constructor(mensajePuerto) { this.mensajePuerto = mensajePuerto; }`
- **Componentes intercambiables:** `MensajeSaludo` y `MensajeBienvenida`.

> **Diagrama detectado:** A la izquierda, un diagrama de bloques tipo puzzle muestra cómo `ObtenerMensaje` puede trabajar con cualquiera de las dos clases de mensaje sin romper la aplicación, porque ambas implementan `obtener()`. A la derecha, un chef principal señala a ayudantes de cocina organizados en la estación de preparación.

---

## I — [[Interface Segregation Principle (ISP)]]
No obligues a depender de métodos innecesarios. Estaciones Especializadas.

- **Puerto inflado (Incorrecto):** `class MensajePuerto` con `obtener()`, `guardar()`, `eliminar()`, `enviarCorreo()`, `imprimir()`.
- **Puertos segregados (Correcto):** `ObtenerMensajePuerto` (solo `obtener()`) y `GuardarMensajePuerto` (solo `guardar(mensaje)`).

> **Diagrama detectado:** A la derecha superior, una estación saturada con múltiples electrodomésticos y herramientas peligrosas y caóticas (licuadora, tostadora, caja registradora, sierra eléctrica). A la derecha inferior, una tabla de herramientas ordenada en la pared ("Usa solo la herramienta que necesitas").

---

## D — [[Dependency Inversion Principle (DIP)]]
Depende de abstracciones, no de detalles. Proveedores Intercambiables.

- **Código incorrecto:** `const mysql = new MySQL(); return mysql.obtenermensaje();`
- **Código correcto:** `this.mensajePuerto = mensajePuerto; return this.mensajePuerto.obtener();`

> **Diagrama detectado:** A la derecha, se contrasta un "Bad Pattern" donde el chef está encadenado a un camión de distribución específico ("Granja MySQL"), frente al "Hexagonal Pattern", donde el núcleo dicta el contrato de ingredientes (`[[Interface]]`) y múltiples proveedores de infraestructura (MySQL, PostgreSQL, Memoria DB) se adaptan a él mediante camiones intercambiables.

---

## La Gran Apertura: Conectando las Piezas en `app.js`
Inyección de Dependencias: Asignando al equipo a sus estaciones antes de abrir.

1. `const mensajeRepositorio = new MensajeMemoriaAdapter();`
2. `const obtenerMensaje = new ObtenerMensaje(mensajeRepositorio);`
3. `const mensajeHttp = new MensajeHttpAdapter(obtenerMensaje);`

> **Diagrama detectado:** A la derecha, un rompecabezas ensambla las piezas del sistema: Chef / Caso de Uso, Despensa / Memoria DB, y Mesero / HTTP Adapter. El archivo `app.js` actúa como el Gerente del restaurante que conecta manualmente los adaptadores al núcleo antes de abrir las puertas.

---

## El Viaje de la Orden: Flujo de la Arquitectura
Cómo viaja la petición HTTP a través de nuestras capas aisladas.

1. **Comedor (Externa / Infraestructura):** Petición HTTP GET $\rightarrow$ Express $\rightarrow$ `MensajeHttpAdapter`. *(Metáfora: Cliente pide al Mesero).*
2. **La Estación de Mando (Puertos):** Adaptador llama al Caso de Uso (`ObtenerMensaje`). *(Metáfora: Mesero deja el ticket de la orden en la cocina).*
3. **La Cocina (Dominio / Aplicación):** Caso de Uso pide datos a través de `MensajePuerto`. *(Metáfora: Chef lee la receta y pide los ingredientes exactos).*
4. **La Despensa (Infraestructura de Datos):** `MensajeMemoriaAdapter` retorna 'Hola Mundo'. *(Metáfora: Ayudante trae los ingredientes. El plato se cocina y viaja de regreso al cliente).*

---

## Matriz de Diagnóstico: [[SOLID]] en la Arquitectura Hexagonal
El resumen definitivo para el arquitecto de software.

| Principio | El Síntoma del Caos (Si lo ignoramos) | La Solución Hexagonal | El Equivalente en el Restaurante |
| :--- | :--- | :--- | :--- |
| **[S] [[Single Responsibility Principle (SRP)\|SRP]]** | Cambiar la base de datos rompe la respuesta web HTTP. | Cada clase tiene una sola responsabilidad concreta. | El mesero intenta cocinar y servir al mismo tiempo. |
| **[O] [[Open/Closed Principle (OCP)\|OCP]]** | Hay que reescribir el caso de uso para un nuevo mensaje. | Se agregan nuevas implementaciones sin tocar la lógica central. | Hay que reescribir todo el menú para añadir un postre. |
| **[L] [[Liskov Substitution Principle (LSP)\|LSP]]** | El caso de uso falla si cambiamos el tipo de mensaje. | Una implementación del puerto reemplaza a otra perfectamente. | El Chef entra en pánico si le cambian al ayudante de cocina. |
| **[I] [[Interface Segregation Principle (ISP)\|ISP]]** | Adaptadores obligados a implementar métodos vacíos o inútiles. | Los puertos son pequeños, específicos y modulares. | Usar una licuadora industrial para cortar un tomate. |
| **[D] [[Dependency Inversion Principle (DIP)\|DIP]]** | El caso de uso depende directamente de MySQL o Express. | El caso de uso dicta el puerto; la infraestructura se adapta a él. | El Chef se niega a cocinar si el tomate no es de una granja específica. |

---

## Tu Primer Turno como Arquitecto en Jefe
Prueba la flexibilidad de tu nuevo sistema.

> **Diagrama detectado:** A la izquierda, una consola ejecutando `npm start` y una respuesta HTTP `200 OK` con el JSON `{ 'mensaje': 'Hola Mundo' }`. A la derecha, un portapapeles titulado **"Misión del Día"** con una lista de verificación:
> - [ ] **Aplica OCP:** Crea una nueva implementación `MensajeDespedida` que retorne "Hasta luego".
> - [ ] **Aplica LSP:** Comprueba que `ObtenerMensaje` funciona con esta nueva clase sin modificar su código interno.
> - [ ] **Aplica DIP:** Crea un nuevo adaptador de salida que obtenga el mensaje desde un arreglo en memoria, reemplazando al actual.
> - [ ] **Valida:** Prueba el endpoint desde tu navegador o [[Postman]]. ¿Se rompió algo? (Pista: ¡No debería!).