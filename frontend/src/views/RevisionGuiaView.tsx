import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { Guia, ResultadoClaseGuia, RevisionGuiaResponse } from '@/api/types'
import { Button } from '@/components/ui/button'
import { enlaceTutoria, formatoCorto, parsearFecha } from '@/lib/asignaturas'
import { cn } from '@/lib/utils'

const OPCIONES: { valor: ResultadoClaseGuia; etiqueta: string }[] = [
  { valor: 'entendida', etiqueta: 'La entendí' },
  { valor: 'con_dudas', etiqueta: 'La entendí, con dudas' },
  { valor: 'pendiente', etiqueta: 'No la revisé o no la entendí' },
]

interface Respuesta {
  resultado?: ResultadoClaseGuia
  dudas: string
}

function Resultado({ guia, r }: { guia: Guia; r: RevisionGuiaResponse }) {
  return (
    <div className="max-w-3xl space-y-8">
      <header className="space-y-2">
        <p className="font-display text-sm italic text-slate-500">{guia.materia}</p>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
          {r.completadas.length === 0
            ? 'Las clases siguen pendientes'
            : r.completadas.length === 1
              ? 'Una clase marcada como vista'
              : `${r.completadas.length} clases marcadas como vistas`}
        </h1>
        {r.completadas.length > 0 && (
          <p className="text-slate-600 dark:text-slate-400">
            {r.completadas.length === 1
              ? 'Ya entra en tu repaso: las próximas preguntas también saldrán de ella.'
              : 'Ya entran en tu repaso: las próximas preguntas también saldrán de ellas.'}
          </p>
        )}
      </header>

      {r.dudas.length > 0 && (
        <section>
          <h2 className="border-b border-slate-200 pb-2 text-xl text-slate-900 dark:border-slate-800 dark:text-slate-100">
            Tus dudas
          </h2>
          <ul className="divide-y divide-slate-200 dark:divide-slate-800">
            {r.dudas.map((d) => (
              <li key={d.tema} className="grid gap-x-6 gap-y-2 py-4 sm:grid-cols-[minmax(0,1fr)_auto]">
                <div className="min-w-0">
                  <p className="font-medium text-slate-900 dark:text-slate-100">{d.tema}</p>
                  <p className="mt-1 whitespace-pre-line break-words text-sm text-slate-600 dark:text-slate-400">
                    {d.dudas}
                  </p>
                </div>
                <Link
                  to={enlaceTutoria(r.materia, d.tema, d.dudas)}
                  className="self-center text-sm font-medium text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
                >
                  Preguntar al tutor →
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      {r.pendientes.length > 0 && (
        <p className="text-sm text-slate-600 dark:text-slate-400">
          Siguen pendientes: {r.pendientes.join(', ')}.{' '}
          <Link
            to={enlaceTutoria(r.materia, r.pendientes[0])}
            className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300"
          >
            Estudiar con el tutor
          </Link>
        </p>
      )}

      <Link to="/" className="inline-block text-sm text-slate-500 underline underline-offset-4 hover:text-slate-800 dark:hover:text-slate-200">
        Volver a Hoy
      </Link>
    </div>
  )
}

export function RevisionGuiaView() {
  const { id = '' } = useParams()
  const [guia, setGuia] = useState<Guia | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [respuestas, setRespuestas] = useState<Respuesta[]>([])
  const [enviando, setEnviando] = useState(false)
  const [resultado, setResultado] = useState<RevisionGuiaResponse | null>(null)

  useEffect(() => {
    api
      .getGuia(id)
      .then((g) => {
        setGuia(g)
        setRespuestas(g.clases.map(() => ({ dudas: '' })))
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
  }, [id])

  const responder = (i: number, cambio: Partial<Respuesta>) =>
    setRespuestas((prev) => prev.map((r, j) => (j === i ? { ...r, ...cambio } : r)))

  const completo = respuestas.length > 0 && respuestas.every((r) => r.resultado)

  const enviar = async () => {
    if (!guia || !completo) return
    try {
      setEnviando(true)
      const r = await api.registrarRevisionGuia(guia.id, {
        resultados: respuestas.map((r, indice) => ({
          indice,
          resultado: r.resultado!,
          dudas: r.resultado === 'con_dudas' ? r.dudas : '',
        })),
      })
      setResultado(r)
    } catch (err) {
      toast.error('No pude guardar tu revisión', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setEnviando(false)
    }
  }

  if (error) {
    return (
      <p className="rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
        No pude abrir la guía: {error}
      </p>
    )
  }
  if (!guia) return <div className="h-48 max-w-3xl animate-pulse rounded-lg bg-slate-200 dark:bg-slate-800" />
  if (resultado) return <Resultado guia={guia} r={resultado} />

  if (guia.revisada) {
    return (
      <div className="max-w-3xl space-y-3">
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Guía ya confirmada</h1>
        <p className="text-slate-600 dark:text-slate-400">
          Ya me dijiste cómo te fue con esta guía de {guia.materia}.
        </p>
        <Link to="/guia" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
          Ver tus guías
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-3xl space-y-8">
      <header className="space-y-2">
        <p className="font-display text-sm italic text-slate-500">{guia.materia}</p>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">¿Cómo te fue con la guía?</h1>
        <p className="text-slate-600 dark:text-slate-400">
          Las que entendiste quedan como vistas. Si te quedaron dudas, escríbelas y las resolvemos con el
          tutor.
        </p>
      </header>

      <ol className="space-y-4">
        {guia.clases.map((c, i) => {
          const fecha = parsearFecha(c.fecha)
          const r = respuestas[i]
          return (
            <li
              key={c.tema}
              className="space-y-3 rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
            >
              <div>
                <p className="cifra text-xs text-slate-500">
                  Clase {i + 1}
                  {fecha && ` · ${formatoCorto.format(fecha)}`}
                </p>
                <p className="font-medium text-slate-900 dark:text-slate-100">{c.tema}</p>
              </div>
              <div role="radiogroup" aria-label={`Resultado de ${c.tema}`} className="flex flex-wrap gap-2">
                {OPCIONES.map((o) => (
                  <button
                    key={o.valor}
                    type="button"
                    role="radio"
                    aria-checked={r?.resultado === o.valor}
                    onClick={() => responder(i, { resultado: o.valor })}
                    className={cn(
                      'cursor-pointer rounded-full border px-3 py-1 text-sm transition-colors',
                      r?.resultado === o.valor
                        ? 'border-indigo-700 bg-indigo-700 text-white dark:border-indigo-400 dark:bg-indigo-400 dark:text-slate-950'
                        : 'border-slate-300 text-slate-700 hover:border-slate-400 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800'
                    )}
                  >
                    {o.etiqueta}
                  </button>
                ))}
              </div>
              {r?.resultado === 'con_dudas' && (
                <textarea
                  value={r.dudas}
                  onChange={(e) => responder(i, { dudas: e.target.value })}
                  rows={3}
                  placeholder="¿Qué no te quedó claro? Cópialo de tu recuadro «Mis dudas»."
                  className="w-full rounded-md border border-slate-300 bg-white p-2 text-sm text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100"
                />
              )}
            </li>
          )
        })}
      </ol>

      <div className="flex flex-wrap items-center gap-4">
        <Button onClick={enviar} disabled={!completo || enviando}>
          {enviando ? 'Guardando…' : 'Confirmar'}
        </Button>
        {!completo && <span className="text-sm text-slate-500">Elige una opción en cada clase.</span>}
      </div>
    </div>
  )
}
