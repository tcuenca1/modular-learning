import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  AlertCircle,
  ArrowLeft,
  ArrowRight,
  Award,
  Brain,
  CheckCircle2,
  HelpCircle,
  RotateCw,
  XCircle,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { DetalleEvaluacion, PreguntaQuiz, ResumenRepaso } from '@/api/types'
import { Markdown, TextoConFormulas } from '@/components/Markdown'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { enlaceTutoria } from '@/lib/asignaturas'

type Modo = 'nuevas' | 'vencidas'

export function QuizView() {
  const navigate = useNavigate()
  const [generando, setGenerando] = useState<Modo | null>(null)
  const [evaluando, setEvaluando] = useState(false)
  const [quizId, setQuizId] = useState<string | null>(null)
  const [preguntas, setPreguntas] = useState<PreguntaQuiz[]>([])
  const [respuestasUsuario, setRespuestasUsuario] = useState<Record<number, string>>({})
  const [preguntaActual, setPreguntaActual] = useState(0)
  const [errorMensaje, setErrorMensaje] = useState<string | null>(null)

  // Resultado tras evaluar
  const [resultado, setResultado] = useState<{
    aciertos: number
    total: number
    porcentaje: number
    detalle: DetalleEvaluacion[]
  } | null>(null)

  // Preguntas vencidas según el repaso espaciado
  const [resumen, setResumen] = useState<ResumenRepaso | null>(null)

  const cargarResumen = () => {
    api
      .getResumenRepaso()
      .then(setResumen)
      .catch(() => setResumen(null))
  }

  useEffect(cargarResumen, [])

  const handleGenerarQuiz = async (modo: Modo = 'nuevas') => {
    try {
      setGenerando(modo)
      setErrorMensaje(null)
      setResultado(null)
      setRespuestasUsuario({})
      setPreguntaActual(0)

      const res = modo === 'vencidas' ? await api.repasoPendiente() : await api.generarQuiz()
      setQuizId(res.quiz_id)
      setPreguntas(res.preguntas)
      toast.success('Repaso listo', {
        description:
          modo === 'vencidas'
            ? `${res.preguntas.length} preguntas que tocaba volver a ver hoy.`
            : `${res.preguntas.length} preguntas sobre lo que ya estudiaste.`,
      })
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      setErrorMensaje(msg)
      toast.error('No pude preparar el repaso', { description: msg })
    } finally {
      setGenerando(null)
    }
  }

  const handleSeleccionarOpcion = (opcion: string) => {
    setRespuestasUsuario((prev) => ({
      ...prev,
      [preguntaActual]: opcion,
    }))
  }

  const handleEnviarQuiz = async () => {
    if (!quizId) return

    // Convertir diccionario a array ordenado según las preguntas
    const respuestasArray = preguntas.map((_, idx) => respuestasUsuario[idx] || '')

    const sinResponder = respuestasArray.filter((r) => !r.trim()).length
    if (sinResponder > 0) {
      const confirmar = confirm(
        `Te faltan ${sinResponder} por responder. ¿Corregir de todos modos?`
      )
      if (!confirmar) return
    }

    try {
      setEvaluando(true)
      const res = await api.evaluarQuiz({
        quiz_id: quizId,
        respuestas: respuestasArray,
      })
      setResultado(res)
      cargarResumen()
      toast.success('Repaso corregido', {
        description: `Acertaste ${res.aciertos} de ${res.total}.`,
      })
    } catch (err) {
      toast.error('No pude corregir tus respuestas', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setEvaluando(false)
    }
  }

  // ------------------------- ESTADO 1: RESUMEN DE RESULTADOS -------------------------
  if (resultado) {
    const esAprobado = resultado.porcentaje >= 60
    const esExcelente = resultado.porcentaje >= 80
    // Enlace a una tutoría centrada en la pregunta fallada
    const refuerzo = (idx: number) => {
      const det = resultado.detalle[idx]
      const materia = det?.materia || preguntas[idx]?.materia
      if (!materia) return null
      return enlaceTutoria(materia, det?.tema || preguntas[idx]?.tema, preguntas[idx]?.enunciado)
    }
    const primeraFallada = resultado.detalle.findIndex((d) => !d.correcto)
    const enlaceRefuerzo = primeraFallada >= 0 ? refuerzo(primeraFallada) : null

    return (
      <div className="space-y-6 pb-12 max-w-4xl mx-auto">
        <Card className="shadow-sm border-slate-200 dark:border-slate-800">
          <CardHeader className="text-center p-8 pb-4">
            <div
              className={`mx-auto flex h-16 w-16 items-center justify-center rounded-full ${
                esExcelente
                  ? 'bg-amber-50 text-amber-600 dark:bg-amber-950/60 dark:text-amber-400'
                  : esAprobado
                  ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/60 dark:text-emerald-400'
                  : 'bg-rose-50 text-rose-600 dark:bg-rose-950/60 dark:text-rose-400'
              }`}
            >
              {esExcelente ? (
                <Award className="h-9 w-9" />
              ) : esAprobado ? (
                <CheckCircle2 className="h-9 w-9" />
              ) : (
                <AlertCircle className="h-9 w-9" />
              )}
            </div>

            <CardTitle className="mt-4 text-2xl font-bold">
              {esExcelente
                ? 'Lo tienes dominado'
                : esAprobado
                ? 'Vas bien'
                : 'Toca repasar'}
            </CardTitle>
            <CardDescription className="text-sm">
              Has respondido correctamente{' '}
              <strong className="text-slate-900 dark:text-white font-semibold">
                {resultado.aciertos}
              </strong>{' '}
              de{' '}
              <strong className="text-slate-900 dark:text-white font-semibold">
                {resultado.total}
              </strong>{' '}
              preguntas.
            </CardDescription>

            <div className="mt-4 flex justify-center items-center gap-3">
              <Badge
                variant={esExcelente ? 'default' : esAprobado ? 'success' : 'destructive'}
                className="text-sm px-3 py-1 font-semibold"
              >
                Puntaje: {resultado.porcentaje}%
              </Badge>
              <Badge variant="secondary">
                {esAprobado ? 'Aprobado' : 'Por reforzar'}
              </Badge>
            </div>
          </CardHeader>

          <CardContent className="p-8 pt-2 space-y-6">
            <div className="space-y-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                Pregunta por pregunta
              </h3>

              {preguntas.map((p, idx) => {
                const det = resultado.detalle[idx]
                const esCorrecta = det?.correcto ?? false
                const elegida = det?.elegida || '(Sin responder)'
                const correcta = det?.respuesta_correcta || ''
                const clase = [det?.materia || p.materia, det?.tema || p.tema].filter(Boolean)
                const enlace = esCorrecta ? null : refuerzo(idx)

                return (
                  <div
                    key={idx}
                    className={`rounded-xl border p-5 text-sm transition-all ${
                      esCorrecta
                        ? 'border-emerald-200 bg-emerald-50/40 dark:border-emerald-950 dark:bg-emerald-950/20'
                        : 'border-rose-200 bg-rose-50/40 dark:border-rose-950 dark:bg-rose-950/20'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-bold bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                          {idx + 1}
                        </span>
                        <p className="font-semibold text-slate-900 dark:text-white">
                          <TextoConFormulas>{p.enunciado}</TextoConFormulas>
                        </p>
                      </div>
                      <div className="shrink-0">
                        {esCorrecta ? (
                          <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                            <CheckCircle2 className="h-4 w-4" /> Correcto
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-xs font-semibold text-rose-600 dark:text-rose-400">
                            <XCircle className="h-4 w-4" /> Incorrecto
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="mt-4 grid gap-2 sm:grid-cols-2 text-xs">
                      <div
                        className={`rounded-lg p-3 border ${
                          esCorrecta
                            ? 'border-emerald-300/60 bg-emerald-100/50 dark:border-emerald-900 dark:bg-emerald-950/40'
                            : 'border-rose-300/60 bg-rose-100/50 dark:border-rose-900 dark:bg-rose-950/40'
                        }`}
                      >
                        <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 mb-1">
                          Tu respuesta
                        </p>
                        <p className="font-medium text-slate-800 dark:text-slate-200">
                          <TextoConFormulas>{elegida}</TextoConFormulas>
                        </p>
                      </div>

                      <div className="rounded-lg p-3 border border-emerald-300/60 bg-emerald-100/50 dark:border-emerald-900 dark:bg-emerald-950/40">
                        <p className="text-[11px] font-semibold uppercase tracking-wider text-emerald-700 dark:text-emerald-400 mb-1">
                          Respuesta correcta
                        </p>
                        <p className="font-medium text-slate-800 dark:text-slate-200">
                          <TextoConFormulas>{correcta}</TextoConFormulas>
                        </p>
                      </div>
                    </div>

                    {!esCorrecta && (
                      <div className="mt-4 space-y-2 border-t border-rose-200/70 pt-3 dark:border-rose-950">
                        {clase.length > 0 && (
                          <p className="text-xs text-slate-500 dark:text-slate-400">{clase.join(' · ')}</p>
                        )}
                        {det?.explicacion && (
                          <Markdown className="text-[0.85rem]">{det.explicacion}</Markdown>
                        )}
                        {enlace && (
                          <Link
                            to={enlace}
                            className="inline-block text-xs font-medium text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
                          >
                            Reforzar este tema →
                          </Link>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>

            <div className="flex flex-col sm:flex-row justify-center gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
              <Button
                variant="default"
                onClick={() => handleGenerarQuiz(resumen?.pendientes_hoy ? 'vencidas' : 'nuevas')}
                disabled={generando !== null}
                className="bg-indigo-600 hover:bg-indigo-500 text-white gap-2 text-xs"
              >
                <RotateCw className="h-3.5 w-3.5" />
                {resumen?.pendientes_hoy
                  ? `Repasar ${resumen.pendientes_hoy} pendientes`
                  : 'Otro repaso'}
              </Button>
              {enlaceRefuerzo && (
                <Button
                  variant="outline"
                  onClick={() => navigate(enlaceRefuerzo)}
                  className="text-xs"
                >
                  Reforzar con el tutor
                </Button>
              )}
              <Button
                variant="ghost"
                onClick={() => navigate('/')}
                className="text-xs"
              >
                Volver a Hoy
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // ------------------------- ESTADO 2: QUIZ ACTIVO EN CURSO -------------------------
  if (preguntas.length > 0) {
    const totalPreguntas = preguntas.length
    const preguntaActualObj = preguntas[preguntaActual]
    const seleccionActual = respuestasUsuario[preguntaActual]
    const progresoPorcentaje = Math.round(((preguntaActual + 1) / totalPreguntas) * 100)
    const contestadas = Object.keys(respuestasUsuario).length

    return (
      <div className="space-y-6 pb-12 max-w-3xl mx-auto">
        {/* Cabecera del Quiz Activo */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200/80 pb-4 dark:border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="gap-1.5 text-indigo-600 font-semibold">
                <Brain className="h-3.5 w-3.5" /> Repaso
              </Badge>
              <span className="text-slate-300">•</span>
              <span className="text-xs font-medium text-slate-500">
                Respondidas: {contestadas} de {totalPreguntas}
              </span>
            </div>
            <h1 className="mt-1 text-3xl font-semibold text-slate-900 dark:text-white">
              Repaso
            </h1>
          </div>
          <div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                if (confirm('¿Dejar el repaso? Perderás tus respuestas.')) {
                  setPreguntas([])
                  setQuizId(null)
                }
              }}
              className="text-xs text-slate-500"
            >
              Cancelar
            </Button>
          </div>
        </div>

        {/* Barra de progreso global */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs text-slate-500">
            <span>
              Pregunta <strong className="text-slate-800 dark:text-slate-200">{preguntaActual + 1}</strong> de {totalPreguntas}
            </span>
            <span>{progresoPorcentaje}% completado</span>
          </div>
          <Progress value={progresoPorcentaje} />
        </div>

        {/* Tarjeta de Pregunta Interactiva */}
        <Card className="shadow-sm border-slate-200/80 dark:border-slate-800">
          <CardHeader className="p-6 pb-4 border-b border-slate-100 dark:border-slate-800/60">
            <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600 uppercase tracking-wider">
              <HelpCircle className="h-4 w-4" /> Enunciado
            </div>
            <CardTitle className="text-lg font-semibold leading-relaxed mt-1 text-slate-900 dark:text-white">
              <TextoConFormulas>{preguntaActualObj.enunciado}</TextoConFormulas>
            </CardTitle>
          </CardHeader>

          <CardContent className="p-6 space-y-3">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Elige una respuesta
            </p>

            <div className="grid gap-2.5">
              {preguntaActualObj.opciones.map((opcion, idx) => {
                const isSelected = seleccionActual === opcion
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSeleccionarOpcion(opcion)}
                    className={`w-full text-left p-4 rounded-xl border text-xs font-medium transition-all cursor-pointer flex items-center justify-between gap-3 ${
                      isSelected
                        ? 'border-indigo-600 bg-indigo-50/80 text-indigo-950 dark:border-indigo-500 dark:bg-indigo-950/40 dark:text-indigo-200 shadow-sm ring-1 ring-indigo-500'
                        : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/70 text-slate-700 dark:border-slate-800 dark:bg-slate-900 dark:hover:bg-slate-800/60 dark:text-slate-300'
                    }`}
                  >
                    <span className="leading-relaxed"><TextoConFormulas>{opcion}</TextoConFormulas></span>
                    <div
                      className={`h-4 w-4 shrink-0 rounded-full border flex items-center justify-center ${
                        isSelected
                          ? 'border-indigo-600 bg-indigo-600 text-white'
                          : 'border-slate-300 dark:border-slate-700'
                      }`}
                    >
                      {isSelected && <div className="h-1.5 w-1.5 rounded-full bg-white" />}
                    </div>
                  </button>
                )
              })}
            </div>

            {/* Controles de Navegación entre Preguntas */}
            <div className="mt-8 flex items-center justify-between border-t border-slate-100 pt-5 dark:border-slate-800">
              <Button
                variant="outline"
                size="sm"
                disabled={preguntaActual === 0}
                onClick={() => setPreguntaActual((p) => p - 1)}
                className="gap-1.5 text-xs"
              >
                <ArrowLeft className="h-3.5 w-3.5" /> Anterior
              </Button>

              <div className="flex items-center gap-1.5">
                {preguntas.map((_, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setPreguntaActual(idx)}
                    className={`h-2.5 rounded-full transition-all cursor-pointer ${
                      idx === preguntaActual
                        ? 'w-6 bg-indigo-600'
                        : respuestasUsuario[idx]
                        ? 'w-2.5 bg-emerald-500'
                        : 'w-2.5 bg-slate-300 dark:bg-slate-700'
                    }`}
                    title={`Pregunta ${idx + 1}`}
                  />
                ))}
              </div>

              {preguntaActual < totalPreguntas - 1 ? (
                <Button
                  size="sm"
                  onClick={() => setPreguntaActual((p) => p + 1)}
                  className="gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs"
                >
                  Siguiente <ArrowRight className="h-3.5 w-3.5" />
                </Button>
              ) : (
                <Button
                  size="sm"
                  onClick={handleEnviarQuiz}
                  disabled={evaluando}
                  className="gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs shadow-sm"
                >
                  {evaluando ? (
                    <>
                      <div className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                      Corrigiendo…
                    </>
                  ) : (
                    <>
                      <CheckCircle2 className="h-3.5 w-3.5" />
                      Corregir
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // ------------------------- ESTADO 3: PANTALLA INICIAL -------------------------
  return (
    <div className="mx-auto max-w-2xl space-y-8 pb-12">
      <div className="space-y-3">
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Repaso</h1>
        <p className="text-lg leading-relaxed text-slate-600 dark:text-slate-400">
          Preguntas sobre las clases que ya terminaste. Las que falles vuelven pronto; las que
          aciertes, cada vez más espaciadas. Las opciones están pensadas para que no se pueda
          adivinar la respuesta por su forma: hay que saberla.
        </p>
      </div>

      {resumen && resumen.pendientes_hoy > 0 && (
        <section className="flex flex-col gap-4 rounded-lg border border-slate-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800 dark:bg-slate-900">
          <div>
            <p className="font-display text-xl text-slate-900 dark:text-slate-50">
              Tienes <span className="cifra font-semibold text-slate-900 underline decoration-marcador decoration-2 underline-offset-4 dark:text-slate-50">{resumen.pendientes_hoy}</span>{' '}
              {resumen.pendientes_hoy === 1 ? 'pregunta' : 'preguntas'} para repasar hoy
            </p>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Las que ya viste y toca volver a ver. No consume cuota de Gemini.
            </p>
          </div>
          <Button
            onClick={() => handleGenerarQuiz('vencidas')}
            disabled={generando !== null}
            className="shrink-0 gap-2"
          >
            {generando === 'vencidas' ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                Preparando…
              </>
            ) : (
              'Repasar ahora'
            )}
          </Button>
        </section>
      )}

      {errorMensaje && (
        <div className="space-y-3 border-l-2 border-amber-400 bg-amber-50/60 py-3 pl-4 pr-3 text-sm dark:bg-amber-950/20">
          <p className="text-amber-900 dark:text-amber-200">{errorMensaje}</p>
          <Button size="sm" variant="outline" onClick={() => navigate('/estudiar?tab=tutoria')}>
            Ir a Tutoría
          </Button>
        </div>
      )}

      <div className="flex flex-wrap items-center gap-4">
        <Button
          variant={resumen?.pendientes_hoy ? 'outline' : 'default'}
          onClick={() => handleGenerarQuiz('nuevas')}
          disabled={generando !== null}
          className="gap-2 px-5"
        >
          {generando === 'nuevas' ? (
            <>
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              Preparando preguntas…
            </>
          ) : (
            'Preguntas nuevas'
          )}
        </Button>
        <span className="text-sm text-slate-500">
          Tres preguntas nuevas de tus clases. Al terminar verás qué fallaste y por qué.
        </span>
      </div>
    </div>
  )
}
