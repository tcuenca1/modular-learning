import { useEffect, useRef, useState } from 'react'
import { Link, NavLink } from 'react-router-dom'
import {
  BookMarked,
  CalendarDays,
  GraduationCap,
  Menu,
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

const ITEMS_NAV: ItemNav[] = [
  { nombre: 'Hoy', ruta: '/', icono: Sun },
  { nombre: 'Estudiar', ruta: '/estudiar', icono: GraduationCap },
  { nombre: 'Calendario', ruta: '/calendario', icono: CalendarDays },
  { nombre: 'Asignaturas', ruta: '/asignaturas', icono: BookMarked },
  { nombre: 'Ajustes', ruta: '/ajustes', icono: Settings },
]

function Marca({ className }: { className?: string }) {
  return (
    <Link to="/" className={cn('flex items-center gap-3 min-w-0', className)}>
      <img src="/favicon.svg" alt="" className="h-8 w-8 shrink-0" />
      <span className="min-w-0 leading-tight">
        <span className="block truncate font-display text-[1.05rem] font-semibold text-slate-900 dark:text-slate-50">
          Modular Learning
        </span>
        <span className="block truncate text-xs text-slate-500 dark:text-slate-400">
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
      <Marca className="px-3" />

      <nav className="mt-8 flex-1 space-y-1 px-3">
        {ITEMS_NAV.map((item) => (
          <EnlaceNav key={item.ruta} item={item} onNavegar={onNavegar} />
        ))}
      </nav>

      <div className="space-y-3 px-3">
        {online === false && (
          <p className="rounded-md bg-rose-50 px-3 py-2 text-xs text-rose-700 dark:bg-rose-950/50 dark:text-rose-300">
            No hay conexión con el servidor local.
          </p>
        )}
        <div className="flex items-center justify-end px-3">
          <ThemeToggle compacto />
        </div>
      </div>
    </div>
  )
}

export function Sidebar() {
  const [abierto, setAbierto] = useState(false)
  const botonMenu = useRef<HTMLButtonElement>(null)
  const botonCerrar = useRef<HTMLButtonElement>(null)

  const cerrar = () => {
    setAbierto(false)
    botonMenu.current?.focus()
  }

  // Con el cajón abierto: foco dentro y Escape lo cierra devolviendo el foco al botón
  useEffect(() => {
    if (!abierto) return
    botonCerrar.current?.focus()
    const alPulsar = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setAbierto(false)
        botonMenu.current?.focus()
      }
    }
    document.addEventListener('keydown', alPulsar)
    return () => document.removeEventListener('keydown', alPulsar)
  }, [abierto])

  return (
    <>
      {/* Escritorio: barra fija */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-60 border-r border-slate-200 bg-slate-100/60 md:block dark:border-slate-800 dark:bg-slate-900/40">
        <ContenidoSidebar />
      </aside>

      {/* Móvil: cabecera + cajón */}
      <header className="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-slate-200 bg-slate-50/95 px-4 backdrop-blur md:hidden dark:border-slate-800 dark:bg-slate-950/95">
        <Marca />
        <div className="flex shrink-0 items-center gap-2">
          <ThemeToggle compacto />
          <button
            ref={botonMenu}
            type="button"
            onClick={() => setAbierto(true)}
            className="rounded-md p-2 text-slate-600 hover:bg-slate-200/60 dark:text-slate-300 dark:hover:bg-slate-800"
            aria-label="Abrir menú"
            aria-expanded={abierto}
            aria-controls="menu-movil"
          >
            <Menu className="h-5 w-5" />
          </button>
        </div>
      </header>

      {abierto && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div className="absolute inset-0 bg-slate-950/40" onClick={cerrar} />
          <aside
            id="menu-movil"
            role="dialog"
            aria-modal="true"
            aria-label="Menú principal"
            className="absolute inset-y-0 left-0 w-64 border-r border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-950"
          >
            <button
              ref={botonCerrar}
              type="button"
              onClick={cerrar}
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
