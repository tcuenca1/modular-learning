/** Utilidades compartidas para cruzar asignaturas, cronogramas y fechas de clase. */
import type { ClaseCronograma, MateriaItem } from '@/api/types'

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
  const ymd = valor.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/)
  if (ymd) return new Date(Number(ymd[1]), Number(ymd[2]) - 1, Number(ymd[3]))
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
export function enlaceTutoria(materia: string, tema?: string, enfoque?: string, claseId?: string): string {
  const q = new URLSearchParams({ tab: 'tutoria', materia })
  if (tema) q.set('tema', tema)
  if (enfoque) q.set('enfoque', enfoque)
  if (claseId) q.set('clase_id', claseId)
  return `/estudiar?${q.toString()}`
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

export interface MateriaConCronograma {
  materia: string
  clases: ClaseCronograma[]
}

/** Asignaturas con cronograma, con el nombre del catálogo cuando coincide con `clave()`. */
export function materiasConCronograma(
  cronogramas: Record<string, ClaseCronograma[]>,
  catalogo: string[]
): MateriaConCronograma[] {
  const porClave = new Map(catalogo.map((n) => [clave(n), n]))
  return Object.entries(cronogramas)
    .filter(([, clases]) => clases.length > 0)
    .map(([nombre, clases]) => ({ materia: porClave.get(clave(nombre)) ?? nombre, clases }))
    .sort((a, b) => a.materia.localeCompare(b.materia))
}

/** Busca una asignatura en el catálogo comparando slug o nombre normalizados con clave(). */
export function buscarMateriaPorClave(materias: MateriaItem[], buscado: string): MateriaItem | undefined {
  const norm = clave(buscado)
  if (!norm) return undefined
  return materias.find((m) => m.slug === buscado || clave(m.slug) === norm || clave(m.nombre) === norm)
}

/**
 * Resuelve la asignatura tras seleccionar un archivo de sílabo o extraer su contenido:
 * - Si el nombre coincide con una asignatura del catálogo, se selecciona esa.
 * - Si no coincide, no se altera la selección existente salvo que el desplegable
 *   estuviera en «__nueva__» y el texto estuviera vacío, en cuyo caso se rellena con el nombre detectado.
 */
export function resolverMateriaSubida(
  materias: MateriaItem[],
  nombreDetectado: string,
  seleccionActual: { materiaSelect: string; subidaMateria: string }
): { materiaSelect: string; subidaMateria: string } {
  const detectado = nombreDetectado.trim()
  if (!detectado) return seleccionActual

  const coincidencia = buscarMateriaPorClave(materias, detectado)
  if (coincidencia) {
    return {
      materiaSelect: coincidencia.nombre,
      subidaMateria: coincidencia.nombre,
    }
  }

  if (seleccionActual.materiaSelect === '__nueva__' && !seleccionActual.subidaMateria.trim()) {
    return {
      materiaSelect: '__nueva__',
      subidaMateria: detectado,
    }
  }

  return seleccionActual
}


