---
materia: [[Programacion Web]]
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [programacion_web, diapositiva, ingesta_ia]
---

# Construcción y Depuración de Arquitecturas Multicapa
Guía de ingeniería para [[Node.js]]: Inversión de Control, Contenedores y Validación End-to-End.

> **Diagrama detectado:** Ilustración conceptual de una arquitectura multicapa en perspectiva isométrica. Muestra un flujo de peticiones (`[REQ-1624a]`) representado como una línea naranja que atraviesa una malla estructural tridimensional, pasando por un nodo central de procesamiento (`INTERFACE SOCKET`) hasta alcanzar un estado de éxito (`[TRACE: A1F9-B302]`).

---

## El Problema del Acoplamiento Fuerte

> **Diagrama detectado:** A la izquierda, una máquina compleja con engranajes rígidos y conexiones físicas directas etiquetada como `UsuarioMySQLAdaptador`. A la derecha, un fragmento de código que muestra `class UsuarioUseCase` instanciando directamente `new UsuarioMySQLAdaptador()`, marcado con una cruz roja, acompañado de un cuadro de texto explicativo que señala: *"El caso de uso conoce y fabrica la implementación concreta. Imposible de simular (mockear) para pruebas."*

```javascript
class UsuarioUseCase {
    constructor() {
        this.repo = new UsuarioMySQLAdaptador(); // ❌
    }
}
```

---

## Inyección de Dependencias: Desacoplamiento Estructural

| Dimensión | Sin DI (Acoplado) | Con DI (Desacoplado) |
| :--- | :--- | :--- |
| Instanciación (¿Quién lo crea?) | ❌ El propio objeto | ✅ Un agente externo |
| Testabilidad (¿Se puede simular?) | ❌ Muy difícil | ✅ Inyección de mocks |
| Flexibility (Cambiar de BD) | ❌ Requiere reescribir código | ✅ Cambio transparente mediante interfaces |

```javascript
constructor(repositorio) { // Inyección (Constructor)
    this.repository = repositorio;
}
```

---

## Inversión de Control (IoC): El Principio de Hollywood
*No nos llames, nosotros te llamamos.*

> **Diagrama detectado:** Comparativa entre "Sin IoC" y "Con IoC". A la izquierda, `UsuarioUseCase` sostiene un control remoto emitiendo señales hacia `Database` y `Logger`. A la derecha, un `Contenedor Maestro` externaliza y gestiona las conexiones hacia `Database`, `Logger`, `UsuarioEntradaPuerto` y `UsuarioUseCase`.

* **IoC** responde al *por qué* (transferir el control de la creación).
* **DI** responde al *cómo* (pasando dependencias por el constructor, setter o método).

---

## Ensamblaje Manual: El Contenedor de Dependencias

> **Diagrama detectado:** Línea de ensamblaje industrial dividida en tres estaciones: Estación 1: Infraestructura (`UsuarioMySQLAdaptador`), Estación 2: Aplicación (`UsuarioUsesCase`) y Estación 3: HTTP (`UsuarioControlador`), donde un brazo robótico ensambla los componentes guiados por el contenedor.

```javascript
function crearUsuarioModulo() {
    const repositorio = new UsuarioMySQLAdaptador();
    const useCase = new UsuarioUsesCase(repositorio);
    const controlador = new UsuarioControlador(useCase);
    return { controlador };
}
```

---

## El Ecosistema de Contenedores en [[Node.js]]

| Herramienta | Tipo | Característica / Ideal para |
| :--- | :--- | :--- |
| Manual | Sin dependencias | Control total, sin magia. Ideal para: Aprender y proyectos limpios (Enfoque actual). |
| [[tsylringe]] | Ligero | Basado en decoradores (`@injectable`). Ideal para: Proyectos [[TypeScript]]. |
| [[awilix]] | Completo | Resolución automática y control de ciclo de vida. Ideal para: Escala media/alta. |
| [[NestJS]] | Framework | IoC integrado (`@Module`, `@Inject`). Ideal para: Arquitecturas empresariales estandarizadas. |

---

## El Embudo de Dependencias Hexagonal

> **Diagrama detectado:** Diagrama concéntrico de [[Arquitectura Hexagonal]]. En el centro se encuentra el Dominio (`Usuario`), rodeado por la Aplicación (`UsuarioUsesCase`) y en la capa exterior [[Infraestructura]] / HTTP (`Router`, `Controlador`, `Adaptador`). Flechas bidireccionales etiquetadas como "Puertos" conectan las capas, indicando que el conocimiento fluye hacia adentro.

*Las capas internas no conocen las externas. La comunicación fluye hacia afuera únicamente a través de interfaces (puertos).*

---

## Operación y Validación: De la Teoría a la Realidad

> **Diagrama detectado:** A la izquierda, un sobre postal naranja con la etiqueta `POST /api/usuarios`. Al centro, una pregunta clave sobre la complejidad de depurar peticiones a través de cinco componentes distintos, y a la derecha una miniatura del embudo hexagonal de capas.

Una arquitectura multicapa desacoplada es robusta, pero compleja de rastrear. ¿Cómo depuramos un flujo que atraviesa cinco componentes distintos sin perder el rastro de la petición original?

---

## El Hilo Fantasma: Trazabilidad con `TraceMiddleware`

> **Diagrama detectado:** Flujo secuencial horizontal desde `Request` pasando por `TraceMiddleware` (que genera un token verde `[ID: 550e8400...]`), `Controlador`, `Use Case` y `Repositiorio`, con una línea punteada inferior que vincula la trazabilidad a lo largo de todo el ciclo.

```javascript
req.traceId = uuidv4();
res.setHeader('x-trace-id', req.traceId);
```
Genera un ID único por petición. Se registra al inicio y al final para calcular la duración en milisegundos.

---

## Depuración Sistemática por Capas

1. **Controlador**
   * *¿El DTO recibió los datos correctos?*
   * ➔ Inspeccionar `req.body` y el DTO.
2. **Use Case**
   * *¿Pasó la regla de negocio?*
   * ➔ Verificar la construcción del `Command`/`Query`.
3. **Repositorio**
   * *¿La base de datos respondió?*
   * ➔ Loguear la entidad resultante de persistencia.
4. **Response DTO**
   * *¿Se filtraron los datos sensibles?*
   * ➔ Comparar la entidad original vs. el DTO final.

---

## Control Centralizado: Middleware de Excepciones

> **Diagrama detectado:** Esquema donde las capas de `Dominio`, `Use Case` y `Repositorio` emiten excepciones (rayos naranjas) hacia un componente centralizado llamado `ExceptionMiddleware`.

```javascript
function ExceptionMiddleware(err, req, res, next) {
    ...
}
```
*(Exactly 4 parameters required by Express: Request object, Response object, Next function)*

Unifica el manejo de respuestas al cliente y garantiza que los errores contengan el `traceId` para su depuración en los logs.

---

## Tipología de Excepciones de Dominio

| Clase de Error | Status HTTP | Ejemplo Práctico |
| :--- | :--- | :--- |
| Clase Base: `ErrorNegocio` | `400 | ERROR_NEGOCIO` | Mensaje genérico de validación fallida. |
| Recurso Faltante: `ErrorNoEncontrado` | `404 | ERROR_NO_ENCONTRADO` | Búsqueda de ID fallida. |
| Conflicto de Estado: `ErrorDuplicado` | `409 | ERROR_DUPLICADO` | Email ya registrado en el sistema. |

```javascript
const existe = await this.repositorio.buscarPorEmail(dto.email);
if (existe) throw new ErrorDuplicado('email', dto.email); // ⬅️ Genera 409 Automático
```

---

## Validación de Flujo End-to-End: `POST /api/usuarios`

* ✅ **1. `TraceMiddleware`:** Header `x-trace-id` inyectado.
  * ✅ **2. `CrearUsuarioDTO`:** Body mapeado, `validar() = []`.
    * ✅ **3. `CrearUsuarioCommand`:** Objeto inmutable con `passwordHash`.
      * ✅ **4. `Repositorio.guardar()`:** Entidad persistida en BD con ID.
        * ✅ **5. `UsuarioResponseDTO`:** Contraseña omitida en respuesta JSON.
          * ✅ **6. Manejo de Errores:** 409 generado si el email se repite.

---

## Evidencia de Consola: Interacciones cURL

* `curl POST /usuarios (Ana Torres)` ➔ **Status 201 Created** | Response sin `passwordHash`
* `curl POST /usuarios (Email repetido)` ➔ **Status 409 Conflict** | Tipo: `ERROR_DUPLICADO`
* `curl POST /usuarios (Datos incompletos)` ➔ **Status 400 Bad Request** | Mensajes de error listados
* `curl GET /usuarios/9999` ➔ **Status 404 Not Found** | Tipo: `ERROR_NO_ENCONTRADO`

---

## La Anatomía Completa del Sistema

> **Diagrama detectado:** Esquema integral de la arquitectura en un contenedor (`UsuarioModulo.js`). Muestra la entrada de la petición `POST /api/usuarios` con el `x-trace-id` pasando por el `TraceMiddleware`, bifurcándose hacia `UsuarioController`, `Adaptadores de Entrada`, `Casos de Uso` (`CrearUsuarioUsecase`), `Dominio` (`Usuario`), y cerrando el ciclo con adaptadores de salida y un `ExceptionMiddleware` global en la base.

Inyección de dependencias para construir. Trazabilidad y middlewares para asegurar. Una arquitectura lista para producción.