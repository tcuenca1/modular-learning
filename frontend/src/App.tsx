import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Toaster } from 'sonner'
import { Sidebar } from '@/components/layout/Sidebar'
import { AsignaturasView } from '@/views/AsignaturasView'
import { ConfigView } from '@/views/ConfigView'
import { DashboardView } from '@/views/DashboardView'
import { HoyView } from '@/views/HoyView'
import { PluginsView } from '@/views/PluginsView'
import { QuizView } from '@/views/QuizView'
import { TutoriaView } from '@/views/TutoriaView'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 text-slate-900 antialiased dark:bg-slate-950 dark:text-slate-100">
        <Sidebar />
        <main className="md:pl-60">
          <div className="mx-auto max-w-5xl px-4 py-8 sm:px-8 md:py-12">
            <Routes>
              <Route path="/" element={<HoyView />} />
              <Route path="/tutoria" element={<TutoriaView />} />
              <Route path="/repaso" element={<QuizView />} />
              <Route path="/progreso" element={<DashboardView />} />
              <Route path="/asignaturas" element={<AsignaturasView />} />
              <Route path="/plugins" element={<PluginsView />} />
              <Route path="/config" element={<ConfigView />} />
              {/* Rutas anteriores */}
              <Route path="/quiz" element={<Navigate to="/repaso" replace />} />
              <Route path="/silabos" element={<Navigate to="/asignaturas" replace />} />
              <Route path="/material" element={<Navigate to="/asignaturas?tab=material" replace />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </main>
        <Toaster position="bottom-right" closeButton />
      </div>
    </BrowserRouter>
  )
}
