/** Utilidades de las guías de estudio offline. */
import type { ExtensionGuia } from '@/api/types'

export const MAXIMO_CLASES_GUIA = 12

export const NOMBRE_EXTENSION: Record<ExtensionGuia, string> = {
  completa: 'completa',
  estandar: 'estándar',
  sintesis: 'síntesis',
}

/** Misma regla que el dominio (`elegir_extension`), solo para anticipar el tamaño de la guía. */
export function extensionPara(n: number): ExtensionGuia {
  if (n <= 2) return 'completa'
  if (n <= 5) return 'estandar'
  return 'sintesis'
}
