/** Lógica del calendario: qué mes abrir y cuál es la próxima clase. */
import type { ClaseFechada } from './asignaturas'

type ClaseConFecha = Pick<ClaseFechada, 'fecha' | 'completada'>

export function primerDiaDelMes(fecha: Date): Date {
  return new Date(fecha.getFullYear(), fecha.getMonth(), 1)
}

/**
 * La clase que toca: la pendiente más próxima desde `hoy` y, si no hay ninguna por delante, la
 * pendiente más antigua (el atraso). Null si todas están completadas.
 */
export function proximaClase<T extends ClaseConFecha>(clases: readonly T[], hoy: Date): T | null {
  const pendientes = clases.filter((c) => !c.completada).sort((a, b) => a.fecha.getTime() - b.fecha.getTime())
  return pendientes.find((c) => c.fecha.getTime() >= hoy.getTime()) ?? pendientes[0] ?? null
}

/** Mes con el que abre el calendario: el actual si tiene clases; si no, el de la próxima clase. */
export function mesInicial(clases: readonly ClaseConFecha[], hoy: Date): Date {
  const actual = primerDiaDelMes(hoy)
  const hayEnElMesActual = clases.some(
    (c) => c.fecha.getMonth() === hoy.getMonth() && c.fecha.getFullYear() === hoy.getFullYear()
  )
  if (hayEnElMesActual) return actual
  const proxima = proximaClase(clases, hoy)
  return proxima ? primerDiaDelMes(proxima.fecha) : actual
}
