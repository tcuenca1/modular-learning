---
materia: [[Programacion Web]]
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [programacion_web, actividad, ingesta_ia]
---

# [[Programacion Web]] - Taller Práctico N°: 01

## 1. Datos Generales

* **Unidad N°1:** [[Desarrollo de aplicaciones Web bajo arquitecturas N-capas]]
* **Tema:** [[Arquitectura N-Capas]] aplicada a sistemas web
* **Fecha:** 09/09/2026
* **Objetivo:** Diseñar la estructura de una aplicación web mediante [[arquitectura multicapa]] aplicando [[separación de responsabilidades]].

---

## 2. Tipo de Actividad

* **Lugar:** No especificado
* **Alcance:** No especificado
* **Forma:** No especificado

---

## 3. Roles y Responsabilidades de los Participantes en la Tarea

| Nombre Estudiante | Rol | Descripción |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Investigador | Actividad |
| [ESTUDIANTE] | Investigador | Actividad |

---

## 4. Evidencias del Desarrollo

### Cliente en ejecución ([[Frontend]]): Interfaz inicial
* URL: `http://localhost:5173/`

> **Captura de pantalla detectada:** Muestra una ventana del navegador con una interfaz web oscura titulada "Cliente React" y un mensaje centrado que indica "Cargando...".
> 

---

### Petición al [[Backend]]: Respuesta del servicio al interactuar con la interfaz

> **Captura de pantalla detectada:** Muestra el navegador con la interfaz "Cliente React" que ahora refleja el texto "Hola desde el servidor con Docker". A la derecha, se despliega la consola de herramientas de desarrollo (DevTools) mostrando la pestaña *Network* (Red) con una petición HTTP GET exitosa al puerto `3000` con código de estado `304 Not Modified` o similar.
> 

---

### Comprobación de la [[API]]: Respuesta JSON del endpoint
* URL: `http://localhost:3000/api/hola`

> **Captura de pantalla detectada:** Muestra una interfaz de terminal o navegador con fondo negro que devuelve un objeto en formato JSON: `{"message": "Hola desde el servidor con Docker"}`.
> 

---

### Servidor en [[Docker]]

> **Captura de pantalla detectada:** Muestra el panel de control de [[Docker]] Desktop (o un gestor de contenedores similar) listando los contenedores activos. Se observa un contenedor en ejecución con el nombre `programacionweb`, uso de CPU del 2.65% y un tiempo de actividad de 2 horas.
>