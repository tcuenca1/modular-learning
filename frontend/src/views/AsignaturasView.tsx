import { useSearchParams } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { MaterialView } from '@/views/MaterialView'
import { SilabosView } from '@/views/SilabosView'

const PESTANAS = [
  { id: 'cronogramas', nombre: 'Cronogramas', detalle: 'Administra tus asignaturas, clases y sílabos del semestre.' },
  { id: 'material', nombre: 'Material', detalle: 'Convierte tus archivos de clase en notas para Obsidian.' },
] as const

type Pestana = (typeof PESTANAS)[number]['id']

export function AsignaturasView() {
  const [params, setParams] = useSearchParams()
  const activa: Pestana = params.get('tab') === 'material' ? 'material' : 'cronogramas'
  const detalle = PESTANAS.find((p) => p.id === activa)?.detalle

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Asignaturas</h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{detalle}</p>
      </div>

      <div role="tablist" className="flex gap-6 border-b border-slate-200 dark:border-slate-800">
        {PESTANAS.map((p) => (
          <button
            key={p.id}
            role="tab"
            type="button"
            aria-selected={activa === p.id}
            onClick={() => setParams(p.id === 'cronogramas' ? {} : { tab: p.id }, { replace: true })}
            className={cn(
              '-mb-px border-b-2 pb-2.5 text-sm transition-colors',
              activa === p.id
                ? 'border-indigo-600 font-medium text-slate-950 dark:border-indigo-400 dark:text-white'
                : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            )}
          >
            {p.nombre}
          </button>
        ))}
      </div>

      {activa === 'cronogramas' ? <SilabosView embebido /> : <MaterialView embebido />}
    </div>
  )
}
