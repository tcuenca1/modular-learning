---
materia: [[Programacion Web]]
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [programacion_web, actividad, ingesta_ia]
---

# [[Taller Practico N°: 01]]

## Información General

* **Unidad N°1:** Desarrollo de aplicaciones Web bajo [[Arquitectura N-capas]]
* **Tema:** [[Arquitectura N-Capas]] aplicada a sistemas web
* **Objetivo:** Diseñar la estructura de una aplicación web mediante [[arquitectura multicapa]] aplicando separación de responsabilidades.
* **Fecha:** 09/09/2026

---

## Roles y Responsabilidades de los Participantes en la Tarea

| Nombre Estudiante | Rol | Descripción |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |
| [ESTUDIANTE] | Investigador | Actividad |

---

## Evidencias y Pruebas del Sistema

### Cliente en ejecución ([[Frontend]])
* **Interfaz inicial en:** `http://localhost:5173/`

> **Captura de pantalla detectada:** Muestra una ventana del navegador con el título "Cliente React" y un indicador de carga "Cargando...".
> 
> ![Cliente React en ejecución](data:image/png;base64,...)

---

### Petición al [[Backend]]
* **Respuesta del servicio al interactuar con la interfaz.**

> **Captura de pantalla detectada:** Muestra la interfaz del "Cliente React" mostrando el mensaje "Hola desde el servidor con Docker" y las [[Developer Tools]] del navegador con la pestaña [[Network]] abierta, detallando una petición HTTP GET con código de estado `304 Not Modified` hacia la URL `http://localhost:3000/api/hola`.
> 
> ![Petición al backend y herramientas de red](data:image/png;base64,...)

---

### Comprobación de la [[API]]
* **Respuesta [[JSON]] del endpoint:** `http://localhost:3000/api/hola`

> **Captura de pantalla detectada:** Muestra una ventana de navegador o cliente [[REST]] mostrando un objeto [[JSON]] con el mensaje de respuesta: `{"message": "Hola desde el servidor con Docker"}`.
> 
> ![Respuesta JSON de la API](data:image/png;base64,...)

---

### Servidor en [[Docker]]

> **Captura de pantalla detectada:** Muestra el panel de administración de [[Docker]] (como [[Docker Desktop]] o una interfaz similar), donde se observa el uso global de contenedores (CPU usage y Memory usage) y una lista de contenedores que incluye uno llamado `programacionweb` activo y en ejecución.
> 
> ![Contenedor de Docker en ejecución](data:image/png;base64,...)