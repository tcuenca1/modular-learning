import React, { useEffect, useState } from 'react'
import {
  Folder,
  HardDrive,
  Info,
  Save,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { Configuracion } from '@/api/types'
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

export function ConfigView() {
  const [config, setConfig] = useState<Configuracion | null>(null)
  const [carpetaMaterial, setCarpetaMaterial] = useState('')
  const [rutaObsidian, setRutaObsidian] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    async function loadConfig() {
      try {
        setLoading(true)
        const data = await api.getConfig()
        setConfig(data)
        setCarpetaMaterial(data.carpeta_material || '')
        setRutaObsidian(data.ruta_obsidian || '')
      } catch (err) {
        toast.error('Error al cargar la configuración', {
          description: err instanceof Error ? err.message : String(err),
        })
      } finally {
        setLoading(false)
      }
    }
    loadConfig()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!carpetaMaterial.trim()) {
      toast.error('Validación fallida', {
        description: 'La ruta de la carpeta de material no puede estar vacía.',
      })
      return
    }

    if (!rutaObsidian.trim()) {
      toast.error('Validación fallida', {
        description: 'La ruta de la bóveda de Obsidian no puede estar vacía.',
      })
      return
    }

    try {
      setSaving(true)
      const res = await api.saveConfig({
        carpeta_material: carpetaMaterial.trim(),
        ruta_obsidian: rutaObsidian.trim(),
      })
      setConfig(res)
      toast.success('¡Configuración guardada correctamente!', {
        description: 'Las rutas locales han sido verificadas y guardadas.',
      })
    } catch (err) {
      toast.error('Error al guardar configuración', {
        description: err instanceof Error ? err.message : String(err),
      })
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-2">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
          <p className="text-sm text-slate-500">Cargando rutas del sistema...</p>
        </div>
      </div>
    )
  }

  const matExiste =
    config?.existe_carpeta_material ?? config?.carpeta_material_existe ?? false
  const obsExiste =
    config?.existe_ruta_obsidian ?? config?.ruta_obsidian_existe ?? false

  return (
    <div className="space-y-8 pb-12 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          Configuración de Rutas Locales
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Define los directorios de almacenamiento para la ingesta de material multimodal y la bóveda de Obsidian.
        </p>
      </div>

      {/* Tarjeta de Estado de Configuración */}
      <div className="grid gap-4 sm:grid-cols-2">
        <Card className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600 dark:bg-indigo-950/60 dark:text-indigo-400">
              <Folder className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Carpeta de Material</p>
              <p className="text-sm font-semibold truncate max-w-[220px]">
                {carpetaMaterial || 'No configurada'}
              </p>
            </div>
          </div>
          <Badge variant={matExiste ? 'success' : 'destructive'}>
            {matExiste ? 'Encontrada en Disco' : 'No Encontrada'}
          </Badge>
        </Card>

        <Card className="p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-50 text-purple-600 dark:bg-purple-950/60 dark:text-purple-400">
              <HardDrive className="h-5 w-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Bóveda de Obsidian</p>
              <p className="text-sm font-semibold truncate max-w-[220px]">
                {rutaObsidian || 'No configurada'}
              </p>
            </div>
          </div>
          <Badge variant={obsExiste ? 'success' : 'destructive'}>
            {obsExiste ? 'Encontrada en Disco' : 'No Encontrada'}
          </Badge>
        </Card>
      </div>

      {/* Formulario */}
      <Card>
        <CardHeader>
          <CardTitle>Rutas de Persistencia y Trabajo</CardTitle>
          <CardDescription>
            Asegúrate de ingresar rutas absolutas válidas correspondientes a tu sistema operativo.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <Folder className="h-3.5 w-3.5 text-indigo-500" />
                Ruta Raíz de Material Académico
              </label>
              <Input
                value={carpetaMaterial}
                onChange={(e) => setCarpetaMaterial(e.target.value)}
                placeholder="Ej. C:/Users/TuUsuario/Universidad o /home/usuario/Universidad"
                className="font-mono text-xs"
                required
              />
              <p className="text-[11px] text-slate-400">
                Directorio donde organizas tus carpetas por asignatura con diapositivas, PDFs y lecturas.
              </p>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <HardDrive className="h-3.5 w-3.5 text-purple-500" />
                Ruta a la Bóveda de Obsidian (Segundo Cerebro)
              </label>
              <Input
                value={rutaObsidian}
                onChange={(e) => setRutaObsidian(e.target.value)}
                placeholder="Ej. C:/Users/TuUsuario/Documents/ObsidianVault"
                className="font-mono text-xs"
                required
              />
              <p className="text-[11px] text-slate-400">
                Directorio raíz de tu bóveda Obsidian donde se guardarán las notas sincronizadas y resúmenes de tutoría.
              </p>
            </div>

            <div className="rounded-lg border border-blue-100 bg-blue-50/50 p-4 text-xs text-blue-800 dark:border-blue-900 dark:bg-blue-950/30 dark:text-blue-300 flex items-start gap-3">
              <Info className="h-4 w-4 mt-0.5 shrink-0" />
              <div>
                <p className="font-semibold">Nota sobre directorios</p>
                <p className="mt-0.5 leading-relaxed">
                  Si la ruta a la bóveda o material aún no existe, el sistema intentará crear las subcarpetas necesarias
                  automáticamente al iniciar la ingesta o tutoría.
                </p>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <Button
                type="submit"
                disabled={saving}
                className="gap-2 bg-indigo-600 hover:bg-indigo-500 text-white px-6"
              >
                {saving ? (
                  <>
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    Guardando...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" /> Guardar Configuración
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
