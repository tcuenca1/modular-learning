import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Check } from 'lucide-react'
import { api } from '@/api/client'
import { AvisoIA } from '@/components/AvisoIA'
import type {
  ClaseCronograma,
  EscaneoMaterial,
  GuiaResumen,
  MateriaStat,
  ResumenRepaso,
} from '@/api/types'
import type { ClaseFechada } from '@/lib/asignaturas'
import {
  clave,
  claveDia,
  clasesConFecha,
  describirFecha,
  enlaceTutoria,
  formatoCorto,
  inicioDelDia,
  parsearFecha,
} from '@/lib/asignaturas'
import { avanceGlobal, estadoHoy, pasosDeArranque, tieneCronograma } from '@/lib/hoy'
import { cn } from '@/lib/utils'

interface Asignatura {
  nombre: string
  stat?: MateriaStat
  siguiente?: ClaseCronograma
  fechaSiguiente?: Date
}

const PASOS = [
  {
    id: 'asignatura',
    titulo: 'Crea una asignatura',
    detalle: 'Por ejemplo, «Bases de Datos».',
    to: '/asignaturas',
  },
  {
    id: 'silabo',
    titulo: 'Sube el sílabo',
    detalle: 'La IA arma el cronograma de clases a partir de él.',
    to: '/asignaturas',
  },
  {
    id: 'tutoria',
    titulo: 'Empieza una tutoría',
    detalle: 'Elige una clase y estudia el tema paso a paso con ayuda de la IA.',
    to: '/estudiar',
  },
] as const

const formatoFecha = new Intl.DateTimeFormat('es', { weekday: 'long', day: 'numeric', month: 'long' })

function capitalizar(texto: string): string {
  return texto.charAt(0).toUpperCase() + texto.slice(1)
}

/** Una marca por clase del cronograma: llenas las completadas, la siguiente resaltada. */
function Regleta({ stat }: { stat: MateriaStat }) {
  return (
    <div role="img" className="flex flex-wrap gap-[3px]" aria-label={`${stat.completados} de ${stat.total} clases`}>
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
  const [asignaturas, setAsignaturas] = useState<Asignatura[] | null>(null)
  const [escaneos, setEscaneos] = useState<EscaneoMaterial[] | null>(null)
  const [errorEscaneo, setErrorEscaneo] = useState(false)
  const [resumen, setResumen] = useState<ResumenRepaso | null>(null)
  const [clasesDeHoy, setClasesDeHoy] = useState<ClaseFechada[]>([])
  const [guiasPorConfirmar, setGuiasPorConfirmar] = useState<GuiaResumen[]>([])
  const [enNube, setEnNube] = useState(false)
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
        setAsignaturas(lista)
      } catch (e) {
        if (activo) setError(e instanceof Error ? e.message : String(e))
      }
    }
    cargar()
    // Secundarios: si fallan, la pantalla sigue siendo útil
    api
      .getResumenRepaso()
      .then((r) => activo && setResumen(r))
      .catch(() => activo && setResumen(null))
    api
      .getGuiasPendientes()
      .then((r) => activo && setGuiasPorConfirmar(r.guias))
      .catch(() => undefined)
    Promise.all([api.getCronogramas(), api.getMaterias()])
      .then(([{ cronogramas }, { materias }]) => {
        if (!activo) return
        const claveHoy = claveDia(hoy)
        setClasesDeHoy(clasesConFecha(cronogramas, materias).filter((c) => claveDia(c.fecha) === claveHoy))
      })
      .catch(() => undefined)
    // En la nube no se escanean carpetas locales; en local se carga aparte
    api
      .getConfig()
      .then((cfg) => {
        if (!activo) return
        if (cfg.en_nube) {
          setEnNube(true)
        } else {
          api
            .escanearMaterial()
            .then((r) => activo && setEscaneos(r.escaneos))
            .catch(() => activo && setErrorEscaneo(true))
        }
      })
      .catch(() => {
        if (!activo) return
        api
          .escanearMaterial()
          .then((r) => activo && setEscaneos(r.escaneos))
          .catch(() => activo && setErrorEscaneo(true))
      })
    return () => {
      activo = false
    }
  }, [hoy])

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
  // Un solo criterio para contador, titular y listas: las clases de las asignaturas listadas
  const avance = asignaturas ? avanceGlobal(asignaturas) : null
  const estado = asignaturas ? estadoHoy(asignaturas) : null
  const pasos = asignaturas ? pasosDeArranque(asignaturas) : []
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
      {/* Guías offline que aún no se confirmaron: lo primero al volver */}
      {guiasPorConfirmar.length > 0 && (
        <Link
          to={guiasPorConfirmar.length === 1 ? `/guia/${guiasPorConfirmar[0].id}/revision` : '/estudiar?tab=guia'}
          className="toque group flex items-center justify-between gap-3 border-l-4 border-marcador bg-white px-4 py-2.5 text-sm transition-colors hover:bg-slate-50 dark:bg-slate-900 dark:hover:bg-slate-800/60"
        >
          <span className="min-w-0 truncate text-slate-700 dark:text-slate-300">
            {guiasPorConfirmar.length === 1 ? (
              <>
                1 guía de <span className="font-medium text-slate-900 dark:text-slate-100">{guiasPorConfirmar[0].materia}</span> por confirmar
              </>
            ) : (
              <>
                <span className="font-medium text-slate-900 dark:text-slate-100">{guiasPorConfirmar.length} guías</span> por confirmar
              </>
            )}
          </span>
          <span className="shrink-0 text-sm font-medium text-indigo-700 group-hover:underline group-hover:underline-offset-4 dark:text-indigo-300">
            {guiasPorConfirmar.length === 1 ? 'Confirmar →' : 'Ver todas →'}
          </span>
        </Link>
      )}

      {/* Lo que toca hoy */}
      <section>
        <p className="cifra text-xs text-slate-500 dark:text-slate-400">
          {capitalizar(formatoFecha.format(hoy))}
        </p>
        {clasesDeHoy.length > 0 && (
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            <span className="font-display italic text-slate-500">Hoy en clase:</span>{' '}
            {clasesDeHoy.map((c, i) => (
              <span key={i}>
                {i > 0 && '; '}
                <Link
                  to={enlaceTutoria(c.materia, c.clase.tema, undefined, c.clase.id)}
                  className={cn(
                    'text-slate-800 underline decoration-slate-300 underline-offset-4 hover:decoration-indigo-600 dark:text-slate-200 dark:decoration-slate-600',
                    c.completada && 'opacity-60'
                  )}
                >
                  {c.clase.tema}
                </Link>{' '}
                <span className="text-slate-500">({c.materia})</span>
              </span>
            ))}
          </p>
        )}

        {!asignaturas ? (
          <div className="mt-4 space-y-3">
            <div className="h-10 w-3/4 motion-safe:animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
            <div className="h-4 w-1/3 motion-safe:animate-pulse rounded bg-slate-200 dark:bg-slate-800" />
          </div>
        ) : estado === 'pendiente' && foco ? (
          <>
            <p className="mt-4 text-xs font-medium uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Siguiente clase
            </p>
            <h1 className="mt-1 max-w-3xl text-2xl font-semibold leading-tight text-slate-900 sm:text-3xl md:text-4xl lg:text-[2.6rem] lg:leading-[1.1] dark:text-slate-50 break-words">
              Te toca <span className="marcador">{foco.siguiente!.tema}</span>
            </h1>
            <p className="mt-3 text-slate-600 dark:text-slate-400">
              {foco.nombre} · la clase {describirFecha(foco.fechaSiguiente, hoy)}
              {foco.fechaSiguiente && ` (${formatoCorto.format(foco.fechaSiguiente)})`}
            </p>
            <Link
              to={enlaceTutoria(foco.nombre, foco.siguiente!.tema, undefined, foco.siguiente!.id)}
              className="toque mt-6 inline-flex items-center gap-2 rounded-md bg-indigo-700 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-800 dark:bg-indigo-400 dark:text-slate-950 dark:hover:bg-indigo-300"
            >
              Estudiar ahora <ArrowRight className="h-4 w-4" />
            </Link>
          </>
        ) : estado === 'al_dia' ? (
          <>
            <h1 className="mt-3 text-2xl font-semibold leading-tight text-slate-900 sm:text-3xl md:text-4xl lg:text-[2.6rem] lg:leading-[1.1] dark:text-slate-50 break-words">
              No tienes clases pendientes.
            </h1>
            <p className="mt-3 text-slate-600 dark:text-slate-400">
              Completaste todas las clases de tus cronogramas. Puedes repasar o revisar el{' '}
              <Link to="/calendario" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
                calendario
              </Link>
              .
            </p>
          </>
        ) : (
          <>
            <h1 className="mt-3 text-2xl font-semibold leading-tight text-slate-900 sm:text-3xl md:text-4xl lg:text-[2.6rem] lg:leading-[1.1] dark:text-slate-50 break-words">
              Aún no tienes clases cargadas.
            </h1>
            <p className="mt-3 text-slate-600 dark:text-slate-400">
              Sigue estos tres pasos para empezar a estudiar.
            </p>
            <section aria-labelledby="primeros-pasos" className="mt-6 max-w-xl rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
              <h2 id="primeros-pasos" className="text-lg text-slate-900 dark:text-slate-100">
                Primeros pasos
              </h2>
              <ol className="mt-3 space-y-3">
                {PASOS.map((paso, i) => {
                  const hecho = pasos[i]?.hecho ?? false
                  return (
                    <li key={paso.id} className="flex items-start gap-3 text-sm">
                      <span
                        aria-hidden="true"
                        className={cn(
                          'mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full border text-xs',
                          hecho
                            ? 'border-indigo-700 bg-indigo-700 text-white dark:border-indigo-400 dark:bg-indigo-400 dark:text-slate-950'
                            : 'border-slate-300 text-slate-500 dark:border-slate-700'
                        )}
                      >
                        {hecho ? <Check className="h-3 w-3" /> : i + 1}
                      </span>
                      <span className="min-w-0">
                        <Link
                          to={paso.to}
                          className="font-medium text-indigo-700 underline underline-offset-4 dark:text-indigo-300"
                        >
                          {paso.titulo}
                        </Link>
                        {hecho && <span className="sr-only"> (hecho)</span>}
                        <span className="block text-slate-500 dark:text-slate-400">{paso.detalle}</span>
                      </span>
                    </li>
                  )
                })}
              </ol>
            </section>
          </>
        )}
      </section>

      <div className="grid gap-12 lg:grid-cols-[minmax(0,1fr)_17rem]">
        {/* Asignaturas */}
        <section>
          <div className="flex items-baseline justify-between border-b border-slate-200 pb-2 dark:border-slate-800">
            <h2 className="text-xl text-slate-900 dark:text-slate-100">Tus asignaturas</h2>
            {avance && (
              <span className="cifra text-xs text-slate-500">
                {avance.completados}/{avance.total} clases ({avance.porcentaje}%)
              </span>
            )}
          </div>

          {asignaturas && asignaturas.length === 0 && (
            <p className="py-5 text-sm text-slate-500 dark:text-slate-400">
              Todavía no hay asignaturas. Crea la primera desde{' '}
              <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
                Asignaturas
              </Link>
              .
            </p>
          )}
          <ul className="divide-y divide-slate-200 dark:divide-slate-800">
            {ordenadas.map((a) => (
              <li key={a.nombre} className="grid gap-x-6 gap-y-2 py-5 sm:grid-cols-[minmax(0,1fr)_auto]">
                <div className="min-w-0 space-y-2">
                  <div className="flex items-baseline gap-3">
                    <h3 className="font-medium text-slate-900 dark:text-slate-100">{a.nombre}</h3>
                    {tieneCronograma(a) && a.stat && (
                      <span className="cifra text-xs text-slate-500">
                        {a.stat.completados}/{a.stat.total} ({Math.round(a.stat.porcentaje)}%)
                      </span>
                    )}
                  </div>
                  {tieneCronograma(a) && a.stat ? (
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
                      <Link
                        to={`/asignaturas?materia=${encodeURIComponent(a.nombre)}`}
                        aria-label={`Subir sílabo de ${a.nombre}`}
                        className="toque inline-flex items-center text-indigo-700 underline underline-offset-4 dark:text-indigo-300"
                      >
                        Subir sílabo
                      </Link>
                    </p>
                  )}
                </div>
                {a.siguiente && (
                  <Link
                    to={enlaceTutoria(a.nombre, a.siguiente.tema, undefined, a.siguiente.id)}
                    className="toque inline-flex items-center justify-self-start self-center text-sm text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
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
            {resumen && resumen.pendientes_hoy > 0 ? (
              <div className="mt-4 space-y-3">
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  <span className="cifra font-semibold text-slate-900 underline decoration-marcador decoration-2 underline-offset-4 dark:text-slate-100">{resumen.pendientes_hoy}</span>{' '}
                  {resumen.pendientes_hoy === 1 ? 'pregunta' : 'preguntas'} para hoy.
                </p>
                <Link
                  to="/estudiar?tab=repaso"
                  className="toque inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-800 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                >
                  Repasar ahora
                </Link>
              </div>
            ) : avance && avance.completados > 0 ? (
              <div className="mt-4 space-y-3">
                <p className="text-sm text-slate-500">
                  Nada pendiente hoy
                  {resumen && resumen.total > 0 && (
                    <>
                      {' '}· <span className="cifra">{resumen.dominadas}</span> de{' '}
                      <span className="cifra">{resumen.total}</span> dominadas
                    </>
                  )}
                  .
                </p>
                <Link
                  to="/estudiar?tab=repaso"
                  className="toque inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-800 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                >
                  Preguntas nuevas <AvisoIA />
                </Link>
              </div>
            ) : (
              <p className="mt-4 text-sm text-slate-500">Completa una clase para desbloquear el repaso.</p>
            )}
          </section>

          {!enNube && (
            <section>
              <h2 className="border-b border-slate-200 pb-2 text-xl text-slate-900 dark:border-slate-800 dark:text-slate-100">
                Material nuevo
              </h2>
            <div className="mt-4 space-y-3 text-sm">
              {errorEscaneo ? (
                <p className="text-slate-500">
                  No pude revisar tus carpetas.{' '}
                  <Link to="/ajustes?tab=config" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
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
                    className="toque inline-flex items-center gap-1.5 rounded-md border border-slate-300 px-3 py-1.5 text-slate-800 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                  >
                    Procesar {pendientesMaterial} {pendientesMaterial === 1 ? 'archivo' : 'archivos'}
                  </Link>
                </>
              )}
            </div>
          </section>
          )}
        </aside>
      </div>
    </div>
  )
}
