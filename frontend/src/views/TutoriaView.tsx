import React, { useEffect, useState } from 'react'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Calendar,
  CheckCircle2,
  Clock,
  HelpCircle,
  Lightbulb,
  RotateCw,
  Send,
  Sparkles,
  Target,
} from 'lucide-react'
import { useSearchParams } from 'react-router-dom'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type {
  ClaseCronograma,
  FinalizarTutoriaResponse,
  SesionTutoriaResponse,
} from '@/api/types'
import { Markdown } from '@/components/Markdown'
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
import { useEventStream } from '@/hooks/useEventStream'
import { clave } from '@/lib/asignaturas'

/** Línea discreta con la pregunta fallada que motiva la sesión de refuerzo. */
function Reforzando({ enfoque, onQuitar }: { enfoque: string; onQuitar?: () => void }) {
  return (
    <p className="flex min-w-0 items-start gap-2 text-sm text-slate-600 dark:text-slate-400">
      <Target className="mt-0.5 h-3.5 w-3.5 shrink-0 text-indigo-600 dark:text-indigo-400" />
      <span className="min-w-0">
        <span className="font-display italic text-slate-500">Reforzando:</span>{' '}
        <span className="break-words text-slate-800 dark:text-slate-200">{enfoque}</span>
        {onQuitar && (
          <button
            type="button"
            onClick={onQuitar}
            className="ml-2 cursor-pointer text-xs text-slate-500 underline underline-offset-4 hover:text-slate-800 dark:hover:text-slate-200"
          >
            quitar
          </button>
        )}
      </span>
    </p>
  )
}

interface DudaChat {
  duda: string
  respuesta: string
}

export function TutoriaView() {
  const [params] = useSearchParams()
  const materiaInicial = params.get('materia') || ''

  // Estado de configuración previa
  const [materias, setMaterias] = useState<string[]>([])
  const [materia, setMateria] = useState(materiaInicial)
  const [nivel, setNivel] = useState('INTERMEDIO')
  const [tema, setTema] = useState(params.get('tema') || '')
  const [enfoque, setEnfoque] = useState(params.get('enfoque') || '')
  const [claseId, setClaseId] = useState<string | undefined>(params.get('clase_id') || undefined)
  const [clasesPendientes, setClasesPendientes] = useState<ClaseCronograma[]>([])
  const [cargandoClases, setCargandoClases] = useState(false)
  const [iniciando, setIniciando] = useState(false)

  // Estado de sesión activa
  const [sesion, setSesion] = useState<SesionTutoriaResponse | null>(null)
  const [pasoActual, setPasoActual] = useState(0)
  const [explicaciones, setExplicaciones] = useState<Record<number, string>>({})
  const [pasosCompletados, setPasosCompletados] = useState<Set<number>>(new Set())

  // Dudas inline por paso
  const [dudasPorPaso, setDudasPorPaso] = useState<Record<number, DudaChat[]>>({})
  const [dudaInput, setDudaInput] = useState('')
  const [enviandoDuda, setEnviandoDuda] = useState(false)

  // Finalización
  const [finalizando, setFinalizando] = useState(false)
  const [resumenFinal, setResumenFinal] = useState<FinalizarTutoriaResponse | null>(null)

  // Cargar catálogo de materias al montar
  useEffect(() => {
    api
      .getMaterias()
      .then((res) => {
        setMaterias(res.materias)
        // El enlace puede traer el nombre derivado del cronograma: se cruza con el catálogo
        const enCatalogo = res.materias.find((m) => clave(m) === clave(materiaInicial))
        if (enCatalogo) setMateria(enCatalogo)
        else if (res.materias.length > 0) setMateria(res.materias[0])
      })
      .catch((err) => console.error(err))
  }, [materiaInicial])

  // Cargar clases pendientes cuando cambia la materia
  useEffect(() => {
    if (!materia) return
    let active = true
    const cargar = async () => {
      setCargandoClases(true)
      try {
        const res = await api.getProximasClases(materia)
        if (active) setClasesPendientes(res.clases)
      } catch (err) {
        console.error(err)
      } finally {
        if (active) setCargandoClases(false)
      }
    }
    cargar()
    return () => {
      active = false
    }
  }, [materia])

  // Hook SSE para streaming de explicación de paso
  const streamUrl = sesion
    ? `/api/tutoria/${encodeURIComponent(sesion.sesion_id)}/paso/${pasoActual}/stream`
    : ''

  const { isStreaming, startStream, stopStream } = useEventStream<{ chunk?: string }>({
    url: streamUrl,
    method: 'GET',
    onMessage: (ev) => {
      if (ev.chunk) {
        setExplicaciones((prev) => ({
          ...prev,
          [pasoActual]: (prev[pasoActual] || '') + ev.chunk,
        }))
      }
    },
    onEnd: () => {
      setPasosCompletados((prev) => new Set(prev).add(pasoActual))
    },
    onError: (err) => {
      toast.error('Se cortó la explicación', { description: err.message })
    },
  })

  // Lanzar stream cuando se avanza a un paso que aún no tiene explicación
  useEffect(() => {
    if (sesion && !explicaciones[pasoActual] && !isStreaming) {
      startStream()
    }
  }, [sesion, pasoActual, explicaciones, isStreaming, startStream])

  const handleIniciar = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!materia.trim() || !tema.trim()) {
      toast.error('Elige una asignatura y escribe qué quieres estudiar.')
      return
    }

    try {
      setIniciando(true)
      const res = await api.iniciarTutoria({
        materia: materia.trim(),
        tema: tema.trim(),
        clase_id: claseId,
        nivel_profundidad: nivel,
        enfoque: enfoque.trim() || undefined,
      })
      setSesion(res)
      setPasoActual(0)
      setExplicaciones({})
      setPasosCompletados(new Set())
      setDudasPorPaso({})
      setResumenFinal(null)
      toast.success('Tu ruta de estudio está lista', {
        description: `Roadmap estructurado en ${res.pasos.length} pasos para dominar "${res.tema}".`,
      })
    } catch (err) {
      toast.error('No pude preparar la sesión', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setIniciando(false)
    }
  }

  const handleEnviarDuda = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!sesion || !dudaInput.trim()) return

    const textoDuda = dudaInput.trim()
    setDudaInput('')
    setEnviandoDuda(true)

    try {
      const res = await api.resolverDuda(sesion.sesion_id, {
        paso: pasoActual,
        duda: textoDuda,
      })
      setDudasPorPaso((prev) => ({
        ...prev,
        [pasoActual]: [
          ...(prev[pasoActual] || []),
          { duda: textoDuda, respuesta: res.respuesta },
        ],
      }))
    } catch (err) {
      toast.error('No pude responder tu duda', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setEnviandoDuda(false)
    }
  }

  const handleFinalizar = async () => {
    if (!sesion) return
    try {
      setFinalizando(true)
      stopStream()
      const res = await api.finalizarTutoria(sesion.sesion_id)
      setResumenFinal(res)
      toast.success('Sesión guardada', {
        description: res.guardado_obsidian
          ? 'La guía de repaso ya está en tu bóveda de Obsidian.'
          : 'Sesión completada.',
      })
    } catch (err) {
      toast.error('No pude guardar la sesión', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setFinalizando(false)
    }
  }

  // ------------------------- VISTA FINALIZADA -------------------------
  if (resumenFinal && sesion) {
    return (
      <div className="space-y-6 pb-12 max-w-4xl mx-auto">
        <Card className="border-emerald-200/80 bg-white dark:border-emerald-950 dark:bg-slate-900 shadow-sm">
          <CardHeader className="text-center p-8 pb-4">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400">
              <CheckCircle2 className="h-8 w-8" />
            </div>
            <CardTitle className="mt-4 text-2xl font-bold">Clase terminada</CardTitle>
            <CardDescription className="text-sm">
              Terminaste <strong className="text-slate-800 dark:text-slate-200">{sesion.tema}</strong> en{' '}
              <span className="text-indigo-600">{sesion.materia}</span>.
            </CardDescription>
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              <Badge variant="success">Marcada como completada</Badge>
              {resumenFinal.guardado_obsidian && (
                <Badge variant="secondary">Guardada en Obsidian</Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="p-8 pt-4 space-y-6">
            <div>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-2">
                Tu guía de repaso
              </h3>
              <div className="rounded-xl border border-slate-200 bg-slate-50/70 p-6 dark:border-slate-800 dark:bg-slate-950/60">
                <Markdown>{resumenFinal.guia}</Markdown>
              </div>
            </div>

            <div className="flex justify-center gap-3 pt-2">
              <Button
                variant="outline"
                onClick={() => {
                  setSesion(null)
                  setResumenFinal(null)
                  setTema('')
                  setEnfoque('')
                }}
              >
                Estudiar otro tema
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // ------------------------- VISTA SESIÓN ACTIVA -------------------------
  if (sesion) {
    const pasoActualObj = sesion.pasos[pasoActual] || { titulo: 'Paso', descripcion: '' }
    const explicacionTexto = explicaciones[pasoActual] || ''
    const dudasActuales = dudasPorPaso[pasoActual] || []

    return (
      <div className="space-y-6 pb-12">
        {/* Cabecera de la sesión */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4 dark:border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
                {sesion.materia}
              </span>
              <span className="text-slate-300">•</span>
              <Badge variant="secondary">{sesion.nivel_profundidad}</Badge>
            </div>
            <h1 className="mt-1 text-3xl font-semibold text-slate-900 dark:text-white">
              {sesion.tema}
            </h1>
            {sesion.enfoque && (
              <div className="mt-2">
                <Reforzando enfoque={sesion.enfoque} />
              </div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                if (confirm('¿Salir de la sesión? Lo que llevas de esta clase no se guardará.')) {
                  setSesion(null)
                }
              }}
              className="text-xs text-slate-500"
            >
              Salir
            </Button>
            <Button
              size="sm"
              onClick={handleFinalizar}
              disabled={finalizando}
              className="bg-emerald-600 hover:bg-emerald-500 text-white gap-1.5 text-xs shadow-sm"
            >
              {finalizando ? (
                <>
                  <div className="h-3 w-3 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  Guardando…
                </>
              ) : (
                <>
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  Terminar y guardar
                </>
              )}
            </Button>
          </div>
        </div>

        {/* Layout en dos columnas: Stepper lateral + Explicación activa */}
        <div className="grid gap-6 lg:grid-cols-12">
          {/* Stepper lateral */}
          <div className="lg:col-span-4 space-y-4">
            <Card>
              <CardHeader className="p-4 pb-2 border-b border-slate-100 dark:border-slate-800">
                <CardTitle className="text-xs font-semibold uppercase tracking-wider text-slate-500 flex items-center justify-between">
                  <span>Ruta</span>
                  <span>
                    {pasoActual + 1} de {sesion.pasos.length}
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent className="p-2 space-y-1">
                {sesion.pasos.map((p, idx) => {
                  const isCurrent = idx === pasoActual
                  const isDone = pasosCompletados.has(idx)

                  return (
                    <button
                      key={idx}
                      onClick={() => {
                        stopStream()
                        setPasoActual(idx)
                      }}
                      className={`w-full text-left p-3 rounded-lg transition-all flex items-start gap-3 cursor-pointer ${
                        isCurrent
                          ? 'bg-indigo-50/80 border border-indigo-200/80 dark:bg-indigo-950/40 dark:border-indigo-800/60'
                          : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'
                      }`}
                    >
                      <div
                        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold ${
                          isDone
                            ? 'bg-emerald-500 text-white'
                            : isCurrent
                            ? 'bg-indigo-600 text-white shadow-sm'
                            : 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                        }`}
                      >
                        {isDone ? <CheckCircle2 className="h-4 w-4" /> : idx + 1}
                      </div>
                      <div className="min-w-0 flex-1">
                        <p
                          className={`text-xs font-medium truncate ${
                            isCurrent
                              ? 'text-indigo-950 dark:text-indigo-200 font-semibold'
                              : 'text-slate-700 dark:text-slate-300'
                          }`}
                        >
                          {p.titulo}
                        </p>
                        <p className="text-[11px] text-slate-400 line-clamp-1 mt-0.5">
                          {p.descripcion}
                        </p>
                      </div>
                    </button>
                  )
                })}
              </CardContent>
            </Card>

            {/* Subtemas adicionales asociados */}
            {(sesion.subtemas_adicionales?.length > 0 || sesion.materiales_asociados?.length > 0) && (
              <Card className="p-4 space-y-2 text-xs">
                <p className="font-semibold text-slate-600 dark:text-slate-300 flex items-center gap-1.5">
                  <Lightbulb className="h-3.5 w-3.5 text-amber-500" />
                  De tus apuntes
                </p>
                {sesion.subtemas_adicionales?.length > 0 && (
                  <p className="text-slate-500 text-[11px]">
                    Subtemas: {sesion.subtemas_adicionales.join(', ')}
                  </p>
                )}
                {sesion.materiales_asociados?.length > 0 && (
                  <p className="text-slate-400 text-[10px]">
                    Materiales: {sesion.materiales_asociados.join(', ')}
                  </p>
                )}
              </Card>
            )}
          </div>

          {/* Área principal de explicación y dudas */}
          <div className="lg:col-span-8 space-y-6">
            <Card className="shadow-sm">
              <CardHeader className="border-b border-slate-100 p-6 pb-4 dark:border-slate-800">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-indigo-600 uppercase tracking-wider">
                    Paso {pasoActual + 1} de {sesion.pasos.length}
                  </span>
                  {isStreaming && (
                    <Badge variant="secondary" className="gap-1.5 text-indigo-600 animate-pulse">
                      <RotateCw className="h-3 w-3 animate-spin" /> Escribiendo…
                    </Badge>
                  )}
                </div>
                <CardTitle className="text-xl font-bold mt-1 text-slate-900 dark:text-white">
                  {pasoActualObj.titulo}
                </CardTitle>
                <CardDescription className="text-xs text-slate-500">
                  {pasoActualObj.descripcion}
                </CardDescription>
              </CardHeader>

              <CardContent className="p-6">
                {/* Explicación en Markdown con fórmulas LaTeX */}
                <div>
                  {explicacionTexto ? (
                    <Markdown>{explicacionTexto}</Markdown>
                  ) : (
                    <div className="flex h-36 items-center justify-center text-slate-400 gap-2">
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-indigo-600 border-t-transparent" />
                      <span>El tutor está preparando la explicación…</span>
                    </div>
                  )}
                </div>

                {/* Controles de avance */}
                <div className="mt-8 flex items-center justify-between border-t border-slate-100 pt-4 dark:border-slate-800">
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={pasoActual === 0}
                    onClick={() => setPasoActual((p) => p - 1)}
                    className="gap-1.5 text-xs"
                  >
                    <ArrowLeft className="h-3.5 w-3.5" /> Anterior
                  </Button>
                  {pasoActual < sesion.pasos.length - 1 ? (
                    <Button
                      size="sm"
                      onClick={() => setPasoActual((p) => p + 1)}
                      className="gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs"
                    >
                      Siguiente paso <ArrowRight className="h-3.5 w-3.5" />
                    </Button>
                  ) : (
                    <Button
                      size="sm"
                      onClick={handleFinalizar}
                      disabled={finalizando}
                      className="gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs"
                    >
                      Finalizar tutoría <CheckCircle2 className="h-3.5 w-3.5" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Resolución de Dudas Inline */}
            <Card className="border-indigo-100 dark:border-indigo-950 shadow-sm">
              <CardHeader className="p-4 pb-2 border-b border-slate-100 dark:border-slate-800">
                <CardTitle className="text-sm font-semibold flex items-center gap-2">
                  <HelpCircle className="h-4 w-4 text-indigo-500" />
                  ¿Dudas sobre este paso?
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 space-y-4">
                {/* Historial de dudas */}
                {dudasActuales.length > 0 && (
                  <div className="space-y-3">
                    {dudasActuales.map((d, i) => (
                      <div key={i} className="space-y-2 rounded-lg bg-slate-50 p-3 text-xs dark:bg-slate-800/40">
                        <div className="flex items-start gap-2 text-indigo-900 dark:text-indigo-200 font-medium">
                          <span className="font-bold">Pregunta:</span> {d.duda}
                        </div>
                        <div className="border-l-2 border-indigo-400 pl-3">
                          <Markdown className="text-[0.85rem]">{d.respuesta}</Markdown>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Formulario para enviar duda */}
                <form onSubmit={handleEnviarDuda} className="flex gap-2">
                  <Input
                    value={dudaInput}
                    onChange={(e) => setDudaInput(e.target.value)}
                    placeholder="Pregunta lo que no te quedó claro…"
                    className="text-xs"
                    disabled={enviandoDuda}
                  />
                  <Button
                    type="submit"
                    disabled={!dudaInput.trim() || enviandoDuda}
                    size="sm"
                    className="gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs shrink-0"
                  >
                    {enviandoDuda ? (
                      <div className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    ) : (
                      <Send className="h-3.5 w-3.5" />
                    )}
                    Preguntar
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  // ------------------------- VISTA CONFIGURACIÓN INICIAL -------------------------
  return (
    <div className="space-y-8 pb-12 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
          Tutoría
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Elige un tema y el tutor te lo explica paso a paso, apoyándose en tus apuntes.
        </p>
      </div>

      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>Qué vas a estudiar</CardTitle>
          <CardDescription>
            Toma una clase pendiente o escribe cualquier tema.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleIniciar} className="space-y-6">
            {enfoque && <Reforzando enfoque={enfoque} onQuitar={() => setEnfoque('')} />}

            {/* Selector de Asignatura y Nivel */}
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Asignatura
                </label>
                <select
                  value={materia}
                  onChange={(e) => { setMateria(e.target.value); setClaseId(undefined); }}
                  className="mt-1 h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                >
                  {materias.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Profundidad
                </label>
                <select
                  value={nivel}
                  onChange={(e) => setNivel(e.target.value)}
                  className="mt-1 h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                >
                  <option value="BÁSICO">Básica: conceptos y visión general</option>
                  <option value="INTERMEDIO">Intermedia: detalle técnico y ejemplos</option>
                  <option value="AVANZADO">Avanzada: casos límite y optimización</option>
                </select>
              </div>
            </div>

            {/* Píldoras de clases pendientes del cronograma con buen espaciado vertical */}
            <div className="space-y-3">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <Calendar className="h-3.5 w-3.5 text-indigo-500" />
                Clases pendientes
              </label>

              {cargandoClases ? (
                <p className="text-xs text-slate-400 py-2">Consultando cronograma...</p>
              ) : clasesPendientes.length > 0 ? (
                <div className="flex flex-wrap gap-2.5 pt-1 pb-1">
                  {clasesPendientes.map((clase, idx) => (
                    <button
                      type="button"
                      key={idx}
                      onClick={() => { setTema(clase.tema); setClaseId(clase.id); }}
                      className="flex cursor-pointer items-center gap-1.5 rounded-full border border-slate-300 bg-transparent px-3 py-1 text-xs text-slate-700 transition-colors hover:border-indigo-400 hover:bg-indigo-50 hover:text-indigo-800 dark:border-slate-700 dark:text-slate-300 dark:hover:border-indigo-500 dark:hover:bg-indigo-950/50 dark:hover:text-indigo-200"
                    >
                      <Clock className="h-3 w-3 text-indigo-600 dark:text-indigo-400" />
                      <span>{clase.tema}</span>
                      {clase.semana && (
                        <span className="text-[10px] text-slate-500">(Sem. {clase.semana})</span>
                      )}
                    </button>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400 italic py-1">
                  Esta asignatura no tiene clases pendientes. Escribe el tema que quieras.
                </p>
              )}
            </div>

            {/* Tema de estudio */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <BookOpen className="h-3.5 w-3.5 text-indigo-500" />
                Tema
              </label>
              <Input
                value={tema}
                onChange={(e) => { setTema(e.target.value); setClaseId(undefined); }}
                placeholder="Ej. Enrutamiento BGP"
                className="text-xs"
                required
              />
              <p className="text-[11px] text-slate-400">
                Puede ser cualquier tema, aunque no esté en el sílabo.
              </p>
            </div>

            {/* Botón primario sólido en color índigo/azul sobrio */}
            <div className="pt-2">
              <Button
                type="submit"
                disabled={iniciando || !tema.trim()}
                className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2.5 rounded-lg shadow-sm gap-2 text-sm transition-colors cursor-pointer"
              >
                {iniciando ? (
                  <>
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Preparando la ruta…
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    Empezar
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
