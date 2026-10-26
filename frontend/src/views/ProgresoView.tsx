import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'
import { api } from '@/api/client'
import type {
  ClaseCronograma,
  EventoHistorial,
  MateriaStat,
  ResultadoClaseGuia,
  StatsResponse,
} from '@/api/types'
import {
  clave,
  describirFecha,
  enlaceTutoria,
  formatoCorto,
  inicioDelDia,
  parsearFecha,
} from '@/lib/asignaturas'
import { cn } from '@/lib/utils'

interface Fila {
  nombre: string
  stat?: MateriaStat
}

const formatoPct = new Intl.NumberFormat('es', { maximumFractionDigits: 0 })

function ClasesPendientes({ materia, hoy }: { materia: string; hoy: Date }) {
  const [clases, setClases] = useState<ClaseCronograma[] | null>(null)

  useEffect(() => {
    let activo = true
    api
      .getProximasClases(materia)
      .then((r) => activo && setClases(r.clases))
      .catch(() => activo && setClases([]))
    return () => {
      activo = false
    }
  }, [materia])

  if (!clases) return <p className="py-3 text-sm text-slate-500">Cargando clases…</p>
  if (clases.length === 0) return <p className="py-3 text-sm text-slate-500">No quedan clases pendientes.</p>

  return (
    <ol className="space-y-1 py-2">
      {clases.map((c, i) => {
        const fecha = parsearFecha(c.fecha)
        return (
          <li key={`${c.tema}-${i}`} className="grid grid-cols-[4.5rem_minmax(0,1fr)_auto] items-baseline gap-3 text-sm">
            <span className="cifra text-xs text-slate-500">{fecha ? formatoCorto.format(fecha) : '—'}</span>
            <span className="min-w-0">
              <span className="text-slate-800 dark:text-slate-200">{c.tema}</span>
              <span className="ml-2 text-xs text-slate-500">{describirFecha(fecha, hoy)}</span>
            </span>
            <Link
              to={enlaceTutoria(materia, c.tema)}
              className="text-xs text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
            >
              Estudiar
            </Link>
          </li>
        )
      })}
    </ol>
  )
}

const ETIQUETA_TIPO: Record<EventoHistorial['tipo'], string> = {
  tutoria: 'Tutoría',
  repaso: 'Repaso',
  guia: 'Guía',
}

const ETIQUETA_RESULTADO: Record<ResultadoClaseGuia, string> = {
  entendida: 'vista',
  con_dudas: 'con dudas',
  pendiente: 'pendiente',
}

/** Últimos eventos de estudio de la asignatura: tutorías terminadas y repasos. */
function HistorialBreve({ materia }: { materia: string }) {
  const [eventos, setEventos] = useState<EventoHistorial[] | null>(null)

  useEffect(() => {
    let activo = true
    api
      .getHistorial(materia)
      .then((r) => activo && setEventos(r.eventos.slice(0, 5)))
      .catch(() => activo && setEventos([]))
    return () => {
      activo = false
    }
  }, [materia])

  if (!eventos || eventos.length === 0) return null

  return (
    <div className="mt-3 border-t border-slate-200 pt-3 dark:border-slate-800">
      <p className="mb-1.5 font-display text-xs italic text-slate-500">Historial reciente</p>
      <ol className="space-y-1">
        {eventos.map((e, i) => {
          const fecha = parsearFecha(e.fecha)
          return (
            <li key={i} className="grid grid-cols-[3.5rem_3.75rem_minmax(0,1fr)_auto] items-baseline gap-2 text-sm sm:grid-cols-[4.5rem_4.5rem_minmax(0,1fr)_auto] sm:gap-3">
              <span className="cifra text-xs text-slate-500">{fecha ? formatoCorto.format(fecha) : '—'}</span>
              <span className="text-xs text-slate-600 dark:text-slate-400">
                {ETIQUETA_TIPO[e.tipo]}
              </span>
              <span className="truncate text-slate-700 dark:text-slate-300">{e.tema || '—'}</span>
              <span className="cifra text-right text-xs text-slate-600 dark:text-slate-400">
                {e.tipo === 'repaso' && e.total !== undefined
                  ? `${e.aciertos ?? 0}/${e.total}`
                  : e.tipo === 'guia' && e.resultado
                    ? ETIQUETA_RESULTADO[e.resultado]
                    : ''}
              </span>
            </li>
          )
        })}
      </ol>
    </div>
  )
}

export function ProgresoView() {
  const [hoy] = useState(() => inicioDelDia(new Date()))
  const [stats, setStats] = useState<StatsResponse | null>(null)
  const [materias, setMaterias] = useState<string[]>([])
  const [abierta, setAbierta] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([api.getStats(), api.getMaterias()])
      .then(([st, m]) => {
        setStats(st)
        setMaterias(m.materias)
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
  }, [])

  // Cruza el catálogo (nombres bien escritos) con las estadísticas (nombres derivados del archivo)
  const filas = useMemo<Fila[]>(() => {
    if (!stats) return []
    const statsPorClave = new Map(Object.entries(stats.materias).map(([n, s]) => [clave(n), { n, s }]))
    const usadas = new Set<string>()
    const lista: Fila[] = materias.map((nombre) => {
      const k = clave(nombre)
      const encontrado = statsPorClave.get(k)
      if (encontrado) usadas.add(k)
      return { nombre, stat: encontrado?.s }
    })
    for (const [k, { n, s }] of statsPorClave) {
      if (!usadas.has(k)) lista.push({ nombre: n, stat: s })
    }
    return lista.sort((a, b) => {
      if (!a.stat !== !b.stat) return a.stat ? -1 : 1
      return (b.stat?.porcentaje ?? 0) - (a.stat?.porcentaje ?? 0) || a.nombre.localeCompare(b.nombre)
    })
  }, [stats, materias])

  if (error) {
    return (
      <p className="rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
        No pude cargar tu progreso: {error}
      </p>
    )
  }

  if (!stats) {
    return (
      <div className="space-y-4">
        <div className="h-9 w-40 animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
        <div className="h-5 w-2/3 animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
      </div>
    )
  }

  const sinCronogramas = stats.total_temas === 0

  return (
    <div className="space-y-10">
      <header className="space-y-3">
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Progreso</h1>
        {sinCronogramas ? (
          <p className="text-lg text-slate-600 dark:text-slate-400">
            Aún no hay cronogramas.{' '}
            <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
              Sube un sílabo
            </Link>{' '}
            para empezar a medir tu avance.
          </p>
        ) : (
          <p className="max-w-2xl text-lg leading-relaxed text-slate-600 dark:text-slate-400">
            Llevas <span className="cifra text-slate-900 dark:text-slate-100">{stats.temas_completados}</span> de{' '}
            <span className="cifra text-slate-900 dark:text-slate-100">{stats.total_temas}</span> clases del
            semestre, el <span className="cifra text-slate-900 dark:text-slate-100">{formatoPct.format(stats.porcentaje_global)}{' '}%</span>.
          </p>
        )}
      </header>

      {!sinCronogramas && (
        <section>
          <div className="grid grid-cols-[minmax(0,1fr)_auto] border-b border-slate-200 pb-2 text-xs text-slate-500 sm:grid-cols-[minmax(0,14rem)_minmax(0,1fr)_4rem_3rem] sm:gap-6 dark:border-slate-800">
            <span>Asignatura</span>
            <span className="hidden sm:block">Avance</span>
            <span className="hidden text-right sm:block">Clases</span>
            <span className="text-right">%</span>
          </div>

          <ul className="divide-y divide-slate-200 dark:divide-slate-800">
            {filas.map((f) => {
              const expandida = abierta === f.nombre
              return (
                <li key={f.nombre}>
                  {f.stat ? (
                    <button
                      type="button"
                      onClick={() => setAbierta(expandida ? null : f.nombre)}
                      aria-expanded={expandida}
                      className="grid w-full cursor-pointer grid-cols-[minmax(0,1fr)_auto] items-center gap-x-6 gap-y-2 py-4 text-left sm:grid-cols-[minmax(0,14rem)_minmax(0,1fr)_4rem_3rem]"
                    >
                      <span className="flex min-w-0 items-center gap-1.5 font-medium text-slate-900 dark:text-slate-100">
                        <ChevronRight
                          className={cn('h-3.5 w-3.5 shrink-0 text-slate-400 transition-transform', expandida && 'rotate-90')}
                        />
                        <span className="truncate">{f.nombre}</span>
                      </span>
                      <span className="col-span-2 row-start-2 h-1.5 overflow-hidden rounded-sm bg-slate-200 sm:col-span-1 sm:row-start-auto dark:bg-slate-800">
                        <span
                          className="block h-full bg-indigo-600 dark:bg-indigo-400"
                          style={{ width: `${Math.min(100, f.stat.porcentaje)}%` }}
                        />
                      </span>
                      <span className="cifra hidden text-right text-sm text-slate-600 sm:block dark:text-slate-400">
                        {f.stat.completados}/{f.stat.total}
                      </span>
                      <span className="cifra text-right text-sm text-slate-900 dark:text-slate-100">
                        {formatoPct.format(f.stat.porcentaje)}
                      </span>
                    </button>
                  ) : (
                    <div className="flex items-baseline justify-between py-4 text-sm">
                      <span className="pl-5 font-medium text-slate-900 dark:text-slate-100">{f.nombre}</span>
                      <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
                        Subir sílabo
                      </Link>
                    </div>
                  )}
                  {expandida && (
                    <div className="mb-4 ml-5 border-l border-slate-200 pl-4 dark:border-slate-800">
                      <ClasesPendientes materia={f.nombre} hoy={hoy} />
                      <HistorialBreve materia={f.nombre} />
                    </div>
                  )}
                </li>
              )
            })}
          </ul>
        </section>
      )}

      {stats.plugins_activos > 0 && (
        <p className="text-sm text-slate-500">
          El tutor tiene memoria práctica de <span className="cifra">{stats.plugins_activos}</span>{' '}
          {stats.plugins_activos === 1 ? 'plugin' : 'plugins'}.{' '}
          <Link to="/plugins" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
            Ver plugins
          </Link>
        </p>
      )}
    </div>
  )
}
