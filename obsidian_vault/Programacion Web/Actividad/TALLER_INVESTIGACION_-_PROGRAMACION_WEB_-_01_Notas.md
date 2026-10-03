---
materia: Programacion Web
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [programacion_web, actividad, ingesta_ia]
---

[[Programacion Web]]

# TALLER INVESTIGACIÓN N°: 01
**Fecha:** 25/09/2026

* **Unidad N°1:** Desarrollo de aplicaciones Web bajo arquitecturas [[Arquitectura N-capas|N-capas]]
* **Tema:** Transferencia de datos entre capas mediante [[DTO]]s y mapeo
* **Objetivo:** Implementar mecanismos de intercambio de datos mediante el mapeo de objetos de dominio a formatos [[JSON]] y formatos binarios de [[Serialización]] para asegurar la interoperabilidad y eficiencia en la comunicación entre sistemas.

## TIPO DE ACTIVIDAD
* **Lugar:** Extraclase
* **Alcance:** Grupal
* **Forma:** Taller, Investigativa

---

## ROLES Y RESPONSABILIDADES DE LOS PARTICIPANTES EN LA TAREA:
| Nombre Estudiante | Rol | Descripción |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |

---

## MOTOR V8 DE NODE.JS Y SU MÓDULO v8

[[Node.js]] está construido sobre v8, el motor open source de Google para [[JavaScript]] y Web Assembly. [[Node.js]] expone un módulo nativo llamado `v8` que permite interactuar con funciones internas del motor.

* **[[Serialización]] (`v8.serialize(value)`):** Convierte cualquier objeto de [[JavaScript]] en una secuencia de bytes estructurados, operando a nivel binario internamente en el motor, lo cual lo hace una opción ideal para preservar los tipos de datos y estructuras.
* **[[Deserialización]] (`v8.deserialize(buffer)`):** Toma la secuencia binaria almacenada en un [[Buffer]] y la reconstruye en memoria de forma exacta, devolviendo el objeto [[JavaScript]] original.

Un [[Buffer]] representa una región de memoria reservada fuera del motor V8 de [[JavaScript]]. Esto permite convertir los datos binarios a otros formatos (como hexadecimal) o medir su tamaño en bytes de manera más fácil y eficiente.

---

## PROCESO DE IMPLEMENTACION DE SERIALIZACION Y DESERIALIZACION BINARIA

Se creó un adaptador de salida que recibe los datos de un usuario / [[DTO]].

> **Captura de código / Estructura de archivos detectada:** 
> Estructura de directorios del proyecto en el editor que muestra la jerarquía de carpetas bajo `src`:
> * `ProgramacionWeb`
>   * `cliente`
>   * `servidor`
>   * `node_modules`
>   * `src`
>     * `aplicacion`
>     * `dominio`
>     * `infraestructura \ adaptadores`
>       * `entrada`
>       * `salida`
>         * `AdapSalida_SerializacionBinaria.js`
>         * `AdapSalida_UsuarioWeb.js`
>     * `app.js`
>   * `.gitignore`
>   * `Dockerfile`
>   * `package-lock.json`
>   * `package.json`
>   * `docker-compose.yml`
>   * `ProgramacionWeb.code-workspace`

Se usó el método `v8.serialize()` para convertir el objeto de [[JavaScript]] en un flujo de bytes estructurado dentro de un buffer binario.

```javascript
serializarYDeserializar(dto) {
  const bufferBinario = v8.serialize({
    nombre: dto.getNombre(),
    contrasena: dto.getContrasena(),
    valido: dto.getValido(),
    ciudad: dto.getCiudad(),
    telefono: dto.getTelefono()
  });
```

Se simuló el almacenamiento o transporte convirtiendo el buffer a hexadecimal y midiendo su tamaño en bytes. También se registró su expresión binaria completa.

```javascript
  return {
    bufferBinario: bufferBinario,
    bufferBinarioHex: bufferBinario.toString('hex'),
    bytesTotales: bufferBinario.length,
    objetoRestaurado
  };
}
```

Se usó el método `v8.deserialize()` para reconstruir el buffer binario de vuelta a un objeto de [[JavaScript]] funcional.

```javascript
const objetoRestaurado = v8.deserialize(bufferBinario);
```

Se expuso en un endpoint [[HTTP]] `http://localhost:3000/6A/usuario-binario` para verificar la respuesta en formato [[JSON]].

> **Captura de pantalla detectada:** 
> Vista del navegador web mostrando la respuesta [[JSON]] devuelta por el endpoint HTTP. Se observa un objeto con las propiedades `"mensaje": "Serialización y Deserialización Binaria con V8 exitosa"`, la estructura del buffer binario (`"type": "Buffer"` con un arreglo numérico en `"data"`), la representación en hexadecimal (`"bufferBinarioHex"`), el tamaño total en bytes (`"bytesTotales"`) y el objeto restaurado con sus respectivas propiedades y valores.