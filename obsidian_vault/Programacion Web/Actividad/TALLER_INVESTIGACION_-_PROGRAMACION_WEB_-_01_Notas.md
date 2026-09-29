---
materia: Programacion Web
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [programacion_web, actividad, ingesta_ia]
---

[[Programacion Web]]

# TALLER INVESTIGACIÓN N°: 01

* **Fecha:** 25/09/2026
* **Unidad N°1:** Desarrollo de aplicaciones Web bajo arquitecturas N-capas
* **Tema:** Transferencia de datos entre capas mediante [[DTOs]] y mapeo
* **Objetivo:** Implementar mecanismos de intercambio de datos mediante el mapeo de objetos de dominio a formatos [[JSON]] y formatos binarios de [[serialización]] para asegurar la interoperabilidad y eficiencia en la comunicación entre sistemas.

---

## 1. MOTOR V8 DE [[Node.js]] Y SU MÓDULO v8

[[Node.js]] está construido sobre v8, el motor open source de Google para JavaScript y Web Assembly. [[Node.js]] expone un módulo nativo llamado `v8` que permite interactuar con funciones internas del motor.

* **Serialización (`v8.serialize(value)`):** Convierte cualquier objeto de JavaScript en una secuencia de bytes estructurados, operando a nivel binario internamente en el motor, lo cual lo hace una opción ideal para preservar los tipos de datos y estructuras.
* **Deserialización (`v8.deserialize(buffer)`):** Toma la secuencia binaria almacenada en un buffer y la reconstruye en memoria de forma exacta, devolviendo el objeto JavaScript original.

Un **buffer** representa una región de memoria reservada fuera del motor V8 de JavaScript. Esto permite convertir los datos binarios a otros formatos (como hexadecimal) o medir su tamaño en bytes de manera más fácil y eficiente.

---

## 2. PROCESO DE IMPLEMENTACIÓN DE SERIALIZACIÓN Y DESERIALIZACIÓN BINARIA

Se creó un adaptador de salida que recibe los datos de un usuario / dto.

> **Captura detectada:** Estructura de directorios del proyecto en el editor de código. Se muestra una arquitectura en capas (`ProgramacionWeb`), dentro de `src` se ubican las carpetas `aplicacion`, `dominio` y `infraestructura\adaptadores` (con subcarpetas `entrada` y `salida`). Dentro de `salida` figuran los archivos `AdapSalida_SerializacionBinaria.js` y `AdapSalida_UsuarioWeb.js`, además de archivos de configuración como `app.js`, `Dockerfile`, `package.json`, `docker-compose.yml`, entre otros.

Se usó el método `v8.serialize()` para convertir el objeto de JavaScript en un flujo de bytes estructurado dentro de un buffer binario.

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
};
```

Se usó el método `v8.deserialize()` para reconstruir el buffer binario de vuelta a un objeto de JavaScript funcional.

```javascript
const objetoRestaurado = v8.deserialize(bufferBinario);
```

Se expuso en un endpoint HTTP `http://localhost:3000/6A/usuario-binario` para verificar la respuesta en formato [[JSON]].

> **Captura detectada:** Navegador web mostrando la respuesta en formato [[JSON]] proveniente del endpoint `http://localhost:3000/6A/usuario-binario`. Se visualiza una estructura [[JSON]] con el mensaje "Serialización y Deserialización Binaria con v8 exitosa", conteniendo las propiedades `bufferBinario` (con su tipo `Buffer` y array de bytes numéricos), `bufferBinarioHex` (representación hexadecimal), `bytesTotales` y el objeto restaurado con sus respectivos atributos de usuario (nombre, contraseña, valor booleano, ciudad y teléfono).

---

## ROLES Y RESPONSABILIDADES DE LOS PARTICIPANTES EN LA TAREA:

| NOMBRE ESTUDIANTE | ROL | DESCRIPCIÓN |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |