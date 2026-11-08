import { useCallback, useEffect, useState } from 'react'
import {
  Check,
  ChevronDown,
  ChevronUp,
  Copy,
  Cpu,
  Folder,
  FolderCheck,
  FolderX,
  Globe,
  Network,
  RefreshCw,
  Settings,
  Terminal,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { PluginInfo } from '@/api/types'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'

const ICON_MAP: Record<string, { icon: typeof Network; color: string }> = {
  cisco: {
    icon: Network,
    color: 'text-sky-500 bg-sky-50 border-sky-100 dark:bg-sky-950/40 dark:border-sky-800',
  },
  nodered: {
    icon: Cpu,
    color: 'text-rose-500 bg-rose-50 border-rose-100 dark:bg-rose-950/40 dark:border-rose-800',
  },
  web: {
    icon: Globe,
    color: 'text-emerald-500 bg-emerald-50 border-emerald-100 dark:bg-emerald-950/40 dark:border-emerald-800',
  },
}

export function PluginsView() {
  const [plugins, setPlugins] = useState<PluginInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [updatingPlugin, setUpdatingPlugin] = useState<string | null>(null)
  const [editingPlugin, setEditingPlugin] = useState<string | null>(null)
  const [carpetaInput, setCarpetaInput] = useState<string>('')
  const [guardandoConfig, setGuardandoConfig] = useState(false)
  const [expandedMemory, setExpandedMemory] = useState<Record<string, boolean>>({})
  const [logOutput, setLogOutput] = useState<string>(
    'Aquí aparece el resultado cuando actualizas un plugin.'
  )
  const [haActualizado, setHaActualizado] = useState(false)
  const [copied, setCopied] = useState(false)

  const cargarPlugins = useCallback(async () => {
    try {
      const res = await api.getPlugins()
      if (res.plugins) {
        setPlugins(res.plugins)
      }
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      toast.error('No se pudieron cargar los plugins', { description: msg })
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let cancelado = false
    api
      .getPlugins()
      .then((res) => {
        if (!cancelado && res.plugins) {
          setPlugins(res.plugins)
        }
      })
      .catch((err) => {
        if (!cancelado) {
          const msg = err instanceof Error ? err.message : String(err)
          toast.error('No se pudieron cargar los plugins', { description: msg })
        }
      })
      .finally(() => {
        if (!cancelado) {
          setLoading(false)
        }
      })
    return () => {
      cancelado = true
    }
  }, [])

  const handleActualizar = async (opcion: string) => {
    try {
      setHaActualizado(true)
      setUpdatingPlugin(opcion)
      toast.info(`Actualizando ${opcion}…`)
      const res = await api.actualizarPlugin(opcion)
      setLogOutput(`[${new Date().toLocaleTimeString()}] ACTUALIZACIÓN: ${res.seleccion}\n\n${res.resultado}`)
      toast.success('Plugin actualizado', {
        description: `${opcion} ya tiene el contexto al día.`,
      })
      setLoading(true)
      await cargarPlugins()
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      setLogOutput(`[${new Date().toLocaleTimeString()}] ERROR: ${msg}`)
      toast.error('No pude actualizar el plugin', { description: msg })
    } finally {
      setUpdatingPlugin(null)
    }
  }

  const handleIniciarEdicion = (plugin: PluginInfo) => {
    setEditingPlugin(plugin.id)
    setCarpetaInput(plugin.carpeta || '')
  }

  const handleGuardarCarpeta = async (pluginId: string) => {
    try {
      setGuardandoConfig(true)
      await api.configurarPlugin({
        clave: pluginId,
        carpeta: carpetaInput.trim(),
      })
      toast.success('Ruta guardada', {
        description: 'La carpeta del plugin fue configurada correctamente.',
      })
      setEditingPlugin(null)
      await cargarPlugins()
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      toast.error('Error guardando la carpeta', { description: msg })
    } finally {
      setGuardandoConfig(false)
    }
  }

  const toggleMemory = (pluginId: string) => {
    setExpandedMemory((prev) => ({ ...prev, [pluginId]: !prev[pluginId] }))
  }

  const handleCopyLogs = () => {
    navigator.clipboard.writeText(logOutput)
    setCopied(true)
    toast.info('Registro copiado')
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="space-y-8 pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
            Plugins Prácticos
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Le dan al tutor el contexto real de tus prácticas: topologías Cisco IOS, flujos Node-RED y proyectos de código.
          </p>
        </div>
        <Button
          onClick={() => handleActualizar('Todos')}
          disabled={updatingPlugin !== null || loading}
          className="gap-2 bg-indigo-600 hover:bg-indigo-500 text-white"
        >
          <RefreshCw className={`h-4 w-4 ${updatingPlugin === 'Todos' ? 'animate-spin' : ''}`} />
          Actualizar todos
        </Button>
      </div>

      {/* Tarjetas de Estado por Plugin */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {plugins.map((plugin) => {
          const conf = ICON_MAP[plugin.id] || {
            icon: Network,
            color: 'text-indigo-500 bg-indigo-50 border-indigo-100 dark:bg-indigo-950/40 dark:border-indigo-800',
          }
          const Icon = conf.icon
          const isUpdating = updatingPlugin === plugin.opcion_key || updatingPlugin === plugin.id
          const isEditing = editingPlugin === plugin.id
          const hasMemory = Boolean(plugin.contexto_reciente && plugin.contexto_reciente.trim())
          const isExpanded = Boolean(expandedMemory[plugin.id])

          return (
            <Card key={plugin.id} className="flex flex-col justify-between transition-all hover:shadow-md">
              <CardHeader className="p-5 pb-3">
                <div className="flex items-center justify-between">
                  <div className={`flex h-10 w-10 items-center justify-center rounded-lg border ${conf.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => (isEditing ? setEditingPlugin(null) : handleIniciarEdicion(plugin))}
                    className="h-8 px-2 text-xs text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
                    title="Configurar carpeta"
                  >
                    <Settings className="h-3.5 w-3.5 mr-1" />
                    {isEditing ? 'Cancelar' : 'Ruta'}
                  </Button>
                </div>
                <div className="mt-3">
                  <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">
                    {plugin.categoria}
                  </span>
                  <CardTitle className="text-base font-semibold mt-0.5">{plugin.nombre}</CardTitle>
                </div>
                <CardDescription className="text-xs leading-relaxed mt-1.5">
                  {plugin.descripcion}
                </CardDescription>

                {/* Formulario de edición de ruta */}
                {isEditing ? (
                  <div className="mt-3 p-3 bg-slate-50 dark:bg-slate-900/60 rounded-lg border border-slate-200 dark:border-slate-800 space-y-2">
                    <label className="text-[11px] font-medium text-slate-600 dark:text-slate-300">
                      Ruta local del proyecto o configuraciones:
                    </label>
                    <Input
                      type="text"
                      placeholder="Ej. C:\Proyectos\MiApp o /home/user/..."
                      value={carpetaInput}
                      onChange={(e) => setCarpetaInput(e.target.value)}
                      className="text-xs h-8"
                    />
                    <div className="flex justify-end gap-2 pt-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setEditingPlugin(null)}
                        className="h-7 text-xs px-2.5"
                      >
                        Cancelar
                      </Button>
                      <Button
                        size="sm"
                        onClick={() => handleGuardarCarpeta(plugin.id)}
                        disabled={guardandoConfig}
                        className="h-7 text-xs px-3 bg-indigo-600 hover:bg-indigo-500 text-white"
                      >
                        Guardar
                      </Button>
                    </div>
                  </div>
                ) : (
                  /* Estado de la carpeta asignada */
                  <div className="mt-3 flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-400">
                    {plugin.carpeta ? (
                      plugin.carpeta_existe ? (
                        <>
                          <FolderCheck className="h-3.5 w-3.5 text-emerald-500 shrink-0" />
                          <span className="truncate font-mono text-[11px]" title={plugin.carpeta}>
                            {plugin.carpeta}
                          </span>
                        </>
                      ) : (
                        <>
                          <FolderX className="h-3.5 w-3.5 text-amber-500 shrink-0" />
                          <span className="truncate text-[11px] text-amber-600 dark:text-amber-400" title={plugin.carpeta}>
                            Carpeta no encontrada
                          </span>
                        </>
                      )
                    ) : (
                      <>
                        <Folder className="h-3.5 w-3.5 text-slate-400 shrink-0" />
                        <span className="text-[11px] text-slate-400 italic">
                          Ruta convencional (bóveda de notas)
                        </span>
                      </>
                    )}
                  </div>
                )}
              </CardHeader>

              <CardContent className="p-5 pt-0 space-y-3">
                {/* Botón expandir memoria extraída */}
                {hasMemory && (
                  <div>
                    <button
                      type="button"
                      onClick={() => toggleMemory(plugin.id)}
                      className="w-full flex items-center justify-between py-1 px-2 text-[11px] font-medium text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 bg-slate-50 dark:bg-slate-900/40 rounded transition-colors"
                    >
                      <span>Contexto técnico activo</span>
                      {isExpanded ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
                    </button>
                    {isExpanded && (
                      <div className="mt-2 max-h-40 overflow-y-auto p-2 bg-slate-100 dark:bg-slate-950 rounded text-[11px] font-mono text-slate-700 dark:text-slate-300 whitespace-pre-wrap border border-slate-200 dark:border-slate-800">
                        {plugin.contexto_reciente}
                      </div>
                    )}
                  </div>
                )}

                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleActualizar(plugin.opcion_key)}
                  disabled={updatingPlugin !== null}
                  className="w-full gap-2 text-xs"
                >
                  <RefreshCw className={`h-3.5 w-3.5 ${isUpdating ? 'animate-spin' : ''}`} />
                  {isUpdating ? 'Escaneando…' : 'Actualizar'}
                </Button>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Visor de Logs con fuente Monoespaciada: solo aparece tras pulsar Actualizar */}
      {haActualizado && (
        <Card>
          <CardHeader className="p-4 pb-2 border-b border-slate-100 dark:border-slate-800 flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <Terminal className="h-4 w-4 text-indigo-500" />
              <CardTitle className="text-sm font-semibold">Registro de sincronización</CardTitle>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopyLogs}
              className="h-8 gap-1.5 text-xs text-slate-500 hover:text-slate-900 dark:hover:text-white"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
              {copied ? 'Copiado' : 'Copiar'}
            </Button>
          </CardHeader>
          <CardContent className="p-0">
            <div className="bg-slate-950 p-4 rounded-b-xl overflow-x-auto min-h-[260px] max-h-[450px]">
              <pre className="font-mono text-xs leading-relaxed text-slate-200 whitespace-pre-wrap">
                {logOutput}
              </pre>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
