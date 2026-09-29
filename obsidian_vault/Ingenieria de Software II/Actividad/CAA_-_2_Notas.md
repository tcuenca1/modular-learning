---
materia: Ingenieria de Software II
tipo: actividad
fecha_procesamiento: 2026-09-29
tags: [ingenieria_de_software_ii, actividad, ingesta_ia]
---

[[Ingenieria de Software II]]

# UNIVERSIDAD TÉCNICA DE MACHALA
## FACULTAD DE INGENIERÍA CIVIL
### CARRERA DE TECNOLOGÍAS DE LA INFORMACIÓN
**INGENIERÍA DE SOFTWARE II – 2026– E2**

---

* **ACTIVIDAD:** CAA - 2
* **FECHA:** 19/09/2026
* **SEMESTRE:** Sexto
* **PARALELO:** A
* **ASIGNATURA:** [[Ingenieria de Software II]]
* **UNIDAD I:** [[Calidad del Software]] y [[Técnicas de Revisión]]
* **TEMA:** Evaluación de la calidad del producto software

#### PROBLEMA:
Construcción de un perfil de calidad. Seleccionar una aplicación web o sistema y establecer requisitos y atributos de calidad evaluables. Definir criterios, escalas y evidencias; posteriormente realizar una valoración cualitativa y cuantitativa que permita determinar fortalezas y debilidades del producto.

**Debe entregar:**
Matriz requisito–atributo–criterio–evidencia, resultados de evaluación y perfil de calidad del producto software.

#### OBJETIVO:
Evaluar la calidad de un producto software mediante criterios cualitativos y cuantitativos sustentados en evidencias.

---

### TIPO DE ACTIVIDAD
* **LUGAR:** Extraclase
* **ALCANCE:** Grupal
* **FORMA:** Resolución de problemas, ejercicios

---

### ROLES Y RESPONSABILIDADES DE LOS PARTICIPANTES EN LA TAREA:
| NOMBRE ESTUDIANTE | ROL | DESCRIPCIÓN |
| :--- | :--- | :--- |
| [ESTUDIANTE 1] | Estudiantes | Realizadores de la actividad |
| [ESTUDIANTE 2] | Estudiantes | Realizadores de la actividad |
| [ESTUDIANTE 3] | Estudiantes | Realizadores de la actividad |
| [ESTUDIANTE 4] | Estudiantes | Realizadores de la actividad |

---

## Construcción de un perfil de calidad

**Producto software seleccionado:** YouTube

YouTube es una plataforma web de distribución y reproducción de contenido audiovisual. Para la presente evaluación se considerará su versión web.

Las funciones delimitadas para la evaluación están relacionadas con la búsqueda de contenido, reproducción de videos, navegación, interacción con contenidos y acceso mediante cuenta de usuario, enfocadas en los atributos de eficiencia, usabilidad, fiabilidad, seguridad y portabilidad. La valoración se realizará mediante requisitos verificables, criterios definidos y evidencias objetivas.

### Matriz requisito–atributo–criterio–evidencia:

| Requisito | Atributo | Criterio | Evidencia |
| :--- | :--- | :--- | :--- |
| Respuesta rápida | Eficiencia de desempeño | Rendimiento. Al menos el 95% de las operaciones responde en $\le 4\text{ s}$. | Captura de reporte de rendimiento de [[Lighthouse]] (Evidencia 1) marcando un First Contentful Paint (FCP) de 3.6 s. |
| Facilidad de uso | Usabilidad | Interactividad. Las tareas principales pueden realizarse sin asistencia. | Según el estudio de Balqis y Subiyakto [1], YouTube obtuvo una puntuación [[SUS]] (System Usability Scale) de 87.6, lo que demuestra empíricamente su usabilidad. |
| Disponibilidad del servicio | Fiabilidad | Disponibilidad. El servicio permanece disponible durante al menos el 99,9 % de los días hábiles. | Captura del portal de monitoreo independiente [[Downdetector]] (Evidencia 2) reportando 0 incidentes masivos en las últimas 24 horas. |
| Protección de la información | Seguridad | Seguridad. Las pruebas no permiten accesos no autorizados a la cuenta. | Captura del certificado [[TLS]]/[[SSL]] del navegador (Evidencia 3) emitido por [[Google Trust Services]], confirmando una conexión [[HTTPS]] cifrada y válida. |
| Funcionamiento en diferentes entornos | Portabilidad | Compatibilidad. Funciona correctamente en diferentes navegadores y dispositivos móviles. | Captura de verificación propia (Evidencia 4) demostrando el correcto renderizado de la interfaz y funcionamiento del reproductor desde un dispositivo móvil. |

*Fuente: Elaboración propia con base en [1], [2] y [3].*

---

> **Capturas y Evidencias Visuales:**
> * **Evidencia 1 (Lighthouse):** Captura de pantalla de la herramienta de auditoría web [[Lighthouse]] mostrando métricas de rendimiento, destacando en un círculo azul el valor de *First Contentful Paint (FCP)* de `3.6 s`.
> * **Evidencia 2 (Downdetector):** Captura del portal [[Downdetector]] para YouTube que muestra el mensaje oficial: *"Los reportes de los usuarios no muestran problemas actuales con YouTube"*, indicando el estado operativo normal de la plataforma.
> * **Evidencia 3 (Certificados):** Captura del visor de certificados de seguridad del navegador para el dominio `*.google.com`, detallando la validez del certificado digital y la entidad emisora.
> * **Evidencia 4 (Verificación propia):** Captura de la interfaz móvil de YouTube en modo oscuro, mostrando la barra de búsqueda inicial, el logotipo de la plataforma y la barra de navegación inferior adaptada a dispositivos móviles (*responsive*).

---

## Resultados de evaluación

### Escalas de valoración utilizadas
Para garantizar la objetividad de la evaluación, se establecieron las siguientes métricas:
* **Cuantitativas:** Escala de razón para tiempos de respuesta (segundos) y puntuación de usabilidad (score [[SUS]] de 0 a 100). Escala nominal para la verificación de certificados y estado de servidores (Activo/Inactivo).
* **Cualitativas:** Se determinaron las categorías de **Fortaleza** (el producto cumple o supera el criterio) y **Debilidad** (el producto incumple el criterio).

### Análisis de Atributos:
1. **Eficiencia de Desempeño:** La auditoría mediante [[Lighthouse]] registró un First Contentful Paint de 3.6 s. Al ser inferior al criterio máximo aceptable de $\le 4\text{ s}$ establecido en la planificación, el sistema aprueba la métrica, constituyendo una Fortaleza en la entrega inicial de contenido.
2. **Usabilidad:** El análisis basado en el instrumento [[SUS]] (System Usability Scale) validado en literatura académica [1] demuestra que la interfaz es intuitiva y permite a los usuarios completar el ciclo de reproducción y búsqueda sin asistencia. Esto se cataloga como una Fortaleza del sistema.
3. **Fiabilidad:** La evidencia del monitoreo externo ([[Downdetector]]) confirma que la plataforma mantiene el criterio de alta disponibilidad exigido ($\ge 99.9\%$), procesando la carga de usuarios concurrentes sin interrupciones masivas. Representa una Fortaleza arquitectónica.
4. **Seguridad:** La validación de los protocolos de transporte demuestra el uso continuo de certificados [[TLS]]/[[SSL]] vigentes emitidos por entidades certificadoras de primer nivel ([[Google Trust Services]]). El cumplimiento estricto del cifrado de datos en tránsito se evalúa como una Fortaleza.
5. **Portabilidad:** La plataforma demostró adaptabilidad (diseño *responsive*) y coexistencia en entornos móviles sin requerir la instalación de aplicaciones nativas, cumpliendo con el criterio de compatibilidad. Se define como una Fortaleza de distribución.

### Perfil de Calidad del Producto Software: YouTube (Versión Web)
La evaluación basada en los principios del estándar [[ISO/IEC 25010]] concluye que la versión web de YouTube posee un perfil de calidad caracterizado por una alta madurez técnica. El sistema demuestra fortalezas transversales en los cinco atributos evaluados (Eficiencia, Usabilidad, Fiabilidad, Seguridad y Portabilidad).

Su arquitectura de distribución de contenido garantiza una alta disponibilidad (Fiabilidad) y conexiones cifradas (Seguridad) para el usuario final. Asimismo, la interfaz logra un equilibrio óptimo entre interactividad (Usabilidad) y compatibilidad multiplataforma (Portabilidad). Desde el punto de vista cuantitativo, la Eficiencia de Desempeño cumple con los umbrales de aceptación (3.6 s de respuesta inicial), determinando que el software es altamente competente y no presenta debilidades críticas o bloqueantes en su capa de interacción con el cliente.

---

## REFERENCIAS BIBLIOGRÁFICAS

[1] J. Balqis and A. Subiyakto, “A Usability Test for YouTube Application Using System Usability Scale (SUS) Method,” *Jurnal Perangkat Lunak*, vol. 6, no. 2, pp. 264–274, 2024. Disponible en: `researchgate.net/publication/381850220_A_Usability_Test_for_YouTube_Application_Using_System_Usability_Scale_SUS_Method`

[2] P. Lew, L. Olsina, and L. Zhang, “Integrating Quality, Quality in Use, Actual Usability and User Experience,” *2010 6th Central and Eastern European Software Engineering Conference*, pp. 117–123, 2010. `https://www.researchgate.net/publication/251995097_Integrating_quality_quality_in_use_actual_usability_and_user_experience`

[3] S. Rafi, M. A. Akbar, and A. A. Khan, “Assessing Software Product Quality in DevOps: An ISO 25010:2023 Perspective,” *EASE Companion ’25*, pp. 10–16, 2025. `https://oulurepo.oulu.fi/bitstream/handle/10024/60473/nbnfioulu-202601221339.pdf`