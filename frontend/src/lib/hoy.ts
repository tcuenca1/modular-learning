/**
 * Criterio único de la pantalla Hoy: solo cuentan las clases de los cronogramas de las
 * asignaturas del catálogo (las que se listan en pantalla). Un cronograma que no corresponde
 * a ninguna asignatura del catálogo no entra en el contador, el titular ni las listas.
 */

export interface AvanceMateria {
  total: number
  completados: number
}

export interface AsignaturaHoy {
  stat?: AvanceMateria
  siguiente?: unknown
}

export interface AvanceGlobal {
  completados: number
  total: number
  porcentaje: number
}

/** Una asignatura tiene cronograma cuando se cruzó con uno que tiene al menos una clase. */
export function tieneCronograma(a: AsignaturaHoy): boolean {
  return !!a.stat && a.stat.total > 0
}

/** Clases completadas / total de las asignaturas con cronograma; null si no hay ninguna. */
export function avanceGlobal(asignaturas: readonly AsignaturaHoy[]): AvanceGlobal | null {
  let total = 0
  let completados = 0
  for (const a of asignaturas) {
    if (!a.stat || a.stat.total <= 0) continue
    total += a.stat.total
    completados += a.stat.completados
  }
  if (total === 0) return null
  return { completados, total, porcentaje: Math.round((completados / total) * 100) }
}

export type EstadoHoy =
  | 'sin_asignaturas' // el catálogo está vacío
  | 'sin_cronogramas' // hay asignaturas, pero ninguna tiene clases cargadas
  | 'pendiente' // alguna asignatura tiene una clase por estudiar
  | 'al_dia' // hay clases y todas están completadas

export function estadoHoy(asignaturas: readonly AsignaturaHoy[]): EstadoHoy {
  if (asignaturas.length === 0) return 'sin_asignaturas'
  if (!asignaturas.some(tieneCronograma)) return 'sin_cronogramas'
  return asignaturas.some((a) => !!a.siguiente) ? 'pendiente' : 'al_dia'
}

/** Los tres pasos de arranque; cada uno indica si ya está hecho. */
export function pasosDeArranque(asignaturas: readonly AsignaturaHoy[]) {
  const conCronograma = asignaturas.some(tieneCronograma)
  const completados = avanceGlobal(asignaturas)?.completados ?? 0
  return [
    { id: 'asignatura', hecho: asignaturas.length > 0 },
    { id: 'silabo', hecho: conCronograma },
    { id: 'tutoria', hecho: completados > 0 },
  ] as const
}
