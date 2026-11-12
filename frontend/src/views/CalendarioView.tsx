import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { api } from '@/api/client'
import type { ClaseFechada } from '@/lib/asignaturas'
import { claveDia, clasesConFecha, enlaceTutoria, inicioDelDia } from '@/lib/asignaturas'
import { mesInicial, primerDiaDelMes, proximaClase } from '@/lib/calendario'
import { cn } from '@/lib/utils'

const DIAS_SEMANA = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
const formatoMes = new Intl.DateTimeFormat('es', { month: 'long', year: 'numeric' })
const formatoDia = new Intl.DateTimeFormat('es', { weekday: 'long', day: 'numeric' })

function capitalizar(texto: string): string {
  return texto.charAt(0).toUpperCase() + texto.slice(1)
}

/** Días que muestra la cuadrícula: semanas completas de lunes a domingo que cubren el mes. */
function diasDeLaCuadricula(mes: Date): Date[] {
  const primero = new Date(mes.getFullYear(), mes.getMonth(), 1)
  const desfase = (primero.getDay() + 6) % 7
  const ultimo = new Date(mes.getFullYear(), mes.getMonth() + 1, 0)
  const total = Math.ceil((desfase + ultimo.getDate()) / 7) * 7
  return Array.from(
    { length: total },
    (_, i) => new Date(mes.getFullYear(), mes.getMonth(), 1 - desfase + i)
  )
}

function EntradaClase({ c, compacta }: { c: ClaseFechada; compacta?: boolean }) {
  return (
    <Link
      to={enlaceTutoria(c.materia, c.clase.tema, undefined, c.clase.id)}
      title={`${c.materia} · ${c.clase.tema}${c.completada ? ' (completada)' : ''}`}
      className={cn(
        'toque group block min-w-0 rounded-sm border-l-2 px-1.5 py-0.5 transition-colors',
        !compacta && 'py-2',
        c.completada
          ? 'border-slate-300 hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800/50'
          : 'border-indigo-600 hover:bg-indigo-50 dark:border-indigo-400 dark:hover:bg-indigo-950/40'
      )}
    >
      <span
        className={cn(
          'block',
          // Completada: color secundario y tachado, sin opacidad (la opacidad rompe el contraste AA)
          c.completada
            ? 'text-slate-500 line-through decoration-slate-400/70'
            : 'text-slate-800 group-hover:text-indigo-800 dark:text-slate-200 dark:group-hover:text-indigo-200',
          compacta ? 'line-clamp-2 text-xs leading-snug' : 'text-sm'
        )}
      >
        {c.clase.tema}
      </span>
      <span className={cn('block truncate text-slate-500', compacta ? 'text-[0.7rem]' : 'text-xs')}>
        {c.materia}
      </span>
    </Link>
  )
}

export function CalendarioView() {
  const [hoy] = useState(() => inicioDelDia(new Date()))
  const [mes, setMes] = useState(() => new Date(hoy.getFullYear(), hoy.getMonth(), 1))
  const [clases, setClases] = useState<ClaseFechada[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([api.getCronogramas(), api.getMaterias()])
      .then(([{ cronogramas }, { materias }]) => {
        const lista = clasesConFecha(cronogramas, materias)
        setClases(lista)
        // Abre en el mes donde hay trabajo, no en un mes vacío
        setMes(mesInicial(lista, hoy))
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
  }, [hoy])

  const porDia = useMemo(() => {
    const mapa = new Map<string, ClaseFechada[]>()
    for (const c of clases ?? []) {
      const k = claveDia(c.fecha)
      mapa.set(k, [...(mapa.get(k) ?? []), c])
    }
    return mapa
  }, [clases])

  const dias = useMemo(() => diasDeLaCuadricula(mes), [mes])
  const delMes = (clases ?? []).filter(
    (c) => c.fecha.getMonth() === mes.getMonth() && c.fecha.getFullYear() === mes.getFullYear()
  )
  const diasConClase = [...new Set(delMes.map((c) => claveDia(c.fecha)))]
  const pendientesDelMes = delMes.filter((c) => !c.completada).length
  const esMesActual = mes.getMonth() === hoy.getMonth() && mes.getFullYear() === hoy.getFullYear()
  const claveHoy = claveDia(hoy)
  const proxima = clases ? proximaClase(clases, hoy) : null
  const proximaEnOtroMes =
    proxima !== null &&
    (proxima.fecha.getMonth() !== mes.getMonth() || proxima.fecha.getFullYear() !== mes.getFullYear())

  const moverMes = (delta: number) => setMes((m) => new Date(m.getFullYear(), m.getMonth() + delta, 1))

  if (error) {
    return (
      <p className="rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
        No pude cargar el calendario: {error}
      </p>
    )
  }

  return (
    <div className="space-y-8">
      <header className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="font-display text-sm italic text-slate-500">Calendario</p>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
            {capitalizar(formatoMes.format(mes))}
          </h1>
          {clases && (
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              {delMes.length === 0 ? (
                'Sin clases este mes.'
              ) : (
                <>
                  <span className="cifra text-slate-900 dark:text-slate-100">{delMes.length}</span>{' '}
                  {delMes.length === 1 ? 'clase' : 'clases'}, <span className="cifra">{pendientesDelMes}</span>{' '}
                  {pendientesDelMes === 1 ? 'pendiente' : 'pendientes'}
                </>
              )}
            </p>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-1">
          {proximaEnOtroMes && proxima && (
            <button
              type="button"
              onClick={() => setMes(primerDiaDelMes(proxima.fecha))}
              className="cursor-pointer rounded-md border border-indigo-300 px-3 py-1 text-sm text-indigo-800 hover:bg-indigo-50 dark:border-indigo-700 dark:text-indigo-200 dark:hover:bg-indigo-950/40"
            >
              Ir a la próxima clase
            </button>
          )}
          <button
            type="button"
            onClick={() => moverMes(-1)}
            className="cursor-pointer rounded-md p-2 text-slate-600 hover:bg-slate-200/60 dark:text-slate-300 dark:hover:bg-slate-800"
            aria-label="Mes anterior"
          >
            <ChevronLeft className="h-4 w-4" />
          </button>
          <button
            type="button"
            onClick={() => setMes(new Date(hoy.getFullYear(), hoy.getMonth(), 1))}
            disabled={esMesActual}
            className="cursor-pointer rounded-md border border-slate-300 px-3 py-1 text-sm text-slate-700 hover:bg-slate-100 disabled:cursor-default disabled:opacity-40 disabled:hover:bg-transparent dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
          >
            Hoy
          </button>
          <button
            type="button"
            onClick={() => moverMes(1)}
            className="cursor-pointer rounded-md p-2 text-slate-600 hover:bg-slate-200/60 dark:text-slate-300 dark:hover:bg-slate-800"
            aria-label="Mes siguiente"
          >
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      </header>

      {!clases ? (
        <div className="h-96 motion-safe:animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
      ) : clases.length === 0 ? (
        <p className="text-slate-600 dark:text-slate-400">
          Tus cronogramas no tienen fechas todavía.{' '}
          <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
            Sube un sílabo
          </Link>{' '}
          para ver qué clase toca cada día.
        </p>
      ) : (
        <>
          {/* Escritorio: cuadrícula mensual */}
          <div className="hidden lg:block">
            <div className="grid grid-cols-7 border-b border-slate-200 pb-2 dark:border-slate-800">
              {DIAS_SEMANA.map((d) => (
                <span key={d} className="px-2 font-display text-xs italic text-slate-500">
                  {d}
                </span>
              ))}
            </div>
            <div className="grid grid-cols-7 border-l border-slate-200 dark:border-slate-800">
              {dias.map((dia) => {
                const k = claveDia(dia)
                const delDia = porDia.get(k) ?? []
                const fuera = dia.getMonth() !== mes.getMonth()
                const esHoy = k === claveHoy
                return (
                  <div
                    key={k}
                    className={cn(
                      'min-h-28 min-w-0 space-y-1 border-r border-b border-slate-200 p-1.5 dark:border-slate-800',
                      fuera && 'bg-slate-100/50 dark:bg-slate-900/30',
                      esHoy && 'bg-white ring-2 ring-inset ring-indigo-600 dark:bg-slate-900 dark:ring-indigo-400'
                    )}
                  >
                    <span
                      className={cn(
                        'cifra inline-block px-1 text-xs',
                        fuera ? 'text-slate-400 dark:text-slate-500' : 'text-slate-600 dark:text-slate-400',
                        esHoy && 'marcador font-semibold text-slate-900 dark:text-slate-50'
                      )}
                    >
                      {dia.getDate()}
                    </span>
                    {!fuera && delDia.map((c, i) => <EntradaClase key={i} c={c} compacta />)}
                  </div>
                )
              })}
            </div>
          </div>

          {/* Móvil: lista por días */}
          <ol className="divide-y divide-slate-200 lg:hidden dark:divide-slate-800">
            {diasConClase.length === 0 && (
              <li className="py-4 text-sm text-slate-500">No hay clases en este mes.</li>
            )}
            {diasConClase.map((k) => {
              const delDia = porDia.get(k) ?? []
              const esHoy = k === claveHoy
              return (
                <li key={k} className="grid grid-cols-[4.5rem_minmax(0,1fr)] gap-3 py-3">
                  <span
                    className={cn(
                      'cifra pt-0.5 text-xs text-slate-500',
                      esHoy && 'font-semibold text-slate-900 dark:text-slate-100'
                    )}
                  >
                    {esHoy ? <span className="marcador">hoy</span> : formatoDia.format(delDia[0].fecha)}
                  </span>
                  <div className="min-w-0 space-y-2">
                    {delDia.map((c, i) => (
                      <EntradaClase key={i} c={c} />
                    ))}
                  </div>
                </li>
              )
            })}
          </ol>

          <p className="flex flex-wrap gap-x-6 gap-y-1 text-xs text-slate-500">
            <span className="flex items-center gap-2">
              <span className="h-3 w-0.5 bg-indigo-600 dark:bg-indigo-400" /> Pendiente: abre la tutoría
            </span>
            <span className="flex items-center gap-2">
              <span className="h-3 w-0.5 bg-slate-300 dark:bg-slate-700" />
              <span className="line-through">Completada</span>
            </span>
          </p>
        </>
      )}
    </div>
  )
}
