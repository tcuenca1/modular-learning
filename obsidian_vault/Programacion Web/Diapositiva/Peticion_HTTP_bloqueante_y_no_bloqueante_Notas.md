---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [programacion_web, diapositiva, ingesta_ia]
---

# [[Programacion Web]] — El Viaje Oculto de un Clic

---

## Página 1

> **Diagrama detectado:** Ilustración conceptual abstracta con líneas de colores púrpura y azul conectadas a través de un círculo central.

# El Viaje Oculto de un Clic
Cómo sobreviven y se rastrean las aplicaciones modernas.

---

## Página 2

> **Diagrama detectado:** Comparación visual entre "El Monolito" (representado como un cubo oscuro, simple pero rígido) y "Microservicios" (una red compleja de cubos, pirámides y prismas interconectados por líneas de colores, caóticos pero escalables).

# La Evolución del Caos
Hoy, un solo clic desencadena una avalancha de peticiones invisibles a través de docenas de servicios.

- **El Monolito:** Simple pero rígido
- **[[Microservicios]]:** Escalables pero caóticos

---

## Página 3

# El Doble Reto de la Escala

1. **¿Cómo manejan los servidores miles de clics a la vez sin colapsar?**
   *(El modelo de Concurrencia)*
2. **¿Cómo evitamos que un clic se pierda en este laberinto?**
   *(El modelo de Rastreo)*

---

## Página 4

> **Diagrama detectado:** Patrón visual repetitivo que muestra a múltiples personas jugando partidas de ajedrez en mesas separadas de manera individual (un trabajador por tarea).

# Modelo Bloqueante: Un Trabajador por Task

> Imagina 100 jugadores de ajedrez jugando 1 partida cada uno.

- ✅ **Excelente para tareas pesadas** (cálculos complejos).
- ❌ **Pésimo para esperar.** Si el oponente tarda en jugar, el trabajador se queda bloqueado sin hacer nada.
- `</>` **Ejemplo clásico:** [[Java]] (`Thread-per-request`).

---

## Página 5

> **Diagrama detectado:** Ilustración de un Gran Maestro de ajedrez caminando en círculo atendiendo múltiples tableros simultáneamente (bucle de eventos).

# Bucle de Eventos: El Maestro de Ajedrez

> Imagina 1 Gran Maestro jugando 100 partidas simultáneas.

- ✅ **Increíblemente eficiente.** Mientras un oponente piensa (espera de red/datos), el Maestro avanza al siguiente tablero. Nunca se detiene.
- `</>` **Ejemplos clásicos:** [[NGINX]], [[Node.js]], [[Python]] ([[FastAPI]]).

---

## Página 6

> **Diagrama detectado:** Gráfico de rendimiento frente a latencia que muestra el punto de quiebre donde el modelo de Bucle de Eventos pierde eficiencia frente al modelo Bloqueante al aumentar el tamaño del mensaje.

# El Límite de Peso: El Estudio RSIS

> El Gran Maestro es rápido, pero falla si le das un tablero demasiado pesado.

- **Punto de quiebre:** Leer mensajes gigantes bloquea al Maestro. El modelo Bloqueante ([[Java]]) es 2.8 veces más rápido aquí.
- **El Bucle de Eventos gana.** Ideal para tareas rápidas y ligeras.

---

## Página 7

# La Tríada de la Observabilidad

- **Logs (El Diario)**
  - ¿Qué pasó? Registros de texto individuales.
  - *Ej.* `"Error de pago"`
- **Métricas (El Panel de Control)**
  - ¿Es normal? Números y tendencias.
  - *Ej.* `"Uso de CPU al 90%"`
- **Trazas (El GPS)**
  - ¿Dónde y por qué ocurrió? El viaje completo de una petición a través del sistema.

---

## Página 8

> **Diagrama detectado:** Línea de tiempo horizontal tipo diagrama de Gantt que muestra una traza principal dividida en Spans anidados (Autenticación, Inventario, Pago).

# Trazas y Spans: La Anatomía del Tiempo

Una [[Traza (Trace)]] es la historia completa. Un [[Span]] es un capítulo individual de esa historia (una operación específica). Al anidarlos, vemos exactamente dónde se pierde el tiempo.

---

## Página 9

> **Diagrama detectado:** Icono de lupa sobre dos paneles que representan los Atributos (contexto) y Eventos (hitos) dentro de un [[Span]].

# ¿Qué hay dentro de un Span?

- **Atributos (El Contexto):** Datos fijos de la operación.
  - *Ej.* `http.route = /checkout`
  - *Ej.* `usuario_id = 492`
- **Eventos (Los Hitos):** Diario de momentos específicos.
  - *Ej.* `T+15ms: Conectando a BD`
  - *Ej.* `T+150ms: Error de lectura`

---

## Página 10

> **Diagrama detectado:** Ilustración de una carrera de relevos (pass the baton), mostrando la transferencia de contexto entre diferentes actores/servicios.

# Propagación de Contexto: El Pase de Testigo

Sin propagación, cada servicio registra su trabajo de forma aislada. La propagación inyecta un testigo (cabeceras HTTP) en cada salto. Si un servicio deja caer el testigo, la traza se rompe y el rastro desaparece.

---

## Página 11

> **Diagrama detectado:** Esquema cilíndrico tipo tubo (representando el formato [[W3C Trace Context]]) dividida en dos componentes: el Trace ID (exterior) y el Parent ID (interior).

# El ADN del Testigo ([[W3C Trace Context]])

- **Trace ID:** Es el mismo para todos. Mantiene unido todo el viaje del usuario.
- **Parent ID:** Cambia en cada salto. Construye el árbol genealógico para saber exactamente quién llamó a quién.

---

## Página 12

> **Diagrama detectado:** Ilustración de un ecosistema complejo donde confluyen múltiples solicitudes hacia un sistema central analizado mediante observabilidad y trazabilidad.

# El Ecosistema Perfecto

> La escalabilidad sin visibilidad es un desastre esperando a ocurrir.

Utilizamos **Bucles de Eventos** para sobrevivir al tráfico masivo, y **Trazabilidad Distribuida** para iluminar el caos. Juntos, crean aplicaciones altamente escalables y completamente transparentes.

---

## Página 13

> **Diagrama detectado:** Logotipo abstracto corporativo con círculos concéntricos en tonos púrpuras y azules.

# Haciendo lo Invisible, Visible.

El código moderno es complejo, distribuido y asíncrono. Ya no podemos depurar mirando un solo servidor. Tenemos que rastrear el viaje completo.