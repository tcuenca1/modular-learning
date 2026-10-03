---
materia: [[Programacion Web]]
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [programacion_web, diapositiva, ingesta_ia]
---

# Arquitectura de Software: Entendiendo DTO y CQRS sin Complicaciones

Entendiendo sistemas complejos a través de analogías simples.

> **Diagrama detectado:** Comparación visual dividida en dos secciones. A la izquierda, un servidor informático grande que representa la [[Arquitectura de Software]]; a la derecha, una cocina organizada que representa un sistema estructurado. En el centro, una flecha con el texto "Traducción simple: DTO & CQRS en acción" conecta ambos mundos.

---

## El Gran Problema de las Aplicaciones que Crecen Demasiado

> **Diagrama detectado:** Un escritorio de oficina caótico con un empleado atendiendo el teléfono, cocinando en una olla pequeña sobre el escritorio, rodeado de pilas de documentos, teléfonos sonando y cajas. En la esquina superior izquierda se destaca el problema de "Exposición de Datos" (mover estructuras pesadas por la red) y en la esquina superior derecha el "Cuello de Botella (CRUD)" (usar la misma base de datos para leer y escribir al mismo tiempo).

A medida que una aplicación crece, enfrenta dos problemas críticos: transportar demasiados datos innecesarios a través de la red y sobrecargar el sistema al intentar realizar lecturas y escrituras en el mismo lugar de forma simultánea.

---

## Parte 1: Objetos de Transferencia de Datos ([[DTO]])

Resolviendo el problema de cómo transportamos la información de forma segura.

> **Diagrama detectado:** Ilustración de una caja gris cerrada con un candado y un lazo, simbolizando un [[DTO]] (Data Transfer Object).

---

## La Entidad de Negocio vs. El Paquete de Envío

| Entidad ([[El Chef]]) | DTO ([[El Repartidor]]) |
| :--- | :--- |
| > **Diagrama detectado:** Ilustración de un chef cocinando en una cocina profesional llena de ingredientes, libros de recetas, carnes y utensilios. | > **Diagrama detectado:** Ilustración de una bolsa de entrega con un ticket de pedido sobre un mostrador limpio, listo para transporte. |
| Contiene reglas de negocio, lógica compleja y secretos del sistema. Nunca debe salir de la cocina. | No tiene lógica, no sabe cocinar. Solo transporta el producto terminado del punto A al punto B. |

Una Entidad u objeto de negocio define un concepto central con comportamiento complejo. Un **[[DTO]]** (*Data Transfer Object*) se utiliza únicamente para aislar y transportar esos datos entre capas o procesos.

---

## Filtrando la Complejidad para el Cliente

> **Diagrama detectado:** Un embudo titulado "Capa del Adaptador DTO". En la parte superior ingresan múltiples servidores complejos; en la salida inferior, un paquete limpio se dirige hacia un dispositivo móvil mediante líneas de transferencia de datos.

* **Eficiencia de Red:** Agrupa los datos para reducir las costosas llamadas remotas entre el cliente y el servidor.
* **Desacoplamiento:** Aísla el modelo de dominio interno de la capa de presentación externa. Un cambio en la base de datos no rompe la aplicación móvil.

---

## Anatomía de un DTO: Cero Lógica, Cien Por Ciento Datos

> **Diagrama detectado:** Diagrama esquemático de un componente estructurado en capas. A la izquierda, marcas de verificación verdes para propiedades, getters y setters (con un cuadro verde de ejemplo "Nombre: Hamburguesa, Precio: $10"). A la derecha, iconos de prohibición en rojo para "Sin Cálculos", "Sin Métodos" y "Sin Lógica de Negocio".

Un DTO no calcula impuestos, no valida reglas comerciales y no guarda datos en la base de datos. 
**Su única responsabilidad es almacenar y entregar sus propios datos.**

---

## Parte 2: Segregación de Responsabilidades ([[CQRS]])

Resolviendo el cuello de botella dividiendo las lecturas de las escrituras.

> **Diagrama detectado:** Dos flechas curvas cruzadas, una de color naranja apuntando hacia arriba/izquierda y otra cian apuntando hacia abajo/derecha, representando la separación de flujos en [[CQRS]].

---

## El Colapso del Sistema CRUD Tradicional

> **Diagrama detectado:** Una base de datos cilíndrica central agrietada bajo presión. Por el lado izquierdo ingresan flechas naranjas pesadas ("Escrituras complejas y transaccionales"), mientras que por el lado derecho salen múltiples flechas azules masivas ("Millones de consultas por segundo").

En un sistema tradicional, intentar que una sola tabla cumpla con escrituras estrictas y lecturas masivas genera contención. Es como si el chef que cocina la comida fuera la única persona autorizada para dictar el menú a cada cliente.

---

## La Solución CQRS: Dividiendo el Restaurante en Dos

[[CQRS]] (*Command Query Responsibility Segregation*) parte de una idea simple: separar lógicamente (y a veces físicamente) el modelo que recibe escrituras del modelo que responde consultas.

> **Diagrama detectado:** Esquema dividido en dos mitades por una línea punteada. 
> * Izquierda (**Modelo de Escritura / Commands / La Cocina**): Chefs cocinando en fogones activos procesando comandas.
> * Derecha (**Modelo de Lectura / Queries / La Pantalla de Estado**): Una pantalla gigante de menú y estado (`Estado: ¡Listo!`) donde los clientes revisan la información cómodamente sentados en las mesas.

---

## Los Comandos (Commands): Modificando el Estado

> **Diagrama detectado:** Un chef junto a una parrilla consultando un libro de recetas, acompañado de un icono circular rojo con un símbolo de prohibición/acción y el texto "Do".

* **Intención:** Representa la intención de realizar una acción (ej. `CreateUserCommand`).
* **Reglas Estrictas:** Valida la lógica de negocio y asegura la integridad transaccional.
* **No devuelve datos:** Modifica el estado del dominio pero no responde con información (salvo confirmación de éxito/error).
* **No Idempotente:** Ejecutar el mismo comando dos veces puede crear dos pedidos distintos.

---

## Las Consultas (Queries): Recuperando la Información

> **Diagrama detectado:** A la izquierda, tres bloques conceptuales con iconos de lupa, candado y gráfico de rendimiento. A la derecha, una tablet digital flotante mostrando una lista de órdenes (ej. `Orden #4501: Completada`, `Orden #4502: En Proceso`) asegurada por un icono de un candado azul.

* **Intención:** Solicita datos al sistema sin alterar su estado (ej. `GetUsersQuery`).
* **Sin Efectos Secundarios:** Las consultas son operaciones seguras e idempotentes. Leer un dato mil veces no cambia nada.
* **Altamente Optimizado:** Puede servir miles de consultas por segundo porque utiliza modelos de datos **desnormalizados** (listos para mostrar).

---

## Matriz Diagnóstica: Comandos vs. Consultas

| Dimensión | Comandos (Escritura) | Consultas (Lectura) |
| :--- | :--- | :--- |
| **Propósito** | Alterar el estado del sistema | Recuperar información del sistema |
| **Idempotencia** | Generalmente **NO** (crea mutación) | **SÍ** (operación segura) |
| **Devuelve Datos** | **NO** (solo éxito/fallo) | **SÍ** (el DTO solicitado) |
| **Metáfora** | La Cocina (validación, preparación) | La Pantalla (rápido, solo lectura) |

---

## El Precio del Rendimiento: Consistencia Eventual

Al separar los modelos, existe una pequeña **ventana de tiempo** donde la **escritura** ya ocurrió, pero la **lectura** aún no se actualiza.

> **Diagrama detectado:** Una línea de producción tipo cinta transportadora. A la izquierda, una "Write DB" entrega una hamburguesa preparada. En el centro, un icono de reloj con ondas y una etiqueta de "Milisegundos de Inconsistencia". A la derecha, la hamburguesa llega a la "Read DB" reflejándose en una pantalla de ordenador y un teléfono móvil con "UI Optimista".

---

## El Ciclo Completo: DTO y CQRS Trabajando Juntos

Empaquetamos nuestras intenciones en DTOs, procesamos los cambios con Comandos, y servimos los resultados a través de Consultas.

> **Diagrama detectado:** Diagrama de flujo circular. 
> 1. Un usuario desde su dispositivo envía un `Command DTO` (paquete gris).
> 2. El paquete ingresa a **La Cocina**.
> 3. A través de un `Event Bus`, se actualiza la información hacia **La Pantalla** (línea punteada de solicitud de lectura).
> 4. El usuario recibe finalmente un `Query DTO` con la información solicitada.

---

## Separar para Escalar: Reglas de Oro

> **Diagrama detectado:** Tres iconos principales que acompañan las reglas: una caja de DTO, flechas de bifurcación CQRS y un triángulo de advertencia con un signo de exclamación.

* **Usa DTOs** para desacoplar tu presentación de tu base de datos y proteger tu lógica de negocio.
* **Usa CQRS** cuando tus necesidades de lectura y escritura sean genuinamente distintas y requieran escalar por separado.
* **Cuidado con la Sobreingeniería:** Si un simple CRUD con una tabla funciona perfectamente, no introduzcas CQRS. La complejidad de la solución siempre debe estar justificada por la complejidad del problema.