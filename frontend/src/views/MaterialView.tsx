import React, { useEffect, useState } from 'react'
import {
  CheckCircle2,
  FileUp,
  FolderSearch,
  Pause,
  Play,
  RotateCw,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type {
  EscaneoMaterial,
  IngestarResponse,
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
import { useEventStream } from '@/hooks/useEventStream'

export function MaterialView() {
  const [materias, setMaterias] = useState<string[]>([])
  const [materiaSeleccionada, setMateriaSeleccionada] = useState<string>('__todas__')
  const [escaneos, setEscaneos] = useState<EscaneoMaterial[]>([])
  const [escaneando, setEscaneando] = useState(false)

  // Subida individual
  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const [uploadMateria, setUploadMateria] = useState('')
  const [uploadTipo, setUploadTipo] = useState('material_complementario')
  const [subiendo, setSubiendo] = useState(false)
  const [resultadoSubida, setResultadoSubida] = useState<IngestarResponse | null>(null)

  // Stream de sincronización en tiempo real
  const [streamProgress, setStreamProgress] = useState<{
    total: number
    hecho: number
    archivoActual: string
    exitosos: number
    fallidos: number
  }>({
    total: 0,
    hecho: 0,
    archivoActual: '',
    exitosos: 0,
    fallidos: 0,
  })

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
        }))
      } else if (ev.evento === 'archivo') {
        setStreamProgress((prev) => ({
          ...prev,
          hecho: ev.indice || prev.hecho + 1,
          archivoActual: ev.archivo || '',
          exitosos: ev.ok ? prev.exitosos + 1 : prev.exitosos,
          fallidos: !ev.ok ? prev.fallidos + 1 : prev.fallidos,
        }))
      } else if (ev.evento === 'fin') {
        toast.success('¡Sincronización finalizada!', {
          description: `Completados con éxito: ${ev.exitosos || 0}, Fallidos: ${ev.fallidos || 0}`,
        })
        handleEscanear()
      }
    },
    onError: (err) => {
      toast.error('Error durante la sincronización', {
        description: err.message,
      })
    },
  })

  useEffect(() => {
    api
      .getMaterias()
      .then((res) => {
        setMaterias(res.materias)
        if (res.materias.length > 0) {
          setUploadMateria((prev) => prev || res.materias[0])
        }
      })
      .catch((err) => console.error(err))
  }, [])

  const handleEscanear = async () => {
    try {
      setEscaneando(true)
      const res = await api.escanearMaterial(
        materiaSeleccionada === '__todas__' ? undefined : materiaSeleccionada
      )
      setEscaneos(res.escaneos)
      const totalPendientes = res.escaneos.reduce((acc, e) => acc + e.pendientes.length, 0)
      toast.info('Escaneo finalizado', {
        description: `Se encontraron ${totalPendientes} archivos nuevos pendientes de ingesta.`,
      })
    } catch (err) {
      toast.error('Error al escanear carpetas de material', {
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
    })
    startStream({ materia: materiaSeleccionada })
  }

  const handleUploadIndividual = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!uploadFile) {
      toast.error('Selecciona un archivo para subir.')
      return
    }
    if (!uploadMateria.trim()) {
      toast.error('Indica la asignatura.')
      return
    }

    try {
      setSubiendo(true)
      const res = await api.ingestarArchivo(uploadFile, uploadMateria.trim(), uploadTipo)
      setResultadoSubida(res)
      toast.success('¡Material ingestado y anonimizado con éxito!', {
        description: `Asignado a Clase ${res.alineacion?.clase_asignada || 'X'} (Afinidad: ${
          res.alineacion?.peso_afinidad || 0
        }%)`,
      })
      setUploadFile(null)
    } catch (err) {
      toast.error('Error al ingestar material', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setSubiendo(false)
    }
  }

  const totalPendientes = escaneos.reduce((acc, e) => acc + e.pendientes.length, 0)
  const pctSincronizacion =
    streamProgress.total > 0
      ? Math.round((streamProgress.hecho / streamProgress.total) * 100)
      : 0

  return (
    <div className="space-y-8 pb-12">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          Gestión e Ingesta Multimodal de Material
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Escanea directorios locales, anonimiza documentos y sincroniza notas con Obsidian en tiempo real.
        </p>
      </div>

      {/* Barra de Controles y Escaneo */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <CardTitle>Escaneo y Sincronización en Tiempo Real</CardTitle>
              <CardDescription>
                Detecta automáticamente diapositivas, lecturas y actividades pendientes en tu carpeta de estudio.
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <select
                value={materiaSeleccionada}
                onChange={(e) => setMateriaSeleccionada(e.target.value)}
                className="h-9 rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
              >
                <option value="__todas__">✨ Todas las Asignaturas</option>
                {materias.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
              <Button
                variant="outline"
                size="sm"
                onClick={handleEscanear}
                disabled={escaneando || isStreaming}
                className="gap-1.5"
              >
                <FolderSearch className={`h-4 w-4 ${escaneando ? 'animate-spin' : ''}`} />
                {escaneando ? 'Escaneando...' : 'Escanear'}
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
                  <Play className="h-4 w-4" /> Sincronizar Pendientes
                </Button>
              )}
            </div>
          </div>
        </CardHeader>

        {/* Panel de progreso de streaming si está activo o hubo eventos */}
        {(isStreaming || events.length > 0) && (
          <CardContent className="border-t border-slate-100 dark:border-slate-800 pt-6 space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-medium">
                <span className="flex items-center gap-2 text-indigo-600">
                  <RotateCw className={`h-3.5 w-3.5 ${isStreaming ? 'animate-spin' : ''}`} />
                  {isStreaming ? 'Sincronizando archivos...' : 'Sincronización pausada o finalizada'}
                </span>
                <span className="text-slate-500">
                  {streamProgress.hecho} / {streamProgress.total} ({pctSincronizacion}%)
                </span>
              </div>
              <Progress value={pctSincronizacion} className="h-2.5" />
              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span className="truncate max-w-[400px]">
                  Archivo actual: <strong className="text-slate-600 dark:text-slate-300">{streamProgress.archivoActual || 'En cola'}</strong>
                </span>
                <span>
                  Éxitos: <strong className="text-emerald-600">{streamProgress.exitosos}</strong> | Fallidos:{' '}
                  <strong className="text-red-500">{streamProgress.fallidos}</strong>
                </span>
              </div>
            </div>

            {/* Log de eventos SSE */}
            <div className="max-h-48 overflow-y-auto rounded-md border border-slate-200 bg-slate-900 p-3 font-mono text-[11px] text-slate-300 dark:border-slate-800">
              {events.map((ev, idx) => (
                <div key={idx} className="leading-relaxed">
                  {ev.evento === 'inicio' && (
                    <span className="text-indigo-400">
                      [INICIO] Iniciando lote de {ev.total} archivo(s)...
                    </span>
                  )}
                  {ev.evento === 'archivo' && ev.ok && (
                    <span className="text-emerald-400">
                      [OK] {ev.archivo} → Clase {ev.clase_asignada ?? 'X'} ({ev.afinidad ?? 0}% afinidad)
                    </span>
                  )}
                  {ev.evento === 'archivo' && !ev.ok && (
                    <span className="text-red-400">
                      [ERROR] {ev.archivo}: {ev.error}
                    </span>
                  )}
                  {ev.evento === 'fin' && (
                    <span className="text-cyan-400">
                      [FIN] Proceso completado. Exitosos: {ev.exitosos}, Fallidos: {ev.fallidos}, Omitidos: {ev.omitidos}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        )}
      </Card>

      {/* Resultados del Escaneo */}
      {escaneos.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold tracking-tight text-slate-900 dark:text-white">
            Resultados del Escaneo por Asignatura
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {escaneos.map((esc, i) => (
              <Card key={i} className={!esc.existe ? 'border-dashed opacity-75' : ''}>
                <CardHeader className="p-4 pb-2">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-sm font-semibold">{esc.materia}</CardTitle>
                    <Badge variant={esc.existe ? 'secondary' : 'destructive'}>
                      {esc.existe ? `${esc.pendientes.length} nuevos` : 'Carpeta no hallada'}
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
                    <span>No soportados (ej. .pptx):</span>
                    <strong className="text-amber-600">{esc.no_soportados}</strong>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Subida Individual y Anonimización */}
      <Card>
        <CardHeader>
          <CardTitle>Subida y Procesamiento Individual</CardTitle>
          <CardDescription>
            Sube un archivo puntual para extraer su conocimiento, aplicar filtros de privacidad y alinearlo al cronograma.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUploadIndividual} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                  Asignatura
                </label>
                <Input
                  value={uploadMateria}
                  onChange={(e) => setUploadMateria(e.target.value)}
                  placeholder="Ej. Programacion Web"
                  className="mt-1"
                  required
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                  Tipo de Material
                </label>
                <select
                  value={uploadTipo}
                  onChange={(e) => setUploadTipo(e.target.value)}
                  className="mt-1 h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                >
                  <option value="material_complementario">Material Complementario</option>
                  <option value="actividad">Actividad / Práctica</option>
                  <option value="diapositiva">Diapositiva de Clase</option>
                  <option value="lectura">Lectura / Artículo</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                  Archivo (.pdf, .docx, .txt, .md)
                </label>
                <Input
                  type="file"
                  accept=".pdf,.docx,.txt,.md"
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
                  Anonimizando y Alineando con IA...
                </>
              ) : (
                <>
                  <FileUp className="h-4 w-4" /> Ingestar Documento Individual
                </>
              )}
            </Button>
          </form>

          {/* Resultado de la Subida */}
          {resultadoSubida && (
            <div className="mt-6 rounded-lg border border-emerald-200 bg-emerald-50/50 p-4 dark:border-emerald-900 dark:bg-emerald-950/20">
              <div className="flex items-center gap-2 text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                <CheckCircle2 className="h-4 w-4" />
                Material Ingestado: {resultadoSubida.archivo}
              </div>
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
    </div>
  )
}
