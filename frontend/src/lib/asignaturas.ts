/** Utilidades compartidas para cruzar asignaturas, cronogramas y fechas de clase. */
import type { ClaseCronograma } from '@/api/types'

export const DIA_MS = 86_400_000

/** Normaliza nombres para cruzar el catálogo de materias con las estadísticas por cronograma. */
export function clave(nombre: string): string {
  return nombre
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '')
}

/** Interpreta fechas dd/mm/aaaa (formato de los cronogramas) o ISO. */
export function parsearFecha(valor: unknown): Date | undefined {
  if (typeof valor !== 'string') return undefined
  const dmy = valor.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/)
  if (dmy) return new Date(Number(dmy[3]), Number(dmy[2]) - 1, Number(dmy[1]))
  const iso = new Date(valor)
  return Number.isNaN(iso.getTime()) ? undefined : iso
}

export function inicioDelDia(fecha: Date): Date {
  return new Date(fecha.getFullYear(), fecha.getMonth(), fecha.getDate())
}

/** "es hoy", "en 3 días", "fue hace 12 días"… */
export function describirFecha(fecha: Date | undefined, hoy: Date): string {
  if (!fecha) return 'sin fecha en el cronograma'
  const dias = Math.round((inicioDelDia(fecha).getTime() - hoy.getTime()) / DIA_MS)
  if (dias === 0) return 'es hoy'
  if (dias === 1) return 'es mañana'
  if (dias > 1) return `en ${dias} días`
  if (dias === -1) return 'fue ayer'
  return `fue hace ${-dias} días`
}

/** Enlace a la tutoría; `enfoque` es la pregunta de repaso fallada que se quiere reforzar. */
export function enlaceTutoria(materia: string, tema?: string, enfoque?: string): string {
  const q = new URLSearchParams({ materia })
  if (tema) q.set('tema', tema)
  if (enfoque) q.set('enfoque', enfoque)
  return `/tutoria?${q.toString()}`
}

export const formatoCorto = new Intl.DateTimeFormat('es', { day: 'numeric', month: 'short' })

export interface ClaseFechada {
  materia: string
  clase: ClaseCronograma
  fecha: Date
  completada: boolean
}

export function esCompletada(clase: ClaseCronograma): boolean {
  return String(clase.estado ?? '').toLowerCase().startsWith('complet')
}

/** Clave de un día del calendario local, para agrupar clases por fecha. */
export function claveDia(fecha: Date): string {
  return `${fecha.getFullYear()}-${fecha.getMonth()}-${fecha.getDate()}`
}

/**
 * Aplana los cronogramas en clases con fecha, ordenadas por día. Los nombres derivados del
 * archivo se sustituyen por el nombre del catálogo cuando coinciden con `clave()`.
 */
export function clasesConFecha(
  cronogramas: Record<string, ClaseCronograma[]>,
  catalogo: string[]
): ClaseFechada[] {
  const porClave = new Map(catalogo.map((n) => [clave(n), n]))
  const lista: ClaseFechada[] = []
  for (const [nombre, clases] of Object.entries(cronogramas)) {
    const materia = porClave.get(clave(nombre)) ?? nombre
    for (const clase of clases) {
      const fecha = parsearFecha(clase.fecha)
      if (fecha) lista.push({ materia, clase, fecha: inicioDelDia(fecha), completada: esCompletada(clase) })
    }
  }
  return lista.sort((a, b) => a.fecha.getTime() - b.fecha.getTime() || a.materia.localeCompare(b.materia))
}
