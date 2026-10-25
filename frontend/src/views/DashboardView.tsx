import { useEffect, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  AlertCircle,
  BookMarked,
  Calendar,
  CheckCircle2,
  Clock,
  Layers,
  Sparkles,
  TrendingUp,
} from 'lucide-react'
import { api } from '@/api/client'
import type { ClaseCronograma, StatsResponse } from '@/api/types'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'

export function DashboardView() {
  const [stats, setStats] = useState<StatsResponse | null>(null)
  const [materias, setMaterias] = useState<string[]>([])
  const [materiaSeleccionada, setMateriaSeleccionada] = useState<string>('')
  const [clases, setClases] = useState<ClaseCronograma[]>([])
  const [loading, setLoading] = useState(true)
  const [loadingClases, setLoadingClases] = useState(false)

  useEffect(() => {
    async function cargarDatos() {
      try {
        setLoading(true)
        const [statsData, matsData] = await Promise.all([
          api.getStats(),
          api.getMaterias(),
        ])
        setStats(statsData)
        setMaterias(matsData.materias)
        if (matsData.materias.length > 0) {
          setMateriaSeleccionada(matsData.materias[0])
        }
      } catch (err) {
        console.error('Error al cargar datos del dashboard:', err)
      } finally {
        setLoading(false)
      }
    }
    cargarDatos()
  }, [])

  useEffect(() => {
    if (!materiaSeleccionada) return
    async function cargarClases() {
      try {
        setLoadingClases(true)
        const res = await api.getProximasClases(materiaSeleccionada)
        setClases(res.clases)
      } catch (err) {
        console.error('Error al cargar próximas clases:', err)
      } finally {
        setLoadingClases(false)
      }
    }
    cargarClases()
  }, [materiaSeleccionada])

  // Formatear datos para el gráfico de barras de Recharts
  const chartData = stats
    ? Object.entries(stats.materias).map(([nombre, info]) => ({
        name: nombre.length > 18 ? `${nombre.slice(0, 16)}...` : nombre,
        nombreCompleto: nombre,
        Completados: info.completados,
        Pendientes: Math.max(0, info.total - info.completados),
        Porcentaje: Number(info.porcentaje.toFixed(1)),
      }))
    : []

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-2">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
          <p className="text-sm text-slate-500">Cargando métricas del sistema...</p>
        </div>
      </div>
    )
  }

  const totalTemas = stats?.total_temas || 0
  const temasCompletados = stats?.temas_completados || 0
  const pctGlobal = stats?.porcentaje_global || 0

  return (
    <div className="space-y-8 pb-12">
      {/* Encabezado */}
      <div>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">
          Progreso
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          Cuánto del sílabo llevas estudiado, asignatura por asignatura.
        </p>
      </div>

      {/* Métricas Globales */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium uppercase tracking-wider text-slate-500">
              Avance Global
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-indigo-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{pctGlobal.toFixed(1)}%</div>
            <Progress value={pctGlobal} className="mt-2 h-1.5" />
            <p className="mt-1.5 text-xs text-slate-500">
              {temasCompletados} de {totalTemas} temas completados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium uppercase tracking-wider text-slate-500">
              Temas Completados
            </CardTitle>
            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              {temasCompletados}
            </div>
            <p className="mt-1 text-xs text-slate-500">
              Clases dominadas y consolidadas en Obsidian
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium uppercase tracking-wider text-slate-500">
              Asignaturas Activas
            </CardTitle>
            <BookMarked className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              {materias.length}
            </div>
            <p className="mt-1 text-xs text-slate-500">
              Materias registradas en el catálogo actual
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-xs font-medium uppercase tracking-wider text-slate-500">
              Plugins en Memoria
            </CardTitle>
            <Layers className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-slate-900 dark:text-white">
              {stats?.plugins_activos || 0}
            </div>
            <p className="mt-1 text-xs text-slate-500">
              Módulos prácticos sincronizados (Cisco, IoT, Web)
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráfico de Progreso por Asignatura */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Desglose de Avance Curricular por Asignatura</CardTitle>
              <CardDescription>
                Comparativa entre temas completados y pendientes por materia
              </CardDescription>
            </div>
            <Badge variant="secondary" className="hidden sm:inline-flex gap-1 items-center">
              <Sparkles className="h-3 w-3 text-indigo-500" /> Telemetría en Vivo
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          {chartData.length > 0 ? (
            <div className="h-[320px] w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--color-slate-200)" />
                  <XAxis
                    dataKey="name"
                    tick={{ fontSize: 12, fill: 'var(--color-slate-500)' }}
                    axisLine={{ stroke: 'var(--color-slate-300)' }}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fontSize: 12, fill: 'var(--color-slate-500)' }}
                    axisLine={{ stroke: 'var(--color-slate-300)' }}
                    tickLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'var(--color-white)',
                      borderRadius: '8px',
                      border: '1px solid var(--color-slate-200)',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                      fontSize: '12px',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
                  <Bar dataKey="Completados" fill="var(--color-indigo-600)" radius={[4, 4, 0, 0]} stackId="a" />
                  <Bar dataKey="Pendientes" fill="var(--color-slate-300)" radius={[4, 4, 0, 0]} stackId="a" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex h-48 flex-col items-center justify-center text-center">
              <AlertCircle className="h-8 w-8 text-slate-400" />
              <p className="mt-2 text-sm font-medium text-slate-600">
                Aún no hay cronogramas extraídos.
              </p>
              <p className="text-xs text-slate-400">
                Dirígete a la sección de Sílabos para cargar tus materias y visualizar métricas.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Sección de Próximas Clases */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 className="text-lg font-semibold tracking-tight text-slate-900 dark:text-white">
              Próximas Clases y Temas de Estudio
            </h2>
            <p className="text-xs text-slate-500">
              Selecciona una asignatura para revisar sus sesiones pendientes
            </p>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {materias.map((mat) => (
              <Button
                key={mat}
                variant={materiaSeleccionada === mat ? 'default' : 'outline'}
                size="sm"
                onClick={() => setMateriaSeleccionada(mat)}
                className="text-xs"
              >
                {mat}
              </Button>
            ))}
          </div>
        </div>

        {loadingClases ? (
          <div className="py-8 text-center text-xs text-slate-400">
            Cargando cronograma de {materiaSeleccionada}...
          </div>
        ) : clases.length > 0 ? (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {clases.map((clase, idx) => (
              <Card key={idx} className="transition-all hover:border-slate-300 hover:shadow-md">
                <CardHeader className="p-4 pb-2">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center gap-1.5 text-xs font-semibold text-indigo-600">
                      <Calendar className="h-3.5 w-3.5" />
                      Clase {clase.clase ?? idx + 1}
                      {clase.semana ? ` • Semana ${clase.semana}` : ''}
                    </span>
                    <Badge variant={clase.estado?.toLowerCase() === 'completado' ? 'success' : 'secondary'}>
                      {clase.estado || 'Pendiente'}
                    </Badge>
                  </div>
                  <CardTitle className="mt-1.5 text-sm font-medium leading-snug line-clamp-2">
                    {clase.tema}
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-4 pt-1 text-xs text-slate-500">
                  {clase.materiales_asociados && clase.materiales_asociados.length > 0 ? (
                    <div className="mt-2 flex items-center gap-1 text-[11px] text-slate-400">
                      <Clock className="h-3 w-3" />
                      {clase.materiales_asociados.length} material(es) vinculado(s)
                    </div>
                  ) : (
                    <p className="text-[11px] text-slate-400 italic">Sin material adicional asignado</p>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="border-dashed">
            <CardContent className="flex flex-col items-center justify-center p-8 text-center">
              <Calendar className="h-8 w-8 text-slate-300" />
              <p className="mt-2 text-sm font-medium text-slate-600">
                No hay clases pendientes para {materiaSeleccionada}.
              </p>
              <p className="text-xs text-slate-400">
                Todas las clases están completadas o aún no se ha estructurado el cronograma.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
