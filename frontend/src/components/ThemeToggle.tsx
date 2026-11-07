import { useEffect, useState } from 'react'
import { Monitor, Moon, Sun } from 'lucide-react'
import { aplicarTema, obtenerTemaGuardado, type Tema } from '@/lib/theme'
import { cn } from '@/lib/utils'

interface ThemeToggleProps {
  compacto?: boolean
  className?: string
}

const OPCIONES: { valor: Tema; etiqueta: string; icono: typeof Sun }[] = [
  { valor: 'light', etiqueta: 'Claro', icono: Sun },
  { valor: 'dark', etiqueta: 'Oscuro', icono: Moon },
  { valor: 'system', etiqueta: 'Sistema', icono: Monitor },
]

export function ThemeToggle({ compacto = true, className }: ThemeToggleProps) {
  const [tema, setTemaState] = useState<Tema>('system')

  useEffect(() => {
    setTemaState(obtenerTemaGuardado())
  }, [])

  const cambiar = (nuevo: Tema) => {
    setTemaState(nuevo)
    aplicarTema(nuevo)
  }

  if (compacto) {
    return (
      <div
        role="group"
        aria-label="Selector de tema"
        className={cn(
          'inline-flex items-center gap-0.5 rounded-lg border border-slate-200 bg-slate-100/80 p-0.5 dark:border-slate-800 dark:bg-slate-900',
          className
        )}
      >
        {OPCIONES.map((op) => {
          const Icono = op.icono
          const activo = tema === op.valor
          return (
            <button
              key={op.valor}
              type="button"
              onClick={() => cambiar(op.valor)}
              title={`Tema ${op.etiqueta}`}
              aria-pressed={activo}
              className={cn(
                'rounded-md p-1.5 text-xs font-medium transition-all cursor-pointer',
                activo
                  ? 'bg-white text-slate-900 shadow-sm dark:bg-slate-800 dark:text-slate-100'
                  : 'text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200'
              )}
            >
              <Icono className="h-3.5 w-3.5" />
              <span className="sr-only">{op.etiqueta}</span>
            </button>
          )
        })}
      </div>
    )
  }

  return (
    <div className={cn('grid grid-cols-3 gap-3', className)}>
      {OPCIONES.map((op) => {
        const Icono = op.icono
        const activo = tema === op.valor
        return (
          <button
            key={op.valor}
            type="button"
            onClick={() => cambiar(op.valor)}
            className={cn(
              'flex flex-col items-center justify-center gap-2 rounded-xl border p-4 text-xs font-medium transition-all cursor-pointer',
              activo
                ? 'border-indigo-600 bg-indigo-50/50 text-indigo-900 ring-2 ring-indigo-500/20 dark:border-indigo-400 dark:bg-indigo-950/40 dark:text-indigo-200'
                : 'border-slate-200 bg-white text-slate-600 hover:bg-slate-50 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-400 dark:hover:bg-slate-800/60'
            )}
          >
            <Icono className="h-5 w-5" />
            <span>{op.etiqueta}</span>
          </button>
        )
      })}
    </div>
  )
}
