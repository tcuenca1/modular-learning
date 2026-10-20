export interface Configuracion {
  configurado: boolean
  carpeta_material: string
  ruta_obsidian: string
  existe_carpeta_material?: boolean
  existe_ruta_obsidian?: boolean
  carpeta_material_existe?: boolean
  ruta_obsidian_existe?: boolean
}

export interface GuardarConfig {
  carpeta_material: string
  ruta_obsidian: string
}

export interface MateriasResponse {
  materias: string[]
}

export interface ClaseCronograma {
  clase?: number | string
  semana?: number | string
  tema: string
  estado?: string
  contenido?: string
  materiales_asociados?: string[]
  subtemas_adicionales?: string[]
  [key: string]: unknown
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
    clases: ClaseCronograma[]
    [key: string]: unknown
  }
}

export interface GuardarSilaboResponse {
  ruta: string
  materias: string[]
}

export interface ArchivoPendiente {
  nombre: string
  ruta: string
  tipo: string
}

export interface EscaneoMaterial {
  materia: string
  carpeta: string
  existe: boolean
  total: number
  omitidos: number
  no_soportados: number
  pendientes: ArchivoPendiente[]
}

export interface EscaneoResponse {
  escaneos: EscaneoMaterial[]
}

export interface IngestarResponse {
  archivo: string
  materia: string
  tipo: string
  ruta_salida: string
  contenido_md: string
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
  exitosos?: number
  fallidos?: number
  omitidos?: number
}

export interface PluginsResponse {
  opciones: string[]
}

export interface ActualizarPluginResponse {
  seleccion: string
  resultado: string
}

// Tutoría
export interface IniciarTutoriaRequest {
  materia: string
  tema: string
  nivel_profundidad?: string
}

export interface PasoRoadmap {
  titulo: string
  descripcion: string
}

export interface SesionTutoriaResponse {
  sesion_id: string
  materia: string
  tema: string
  nivel_profundidad: string
  pasos: PasoRoadmap[]
  materiales_asociados: string[]
  subtemas_adicionales: string[]
}

export interface ResolverDudaRequest {
  paso: number
  duda: string
}

export interface ResolverDudaResponse {
  respuesta: string
}

export interface FinalizarTutoriaResponse {
  guia: string
  guardado_obsidian: boolean
  clase_completada: boolean
}

// Quiz
export interface PreguntaQuiz {
  enunciado: string
  opciones: string[]
}

export interface GenerarQuizResponse {
  quiz_id: string
  preguntas: PreguntaQuiz[]
}

export interface EvaluarQuizRequest {
  quiz_id: string
  respuestas: string[]
}

export interface DetalleEvaluacion {
  correcto: boolean
  respuesta_correcta: string
  elegida: string
}

export interface EvaluarQuizResponse {
  aciertos: number
  total: number
  porcentaje: number
  detalle: DetalleEvaluacion[]
}
