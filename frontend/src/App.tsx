import { lazy, Suspense, useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { BrowserRouter, Navigate, Outlet, Route, Routes, useSearchParams } from 'react-router-dom'
import { Toaster } from 'sonner'
import { api, EVENTO_SESION_EXPIRADA } from '@/api/client'
import type { Usuario } from '@/api/types'
import { Sidebar } from '@/components/layout/Sidebar'
import { Button } from '@/components/ui/button'
import { SesionContext } from '@/hooks/useSesion'
import type { ContextoSesion } from '@/hooks/useSesion'

const LoginView = lazy(() => import('@/views/LoginView').then((m) => ({ default: m.LoginView })))

// Cada vista se descarga al visitarla: el JS inicial solo lleva el marco y lo compartido
const AjustesView = lazy(() => import('@/views/AjustesView').then((m) => ({ default: m.AjustesView })))
const AsignaturasView = lazy(() =>
  import('@/views/AsignaturasView').then((m) => ({ default: m.AsignaturasView }))
)
const CalendarioView = lazy(() =>
  import('@/views/CalendarioView').then((m) => ({ default: m.CalendarioView }))
)
const EstudiarView = lazy(() => import('@/views/EstudiarView').then((m) => ({ default: m.EstudiarView })))
const GuiaImprimirView = lazy(() =>
  import('@/views/GuiaImprimirView').then((m) => ({ default: m.GuiaImprimirView }))
)
const HoyView = lazy(() => import('@/views/HoyView').then((m) => ({ default: m.HoyView })))
const RevisionGuiaView = lazy(() =>
  import('@/views/RevisionGuiaView').then((m) => ({ default: m.RevisionGuiaView }))
)

/** Mientras baja el código de una vista: reserva el espacio para no mover el contenido. */
function Cargando() {
  return (
    <div role="status" aria-live="polite" className="min-h-[60vh]">
      <span className="sr-only">Cargando…</span>
    </div>
  )
}

/** Redirige a una ruta conservando los parámetros de búsqueda (query) */
function RedirigirConQuery({ ruta, tab }: { ruta: string; tab?: string }) {
  const [params] = useSearchParams()
  const p = new URLSearchParams(params)
  if (tab) p.set('tab', tab)
  const query = p.toString()
  return <Navigate to={`${ruta}${query ? `?${query}` : ''}`} replace />
}

/** Marco de la aplicación: barra lateral y columna de contenido. */
function Marco() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 antialiased dark:bg-slate-950 dark:text-slate-100">
      <a
        href="#contenido"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-md focus:bg-indigo-700 focus:px-3 focus:py-2 focus:text-sm focus:font-medium focus:text-white"
      >
        Saltar al contenido
      </a>
      <Sidebar />
      <main id="contenido" tabIndex={-1} className="min-w-0 outline-none md:pl-60">
        <div className="mx-auto max-w-5xl px-4 py-8 sm:px-8 md:py-12">
          <Suspense fallback={<Cargando />}>
            <Outlet />
          </Suspense>
        </div>
      </main>
    </div>
  )
}

type EstadoAcceso =
  | { fase: 'cargando' }
  | { fase: 'error'; mensaje: string }
  | { fase: 'listo'; autenticacion: boolean; usuario: Usuario | null }

/** Pantalla a página completa mientras se consulta la sesión: reserva el espacio, sin parpadeo. */
function PantallaCompleta({ children }: { children?: ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4 dark:bg-slate-950">
      {children}
    </div>
  )
}

/** Consulta la sesión al arrancar y decide entre login y aplicación. */
function PuertaAcceso({ children }: { children: ReactNode }) {
  const [estado, setEstado] = useState<EstadoAcceso>({ fase: 'cargando' })

  const consultar = useCallback(() => {
    api
      .getSesion()
      .then((s) => setEstado({ fase: 'listo', autenticacion: s.autenticacion, usuario: s.usuario }))
      .catch((err) =>
        setEstado({
          fase: 'error',
          mensaje: err instanceof Error ? err.message : 'No hay conexión con el servidor.',
        })
      )
  }, [])

  useEffect(() => {
    consultar()
  }, [consultar])

  // Cualquier 401 posterior (sesión caducada) devuelve al login
  useEffect(() => {
    const alExpirar = () =>
      setEstado((e) => (e.fase === 'listo' && e.autenticacion ? { ...e, usuario: null } : e))
    window.addEventListener(EVENTO_SESION_EXPIRADA, alExpirar)
    return () => window.removeEventListener(EVENTO_SESION_EXPIRADA, alExpirar)
  }, [])

  const salir = useCallback(async () => {
    try {
      await api.logout()
    } catch {
      // Aunque falle la red, se vuelve al login; el servidor decide si la cookie sigue viva
    }
    // Recarga completa en la portada: borra el estado en memoria y la URL (con su tema, asignatura
    // o clase) de la cuenta anterior, para que la siguiente persona no vea nada suyo.
    window.location.replace('/')
  }, [])

  const valor = useMemo<ContextoSesion>(
    () => ({
      autenticacion: estado.fase === 'listo' && estado.autenticacion,
      usuario: estado.fase === 'listo' ? estado.usuario : null,
      salir,
    }),
    [estado, salir]
  )

  if (estado.fase === 'cargando') {
    return (
      <PantallaCompleta>
        <div role="status" aria-live="polite">
          <span className="sr-only">Cargando…</span>
        </div>
      </PantallaCompleta>
    )
  }

  if (estado.fase === 'error') {
    return (
      <PantallaCompleta>
        <div role="alert" className="max-w-sm space-y-3 text-center">
          <p className="text-sm text-rose-800 dark:text-rose-200">
            No pude comprobar tu sesión: {estado.mensaje}
          </p>
          <Button
            onClick={() => {
              setEstado({ fase: 'cargando' })
              consultar()
            }}
          >Reintentar</Button>
        </div>
      </PantallaCompleta>
    )
  }

  if (estado.autenticacion && !estado.usuario) {
    return (
      <Suspense fallback={<PantallaCompleta />}>
        <LoginView
          alAcceder={(usuario) => setEstado({ fase: 'listo', autenticacion: true, usuario })}
        />
      </Suspense>
    )
  }

  return <SesionContext.Provider value={valor}>{children}</SesionContext.Provider>
}

export default function App() {
  return (
    <BrowserRouter>
      <PuertaAcceso>
        <Routes>
          {/* Sin barra lateral: es la hoja que se imprime o guarda como PDF */}
          <Route
            path="/guia/:id/imprimir"
            element={
              <Suspense fallback={<Cargando />}>
                <GuiaImprimirView />
              </Suspense>
            }
          />
          <Route element={<Marco />}>
            <Route path="/" element={<HoyView />} />
            <Route path="/estudiar" element={<EstudiarView />} />
            <Route path="/calendario" element={<CalendarioView />} />
            <Route path="/asignaturas" element={<AsignaturasView />} />
            <Route path="/ajustes" element={<AjustesView />} />
            <Route path="/guia/:id/revision" element={<RevisionGuiaView />} />
  
            {/* Rutas anteriores con redirección y conservación de query */}
            <Route path="/tutoria" element={<RedirigirConQuery ruta="/estudiar" tab="tutoria" />} />
            <Route path="/repaso" element={<RedirigirConQuery ruta="/estudiar" tab="repaso" />} />
            <Route path="/guia" element={<RedirigirConQuery ruta="/estudiar" tab="guia" />} />
            <Route path="/quiz" element={<RedirigirConQuery ruta="/estudiar" tab="repaso" />} />
            <Route path="/progreso" element={<Navigate to="/" replace />} />
            <Route path="/plugins" element={<RedirigirConQuery ruta="/ajustes" tab="plugins" />} />
            <Route path="/config" element={<RedirigirConQuery ruta="/ajustes" tab="config" />} />
            <Route path="/silabos" element={<RedirigirConQuery ruta="/asignaturas" />} />
            <Route path="/material" element={<RedirigirConQuery ruta="/asignaturas" tab="material" />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </PuertaAcceso>
      <Toaster position="bottom-right" closeButton />
    </BrowserRouter>
  )
}
