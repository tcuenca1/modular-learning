---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [programacion_web, diapositiva, ingesta_ia]
---

[[Programacion Web]]

# El Viaje Oculto de un Clic
Cómo sobreviven y se rastrean las aplicaciones modernas.

> **Diagrama detectado:** Ilustración conceptual con una línea púrpura y azul que serpentea pasando por un círculo central blanco con un borde grueso púrpura, simbolizando el trayecto de una petición.

---

## La Evolución del Caos
Hoy, un solo clic desencadena una avalancha de peticiones invisibles a través de docenas de servicios.

- **El Monolito:** Simple pero rígido
- **Microservicios:** Escalables pero caóticos

> **Diagrama detectado:** Comparación visual entre una arquitectura monolítica (representada por un cubo negro gigante, sólido y cerrado por el que atraviesa una línea recta) y una arquitectura de microservicios (representada por múltiples cubos, pirámides y prismas hexagonales de colores conectados en una malla compleja).

---

## El Doble Reto de la Escala

1. **¿Cómo manejan los servidores miles de clics a la vez sin colapsar?**
   *(El modelo de [[Concurrencia]])*
2. **¿Cómo evitamos que un clic se pierda en este laberinto?**
   *(El modelo de [[Rastreo]])*

---

## Modelo Bloqueante: Un Trabajador por Tarea

> **Diagrama detectado:** Cuadrícula con múltiples tableros de ajedrez donde cada mesa está ocupada por dos jugadores sentados, ilustrando el modelo de un trabajador por tarea (ej. [[Java]] Thread-per-request).

*Imagina 100 jugadores de ajedrez jugando 1 partida cada uno.*

- **✓** Excelente para tareas pesadas (cálculos complejos).
- **✕** Pésimo para esperar. Si el oponente tarda en jugar, el trabajador se queda bloqueado sin hacer nada.
- **`</>`** Ejemplo clásico: [[Java]] (Thread-per-request).

---

## Bucle de Eventos: El Maestro de Ajedrez

> **Diagrama detectado:** Un maestro de ajedrez en el centro camina en bucle alrededor de múltiples tableros de ajedrez simultáneos (representando el patrón de asincronía y [[Node.js]] / [[NGINX]]).

*Imagina 1 Gran Maestro jugando 100 partidas simultáneas.*

- **✓** Increíblemente eficiente. Mientras un oponente piensa (espera de red/datos), el Maestro avanza al siguiente tablero. Nunca se detiene.
- **`</>`** Ejemplos clásicos: [[NGINX]], [[Node.js]], [[Python]] ([[FastAPI]]).

---

## El Límite de Peso: El Estudio RSIS

*El Gran Maestro es rápido, pero falla si le das un tablero demasiado pesado.*

- **Punto de quiebre:** Leer mensajes gigantes bloquea al Maestro. El modelo Bloqueante ([[Java]]) es 2.8 veces más rápido aquí.
- El **Bucle de Eventos** gana. Ideal para tareas rápidas y ligeras.

> **Gráfico detectado:** Gráfica cartesiana que contrasta el rendimiento/latencia frente al tamaño del mensaje. Muestra cómo el modelo de bucle de eventos (curva azul) decae a partir de los 120KB, cruzándose con el rendimiento constante del modelo bloqueante de [[Java]].

---

## La Tríada de la Observabilidad

- **Logs (El Diario)**
  - ¿Qué pasó? Registros de texto individuales.
  - Ej. `"Error de pago"`
- **Métricas (El Panel de Control)**
  - ¿Es normal? Números y tendencias.
  - Ej. `"Uso de CPU al 90%"`
- **Trazas (El GPS)**
  - ¿Dónde y por qué ocurrió? El viaje completo de una petición a través del sistema.

> **Diagrama detectado:** Tres tarjetas informativas que representan Logs (icono de documento), Métricas (icono de velocímetro) y Trazas (icono de mapa GPS con una ruta trazada).

---

## Trazas y Spans: La Anatomía del Tiempo

Una [[Traza]] es la historia completa. Un [[Span]] es un capítulo individual de esa historia (una operación específica). Al anidarlos, vemos exactamente dónde se pierde el tiempo.

> **Diagrama detectado:** Cronograma (timeline) de una traza denominada "Traza (Trace): La Compra Completa (200ms)", que contiene tres Spans anidados y secuenciales: Span A: Autenticación (50ms), Span B: Inventario (100ms) y Span C: Pago (50ms).

---

## ¿Qué hay dentro de un Span?

> **Diagrama detectado:** Esquema ilustrativo con una lupa que desglosa el contenido de un Span en dos componentes principales: Atributos y Eventos.

- **Atributos (El Contexto)**
  - Datos fijos de la operación.
  - Ej. `http.route = /checkout`
  - Ej. `usuario_id = 492`
- **Eventos (Los Hitos)**
  - Diario de momentos específicos.
  - Ej. `T+15ms: Conectando a BD`
  - Ej. `T+150ms: Error de lectura`

---

## Propagación de Contexto: El Pase de Testigo

Sin propagación, cada servicio registra su trabajo de forma aislada. La propagación inyecta un testigo (cabeceras [[HTTP]]) en cada salto. Si un servicio deja caer el testigo, la traza se rompe y el rastro desaparece.

> **Diagrama detectado:** Ilustración de una carrera de relevos (postes de conexión) donde atletas de colores pasan un testigo (bastón naranja) de un servicio a otro a lo largo de una línea de ruta discontinua.

---

## El ADN del Testigo ([[W3C Trace Context]])

> **Diagrama detectado:** Corte esquemático cilíndrico de un token o cabecera que ilustra cómo se compone internamente de un [[Trace ID]] (canal central continuo) y un [[Parent ID]] (segmentos encadenados que forman el árbol genealógico).

- **Trace ID**
  - Es el mismo para todos. Mantiene unido todo el viaje del usuario.
- **Parent ID**
  - Cambia en cada salto. Construye el árbol genealógico para saber exactamente quién llamó a quién.

---

## El Ecosistema Perfecto

*La escalabilidad sin visibilidad es un desastre esperando a ocurrir.*

> **Diagrama detectado:** Ilustración de un sistema complejo donde una figura central recibe múltiples peticiones externas de colores y las canaliza hacia un laberinto estructurado con flujos de trazas limpios y controlados al salir.

Utilizamos [[Bucle de Eventos|Bucles de Eventos]] para sobrevivir al tráfico masivo, y [[Trazabilidad Distribuida]] para iluminar el caos. Juntos, crean aplicaciones altamente escalables y completamente transparentes.

---

## Haciendo lo Invisible, Visible.

El código moderno es complejo, distribuido y asíncrono. Ya no podemos depurar mirando un solo servidor. Tenemos que rastrear el viaje completo.