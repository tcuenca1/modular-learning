import React, { useEffect, useState } from 'react'
import {
  Cloud,
  Folder,
  HardDrive,
  Palette,
  Save,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { Configuracion } from '@/api/types'
import { ThemeToggle } from '@/components/ThemeToggle'
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
        toast.error('No pude leer la configuración', {
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
      toast.error('Revisa las rutas', {
        description: 'La ruta de la carpeta de material no puede estar vacía.',
      })
      return
    }

    if (!rutaObsidian.trim()) {
      toast.error('Revisa las rutas', {
        description: 'La carpeta de notas no puede estar vacía.',
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
      toast.success('Configuración guardada', {
        description: 'Las rutas locales han sido verificadas y guardadas.',
      })
    } catch (err) {
      toast.error('No pude guardar la configuración', {
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
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
          Configuración
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Dónde está tu material de clase, apariencia de la aplicación y modo de trabajo.
        </p>
      </div>

      {/* Selector de Apariencia / Tema */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Palette className="h-5 w-5 text-indigo-500" />
            Apariencia
          </CardTitle>
          <CardDescription>
            Elige el tema visual: claro, oscuro o sincronizado automáticamente con tu sistema operativo.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ThemeToggle compacto={false} />
        </CardContent>
      </Card>

      {/* Aviso de entorno en la nube */}
      {config?.en_nube && (
        <div className="rounded-xl border border-indigo-200 bg-indigo-50/60 p-4 dark:border-indigo-900 dark:bg-indigo-950/30">
          <div className="flex items-start gap-3">
            <Cloud className="h-5 w-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
            <div className="text-xs space-y-1">
              <p className="font-semibold text-indigo-950 dark:text-indigo-200">
                Despliegue activo en la nube (Render / Neon)
              </p>
              <p className="text-slate-600 dark:text-slate-300">
                El servidor en la nube opera dentro de un contenedor Linux y no puede acceder directamente
                a rutas de tu disco local (ej. <code>C:\Users\...</code>). Para añadir archivos de clase en la nube,
                sube tus documentos individuales desde la sección <strong>Material</strong> o utiliza la sincronización
                híbrida ejecutando la app en local conectada a tu misma base de datos.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Formulario */}
      <Card>
        <CardHeader>
          <CardTitle>Carpetas</CardTitle>
          <CardDescription>
            Usa rutas completas, por ejemplo C:/Users/tu_usuario/Universidad.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="config-carpeta-material" className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <Folder className="h-3.5 w-3.5 text-indigo-500" />
                Carpeta de material
              </label>
              <Input
                id="config-carpeta-material"
                value={carpetaMaterial}
                onChange={(e) => setCarpetaMaterial(e.target.value)}
                placeholder="Ej. C:/Users/tu_usuario/Universidad"
                className="font-mono text-xs"
                required
              />
              <p className="text-[11px] text-slate-500">
                <span className={matExiste ? 'text-emerald-700 dark:text-emerald-400' : 'text-amber-700 dark:text-amber-400'}>
                  {matExiste ? 'La carpeta existe.' : 'Esta carpeta no existe todavía.'}
                </span>{' '}
                Dentro debe haber una subcarpeta por asignatura.
              </p>
            </div>

            <div className="space-y-2">
              <label htmlFor="config-ruta-obsidian" className="text-xs font-semibold text-slate-700 dark:text-slate-300 flex items-center gap-1.5">
                <HardDrive className="h-3.5 w-3.5 text-purple-500" />
                Carpeta de notas (Obsidian)
              </label>
              <Input
                id="config-ruta-obsidian"
                value={rutaObsidian}
                onChange={(e) => setRutaObsidian(e.target.value)}
                placeholder="Ej. C:/Users/tu_usuario/Documents/Obsidian"
                className="font-mono text-xs"
                required
              />
              <p className="text-[11px] text-slate-500">
                <span className={obsExiste ? 'text-emerald-700 dark:text-emerald-400' : 'text-amber-700 dark:text-amber-400'}>
                  {obsExiste ? 'La carpeta existe.' : 'Esta carpeta no existe todavía.'}
                </span>{' '}
                Aquí se guardan las notas y las guías de cada tutoría: es la carpeta de tu bóveda en la app Obsidian.
              </p>
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
                    Guardando…
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" /> Guardar
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
