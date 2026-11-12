import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { AlertCircle, Check, Clock, Download, FileDown, RotateCw, Trash2, Undo2 } from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import { AvisoIA } from '@/components/AvisoIA'
import type { Guia, GuiaResumen, ParcialItem } from '@/api/types'
import { Button } from '@/components/ui/button'
import type { MateriaConCronograma } from '@/lib/asignaturas'
import { clave, esCompletada, formatoCorto, materiasConCronograma, parsearFecha } from '@/lib/asignaturas'
import { describirCorte, resolverIndiceHasta } from '@/lib/parciales'
import { MAXIMO_CLASES_GUIA, NOMBRE_EXTENSION, extensionPara } from '@/lib/guias'
import { cn } from '@/lib/utils'

type EstadoClase = 'espera' | 'generando' | 'lista' | 'error'

const selectClase =
  'mt-1 h-9 w-full min-w-0 rounded-md border border-slate-300 bg-white px-2 text-sm text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-100'

function etiquetaClase(i: number, fecha: unknown, tema: string): string {
  const f = parsearFecha(fecha)
  return `${i + 1} · ${f ? `${formatoCorto.format(f)} · ` : ''}${tema}`
}

function Generacion({
  guia,
  estados,
  onReintentar,
}: {
  guia: Guia
  estados: EstadoClase[]
  onReintentar: () => void
}) {
  const listas = estados.filter((e) => e === 'lista').length
  const generando = estados.includes('generando')
  const fallidas = estados.filter((e) => e === 'error').length

  return (
    <section className="space-y-5 rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-xl text-slate-900 dark:text-slate-50">{guia.materia}</h2>
        <span className="cifra text-xs text-slate-500">
          {listas}/{guia.clases.length} clases · {NOMBRE_EXTENSION[guia.extension]}
          {guia.tiempo_minutos ? ` · ${guia.tiempo_minutos} min` : ''}
        </span>
      </div>

      <ol className="space-y-2">
        {guia.clases.map((c, i) => (
          <li key={c.clase_id || `${c.tema}-${i}`} className="flex items-start gap-3 text-sm">
            <span className="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center">
              {estados[i] === 'lista' ? (
                <Check className="h-4 w-4 text-indigo-700 dark:text-indigo-300" />
              ) : estados[i] === 'generando' ? (
                <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-indigo-600 border-t-transparent" />
              ) : estados[i] === 'error' ? (
                <AlertCircle className="h-4 w-4 text-rose-600" />
              ) : (
                <span className="h-1.5 w-1.5 rounded-full bg-slate-300 dark:bg-slate-600" />
              )}
            </span>
            <span
              className={cn(
                'min-w-0',
                estados[i] === 'espera' ? 'text-slate-500' : 'text-slate-800 dark:text-slate-200'
              )}
            >
              {c.tema}
            </span>
          </li>
        ))}
      </ol>

      {generando ? (
        <p className="text-sm text-slate-500">
          Escribiendo una clase cada vez; puede tardar un poco. No cierres esta página.
        </p>
      ) : fallidas > 0 ? (
        <div className="flex flex-wrap items-center gap-3">
          <p className="text-sm text-rose-700 dark:text-rose-300">
            {fallidas === 1 ? 'Una clase no se pudo generar.' : `${fallidas} clases no se pudieron generar.`}
          </p>
          <Button size="sm" variant="outline" onClick={onReintentar} className="gap-1.5">
            <RotateCw className="h-3.5 w-3.5" /> Reintentar
          </Button>
        </div>
      ) : (
        <div className="flex flex-col gap-3 border-t border-slate-200 pt-4 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800">
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Lista. Descárgala directamente en PDF o ábrela para imprimirla; al volver te preguntaré cómo te fue.
          </p>
          <div className="flex items-center gap-2">
            <a
              href={`/api/guias/${guia.id}/pdf`}
              download
              className="inline-flex shrink-0 items-center justify-center gap-2 rounded-md bg-indigo-700 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-800 dark:bg-indigo-400 dark:text-slate-950 dark:hover:bg-indigo-300"
            >
              <Download className="h-4 w-4" /> Descargar PDF
            </a>
            <Link
              to={`/guia/${guia.id}/imprimir`}
              className="inline-flex shrink-0 items-center justify-center gap-1.5 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              <FileDown className="h-4 w-4" /> Vista previa
            </Link>
          </div>
        </div>
      )}
    </section>
  )
}

function ListaGuias({
  guias,
  onContinuar,
  onEliminar,
  onDeshacer,
}: {
  guias: GuiaResumen[]
  onContinuar: (id: string) => void
  onEliminar: (id: string) => void
  onDeshacer: (id: string) => void
}) {
  if (guias.length === 0) return null
  return (
    <section>
      <h2 className="border-b border-slate-200 pb-2 text-xl text-slate-900 dark:border-slate-800 dark:text-slate-100">
        Tus guías
      </h2>
      <ul className="divide-y divide-slate-200 dark:divide-slate-800">
        {guias.map((g) => {
          const creada = parsearFecha(g.creada)
          return (
            <li key={g.id} className="grid gap-x-6 gap-y-1 py-4 sm:grid-cols-[minmax(0,1fr)_auto]">
              <div className="min-w-0">
                <p className="font-medium text-slate-900 dark:text-slate-100">{g.materia}</p>
                <p className="truncate text-sm text-slate-500 dark:text-slate-400">
                  {creada && <span className="cifra">{formatoCorto.format(creada)} · </span>}
                  {g.temas.length === 1 ? g.temas[0] : `${g.temas.length} clases: ${g.temas.join(', ')}`}
                  {g.tiempo_minutos ? ` (${g.tiempo_minutos} min)` : ''}
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
                {!g.completa ? (
                  <button
                    type="button"
                    onClick={() => onContinuar(g.id)}
                    className="cursor-pointer text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
                  >
                    Terminar de generar
                  </button>
                ) : (
                  <>
                    {g.pendiente_de_confirmar && (
                      <Link
                        to={`/guia/${g.id}/revision`}
                        className="font-medium text-slate-900 underline decoration-marcador decoration-2 underline-offset-4 dark:text-slate-100"
                      >
                        ¿Cómo te fue?
                      </Link>
                    )}
                    <a
                      href={`/api/guias/${g.id}/pdf`}
                      download
                      title="Descargar PDF directamente"
                      className="inline-flex items-center gap-1 font-medium text-indigo-700 hover:underline hover:underline-offset-4 dark:text-indigo-300"
                    >
                      <Download className="h-3 w-3" /> PDF
                    </a>
                    <Link
                      to={`/guia/${g.id}/imprimir`}
                      className="text-slate-500 hover:underline hover:underline-offset-4 dark:text-slate-400 text-xs"
                    >
                      Ver
                    </Link>
                    {g.revisada && (
                      <span className="flex items-center gap-1.5 text-xs text-slate-500">
                        confirmada
                        <button
                          type="button"
                          onClick={() => onDeshacer(g.id)}
                          title="Deshacer confirmación y volver clases a pendientes"
                          className="cursor-pointer text-amber-600 hover:text-amber-700 dark:text-amber-400"
                        >
                          <Undo2 className="h-3 w-3" />
                        </button>
                      </span>
                    )}
                  </>
                )}
                <button
                  type="button"
                  onClick={() => onEliminar(g.id)}
                  title="Eliminar guía"
                  className="cursor-pointer text-slate-400 hover:text-rose-600 dark:hover:text-rose-400"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            </li>
          )
        })}
      </ul>
    </section>
  )
}

export function GuiaView() {
  const [params] = useSearchParams()
  const [materias, setMaterias] = useState<MateriaConCronograma[] | null>(null)
  const [guias, setGuias] = useState<GuiaResumen[]>([])
  const [parciales, setParciales] = useState<ParcialItem[]>([])
  const [error, setError] = useState<string | null>(null)

  const [materia, setMateria] = useState('')
  const [desde, setDesde] = useState(0)
  const [hasta, setHasta] = useState(0)
  const [tiempoMinutos, setTiempoMinutos] = useState<number | null>(null)
  const [tiempoCustom, setTiempoCustom] = useState('')

  const [guia, setGuia] = useState<Guia | null>(null)
  const [estados, setEstados] = useState<EstadoClase[]>([])
  const [creando, setCreando] = useState(false)

  const [editandoParciales, setEditandoParciales] = useState(false)
  const [nuevoNombreParcial, setNuevoNombreParcial] = useState('')
  const [nuevoHastaParcial, setNuevoHastaParcial] = useState(0)

  const cargarGuias = () => {
    api
      .listarGuias()
      .then((r) => setGuias(r.guias))
      .catch(() => setGuias([]))
  }

  const cargarParciales = (nom: string) => {
    if (!nom) return
    api
      .getParciales(nom)
      .then((r) => setParciales(r.parciales || []))
      .catch(() => setParciales([]))
  }

  useEffect(() => {
    Promise.all([api.getCronogramas(), api.getMaterias()])
      .then(([{ cronogramas }, { materias: catalogo }]) => {
        const lista = materiasConCronograma(cronogramas, catalogo)
        setMaterias(lista)
        const pedida = params.get('materia')
        const elegida = lista.find((m) => pedida && clave(m.materia) === clave(pedida)) ?? lista[0]
        if (!elegida) return
        const tema = params.get('tema')
        const porTema = tema ? elegida.clases.findIndex((c) => c.tema === tema) : -1
        const inicio = porTema >= 0 ? porTema : Math.max(0, elegida.clases.findIndex((c) => !esCompletada(c)))
        setMateria(elegida.materia)
        setDesde(inicio)
        setHasta(inicio)
        cargarParciales(elegida.materia)
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
    cargarGuias()
  }, [params])

  const actual = useMemo(() => materias?.find((m) => m.materia === materia), [materias, materia])
  const [ini, fin] = desde <= hasta ? [desde, hasta] : [hasta, desde]
  const elegidas = actual?.clases.slice(ini, fin + 1) ?? []
  const demasiadas = elegidas.length > MAXIMO_CLASES_GUIA

  const cambiarMateria = (nombre: string) => {
    const m = materias?.find((x) => x.materia === nombre)
    const inicio = Math.max(0, m?.clases.findIndex((c) => !esCompletada(c)) ?? 0)
    setMateria(nombre)
    setDesde(inicio)
    setHasta(inicio)
    cargarParciales(nombre)
  }

  const generar = async (g: Guia, indices: number[]) => {
    for (const i of indices) {
      setEstados((prev) => prev.map((e, j) => (j === i ? 'generando' : e)))
      try {
        await api.generarClaseGuia(g.id, i)
        setEstados((prev) => prev.map((e, j) => (j === i ? 'lista' : e)))
      } catch (err) {
        setEstados((prev) => prev.map((e, j) => (j === i ? 'error' : e)))
        toast.error(`No pude escribir «${g.clases[i].tema}»`, {
          description: err instanceof Error ? err.message : String(err),
        })
      }
    }
    cargarGuias()
  }

  const empezar = (g: Guia) => {
    const iniciales = g.clases.map((c): EstadoClase => (c.contenido ? 'lista' : 'espera'))
    setGuia(g)
    setEstados(iniciales)
    generar(g, iniciales.flatMap((e, i) => (e === 'lista' ? [] : [i])))
  }

  const crear = async () => {
    if (!actual || elegidas.length === 0 || demasiadas) return
    try {
      setCreando(true)
      const idsOTemas = elegidas.map((c) => (c.id ? String(c.id) : c.tema))
      empezar(await api.crearGuia(actual.materia, idsOTemas, tiempoMinutos ?? undefined))
    } catch (err) {
      toast.error('No pude crear la guía', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setCreando(false)
    }
  }

  const continuar = async (id: string) => {
    try {
      empezar(await api.getGuia(id))
    } catch (err) {
      toast.error('No pude abrir la guía', { description: err instanceof Error ? err.message : String(err) })
    }
  }

  const eliminarGuia = async (id: string) => {
    if (!confirm('¿Seguro que deseas eliminar esta guía?')) return
    try {
      await api.eliminarGuia(id)
      toast.success('Guía eliminada')
      cargarGuias()
    } catch (err) {
      toast.error('Error al eliminar la guía', { description: String(err) })
    }
  }

  const deshacerRevision = async (id: string) => {
    if (!confirm('¿Deshacer confirmación? Las clases volverán al estado pendiente.')) return
    try {
      await api.deshacerRevisionGuia(id)
      toast.success('Confirmación revertida')
      cargarGuias()
    } catch (err) {
      toast.error('Error al deshacer confirmación', { description: String(err) })
    }
  }

  const seleccionarCorteParcial = (p: ParcialItem) => {
    if (!actual) return
    const idx = resolverIndiceHasta(actual.clases, p.hasta)
    if (idx >= 0) {
      setDesde(0)
      setHasta(idx)
      toast.info(`Seleccionado hasta ${p.nombre} (clase ${idx + 1})`)
    } else {
      toast.error(`No se pudo localizar la clase donde termina ${p.nombre}`)
    }
  }

  const guardarNuevoParcial = async () => {
    if (!actual || !nuevoNombreParcial.trim()) return
    const claseObj = actual.clases[nuevoHastaParcial]
    if (!claseObj?.id) return
    const nuevos = [...parciales.filter((p) => p.nombre !== nuevoNombreParcial.trim()), {
      nombre: nuevoNombreParcial.trim(),
      hasta: String(claseObj.id),
    }]
    try {
      await api.guardarParciales(actual.materia, nuevos)
      setParciales(nuevos)
      setNuevoNombreParcial('')
      setEditandoParciales(false)
      toast.success('Parcial guardado')
    } catch (e) {
      toast.error('Error al guardar parcial', { description: String(e) })
    }
  }

  const generando = estados.includes('generando')

  if (error) {
    return (
      <p className="rounded-md border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-200">
        No pude cargar tus asignaturas: {error}
      </p>
    )
  }

  return (
    <div className="max-w-3xl space-y-10">
      <header className="space-y-1">
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Guía offline</h1>
        <p className="text-base text-slate-600 dark:text-slate-400">
          Prepara clases en un cuaderno A5 descargable para estudiar sin pantalla.
        </p>
      </header>

      {guia ? (
        <div className="space-y-3">
          <Generacion
            guia={guia}
            estados={estados}
            onReintentar={() => generar(guia, estados.flatMap((e, i) => (e === 'error' ? [i] : [])))}
          />
          {!generando && (
            <button
              type="button"
              onClick={() => {
                setGuia(null)
                setEstados([])
              }}
              className="cursor-pointer text-sm text-slate-500 underline underline-offset-4 hover:text-slate-800 dark:hover:text-slate-200"
            >
              Preparar otra guía
            </button>
          )}
        </div>
      ) : !materias ? (
        <div className="h-48 motion-safe:animate-pulse rounded-lg bg-slate-200 dark:bg-slate-800" />
      ) : materias.length === 0 ? (
        <p className="text-slate-600 dark:text-slate-400">
          Aún no hay cronogramas.{' '}
          <Link to="/asignaturas" className="text-indigo-700 underline underline-offset-4 dark:text-indigo-300">
            Sube un sílabo
          </Link>{' '}
          para preparar guías de sus clases.
        </p>
      ) : (
        <section className="space-y-6 rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300">
            Asignatura
            <select value={materia} onChange={(e) => cambiarMateria(e.target.value)} className={selectClase}>
              {materias.map((m) => (
                <option key={m.materia} value={m.materia}>
                  {m.materia}
                </option>
              ))}
            </select>
          </label>

          {/* Fin de cada parcial */}
          {actual && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500 uppercase tracking-wide">
                  Fin de cada parcial
                </span>
                <button
                  type="button"
                  onClick={() => setEditandoParciales(!editandoParciales)}
                  className="cursor-pointer text-xs text-indigo-600 hover:underline dark:text-indigo-400"
                >
                  {editandoParciales ? 'Cerrar' : '+ Definir parcial'}
                </button>
              </div>
              <p className="text-xs text-slate-500">
                Elige la última clase de cada parcial para armar guías de todo el parcial.
              </p>

              {parciales.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {parciales.map((p) => (
                    <button
                      key={p.nombre}
                      type="button"
                      onClick={() => seleccionarCorteParcial(p)}
                      title={describirCorte(actual.clases, p.hasta)}
                      className="cursor-pointer rounded-full border border-indigo-200 bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700 transition hover:bg-indigo-100 dark:border-indigo-900/60 dark:bg-indigo-950/40 dark:text-indigo-300"
                    >
                      {p.nombre}
                    </button>
                  ))}
                </div>
              )}

              {editandoParciales && (
                <div className="rounded-md border border-slate-200 bg-slate-50 p-3 space-y-3 dark:border-slate-800 dark:bg-slate-950/50">
                  <div className="grid gap-3 sm:grid-cols-2">
                    <label className="block text-xs font-medium text-slate-700 dark:text-slate-300">
                      Nombre del parcial
                      <input
                        type="text"
                        placeholder="Ej: Parcial 1"
                        value={nuevoNombreParcial}
                        onChange={(e) => setNuevoNombreParcial(e.target.value)}
                        className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white"
                      />
                    </label>
                    <label className="block text-xs font-medium text-slate-700 dark:text-slate-300">
                      Hasta la clase
                      <select
                        value={nuevoHastaParcial}
                        onChange={(e) => setNuevoHastaParcial(Number(e.target.value))}
                        className="mt-1 h-8 w-full rounded border border-slate-300 bg-white px-2 text-xs dark:border-slate-700 dark:bg-slate-900 dark:text-white"
                      >
                        {actual.clases.map((c, i) => (
                          <option key={i} value={i}>
                            {i + 1} · {c.tema}
                          </option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <Button size="sm" onClick={guardarNuevoParcial} disabled={!nuevoNombreParcial.trim()}>
                    Guardar parcial
                  </Button>
                </div>
              )}
            </div>
          )}

          {/* Rango de clases */}
          {actual && (
            <div className="grid gap-4 sm:grid-cols-2">
              <label className="block min-w-0 text-sm font-medium text-slate-700 dark:text-slate-300">
                Desde la clase
                <select value={desde} onChange={(e) => setDesde(Number(e.target.value))} className={selectClase}>
                  {actual.clases.map((c, i) => (
                    <option key={c.id || i} value={i}>
                      {etiquetaClase(i, c.fecha, c.tema)}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block min-w-0 text-sm font-medium text-slate-700 dark:text-slate-300">
                Hasta la clase
                <select value={hasta} onChange={(e) => setHasta(Number(e.target.value))} className={selectClase}>
                  {actual.clases.map((c, i) => (
                    <option key={c.id || i} value={i}>
                      {etiquetaClase(i, c.fecha, c.tema)}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          )}

          {/* Reparto según tiempo disponible */}
          <div className="space-y-2 border-t border-slate-200 pt-4 dark:border-slate-800">
            <span className="flex items-center gap-1.5 text-xs font-medium text-slate-600 dark:text-slate-400">
              <Clock className="h-3.5 w-3.5" /> Tiempo disponible para estudiar (opcional)
            </span>
            <div className="flex flex-wrap items-center gap-2">
              {[
                { label: 'Libre (por clases)', val: null },
                { label: '1 hora', val: 60 },
                { label: '2 horas', val: 120 },
                { label: '4 horas', val: 240 },
              ].map((opt) => (
                <button
                  key={opt.label}
                  type="button"
                  onClick={() => {
                    setTiempoMinutos(opt.val)
                    setTiempoCustom('')
                  }}
                  className={cn(
                    'cursor-pointer rounded-md border px-3 py-1.5 text-xs font-medium transition',
                    tiempoMinutos === opt.val && !tiempoCustom
                      ? 'border-indigo-600 bg-indigo-50 text-indigo-700 dark:border-indigo-400 dark:bg-indigo-950/40 dark:text-indigo-300'
                      : 'border-slate-300 text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800'
                  )}
                >
                  {opt.label}
                </button>
              ))}
              <input
                type="number"
                placeholder="Minutos..."
                value={tiempoCustom}
                onChange={(e) => {
                  setTiempoCustom(e.target.value)
                  const v = Number(e.target.value)
                  setTiempoMinutos(v > 0 ? v : null)
                }}
                className="h-8 w-24 rounded-md border border-slate-300 bg-white px-2 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-700 dark:bg-slate-900 dark:text-white"
              />
            </div>
          </div>

          {elegidas.length > 0 && (
            <div className="space-y-2 border-t border-slate-200 pt-4 dark:border-slate-800">
              <p className="text-sm text-slate-600 dark:text-slate-400">
                <span className="cifra text-slate-900 dark:text-slate-100">{elegidas.length}</span>{' '}
                {elegidas.length === 1 ? 'clase' : 'clases'}, versión{' '}
                <span className="font-display italic">
                  {NOMBRE_EXTENSION[extensionPara(elegidas.length, tiempoMinutos)]}
                </span>
                {tiempoMinutos ? ` (${Math.round(tiempoMinutos / elegidas.length)} min por clase)` : ''}
                {elegidas.some(esCompletada) && ' · incluye clases que ya viste'}
              </p>
              {demasiadas && (
                <p className="text-sm text-rose-700 dark:text-rose-300">
                  Como máximo {MAXIMO_CLASES_GUIA} clases por guía.
                </p>
              )}
              <p className="text-xs text-slate-500">
                Cada clase es una consulta a Gemini y tarda unos segundos.
              </p>
            </div>
          )}

          <Button onClick={crear} disabled={creando || elegidas.length === 0 || demasiadas} className="gap-2">
            <FileDown className="h-4 w-4" />
            {creando ? 'Preparando…' : (<>Generar guía <AvisoIA /></>)}
          </Button>
        </section>
      )}

      <ListaGuias
        guias={guias}
        onContinuar={continuar}
        onEliminar={eliminarGuia}
        onDeshacer={deshacerRevision}
      />
    </div>
  )
}
