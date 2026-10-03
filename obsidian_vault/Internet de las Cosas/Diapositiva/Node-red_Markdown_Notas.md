---
materia: Internet de las Cosas
tipo: diapositiva
fecha_procesamiento: 2026-10-03
tags: [internet_de_las_cosas, diapositiva, ingesta_ia]
---

[[Internet de las Cosas]]

---

## UTMACH

### First-Tier Header
Hello There, this is a paragraph that is split over multiple lines in the source, but displays as a single formatted paragraph.
To start a new paragraph, we separate it with a blank line from the previous paragraph.

### Second-Tier Header
* this is a bullet point list
* this is another item in the list

### Third-Tier Header
1. this is a numbered list
2. this is another item in the list

### Fourth-Tier Header
Link --> Grupo 1
Link --> Grupo 2

---

> **Captura de pantalla detectada (Página 1):** Muestra vistas de interfaz web de usuario con el título "Proyecto - Markdown 1", conteniendo un menú lateral con las opciones "Grupo 1" y "Grupo 2", además de tres vistas de navegador web mostrando el texto formateado (Página principal), un campo de texto etiquetado como "text" para el **Grupo 1** con un botón "Return Home", y una gráfica tipo tacómetro ([[Gauge]]) marcando 0 unidades para el **Grupo 2**.

---

> **Diagrama detectado (Página 2):** Muestra un flujo de nodos de Node-RED. 
> - Un bloque inicial con un nodo `Readme` y un nodo `markdown`.
> - Dos contenedores de grupos separados ("Grupo 1" y "Grupo 2") compuestos cada uno por: un nodo `timestamp`, un nodo `random`, un nodo `ui control` y un nodo de navegación "Return Home".
> Abajo se incluye la referencia de uso de Markdown, los enlaces a la documentación oficial y los iconos de Material Design.

---

## Configuración de Nodos ([[Node-RED]])

- **Nodo Markdown (Proyecto - Markdown 1):**
  - **Name:** Proyecto - Markdown 1
  - **UI:** Markdown 1 [/dashboard]
  - **Path:** `/page1`
  - **Icon:** `home`
  - **Theme:** Default Theme
  - **Layout:** Notebook

- **Nodo Grupo 1 (Edit text node):**
  - **Name:** Grupo 1
  - **UI:** Markdown 1 [/dashboard]
  - **Path:** `/page2`
  - **Icon:** `thermometer-lines`
  - **Theme:** Default Theme
  - **Layout:** Notebook

- **Nodo Grupo 2 (Edit gauge node):**
  - **Name:** Grupo 2
  - **UI:** Markdown 1 [/dashboard]
  - **Path:** `/page3`
  - **Icon:** `router-network-wireless`
  - **Theme:** Default Theme
  - **Layout:** Notebook