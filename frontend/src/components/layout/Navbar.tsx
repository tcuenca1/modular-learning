import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  BarChart3,
  BookOpen,
  Brain,
  FolderSync,
  GraduationCap,
  Layers,
  Settings,
  Sparkles,
} from 'lucide-react'
import { api } from '@/api/client'
import { cn } from '@/lib/utils'

export function Navbar() {
  const location = useLocation()
  const [online, setOnline] = useState<boolean | null>(null)

  useEffect(() => {
    api
      .getConfig()
      .then(() => setOnline(true))
      .catch(() => setOnline(false))
  }, [])

  const navItems = [
    { name: 'Dashboard', path: '/', icon: BarChart3 },
    { name: 'Tutoría', path: '/tutoria', icon: GraduationCap },
    { name: 'Quiz', path: '/quiz', icon: Brain },
    { name: 'Sílabos', path: '/silabos', icon: BookOpen },
    { name: 'Material', path: '/material', icon: FolderSync },
    { name: 'Plugins', path: '/plugins', icon: Layers },
    { name: 'Configuración', path: '/config', icon: Settings },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200/80 bg-white/80 backdrop-blur-md dark:border-slate-800 dark:bg-slate-900/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-2.5 transition-opacity hover:opacity-90">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 text-white shadow-sm shadow-indigo-200 dark:shadow-none">
              <Sparkles className="h-5 w-5" />
            </div>
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-900 tracking-tight dark:text-white">
                  Modular Learning
                </span>
                <span className="rounded bg-indigo-50 px-1.5 py-0.5 text-[10px] font-semibold text-indigo-700 border border-indigo-100 dark:bg-indigo-950 dark:text-indigo-300 dark:border-indigo-800">
                  v2.0
                </span>
              </div>
              <span className="text-[11px] text-slate-500 font-medium">Segundo Cerebro & Tutor IA</span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={cn(
                    'flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-white'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800/60 dark:hover:text-slate-200'
                  )}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                </Link>
              )
            })}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-full border border-slate-200/80 bg-slate-50/50 px-3 py-1 text-xs font-medium text-slate-600 dark:border-slate-800 dark:bg-slate-800/50 dark:text-slate-300">
            <span
              className={cn(
                'h-2 w-2 rounded-full',
                online === true
                  ? 'bg-emerald-500 animate-pulse'
                  : online === false
                  ? 'bg-rose-500'
                  : 'bg-amber-400'
              )}
            />
            {online === true ? 'API Conectada' : online === false ? 'API Desconectada' : 'Verificando...'}
          </div>
        </div>
      </div>
    </header>
  )
}
