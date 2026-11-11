/** Presentación de rutas del equipo: en pantalla solo el último tramo; la ruta completa, en un title. */

/** Último tramo de una ruta (`C:\Users\yo\Uni\Redes` → `Redes`); admite / y \ y separadores finales. */
export function ultimoTramo(ruta: string | null | undefined): string {
  if (!ruta) return ''
  const tramos = ruta.split(/[\\/]+/).filter(Boolean)
  return tramos.length > 0 ? tramos[tramos.length - 1] : ruta
}
