import React, { useState } from 'react'
import {
  AlertCircle,
  FileText,
  Plus,
  Save,
  Trash2,
  UploadCloud,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { ClaseCronograma } from '@/api/types'
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

export function SilabosView() {
  const [file, setFile] = useState<File | null>(null)
  const [materia, setMateria] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  const [extracting, setExtracting] = useState(false)
  const [saving, setSaving] = useState(false)
  const [clases, setClases] = useState<ClaseCronograma[]>([])

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
      const droppedFile = e.dataTransfer.files[0]
      validateAndSetFile(droppedFile)
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
    if (!materia) {
      const base = f.name.replace(/\.[^/.]+$/, '').replace(/SYLLABUS/gi, '').replace(/[-_]/g, ' ').trim()
      setMateria(base)
    }
    toast.info(`Archivo seleccionado: ${f.name}`)
  }

  const handleExtraer = async () => {
    if (!file) {
      toast.error('Selecciona un archivo de sílabo primero.')
      return
    }

    try {
      setExtracting(true)
      const res = await api.extraerSilabo(file, materia)
      setMateria(res.materia)
      setClases(res.datos.clases || [])
      toast.success('¡Extracción completada con éxito!', {
        description: `Se estructuraron ${res.datos.clases?.length || 0} sesiones de clase.`,
      })
    } catch (err) {
      toast.error('Error al extraer cronograma', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setExtracting(false)
    }
  }

  const handleUpdateTema = (index: number, newTema: string) => {
    setClases((prev) => {
      const updated = [...prev]
      updated[index] = { ...updated[index], tema: newTema }
      return updated
    })
  }

  const handleUpdateSemana = (index: number, newSemana: string) => {
    setClases((prev) => {
      const updated = [...prev]
      updated[index] = { ...updated[index], semana: newSemana }
      return updated
    })
  }

  const handleAddClase = () => {
    const nextIdx = clases.length + 1
    setClases((prev) => [
      ...prev,
      {
        clase: nextIdx,
        semana: Math.ceil(nextIdx / 2),
        tema: 'Nuevo tema de clase',
        estado: 'pendiente',
      },
    ])
  }

  const handleDeleteClase = (index: number) => {
    setClases((prev) => prev.filter((_, i) => i !== index))
  }

  const handleGuardar = async () => {
    if (!materia.trim()) {
      toast.error('Indica el nombre de la asignatura.')
      return
    }
    if (clases.length === 0) {
      toast.error('No hay clases para guardar.')
      return
    }

    try {
      setSaving(true)
      const res = await api.guardarSilabo(materia.trim(), clases)
      toast.success('¡Cronograma guardado exitosamente!', {
        description: `Guardado en ${res.ruta}`,
      })
    } catch (err) {
      toast.error('Error al guardar cronograma', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-8 pb-12">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          Extracción y Gestión de Sílabos
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Convierte sílabos académicos en cronogramas estructurados mediante IA con vista previa editable.
        </p>
      </div>

      {/* Zona Drag & Drop */}
      <Card>
        <CardHeader>
          <CardTitle>Cargar Archivo de Sílabo</CardTitle>
          <CardDescription>
            Soporta documentos en formato PDF institucional, Markdown o Texto plano (.pdf, .md, .txt)
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
              {file ? file.name : 'Arrastra y suelta tu sílabo aquí o haz clic para explorar'}
            </p>
            <p className="mt-1 text-xs text-slate-400">
              {file ? `${(file.size / 1024).toFixed(1)} KB` : 'Máximo recomendado 20 MB'}
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="text-xs font-medium text-slate-600 dark:text-slate-400">
                Nombre de la Asignatura
              </label>
              <Input
                placeholder="Ej. Seguridad de la Información"
                value={materia}
                onChange={(e) => setMateria(e.target.value)}
                className="mt-1"
              />
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
                    Analizando y Extrayendo con IA...
                  </>
                ) : (
                  <>
                    <FileText className="h-4 w-4" />
                    Procesar y Extraer Cronograma
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Vista Previa Editable del Cronograma */}
      {clases.length > 0 && (
        <Card>
          <CardHeader className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <CardTitle>Vista Previa del Cronograma</CardTitle>
                <Badge variant="outline">{clases.length} clases</Badge>
              </div>
              <CardDescription>
                Revisa o edita los títulos y semanas antes de consolidar el cronograma en disco.
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={handleAddClase} className="gap-1.5">
                <Plus className="h-4 w-4" /> Añadir Clase
              </Button>
              <Button
                size="sm"
                onClick={handleGuardar}
                disabled={saving}
                className="gap-1.5 bg-emerald-600 hover:bg-emerald-500 text-white"
              >
                {saving ? (
                  <>
                    <div className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Guardando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" /> Guardar Cronograma
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
                    <TableHead>Tema Académico</TableHead>
                    <TableHead className="w-32">Estado</TableHead>
                    <TableHead className="w-16 text-right">Acción</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {clases.map((clase, idx) => (
                    <TableRow key={idx}>
                      <TableCell className="font-semibold text-slate-500">
                        {clase.clase ?? idx + 1}
                      </TableCell>
                      <TableCell>
                        <Input
                          value={clase.semana ?? ''}
                          onChange={(e) => handleUpdateSemana(idx, e.target.value)}
                          className="h-8 text-xs"
                          placeholder="1"
                        />
                      </TableCell>
                      <TableCell>
                        <Input
                          value={clase.tema}
                          onChange={(e) => handleUpdateTema(idx, e.target.value)}
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
                          onClick={() => handleDeleteClase(idx)}
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

      {clases.length === 0 && !extracting && (
        <div className="rounded-lg border border-slate-200/80 bg-slate-50/50 p-6 text-center text-slate-500 dark:border-slate-800 dark:bg-slate-900/50">
          <AlertCircle className="mx-auto h-8 w-8 text-slate-400" />
          <p className="mt-2 text-sm font-medium">Ningún cronograma cargado actualmente</p>
          <p className="text-xs text-slate-400">
            Carga un archivo de sílabo arriba para extraer las clases automáticamente.
          </p>
        </div>
      )}
    </div>
  )
}
