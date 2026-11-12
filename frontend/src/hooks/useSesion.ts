import { createContext, useContext } from 'react'
import type { Usuario } from '@/api/types'

export interface ContextoSesion {
  /** false: modo local sin login */
  autenticacion: boolean
  usuario: Usuario | null
  salir: () => Promise<void>
}

export const SesionContext = createContext<ContextoSesion>({
  autenticacion: false,
  usuario: null,
  salir: async () => {},
})

export function useSesion(): ContextoSesion {
  return useContext(SesionContext)
}
