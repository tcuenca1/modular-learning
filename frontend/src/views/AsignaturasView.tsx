import { useCallback, useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { BookMarked, Check, Edit2, Plus, X } from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { MateriaItem } from '@/api/types'
import { buscarMateriaPorClave } from '@/lib/asignaturas'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { cn } from '@/lib/utils'
import { MaterialView } from '@/views/MaterialView'
import { SilabosView } from '@/views/SilabosView'

const PESTANAS = [
  { id: 'clases', nombre: 'Clases', detalle: 'Administra tus clases, fechas y sílabos del semestre.' },
  { id: 'material', nombre: 'Material', detalle: 'Convierte tus archivos de clase en notas para Obsidian.' },
  { id: 'proyectos', nombre: 'Proyectos', detalle: 'Supervisa el código y notas de proyectos de asignatura.' },
] as const

type Pestana = (typeof PESTANAS)[number]['id']

export function AsignaturasView() {
  const [params, setParams] = useSearchParams()

  // Retrocompatibilidad de pestañas
  const tabParam = params.get('tab')
  const activa: Pestana =
    tabParam === 'material'
      ? 'material'
      : tabParam === 'proyectos'
        ? 'proyectos'
        : 'clases' // 'cronogramas' o cualquier otro valor redirige a 'clases'

  const detalle = PESTANAS.find((p) => p.id === activa)?.detalle

  // Catálogo de asignaturas
  const [materias, setMaterias] = useState<MateriaItem[]>([])
  const [materiaActiva, setMateriaActiva] = useState<string>('')
  const materiaQueryInicial = useRef(params.get('materia'))

  // Acciones sobre la asignatura activa
  const [renombrando, setRenombrando] = useState(false)
  const [nuevoNombre, setNuevoNombre] = useState('')
  const [creando, setCreando] = useState(false)
  const [nombreNueva, setNombreNueva] = useState('')
  const [guardandoNueva, setGuardandoNueva] = useState(false)

  const cargarMaterias = useCallback((seleccionarNombreOSlug?: string) => {
    return api
      .getMaterias()
      .then((res) => {
        const lista: MateriaItem[] =
          res.catalogo && res.catalogo.length > 0
            ? res.catalogo
            : (res.materias || []).map((m) => ({
                slug: m.toLowerCase().replace(/\s+/g, '-'),
                nombre: m,
              }))
        setMaterias(lista)

        if (lista.length > 0) {
          if (seleccionarNombreOSlug) {
            const match = buscarMateriaPorClave(lista, seleccionarNombreOSlug)
            if (match) {
              setMateriaActiva(match.slug)
              return
            }
          }
          setMateriaActiva((prev) => {
            if (prev && lista.some((m) => m.slug === prev)) return prev
            const queryMateria = materiaQueryInicial.current
            if (queryMateria) {
              const encontrada = buscarMateriaPorClave(lista, queryMateria)
              if (encontrada) return encontrada.slug
            }
            return lista[0].slug
          })
        } else {
          setMateriaActiva('')
        }
      })
      .catch((e) => {
        toast.error('No pude cargar el catálogo de asignaturas', {
          description: e instanceof Error ? e.message : String(e),
        })
      })
  }, [])

  useEffect(() => {
    void cargarMaterias()
  }, [cargarMaterias])

  const materiaActivaObj = materias.find((m) => m.slug === materiaActiva)

  // La asignatura activa vive en la URL: sobrevive a recargas y se puede compartir el enlace
  useEffect(() => {
    if (!materiaActiva) return
    setParams(
      (prev) => {
        if (prev.get('materia') === materiaActiva) return prev
        const p = new URLSearchParams(prev)
        p.set('materia', materiaActiva)
        return p
      },
      { replace: true }
    )
  }, [materiaActiva, setParams])

  const cambiarTab = (pId: Pestana) => {
    const p = new URLSearchParams(params)
    if (pId === 'clases') {
      p.delete('tab')
    } else {
      p.set('tab', pId)
    }
    setParams(p, { replace: true })
  }

  const handleCrearMateria = async () => {
    const limpia = nombreNueva.trim()
    if (!limpia || guardandoNueva) return
    setGuardandoNueva(true)
    try {
      await api.createMateria(limpia)
      toast.success(`Asignatura "${limpia}" creada`, {
        description: 'Ahora sube su sílabo o añade clases en la pestaña Clases.',
      })
      setCreando(false)
      setNombreNueva('')
      await cargarMaterias(limpia)
    } catch (err) {
      toast.error('No se pudo crear la asignatura', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setGuardandoNueva(false)
    }
  }

  const handleRenombrar = async () => {
    const limpia = nuevoNombre.trim()
    if (!limpia || !materiaActivaObj || limpia === materiaActivaObj.nombre) {
      setRenombrando(false)
      return
    }
    try {
      await api.renombrarMateria(materiaActiva, limpia)
      toast.success(`Asignatura renombrada a "${limpia}"`)
      setRenombrando(false)
      await cargarMaterias(limpia)
    } catch (err) {
      toast.error('No se pudo renombrar la asignatura', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  return (
    <div className="space-y-6">
      {/* Cabecera y Selector compartido */}
      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Asignaturas</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{detalle}</p>
        </div>

        {/* Selector de Asignatura Único y Compartido */}
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-slate-200 bg-white p-3 shadow-xs dark:border-slate-800 dark:bg-slate-900">
          <div className="flex min-w-0 max-w-full flex-wrap items-center gap-3">
            <div className="flex items-center gap-2">
              <BookMarked className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
              <span className="text-xs font-medium text-slate-600 dark:text-slate-400">
                Asignatura:
              </span>
            </div>

            {materias.length > 0 ? (
              <div className="flex min-w-0 max-w-full items-center gap-2">
                <select
                  value={materiaActiva}
                  onChange={(e) => setMateriaActiva(e.target.value)}
                  className="h-8 min-w-0 max-w-full truncate rounded-md border border-slate-200 bg-white px-2.5 text-xs font-semibold text-slate-900 shadow-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                >
                  {materias.map((m) => (
                    <option key={m.slug} value={m.slug}>
                      {m.nombre}
                    </option>
                  ))}
                </select>

                {renombrando ? (
                  <div className="flex items-center gap-1.5">
                    <Input
                      value={nuevoNombre}
                      onChange={(e) => setNuevoNombre(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') void handleRenombrar()
                        if (e.key === 'Escape') setRenombrando(false)
                      }}
                      className="h-8 text-xs font-medium w-48 max-w-full"
                      autoFocus
                    />
                    <Button size="sm" onClick={handleRenombrar} className="h-8 px-2 text-xs">
                      <Check className="h-3.5 w-3.5" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => setRenombrando(false)}
                      className="h-8 px-2"
                    >
                      <X className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                ) : (
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => {
                      setNuevoNombre(materiaActivaObj?.nombre || '')
                      setRenombrando(true)
                    }}
                    title="Renombrar asignatura"
                    className="h-8 w-8 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                  >
                    <Edit2 className="h-3.5 w-3.5" />
                  </Button>
                )}
              </div>
            ) : (
              <span className="text-xs text-slate-500 dark:text-slate-400">
                Aún no tienes asignaturas: crea la primera con «Nueva asignatura».
              </span>
            )}
          </div>

          <div>
            {creando ? (
              <div className="flex items-center gap-1.5">
                <Input
                  value={nombreNueva}
                  onChange={(e) => setNombreNueva(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') void handleCrearMateria()
                    if (e.key === 'Escape') setCreando(false)
                  }}
                  placeholder="Nombre de la nueva asignatura"
                  className="h-8 text-xs w-52 max-w-full"
                  maxLength={80}
                  autoFocus
                />
                <Button
                  size="sm"
                  onClick={handleCrearMateria}
                  disabled={guardandoNueva || !nombreNueva.trim()}
                  className="h-8 px-2.5 text-xs"
                >
                  {guardandoNueva ? 'Guardando…' : 'Guardar'}
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setCreando(false)}
                  className="h-8 px-2"
                >
                  <X className="h-3.5 w-3.5" />
                </Button>
              </div>
            ) : (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCreando(true)}
                className="h-8 gap-1.5 text-xs"
              >
                <Plus className="h-3.5 w-3.5" /> Nueva asignatura
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Selector de Pestañas: Clases, Material, Proyectos */}
      <div role="tablist" className="flex gap-6 border-b border-slate-200 dark:border-slate-800">
        {PESTANAS.map((p) => (
          <button
            key={p.id}
            role="tab"
            type="button"
            aria-selected={activa === p.id}
            onClick={() => cambiarTab(p.id)}
            className={cn(
              '-mb-px border-b-2 pb-2.5 text-sm transition-colors cursor-pointer',
              activa === p.id
                ? 'border-indigo-600 font-medium text-slate-950 dark:border-indigo-400 dark:text-white'
                : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            )}
          >
            {p.nombre}
          </button>
        ))}
      </div>

      {/* Contenido según pestaña */}
      {activa === 'clases' && (
        <SilabosView
          embebido
          materiaActivaSlug={materiaActiva}
          onRecargarCatalogo={cargarMaterias}
        />
      )}

      {activa === 'material' && (
        <MaterialView
          embebido
          modo="materiales"
          materiaFiltro={materiaActivaObj?.nombre || '__todas__'}
        />
      )}

      {activa === 'proyectos' && (
        <MaterialView
          embebido
          modo="proyectos"
          materiaFiltro={materiaActivaObj?.nombre || '__todas__'}
        />
      )}
    </div>
  )
}
