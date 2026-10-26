import type {
  ActualizarPluginResponse,
  ClaseCronograma,
  ClaseGuia,
  Configuracion,
  CronogramasResponse,
  EscaneoResponse,
  EvaluarQuizRequest,
  EvaluarQuizResponse,
  ExtraerSilaboResponse,
  FinalizarTutoriaResponse,
  GenerarQuizResponse,
  GuardarConfig,
  GuardarSilaboResponse,
  Guia,
  HistorialResponse,
  IngestarResponse,
  IniciarTutoriaRequest,
  ListaGuiasResponse,
  MateriasResponse,
  PluginsResponse,
  ProximasClasesResponse,
  ResolverDudaRequest,
  ResolverDudaResponse,
  ResumenRepaso,
  RevisionGuiaRequest,
  RevisionGuiaResponse,
  SesionTutoriaResponse,
  StatsResponse,
} from './types'

const BASE_URL = ''

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMsg = `Error ${res.status}: ${res.statusText}`
    try {
      const err = await res.json()
      if (err.detail) {
        errorMsg = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail)
      }
    } catch {
      // Usar statusText
    }
    throw new Error(errorMsg)
  }
  return res.json()
}

export const api = {
  // Configuración
  async getConfig(): Promise<Configuracion> {
    const res = await fetch(`${BASE_URL}/api/config`)
    return handleResponse<Configuracion>(res)
  },

  async saveConfig(data: GuardarConfig): Promise<Configuracion> {
    const res = await fetch(`${BASE_URL}/api/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<Configuracion>(res)
  },

  // Materias
  async getMaterias(): Promise<MateriasResponse> {
    const res = await fetch(`${BASE_URL}/api/materias`)
    return handleResponse<MateriasResponse>(res)
  },

  async createMateria(nombre: string): Promise<MateriasResponse> {
    const res = await fetch(`${BASE_URL}/api/materias`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre }),
    })
    return handleResponse<MateriasResponse>(res)
  },

  async getProximasClases(materia: string): Promise<ProximasClasesResponse> {
    const res = await fetch(`${BASE_URL}/api/materias/${encodeURIComponent(materia)}/clases`)
    return handleResponse<ProximasClasesResponse>(res)
  },

  async getCronogramas(): Promise<CronogramasResponse> {
    const res = await fetch(`${BASE_URL}/api/materias/cronogramas`)
    return handleResponse<CronogramasResponse>(res)
  },

  // Stats
  async getStats(): Promise<StatsResponse> {
    const res = await fetch(`${BASE_URL}/api/stats`)
    return handleResponse<StatsResponse>(res)
  },

  // Sílabos
  async extraerSilabo(archivo: File, materia?: string): Promise<ExtraerSilaboResponse> {
    const formData = new FormData()
    formData.append('archivo', archivo)
    if (materia) {
      formData.append('materia', materia)
    }
    const res = await fetch(`${BASE_URL}/api/silabo/extraer`, {
      method: 'POST',
      body: formData,
    })
    return handleResponse<ExtraerSilaboResponse>(res)
  },

  async guardarSilabo(
    materia: string,
    clases: ClaseCronograma[]
  ): Promise<GuardarSilaboResponse> {
    const res = await fetch(`${BASE_URL}/api/silabo/guardar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ materia, datos: { clases } }),
    })
    return handleResponse<GuardarSilaboResponse>(res)
  },

  // Material
  async escanearMaterial(materia?: string): Promise<EscaneoResponse> {
    const url = materia
      ? `${BASE_URL}/api/material/escanear?materia=${encodeURIComponent(materia)}`
      : `${BASE_URL}/api/material/escanear`
    const res = await fetch(url)
    return handleResponse<EscaneoResponse>(res)
  },

  async ingestarArchivo(
    archivo: File,
    materia: string,
    tipo: string = 'material_complementario'
  ): Promise<IngestarResponse> {
    const formData = new FormData()
    formData.append('archivo', archivo)
    formData.append('materia', materia)
    formData.append('tipo', tipo)

    const res = await fetch(`${BASE_URL}/api/material/ingestar`, {
      method: 'POST',
      body: formData,
    })
    return handleResponse<IngestarResponse>(res)
  },

  // Plugins
  async getPlugins(): Promise<PluginsResponse> {
    const res = await fetch(`${BASE_URL}/api/plugins`)
    return handleResponse<PluginsResponse>(res)
  },

  async actualizarPlugin(seleccion: string): Promise<ActualizarPluginResponse> {
    const res = await fetch(`${BASE_URL}/api/plugins/actualizar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ seleccion }),
    })
    return handleResponse<ActualizarPluginResponse>(res)
  },

  // Tutoría
  async iniciarTutoria(data: IniciarTutoriaRequest): Promise<SesionTutoriaResponse> {
    const res = await fetch(`${BASE_URL}/api/tutoria/iniciar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<SesionTutoriaResponse>(res)
  },

  async resolverDuda(sesion_id: string, data: ResolverDudaRequest): Promise<ResolverDudaResponse> {
    const res = await fetch(`${BASE_URL}/api/tutoria/${encodeURIComponent(sesion_id)}/duda`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<ResolverDudaResponse>(res)
  },

  async finalizarTutoria(sesion_id: string): Promise<FinalizarTutoriaResponse> {
    const res = await fetch(`${BASE_URL}/api/tutoria/${encodeURIComponent(sesion_id)}/finalizar`, {
      method: 'POST',
    })
    return handleResponse<FinalizarTutoriaResponse>(res)
  },

  // Quiz
  async generarQuiz(): Promise<GenerarQuizResponse> {
    const res = await fetch(`${BASE_URL}/api/quiz/generar`)
    return handleResponse<GenerarQuizResponse>(res)
  },

  async evaluarQuiz(data: EvaluarQuizRequest): Promise<EvaluarQuizResponse> {
    const res = await fetch(`${BASE_URL}/api/quiz/evaluar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<EvaluarQuizResponse>(res)
  },

  // Repaso espaciado
  async getResumenRepaso(): Promise<ResumenRepaso> {
    const res = await fetch(`${BASE_URL}/api/repaso/resumen`)
    return handleResponse<ResumenRepaso>(res)
  },

  /** Quiz con las preguntas vencidas; se corrige con `evaluarQuiz`. */
  async repasoPendiente(): Promise<GenerarQuizResponse> {
    const res = await fetch(`${BASE_URL}/api/repaso/pendientes`)
    return handleResponse<GenerarQuizResponse>(res)
  },

  async getHistorial(materia?: string, tema?: string): Promise<HistorialResponse> {
    const q = new URLSearchParams()
    if (materia) q.set('materia', materia)
    if (tema) q.set('tema', tema)
    const res = await fetch(`${BASE_URL}/api/repaso/historial?${q.toString()}`)
    return handleResponse<HistorialResponse>(res)
  },

  // Guías offline
  async listarGuias(): Promise<ListaGuiasResponse> {
    const res = await fetch(`${BASE_URL}/api/guias`)
    return handleResponse<ListaGuiasResponse>(res)
  },

  async getGuiasPendientes(): Promise<ListaGuiasResponse> {
    const res = await fetch(`${BASE_URL}/api/guias/pendientes`)
    return handleResponse<ListaGuiasResponse>(res)
  },

  async getGuia(id: string): Promise<Guia> {
    const res = await fetch(`${BASE_URL}/api/guias/${encodeURIComponent(id)}`)
    return handleResponse<Guia>(res)
  },

  /** Registra la guía con sus clases; el contenido se genera después, clase a clase. */
  async crearGuia(materia: string, temas: string[]): Promise<Guia> {
    const res = await fetch(`${BASE_URL}/api/guias`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ materia, temas }),
    })
    return handleResponse<Guia>(res)
  },

  async generarClaseGuia(id: string, indice: number): Promise<ClaseGuia> {
    const res = await fetch(`${BASE_URL}/api/guias/${encodeURIComponent(id)}/clases/${indice}`, {
      method: 'POST',
    })
    return handleResponse<ClaseGuia>(res)
  },

  async registrarRevisionGuia(id: string, data: RevisionGuiaRequest): Promise<RevisionGuiaResponse> {
    const res = await fetch(`${BASE_URL}/api/guias/${encodeURIComponent(id)}/revision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<RevisionGuiaResponse>(res)
  },
}
