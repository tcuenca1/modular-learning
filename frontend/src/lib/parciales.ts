/** Utilidades para la resolución y presentación de cortes de parcial. */
import { parsearFecha } from './asignaturas'

export interface ClaseParaCorte {
  id?: string | number
  tema?: string
  fecha?: string
}

/**
 * Resuelve el índice de la clase hasta la cual abarca un corte de parcial.
 *
 * 1. Primero busca una clase cuyo id coincida con `hasta`.
 * 2. Si no coincide con ningún id, interpreta `hasta` como fecha (antiguos cortes con fecha,
 *    ej. "15/10/2026" o "2026-10-15"). En ese caso, devuelve el índice de la última clase
 *    cuya fecha sea menor o igual a esa fecha de corte.
 * 3. Si `hasta` es inválido o no coincide con ninguna clase ni fecha válida, devuelve -1.
 */
export function resolverIndiceHasta(
  clases: readonly ClaseParaCorte[],
  hasta: string | undefined | null
): number {
  if (!hasta || clases.length === 0) return -1

  const hastaStr = String(hasta).trim()
  if (!hastaStr) return -1

  // 1. Coincidencia directa por id
  const idxId = clases.findIndex((c) => c.id !== undefined && String(c.id) === hastaStr)
  if (idxId !== -1) return idxId

  // 2. Coincidencia por fecha antigua
  const fechaCorte = parsearFecha(hastaStr)
  if (fechaCorte) {
    const tiempoCorte = fechaCorte.getTime()
    let ultimoIdx = -1
    for (let i = 0; i < clases.length; i++) {
      const fechaClase = parsearFecha(clases[i].fecha)
      if (fechaClase && fechaClase.getTime() <= tiempoCorte) {
        ultimoIdx = i
      }
    }
    return ultimoIdx
  }

  // 3. Valor inválido
  return -1
}

/**
 * Devuelve una descripción legible de la clase límite del corte (tema y fecha),
 * evitando mostrar identificadores crudos.
 */
export function describirCorte(
  clases: readonly ClaseParaCorte[],
  hasta: string | undefined | null
): string {
  const idx = resolverIndiceHasta(clases, hasta)
  if (idx >= 0) {
    const c = clases[idx]
    const partes: string[] = []
    if (c.fecha) partes.push(c.fecha)
    if (c.tema) partes.push(c.tema)
    if (partes.length > 0) return partes.join(' · ')
    return `Clase ${idx + 1}`
  }
  return hasta || 'final'
}
