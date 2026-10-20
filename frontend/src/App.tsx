import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Toaster } from 'sonner'
import { Navbar } from '@/components/layout/Navbar'
import { ConfigView } from '@/views/ConfigView'
import { DashboardView } from '@/views/DashboardView'
import { MaterialView } from '@/views/MaterialView'
import { PluginsView } from '@/views/PluginsView'
import { QuizView } from '@/views/QuizView'
import { SilabosView } from '@/views/SilabosView'
import { TutoriaView } from '@/views/TutoriaView'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 text-slate-900 antialiased selection:bg-indigo-500 selection:text-white dark:bg-slate-950 dark:text-slate-50">
        <Navbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<DashboardView />} />
            <Route path="/tutoria" element={<TutoriaView />} />
            <Route path="/quiz" element={<QuizView />} />
            <Route path="/silabos" element={<SilabosView />} />
            <Route path="/material" element={<MaterialView />} />
            <Route path="/plugins" element={<PluginsView />} />
            <Route path="/config" element={<ConfigView />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Toaster position="top-right" richColors closeButton />
      </div>
    </BrowserRouter>
  )
}
