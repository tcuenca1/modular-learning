import type { SesionTutoriaResponse } from '@/api/types'

/**
 * Copia de la tutoría en curso en `sessionStorage`: sobrevive a recargar la página o a que el
 * navegador del móvil descarte la pestaña, y desaparece al cerrarla. Nunca debe cruzar cuentas:
 * se borra al cerrar sesión y cuando caduca.
 */
const CLAVE = 'ml.tutoria.v1'

export interface DudaGuardada {
  duda: string
  respuesta: string
}

export interface TutoriaGuardada {
  /** Destino con el que se abrió la vista (materia|tema|clase): otro destino = otra tutoría. */
  origen: string
  sesion: SesionTutoriaResponse
  pasoActual: number
  explicaciones: Record<number, string>
  completados: number[]
  dudas: Record<number, DudaGuardada[]>
}

function almacen(): Storage | null {
  try {
    return window.sessionStorage
  } catch {
    return null
  }
}

function esRegistro(valor: unknown): valor is Record<string, unknown> {
  return typeof valor === 'object' && valor !== null && !Array.isArray(valor)
}

/** Devuelve la tutoría guardada si es válida y corresponde a este destino; si no, null. */
export function leerTutoriaGuardada(origen: string): TutoriaGuardada | null {
  const s = almacen()
  if (!s) return null
  try {
    const bruto = s.getItem(CLAVE)
    if (!bruto) return null
    const d: unknown = JSON.parse(bruto)
    if (!esRegistro(d) || d.origen !== origen || !esRegistro(d.sesion)) return null
    const sesion = d.sesion as unknown as SesionTutoriaResponse
    if (typeof sesion.sesion_id !== 'string' || !Array.isArray(sesion.pasos) || sesion.pasos.length === 0) {
      return null
    }
    const ultimo = sesion.pasos.length - 1
    const paso = typeof d.pasoActual === 'number' ? Math.min(Math.max(0, d.pasoActual), ultimo) : 0
    return {
      origen,
      sesion,
      pasoActual: paso,
      explicaciones: esRegistro(d.explicaciones) ? (d.explicaciones as Record<number, string>) : {},
      completados: Array.isArray(d.completados)
        ? d.completados.filter((n): n is number => typeof n === 'number')
        : [],
      dudas: esRegistro(d.dudas) ? (d.dudas as Record<number, DudaGuardada[]>) : {},
    }
  } catch {
    return null
  }
}

export function guardarTutoria(estado: TutoriaGuardada): void {
  try {
    almacen()?.setItem(CLAVE, JSON.stringify(estado))
  } catch {
    // Sin espacio o bloqueado: la tutoría sigue en memoria, solo no sobrevivirá a una recarga
  }
}

export function borrarTutoriaGuardada(): void {
  try {
    almacen()?.removeItem(CLAVE)
  } catch {
    // Nada que borrar si el almacenamiento no está disponible
  }
}
