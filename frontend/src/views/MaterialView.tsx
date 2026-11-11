import React, { useCallback, useEffect, useState } from 'react'
import {
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Cloud,
  Code,
  Cpu,
  FileCheck2,
  FileText,
  FileUp,
  FolderGit2,
  FolderSearch,
  Layers,
  Pause,
  Play,
  RefreshCw,
  RotateCw,
  ShieldCheck,
  Sparkles,
  Trash2,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type {
  EscaneoMaterial,
  EstadoProyectoResponse,
  IngestarResponse,
  MaterialRegistrado,
  ProyectoCandidato,
  ProyectoInfo,
  SincronizarEvento,
} from '@/api/types'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Progress } from '@/components/ui/progress'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useEventStream } from '@/hooks/useEventStream'
import { cn } from '@/lib/utils'

function formatTipoProyecto(tipo: string) {
  switch (tipo) {
    case 'software':
      return {
        label: 'Software / Código',
        badgeClass: 'bg-sky-50 text-sky-700 border-sky-200 dark:bg-sky-950/40 dark:text-sky-300 dark:border-sky-800',
        icon: <Code className="h-3.5 w-3.5 text-sky-500" />,
      }
    case 'iot':
      return {
        label: 'IoT / Node-RED',
        badgeClass: 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800',
        icon: <Cpu className="h-3.5 w-3.5 text-emerald-500" />,
      }
    case 'documental_auditoria':
      return {
        label: 'Auditoría / SGSI',
        badgeClass: 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-950/40 dark:text-indigo-300 dark:border-indigo-800',
        icon: <ShieldCheck className="h-3.5 w-3.5 text-indigo-500" />,
      }
    case 'documento_rector':
      return {
        label: 'Doc. Rector',
        badgeClass: 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800',
        icon: <FileText className="h-3.5 w-3.5 text-amber-500" />,
      }
    default:
      return {
        label: tipo,
        badgeClass: 'bg-slate-50 text-slate-700 border-slate-200 dark:bg-slate-900 dark:text-slate-300',
        icon: <FolderGit2 className="h-3.5 w-3.5 text-slate-500" />,
      }
  }
}

function formatParcial(parcial: string) {
  switch (parcial) {
    case 'primer_parcial':
      return '1er Parcial'
    case 'segundo_parcial':
      return '2do Parcial'
    case 'general':
    default:
      return 'General'
  }
}

function formatearFecha(iso: string) {
  try {
    const d = new Date(iso)
    if (isNaN(d.getTime())) return iso
    return d.toLocaleString('es-EC', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return iso
  }
}

export function MaterialView({
  embebido = false,
  modo,
  materiaFiltro,
}: {
  embebido?: boolean
  modo?: 'materiales' | 'proyectos'
  materiaFiltro?: string
}) {
  const [internalSubpestaña, setInternalSubpestaña] = useState<'materiales' | 'proyectos'>('materiales')
  const subpestaña = modo || internalSubpestaña
  const setSubpestaña = setInternalSubpestaña

  const [materias, setMaterias] = useState<string[]>([])
  const [internalMateriaSeleccionada, setInternalMateriaSeleccionada] = useState<string>('__todas__')
  const materiaSeleccionada = materiaFiltro !== undefined ? materiaFiltro : internalMateriaSeleccionada
  const setMateriaSeleccionada = setInternalMateriaSeleccionada
  const [escaneos, setEscaneos] = useState<EscaneoMaterial[]>([])
  const [escaneando, setEscaneando] = useState(false)
  const [enNube, setEnNube] = useState(false)
  const [vaciando, setVaciando] = useState(false)

  // Subida individual de material
  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const [uploadMateria, setUploadMateria] = useState('')
  const [uploadTipo, setUploadTipo] = useState('material_complementario')
  const [subiendo, setSubiendo] = useState(false)
  const [resultadoSubida, setResultadoSubida] = useState<IngestarResponse | null>(null)
  const [mostrarSubida, setMostrarSubida] = useState(false)

  // Materiales registrados (ingestados)
  const [registrados, setRegistrados] = useState<MaterialRegistrado[]>([])
  const [cargandoRegistrados, setCargandoRegistrados] = useState(true)
  const [eliminandoArchivo, setEliminandoArchivo] = useState<string | null>(null)

  // Proyectos
  const [proyectos, setProyectos] = useState<ProyectoInfo[]>([])
  const [candidatos, setCandidatos] = useState<ProyectoCandidato[]>([])
  const [estadosProyectos, setEstadosProyectos] = useState<Record<string, EstadoProyectoResponse>>({})
  const [cargandoProyectos, setCargandoProyectos] = useState(true)
  const [actualizandoProyectoId, setActualizandoProyectoId] = useState<string | null>(null)
  const [ingestandoRuta, setIngestandoRuta] = useState<string | null>(null)
  const [verificandoEstados, setVerificandoEstados] = useState(false)

  // Stream de sincronización en tiempo real
  const [streamProgress, setStreamProgress] = useState<{
    total: number
    hecho: number
    archivoActual: string
    exitosos: number
    fallidos: number
    avisos: { archivo: string; aviso: string }[]
  }>({
    total: 0,
    hecho: 0,
    archivoActual: '',
    exitosos: 0,
    fallidos: 0,
    avisos: [],
  })

  const cargarRegistrados = useCallback(async () => {
    try {
      const res = await api.getMaterialesRegistrados()
      setRegistrados(res.materiales || [])
    } catch (err) {
      console.error('Error cargando materiales registrados:', err)
    } finally {
      setCargandoRegistrados(false)
    }
  }, [])

  const verificarEstados = useCallback(async (lista: ProyectoInfo[]) => {
    try {
      setVerificandoEstados(true)
      const estadosTemp: Record<string, EstadoProyectoResponse> = {}
      await Promise.all(
        lista.map(async (p) => {
          try {
            const est = await api.getEstadoProyecto(p.id)
            estadosTemp[p.id] = est
          } catch {
            // Ignorar fallo puntual
          }
        })
      )
      setEstadosProyectos((prev) => ({ ...prev, ...estadosTemp }))
    } finally {
      setVerificandoEstados(false)
    }
  }, [])

  const cargarProyectos = useCallback(
    async (materiaFiltro?: string) => {
      try {
        const mat =
          materiaFiltro ?? (materiaSeleccionada === '__todas__' ? undefined : materiaSeleccionada)
        const [resProy, resCand] = await Promise.all([
          api.getProyectos(mat).catch(() => ({ proyectos: [] })),
          enNube ? Promise.resolve({ candidatos: [] }) : api.escanearProyectos(mat).catch(() => ({ candidatos: [] })),
        ])
        const listaProyectos = resProy.proyectos || []
        setProyectos(listaProyectos)
        setCandidatos(resCand.candidatos || [])

        if (listaProyectos.length > 0) {
          verificarEstados(listaProyectos)
        }
      } catch (err) {
        console.error('Error cargando proyectos:', err)
      } finally {
        setCargandoProyectos(false)
      }
    },
    [materiaSeleccionada, verificarEstados, enNube]
  )

  const {
    isStreaming,
    events,
    startStream,
    stopStream,
    clearEvents,
  } = useEventStream<SincronizarEvento>({
    url: '/api/material/sincronizar/stream',
    method: 'POST',
    onMessage: (ev) => {
      if (ev.evento === 'inicio') {
        setStreamProgress((prev) => ({
          ...prev,
          total: ev.total || 0,
          hecho: 0,
          exitosos: 0,
          fallidos: 0,
          avisos: [],
        }))
      } else if (ev.evento === 'archivo') {
        setStreamProgress((prev) => ({
          ...prev,
          hecho: ev.indice || prev.hecho + 1,
          archivoActual: ev.archivo || '',
          exitosos: ev.ok ? prev.exitosos + 1 : prev.exitosos,
          fallidos: !ev.ok ? prev.fallidos + 1 : prev.fallidos,
          avisos: ev.aviso
            ? [...prev.avisos, { archivo: ev.archivo || '', aviso: ev.aviso }]
            : prev.avisos,
        }))
      } else if (ev.evento === 'fin') {
        toast.success('Material procesado', {
          description: `Completados con éxito: ${ev.exitosos || 0}, Fallidos: ${ev.fallidos || 0}`,
        })
        handleEscanear()
        cargarRegistrados()
      }
    },
    onError: (err) => {
      toast.error('Se interrumpió el procesamiento', {
        description: err.message,
      })
    },
  })

  useEffect(() => {
    api
      .getConfig()
      .then((cfg) => {
        if (cfg.en_nube) setEnNube(true)
      })
      .catch(() => {})

    api
      .getMaterias()
      .then((res) => {
        setMaterias(res.materias)
        if (res.materias.length > 0) {
          setUploadMateria((prev) => (prev && res.materias.includes(prev) ? prev : res.materias[0]))
        }
      })
      .catch((err) => console.error(err))

    api
      .getMaterialesRegistrados()
      .then((res) => {
        setRegistrados(res.materiales || [])
      })
      .catch((err) => {
        console.error('Error cargando materiales registrados:', err)
      })
      .finally(() => {
        setCargandoRegistrados(false)
      })
  }, [])

  useEffect(() => {
    let cancelado = false
    api
      .getConfig()
      .then((cfg) => {
        if (cancelado) return
        const enLaNube = Boolean(cfg.en_nube)
        setEnNube(enLaNube)
        const mat = materiaSeleccionada === '__todas__' ? undefined : materiaSeleccionada
        return Promise.all([
          api.getProyectos(mat).catch(() => ({ proyectos: [] })),
          enLaNube
            ? Promise.resolve({ candidatos: [] })
            : api.escanearProyectos(mat).catch(() => ({ candidatos: [] })),
        ])
      })
      .then((res) => {
        if (!res || cancelado) return
        const [resProy, resCand] = res
        const listaProyectos = resProy.proyectos || []
        setProyectos(listaProyectos)
        setCandidatos(resCand.candidatos || [])
        if (listaProyectos.length > 0) {
          verificarEstados(listaProyectos)
        }
      })
      .catch((err) => {
        console.error('Error cargando proyectos:', err)
      })
      .finally(() => {
        if (!cancelado) {
          setCargandoProyectos(false)
        }
      })

    return () => {
      cancelado = true
    }
  }, [materiaSeleccionada, verificarEstados])

  const handleEscanear = async () => {
    try {
      setEscaneando(true)
      const res = await api.escanearMaterial(
        materiaSeleccionada === '__todas__' ? undefined : materiaSeleccionada
      )
      setEscaneos(res.escaneos)
      const totalPendientes = res.escaneos.reduce((acc, e) => acc + e.pendientes.length, 0)
      toast.info('Carpetas revisadas', {
        description: `${totalPendientes} archivos nuevos de estudio por procesar.`,
      })
      await cargarProyectos()
    } catch (err) {
      toast.error('No pude revisar tus carpetas', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setEscaneando(false)
    }
  }

  const handleStartSync = () => {
    clearEvents()
    setStreamProgress({
      total: 0,
      hecho: 0,
      archivoActual: 'Preparando análisis...',
      exitosos: 0,
      fallidos: 0,
      avisos: [],
    })
    startStream({ materia: materiaSeleccionada })
  }

  const handleUploadIndividual = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!uploadFile) {
      toast.error('Elige un archivo.')
      return
    }
    if (!uploadMateria.trim()) {
      toast.error('Selecciona una asignatura.')
      return
    }

    try {
      setSubiendo(true)
      const res = await api.ingestarArchivo(uploadFile, uploadMateria.trim(), uploadTipo)
      setResultadoSubida(res)
      toast.success('Nota creada', {
        description: `Asignado a Clase ${res.alineacion?.clase_asignada || 'X'} (Afinidad: ${
          res.alineacion?.peso_afinidad || 0
        }%)`,
      })
      setUploadFile(null)
      cargarRegistrados()
    } catch (err) {
      toast.error('No pude procesar el archivo', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setSubiendo(false)
    }
  }

  const handleEliminarMaterial = async (archivo: string) => {
    const borrarNota = window.confirm(
      `¿Deseas desvincular el material "${archivo}"?\n\n` +
      `Presiona Aceptar para desvincularlo y BORRAR también su nota en Obsidian.\n` +
      `Presiona Cancelar si no deseas continuar.`
    )
    if (!borrarNota) return

    try {
      setEliminandoArchivo(archivo)
      await api.eliminarMaterial(archivo, true)
      toast.success('Material eliminado', {
        description: `"${archivo}" fue desvinculado de las clases y su nota en Obsidian eliminada.`,
      })
      setRegistrados((prev) => prev.filter((m) => (m.archivo || m.nombre) !== archivo))
    } catch (err) {
      toast.error('No se pudo eliminar el material', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setEliminandoArchivo(null)
    }
  }

  const handleIngestarProyecto = async (c: ProyectoCandidato) => {
    try {
      setIngestandoRuta(c.ruta)
      const res = await api.ingestarProyecto({
        materia: c.materia,
        nombre: c.nombre,
        parcial: c.parcial,
        ruta: c.ruta,
        tipo: c.tipo,
      })
      toast.success('Ficha de proyecto creada en Obsidian', {
        description: `"${res.proyecto.nombre}" (${formatTipoProyecto(res.proyecto.tipo).label}) sincronizado.`,
      })
      await cargarProyectos()
    } catch (err) {
      toast.error('No se pudo procesar el proyecto', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setIngestandoRuta(null)
    }
  }

  const handleActualizarProyecto = async (id: string, nombre: string) => {
    try {
      setActualizandoProyectoId(id)
      await api.actualizarProyecto(id)
      toast.success('Ficha técnica actualizada', {
        description: `Se detectaron cambios en disco y se actualizó la nota en Obsidian para "${nombre}".`,
      })
      await cargarProyectos()
    } catch (err) {
      toast.error('Error al actualizar el proyecto', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setActualizandoProyectoId(null)
    }
  }

  const handleEliminarProyecto = async (id: string, nombre: string) => {
    const conf = window.confirm(
      `¿Deseas desvincular el proyecto "${nombre}" del registro?\n\n` +
      `Presiona Aceptar para continuar. Tu carpeta original de archivos no será modificada.`
    )
    if (!conf) return

    try {
      await api.eliminarProyecto(id)
      toast.success('Proyecto desvinculado', {
        description: `"${nombre}" fue eliminado del registro de proyectos.`,
      })
      setProyectos((prev) => prev.filter((p) => p.id !== id))
    } catch (err) {
      toast.error('No se pudo desvincular el proyecto', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleVaciarTodo = async () => {
    const conf = window.confirm(
      '⚠️ ATENCIÓN: VACIADO DE MATERIALES Y PROYECTOS\n\n' +
      '¿Estás seguro de que deseas vaciar todos los materiales y proyectos convertidos en notas?\n\n' +
      '• Se limpiará el registro de materiales y proyectos.\n' +
      '• Se borrarán las notas autogeneradas en Obsidian (Material, Actividades, Proyectos).\n' +
      '• Tu configuración (.obsidian/), sílabos y cronogramas quedarán intactos.\n' +
      '• Tus carpetas originales de OneDrive quedan 100% protegidas en solo lectura.\n\n' +
      '¿Deseas continuar?'
    )
    if (!conf) return

    try {
      setVaciando(true)
      const res = await api.vaciarMateriales(true)
      toast.success('Vaciado completado', {
        description: `${res.resultado.total_materiales_eliminados} materiales y ${res.resultado.total_proyectos_eliminados} proyectos eliminados (${res.resultado.notas_obsidian_borradas} notas de Obsidian borradas).`,
      })
      await Promise.all([cargarRegistrados(), cargarProyectos(), handleEscanear()])
    } catch (err) {
      toast.error('Error al vaciar materiales', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setVaciando(false)
    }
  }

  const totalPendientes = escaneos.reduce((acc, e) => acc + e.pendientes.length, 0)
  const pctSincronizacion =
    streamProgress.total > 0
      ? Math.round((streamProgress.hecho / streamProgress.total) * 100)
      : 0

  const registradosFiltrados = materiaSeleccionada === '__todas__'
    ? registrados
    : registrados.filter((m) => m.materia?.toLowerCase() === materiaSeleccionada.toLowerCase())

  const proyectosFiltrados = materiaSeleccionada === '__todas__'
    ? proyectos
    : proyectos.filter((p) => p.materia?.toLowerCase() === materiaSeleccionada.toLowerCase())

  const candidatosFiltrados = materiaSeleccionada === '__todas__'
    ? candidatos
    : candidatos.filter((c) => c.materia?.toLowerCase() === materiaSeleccionada.toLowerCase())

  // Proyectos candidatos que aún no están en la lista de registrados
  const candidatosSinRegistrar = candidatosFiltrados.filter(
    (c) => !proyectosFiltrados.some((p) => p.ruta_origen === c.ruta || p.nombre.toLowerCase() === c.nombre.toLowerCase())
  )

  const proyectosConCambios = proyectosFiltrados.filter(
    (p) => estadosProyectos[p.id]?.estado === 'cambios_detectados'
  )

  return (
    <div className="space-y-8 pb-12">
      {!embebido && (
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
            Gestión de material
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Escanea directorios de clase, procesa proyectos universales y sincroniza notas estructuradas en Obsidian.
          </p>
        </div>
      )}

      {/* Aviso modo en la nube */}
      {enNube && (
        <div className="rounded-xl border border-indigo-200 bg-indigo-50/60 p-4 dark:border-indigo-900 dark:bg-indigo-950/30">
          <div className="flex items-start gap-3">
            <Cloud className="h-5 w-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <p className="font-semibold text-indigo-950 dark:text-indigo-200">
                Despliegue en la nube
              </p>
              <p className="text-slate-600 dark:text-slate-300">
                El servidor en Render no tiene acceso a las carpetas físicas de tu ordenador local.
                Para procesar nuevos documentos, utiliza la sección <strong>Subir un archivo suelto</strong> de abajo
                o ejecuta la aplicación en modo local apuntando a tu base de datos Neon.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Barra de Controles y Escaneo */}
      {!enNube && (
        <Card>
          <CardHeader>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <CardTitle>Tus carpetas de asignatura</CardTitle>
              <CardDescription>
                Detecta materiales de estudio, actividades y proyectos de parcial en <code>6. SEXTO/</code>.
              </CardDescription>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {!embebido && (
                <select
                  value={materiaSeleccionada}
                  onChange={(e) => { setCargandoProyectos(true); setMateriaSeleccionada(e.target.value); }}
                  className="h-9 rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                >
                  <option value="__todas__">Todas las asignaturas</option>
                  {materias.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              )}

              <Button
                variant="outline"
                size="sm"
                onClick={handleEscanear}
                disabled={escaneando || isStreaming || cargandoProyectos}
                className="gap-1.5"
              >
                <FolderSearch className={`h-4 w-4 ${escaneando ? 'animate-spin' : ''}`} />
                {escaneando ? 'Revisando…' : 'Revisar carpetas'}
              </Button>

              {isStreaming ? (
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={stopStream}
                  className="gap-1.5"
                >
                  <Pause className="h-4 w-4" /> Detener
                </Button>
              ) : (
                <Button
                  size="sm"
                  onClick={handleStartSync}
                  disabled={totalPendientes === 0 && escaneos.length > 0}
                  className="gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white"
                >
                  <Play className="h-4 w-4" /> Procesar {totalPendientes > 0 ? `(${totalPendientes})` : 'nuevos'}
                </Button>
              )}


            </div>
          </div>
        </CardHeader>

        {/* Panel de progreso de streaming si está activo o hubo eventos */}
        {(isStreaming || events.length > 0) && (
          <CardContent className="border-t border-slate-100 dark:border-slate-800 pt-6 space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-medium text-slate-600 dark:text-slate-400">
                <span>
                  Procesando: {streamProgress.archivoActual || 'Iniciando...'}
                </span>
                <span>
                  {streamProgress.hecho} de {streamProgress.total} ({pctSincronizacion}%)
                </span>
              </div>
              <Progress value={pctSincronizacion} className="h-2" />
            </div>

            {/* Resumen de resultados rápidos */}
            <div className="flex gap-4 text-xs">
              <span className="text-emerald-600 font-medium">
                Éxito: {streamProgress.exitosos}
              </span>
              <span className="text-rose-600 font-medium">
                Errores: {streamProgress.fallidos}
              </span>
            </div>

            {streamProgress.avisos.length > 0 && (
              <div className="mt-3 space-y-1.5 rounded-md border border-amber-200 bg-amber-50/70 p-3 text-xs text-amber-900 dark:border-amber-900/50 dark:bg-amber-950/20 dark:text-amber-300">
                <div className="font-semibold flex items-center gap-1.5">
                  <AlertCircle className="h-4 w-4 shrink-0 text-amber-600" />
                  Avisos de procesamiento ({streamProgress.avisos.length}):
                </div>
                <ul className="list-disc pl-5 space-y-1">
                  {streamProgress.avisos.map((item, idx) => (
                    <li key={idx}>
                      <span className="font-medium">{item.archivo}:</span> {item.aviso}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        )}
      </Card>
      )}

      {/* Selector de Sub-pestañas: solo si no está controlado externamente */}
      {!modo && (
        <div className="flex items-center gap-4 border-b border-slate-200 dark:border-slate-800 pb-1">
          <button
            type="button"
            onClick={() => setSubpestaña('materiales')}
            className={cn(
              'flex items-center gap-2 pb-2 text-sm font-medium border-b-2 transition-colors',
              subpestaña === 'materiales'
                ? 'border-indigo-600 text-indigo-600 dark:border-indigo-400 dark:text-indigo-400'
                : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            )}
          >
            <Layers className="h-4 w-4" />
            Materiales y Actividades
            <Badge variant="secondary" className="text-xs px-1.5 py-0">
              {registradosFiltrados.length}
            </Badge>
          </button>

          <button
            type="button"
            onClick={() => setSubpestaña('proyectos')}
            className={cn(
              'flex items-center gap-2 pb-2 text-sm font-medium border-b-2 transition-colors',
              subpestaña === 'proyectos'
                ? 'border-indigo-600 text-indigo-600 dark:border-indigo-400 dark:text-indigo-400'
                : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            )}
          >
            <FolderGit2 className="h-4 w-4" />
            Proyectos de Asignatura
            <Badge variant="secondary" className="text-xs px-1.5 py-0">
              {proyectosFiltrados.length}
            </Badge>
            {candidatosSinRegistrar.length > 0 && (
              <Badge className="bg-amber-500/15 text-amber-600 border border-amber-300 dark:border-amber-800 text-[10px] px-1.5 py-0">
                {candidatosSinRegistrar.length} pendientes
              </Badge>
            )}
            {proyectosConCambios.length > 0 && (
              <Badge className="bg-rose-500/15 text-rose-600 border border-rose-300 dark:border-rose-800 text-[10px] px-1.5 py-0">
                {proyectosConCambios.length} con cambios
              </Badge>
            )}
          </button>
        </div>
      )}

      {/* CONTENIDO PESTAÑA 1: MATERIALES Y ACTIVIDADES */}
      {subpestaña === 'materiales' && (
        <div className="space-y-8">
                    {/* Historial de Materiales Ingestados */}
          <Card>
            <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <CardTitle>Materiales convertidos en notas ({registradosFiltrados.length})</CardTitle>
                <CardDescription>
                  Documentos individuales de estudio y actividades convertidos en notas vinculadas con el cronograma.
                </CardDescription>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <Button
                  variant={mostrarSubida ? 'secondary' : 'default'}
                  size="sm"
                  onClick={() => setMostrarSubida((v) => !v)}
                  className="gap-1.5"
                >
                  <FileUp className="h-4 w-4" />
                  {mostrarSubida ? 'Cerrar subida' : 'Subir un archivo'}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => { setCargandoRegistrados(true); void cargarRegistrados(); }}
                  disabled={cargandoRegistrados}
                  className="gap-1.5"
                >
                  <RotateCw className={`h-4 w-4 ${cargandoRegistrados ? 'animate-spin' : ''}`} />
                  Actualizar lista
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {registradosFiltrados.length === 0 ? (
                <p className="text-sm text-slate-500 py-4 text-center">
                  No hay materiales registrados para la selección actual.
                </p>
              ) : (
                <div className="rounded-lg border border-slate-200 dark:border-slate-800">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Archivo</TableHead>
                        <TableHead className="w-40">Asignatura</TableHead>
                        <TableHead className="w-32">Tipo</TableHead>
                        <TableHead>Nota de Obsidian</TableHead>
                        <TableHead className="w-16 text-right">Acción</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {registradosFiltrados.map((m, idx) => {
                        const nombreArchivo = m.archivo || m.nombre || `material_${idx}`
                        const estaEliminando = eliminandoArchivo === nombreArchivo
                        return (
                          <TableRow key={idx}>
                            <TableCell className="font-medium text-slate-900 dark:text-slate-100 flex items-center gap-2">
                              <FileText className="h-4 w-4 text-indigo-500 shrink-0" />
                              <span className="truncate max-w-xs">{nombreArchivo}</span>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">{m.materia}</Badge>
                            </TableCell>
                            <TableCell className="text-xs text-slate-500">
                              {m.tipo || 'complementario'}
                            </TableCell>
                            <TableCell className="font-mono text-xs text-slate-500 truncate max-w-xs">
                              {m.nota || '—'}
                            </TableCell>
                            <TableCell className="text-right">
                              <Button
                                variant="ghost"
                                size="icon"
                                disabled={estaEliminando}
                                onClick={() => handleEliminarMaterial(nombreArchivo)}
                                title="Desvincular y eliminar nota en Obsidian"
                                className="h-8 w-8 text-slate-400 hover:text-red-600"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </TableCell>
                          </TableRow>
                        )
                      })}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Subida Individual y Anonimización */}
          {mostrarSubida && (
            <Card>
            <CardHeader>
              <CardTitle>Subir un archivo suelto</CardTitle>
              <CardDescription>
                Se convierte en nota, se quitan los datos personales y se asigna a la clase que corresponda.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleUploadIndividual} className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-3">
                  <div>
                    <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                      Asignatura
                    </label>
                    <select
                      value={uploadMateria}
                      onChange={(e) => setUploadMateria(e.target.value)}
                      className="mt-1 h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                      required
                    >
                      {materias.length === 0 ? (
                        <option value="">Sin asignaturas registradas</option>
                      ) : (
                        materias.map((m) => (
                          <option key={m} value={m}>
                            {m}
                          </option>
                        ))
                      )}
                    </select>
                  </div>

                  <div>
                    <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                      Tipo
                    </label>
                    <select
                      value={uploadTipo}
                      onChange={(e) => setUploadTipo(e.target.value)}
                      className="mt-1 h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                    >
                      <option value="material_complementario">Material de Estudio / Complementario</option>
                      <option value="actividad">Actividad o práctica</option>
                      <option value="diapositiva">Diapositivas</option>
                      <option value="lectura">Lectura o artículo</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                      Archivo (.pdf, .docx, .pptx, .txt, .md)
                    </label>
                    <Input
                      type="file"
                      accept=".pdf,.docx,.pptx,.txt,.md"
                      onChange={(e) => {
                        if (e.target.files && e.target.files[0]) {
                          setUploadFile(e.target.files[0])
                        }
                      }}
                      className="mt-1"
                      required
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  disabled={subiendo || !uploadFile}
                  className="gap-2 bg-indigo-600 hover:bg-indigo-500 text-white"
                >
                  {subiendo ? (
                    <>
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                      Procesando…
                    </>
                  ) : (
                    <>
                      <FileUp className="h-4 w-4" /> Convertir en nota
                    </>
                  )}
                </Button>
              </form>

              {/* Resultado de la Subida */}
              {resultadoSubida && (
                <div className="mt-6 rounded-lg border border-emerald-200 bg-emerald-50/50 p-4 dark:border-emerald-900 dark:bg-emerald-950/20">
                  <div className="flex items-center gap-2 text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                    <CheckCircle2 className="h-4 w-4" />
                    Material convertido en nota: {resultadoSubida.archivo}
                  </div>
                  {resultadoSubida.aviso && (
                    <div className="mt-2 flex items-start gap-1.5 rounded border border-amber-300 bg-amber-50 p-2 text-xs text-amber-800 dark:border-amber-800 dark:bg-amber-950/40 dark:text-amber-300">
                      <AlertCircle className="h-4 w-4 shrink-0 mt-0.5 text-amber-600" />
                      <span>{resultadoSubida.aviso}</span>
                    </div>
                  )}
                  <div className="mt-2 grid gap-2 sm:grid-cols-2 text-xs text-emerald-700 dark:text-emerald-400">
                    <div>
                      <span className="font-medium">Alineación Curricular:</span> Clase{' '}
                      {resultadoSubida.alineacion?.clase_asignada ?? 'X'} (Afinidad:{' '}
                      {resultadoSubida.alineacion?.peso_afinidad ?? 0}%)
                    </div>
                    <div>
                      <span className="font-medium">Destino Obsidian:</span>{' '}
                      <span className="font-mono text-[11px] truncate block">
                        {resultadoSubida.ruta_salida}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
          )}

          {/* Resultados del Escaneo */}
          {escaneos.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-lg font-semibold tracking-tight text-slate-900 dark:text-white">
                Archivos encontrados en carpetas
              </h2>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {escaneos.map((esc, i) => (
                  <Card key={i} className={!esc.existe ? 'border-dashed opacity-75' : ''}>
                    <CardHeader className="p-4 pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle as="h3" className="text-sm font-semibold">{esc.materia}</CardTitle>
                        <Badge variant={esc.existe ? 'secondary' : 'destructive'}>
                          {esc.existe ? `${esc.pendientes.length} nuevos` : 'No existe la carpeta'}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="p-4 pt-1 text-xs space-y-1 text-slate-500">
                      <div className="flex justify-between">
                        <span>Archivos totales:</span>
                        <strong className="text-slate-700 dark:text-slate-300">{esc.total}</strong>
                      </div>
                      <div className="flex justify-between">
                        <span>Ya procesados:</span>
                        <strong className="text-emerald-600">{esc.omitidos}</strong>
                      </div>
                      <div className="flex justify-between">
                        <span>No soportados:</span>
                        <strong className="text-amber-600">{esc.no_soportados}</strong>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* CONTENIDO PESTAÑA 2: PROYECTOS DE ASIGNATURA */}
      {subpestaña === 'proyectos' && (
        <div className="space-y-8">
          {/* Explicación y directriz de arquitectura */}
          <div className="rounded-xl border border-indigo-100 bg-indigo-50/40 p-4 dark:border-indigo-950 dark:bg-indigo-950/20">
            <div className="flex items-start gap-3">
              <Sparkles className="h-5 w-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
              <div className="text-xs space-y-1">
                <p className="font-semibold text-indigo-950 dark:text-indigo-200">
                  Fichas Técnicas Universales y Trazabilidad Fija (Opción A)
                </p>
                <p className="text-slate-600 dark:text-slate-300">
                  Las carpetas de proyecto (código fuente, flujos Node-RED, auditorías SGSI o documentos rectores) se conservan
                  en <strong>solo lectura</strong> en tu OneDrive. Cada proyecto genera una ficha técnica de arquitectura en{' '}
                  <code className="text-indigo-700 dark:text-indigo-300 font-mono">
                    Obsidian/&lt;Asignatura&gt;/Proyectos/&lt;Nombre&gt;.md
                  </code>{' '}
                  con seguimiento continuo de modificaciones en disco para mantenerla siempre al día.
                </p>
              </div>
            </div>
          </div>

          {/* Proyectos detectados en disco (pendientes de convertir) */}
          <Card>
            <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <CardTitle>Proyectos detectados en carpeta ({candidatosSinRegistrar.length} pendientes)</CardTitle>
                <CardDescription>
                  Escaneados automáticamente en <code>PROYECTO/</code> (General) o <code>PROYECTOS/</code> (1er y 2do Parcial).
                </CardDescription>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => { setCargandoProyectos(true); void cargarProyectos(); }}
                disabled={cargandoProyectos}
                className="gap-1.5"
              >
                <RefreshCw className={`h-4 w-4 ${cargandoProyectos ? 'animate-spin' : ''}`} />
                Re-escanear proyectos
              </Button>
            </CardHeader>
            <CardContent>
              {candidatosSinRegistrar.length === 0 ? (
                <div className="py-6 text-center text-xs text-slate-500">
                  {candidatosFiltrados.length > 0 ? (
                    <span className="text-emerald-600 dark:text-emerald-400 font-medium flex items-center justify-center gap-1.5">
                      <CheckCircle2 className="h-4 w-4" /> Todos los proyectos detectados ya tienen su ficha técnica en Obsidian.
                    </span>
                  ) : (
                    'No se detectaron nuevas carpetas de proyecto en la selección actual.'
                  )}
                </div>
              ) : (
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {candidatosSinRegistrar.map((cand, idx) => {
                    const tipoFmt = formatTipoProyecto(cand.tipo)
                    const estaIngestando = ingestandoRuta === cand.ruta
                    return (
                      <Card key={idx} className="border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40">
                        <CardHeader className="p-4 pb-2">
                          <div className="flex items-start justify-between gap-2">
                            <div className="space-y-1">
                              <div className="flex items-center gap-1.5">
                                {tipoFmt.icon}
                                <span className="font-semibold text-sm text-slate-900 dark:text-slate-100 truncate max-w-[180px]">
                                  {cand.nombre}
                                </span>
                              </div>
                              <Badge variant="outline" className="text-[11px]">
                                {cand.materia}
                              </Badge>
                            </div>
                            <Badge className={cn('text-[10px] border', tipoFmt.badgeClass)}>
                              {tipoFmt.label}
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent className="p-4 pt-2 text-xs space-y-3">
                          <div className="flex justify-between text-slate-500">
                            <span>Parcial:</span>
                            <strong className="text-slate-700 dark:text-slate-300">
                              {formatParcial(cand.parcial)}
                            </strong>
                          </div>
                          <div className="text-[11px] font-mono text-slate-500 truncate" title={cand.ruta}>
                            {cand.ruta}
                          </div>
                          <Button
                            size="sm"
                            className="w-full gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white"
                            disabled={estaIngestando}
                            onClick={() => handleIngestarProyecto(cand)}
                          >
                            {estaIngestando ? (
                              <>
                                <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                                Generando ficha…
                              </>
                            ) : (
                              <>
                                <Sparkles className="h-3.5 w-3.5" />
                                Convertir en nota
                              </>
                            )}
                          </Button>
                        </CardContent>
                      </Card>
                    )
                  })}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Proyectos Registrados con Trazabilidad Continua */}
          <Card>
            <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <CardTitle>Fichas de proyectos registradas ({proyectosFiltrados.length})</CardTitle>
                <CardDescription>
                  Trazabilidad de cambios en disco, total de artefactos y fichas técnicas generadas en Obsidian.
                </CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => verificarEstados(proyectosFiltrados)}
                  disabled={verificandoEstados || proyectosFiltrados.length === 0}
                  className="gap-1.5"
                >
                  <RefreshCw className={`h-4 w-4 ${verificandoEstados ? 'animate-spin' : ''}`} />
                  {verificandoEstados ? 'Comprobando…' : 'Comprobar cambios'}
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              {proyectosFiltrados.length === 0 ? (
                <p className="text-sm text-slate-500 py-6 text-center">
                  No hay proyectos registrados para la asignatura seleccionada. Convierte uno desde la sección superior.
                </p>
              ) : (
                <div className="rounded-lg border border-slate-200 dark:border-slate-800">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Proyecto</TableHead>
                        <TableHead className="w-36">Asignatura</TableHead>
                        <TableHead className="w-28">Parcial</TableHead>
                        <TableHead className="w-36">Tipo</TableHead>
                        <TableHead className="w-32">Trazabilidad</TableHead>
                        <TableHead>Último análisis</TableHead>
                        <TableHead className="w-28 text-right">Acciones</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {proyectosFiltrados.map((p) => {
                        const tipoFmt = formatTipoProyecto(p.tipo)
                        const estado = estadosProyectos[p.id]
                        const estaActualizando = actualizandoProyectoId === p.id
                        const tieneCambios = estado?.estado === 'cambios_detectados'

                        return (
                          <TableRow key={p.id}>
                            <TableCell className="font-medium text-slate-900 dark:text-slate-100">
                              <div className="flex items-center gap-2">
                                {tipoFmt.icon}
                                <div>
                                  <div className="font-semibold">{p.nombre}</div>
                                  <div className="text-[11px] text-slate-400 font-mono truncate max-w-xs" title={p.ruta_nota_obsidian}>
                                    {p.ruta_nota_obsidian}
                                  </div>
                                </div>
                              </div>
                            </TableCell>

                            <TableCell>
                              <Badge variant="outline">{p.materia}</Badge>
                            </TableCell>

                            <TableCell className="text-xs text-slate-600 dark:text-slate-300">
                              {formatParcial(p.parcial)}
                            </TableCell>

                            <TableCell>
                              <Badge className={cn('text-[11px] border', tipoFmt.badgeClass)}>
                                {tipoFmt.label}
                              </Badge>
                              <div className="text-[10px] text-slate-400 mt-0.5">
                                {p.total_archivos} archivo{p.total_archivos === 1 ? '' : 's'}
                              </div>
                            </TableCell>

                            <TableCell>
                              {tieneCambios ? (
                                <Badge className="bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800 gap-1 text-[11px]">
                                  <AlertTriangle className="h-3 w-3" />
                                  Cambios detectados
                                </Badge>
                              ) : estado?.estado === 'carpeta_eliminada' ? (
                                <Badge variant="destructive" className="gap-1 text-[11px]">
                                  No encontrado
                                </Badge>
                              ) : (
                                <Badge className="bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800 gap-1 text-[11px]">
                                  <FileCheck2 className="h-3 w-3" />
                                  Al día
                                </Badge>
                              )}
                            </TableCell>

                            <TableCell className="text-xs text-slate-500">
                              <div className="flex items-center gap-1">
                                <Clock className="h-3 w-3 text-slate-400" />
                                <span>{formatearFecha(p.fecha_analisis)}</span>
                              </div>
                            </TableCell>

                            <TableCell className="text-right">
                              <div className="flex items-center justify-end gap-1">
                                <Button
                                  variant={tieneCambios ? 'default' : 'outline'}
                                  size="sm"
                                  disabled={estaActualizando}
                                  onClick={() => handleActualizarProyecto(p.id, p.nombre)}
                                  title="Re-analizar archivos y actualizar ficha en Obsidian"
                                  className={cn(
                                    'h-7 px-2 text-xs gap-1',
                                    tieneCambios ? 'bg-amber-600 hover:bg-amber-500 text-white' : ''
                                  )}
                                >
                                  <RefreshCw className={`h-3 w-3 ${estaActualizando ? 'animate-spin' : ''}`} />
                                  {estaActualizando ? 'Actualizando…' : 'Actualizar'}
                                </Button>

                                <Button
                                  variant="ghost"
                                  size="icon"
                                  onClick={() => handleEliminarProyecto(p.id, p.nombre)}
                                  title="Desvincular proyecto del registro"
                                  className="h-7 w-7 text-slate-400 hover:text-red-600"
                                >
                                  <Trash2 className="h-3.5 w-3.5" />
                                </Button>
                              </div>
                            </TableCell>
                          </TableRow>
                        )
                      })}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Zona peligrosa */}
      <div className="rounded-lg border border-rose-200 bg-rose-50/20 p-5 dark:border-rose-950 dark:bg-rose-950/10">
        <h3 className="text-sm font-semibold text-rose-900 dark:text-rose-200">
          Zona peligrosa
        </h3>
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
          Acciones destructivas que afectan al registro de documentos y notas en Obsidian.
        </p>
        <div className="mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={handleVaciarTodo}
            disabled={vaciando || isStreaming}
            className="gap-1.5 text-xs text-rose-600 border-rose-200 hover:bg-rose-50 dark:border-rose-900/60 dark:hover:bg-rose-950/40"
            title="Vacía de forma segura el registro y notas de Obsidian de Material, Actividades y Proyectos"
          >
            <Trash2 className={`h-4 w-4 ${vaciando ? 'animate-spin' : ''}`} />
            {vaciando ? 'Vaciando…' : 'Vaciar todo el material'}
          </Button>
        </div>
      </div>
    </div>
  )
}
