import { useEffect, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import {
  BookMarked,
  CalendarDays,
  FileDown,
  GraduationCap,
  Layers,
  LineChart,
  Menu,
  Repeat2,
  Settings,
  Sun,
  X,
} from 'lucide-react'
import type { LucideIcon } from 'lucide-react'
import { api } from '@/api/client'
import { ThemeToggle } from '@/components/ThemeToggle'
import { cn } from '@/lib/utils'

interface ItemNav {
  nombre: string
  ruta: string
  icono: LucideIcon
}

const GRUPOS: { titulo: string; items: ItemNav[] }[] = [
  {
    titulo: 'Estudiar',
    items: [
      { nombre: 'Hoy', ruta: '/', icono: Sun },
      { nombre: 'Calendario', ruta: '/calendario', icono: CalendarDays },
      { nombre: 'Tutoría', ruta: '/tutoria', icono: GraduationCap },
      { nombre: 'Repaso', ruta: '/repaso', icono: Repeat2 },
      { nombre: 'Guía offline', ruta: '/guia', icono: FileDown },
      { nombre: 'Progreso', ruta: '/progreso', icono: LineChart },
    ],
  },
  {
    titulo: 'Biblioteca',
    items: [
      { nombre: 'Asignaturas', ruta: '/asignaturas', icono: BookMarked },
      { nombre: 'Plugins', ruta: '/plugins', icono: Layers },
    ],
  },
]

function Marca() {
  return (
    <Link to="/" className="flex items-center gap-3 px-3">
      <img src="/favicon.svg" alt="" className="h-8 w-8" />
      <span className="leading-tight">
        <span className="block font-display text-[1.05rem] font-semibold text-slate-900 dark:text-slate-50">
          Modular Learning
        </span>
        <span className="block text-xs text-slate-500 dark:text-slate-400">
          cuaderno de estudio
        </span>
      </span>
    </Link>
  )
}

function EnlaceNav({ item, onNavegar }: { item: ItemNav; onNavegar?: () => void }) {
  const Icono = item.icono
  return (
    <NavLink
      to={item.ruta}
      end={item.ruta === '/'}
      onClick={onNavegar}
      className={({ isActive }) =>
        cn(
          'group relative flex items-center gap-3 rounded-md px-3 py-1.5 text-[0.9rem] transition-colors',
          isActive
            ? 'bg-slate-200/60 font-medium text-slate-950 dark:bg-slate-800/70 dark:text-white'
            : 'text-slate-600 hover:bg-slate-200/40 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800/40 dark:hover:text-slate-100'
        )
      }
    >
      {({ isActive }) => (
        <>
          <span
            aria-hidden
            className={cn(
              'absolute -left-3 top-1.5 bottom-1.5 w-[3px] rounded-r bg-indigo-600 transition-opacity dark:bg-indigo-400',
              isActive ? 'opacity-100' : 'opacity-0'
            )}
          />
          <Icono
            className={cn(
              'h-4 w-4 shrink-0',
              isActive ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-400 group-hover:text-slate-600'
            )}
            strokeWidth={1.75}
          />
          {item.nombre}
        </>
      )}
    </NavLink>
  )
}

function ContenidoSidebar({ onNavegar }: { onNavegar?: () => void }) {
  const [online, setOnline] = useState<boolean | null>(null)

  useEffect(() => {
    api
      .getConfig()
      .then(() => setOnline(true))
      .catch(() => setOnline(false))
  }, [])

  return (
    <div className="flex h-full flex-col py-5">
      <Marca />

      <nav className="mt-8 flex-1 space-y-7 px-3">
        {GRUPOS.map((grupo) => (
          <div key={grupo.titulo}>
            <p className="mb-1.5 px-3 font-display text-xs italic text-slate-500 dark:text-slate-500">
              {grupo.titulo}
            </p>
            <div className="space-y-0.5">
              {grupo.items.map((item) => (
                <EnlaceNav key={item.ruta} item={item} onNavegar={onNavegar} />
              ))}
            </div>
          </div>
        ))}
      </nav>

      <div className="space-y-3 px-3">
        {online === false && (
          <p className="rounded-md bg-rose-50 px-3 py-2 text-xs text-rose-700 dark:bg-rose-950/50 dark:text-rose-300">
            No hay conexión con el servidor local.
          </p>
        )}
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <EnlaceNav
              item={{ nombre: 'Configuración', ruta: '/config', icono: Settings }}
              onNavegar={onNavegar}
            />
          </div>
          <ThemeToggle compacto />
        </div>
      </div>
    </div>
  )
}

export function Sidebar() {
  const [abierto, setAbierto] = useState(false)

  return (
    <>
      {/* Escritorio: barra fija */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-60 border-r border-slate-200 bg-slate-100/60 md:block dark:border-slate-800 dark:bg-slate-900/40">
        <ContenidoSidebar />
      </aside>

      {/* Móvil: cabecera + cajón */}
      <header className="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-slate-200 bg-slate-50/95 px-4 backdrop-blur md:hidden dark:border-slate-800 dark:bg-slate-950/95">
        <Marca />
        <div className="flex items-center gap-2">
          <ThemeToggle compacto />
          <button
            type="button"
            onClick={() => setAbierto(true)}
            className="rounded-md p-2 text-slate-600 hover:bg-slate-200/60 dark:text-slate-300 dark:hover:bg-slate-800"
            aria-label="Abrir menú"
          >
            <Menu className="h-5 w-5" />
          </button>
        </div>
      </header>

      {abierto && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div className="absolute inset-0 bg-slate-950/40" onClick={() => setAbierto(false)} />
          <aside className="absolute inset-y-0 left-0 w-64 border-r border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-950">
            <button
              type="button"
              onClick={() => setAbierto(false)}
              className="absolute right-3 top-5 rounded-md p-1.5 text-slate-500 hover:bg-slate-200/60 dark:hover:bg-slate-800"
              aria-label="Cerrar menú"
            >
              <X className="h-4 w-4" />
            </button>
            {/* Cerrar el cajón al navegar */}
            <ContenidoSidebar onNavegar={() => setAbierto(false)} />
          </aside>
        </div>
      )}
    </>
  )
}
