---
materia: [[Programacion Web]]
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [programacion_web, actividad, ingesta_ia]
---

# TALLER PRÁCTICO N°: 03

- **Fecha:** 18/09/2026
- **Unidad N°1:** [[Desarrollo de aplicaciones Web bajo arquitecturas N-capas]]
- **Tema:** Modularidad, cohesión y desacoplamiento en soluciones multicapa
- **Objetivo:** Estructurar aplicaciones de [[software]] escalables mediante el modelado de reglas de negocio con diseño guiado por el dominio táctico ([[DDD]]) y la organización de componentes bajo arquitectura limpia ([[Clean Architecture]]).

## Tipo de Actividad

- **Lugar:** [Sin marcar]
- **Alcance:** Individual
- **Forma:** Taller / Práctica de clase / Resolución de problemas, ejercicios

## Roles y Responsabilidades

| Nombre Estudiante | Rol | Descripción |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |

---

## Desarrollo y Pruebas del Proyecto

Prueba de funcionamiento del endpoint `http://localhost:3000/6A/usuario`.

> **Captura detectada:** Interfaz de navegador web mostrando una prueba de endpoint en `http://localhost:3000/6A/usuario` que devuelve una respuesta en formato JSON con el mensaje `{"message":false}`.
> ![Prueba endpoint usuario](data:image/png;base64,...)

---

Prueba de autenticación con el endpoint `http://localhost:3000/6A/usuario?usu=juan&cont=perez`. El usuario “juan” con contraseña “perez” existe.

> **Captura detectada:** Interfaz de navegador web mostrando una solicitud al endpoint `http://localhost:3000/6A/usuario?usu=juan&cont=perez` devolviendo una respuesta JSON con el mensaje `{"message":true}`.

---

Prueba de autenticación con el endpoint `http://localhost:3000/6A/usuario?usu=juan&cont=perez1`. El usuario “juan” existe, pero no con contraseña “perez1”.

> **Captura detectada:** Interfaz de navegador web mostrando una solicitud al endpoint `http://localhost:3000/6A/usuario?usu=juan&cont=perez1` devolviendo una respuesta JSON con el mensaje `{"message":false}`.

---

## Estructura Actual del Proyecto

> **Captura detectada:** Vista del explorador de archivos de un proyecto [[Node.js]] estructurado bajo [[Clean Architecture]] dentro de la carpeta `src`:
> - `aplicacion/`
>   - `caso_uso/` (`CasoUso_Mensaje.js`, `CasoUso_Usuario.js`)
>   - `puerto/`
>     - `entrada/` (`PuertoEntradaMensaje.js`, `PuertoEntradaUsuarioWeb.js`)
>     - `salida/` (`PuertoSalidaUsuarioWeb.js`)
> - `dominio/` (`Mensaje.js`, `MensajeBuenosDias.js`, `Usuario.js`)
> - `infraestructura/`
>   - `adaptadores/`
>     - `entrada/` (`AdapEntrada_PeticionWeb.js`, `AdapEntrada_UsuarioWeb.js`)
>     - `salida/` (`AdapSalida_UsuarioWeb.js`)
> - `app.js`
> - `.gitignore`
> - `Dockerfile`
> - `package-lock.json`
> - `package.json`