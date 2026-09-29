---
materia: [[Programacion Web]]
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [programacion_web, diapositiva, ingesta_ia]
---

# Construcción y Depuración de Arquitecturas Multicapa
*Guía de ingeniería para [[Node.js]]: Inversión de Control, Contenedores y Validación End-to-End.*

> **Diagrama detectado:** Ilustración principal de la guía que muestra una estructura arquitectónica en capas de tipo rejilla técnica, donde un flujo de solicitudes (`Request Flow [REQ-1624a]`) viaja desde la izquierda a través de conexiones anaranjadas hacia un núcleo de procesamiento central de interfaz (`Interface Socket`) para resultar en un estado exitoso (`Success State [Trace: A1F9-B302]`).

---

## 1. El Problema del Acoplamiento Fuerte

> **Diagrama detectado:** Representación visual de un acoplamiento fuerte utilizando una máquina mecánica compleja con engranajes rígidos, cables y un brazo mecánico conectado directamente. Al lado se muestra el fragmento de código:
> ```js
> class UsuarioUsesCase {
>     constructor() {
>         this.repo = new UsuarioMySQLAdaptador(); // ❌
>     }
> }
> ```
> Un cuadro de texto explicativo señala: *"El caso de uso conoce y fabrica la implementación concreta. Imposible de simular (mockear) para pruebas."*

---

## 2. Inyección de Dependencias: Desacoplamiento Estructural

| Dimensión | Sin DI (Acoplado) | Con DI (Desacoplado) |
| :--- | :--- | :--- |
| Instanciación (¿Quién lo crea?) | ❌ El propio objeto | ✅ Un agente externo |
| Testabilidad (¿Se puede simular?) | ❌ Muy difícil | ✅ Inyección de mocks |
| Flexibility (Cambiar de BD) | ❌ Requiere reescribir código | ✅ Cambio transparente mediante interfaces |

> **Fragmento de código detectado:**
> ```js
> constructor(repositorio) {
>     this.repositorio = repositorio;
> }
> ```
> Una flecha verde indica que esto corresponde a la **Inyección (Constructor)**.

---

## 3. Inversión de Control (IoC): El Principio de Hollywood
*No nos llamas, nosotros te llamamos.*

> **Diagrama detectado:** 
> - **Sin IoC:** La clase `UsuarioUsesCase` maneja un control remoto mediante el cual dispara dependencias directas hacia `Database` y `Logger`.
> - **Con IoC:** Un componente superior llamado `Contenedor Maestro` gestiona y distribuye las dependencias hacia `Database`, `Logger` y `UsuarioEntradaPuerto / UsuarioUsesCase`.

**Diferencia conceptual clave:**
- **IoC** responde al *por qué* (transferir el control de la creación).
- **DI** responde al *cómo* (pasando dependencias por el constructor, setter o método).

---

## 4. Ensamblaje Manual: El Contenedor de Dependencias

> **Diagrama detectado:** Una cadena de montaje industrial con tres estaciones:
> - **Estación 3: HTTP** (`UsuarioControlador`)
> - **Estación 2: Aplicación** (`UsuarioUsesCase`) operada por un brazo robótico.
> - **Estación 1: Infraestructura** (`UsuarioMySQLAdaptador`) sobre una cinta transportadora.
> 
> Abajo se muestra la función de ensamblaje en código:
> ```js
> function crearUsuarioModulo() {
>     const repositorio = new UsuarioMySQLAdaptador();
>     const useCase = new UsuarioUsesCase(repositorio);
>     const controlador = new UsuarioControlador(useCase);
>     return { controlador };
> }
> ```

---

## 5. El Ecosistema de Contenedores en [[Node.js]]

| Herramienta | Tipo | Característica / Ideal para |
| :--- | :--- | :--- |
| **Manual** | Sin dependencias | Control total, sin magia. Ideal para: Aprender y proyectos limpios (Enfoque actual). |
| **[[tsyringe]]** | Ligero | Basado en decoradores (`@injectable`). Ideal para: Proyectos [[TypeScript]]. |
| **[[awilix]]** | Completo | Resolución automática y control de ciclo de vida. Ideal para: Escala media/alta. |
| **[[NestJS]]** | Framework | IoC integrado (`@Module`, `@Inject`). Ideal para: Arquitecturas empresariales estandarizadas. |

---

## 6. El Embudo de Dependencias Hexagonal

> **Diagrama detectado:** Esquema de arquitectura hexagonal/multicapa concéntrica donde el `Dominio (Usuario)` se encuentra en el núcleo, rodeado por la capa de `Aplicación (UsuarioUsesCase)` y finalmente la capa de `Infraestructura / HTTP (Router, Controlador, Adaptador)`. Las flechas de "Conocimiento" y "Puertos" indican que las capas internas no conocen las externas; la comunicación fluye hacia afuera únicamente a través de interfaces (puertos).

---

## 7. Operación y Validación: De la Teoría a la Realidad

> **Diagrama detectado:** A la izquierda, un sobre postal con una petición HTTP `POST /api/usuarios`. A la derecha, el esquema de capas de la arquitectura hexagonal.
> **Pregunta planteada:** *"Una arquitectura multicapa desacoplada es robusta, pero compleja de rastrear. ¿Cómo depuramos un flujo que atraviesa cinco componentes distintos sin perder el rastro de la petición original?"*

---

## 8. El Hilo Fantasma: Trazabilidad con `TraceMiddleware`

> **Diagrama detectado:** Diagrama de flujo horizontal donde una solicitud (`Request`) pasa por `TraceMiddleware` (generando un ID `[ID: 550e8400...]`), para luego continuar hacia el `Controlador`, `Use Case` y `Repositorio`. Una línea discontinua verde conecta todos los componentes con el middleware de seguimiento.
> 
> **Fragmento de código detectado:**
> ```js
> req.traceId = uuidv4();
> res.setHeader('x-trace-id', req.traceId);
> ```
> **Explicación:** Genera un ID único por petición. Se registra al inicio y al final para calcular la duración en milisegundos.

---

## 9. Depuración Sistemática por Capas

> **Diagrama detectado:** Línea de tiempo horizontal con pasos de inspección mediante lupas:
> 1. **Controlador:** *¿El DTO recibió los datos correctos?* $\rightarrow$ Inspeccionar `req.body` y el DTO.
> 2. **Use Case:** *¿Pasó la regla de negocio?* $\rightarrow$ Verificar la construcción del Command/Query.
> 3. **Repositorio:** *¿La base de datos respondió?* $\rightarrow$ Loguear la entidad resultante de persistencia.
> 4. **Response DTO:** *¿Se filtraron los datos sensibles?* $\rightarrow$ Comparar la entidad original vs. el DTO final.

---

## 10. Control Centralizado: Middleware de Excepciones

> **Diagrama detectado:** Múltiples flechas de error (rayos) saliendo desde `Dominio`, `Use Case` y `Repositorio` hacia un componente centralizado a la derecha llamado `ExceptionMiddleware`.
> 
> **Fragmento de código detectado:**
> ```js
> function ExceptionMiddleware(err, req, res, next) {
>     ...
> }
> ```
> *Nota: Exáctamente 4 parámetros requeridos por [[Express]]: Request object, Response object, Next function.*
> 
> **Propósito:** Unifica el manejo de respuestas al cliente y garantiza que los errores contengan el `traceId` para su depuración en los logs.

---

## 11. Tipología de Excepciones de Dominio

| Clase de Error | Status HTTP | Ejemplo Práctico |
| :--- | :--- | :--- |
| Clase Base: `ErrorNegocio` | `400 | ERROR_NEGOCIO` | Mensaje genérico de validación fallida. |
| Recurso Faltante: `ErrorNoEncontrado` | `404 | ERROR_NO_ENCONTRADO` | Búsqueda de ID fallida. |
| Conflicto de Estado: `ErrorDuplicado` | `409 | ERROR_DUPLICADO` | Email ya registrado en el sistema. |

> **Fragmento de código detectado:**
> ```js
> const existe = await this.repositorio.buscarPorEmail(dto.email);
> if (existe) throw new ErrorDuplicado('email', dto.email); // ⬅ Genera 409 Automático
> ```

---

## 12. Validación de Flujo End-to-End: `POST /api/usuarios`

> **Diagrama detectado:** Lista de verificación jerárquica con iconos de éxito:
> - ✅ **1. TraceMiddleware:** Header `x-trace-id` inyectado.
> - ✅ **2. CrearUsuarioDTO:** Body mapeado, `validar() = []`.
>   - ✅ **3. CrearUsuarioCommand:** Objeto inmutable con `passwordHash`.
>     - ✅ **4. Repositorio.guardar():** Entidad persistida en BD con ID.
>       - ✅ **5. UsuarioResponseDTO:** Contraseña omitida en respuesta JSON.
>         - ✅ **6. Manejo de Errores:** 409 generado si el email se repite.

---

## 13. Evidencia de Consola: Interacciones cURL

> **Diagrama detectado:** Cuatro bloques simulando terminales de comandos:
> - **Bloque 1:** `curl POST /usuarios (Ana Torres)` $\rightarrow$ `Status 201 Created | Response sin passwordHash`
> - **Bloque 2:** `curl POST /usuarios (Email repetido)` $\rightarrow$ `Status 409 Conflict | Tipo: ERROR_DUPLICADO`
> - **Bloque 3:** `curl POST /usuarios (Datos incompletos)` $\rightarrow$ `Status 400 Bad Request | Mensajes de error listados`
> - **Bloque 4:** `curl GET /usuarios/9999` $\rightarrow$ `Status 404 Not Found | Tipo: ERROR_NO_ENCONTRADO`

---

## 14. La Anatomía Completa del Sistema

> **Diagrama detectado:** Vista global del sistema encapsulada dentro de un contenedor (`Contenedor (UsuarioModulo.js)`). Muestra la entrada de una petición `POST /api/usuarios` con su respectivo `x-trace-id`, procesada por el `TraceMiddleware`, pasando por el `UsuarioControlador`, la capa de casos de uso (`CrearUsuarioUseCase`, `CrearUsuarioCommand`), el núcleo de `Dominio (Entidades & Servicios)` y saliendo a través de adaptadores de salida hacia el `ExceptionMiddleware` inferior.
> 
> *Inyección de dependencias para construir. Trazabilidad y middlewares para asegurar. Una arquitectura lista para producción.*