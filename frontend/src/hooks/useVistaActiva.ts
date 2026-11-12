import { createContext, useContext } from 'react'

/**
 * Las vistas con IA (Estudiar, Asignaturas) se mantienen montadas al navegar para no perder una
 * generación en curso. Este contexto avisa si la vista está a la vista: las que tocan la URL deben
 * quedarse quietas mientras están ocultas.
 */
export const VistaActivaContext = createContext(true)

export function useVistaActiva(): boolean {
  return useContext(VistaActivaContext)
}
