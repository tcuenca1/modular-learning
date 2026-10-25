/** Utilidades compartidas para cruzar asignaturas, cronogramas y fechas de clase. */

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

export function enlaceTutoria(materia: string, tema?: string): string {
  const q = new URLSearchParams({ materia })
  if (tema) q.set('tema', tema)
  return `/tutoria?${q.toString()}`
}

export const formatoCorto = new Intl.DateTimeFormat('es', { day: 'numeric', month: 'short' })
