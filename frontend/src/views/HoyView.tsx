import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'
import { api } from '@/api/client'
import type { ClaseCronograma, EscaneoMaterial, MateriaStat, StatsResponse } from '@/api/types'
import { cn } from '@/lib/utils'

interface Asignatura {
  nombre: string
  stat?: MateriaStat
  siguiente?: ClaseCronograma
  fechaSiguiente?: Date
}

const DIA_MS = 86_400_000

/** Normaliza nombres para cruzar el catálogo de materias con las estadísticas por cronograma. */
function clave(nombre: string): string {
  return nombre
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '')
}

/** Interpreta fechas dd/mm/aaaa (formato de los cronogramas) o ISO. */
function parsearFecha(valor: unknown): Date | undefined {
  if (typeof valor !== 'string') return undefined
  const dmy = valor.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/)
  if (dmy) return new Date(Number(dmy[3]), Number(dmy[2]) - 1, Number(dmy[1]))
  const iso = new Date(valor)
  return Number.isNaN(iso.getTime()) ? undefined : iso
}

function inicioDelDia(fecha: Date): Date {
  return new Date(fecha.getFullYear(), fecha.getMonth(), fecha.getDate())
}

function describirFecha(fecha: Date | undefined, hoy: Date): string {
  if (!fecha) return 'sin fecha en el cronograma'
  const dias = Math.round((inicioDelDia(fecha).getTime() - hoy.getTime()) / DIA_MS)
  if (dias === 0) return 'es hoy'
  if (dias === 1) return 'es mañana'
  if (dias > 1) return `en ${dias} días`
  if (dias === -1) return 'fue ayer'
  return `fue hace ${-dias} días`
}

const formatoFecha = new Intl.DateTimeFormat('es', { weekday: 'long', day: 'numeric', month: 'long' })
const formatoCorto = new Intl.DateTimeFormat('es', { day: 'numeric', month: 'short' })

function capitalizar(texto: string): string {
  return texto.charAt(0).toUpperCase() + texto.slice(1)
}

function enlaceTutoria(a: Asignatura): string {
  const q = new URLSearchParams({ materia: a.nombre })
  if (a.siguiente?.tema) q.set('tema', a.siguiente.tema)
  return `/tutoria?${q.toString()}`
}

/** Una marca por clase del cronograma: llenas las completadas, la siguiente resaltada. */
function Regleta({ stat }: { stat: MateriaStat }) {
  return (
    <div className="flex flex-wrap gap-[3px]" aria-label={`${stat.completados} de ${stat.total} clases`}>
      {Array.from({ length: stat.total }, (_, i) => (
        <span
          key={i}
          className={cn(
            'h-3 w-1.5 rounded-[1px]',
            i < stat.completados
              ? 'bg-indigo-600 dark:bg-indigo-400'
              : i === stat.completados
                ? 'bg-marcador'
                : 'bg-slate-300/70 dark:bg-slate-700'
          )}
        />
      ))}
    </div>
  )
}

export function HoyView() {
  const [hoy] = useState(() => inicioDelDia(new Date()))
  const [stats, setStats] = useState<StatsResponse | null>(null)
  const [asignaturas, setAsignaturas] = useState<Asignatura[] | null>(null)
  const [escaneos, setEscaneos] = useState<EscaneoMaterial[] | null>(null)
  const [errorEscaneo, setErrorEscaneo] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let activo = true
    const cargar = async () => {
      try {
        const [st, { materias }] = await Promise.all([api.getStats(), api.getMaterias()])
        const statsPorClave = new Map(Object.entries(st.materias).map(([n, s]) => [clave(n), s]))
        const lista = await Promise.all(
          materias.map(async (nombre): Promise<Asignatura> => {
            const stat = statsPorClave.get(clave(nombre))
            if (!stat) return { nombre }
            const { clases } = await api.getProximasClases(nombre).catch(() => ({ clases: [] }))
            const siguiente = clases[0]
            return { nombre, stat, siguiente, fechaSiguiente: parsearFecha(siguiente?.fecha) }
          })
        )
        if (!activo) return
        setStats(st)
        setAsignaturas(lista)
      } catch (e) {
        if (activo) setError(e instanceof Error ? e.message : String(e))
      }
    }
    cargar()
    // El escaneo recorre carpetas locales y puede tardar: se carga aparte
    api
      .escanearMaterial()
      .then((r) => activo && setEscaneos(r.escaneos))
      .catch(() => activo && setErrorEscaneo(true))
    return () => {
      activo = false
    }
  }, [])

  // Lo que toca: la clase pendiente más antigua (o la más próxima si no hay atrasos)
  const ordenadas = useMemo(() => {
    if (!asignaturas) return []
    const tiempo = (a: Asignatura) => a.fechaSiguiente?.getTime() ?? Number.POSITIVE_INFINITY
    return [...asignaturas].sort((a, b) => {
      if (!!a.siguiente !== !!b.siguiente) return a.siguiente ? -1 : 1
      return tiempo(a) - tiempo(b)
    })
  }, [asignaturas])

  const foco = ordenadas.find((a) => a.siguiente)
  const pendientesMaterial = escaneos?.reduce((n, e) => n + e.pendientes.length, 0) ?? 0
  const conMaterial = escaneos?.filter((e) => e.pendientes.length > 0) ?? []

  if (error) {
    return (
      <p className="rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
        No pude cargar tu día: {error}
      </p>
    )
  }

  return (
    <div className="space-y-12">
      {/* Lo que toca hoy */}
      <section>
        <p className="cifra text-xs text-slate-500 dark:text-slate-400">
          {capitalizar(formatoFecha.format(hoy))}
        </p>

        {!asignaturas ? (
          <div className="mt-4 space-y-3">
            <div className="h-10 w-3/4 animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
            <div className="h-4 w-1/3 animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
          </div>
        ) : foco ? (
          <>
            <h1 className="mt-3 max-w-3xl text-[2.6rem] leading-[1.1] text-slate-900 dark:text-slate-50">
              Te toca <span className="marcador">{foco.siguiente!.tema}</span>
            </h1>
            <p className="mt-3 text-slate-600 dark:text-slate-400">
              {foco.nombre} · la clase {describirFecha(foco.fechaSiguiente, hoy)}
              {foco.fechaSiguiente && ` (${formatoCorto.format(foco.fechaSiguiente)})`}
            </p>
            <Link
              to={enlaceTutoria(foco)}
              className="mt-6 inline-flex items-center gap-2 rounded-md bg-indigo-700 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-800 dark:bg-indigo-400 dark:text-slate-950 dark:hover:bg-indigo-300"
            >
              Estudiar ahora <ArrowRight className="h-4 w-4" />
            </Link>
          </>
        ) : (
          <>
            <h1 className="mt-3 text-[2.6rem] leading-[1.1] text-slate-900 dark:text-slate-50">
              No tienes clases pendientes.
            </h1>
            <p className="mt-3 text-slate-600 dark:text-slate-400">
              Sube el sílabo de una asignatura para planificar el semestre.{' '}
              <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
                Ir a Asignaturas
              </Link>
            </p>
          </>
        )}
      </section>

      <div className="grid gap-12 lg:grid-cols-[minmax(0,1fr)_17rem]">
        {/* Asignaturas */}
        <section>
          <div className="flex items-baseline justify-between border-b border-slate-200 pb-2 dark:border-slate-800">
            <h2 className="text-xl text-slate-900 dark:text-slate-100">Tus asignaturas</h2>
            {stats && (
              <span className="cifra text-xs text-slate-500">
                {stats.temas_completados}/{stats.total_temas} clases
              </span>
            )}
          </div>

          <ul className="divide-y divide-slate-200 dark:divide-slate-800">
            {ordenadas.map((a) => (
              <li key={a.nombre} className="grid gap-x-6 gap-y-2 py-5 sm:grid-cols-[minmax(0,1fr)_auto]">
                <div className="min-w-0 space-y-2">
                  <div className="flex items-baseline gap-3">
                    <h3 className="font-medium text-slate-900 dark:text-slate-100">{a.nombre}</h3>
                    {a.stat && (
                      <span className="cifra text-xs text-slate-500">
                        {a.stat.completados}/{a.stat.total}
                      </span>
                    )}
                  </div>
                  {a.stat ? (
                    <>
                      <Regleta stat={a.stat} />
                      <p className="truncate text-sm text-slate-500 dark:text-slate-400">
                        {a.siguiente
                          ? `Siguiente: ${a.siguiente.tema} — ${describirFecha(a.fechaSiguiente, hoy)}`
                          : 'Cronograma completado.'}
                      </p>
                    </>
                  ) : (
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      Aún sin cronograma.{' '}
                      <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
                        Subir sílabo
                      </Link>
                    </p>
                  )}
                </div>
                {a.siguiente && (
                  <Link
                    to={enlaceTutoria(a)}
                    className="self-center text-sm text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
                  >
                    Estudiar →
                  </Link>
                )}
              </li>
            ))}
          </ul>
        </section>

        {/* Columna lateral: repaso y material */}
        <aside className="space-y-10">
          <section>
            <h2 className="border-b border-slate-200 pb-2 text-xl text-slate-900 dark:border-slate-800 dark:text-slate-100">
              Repaso
            </h2>
            {stats && stats.temas_completados > 0 ? (
              <div className="mt-4 space-y-3">
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Tienes <span className="cifra text-slate-900 dark:text-slate-100">{stats.temas_completados}</span>{' '}
                  {stats.temas_completados === 1 ? 'tema listo' : 'temas listos'} para ponerte a prueba.
                </p>
                <Link
                  to="/repaso"
                  className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-800 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                >
                  Hacer un repaso
                </Link>
              </div>
            ) : (
              <p className="mt-4 text-sm text-slate-500">Completa una clase para desbloquear el repaso.</p>
            )}
          </section>

          <section>
            <h2 className="border-b border-slate-200 pb-2 text-xl text-slate-900 dark:border-slate-800 dark:text-slate-100">
              Material nuevo
            </h2>
            <div className="mt-4 space-y-3 text-sm">
              {errorEscaneo ? (
                <p className="text-slate-500">
                  No pude revisar tus carpetas.{' '}
                  <Link to="/config" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
                    Revisa la configuración
                  </Link>
                </p>
              ) : !escaneos ? (
                <p className="text-slate-500">Revisando tus carpetas…</p>
              ) : pendientesMaterial === 0 ? (
                <p className="text-slate-500">Todo tu material ya está en Obsidian.</p>
              ) : (
                <>
                  <ul className="space-y-1.5">
                    {conMaterial.map((e) => (
                      <li key={e.materia} className="flex justify-between gap-3 text-slate-600 dark:text-slate-400">
                        <span className="truncate">{e.materia}</span>
                        <span className="cifra text-slate-900 dark:text-slate-100">{e.pendientes.length}</span>
                      </li>
                    ))}
                  </ul>
                  <Link
                    to="/asignaturas?tab=material"
                    className="inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-slate-800 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                  >
                    Procesar {pendientesMaterial} {pendientesMaterial === 1 ? 'archivo' : 'archivos'}
                  </Link>
                </>
              )}
            </div>
          </section>
        </aside>
      </div>
    </div>
  )
}
