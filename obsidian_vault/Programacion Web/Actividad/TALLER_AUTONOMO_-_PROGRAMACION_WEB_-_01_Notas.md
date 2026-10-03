---
materia: Programacion Web
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [programacion_web, actividad, ingesta_ia]
---

# [[Programacion Web]] - Taller Autónomo N°: 01

| Campo | Detalle |
| :--- | :--- |
| **TALLER AUTÓNOMO N°:** | 01 |
| **FECHA:** | 18/09/2026 |
| **UNIDAD N°:** | 01 - [[Desarrollo de aplicaciones Web bajo arquitecturas N-capas]] |
| **TEMA:** | Modularidad, cohesión y desacoplamiento en soluciones multicapa |
| **OBJETIVO:** | Estructurar aplicaciones de software escalables mediante el modelado de reglas de negocio con diseño guiado por el dominio táctico ([[DDD]]) y la organización de componentes bajo arquitectura limpia ([[Clean Architecture]]). |

---

## TIPO DE ACTIVIDAD

* **LUGAR:** Extraclase
* **ALCANCE:** Individual
* **FORMA:** Taller

---

## ROLES Y RESPONSABILIDADES DE LOS PARTICIPANTES EN LA TAREA

| NOMBRE ESTUDIANTE | ROL | DESCRIPCIÓN |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |

---

## Pruebas de Funcionamiento y Autenticación de Endpoints

> **Captura de pantalla detectada:** Muestra una ventana de navegador web mostrando la respuesta en formato JSON `{"message":false}` al acceder al endpoint `http://localhost:3000/6A/usuario`.

* **Prueba de funcionamiento del endpoint:** `http://localhost:3000/6A/usuario`

> **Captura de pantalla detectada:** Muestra el resultado de la solicitud GET en el navegador indicando éxito con `{"message":true}` tras autenticarse con el usuario "juan" y contraseña "perez".

* **Prueba de autenticación (Éxito):** `http://localhost:3000/6A/usuario?usu=juan&cont=perez`
  * *Descripción:* El usuario “juan” con contraseña “perez” existe.

> **Captura de pantalla detectada:** Muestra el resultado de la solicitud GET en el navegador indicando fallo con `{"message":false}` al enviar una contraseña incorrecta para el usuario "juan".

* **Prueba de autenticación (Fallo):** `http://localhost:3000/6A/usuario?usu=juan&cont=perez1`
  * *Descripción:* El usuario “juan” existe, pero no con contraseña “perez1”.

---

## Estructura Actual del Proyecto

> **Captura de pantalla detectada:** Árbol de directorios de un proyecto de [[Node.js]] estructurado bajo principios de [[Clean Architecture]]:
> * Carpeta `src/`
>   * `aplicacion/`
>     * `caso_uso/` (`CasoUso_Mensaje.js`, `CasoUso_Usuario.js`)
>     * `puerto/`
>       * `entrada/` (`PuertoEntradaMensaje.js`, `PuertoEntradaUsuarioWeb.js`)
>       * `salida/` (`PuertoSalidaUsuarioWeb.js`)
>   * `dominio/` (`Mensaje.js`, `MensajeBuenosDias.js`, `Usuario.js`)
>   * `infraestructura/`
>     * `adaptadores/`
>       * `entrada/` (`AdaptEntrada_PeticionWeb.js`, `AdaptEntrada_UsuarioWeb.js`)
>       * `salida/` (`AdaptSalida_UsuarioWeb.js`)
>   * Archivos raíz: `app.js`, `.gitignore`, `Dockerfile`, `package-lock.json`, `package.json`