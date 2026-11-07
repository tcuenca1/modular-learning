/** Utilidades de las guías de estudio offline. */
import type { ExtensionGuia } from '@/api/types'

export const MAXIMO_CLASES_GUIA = 16

export const NOMBRE_EXTENSION: Record<ExtensionGuia, string> = {
  completa: 'completa',
  estandar: 'estándar',
  sintesis: 'síntesis',
}

/** Misma regla que el dominio (`elegir_extension`), con presupuesto de tiempo opcional. */
export function extensionPara(n: number, tiempoMinutos?: number | null): ExtensionGuia {
  if (n <= 0) return 'estandar'
  if (tiempoMinutos && tiempoMinutos > 0) {
    const minPorClase = tiempoMinutos / n
    if (minPorClase >= 45) return 'completa'
    if (minPorClase >= 20) return 'estandar'
    return 'sintesis'
  }
  if (n <= 2) return 'completa'
  if (n <= 5) return 'estandar'
  return 'sintesis'
}
