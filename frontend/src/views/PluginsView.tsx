import { useState } from 'react'
import {
  Check,
  Copy,
  Cpu,
  Globe,
  Network,
  RefreshCw,
  Terminal,
} from 'lucide-react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

interface PluginCardInfo {
  id: string
  title: string
  optionKey: string
  category: string
  description: string
  icon: typeof Network
  color: string
}

const PLUGIN_DEFINITIONS: PluginCardInfo[] = [
  {
    id: 'cisco',
    title: 'Cisco Packet Tracer',
    optionKey: 'Cisco (Actividades)',
    category: 'Redes y Telecomunicaciones',
    description:
      'Indexa comandos de configuración IOS, topologías de conmutación, enrutamiento y memorias técnicas.',
    icon: Network,
    color: 'text-sky-500 bg-sky-50 border-sky-100 dark:bg-sky-950/40 dark:border-sky-800',
  },
  {
    id: 'nodered',
    title: 'Node-RED IoT Hub',
    optionKey: 'Node-RED (Flujos JSON)',
    category: 'Internet de las Cosas',
    description:
      'Parsea flujos JSON locales, nodos MQTT, telemetría de sensores y dashboards industriales.',
    icon: Cpu,
    color: 'text-rose-500 bg-rose-50 border-rose-100 dark:bg-rose-950/40 dark:border-rose-800',
  },
  {
    id: 'web',
    title: 'Web & Fullstack Dev',
    optionKey: 'Web (Proyectos)',
    category: 'Desarrollo de Software',
    description:
      'Sincroniza proyectos de frontend, backend, APIs REST y arquitecturas de software.',
    icon: Globe,
    color: 'text-emerald-500 bg-emerald-50 border-emerald-100 dark:bg-emerald-950/40 dark:border-emerald-800',
  },
]

export function PluginsView() {
  const [updatingPlugin, setUpdatingPlugin] = useState<string | null>(null)
  const [logOutput, setLogOutput] = useState<string>(
    '// Registros de sincronización de plugins prácticos.\n// Selecciona un plugin arriba para ejecutar la indexación y actualizar el contexto de memoria...'
  )
  const [copied, setCopied] = useState(false)


  const handleActualizar = async (opcion: string) => {
    try {
      setUpdatingPlugin(opcion)
      toast.info(`Actualizando plugin: ${opcion}...`)
      const res = await api.actualizarPlugin(opcion)
      setLogOutput(`[${new Date().toLocaleTimeString()}] ACTUALIZACIÓN: ${res.seleccion}\n\n${res.resultado}`)
      toast.success('¡Plugin actualizado con éxito!', {
        description: `Se refrescó el contexto de memoria para ${opcion}.`,
      })
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      setLogOutput(`[${new Date().toLocaleTimeString()}] ERROR: ${msg}`)
      toast.error('Error al actualizar plugin', { description: msg })
    } finally {
      setUpdatingPlugin(null)
    }
  }

  const handleCopyLogs = () => {
    navigator.clipboard.writeText(logOutput)
    setCopied(true)
    toast.info('Logs copiados al portapapeles')
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="space-y-8 pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
            Plugins Prácticos y Memoria Técnica
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Adaptadores de entorno para conectar el tutor con actividades prácticas, simulaciones y flujos.
          </p>
        </div>
        <Button
          onClick={() => handleActualizar('Todos')}
          disabled={updatingPlugin !== null}
          className="gap-2 bg-indigo-600 hover:bg-indigo-500 text-white"
        >
          <RefreshCw className={`h-4 w-4 ${updatingPlugin === 'Todos' ? 'animate-spin' : ''}`} />
          Sincronizar Todos los Plugins
        </Button>
      </div>

      {/* Tarjetas de Estado por Plugin */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {PLUGIN_DEFINITIONS.map((plugin) => {
          const Icon = plugin.icon
          const isUpdating = updatingPlugin === plugin.optionKey
          return (
            <Card key={plugin.id} className="flex flex-col justify-between transition-all hover:shadow-md">
              <CardHeader className="p-5 pb-3">
                <div className="flex items-center justify-between">
                  <div className={`flex h-10 w-10 items-center justify-center rounded-lg border ${plugin.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <Badge variant="success">Activo</Badge>
                </div>
                <div className="mt-3">
                  <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">
                    {plugin.category}
                  </span>
                  <CardTitle className="text-base font-semibold mt-0.5">{plugin.title}</CardTitle>
                </div>
                <CardDescription className="text-xs leading-relaxed mt-1.5">
                  {plugin.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="p-5 pt-0">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleActualizar(plugin.optionKey)}
                  disabled={updatingPlugin !== null}
                  className="w-full gap-2 text-xs"
                >
                  <RefreshCw className={`h-3.5 w-3.5 ${isUpdating ? 'animate-spin' : ''}`} />
                  {isUpdating ? 'Indexando flujos...' : 'Actualizar Memoria'}
                </Button>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Visor de Logs con fuente Monoespaciada */}
      <Card>
        <CardHeader className="p-4 pb-2 border-b border-slate-100 dark:border-slate-800 flex flex-row items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="h-4 w-4 text-indigo-500" />
            <CardTitle className="text-sm font-semibold">Consola de Telemetría e Inspección de Plugins</CardTitle>
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
    </div>
  )
}
