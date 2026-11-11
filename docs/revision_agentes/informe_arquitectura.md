# Informe de revisión arquitectónica — Modular Learning

Alcance: lectura de CLAUDE.md, docs/ARCHITECTURE.md, docs/DESPLIEGUE.md, backend/pyproject.toml, backend/src/modular_learning (core, infrastructure, apps, bootstrap) y estructura de frontend/src. No se leyó .env ni data/. Todas las rutas son relativas a la raíz del repo.

## 1. Veredicto global

La arquitectura es correcta en lo esencial y la hexagonal se cumple de verdad, no solo en el papel. La regla de dependencia está hecha cumplir por herramienta. `core` no importa infraestructura, `apps` ni `settings`. El composition root es único (`bootstrap.py`). La persistencia está tras un puerto limpio. La complejidad es en general proporcionada a un proyecto de un solo desarrollador, con dos excepciones: demasiadas abstracciones para un solo implementador, y un `PluginsService` que viola el propio espíritu hexagonal.

Los problemas reales no están en la estructura de capas. Están en tres sitios:
1. Una fuga de conocimiento específico del usuario dentro de `core/application/plugins.py`.
2. Dominio anémico: los casos de uso intercambian `dict[str, Any]`.
3. Dos componentes React de unas 1.200 líneas y ninguna garantía de concurrencia en la persistencia.

Nota global: el diseño es sólido, con deuda localizada y manejable.

## 2. Verificación con herramientas

- **Contratos import-linter** (comando indicado, 140 archivos, 529 dependencias): 3 mantenidos, 0 rotos.
  - "Core es agnóstico" (`pyproject.toml`, secciones `tool.importlinter.contracts`).
  - "El dominio no depende de los casos de uso".
  - "Infraestructura solo depende de los puertos del core".
- **Fugas en core** (grep): no hay `open(`, `print(`, `settings`, `HTTPException`, `fastapi` ni `infrastructure` en `core/`. Sí hay `import os` en `core/application/ingesta.py:7`, `plugins.py:5` y `silabo.py:5`. Se usa solo como manipulación de rutas (`os.path.join/splitext/basename/relpath/sep`), sin tocar disco. El contrato no lo prohíbe y el CLAUDE.md dice que `core` no hace I/O, así que técnicamente no hay violación. Pero `os.sep` y `os.path` acoplan la lógica a la semántica de rutas del SO anfitrión.
- **Acoplamiento apps/api <-> apps/cli**: nulo (grep cruzado vacío).
- **Instancias globales**: los únicos globales de módulo son `router = APIRouter(...)` y `console = Console()` (legítimos). Hay un global real en `bootstrap.py:89` (`_global_container`), con `get_container()` en `:238`, usado como fallback por `apps/api/dependencies.py:get_container`. Es un singleton de composition root, tolerable, pero contradice la regla "nada de instancias globales" si se lee literalmente.
- **`settings`**: solo lo importan `bootstrap.py`, `infrastructure/documents/lector_documentos.py` e `infrastructure/persistence/almacen.py`. Coincide con lo declarado en CLAUDE.md.
- **Ciclos**: import-linter analizó el grafo sin reportar ciclos. No hay contrato específico de "layers" ni de aciclicidad; esto es una garantía implícita, no explícita.
- **Tests**: 145 funciones `test_` (87 unit, 58 integration) más 4 archivos de test en frontend (`frontend/src/lib/*.test.ts`). Hay un único archivo de test de API (`tests/integration/api/test_api.py`).

## 3. Tabla de conformidad por principio

| Principio | Estado | Evidencia |
|---|---|---|
| Hexagonal: puertos como contratos del core | Cumple | 16 ABC en `core/ports/*.py`, 18 adaptadores en `infrastructure/` |
| Hexagonal: adaptadores primarios sin lógica | Cumple en gran parte | Routers 100-175 líneas, CLI 629 líneas totales. Los routers solo traducen `ValueError` a 400 y `None`/`False` a 404 (`apps/api/routers/materias.py:51,61,88,124,126,137`) |
| Hexagonal: composition root único | Cumple | `bootstrap.py:92 build_container`, DI vía `Depends(get_*_service)` en `apps/api/dependencies.py` |
| Hexagonal: puerto nombrado | Ambiguo | `LLMPort = LLMAdapterBase` (`core/ports/llm.py:32`). Alias para tapar un nombre mal elegido. ARCHITECTURE.md dice "Protocols / ABC" y todo son ABC |
| Clean Arch: regla de dependencia | Cumple | Contratos kept. `domain` -> nada; `application` -> `domain`/`ports`; `infrastructure` -> `ports`/`domain` |
| Clean Arch: entidades/casos de uso nítidos | Parcial | Entidades existen (`Materia`, `Proyecto`, `Tarjeta`, `GuiaOffline`) pero cronograma, clases, registro de materiales, quiz y alineación circulan como `dict` |
| S (responsabilidad única) | Parcial | `MateriasService` (174 líneas, 16 métodos) mezcla catálogo, cronograma, clases, parciales y cascada de borrado. `PluginsService` (284 líneas) mezcla configuración, memoria y descubrimiento de carpetas |
| O (abierto/cerrado) | Violado | `PluginsService` ramifica por nombre de plugin (`"node-red"`, `"cisco"`, `"web"`) con `hasattr(plugin, "analizar_carpeta")` en `core/application/plugins.py:~193-280`. Añadir un plugin exige editar el servicio |
| L (Liskov) | Violado puntual | `PluginPracticoBase` define 4 métodos, pero el servicio hace `hasattr` para `analizar_carpeta/analizar_flujo/analizar_proyecto`: el contrato no refleja lo que los clientes necesitan |
| I (segregación de interfaces) | Parcial | `CronogramaRepo` (`ports/repositorios.py:11-79`) es un puerto gordo. `AjustesPort` mezcla estado de configuración con rutas y validación de disco |
| D (inversión de dependencias) | Cumple | Servicios reciben ABC por constructor. Violación menor: `MateriasService.__init__` tiene `proyectos_service: Any` (`core/application/materias.py:~29`) más `Optional` en repos, con ramas `if self.registro_repo:`. Dependencia entre servicios sin tipar y dependencias opcionales |
| DDD ligero: lenguaje ubicuo | Cumple | Vocabulario consistente en español (materia, cronograma, clase, tutoría, repaso, guía offline) |
| DDD ligero: modelo rico | No cumple | `core/domain/` son funciones y dataclasses. Los invariantes de `Cronograma`/`Clase` viven en repo y servicios (`json_repositorios.py:172 guardar_cronograma` = ~145 líneas de reglas de normalización en el adaptador) |
| DDD ligero: agregados/límites | Ambiguo | `Materia` es en la práctica la raíz de agregado (cronograma, registro, proyectos) pero la cascada de borrado se hace a mano en `MateriasService.eliminar_materia` |
| Testabilidad | Cumple | Fakes en memoria (`tests/unit/application/fake_adapters.py`, 536 líneas), un fake por puerto. Pirámide razonable (unit 60%, integración 40%) |
| Aislamiento del despliegue | Cumple | `AlmacenDocumentos` (ABC) + `AlmacenArchivos` / `AlmacenPostgres` seleccionados por `DATABASE_URL`; `DocumentoJson` encapsula serialización |

## 4. Hallazgos detallados

### 4.1 Lo que se cumple (con evidencia)
- Regla de dependencia verificada por herramienta, no por revisión (3/3 contratos). Es el activo arquitectónico más valioso.
- `core/application` no contiene `fastapi`, `HTTPException`, `print`, `open` ni `settings`. Los errores de negocio son excepciones estándar (`ValueError`) que los routers traducen. Es correcto, aunque pobre (ver 4.2).
- `bootstrap.py` es el único lugar que conoce adaptadores concretos (líneas 32-53 importan `infrastructure.*`). Los routers obtienen servicios por `Depends`.
- La persistencia está aislada: los repos `Json*` no abren archivos, usan `DocumentoJson` -> `AlmacenDocumentos`. Cambiar a Postgres no tocó ni servicios ni repos. Esto está bien resuelto para el tamaño del sistema.
- Prompts como recursos (`core/prompts/*.md`) cargados vía puerto; ningún prompt hardcodeado en infraestructura de Gemini.
- Proveedor LLM aislado: `grep -rn "genai\|google" core apps` no devuelve nada. Gemini solo aparece en `infrastructure/llm/gemini_adapter.py` y en un docstring genérico.

### 4.2 Lo que se viola o es ambiguo
1. **Conocimiento del usuario hardcodeado en el núcleo** (`core/application/plugins.py`): literales `"Internet de las Cosas"`, `"Tecnologias de Conmutacion I"`, `"Programacion Web"`, y nombres de plugin `node-red`, `cisco`, `web`. Es la violación más seria: el núcleo "agnóstico" contiene los nombres de las asignaturas del estudiante y una cascada if/elif de tres plugins. Además genera Markdown de presentación (`### [Cisco] ...`) dentro de un servicio de aplicación.
2. **Dominio anémico / "dict-ly typed"**: `core/domain/alineador_curricular.py` (`asignar_material_a_clase`, `_construir_prompt`) opera sobre `list[dict[str, Any]]`; los servicios devuelven `dict[str, Any]` (`ingesta.py:136,165,194,217,236,264`; `evaluacion.py:92,159`; `guias.py:159,214`). Los routers acaban recibiendo diccionarios y reglas implícitas de claves. No hay tipos para `Clase`, `Cronograma`, `Parcial`, `PreguntaQuiz`, `Material`. Consecuencia: el contrato real está en el JSON en disco y en `frontend/src/api/types.ts` (473 líneas), no en el dominio.
3. **Lógica de dominio en el adaptador**: `JsonCronogramaRepo.guardar_cronograma` (`json_repositorios.py:172-316`, ~145 líneas) normaliza clases, asigna IDs, fusiona estado. `json_repositorios.py` (480 líneas) es el archivo más grande del backend porque hace trabajo del dominio. Un repositorio debería persistir, no decidir.
4. **`MateriasService`** (16 métodos) es un servicio dios de bajo nivel: catálogo + clases + cronograma + parciales + cascada. Tiene acoplamiento de servicio a servicio vía `proyectos_service: Any` con rama de reserva a `proyectos_repo`: dos caminos para lo mismo (`materias.py:eliminar_materia`).
5. **Plugins**: `PluginPracticoBase` no describe las operaciones que el servicio invoca (`analizar_carpeta`, etc.). El `hasattr` es un olor de contrato roto. Además, `ProyectosService` y `PluginsService` solapan en "contexto práctico de la asignatura".
6. **Alias y nomenclatura**: `LLMPort = LLMAdapterBase` y `LLM_GeminiAdapter` (snake-case en clase). Puerto con nombre de "adaptador base" confunde la semántica hexagonal.
7. **Contrato de estado oculto**: `ConfiguracionService`/`JsonAjustesRepo` leen `os.getenv` y mutan configuración de módulo (el ARCHITECTURE.md habla de "actualización en memoria de settings"); estado global implícito dentro de un adaptador.
8. **Manejo de errores**: todo es `ValueError`/`None`/`False`. Los routers traducen por convención (400/404), y el 404 se distingue de 400 por el tipo de retorno, no por una jerarquía de excepciones de dominio (`NoEncontrado`, `Invalido`). Frágil si un mensaje cambia (`materias.py:124` hace `HTTPException(404, detail=str(e))` desde una excepción).
9. **Funciones largas fuera de dominio**: `PluginsService` método de sincronización (~90 líneas con anidamiento 5), `JsonCronogramaRepo.guardar_cronograma` (~145), `IngestaService` (407 líneas, 8 métodos públicos, mezcla clasificación por ruta, conversión, alineación, escritura de nota y limpieza).

### 4.3 Frontend
- Estructura: `api/` (client + types), `views/`, `components/ui` (kit pequeño), `lib/` (lógica pura con tests: `asignaturas`, `guias`, `parciales`, `theme`), `hooks/useEventStream.ts`. La separación vistas / lib / api es correcta y `lib/` es el sitio sano.
- **Componentes gigantes**: `MaterialView.tsx` 1.279 líneas (un solo componente exportado desde la línea 120, ~1.160 líneas, 27 `useState`/`useEffect`) y `SilabosView.tsx` 1.226 líneas (un componente desde la línea 38, 31 hooks). Más `TutoriaView` 697, `GuiaView` 612, `QuizView` 559. Cuatro vistas superan las 550 líneas. Mezclan fetching, estado de formulario, lógica de presentación y "zona peligrosa".
- **Estado**: solo `useState/useEffect` locales, sin librería de caché de servidor (no hay react-query/zustand/redux en `package.json`). Cada vista re-implementa carga/error/refresh; hay duplicación previsible (formateadores de fecha y parcial dentro de `MaterialView.tsx:57-104` que ya existen conceptualmente en `lib/parciales.ts`).
- `MaterialView` sirve dos modos (`materiales` y `proyectos`) con un solo componente: acoplamiento por reutilización excesiva.
- Cobertura de tests de frontend: 4 archivos sobre `lib/` y 0 sobre vistas/hooks (incluido `useEventStream.ts`, 230 líneas de lógica asíncrona de SSE).
- Tipos duplicados a mano entre backend (dicts) y `types.ts`; no hay generación desde OpenAPI. Los `dict[str, Any]` hacen que FastAPI no pueda generar un esquema útil.

### 4.4 Testabilidad y pirámide
- Base unitaria buena: un fake por puerto, tests por servicio (`test_ingesta_service`, `test_tutoria_service`, etc.).
- Integración de infraestructura (9 archivos) y API (1 archivo, `test_api.py`) con `tmp_path` y `dependency_overrides`. Es proporcionada. Falta: tests de `AlmacenPostgres` contra Postgres real (solo se inyecta `pool` fake), y tests de contrato compartidos entre fake y adaptador real (nada garantiza que `fake_adapters.py` se comporta como `Json*`; riesgo de divergencia a 536 líneas de fakes).
- Sin tests E2E del frontend ni de las rutas SSE.

### 4.5 Coherencia docs vs código
- Coincide: diagrama de capas, lista de puertos y adaptadores, contratos de import, ubicación de `AlmacenDocumentos`.
- Divergencias detectadas:
  - ARCHITECTURE.md dice "Puertos abstractos (Protocols / ABC)" y "typing.Protocol": en el código todos son `ABC` y el nombre `LLMPort` es un alias.
  - Afirma que el dominio es "sin acceso a disco, red ni librerías externas" y que el núcleo "es independiente de sistemas de archivos"; `core/application` importa `os` y construye rutas con `os.path.join`/`os.sep`, y contiene nombres de carpetas de asignaturas concretas.
  - Describe `PluginsService` como "configuración de rutas y memoria"; en realidad también descubre archivos y compone texto de presentación.
  - No documenta el singleton `_global_container` ni el fallback de `dependencies.get_container`.
  - Los números ("once servicios", "11 routers") coinciden con el código.
  - Documentación en emojis y de 150+ líneas con listado de pestañas del frontend: documento de producto mezclado con documento de arquitectura.

### 4.6 Despliegue (AlmacenDocumentos)
Bien aislado: ABC de cuatro métodos (`leer/escribir/listar/eliminar`), dos implementaciones, selección por entorno en `almacen_por_defecto()`, `DocumentoJson` por encima. Es la única abstracción de persistencia claramente justificada por una segunda implementación real. Reservas:
- `AlmacenPostgres` mantiene un caché en memoria sin invalidación entre procesos (`almacen.py` `_cache`). Con más de un worker/instancia de Render, las lecturas serían obsoletas y las escrituras se pisarían. Hoy es un único proceso, pero no está garantizado ni documentado.
- Modelo clave-valor de documento entero: leer-modificar-escribir sin versionado. Es el punto débil de concurrencia (ver 4.7).
- `deploy/subir_datos.py` y `ML_EN_NUBE` (flag de entorno que oculta funciones) son lógica de despliegue que se filtra a la UI/servicios; es una decisión de producto vía variable de entorno, razonable pero fuera de un puerto.

### 4.7 Riesgos
- **Concurrencia en JSON**: `AlmacenArchivos.escribir` es atómico por archivo (`os.replace`, `almacen.py:77`), pero no hay ningún `Lock` en todo el backend (grep de `Lock|threading` vacío). Cada repo hace lectura-modificación-escritura de un documento completo (`registro_materiales.json`, `ajustes.json`, `cronograma`). Dos peticiones concurrentes (FastAPI ejecuta endpoints sync en threadpool) pueden perder actualizaciones. Con el SSE de tutoría, la ingesta larga y el cierre de clase simultáneos, el riesgo es real aunque de baja probabilidad con un solo usuario. No hay `run_in_threadpool`/`to_thread` explícito: los endpoints SSE que llaman a Gemini en modo síncrono deben ser `def` para no bloquear el loop (no verificado exhaustivamente).
- **`SessionStore` en memoria** (`apps/api/session_store.py`): sesiones de tutoría y quizzes viven en dicts del proceso; se pierden al reiniciar (Render duerme el servicio a los 15 min, según DESPLIEGUE.md) y no escalan a varias instancias. Sin TTL ni límite visible, hay fuga de memoria lenta.
- **Acoplamiento a Gemini**: el puerto es mínimo y razonable (4 métodos), pero (a) `generar_texto_con_archivo` recibe un `dict` con claves de `mime_type/path/data` (estructura de proveedor); (b) el JSON estructurado y la rotación de modelos/reintentos de cuota viven dentro del adaptador (correcto); (c) los prompts asumen modelo capaz de multimodalidad PDF. Cambiar de proveedor es viable, pero no hay un segundo adaptador que lo demuestre, ni un fake de LLM con tests de contrato.
- **Escalabilidad**: documento JSON entero por clave; `listar()` en Postgres trae `clave, contenido` de todas las filas del prefijo. Aceptable para decenas de materias. No es una arquitectura para multiusuario: no existe concepto de usuario/tenant (la autenticación es HTTP Basic de un solo usuario).
- **Seguridad de bordes** (fuera del alcance estricto, pero arquitectónico): `AccesoBasico` en un middleware de un solo usuario; `ConfiguracionService` persiste `gemini_api_key` (según ARCHITECTURE.md) en `ajustes.json`/`documentos` en claro.

## 5. ¿Sobreingeniería?

Veredicto: moderada, concentrada en pocos puntos. Para ~9.200 líneas de backend, 11 servicios y 16 puertos es denso pero no absurdo.

- **Puertos con una sola implementación** (de verdad no justificados por polimorfismo, sí por testabilidad con fakes): `LLM` (aislamiento de proveedor/coste, justificado), `BovedaNotasPort`, `LectorDocumentosPort`, `ConversorPdfPort`, `ExportadorPdfPort`, `InspectorProyectosPort`, `AjustesPort`, `GuiasRepo`, `TarjetasRepo`, `HistorialRepo`, `ProyectosRepo`, `PluginConfigRepoPort`, `MateriaRepo`, `RegistroMaterialesRepo`. Solo `PluginPracticoBase` (3 impl.) y `AlmacenDocumentos` (2 impl.) tienen polimorfismo real. El resto se justifica únicamente porque habilita fakes en tests y mantiene `core` libre de I/O, que es una razón válida aquí (el CLAUDE.md la declara y los tests la aprovechan). No recomiendo eliminar puertos; sí evitar crear más puertos por reflejo.
- **Repos de una sola tabla duplicados**: `TarjetasRepo`+`HistorialRepo`+`GuiasRepo`+`PluginConfigRepo`+`ProyectosRepo`+`RegistroMateriales`+`Materia` son siete wrappers de "una lista de dicts en un JSON". Candidatos a un único `Repositorio[T]` genérico sobre `DocumentoJson`.
- **Servicios-pasaporte**: `ConfiguracionService` (5 métodos, 0 `ajustes_port`: delega casi todo), `TelemetriaService` (1 método), y buena parte de `MateriasService` (catálogo) son delgados: cada llamada se reduce a `repo.x()`. Aportan un lugar para DI y límite para la API, pero no encapsulan reglas. Aceptable; no crear más.
- **Doble interfaz CLI + web**: justificada (dos adaptadores reales sobre el mismo núcleo), y de hecho es la mejor prueba de que la hexagonal no es decorativa. Pero el CLI (629 líneas) es mucho menos mantenido que la web (7 de 11 routers no tienen contraparte CLI); conviene decidir si el CLI sigue siendo ciudadano de primera.
- **Plugins**: tres plugins hardcodeados (Cisco, Node-RED, Web) y asociados a asignaturas concretas del autor (Packet Tracer, IoT). Sobreespecializado para un producto genérico, aunque coherente para uso personal.

## 6. Deuda técnica priorizada

| # | Prioridad | Deuda | Coste |
|---|---|---|---|
| 1 | Alta | Eliminar nombres de asignaturas/plugins hardcodeados y cascada if/elif en `PluginsService`; mover descubrimiento a cada plugin (`analizar(ruta)` en el puerto) y rutas de búsqueda a configuración | Medio |
| 2 | Alta | Concurrencia: añadir bloqueo por clave en `AlmacenDocumentos` (lock de proceso en `AlmacenArchivos`; `SELECT ... FOR UPDATE` o `updated_at` optimista en Postgres) y definir una operación `modificar(clave, fn)` | Medio |
| 3 | Alta | Trocear `MaterialView.tsx` y `SilabosView.tsx` (extraer subcomponentes y hooks `useMateriales`, `useCronograma`, "zona peligrosa") | Medio |
| 4 | Media | Tipar el dominio: dataclasses `Clase`, `Cronograma`, `Parcial`, `Material`, `PreguntaQuiz`; mover normalización de `guardar_cronograma` al dominio; devolver tipos desde servicios y modelos Pydantic en la API para obtener OpenAPI útil | Alto |
| 5 | Media | Jerarquía de excepciones de dominio (`NoEncontrado`, `ReglaDeNegocio`) mapeada centralmente con `exception_handler` en `apps/api/main.py`; borrar el patrón `if not ok: raise HTTPException(404)` | Bajo |
| 6 | Media | `SessionStore`: TTL, límite y/o persistencia; documentar que solo vale para un proceso | Bajo |
| 7 | Media | Partir `MateriasService` (catálogo vs cronograma/clases) y reemplazar `proyectos_service: Any` por un puerto o evento; quitar parámetros opcionales con ramas | Medio |
| 8 | Baja | `LLMPort`: renombrar clase a `LLMPort` y eliminar el alias; renombrar `LLM_GeminiAdapter` -> `GeminiAdapter`; sustituir el `dict` de archivo por un dataclass `ArchivoAdjunto` | Bajo |
| 9 | Baja | Sacar `os` de `core/application` (pasar a `PurePath`/`posixpath` o a un método `unir_ruta` del lector) y añadir `os`, `pathlib` a los módulos prohibidos del contrato | Bajo |
| 10 | Baja | Añadir contratos import-linter de tipo `layers` (apps > application > domain) y `independence` (api / cli) para blindar lo que hoy solo se cumple por costumbre | Bajo |
| 11 | Baja | Tests de contrato compartidos fake vs adaptador real; tests de `useEventStream` y de vistas clave; integración contra Postgres real en CI | Medio |
| 12 | Baja | Actualizar ARCHITECTURE.md (ABC no Protocol, singleton, matices de `os`), separar documentación de producto de la arquitectónica | Bajo |

## 7. Recomendaciones

**Qué simplificar**
- Colapsar los siete repos "lista de dicts en JSON" en un repositorio genérico sobre `DocumentoJson`; conservar los puertos pero reducir el boilerplate de adaptadores.
- No crear más servicios delgados; fusionar `TelemetriaService` en un servicio de lectura/consulta si no gana reglas.
- Eliminar el alias `LLMPort`, la rama `proyectos_repo`/`proyectos_service` duplicada en `MateriasService` y el `_global_container` (usar solo `app.state.container` y construir en el entrypoint del CLI).
- Decidir el destino del CLI: o se mantiene en paridad mínima, o se declara "modo mantenimiento" en la documentación.

**Qué reforzar**
- Hacer del dominio la fuente de verdad de los tipos (punto 4 de la deuda): es la única forma de que la hexagonal ofrezca valor más allá de la inyección de dependencias.
- Convertir la política de plugins en un contrato (`PluginPracticoBase` con `analizar(ruta)` y `nombre`) y registrar plugins por entry-point o lista en `bootstrap`, sin conocimiento de asignaturas en `core`.
- Endurecer persistencia: bloqueo y escritura condicional; documentar la restricción de "un solo proceso".
- Añadir contratos `layers` + `independence` y prohibir `os`/`pathlib` en `core` para que la regla "core no hace I/O" sea verificable.
- Frontend: introducir una capa de datos (TanStack Query o hooks propios) y dividir las vistas gigantes; generar `types.ts` desde OpenAPI una vez que la API devuelva modelos tipados.

## 8. Limitaciones de esta revisión
- No se ejecutaron los tests ni la web; la conformidad se midió por contratos, greps y lectura de código.
- No se leyeron en profundidad `gemini_adapter.py`, `tutoria.py` ni los routers SSE: la afirmación sobre bloqueo del event loop queda sin verificar.
- Algunos números de línea (p. ej. rangos de `plugins.py`, `eliminar_materia`) son aproximados; los demás se extrajeron de grep/wc.
