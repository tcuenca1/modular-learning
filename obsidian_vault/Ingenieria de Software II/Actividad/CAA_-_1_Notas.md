---
materia: Ingenieria de Software II
tipo: actividad
fecha_procesamiento: 2026-09-30
tags: [ingenieria_de_software_ii, actividad, ingesta_ia]
---

# [[Ingenieria de Software II]] - Análisis comparativo de modelos de calidad

**UNIVERSIDAD TÉCNICA DE MACHALA**  
**FACULTAD DE INGENIERÍA CIVIL**  
**CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN**  
**INGENIERÍA DE SOFTWARE II – 2026– E2**  

---

## 1. Datos de la Actividad

* **ACTIVIDAD:** C1  
* **FECHA:** 13/09/2026  
* **SEMESTRE:** Sexto  
* **PARALELO:** A  
* **ASIGNATURA:** [[Ingeniería de Software II]]  
* **UNIDAD I:** [[Calidad del Software]] y Técnicas de Revisión  
* **TEMA:** Fundamentos y modelos de [[calidad del software]]  

### Problema
Análisis comparativo de modelos de calidad. Seleccionar un producto software real y analizarlo desde las perspectivas de calidad. Comparar las dimensiones de Garvin, los factores de McCall y el modelo [[ISO/IEC 9126]], determinando qué aspectos de calidad permite evaluar cada enfoque y justificando cuál sería más apropiado para el producto seleccionado.

**Debe entregar:**
Matriz comparativa Garvin–McCall–[[ISO/IEC 9126]] aplicada al producto seleccionado + conclusión técnica argumentada.

### Objetivo
Analizar los fundamentos de la [[calidad del software]] mediante sus conceptos, perspectivas y relación con el proceso y [[producto software]].

---

## 2. Roles y Responsabilidades

| NOMBRE ESTUDIANTE | ROL | DESCRIPCIÓN |
| :--- | :--- | :--- |
| [ESTUDIANTE] | Estudiante | Realizador De La Actividad |
| [ESTUDIANTE] | Estudiante | Realizador De La Actividad |
| [ESTUDIANTE] | Estudiante | Realizador De La Actividad |
| [ESTUDIANTE] | Estudiante | Realizador De La Actividad |

---

## 3. Análisis comparativo de modelos de calidad

### Producto software seleccionado: Telegram
Para el análisis se seleccionó **Telegram**, una aplicación de mensajería que permite enviar mensajes, archivos y contenido multimedia, además de realizar llamadas, crear grupos y canales. Es un producto adecuado para analizar la [[calidad del software]] porque integra diferentes funciones y su funcionamiento depende tanto de la aplicación como de la conexión de red y del dispositivo utilizado.

### Matriz comparativa Garvin–McCall–ISO/IEC 9126 aplicada al producto seleccionado

| Aspecto de calidad | Garvin | McCall | ISO/IEC 9126 |
| :--- | :--- | :--- | :--- |
| **Rendimiento / eficiencia** | Evalúa el desempeño de Telegram en tareas como envío de mensajes, carga de archivos y llamadas. | Evalúa la cantidad de recursos de hardware (RAM, batería) y código necesarios para ejecutar la aplicación fluidamente. | Mide el comportamiento temporal (tiempos de respuesta en chats) y la utilización de recursos bajo demanda. |
| **Funciones** | Considera las funciones adicionales que ofrece Telegram, como grupos, canales, bots, etc. | Evalúa en qué medida la aplicación satisface sus especificaciones base de mensajería y transmisión de datos. | Mide la exactitud de las características de la app para resolver las necesidades comunicativas del usuario. |
| **Confiabilidad** | Considera la capacidad de Telegram para mantener un funcionamiento estable. | Mide la probabilidad de que la aplicación no presente fallos o cierres inesperados durante una sesión de usuario. | Evalúa la madurez del software, su tolerancia a fallos de red y su capacidad de recuperación ante caídas de conexión. |
| **Facilidad de uso** | Considera la presentación de la interfaz y la percepción del usuario. | Considera el esfuerzo necesario para que un usuario nuevo aprenda a navegar por los chats y configuraciones. | Mide la capacidad de aprendizaje, la operabilidad y qué tan atractiva visualmente es la interfaz. |
| **Mantenimiento** | Se relaciona con las acciones de corrección, actualización y mantenimiento del producto. | Mide el esfuerzo requerido para localizar errores y modificar el código para añadir características. | Evalúa la facilidad con la que el sistema puede ser analizado, modificado y probado tras cada actualización. |
| **Adaptación a diferentes entornos** | Puede relacionarse con la capacidad del producto para mantenerse vigente mediante actualizaciones. | Evalúa el esfuerzo para migrar y operar el sistema en distintos ecosistemas (Android, iOS, Windows, Web). | Mide la adaptabilidad, facilidad de instalación y coexistencia del software con otros sistemas operativos. |
| **Interoperabilidad** | No presenta una dimensión específica equivalente. | Mide el esfuerzo para vincular la aplicación con otros sistemas (uso de [[APIs]] para conectar bots externos). | Se evalúa dentro de la funcionalidad, midiendo la interacción con sistemas específicos. |
| **Cumplimiento** | Considera el cumplimiento de requisitos y especificaciones. | Evalúa el control de acceso y seguridad (ej. cifrado de extremo a extremo en chats secretos). | Mide la capacidad del sistema para proteger la información y evitar accesos no autorizados. |

> **Nota bibliográfica:** Elaboración propia con base en Garvin [1], McCall [2] e [[ISO/IEC 9126]] [3].

---

## 4. Conclusión técnica argumentada

Para evaluar un producto de software como Telegram, el modelo [[ISO/IEC 9126]] resulta ser el más apropiado, lo cual se justifica bajo tres criterios técnicos:

1. Las dimensiones de Garvin fueron originalmente diseñadas para la manufactura de hardware y la industria en general. Forzar sus conceptos (como la durabilidad y estética) al código fuente o a la arquitectura en la nube de Telegram puede generar ambigüedades, ya que no están diseñadas para el software en sí.
2. El modelo de McCall por otro lado representa una mejora al centrarse en el software, pero su estructura se orienta al punto de vista del desarrollador (características como operación, revisión y transición). Este modelo es útil para el equipo de ingeniería de Telegram, pero resulta ser limitante a la hora de evaluar la experiencia del usuario final.
3. Finalmente está el modelo [[ISO/IEC 9126]], que fue creado específicamente para la evaluación integral del software. Este modelo define características y subcaracterísticas que encajan con la arquitectura de aplicaciones modernas, como Telegram en este caso. Al evaluar la calidad interna, externa y en uso de un software, lo hace un modelo óptimo para la evaluación de la calidad en sistemas actuales.

---

## Referencias Bibliográficas

[1] D. A. Garvin, “Competing on the Eight Dimensions of Quality,” *Harvard Business Review*, vol. 65, no. 6, pp. 101–109, Nov.–Dec. 1987. Disponible en: [https://hbr.org/1987/11/competing-on-the-eight-dimensions-of-quality](https://hbr.org/1987/11/competing-on-the-eight-dimensions-of-quality)

[2] J. A. McCall, P. K. Richards, y G. F. Walters, “Modelo de calidad McCall,” *Evaluación Red Grupo 2*. [En línea]. Disponible: [http://sites.google.com/view/evaluacionredgrupo2/modelos-de-calidad-mccall](http://sites.google.com/view/evaluacionredgrupo2/modelos-de-calidad-mccall).

[3] ISO/IEC, “ISO/IEC 9126 — Software engineering — Product quality,” ISO, 2005. [En línea]. Disponible: [https://www.iso.org/standard/22749.html](https://www.iso.org/standard/22749.html).