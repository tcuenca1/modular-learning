/** Validaciones puras del acceso con cuentas. Devuelven un mensaje en español o null si es válido. */

export const LONGITUD_MINIMA_CONTRASENA = 10

const PATRON_CORREO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export function validarCorreo(correo: string): string | null {
  const limpio = correo.trim()
  if (!limpio) return 'Escribe tu correo.'
  if (!PATRON_CORREO.test(limpio)) return 'Escribe un correo válido, por ejemplo nombre@dominio.com.'
  return null
}

export function validarContrasenaNueva(contrasena: string): string | null {
  if (!contrasena) return 'Escribe la nueva contraseña.'
  if (contrasena.length < LONGITUD_MINIMA_CONTRASENA) {
    return `La contraseña debe tener al menos ${LONGITUD_MINIMA_CONTRASENA} caracteres.`
  }
  return null
}

export function validarCoincidencia(nueva: string, confirmacion: string): string | null {
  if (nueva !== confirmacion) return 'Las contraseñas no coinciden.'
  return null
}

/** Primer error del formulario de acceso, o null si se puede enviar. */
export function validarLogin(correo: string, contrasena: string): string | null {
  return validarCorreo(correo) ?? (contrasena ? null : 'Escribe tu contraseña.')
}

/** Primer error del formulario de cambio de contraseña, o null si se puede enviar. */
export function validarCambioContrasena(
  actual: string,
  nueva: string,
  confirmacion: string
): string | null {
  if (!actual) return 'Escribe tu contraseña actual.'
  return (
    validarContrasenaNueva(nueva) ??
    validarCoincidencia(nueva, confirmacion) ??
    (nueva === actual ? 'La nueva contraseña debe ser distinta de la actual.' : null)
  )
}

/** Primer error del formulario de alta de usuario, o null si se puede enviar. */
export function validarNuevoUsuario(correo: string, nombre: string, contrasena: string): string | null {
  if (!nombre.trim()) return 'Escribe el nombre.'
  return validarCorreo(correo) ?? validarContrasenaNueva(contrasena)
}
