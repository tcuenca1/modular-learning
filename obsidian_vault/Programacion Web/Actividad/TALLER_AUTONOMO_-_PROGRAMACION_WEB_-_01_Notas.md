---
materia: [[Programacion Web]]
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [programacion_web, actividad, ingesta_ia]
---

# TALLER AUTÓNOMO N°: 01

**Fecha:** 18/09/2026  
**Unidad N°1:** [[Desarrollo de aplicaciones Web bajo arquitecturas N-capas]]  
**Tema:** Modularidad, cohesión y desacoplamiento en soluciones multicapa  

## Objetivo
Estructurar aplicaciones de software escalables mediante el modelado de reglas de negocio con [[diseño guiado por el dominio táctico (DDD)]] y la organización de componentes bajo [[Clean Architecture|arquitectura limpia (Clean Architecture)]].

---

## Tipo de Actividad

| Lugar | Alcance | Forma |
| :--- | :--- | :--- |
| ☐ Intraclase<br>☒ Extraclase | ☒ Individual<br>☐ Grupal | ☒ Taller<br>☐ Síntesis, esquemas<br>☐ Caso de estudio<br>☐ Investigativa |
| | | ☐ Práctica de laboratorio<br>☐ Práctica de clase<br>☐ Resolución de problemas, ejercicios<br>☐ Ensayo, artículo<br>☐ Informe e exposición |

**Calificación:** [Pendiente]

---

## Roles y Responsabilidades de los Participantes en la Tarea

| Nombre Estudiante | Rol | Descripción |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |

---

## Pruebas de Funcionamiento y Endpoints

### 1. Prueba de funcionamiento básico
* **Endpoint:** `http://localhost:3000/6A/usuario`

> **Captura de pantalla detectada:** Muestra una ventana de navegador web ejecutando el endpoint anterior sobre [[Node.js]] / [[Express]], con una respuesta en formato [[JSON]] que devuelve el objeto `{"message":false}`.

---

### 2. Prueba de autenticación exitosa
* **Endpoint:** `http://localhost:3000/6A/usuario?usu=juan&cont=perez`
* **Descripción:** El usuario “juan” con contraseña “perez” existe.

> **Captura de pantalla detectada:** Muestra la ejecución en el navegador del endpoint con parámetros de consulta de usuario y contraseña correctos, arrojando como respuesta [[JSON]] el valor `{"message":true}`.

---

### 3. Prueba de autenticación fallida (Contraseña incorrecta)
* **Endpoint:** `http://localhost:3000/6A/usuario?usu=juan&cont=perez1`
* **Descripción:** El usuario “juan” existe, pero no con la contraseña “perez1”.

> **Captura de pantalla detectada:** Muestra una solicitud HTTP con credenciales inválidas donde el servidor responde con la estructura [[JSON]] `{"message":false}`.

---

## Estructura Actual del Proyecto

> **Captura de pantalla detectada:** Muestra el árbol de directorios del proyecto en un entorno de desarrollo ([[IDE]] como [[Visual Studio Code]]):
> ```text
> 📁 servidor
>   📁 node_modules
>   📁 src
>     📁 aplicacion
>       📁 caso_uso
>         📄 CasoUso_Mensaje.js
>         📄 CasoUso_Usuario.js
>       📁 puerto
>         📁 entrada
>           📄 PuertoEntradaMensaje.js
>           📄 PuertoEntradaUsuarioWeb.js
>         📁 salida
>           📄 PuertoSalidaUsuarioWeb.js
>     📁 dominio
>       📄 Mensaje.js
>       📄 MensajeBuenosDias.js
>       📄 Usuario.js
>     📁 infraestructura
>       📁 adaptadores
>         📁 entrada
>           📄 AdapEntrada_PeticionWeb.js
>           📄 AdapEntrada_UsuarioWeb.js
>         📁 salida
>           📄 AdapSalida_UsuarioWeb.js
>     📄 app.js
>   📄 .gitignore
>   📄 Dockerfile
>   📄 package-lock.json
>   📄 package.json
> ```