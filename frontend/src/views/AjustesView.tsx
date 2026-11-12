import { useSearchParams } from 'react-router-dom'
import { Layers, Settings, UserRound } from 'lucide-react'
import { useSesion } from '@/hooks/useSesion'
import { cn } from '@/lib/utils'
import { CuentaView } from '@/views/CuentaView'
import { ConfigView } from '@/views/ConfigView'
import { PluginsView } from '@/views/PluginsView'

const PESTANAS = [
  { id: 'config', nombre: 'Configuración', icono: Settings },
  { id: 'plugins', nombre: 'Plugins', icono: Layers },
  { id: 'cuenta', nombre: 'Cuenta', icono: UserRound },
] as const

type Pestana = (typeof PESTANAS)[number]['id']

export function AjustesView() {
  const [params, setParams] = useSearchParams()
  const { autenticacion } = useSesion()

  // «Cuenta» solo existe con autenticación activa
  const pestanas = PESTANAS.filter((p) => p.id !== 'cuenta' || autenticacion)
  const tabParam = params.get('tab')
  const activa: Pestana =
    tabParam === 'plugins' ? 'plugins' : tabParam === 'cuenta' && autenticacion ? 'cuenta' : 'config'

  const cambiarTab = (nueva: Pestana) => {
    const p = new URLSearchParams(params)
    if (nueva === 'config') {
      p.delete('tab')
    } else {
      p.set('tab', nueva)
    }
    setParams(p, { replace: true })
  }

  return (
    <div className="space-y-6">
      {/* Selector de Pestañas: Configuración, Plugins */}
      <div role="tablist" className="flex gap-6 border-b border-slate-200 dark:border-slate-800">
        {pestanas.map((p) => {
          const Icono = p.icono
          const esActiva = activa === p.id
          return (
            <button
              key={p.id}
              role="tab"
              type="button"
              aria-selected={esActiva}
              onClick={() => cambiarTab(p.id)}
              className={cn(
                'flex items-center gap-2 -mb-px border-b-2 pb-2.5 text-sm transition-colors cursor-pointer',
                esActiva
                  ? 'border-indigo-600 font-medium text-slate-950 dark:border-indigo-400 dark:text-white'
                  : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
              )}
            >
              <Icono className="h-4 w-4" />
              {p.nombre}
            </button>
          )
        })}
      </div>

      {/* Contenido según pestaña */}
      {activa === 'config' && <ConfigView />}
      {activa === 'plugins' && <PluginsView />}
      {activa === 'cuenta' && <CuentaView />}
    </div>
  )
}
