---
materia: Programacion Web
tipo: diapositiva
fecha_procesamiento: 2026-09-30
tags: [programacion_web, diapositiva, ingesta_ia]
---

[[Programacion Web]]

# La Evolución hacia el Dominio
## El paso estratégico de la arquitectura en capas a los modelos hexagonales

> **Diagrama detectado:** Muestra la transición visual desde una estructura lineal de capas horizontales tradicionales (Presentación, Aplicación, Infraestructura) hacia una [[Arquitectura Hexagonal]] (o Ports and Adapters), donde el núcleo central es el **DOMINIO**, rodeado por adaptadores y puertos de entrada/salida conectados a servicios externos.

---

## 1. La arquitectura define los componentes, la forma y las reglas de diseño

> **Diagrama detectado:** Comparación entre el [[Diseño Civil]] y el [[Diseño Software]]. 
> - En Diseño Civil: Ladrillos/bloques de construcción, cemento, planos y cimientos.
> - En Diseño Software: Módulos/componentes reutilizables, conectores software, topología y patrones.
> 
> Se presenta la fórmula de [[Arquitectura de Software]] según Perry & Wolf (1991): 
> $\text{AS} = \{\text{Componentes} + \text{Forma} + \text{Lógica}\}$
> - **Componentes:** Clases y paquetes.
> - **Forma:** Cómo se conectan y organizan.
> - **Lógica:** Las decisiones que justifican el patrón elegido.

---

## 2. El paradigma tradicional estructuraba el software en capas lógicas apiladas

> **Diagrama detectado:** Un esquema vertical de capas apiladas:
> 1. **Capa de Presentación** (Interfaces web, Vistas)
> 2. **Capa de Negocio** (Lógica y modelos)
> 3. **Capa de Persistencia** (Base de datos, Acceso a datos)
> 
> **El Propósito Original:** Separar responsabilidades para resolver el caos de los primeros sistemas monolíticos.
> 
> **El Flujo Rígido:** La capa superior depende de la intermedia, y la intermedia depende directamente de la persistencia física (*top-down*).

---

## 3. El acoplamiento tecnológico contamina el conocimiento del negocio

> **Diagrama detectado:** Un bloque central titulado **Capa de Negocio (Lógica y modelos)** enredado con múltiples tecnologías externas (marcos de trabajo frontend, bases de datos [[SQL]], etc.). Contiene tres etiquetas de advertencia:
> - **Tag 1 (Migraciones Riesgosas):** Cambiar un [[Framework]] obliga a reescribir la lógica central.
> - **Tag 2 (Pruebas Limitadas):** Los *tests* exigen replicar infraestructuras complejas (BDs reales, servidores web).
> - **Tag 3 (Conocimiento Diluido):** Las reglas funcionales se pierden en código de configuración y librerías.

---

## 4. Domain-Driven Design (DDD) aisla y protege el valor estratégico

> **Diagrama detectado:** Una ilustración metafórica de una fortaleza medieval titulada **"The Domain"** rodeada por un foso y murallas de **Contexto Delimitado (Bounded Context)**, repeliendo agentes externos como APIs, bases de datos SQL y servicios en la nube.
> 
> - **El Foco Central:** La complejidad más significativa radica en las reglas de negocio, no en la tecnología.
> - **[[Lenguaje Ubicuo]]:** Expertos del negocio y programadores utilizan exactamente la misma terminología (reflejada en el código).
> - **[[Contextos Delimitados]]:** Fronteras estrictas donde un modelo evoluciona sin ser afectado por el exterior.

---

## 5. La regla de dependencia invierte el flujo de control hacia el centro

> **Diagrama detectado:** Un diagrama de círculos concéntricos que van desde el exterior hacia el núcleo:
> - Exterior: `Web, UI, DB`
> - Intermedios: `Controllers, Presenters`, `Use Cases`
> - Centro: `Entities`
> 
> **La Ley Inquebrantable:** Las dependencias del código fuente deben dirigirse sólo hacia adentro, hacia las políticas de nivel superior.
> 
> - **Aislamiento Total:** El círculo interno no conoce absolutamente nada del círculo externo. No hay referencias a bases de datos, frameworks, ni interfaces de usuario en el núcleo.

---

## 6. La Arquitectura Hexagonal establece fronteras mediante puertos y adaptadores

> **Diagrama detectado:** Un hexágono central con el **Modelo de Dominio** y **Servicios de Aplicación**, rodeado por **Puertos** (interfaces) y **Adaptadores** (implementaciones tecnológicas) que se conectan con servicios externos y bases de datos.
> 
> - **Puertos:** Interfaces que definen qué necesita el negocio (ej. *"Guardar Contratación"*).
> - **Adaptadores:** Implementaciones tecnológicas intercambiables que definen cómo se hace (ej. `JPA`).
> - **El Resultado:** La aplicación se maneja igual por un usuario, un test o un script.

---

## 7. Diagnóstico Estructural: Capas vs. Hexágonos

| Diagnóstico | Arquitectura en Capas | Arquitectura Hexagonal |
| :--- | :--- | :--- |
| **Flujo de Dependencias** | Top-down (Presentación $\to$ Negocio $\to$ Datos). | Invertido (Todo apunta hacia el Dominio central). |
| **Testabilidad** | Compleja, requiere *mocks* pesados y bases de datos reales. | Aislada y unitaria por diseño mediante puertos. |
| **Conocimiento Funcional** | Diluido entre infraestructura (Modelos Anémicos). | Concentrado, expresivo y protegido (Agregados y Entidades). |
| **Flexibilidad Tecnológica** | Rígida; cambiar la base de datos afecta directamente al negocio. | *'Plug-and-Play'*; los adaptadores se reemplazan sin tocar el núcleo. |

---

## 8. Caso de Estudio: Plataforma Digital de Empleo (Viedma)

> **Diagrama detectado:** Un diagrama con tres delimitaciones de [[Bounded Context]]: **Contratation** (incluye `Qualification`, `Contratation`), **Profile** (`CV`, `Company`, `Account`) y **Service** (`ServiceCategory`, `Service`).
> 
> - **El Contexto:** Unificar la oferta y demanda de oficios conectando ciudadanos, empresas y entidades.
> - **La Estrategia [[Domain-Driven Design (DDD)|DDD]]:** Dividir el sistema masivo en subsistemas autónomos con lenguajes ubicuos definidos.
> - **El Caso de Uso Crítico:** Contratación de un servicio. El sistema debe orquestar estados (Pendiente, Aceptado, Rechazado) sin atarse a una tecnología de persistencia específica.

---

## 9. La Refactorización Visual: Inversión de Control en Acción

> **Diagrama detectado:** Flujo comparativo antes y después de aplicar **[[Inversión de Control (IoC)|Inversión de Control (IoC)]]**:
> - **Estado Anterior:** $\text{Controlador} \to \text{Servicio} \to \text{DAO / Persistencia}$
> - **Nuevo Estado:** $\text{Aplicación} \to \text{Dominio} \leftarrow \text{Infraestructura}$
> 
> **El dominio deja de depender del código técnico.** La lógica de negocio se aísla por completo, obligando a la base de datos y a la web a adaptarse a los contratos definidos por el Dominio.

---

## 10. Anatomía de la Solución Hexagonal (Flujo de Contratación)

> **Diagrama detectado:** Esquema de flujo técnico dividido en tres secciones (**Aplicación**, **Dominio** (Núcleo Inmutable), e **Infraestructura**):
> - `ContratationController` (Adaptador de Entrada) $\to$ `ContratationService` $\to$ `DomainContratationService` $\to$ `ContratationRepository` (Puerto) $\leftarrow$ `ContratationRepositoryJPA` (Adaptador de Salida).

---

## 11. La implementación táctica: Contratos vs. Detalles

> **Diagrama detectado:** Ilustración de un enchufe conectando el **Puerto (Aislado en el Dominio)** con el **Adaptador (Relegado a la Infraestructura)** mediante código Java:
> - **Puerto:** `public interface ContratationRepository { void save(Contratation c); }` (El negocio dicta QUÉ necesita para funcionar).
> - **Adaptador:** `public class ContratationRepositoryJPA implements ContratationRepository { ... jpaRepository.save(c); }` (La tecnología se pliega a las reglas del negocio).

---

## 12. Síntesis Teórica: Principios Fundamentales Alcanzados

> **Diagrama detectado:** Tres iconos representativos:
> 1. **Alta Cohesión:** Red interconectada de nodos. Las reglas de negocio y cambios de estado residen exclusivamente en entidades ricas y servicios de dominio.
> 2. **Bajo Acoplamiento:** Cadenas rompiéndose junto a un enchufe. Independencia tecnológica; una migración de base de datos no requiere alterar la lógica central.
> 3. **Inversión de Control:** Engranajes girando. A través de la inyección de dependencias, la capa de datos obedece las abstracciones de la capa superior.

---

## 13. El Dominio como Fortín Inmutable

> **Diagrama detectado:** Un gran hexágono dorado central ("El Dominio") rodeado por diversos iconos tecnológicos periféricos (bases de datos, nubes, dispositivos móviles, interfaces web).
> 
> **La Lección Definitiva:** El software moderno no organiza tecnologías, protege el conocimiento humano. Los frameworks caducan. Las bases de datos migran. Las interfaces de usuario evolucionan. **El dominio del negocio permanece.** La tecnología siempre será un detalle periférico, nunca el núcleo.