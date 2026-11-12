export interface Configuracion {
  configurado: boolean
  carpeta_material: string
  ruta_obsidian: string
  existe_carpeta_material?: boolean
  existe_ruta_obsidian?: boolean
  carpeta_material_existe?: boolean
  ruta_obsidian_existe?: boolean
  en_nube?: boolean
}

export interface GuardarConfig {
  carpeta_material: string
  ruta_obsidian: string
}

export interface MateriaItem {
  slug: string
  nombre: string
}

export interface MateriasResponse {
  materias: string[]
  catalogo?: MateriaItem[]
}

export interface ClaseCronograma {
  id?: string
  clase?: number | string
  semana?: number | string
  /** dd/mm/aaaa */
  fecha?: string
  tema: string
  estado?: string
  contenido?: string
  objetivo?: string
  materiales_asociados?: string[]
  subtemas_adicionales?: string[]
  [key: string]: unknown
}

export interface ParcialItem {
  nombre: string
  hasta?: string
  [key: string]: unknown
}

export interface CronogramasResponse {
  /** Clave: nombre derivado del archivo de cronograma (cruzar con `clave()`) */
  cronogramas: Record<string, ClaseCronograma[]>
}

export interface ProximasClasesResponse {
  clases: ClaseCronograma[]
}

export interface MateriaStat {
  total: number
  completados: number
  porcentaje: number
}

export interface StatsResponse {
  total_temas: number
  temas_completados: number
  porcentaje_global: number
  materias: Record<string, MateriaStat>
  plugins_activos: number
}

export interface ExtraerSilaboResponse {
  materia: string
  datos: {
    clases?: ClaseCronograma[]
    asignatura?: string
    codigo?: string
    profesor?: string
    periodo?: string
    [key: string]: unknown
  }
}

export interface GuardarSilaboResponse {
  ok?: boolean
  ruta: string
  materias?: string[]
}

export interface ArchivoPendiente {
  nombre: string
  ruta: string
  tipo: string
}

export interface EscaneoMaterial {
  materia: string
  carpeta?: string
  ruta_carpeta?: string
  existe: boolean
  total: number
  omitidos: number
  no_soportados: number
  pendientes: ArchivoPendiente[] | string[]
}

export interface EscanearResponse {
  escaneos: EscaneoMaterial[]
}
export type EscaneoResponse = EscanearResponse

export interface MaterialRegistrado {
  archivo: string
  nombre?: string
  materia: string
  fecha: string
  tipo?: string
  nota?: string
}

export interface IngestarResponse {
  archivo: string
  materia: string
  tipo: string
  ruta_salida: string
  contenido_md: string
  aviso?: string
  alineacion?: {
    clase_asignada?: number | string
    peso_afinidad?: number
    [key: string]: unknown
  }
}

export interface SincronizarEvento {
  evento: 'inicio' | 'archivo' | 'fin' | 'error'
  total?: number
  materias?: string[]
  indice?: number
  materia?: string
  archivo?: string
  tipo?: string
  ok?: boolean
  clase_asignada?: number | string
  afinidad?: number
  ruta_salida?: string
  error?: string
  aviso?: string
  exitosos?: number
  fallidos?: number
  omitidos?: number
}

export interface SincronizarResponse {
  total: number
  procesados: number
  errores: { archivo: string; error: string }[]
}

export interface PluginInfo {
  id: string
  nombre: string
  opcion_key: string
  categoria: string
  descripcion: string
  carpeta: string
  carpeta_existe: boolean
  materia: string
  contexto_reciente: string
}

export interface PluginsResponse {
  opciones: string[]
  plugins?: PluginInfo[]
}

export interface ConfigurarPluginRequest {
  clave: string
  carpeta?: string
  materia?: string
}

export interface ActualizarPluginResponse {
  seleccion: string
  resultado: string
}

// Proyectos
export interface ProyectoInfo {
  id: string
  nombre: string
  materia: string
  parcial: 'general' | 'primer_parcial' | 'segundo_parcial'
  tipo: 'software' | 'iot' | 'documental_auditoria' | 'documento_rector'
  ruta_origen: string
  ruta_nota_obsidian: string
  fecha_analisis: string
  mtime_archivos: number
  total_archivos: number
  hash_estado: string
}

export interface ProyectoCandidato {
  materia: string
  parcial: 'general' | 'primer_parcial' | 'segundo_parcial'
  nombre: string
  ruta: string
  tipo: 'software' | 'iot' | 'documental_auditoria' | 'documento_rector'
}

export interface EstadoProyectoResponse {
  existe: boolean
  proyecto?: ProyectoInfo
  estado: 'al_dia' | 'cambios_detectados' | 'carpeta_eliminada' | 'no_encontrado'
  modificado?: boolean
  mtime_registrado?: number
  mtime_actual?: number
  total_archivos_actual?: number
  hash_actual?: string
  mensaje?: string
}

export interface IngestarProyectoRequest {
  materia: string
  nombre: string
  parcial?: string
  ruta: string
  tipo?: string
}

export interface VaciarMaterialesResponse {
  ok: boolean
  resultado: {
    total_materiales_eliminados: number
    total_proyectos_eliminados: number
    notas_obsidian_borradas: number
  }
}

// Tutoría
export interface PasoRoadmap {
  titulo: string
  descripcion: string
}

export interface IniciarTutoriaRequest {
  materia: string
  tema: string
  clase_id?: string
  nivel_profundidad?: 'resumen' | 'estandar' | 'profundo' | string
  enfoque?: string
}

export interface SesionTutoriaResponse {
  sesion_id: string
  materia: string
  tema: string
  clase_id?: string
  nivel_profundidad: string
  pasos: PasoRoadmap[]
  materiales_asociados: string[]
  subtemas_adicionales: string[]
  enfoque: string | null
  fallos_previos: string[]
}
export type IniciarTutoriaResponse = SesionTutoriaResponse

export interface ExplicarPasoResponse {
  paso_index: number
  explicacion: string
}

export interface ResolverDudaRequest {
  paso: number
  duda: string
}

export interface ResponderDudaResponse {
  paso_index?: number
  duda?: string
  respuesta: string
}
export type ResolverDudaResponse = ResponderDudaResponse

export interface FinalizarTutoriaResponse {
  guia: string
  guardado_obsidian: boolean
  clase_completada: boolean
  sesion_id?: string
  materia?: string
  tema?: string
  resumen_sesion?: string
  nota_guardada?: string
  repaso_actualizado?: boolean
}

// Quiz
export interface PreguntaQuiz {
  enunciado: string
  opciones: string[]
  materia: string
  tema: string
}

export interface DetalleEvaluacion {
  correcto: boolean
  respuesta_correcta: string
  elegida: string
  materia: string
  tema: string
  explicacion: string
}

export interface GenerarQuizResponse {
  quiz_id: string
  preguntas: PreguntaQuiz[]
  paso_index?: number
  pregunta?: string
  opciones?: string[]
  respuesta_correcta?: number
  explicacion?: string
}

export interface EvaluarQuizRequest {
  quiz_id: string
  respuestas: string[]
}

export interface EvaluarQuizResponse {
  aciertos: number
  total: number
  porcentaje: number
  detalle: DetalleEvaluacion[]
  es_correcta?: boolean
  retroalimentacion?: string
}

export interface AjustesConfig {
  tutor?: {
    estilo?: string
    profundidad_defecto?: string
    analogias_frecuentes?: boolean
    [key: string]: unknown
  }
  repaso?: {
    intervalos_sm2?: number[]
    limite_diario?: number
    algoritmo?: string
    [key: string]: unknown
  }
  ingesta?: {
    extensiones_permitidas?: string[]
    ignorar_patrones?: string[]
    anonimizar_datos?: boolean
    [key: string]: unknown
  }
  guias?: {
    extension_defecto?: ExtensionGuia
    tiempo_promedio_clase_min?: number
    [key: string]: unknown
  }
  rutas?: {
    boveda?: string
    cronogramas?: string
    config?: string
    repaso?: string
    [key: string]: unknown
  }
  [key: string]: unknown
}

// Repaso espaciado (SM-2)
export type DificultadRepaso = 'otra_vez' | 'dificil' | 'bien' | 'facil'

export interface ResumenRepaso {
  pendientes_hoy: number
  total: number
  dominadas: number
}

export interface TarjetaRepaso {
  id: string
  materia: string
  pregunta: string
  respuesta: string
  intervalo_dias: number
  repeticiones: number
  factor_facilidad: number
  proxima_revision: string
  estado: string
  clase_origen?: string
  fuente?: string
  tipo?: string
  opciones?: string[]
  ultima_respuesta?: string
  explicacion?: string
}

export interface TarjetasRepasoResponse {
  tarjetas: TarjetaRepaso[]
  pendientes_hoy: TarjetaRepaso[]
  total_pendientes: number
}

export interface ResponderTarjetaResponse {
  tarjeta: TarjetaRepaso
  dias_proxima: number
}

export interface EventoHistorial {
  tipo: 'tutoria' | 'repaso' | 'guia'
  fecha: string
  materia: string
  tema: string
  aciertos?: number
  total?: number
  falladas?: number
  resultado?: ResultadoClaseGuia
  dudas?: string
}

export interface HistorialResponse {
  eventos: EventoHistorial[]
}

// Guías de estudio offline
export type ExtensionGuia = 'completa' | 'estandar' | 'sintesis'
export type ResultadoClaseGuia = 'entendida' | 'con_dudas' | 'pendiente'

export interface ClaseGuia {
  clase_id?: string
  tema: string
  /** dd/mm/aaaa */
  fecha: string
  contenido: string
  /** Respuestas de la autoevaluación, que van al final del documento */
  respuestas: string
  resultado: ResultadoClaseGuia | null
  dudas: string
  estado_previo?: string | null
}

export interface Guia {
  id: string
  materia: string
  extension: ExtensionGuia
  creada: string
  revisada: string | null
  completa: boolean
  pendiente_de_confirmar: boolean
  tiempo_minutos?: number | null
  clases: ClaseGuia[]
}

/** Guía sin el contenido de las clases, para listados */
export interface GuiaResumen extends Omit<Guia, 'clases'> {
  temas: string[]
  tiempo_minutos?: number | null
}

export interface ListaGuiasResponse {
  guias: GuiaResumen[]
}

export interface RevisionGuiaRequest {
  resultados: { indice: number; resultado: ResultadoClaseGuia; dudas?: string }[]
}

export interface RevisionGuiaResponse {
  materia: string
  completadas: string[]
  pendientes: string[]
  dudas: { tema: string; dudas: string }[]
}

// Cuentas y sesión
export interface Usuario {
  id: string
  correo: string
  nombre: string
  es_admin: boolean
}

export interface UsuarioAdmin extends Usuario {
  activo: boolean
  creado: string
}

export interface EstadoSesion {
  /** false: modo local sin login, se entra directo a la app */
  autenticacion: boolean
  usuario: Usuario | null
}

export interface LoginRequest {
  correo: string
  contrasena: string
}

export interface CambiarContrasenaRequest {
  actual: string
  nueva: string
}

export interface CrearUsuarioRequest {
  correo: string
  nombre: string
  contrasena: string
}

export interface ActualizarUsuarioRequest {
  activo?: boolean
  contrasena?: string
}
