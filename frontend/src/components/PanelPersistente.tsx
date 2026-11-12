import { useState } from 'react'
import type { ReactNode } from 'react'

/**
 * Panel de una pestaña que, una vez abierto, sigue montado aunque se cambie de pestaña: solo se
 * oculta. Así una tutoría, un quiz o una ingesta en curso no se pierden al mirar otra pestaña.
 */
export function PanelPersistente({ activo, children }: { activo: boolean; children: ReactNode }) {
  const [abierto, setAbierto] = useState(activo)
  if (activo && !abierto) setAbierto(true)
  if (!abierto) return null
  return <div hidden={!activo}>{children}</div>
}
