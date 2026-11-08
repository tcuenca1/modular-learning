import { useSearchParams } from 'react-router-dom'
import { FileDown, GraduationCap, Repeat2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import { GuiaView } from '@/views/GuiaView'
import { QuizView } from '@/views/QuizView'
import { TutoriaView } from '@/views/TutoriaView'

const PESTANAS = [
  { id: 'tutoria', nombre: 'Tutoría', icono: GraduationCap },
  { id: 'repaso', nombre: 'Repaso', icono: Repeat2 },
  { id: 'guia', nombre: 'Guía offline', icono: FileDown },
] as const

type Pestana = (typeof PESTANAS)[number]['id']

export function EstudiarView() {
  const [params, setParams] = useSearchParams()

  const tabParam = params.get('tab')
  const activa: Pestana =
    tabParam === 'repaso'
      ? 'repaso'
      : tabParam === 'guia'
        ? 'guia'
        : 'tutoria'

  const cambiarTab = (nueva: Pestana) => {
    const p = new URLSearchParams(params)
    if (nueva === 'tutoria') {
      p.delete('tab')
    } else {
      p.set('tab', nueva)
    }
    setParams(p, { replace: true })
  }

  return (
    <div className="space-y-6">
      {/* Selector de Pestañas: Tutoría, Repaso, Guía offline */}
      <div role="tablist" className="flex gap-6 border-b border-slate-200 dark:border-slate-800">
        {PESTANAS.map((p) => {
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

      {/* Contenido del modo activo */}
      {activa === 'tutoria' && <TutoriaView />}
      {activa === 'repaso' && <QuizView />}
      {activa === 'guia' && <GuiaView />}
    </div>
  )
}
