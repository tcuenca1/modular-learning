---
materia: [[Programacion Web]]
tipo: diapositiva
fecha_procesamiento: 2026-09-29
tags: [programacion_web, diapositiva, ingesta_ia]
---

# La Evolución hacia el Dominio: El paso estratégico de la arquitectura en capas a los modelos hexagonales

> **Diagrama detectado:** Portada de la presentación con el título "La Evolución hacia el Dominio", subtítulo sobre el paso estratégico de la arquitectura en capas a los modelos hexagonales, mostrando un esquema visual de la transición desde líneas paralelas de capas (Presentación, Aplicación, Infraestructura) hacia una estructura hexagonal con el [[Dominio]] en el centro rodeado por adaptadores, entradas, salidas y servicios externos.

---

## 1. La arquitectura define los componentes, la forma y las reglas de diseño

> **Diagrama detectado:** Comparación visual en cuatro cuadrantes entre "Diseño Civil" (con ilustraciones de ladrillos, cemento, planos y cimientos) y "Diseño Software" (con diagramas de componentes reutilizables, conectores de software, topologías y patrones). En la parte inferior central se destaca la fórmula de arquitectura de software: $\text{AS} = \{\text{Componentes} + \text{Forma} + \text{Lógica}\}$ (según Perry & Wolf, 1991), desglosada en:
> - **Componentes:** Clases y paquetes.
> - **Forma:** Cómo se conectan y organizan.
> - **Lógica:** Las decisiones que justifican el patrón elegido.

---

## 2. El paradigma tradicional estructuraba el software en capas lógicas apiladas

> **Diagrama detectado:** Esquema vertical en 3D de una arquitectura en capas tradicional con tres bloques principales en orden descendente:
> 1. **Capa de Presentación** (Interfaces web, Vistas).
> 2. **Capa de Negocio** (Lógica y modelos).
> 3. **Capa de Persistencia** (Base de datos, Acceso a datos).
> Flujo de dependencia indicado con flechas hacia abajo (top-down), acompañado de paneles laterales que explican:
> - **El Propósito Original:** Separar responsabilidades para resolver el caos de los primeros sistemas monolíticos.
> - **El Flujo Rígido:** La capa superior depende de la intermedia, y la intermedia depende directamente de la persistencia física (top-down).

---

## 3. El acoplamiento tecnológico contamina el conocimiento del negocio

> **Diagrama detectado:** Ilustración conceptual donde un rectángulo central etiquetado como **Capa de Negocio (Lógica y modelos)** aparece enredado y contaminado por múltiples cables, conectores y tecnologías externas como frameworks de [[UI]] (React, Vue, Angular, dispositivos móviles) arriba, y motores de bases de datos [[SQL]] abajo. Contiene tres llamadas de advertencia (Tags):
> - **Migraciones Riesgosas (Tag 1):** Cambiar un framework obliga a reescribir la lógica central.
> - **Pruebas Limitadas (Tag 2):** Los test exigen replicar infraestructuras complejas (BDs reales, servidores web).
> - **Conocimiento Diluido (Tag 3):** Las reglas funcionales se pierden en código de configuración y librerías.

---

## 4. [[Domain-Driven Design (DDD)]] aisla y protege el valor estratégico

> **Diagrama detectado:** Representación de un castillo amurallado denominado **The Domain** dentro de un **Contexto Delimitado (Bounded Context)**. El castillo protege el núcleo del negocio frente a múltiples peticiones y tecnologías externas (APIs, bases de datos SQL, servicios en la nube, interfaces de usuario) que se encuentran fuera de las murallas. Panel lateral con tres conceptos clave:
> - **El Foco Central:** La complejidad más significativa radica en las reglas de negocio, no en la tecnología.
> - **[[Lenguaje Ubicuo]]:** Expertos del negocio y programadores utilizan exactamente la misma terminología (reflejada en el código).
> - **[[Contextos Delimitados]]:** Fronteras estrictas donde un modelo evoluciona sin ser afectado por el exterior.

---

## 5. La regla de dependencia invierte el flujo de control hacia el centro

> **Diagrama detectado:** Diagrama de círculos concéntricos (Arquitectura Limpia / Clean Architecture) con flechas apuntando desde los círculos externos hacia el centro:
> - Anillo Exterior: `Web, UI, DB` / `Controllers, Presenters`
> - Anillo Intermedio: `Use Cases`
> - Núcleo Central: `Entities`
> Cuadro lateral resaltando **La Ley Inquebrantable:**
> *"Las dependencias del código fuente deben dirigirse sólo hacia adentro, hacia las políticas de nivel superior."*
> - **Aislamiento Total:** El círculo interno no conoce absolutamente nada del círculo externo. No hay referencias a bases de datos, frameworks, ni interfaces de usuario en el núcleo.

---

## 6. La [[Arquitectura Hexagonal]] establece fronteras mediante puertos y adaptadores

> **Diagrama detectado:** Esquema de una [[Arquitectura Hexagonal]] con un polígono de seis lados que encierra el **Modelo de Dominio** y los **Servicios de Aplicación**. En los bordes del hexágono se muestran **Puertos** (interfaces) y hacia el exterior se conectan **Adaptadores** que interactúan con la nube, bases de datos o interfaces web. Panel explicativo inferior:
> - **Puertos:** Interfaces que definen qué necesita el negocio (ej. "Guardar Contratación").
> - **Adaptadores:** Implementaciones tecnológicas intercambiables que definen cómo se hace (ej. "JPA").
> - **El Resultado:** La aplicación se maneja igual por un usuario, un test o un script.

---

## 7. Diagnóstico Estructural: Capas vs. Hexágonos

| Diagnóstico | [[Arquitectura en Capas]] | [[Arquitectura Hexagonal]] |
| :--- | :--- | :--- |
| **Flujo de Dependencias** | Top-down (Presentación -> Negocio -> Datos). | Invertido (Todo apunta al **Dominio** central). |
| **Testabilidad** | Compleja, requiere mocks pesados y bases de datos reales. | Aislada y unitaria por diseño mediante puertos. |
| **Conocimiento Funcional** | Diluido entre infraestructura (Modelos Anémicos). | Concentrado, expresivo y protegido (Agregados y Entidades). |
| **Flexibilidad Tecnológica** | Rígida; cambiar la base de datos afecta directamente al negocio. | 'Plug-and-Play'; los adaptadores se reemplazan sin tocar el núcleo. |

---

## 8. Caso de Estudio: Plataforma Digital de Empleo (Viedma)

> **Diagrama detectado:** Diagrama de bloques y relaciones (Bounded Contexts) que divide el sistema en subsistemas:
> - `<<Bounded Context>> Contratation` (incluyendo `Qualification` y `Contratatacion`).
> - `<<Bounded Context>> Profile` (incluyendo `CV`, `Company`, `Account`).
> - `<<Bounded Context>> Service` (incluyendo `ServiceCategory`, `Service`).
> Paneles descriptivos:
> - **El Contexto:** Unificar la oferta y demanda de oficios conectando ciudadanos, empresas y entidades.
> - **La Estrategia DDD:** Dividir el sistema masivo en subsistemas autónomos con lenguajes ubicuos definidos.
> - **El Caso de Uso Crítico:** Contratación de un servicio. El sistema debe orquestar estados (Pendiente, Aceptado, Rechazado) sin atarse a una tecnología de persistencia específica.

---

## 9. La Refactorización Visual: Inversión de Control en Acción

> **Diagrama detectado:** Comparativa antes y después de aplicar inversión de control.
> - **Estado Anterior (Lineal tradicional):** `Controlador` -> `Servicio` -> `DAO / Persistencia`
> - **Proceso central:** Símbolo circular grande de **Inversión de Control (IoC)**.
> - **Nuevo Estado (Hexagonal):** `Aplicación` -> `Dominio` (hexágono naranja central) <- `Infraestructura`
> Pie de página explicativo: *"El dominio deja de depender del código técnico. La lógica de negocio se aísla por completo, obligando a la base de datos y a la web a adaptarse a los contratos definidos por el Dominio."*

---

## 10. Anatomía de la Solución Hexagonal (Flujo de Contratación)

> **Diagrama detectado:** Diagrama de secuencia o componentes distribuidos en tres columnas arquitectónicas:
> 1. **Aplicación:** `ContratationController` (Adaptador de Entrada) dirigido por API RESTful, Spring MVC.
> 2. **Dominio (Núcleo Inmutable):** `ContratationService` -> `DomainContratationService` -> `ContratationRepository`. Reglas puras en Java, Raíz Agregada, cero dependencias externas.
> 3. **Infraestructura:** `ContratationRepositoryJPA` (Adaptador de Salida) dirigido por el dominio (Spring Data JPA, BD Relacional).

---

## 11. La implementación táctica: Contratos vs. Detalles

> **Diagrama detectado:** Esquema de código dividido en dos zonas conectadas por un conector/enchufe:
> - **El Puerto (Aislado en el Dominio):** Bloque naranja que muestra el contrato en código Java (`public interface ContratationRepository { void save(Contratation c); }`). Nota: *El negocio dicta QUÉ necesita para funcionar. No sabe de SQL ni de Hibernate.*
> - **El Adaptador (Relegado a la Infraestructura):** Bloque gris que muestra la implementación técnica (`public class ContratationRepositoryJPA implements ContratationRepository { ... jpaRepository.save(c); }`). Nota: *La tecnología se pliega a las reglas del negocio. Implementa el CÓMO.*

---

## 12. Síntesis Teórica: Principios Fundamentales Alcanzados

> **Diagrama detectado:** Tres iconos principales que representan los pilares logrados:
> 1. **Alta Cohesión:** Ilustrado con una red neuronal esférica interconectada. *"Agrupación con Propósito. Las reglas de negocio, como los cambios de estado, ahora residen exclusivamente en entidades ricas y servicios de dominio."*
> 2. **Bajo Acoplamiento:** Ilustrado con cadenas rompiéndose y un enchufe desconectado. *"Independencia Tecnológica. El núcleo no importa dependencias. Una migración de base de datos no requiere alterar ni una línea de la lógica central."*
> 3. **Inversión de Control:** Ilustrado con engranajes interconectados con flechas circulares. *"El Motor Arquitectónico. A través de la inyección de dependencias, la capa de datos ahora obedece a las abstracciones de la capa superior."*

---

## 13. El Dominio como Fortín Inmutable

> **Diagrama detectado:** Hexágono central naranja sólido rodeado de iconos tecnológicos periféricos (bases de datos, nubes, dispositivos móviles, interfaces web, engranajes).
> 
> > *La Lección Definitiva: El software moderno no organiza tecnologías, protege el conocimiento humano. Los frameworks caducan. Las bases de datos migran. Las interfaces de usuario evolucionan. El dominio del negocio permanece. La tecnología siempre será un detalle periférico, nunca el núcleo.*