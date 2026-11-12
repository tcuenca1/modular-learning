import React, { useCallback, useEffect, useRef, useState } from 'react'
import {
  AlertCircle,
  Calendar,
  Check,
  Edit2,
  FileText,
  Plus,
  Save,
  Sparkles,
  Trash2,
  UploadCloud,
  X,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import { AvisoIA } from '@/components/AvisoIA'
import type { ClaseCronograma, MateriaItem, ParcialItem } from '@/api/types'
import { buscarMateriaPorClave, resolverMateriaSubida } from '@/lib/asignaturas'
import { describirCorte } from '@/lib/parciales'
import { ultimoTramo } from '@/lib/rutas'
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export function SilabosView({
  embebido = false,
  materiaActivaSlug,
  onRecargarCatalogo,
}: {
  embebido?: boolean
  materiaActivaSlug?: string
  onRecargarCatalogo?: (seleccionar?: string) => Promise<void>
}) {
  const [tabActiva, setTabActiva] = useState<'gestionar' | 'subir'>('gestionar')
  const [mostrandoSubirSilabo, setMostrandoSubirSilabo] = useState(false)

  // Catálogo de asignaturas
  const [materias, setMaterias] = useState<MateriaItem[]>([])
  const [internalMateriaActiva, setMateriaActiva] = useState<string>('')
  const materiaActiva = materiaActivaSlug || internalMateriaActiva

  // Renombrar y crear asignatura
  const [renombrando, setRenombrando] = useState(false)
  const [nuevoNombreMateria, setNuevoNombreMateria] = useState('')
  const [creandoMateria, setCreandoMateria] = useState(false)
  const [nombreNuevaMateria, setNombreNuevaMateria] = useState('')

  // Cronograma activo
  const [clasesCronograma, setClasesCronograma] = useState<ClaseCronograma[]>([])
  const [cargandoClases, setCargandoClases] = useState(true)

  // Parciales de la materia activa
  const [parciales, setParciales] = useState<ParcialItem[]>([])
  const [editandoParciales, setEditandoParciales] = useState(false)
  const [nuevoParcialNombre, setNuevoParcialNombre] = useState('Parcial 1')
  const [nuevoParcialHasta, setNuevoParcialHasta] = useState('')

  // Edición y creación de clase
  const [claseEnEdicion, setClaseEnEdicion] = useState<ClaseCronograma | null>(null)
  const [mostrandoNuevaClase, setMostrandoNuevaClase] = useState(false)
  const [nuevaClaseTema, setNuevaClaseTema] = useState('')
  const [nuevaClaseFecha, setNuevaClaseFecha] = useState('')
  const [nuevaClaseSemana, setNuevaClaseSemana] = useState('1')
  const [guardandoClase, setGuardandoClase] = useState(false)

  // Subida de sílabo nuevo (extracción)
  const [file, setFile] = useState<File | null>(null)
  const [subidaMateria, setSubidaMateria] = useState('')
  const [materiaSelect, setMateriaSelect] = useState('__nueva__')
  const [isDragging, setIsDragging] = useState(false)
  const [extracting, setExtracting] = useState(false)
  const [saving, setSaving] = useState(false)
  const [clasesExtraidas, setClasesExtraidas] = useState<ClaseCronograma[]>([])
  // De dónde salen las clases que se están revisando: un sílabo subido o un borrador de la IA
  const [origenBorrador, setOrigenBorrador] = useState<'silabo' | 'ia'>('silabo')
  const [generando, setGenerando] = useState(false)
  const [recarga, setRecarga] = useState(0)

  const cargarCatalogo = useCallback(async (seleccionar?: string) => {
    try {
      const res = await api.getMaterias()
      const lista: MateriaItem[] = res.catalogo && res.catalogo.length > 0
        ? res.catalogo
        : (res.materias || []).map((m) => ({ slug: m.toLowerCase().replace(/\s+/g, '-'), nombre: m }))

      setMaterias(lista)
      if (lista.length > 0) {
        let destino = ''
        if (seleccionar) {
          const coincidencia = buscarMateriaPorClave(lista, seleccionar)
          if (coincidencia) {
            destino = coincidencia.slug
          }
        }
        if (!destino && materiaActiva) {
          const coincideActiva = lista.find((m) => m.slug === materiaActiva)
          if (coincideActiva) {
            destino = materiaActiva
          }
        }
        if (!destino) {
          destino = lista[0].slug
        }
        setMateriaActiva(destino)
        const activaObj = lista.find((m) => m.slug === destino)
        if (activaObj) {
          setMateriaSelect((prev) => (prev === '__nueva__' ? activaObj.nombre : prev))
          setSubidaMateria((prev) => (prev ? prev : activaObj.nombre))
        }
        setCargandoClases(true)
        setRecarga((r) => r + 1)
      } else {
        setMateriaActiva('')
        setCargandoClases(false)
        setClasesCronograma([])
        setParciales([])
      }
    } catch (err) {
      toast.error('No pude cargar las asignaturas', {
        description: err instanceof Error ? err.message : String(err),
      })
      setCargandoClases(false)
    }
  }, [materiaActiva])

  const cambiarMateria = (slug: string) => {
    if (slug === materiaActiva) return
    setMateriaActiva(slug)
    setCargandoClases(true)
    setRenombrando(false)
    setClaseEnEdicion(null)
    setMostrandoNuevaClase(false)
    setEditandoParciales(false)
  }

  useEffect(() => {
    api
      .getMaterias()
      .then((res) => {
        const lista: MateriaItem[] =
          res.catalogo && res.catalogo.length > 0
            ? res.catalogo
            : (res.materias || []).map((m) => ({ slug: m.toLowerCase().replace(/\s+/g, '-'), nombre: m }))
        setMaterias(lista)
        if (lista.length > 0) {
          setMateriaActiva(lista[0].slug)
          setCargandoClases(true)
        } else {
          setCargandoClases(false)
        }
      })
      .catch((err) => {
        toast.error('No pude cargar las asignaturas', {
          description: err instanceof Error ? err.message : String(err),
        })
        setCargandoClases(false)
      })
  }, [])

  useEffect(() => {
    if (!materiaActiva) return
    let cancelado = false
    Promise.all([
      api.getCronogramaMateria(materiaActiva),
      api.getParciales(materiaActiva).catch(() => ({ parciales: [] })),
    ])
      .then(([resClases, resParciales]) => {
        if (!cancelado) {
          setClasesCronograma(resClases.clases || [])
          setParciales(resParciales.parciales || [])
        }
      })
      .catch(() => {
        if (!cancelado) {
          setClasesCronograma([])
          setParciales([])
        }
      })
      .finally(() => {
        if (!cancelado) {
          setCargandoClases(false)
        }
      })

    return () => {
      cancelado = true
    }
  }, [materiaActiva, recarga])

  // --- Handlers Materia ---
  const handleRenombrarMateria = async () => {
    if (!nuevoNombreMateria.trim()) {
      toast.error('El nombre no puede estar vacío.')
      return
    }
    try {
      await api.renombrarMateria(materiaActiva, nuevoNombreMateria.trim())
      toast.success('Asignatura renombrada')
      setRenombrando(false)
      await cargarCatalogo(materiaActiva)
    } catch (err) {
      toast.error('No se pudo renombrar', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleCrearMateria = async () => {
    if (!nombreNuevaMateria.trim()) {
      toast.error('Escribe el nombre de la asignatura.')
      return
    }
    try {
      await api.createMateria(nombreNuevaMateria.trim())
      toast.success('Asignatura añadida')
      setNombreNuevaMateria('')
      setCreandoMateria(false)
      await cargarCatalogo()
    } catch (err) {
      toast.error('No se pudo crear la asignatura', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleEliminarMateria = async () => {
    const mObj = materias.find((m) => m.slug === materiaActiva)
    const nombre = mObj?.nombre || materiaActiva
    if (
      !window.confirm(
        `¿Eliminar la asignatura "${nombre}"?\n\n` +
        `Esto eliminará permanentemente su cronograma y desvinculará sus materiales registrados.`
      )
    ) {
      return
    }

    try {
      await api.eliminarMateria(materiaActiva)
      toast.success(`Asignatura "${nombre}" eliminada`)
      await cargarCatalogo()
      if (onRecargarCatalogo) {
        await onRecargarCatalogo()
      }
    } catch (err) {
      toast.error('No se pudo eliminar la asignatura', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleEliminarCronograma = async () => {
    const mObj = materias.find((m) => m.slug === materiaActiva)
    const nombre = mObj?.nombre || materiaActiva
    if (
      !window.confirm(
        `¿Vaciar el cronograma de "${nombre}"?\n\n` +
        `Se borrarán todas sus clases pero se conservará la asignatura en el catálogo.`
      )
    ) {
      return
    }

    try {
      await api.eliminarCronograma(materiaActiva)
      toast.success('Cronograma vaciado')
      setClasesCronograma([])
    } catch (err) {
      toast.error('No se pudo vaciar el cronograma', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  // --- Handlers Parciales ---
  const handleGuardarParcial = async () => {
    if (!nuevoParcialNombre.trim() || !nuevoParcialHasta.trim()) {
      toast.error('Indica el nombre del parcial y la clase donde termina.')
      return
    }
    const actualizados = [...parciales.filter((p) => p.nombre !== nuevoParcialNombre), {
      nombre: nuevoParcialNombre.trim(),
      hasta: nuevoParcialHasta.trim(),
    }]
    try {
      await api.guardarParciales(materiaActiva, actualizados)
      setParciales(actualizados)
      setNuevoParcialNombre('')
      setNuevoParcialHasta('')
      setEditandoParciales(false)
      toast.success('Parcial guardado')
    } catch (err) {
      toast.error('No pude guardar el parcial', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleEliminarParcial = async (nombreParcial: string) => {
    const actualizados = parciales.filter((p) => p.nombre !== nombreParcial)
    try {
      await api.guardarParciales(materiaActiva, actualizados)
      setParciales(actualizados)
      toast.success('Parcial eliminado')
    } catch {
      toast.error('No pude eliminar el parcial')
    }
  }

  // --- Handlers Clases ---
  const handleToggleEstadoClase = async (clase: ClaseCronograma) => {
    const nuevoEstado = clase.estado?.toLowerCase() === 'completado' ? 'pendiente' : 'completado'
    const id = clase.id || clase.tema
    try {
      await api.cambiarEstadoClase(materiaActiva, id, nuevoEstado)
      setClasesCronograma((prev) =>
        prev.map((c) => (c.id === clase.id ? { ...c, estado: nuevoEstado } : c))
      )
      toast.success(
        nuevoEstado === 'completado'
          ? 'Clase marcada como completada'
          : 'Clase devuelta a pendiente'
      )
    } catch (err) {
      toast.error('No pude cambiar el estado de la clase', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleEliminarClase = async (clase: ClaseCronograma) => {
    if (!window.confirm(`¿Eliminar la clase "${clase.tema}" del cronograma?`)) return
    const id = clase.id || clase.tema
    try {
      await api.eliminarClase(materiaActiva, id)
      toast.success('Clase eliminada')
      setClasesCronograma((prev) => prev.filter((c) => c.id !== clase.id))
    } catch (err) {
      toast.error('No pude eliminar la clase', {
        description: err instanceof Error ? err.message : String(err),
      })
    }
  }

  const handleGuardarEdicionClase = async () => {
    if (!claseEnEdicion) return
    const id = claseEnEdicion.id || claseEnEdicion.tema
    try {
      setGuardandoClase(true)
      const res = await api.editarClase(materiaActiva, id, {
        tema: claseEnEdicion.tema,
        fecha: claseEnEdicion.fecha,
        semana: claseEnEdicion.semana,
        contenido: claseEnEdicion.contenido,
      })
      setClasesCronograma((prev) =>
        prev.map((c) => (c.id === claseEnEdicion.id ? { ...c, ...res.clase } : c))
      )
      toast.success('Clase actualizada')
      setClaseEnEdicion(null)
    } catch (err) {
      toast.error('No pude guardar los cambios', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setGuardandoClase(false)
    }
  }

  const handleAgregarNuevaClase = async () => {
    if (!nuevaClaseTema.trim()) {
      toast.error('Escribe el tema de la clase.')
      return
    }
    try {
      setGuardandoClase(true)
      const nextIdx = clasesCronograma.length + 1
      const res = await api.agregarClase(materiaActiva, {
        clase: nextIdx,
        tema: nuevaClaseTema.trim(),
        fecha: nuevaClaseFecha.trim(),
        semana: nuevaClaseSemana.trim() || '1',
        estado: 'pendiente',
      })
      setClasesCronograma((prev) => [...prev, res.clase])
      toast.success('Clase agregada al cronograma')
      setNuevaClaseTema('')
      setNuevaClaseFecha('')
      setMostrandoNuevaClase(false)
    } catch (err) {
      toast.error('No pude agregar la clase', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setGuardandoClase(false)
    }
  }

  // --- Handlers Subida y Extracción de Sílabos ---
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0])
    }
  }


  const handleSelectMateriaSubida = (valor: string) => {
    setMateriaSelect(valor)
    if (valor === '__nueva__') {
      setSubidaMateria('')
    } else {
      setSubidaMateria(valor)
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0])
    }
  }

  const validateAndSetFile = (f: File) => {
    const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase()
    if (!['.pdf', '.md', '.txt'].includes(ext)) {
      toast.error('Formato no soportado', {
        description: 'Por favor selecciona un archivo PDF, Markdown o TXT.',
      })
      return
    }
    setFile(f)
    const base = f.name
      .replace(/\.[^/.]+$/, '')
      .replace(/SYLLABUS/gi, '')
      .replace(/[-_]/g, ' ')
      .trim()
    const nueva = resolverMateriaSubida(materias, base, { materiaSelect, subidaMateria })
    setMateriaSelect(nueva.materiaSelect)
    setSubidaMateria(nueva.subidaMateria)
    toast.info(`Archivo seleccionado: ${f.name}`)
  }

  const handleExtraer = async () => {
    if (!file) {
      toast.error('Primero elige el archivo del sílabo.')
      return
    }

    try {
      setExtracting(true)
      const res = await api.extraerSilabo(file, subidaMateria)
      if (res.materia) {
        const nueva = resolverMateriaSubida(materias, res.materia, {
          materiaSelect,
          subidaMateria,
        })
        setMateriaSelect(nueva.materiaSelect)
        setSubidaMateria(nueva.subidaMateria)
      }
      setClasesExtraidas(res.datos.clases || [])
      setOrigenBorrador('silabo')
      toast.success('Clases extraídas', {
        description: `Se estructuraron ${res.datos.clases?.length || 0} sesiones de clase.`,
      })
    } catch (err) {
      toast.error('No pude leer el sílabo', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setExtracting(false)
    }
  }

  const handleGenerarConIA = async () => {
    const nombre = materiaSeleccionadaObj?.nombre
    if (!nombre || generando) return
    try {
      setGenerando(true)
      const res = await api.generarCronograma(nombre)
      const clases = res.datos.clases || []
      setClasesExtraidas(clases)
      setOrigenBorrador('ia')
      setFile(null)
      setMateriaSelect(nombre)
      setSubidaMateria(nombre)
      setMostrandoSubirSilabo(true) // abre la pantalla de revisión, con las clases ya cargadas
      toast.success('Borrador generado', {
        description: `${clases.length} clases de introducción. Revísalas antes de guardar.`,
      })
    } catch (err) {
      toast.error('No pude generar las clases', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setGenerando(false)
    }
  }

  const handleGuardarSilaboExtraido = async () => {
    if (!subidaMateria.trim()) {
      toast.error('Escribe el nombre de la asignatura.')
      return
    }
    if (clasesExtraidas.length === 0) {
      toast.error('No hay clases para guardar.')
      return
    }

    try {
      setSaving(true)
      const res = await api.guardarSilabo(subidaMateria.trim(), clasesExtraidas)
      toast.success('Cronograma guardado', {
        description: `Guardado en ${ultimoTramo(res.ruta)}`,
      })
      setClasesExtraidas([])
      setOrigenBorrador('silabo')
      setFile(null)
      setMostrandoSubirSilabo(false)
      await cargarCatalogo(subidaMateria.trim())
      if (onRecargarCatalogo) {
        await onRecargarCatalogo(subidaMateria.trim())
      }
      setTabActiva('gestionar')
    } catch (err) {
      toast.error('No pude guardar el cronograma', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setSaving(false)
    }
  }

  const materiaSeleccionadaObj = materias.find((m) => m.slug === materiaActiva)

  // Embebido, la asignatura activa la elige el padre: si es una recién creada que este panel
  // aún no conoce, se recarga el catálogo (una vez por asignatura) para no quedar en blanco.
  const catalogoPedidoPara = useRef('')
  useEffect(() => {
    if (!embebido || !materiaActivaSlug || materias.some((m) => m.slug === materiaActivaSlug)) return
    if (catalogoPedidoPara.current === materiaActivaSlug) return
    catalogoPedidoPara.current = materiaActivaSlug
    void cargarCatalogo(materiaActivaSlug)
  }, [embebido, materiaActivaSlug, materias, cargarCatalogo])

  // El panel de subir sílabo parte de la asignatura activa, no de «Nueva asignatura…»
  const nombreActiva = materiaSeleccionadaObj?.nombre
  const [nombreSincronizado, setNombreSincronizado] = useState<string>()
  if (nombreActiva && nombreActiva !== nombreSincronizado) {
    setNombreSincronizado(nombreActiva)
    setMateriaSelect(nombreActiva)
    setSubidaMateria(nombreActiva)
  }

  return (
    <div className="space-y-6 pb-12">
      {!embebido && (
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
            Cronogramas y Sílabos
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Administra tus asignaturas, define dónde termina cada parcial, cambia estados de clase y extrae nuevos sílabos.
          </p>
        </div>
      )}

      {/* Selector de modo: Gestionar vs Subir (solo si no está embebido) */}
      {!embebido && (
        <div className="flex gap-2 border-b border-slate-200 pb-3 dark:border-slate-800">
          <Button
            variant={tabActiva === 'gestionar' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => { setTabActiva('gestionar'); setMostrandoSubirSilabo(false); }}
            className="gap-2"
          >
            <Calendar className="h-4 w-4" />
            Gestionar Asignaturas y Clases
          </Button>
          <Button
            variant={tabActiva === 'subir' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => { setTabActiva('subir'); setMostrandoSubirSilabo(true); }}
            className="gap-2"
          >
            <UploadCloud className="h-4 w-4" />
            Subir e Importar Sílabo
          </Button>
        </div>
      )}

      {(tabActiva === 'gestionar' && !mostrandoSubirSilabo) ? (
        <div className="space-y-6">
          {/* Fila de Asignaturas (solo si no está embebido) */}
          {!embebido && (
            <Card>
            <CardHeader className="p-4 pb-2">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <CardTitle className="text-base font-semibold">Tus asignaturas</CardTitle>
                <div className="flex items-center gap-2">
                  {creandoMateria ? (
                    <div className="flex items-center gap-2">
                      <Input
                        value={nombreNuevaMateria}
                        onChange={(e) => setNombreNuevaMateria(e.target.value)}
                        placeholder="Nombre de la nueva asignatura"
                        className="h-8 text-xs w-56"
                      />
                      <Button size="sm" onClick={handleCrearMateria} className="h-8 px-2 text-xs">
                        Guardar
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => setCreandoMateria(false)}
                        className="h-8 px-2"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ) : (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCreandoMateria(true)}
                      className="h-8 gap-1.5 text-xs"
                    >
                      <Plus className="h-3.5 w-3.5" /> Nueva asignatura
                    </Button>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-4 pt-1">
              <div className="flex flex-wrap gap-2">
                {materias.map((m) => {
                  const activa = m.slug === materiaActiva
                  return (
                    <button
                      key={m.slug}
                      type="button"
                      onClick={() => cambiarMateria(m.slug)}
                      className={`cursor-pointer rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors ${
                        activa
                          ? 'border-indigo-600 bg-indigo-50 text-indigo-900 dark:border-indigo-400 dark:bg-indigo-950/60 dark:text-indigo-200'
                          : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-300 dark:hover:bg-slate-800'
                      }`}
                    >
                      {m.nombre}
                    </button>
                  )
                })}
              </div>
            </CardContent>
          </Card>
          )}

          {/* Gestión de la Asignatura Seleccionada */}
          {materiaSeleccionadaObj && (
            <>
            <Card>
              <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div className="min-w-0 space-y-1">
                  <div className="flex min-w-0 items-center gap-2">
                    {renombrando ? (
                      <div className="flex items-center gap-2">
                        <Input
                          value={nuevoNombreMateria}
                          onChange={(e) => setNuevoNombreMateria(e.target.value)}
                          className="h-8 text-sm font-semibold max-w-sm"
                        />
                        <Button size="sm" onClick={handleRenombrarMateria} className="h-8 gap-1">
                          <Check className="h-3.5 w-3.5" /> Guardar
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setRenombrando(false)}
                          className="h-8"
                        >
                          <X className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    ) : (
                      <>
                        <CardTitle className="min-w-0 text-xl [overflow-wrap:anywhere]">
                          {materiaSeleccionadaObj.nombre}
                        </CardTitle>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => { setNuevoNombreMateria(materiaSeleccionadaObj?.nombre || ""); setRenombrando(true); }}
                          title="Renombrar asignatura"
                          className="h-7 w-7 text-slate-400 hover:text-slate-600"
                        >
                          <Edit2 className="h-3.5 w-3.5" />
                        </Button>
                      </>
                    )}
                  </div>
                  <CardDescription>
                    {clasesCronograma.length} {clasesCronograma.length === 1 ? 'clase' : 'clases'} en el cronograma
                  </CardDescription>
                </div>

                <div className="flex flex-wrap items-center gap-2">
                  <Button
                    variant={mostrandoSubirSilabo ? 'secondary' : 'default'}
                    size="sm"
                    onClick={() => setMostrandoSubirSilabo(!mostrandoSubirSilabo)}
                    className="gap-1.5 text-xs"
                  >
                    <UploadCloud className="h-3.5 w-3.5" />
                    {mostrandoSubirSilabo ? 'Volver a clases' : 'Subir sílabo'}
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setMostrandoNuevaClase(true)}
                    className="gap-1.5 text-xs"
                  >
                    <Plus className="h-3.5 w-3.5" /> Añadir clase
                  </Button>
                </div>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* Fin de cada parcial */}
                <div className="rounded-lg border border-slate-200 bg-slate-50/50 p-4 dark:border-slate-800 dark:bg-slate-900/50 space-y-3">
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                    <div className="min-w-0">
                      <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
                        Fin de cada parcial
                      </h3>
                      <p className="text-xs text-slate-500">
                        Elige la última clase de cada parcial: sirve para generar guías de todo el parcial.
                      </p>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditandoParciales(!editandoParciales)}
                      className="text-xs h-7"
                    >
                      {editandoParciales ? 'Cerrar' : '+ Añadir / editar parciales'}
                    </Button>
                  </div>

                  {parciales.length > 0 && (
                    <div className="flex flex-wrap gap-2 pt-1">
                      {parciales.map((p) => (
                        <div
                          key={p.nombre}
                          className="flex items-center gap-1.5 rounded-full border border-indigo-200 bg-white px-3 py-1 text-xs font-medium text-indigo-900 dark:border-indigo-800 dark:bg-slate-950 dark:text-indigo-200"
                        >
                          <span>{p.nombre}: hasta {describirCorte(clasesCronograma, p.hasta)}</span>
                          <button
                            type="button"
                            onClick={() => handleEliminarParcial(p.nombre)}
                            className="ml-1 text-slate-400 hover:text-red-600"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {editandoParciales && (
                    <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                      <Input
                        value={nuevoParcialNombre}
                        onChange={(e) => setNuevoParcialNombre(e.target.value)}
                        placeholder="Ej. Parcial 1"
                        className="h-8 text-xs w-36"
                      />
                      <select
                        value={nuevoParcialHasta}
                        onChange={(e) => setNuevoParcialHasta(e.target.value)}
                        className="h-8 rounded-md border border-slate-200 bg-white px-2 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200 max-w-xs"
                      >
                        <option value="">Selecciona clase límite…</option>
                        {clasesCronograma.map((c, i) => (
                          <option key={c.id || i} value={c.id ? String(c.id) : String(i)}>
                            {c.fecha ? `[${c.fecha}] ` : ''}{c.tema}
                          </option>
                        ))}
                      </select>
                      <Button size="sm" onClick={handleGuardarParcial} disabled={!nuevoParcialNombre.trim() || !nuevoParcialHasta.trim()} className="h-8 text-xs">
                        Guardar parcial
                      </Button>
                    </div>
                  )}
                </div>

                {/* Formulario Añadir Clase */}
                {mostrandoNuevaClase && (
                  <div className="rounded-lg border border-indigo-200 bg-indigo-50/40 p-4 dark:border-indigo-900 dark:bg-indigo-950/20 space-y-3">
                    <h4 className="text-xs font-semibold text-indigo-900 dark:text-indigo-200">
                      Nueva clase para {materiaSeleccionadaObj.nombre}
                    </h4>
                    <div className="grid gap-3 sm:grid-cols-4">
                      <div className="sm:col-span-2">
                        <Input
                          placeholder="Tema de la clase"
                          value={nuevaClaseTema}
                          onChange={(e) => setNuevaClaseTema(e.target.value)}
                          className="h-8 text-xs"
                        />
                      </div>
                      <div>
                        <Input
                          placeholder="Fecha (dd/mm/aaaa)"
                          value={nuevaClaseFecha}
                          onChange={(e) => setNuevaClaseFecha(e.target.value)}
                          className="h-8 text-xs"
                        />
                      </div>
                      <div>
                        <Input
                          placeholder="Semana (ej. 1)"
                          value={nuevaClaseSemana}
                          onChange={(e) => setNuevaClaseSemana(e.target.value)}
                          className="h-8 text-xs"
                        />
                      </div>
                    </div>
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setMostrandoNuevaClase(false)}
                        className="h-8 text-xs"
                      >
                        Cancelar
                      </Button>
                      <Button
                        size="sm"
                        onClick={handleAgregarNuevaClase}
                        disabled={guardandoClase}
                        className="h-8 text-xs bg-indigo-600 hover:bg-indigo-500 text-white"
                      >
                        Guardar clase
                      </Button>
                    </div>
                  </div>
                )}

                {/* Modal / Formulario Editar Clase */}
                {claseEnEdicion && (
                  <div className="rounded-lg border border-amber-200 bg-amber-50/50 p-4 dark:border-amber-900 dark:bg-amber-950/20 space-y-3">
                    <h4 className="text-xs font-semibold text-amber-900 dark:text-amber-200">
                      Editar Clase: {claseEnEdicion.tema}
                    </h4>
                    <div className="grid gap-3 sm:grid-cols-3">
                      <div className="sm:col-span-2">
                        <label className="text-[11px] text-slate-500">Tema</label>
                        <Input
                          value={claseEnEdicion.tema}
                          onChange={(e) =>
                            setClaseEnEdicion({ ...claseEnEdicion, tema: e.target.value })
                          }
                          className="h-8 text-xs mt-1"
                        />
                      </div>
                      <div>
                        <label className="text-[11px] text-slate-500">Fecha</label>
                        <Input
                          value={claseEnEdicion.fecha || ''}
                          onChange={(e) =>
                            setClaseEnEdicion({ ...claseEnEdicion, fecha: e.target.value })
                          }
                          className="h-8 text-xs mt-1"
                        />
                      </div>
                    </div>
                    <div>
                      <label className="text-[11px] text-slate-500">Contenido o Resumen</label>
                      <Input
                        value={claseEnEdicion.contenido || ''}
                        onChange={(e) =>
                          setClaseEnEdicion({ ...claseEnEdicion, contenido: e.target.value })
                        }
                        placeholder="Contenido teórico abordado"
                        className="h-8 text-xs mt-1"
                      />
                    </div>
                    <div className="flex justify-end gap-2 pt-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setClaseEnEdicion(null)}
                        className="h-8 text-xs"
                      >
                        Cancelar
                      </Button>
                      <Button
                        size="sm"
                        onClick={handleGuardarEdicionClase}
                        disabled={guardandoClase}
                        className="h-8 text-xs bg-amber-600 hover:bg-amber-500 text-white"
                      >
                        Actualizar
                      </Button>
                    </div>
                  </div>
                )}

                {/* Tabla de Clases */}
                {cargandoClases ? (
                  <div className="py-8 text-center text-sm text-slate-500">
                    Cargando clases del cronograma…
                  </div>
                ) : clasesCronograma.length === 0 ? (
                  <div className="rounded-lg border border-slate-200/80 bg-slate-50/50 p-6 text-center text-slate-500 dark:border-slate-800 dark:bg-slate-900/50">
                    <AlertCircle className="mx-auto h-8 w-8 text-slate-400" />
                    <p className="mt-2 text-sm font-medium text-slate-800 dark:text-slate-200">
                      No hay clases registradas en este cronograma
                    </p>
                    <p className="mt-1 text-xs text-slate-400">
                      Sube el sílabo oficial para estructurar las sesiones automáticamente o añade clases manualmente.
                    </p>
                    <div className="mt-4 flex flex-wrap justify-center gap-3">
                      <Button
                        size="sm"
                        onClick={() => setMostrandoSubirSilabo(true)}
                        className="gap-1.5 text-xs bg-indigo-600 hover:bg-indigo-500 text-white"
                      >
                        <UploadCloud className="h-3.5 w-3.5" /> Subir sílabo
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setMostrandoNuevaClase(true)}
                        className="gap-1.5 text-xs"
                      >
                        <Plus className="h-3.5 w-3.5" /> Añadir clase
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleGenerarConIA}
                        disabled={generando}
                        className="gap-1.5 text-xs"
                      >
                        <Sparkles className="h-3.5 w-3.5" />
                        {generando ? (
                          'Generando…'
                        ) : (
                          <>
                            Generar con IA <AvisoIA />
                          </>
                        )}
                      </Button>
                    </div>
                    <p className="mt-3 text-xs text-slate-500">
                      «Generar con IA» propone unas 10 clases de introducción a la materia (nivel medio) que
                      puedes revisar antes de guardar.
                    </p>
                  </div>
                ) : (
                  <div className="rounded-lg border border-slate-200 dark:border-slate-800">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead className="w-12 text-center">#</TableHead>
                          <TableHead className="w-24">Fecha</TableHead>
                          <TableHead>Tema académico</TableHead>
                          <TableHead className="w-28 text-center">Estado</TableHead>
                          <TableHead className="w-24 text-center">Materiales</TableHead>
                          <TableHead className="w-20 text-right">Acción</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {clasesCronograma.map((c, idx) => {
                          const completada = c.estado?.toLowerCase() === 'completado'
                          return (
                            <TableRow key={c.id || idx}>
                              <TableCell className="text-center font-mono text-xs text-slate-400">
                                {c.clase ?? idx + 1}
                              </TableCell>
                              <TableCell className="text-xs text-slate-500">
                                {c.fecha || '—'}
                              </TableCell>
                              <TableCell>
                                <span className="font-medium text-slate-900 dark:text-slate-100 text-sm">
                                  {c.tema}
                                </span>
                                {c.contenido && (
                                  <p className="text-xs text-slate-500 truncate max-w-md">
                                    {c.contenido}
                                  </p>
                                )}
                              </TableCell>
                              <TableCell className="text-center">
                                <button
                                  type="button"
                                  onClick={() => handleToggleEstadoClase(c)}
                                  className="cursor-pointer transition-transform hover:scale-105"
                                  title="Haz clic para alternar entre pendiente y completado"
                                >
                                  <Badge variant={completada ? 'success' : 'secondary'}>
                                    {completada ? 'Completado' : 'Pendiente'}
                                  </Badge>
                                </button>
                              </TableCell>
                              <TableCell className="text-center text-xs text-slate-500">
                                {c.materiales_asociados?.length || 0}
                              </TableCell>
                              <TableCell className="text-right">
                                <div className="flex items-center justify-end gap-1">
                                  <Button
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => setClaseEnEdicion(c)}
                                    title="Editar clase"
                                    className="h-7 w-7 text-slate-400 hover:text-slate-700"
                                  >
                                    <Edit2 className="h-3.5 w-3.5" />
                                  </Button>
                                  <Button
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => handleEliminarClase(c)}
                                    title="Eliminar clase"
                                    className="h-7 w-7 text-slate-400 hover:text-red-600"
                                  >
                                    <Trash2 className="h-3.5 w-3.5" />
                                  </Button>
                                </div>
                              </TableCell>
                            </TableRow>
                          )
                        })}
                      </TableBody>
                    </Table>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Zona peligrosa */}
            <div className="rounded-lg border border-rose-200 bg-rose-50/20 p-5 dark:border-rose-950 dark:bg-rose-950/10">
              <h3 className="text-sm font-semibold text-rose-900 dark:text-rose-200">
                Zona peligrosa
              </h3>
              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                Acciones destructivas e irreversibles para los datos de esta asignatura.
              </p>
              <div className="mt-4 flex flex-wrap items-center gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleEliminarCronograma}
                  className="h-auto max-w-full gap-1.5 whitespace-normal break-words py-1.5 text-left text-xs text-amber-700 border-amber-300 hover:bg-amber-50 dark:text-amber-400 dark:border-amber-900/60 dark:hover:bg-amber-950/40"
                >
                  <span className="min-w-0 [overflow-wrap:anywhere]">
                    Vaciar cronograma de {materiaSeleccionadaObj.nombre}
                  </span>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleEliminarMateria}
                  className="h-auto max-w-full gap-1.5 whitespace-normal break-words py-1.5 text-left text-xs text-rose-600 border-rose-200 hover:bg-rose-50 dark:border-rose-900/60 dark:hover:bg-rose-950/40"
                >
                  <Trash2 className="h-3.5 w-3.5 shrink-0" />
                  <span className="min-w-0 [overflow-wrap:anywhere]">
                    Eliminar asignatura {materiaSeleccionadaObj.nombre}
                  </span>
                </Button>
              </div>
            </div>
            </>
          )}
        </div>
      ) : (
        /* Modo Subir Nuevo Sílabo */
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Subir e importar sílabo</CardTitle>
              <CardDescription>
                PDF, Markdown o texto plano. La IA estructurará las sesiones de clase automáticamente.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 text-center transition-all ${
                  isDragging
                    ? 'border-indigo-600 bg-indigo-50/50 dark:border-indigo-400 dark:bg-indigo-950/20'
                    : 'border-slate-200 hover:border-slate-300 dark:border-slate-800 dark:hover:border-slate-700'
                }`}
              >
                <input
                  type="file"
                  accept=".pdf,.md,.txt"
                  onChange={handleFileInput}
                  className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
                  id="file-upload"
                />
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
                  <UploadCloud className="h-6 w-6" />
                </div>
                <p className="mt-3 text-sm font-medium text-slate-900 dark:text-white">
                  {file ? file.name : 'Arrastra el sílabo aquí o haz clic para elegirlo'}
                </p>
                <p className="mt-1 text-xs text-slate-400">
                  {file ? `${(file.size / 1024).toFixed(1)} KB` : 'Hasta 20 MB'}
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <div>
                    <label htmlFor="silabo-asignatura" className="text-xs font-medium text-slate-600 dark:text-slate-400">
                      Asignatura
                    </label>
                    <select
                      id="silabo-asignatura"
                      value={materiaSelect}
                      onChange={(e) => handleSelectMateriaSubida(e.target.value)}
                      className="mt-1 h-9 w-full rounded-md border border-slate-200 bg-white px-3 text-xs font-medium text-slate-900 shadow-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-slate-800 dark:bg-slate-950 dark:text-slate-200"
                    >
                      {materias.map((m) => (
                        <option key={m.slug} value={m.nombre}>
                          {m.nombre}
                        </option>
                      ))}
                      <option value="__nueva__">Nueva asignatura…</option>
                    </select>
                  </div>
                  {materiaSelect === '__nueva__' && (
                    <div>
                      <Input
                        placeholder="Nombre de la nueva asignatura"
                        value={subidaMateria}
                        onChange={(e) => setSubidaMateria(e.target.value)}
                        className="mt-1"
                        autoFocus
                      />
                    </div>
                  )}
                </div>
                <div className="flex items-end">
                  <Button
                    onClick={handleExtraer}
                    disabled={!file || extracting}
                    className="w-full gap-2"
                  >
                    {extracting ? (
                      <>
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                        Leyendo el sílabo…
                      </>
                    ) : (
                      <>
                        <FileText className="h-4 w-4" />
                        Extraer clases <AvisoIA />
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Vista Previa Editable del Cronograma Extraído */}
          {clasesExtraidas.length > 0 && (
            <Card>
              <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <CardTitle>
                      {origenBorrador === 'ia'
                        ? 'Revisa el borrador generado por IA'
                        : 'Revisa las clases extraídas'}
                    </CardTitle>
                    <Badge variant="outline">{clasesExtraidas.length} clases</Badge>
                  </div>
                  <CardDescription>
                    {origenBorrador === 'ia'
                      ? 'Es un plan general de introducción, sin fechas ni datos de tu curso. Edita, quita o corrige lo que haga falta antes de guardar.'
                      : 'Corrige lo que haga falta antes de guardar en el cronograma.'}
                  </CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    size="sm"
                    onClick={handleGuardarSilaboExtraido}
                    disabled={saving}
                    className="gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white"
                  >
                    {saving ? (
                      <>
                        <div className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                        Guardando…
                      </>
                    ) : (
                      <>
                        <Save className="h-4 w-4" /> Guardar cronograma
                      </>
                    )}
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="rounded-lg border border-slate-200 dark:border-slate-800">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead className="w-16">#</TableHead>
                        <TableHead className="w-28">Semana</TableHead>
                        <TableHead>Tema académico</TableHead>
                        <TableHead className="w-32">Estado</TableHead>
                        <TableHead className="w-16 text-right">Acción</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {clasesExtraidas.map((clase, idx) => (
                        <TableRow key={idx}>
                          <TableCell className="font-semibold text-slate-500">
                            {clase.clase ?? idx + 1}
                          </TableCell>
                          <TableCell>
                            <Input
                              value={clase.semana ?? ''}
                              onChange={(e) => {
                                const val = e.target.value
                                setClasesExtraidas((prev) =>
                                  prev.map((c, i) => (i === idx ? { ...c, semana: val } : c))
                                )
                              }}
                              className="h-8 text-xs"
                              placeholder="1"
                            />
                          </TableCell>
                          <TableCell>
                            <Input
                              value={clase.tema}
                              onChange={(e) => {
                                const val = e.target.value
                                setClasesExtraidas((prev) =>
                                  prev.map((c, i) => (i === idx ? { ...c, tema: val } : c))
                                )
                              }}
                              className="h-8 text-sm"
                            />
                          </TableCell>
                          <TableCell>
                            <Badge
                              variant={
                                clase.estado?.toLowerCase() === 'completado' ? 'success' : 'secondary'
                              }
                            >
                              {clase.estado || 'pendiente'}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-right">
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() =>
                                setClasesExtraidas((prev) => prev.filter((_, i) => i !== idx))
                              }
                              className="h-8 w-8 text-slate-400 hover:text-red-600"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
