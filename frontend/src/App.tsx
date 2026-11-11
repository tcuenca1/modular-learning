import { BrowserRouter, Navigate, Outlet, Route, Routes, useSearchParams } from 'react-router-dom'
import { Toaster } from 'sonner'
import { Sidebar } from '@/components/layout/Sidebar'
import { AjustesView } from '@/views/AjustesView'
import { AsignaturasView } from '@/views/AsignaturasView'
import { CalendarioView } from '@/views/CalendarioView'
import { EstudiarView } from '@/views/EstudiarView'
import { GuiaImprimirView } from '@/views/GuiaImprimirView'
import { HoyView } from '@/views/HoyView'
import { RevisionGuiaView } from '@/views/RevisionGuiaView'

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
          <Outlet />
        </div>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Sin barra lateral: es la hoja que se imprime o guarda como PDF */}
        <Route path="/guia/:id/imprimir" element={<GuiaImprimirView />} />
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
      <Toaster position="bottom-right" closeButton />
    </BrowserRouter>
  )
}
