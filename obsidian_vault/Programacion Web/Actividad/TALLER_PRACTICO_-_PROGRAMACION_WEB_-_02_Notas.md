---
materia: Programacion Web
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [programacion_web, actividad, ingesta_ia]
---

[[Programacion Web]]

# TALLER PRÁCTICO N°: 03

**FECHA:** 18/09/2026  
**UNIDAD N°1:** Desarrollo de aplicaciones Web bajo arquitecturas [[Arquitectura N-capas|N-capas]]  
**TEMA:** Modularidad, cohesión y desacoplamiento en soluciones multicapa  
**OBJETIVO:** Estructurar aplicaciones de software escalables mediante el modelado de reglas de negocio con diseño guiado por el dominio táctico ([[DDD]]) y la organización de componentes bajo [[Clean Architecture]].

---

## TIPO DE ACTIVIDAD

* **LUGAR:** [No seleccionado / Indefinido]
* **ALCANCE:** Individual
* **FORMA:** Taller

---

## ROLES Y RESPONSABILIDADES DE LOS PARTICIPANTES EN LA TAREA

| NOMBRE ESTUDIANTE | ROL | DESCRIPCIÓN |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |

---

## EVIDENCIAS DE PRUEBAS Y FUNCIONAMIENTO

Prueba de funcionamiento del endpoint `http://localhost:3000/6A/usuario`.

> **Captura de pantalla detectada:** Consola mostrando una solicitud HTTP a través de un navegador web hacia `http://localhost:3000/6A/usuario`, devolviendo en formato JSON la respuesta `{"message":false}`.
> ![Prueba de endpoint usuario](https://via.placeholder.com/600x200?text=Captura+de+Pantalla+Endpoint+Usuario)

Prueba de autenticación con el endpoint `http://localhost:3000/6A/usuario?usu=juan&cont=perez`. El usuario “juan” con contraseña “perez” existe.

> **Captura de pantalla detectada:** Consola mostrando una solicitud GET de autenticación con parámetros de usuario y contraseña exitosa (`usu=juan&cont=perez`), devolviendo la respuesta JSON `{"message":true}`.
> ![Prueba de autenticación exitosa](https://via.placeholder.com/600x200?text=Captura+de+Pantalla+Auth+Exitosa)

Prueba de autenticación con el endpoint `http://localhost:3000/6A/usuario?usu=juan&cont=perez1`. El usuario “juan” existe, pero no con contraseña “perez1”.

> **Captura de pantalla detectada:** Consola mostrando una solicitud GET de autenticación fallida debido a credenciales incorrectas (`usu=juan&cont=perez1`), devolviendo la respuesta JSON `{"message":false}`.
> ![Prueba de autenticación fallida](https://via.placeholder.com/600x200?text=Captura+de+Pantalla+Auth+Fallida)

---

## Estructura actual del proyecto

> **Captura de pantalla detectada:** Árbol de directorios de un proyecto [[Node.js]] estructurado bajo [[Clean Architecture]]:
> - `servidor/`
>   - `node_modules/`
>   - `src/`
>     - `aplicacion/`
>       - `caso_uso/` (`CasoUso_Mensaje.js`, `CasoUso_Usuario.js`)
>       - `puerto/`
>         - `entrada/` (`PuertoEntradaMensaje.js`, `PuertoEntradaUsuarioWeb.js`)
>         - `salida/` (`PuertoSalidaUsuarioWeb.js`)
>     - `dominio/` (`Mensaje.js`, `MensajeBuenosDias.js`, `Usuario.js`)
>     - `infraestructura/`
>       - `adaptadores/`
>         - `entrada/` (`AdaptEntrada_PeticionWeb.js`, `AdaptEntrada_UsuarioWeb.js`)
>         - `salida/` (`AdaptSalida_UsuarioWeb.js`)
>     - `app.js`
>   - `.gitignore`
>   - `Dockerfile`
>   - `package-lock.json`
>   - `package.json`
> ![Estructura del proyecto](https://via.placeholder.com/400x400?text=Estructura+Clean+Architecture+NodeJS)