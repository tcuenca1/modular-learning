---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [programacion_web, diapositiva, ingesta_ia]
---

[[Programacion Web]]

# Arquitectura de Software: Entendiendo DTO y CQRS sin Complicaciones
Entendiendo sistemas complejos a través de analogías simples.

> **Diagrama detectado:** Vista general que compara un servidor de arquitectura de software a la izquierda con una cocina organizada como sistema a la derecha, unidos por una flecha central que indica "Traducción simple: DTO & CQRS en acción".

---

## El Gran Problema de las Aplicaciones que Crecen Demasiado

> **Diagrama detectado:** Ilustración de un escritorio saturado de papeles, cajas y una persona estresada cocinando y hablando por teléfono a la vez, destacando dos problemas: "Exposición de Datos" (mover estructuras pesadas por la red) y "Cuello de Botella (CRUD)" (usar la misma base de datos para leer y escribir al mismo tiempo).

A medida que una aplicación crece, enfrenta dos problemas críticos: transportar demasiados datos innecesarios a través de la red y sobrecargar el sistema al intentar realizar lecturas y escrituras en el mismo lugar de forma simultánea.

---

# Parte 1: Objetos de Transferencia de Datos ([[DTO]])

Resolviendo el problema de cómo transportamos la información de forma segura.

> **Diagrama detectado:** Icono central de una caja de envío cerrada con un candado, representando un [[DTO]].

---

## La Entidad de Negocio vs. El Paquete de Envío

| Entidad (El Chef) | [[DTO]] (El Repartidor) |
| :--- | :--- |
| > **Diagrama detectado:** Ilustración de un chef cocinando en una cocina llena de ingredientes y libros de recetas. | > **Diagrama detectado:** Ilustración de una bolsa de entrega con un ticket de pedido sobre una barra. |
| Contiene reglas de negocio, lógica compleja y secretos del sistema. Nunca debe salir de la cocina. | No tiene lógica, no sabe cocinar. Solo transporta el producto terminado del punto A al punto B. |

Una Entidad u objeto de negocio define un concepto central con comportamiento complejo. Un [[DTO]] (*Data Transfer Object*) se utiliza únicamente para aislar y transportar esos datos entre capas o procesos.

---

## Filtrando la Complejidad para el Cliente

> **Diagrama detectado:** Un embudo ("Capa del Adaptador DTO") que recibe múltiples servidores caóticos en la parte superior y entrega paquetes limpios a un teléfono móvil en la parte inferior.

*   **Eficiencia de Red:** Agrupa los datos para reducir las costosas llamadas remotas entre el cliente y el servidor.
*   **Desacoplamiento:** Aísla el modelo de dominio interno de la capa de presentación externa. Un cambio en la base de datos no rompe la aplicación móvil.

---

## Anatomía de un [[DTO]]: Cero Lógica, Cien Por Ciento Datos

> **Diagrama detectado:** Esquema desglosado de un servidor mostrando propiedades, getters y setters con marcas de verificación verdes a la izquierda, y símbolos de prohibición rojos a la derecha para "Sin Cálculos", "Sin Métodos" y "Sin Lógica de Negocio", acompañado de una tarjeta flotante con `Nombre: Hamburguesa, Precio: $10`.

Un [[DTO]] no calcula impuestos, no valida reglas comerciales y no guarda datos en la base de datos.  
**Su única responsabilidad es almacenar y entregar sus propios datos.**

---

# Parte 2: Segregación de Responsabilidades ([[CQRS]])

Resolviendo el cuello de botella dividiendo las lecturas de las escrituras.

> **Diagrama detectado:** Dos flechas curvas cruzadas, una naranja orientada hacia arriba y otra azul orientada hacia abajo.

---

## El Colapso del Sistema [[CRUD]] Tradicional

> **Diagrama detectado:** Un cilindro central de base de datos agrietado con múltiples flechas naranjas de "Escrituras complejas y transaccionales" entrando por la izquierda y un abanico masivo de flechas azules de "Millones de consultas por segundo" saliendo por la derecha.

En un sistema tradicional, intentar que una sola tabla cumpla con escrituras estrictas y lecturas masivas genera contención. Es como si el chef que cocina la comida fuera la única persona autorizada para dictar el menú a cada cliente.

---

## La Solución [[CQRS]]: Dividiendo el Restaurante en Dos

[[CQRS]] (*Command Query Responsibility Segregation*) parte de una idea simple: separar lógicamente (y a veces físicamente) el modelo que recibe escrituras del modelo que responde consultas.

> **Diagrama detectado:** División visual del sistema en dos secciones separadas por una línea punteada: A la izquierda el "Modelo de Escritura (Commands)" representado por una cocina activa, y a la derecha el "Modelo de Lectura (Queries)" representado por una pantalla de estado y clientes consultando menús.

---

## Los Comandos ([[Commands]]): Modificando el Estado

> **Diagrama detectado:** Ilustración de un chef cocinando carne a la parrilla junto con un icono de prohibido o acción de cambio.

*   **Intención:** Representa la intención de realizar una acción (ej. `CreateUserCommand`).
*   **Reglas Estrictas:** Valida la lógica de negocio y asegura la integridad transaccional.
*   **No devuelve datos:** Modifica el estado del dominio pero no responde con información (salvo confirmación de éxito/error).
*   **No Idempotente:** Ejecutar el mismo comando dos veces puede crear dos pedidos distintos.

---

## Las Consultas ([[Queries]]): Recuperando la Información

> **Diagrama detectado:** Pantalla de tablet mostrando un listado de órdenes con estados variados (Completada, En Proceso, Lista para Envío, Pendiente) protegida por un icono de un candado azul.

*   **Intención:** Solicita datos al sistema sin alterar su estado (ej. `GetUsersQuery`).
*   **Sin Efectos Secundarios:** Las consultas son operaciones seguras e idempotentes. Leer un dato mil veces no cambia nada.
*   **Altamente Optimizado:** Puede servir miles de consultas por segundo porque utiliza modelos de datos **desnormalizados** (listos para mostrar).

---

## Matriz Diagnóstica: Comandos vs. Consultas

| Dimensión | Comandos (Escritura) | Consultas (Lectura) |
| :--- | :--- | :--- |
| **Propósito** | Alterar el estado del sistema | Recuperar información del sistema |
| **Idempotencia** | Generalmente **NO** (crea mutación) | **SÍ** (operación segura) |
| **Devuelve Datos** | **NO** (solo éxito/fallo) | **SÍ** (el [[DTO]] solicitado) |
| **Metáfora** | La Cocina (validación, preparación) | La Pantalla (rápido, solo lectura) |

---

## El Precio del Rendimiento: Consistencia Eventual

Al separar los modelos, existe una pequeña **ventana de tiempo** donde la **escritura** ya ocurrió, pero la **lectura** aún no se actualiza.

> **Diagrama detectado:** Cinta transportadora que traslada una hamburguesa desde una "Write DB" (Cocina) pasando por un icono de reloj con la etiqueta "Milisegundos de Inconsistencia" hacia una "Read DB" (Pantalla/UI Optimista).

---

## El Ciclo Completo: [[DTO]] y [[CQRS]] Trabajando Juntos

Empaquetamos nuestras intenciones en [[DTO]]s, procesamos los cambios con [[Commands]], y servimos los resultados a través de [[Queries]]

> **Diagrama detectado:** Diagrama de flujo circular donde un usuario envía un "1. Command DTO" hacia "La Cocina", la cual mediante un "2. Event Bus (Aktualización)" alimenta a "La Pantalla", permitiendo al usuario realizar una "3. Solicita Lectura" que retorna un "4. Query DTO".

---

## Separar para Escalar: Reglas de Oro

> **Diagrama detectado:** Iconos de caja de envío ([[DTO]]), flechas cruzadas ([[CQRS]]) y símbolo de advertencia con triángulo amarillo.

*   Usa **[[DTO]]s** para desacoplar tu presentación de tu base de datos y proteger tu lógica de negocio.
*   Usa **[[CQRS]]** cuando tus necesidades de lectura y escritura sean genuinamente distintas y requieran escalar por separado.
*   **Cuidado con la Sobreingeniería:** Si un simple [[CRUD]] con una tabla funciona perfectamente, no introduzcas [[CQRS]]. La complejidad de la solución siempre debe estar justificada por la complejidad del problema.