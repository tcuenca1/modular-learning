import { describe, expect, it } from 'vitest'
import {
  validarCambioContrasena,
  validarContrasenaNueva,
  validarCoincidencia,
  validarCorreo,
  validarLogin,
  validarNuevoUsuario,
} from './auth'

describe('validarCorreo', () => {
  it('acepta correos normales con espacios alrededor', () => {
    expect(validarCorreo(' ana@uni.edu.ec ')).toBeNull()
  })
  it('rechaza vacío y formatos incompletos', () => {
    expect(validarCorreo('')).toBe('Escribe tu correo.')
    expect(validarCorreo('   ')).toBe('Escribe tu correo.')
    expect(validarCorreo('ana')).toMatch(/válido/)
    expect(validarCorreo('ana@uni')).toMatch(/válido/)
    expect(validarCorreo('a na@uni.com')).toMatch(/válido/)
  })
})

describe('validarContrasenaNueva', () => {
  it('exige al menos 10 caracteres', () => {
    expect(validarContrasenaNueva('')).toMatch(/Escribe/)
    expect(validarContrasenaNueva('123456789')).toMatch(/10 caracteres/)
    expect(validarContrasenaNueva('1234567890')).toBeNull()
  })
})

describe('validarCoincidencia', () => {
  it('compara exactamente', () => {
    expect(validarCoincidencia('abc', 'abc')).toBeNull()
    expect(validarCoincidencia('abc', 'abC')).toBe('Las contraseñas no coinciden.')
  })
})

describe('validarLogin', () => {
  it('pide correo válido y contraseña', () => {
    expect(validarLogin('', 'x')).toBe('Escribe tu correo.')
    expect(validarLogin('a@b.co', '')).toBe('Escribe tu contraseña.')
    expect(validarLogin('a@b.co', 'x')).toBeNull()
  })
})

describe('validarCambioContrasena', () => {
  it('valida en orden: actual, longitud, coincidencia, distinta', () => {
    expect(validarCambioContrasena('', 'nuevaclave123', 'nuevaclave123')).toMatch(/actual/)
    expect(validarCambioContrasena('vieja', 'corta', 'corta')).toMatch(/10 caracteres/)
    expect(validarCambioContrasena('vieja', 'nuevaclave123', 'otraclave123')).toMatch(/no coinciden/)
    expect(validarCambioContrasena('nuevaclave123', 'nuevaclave123', 'nuevaclave123')).toMatch(/distinta/)
    expect(validarCambioContrasena('vieja', 'nuevaclave123', 'nuevaclave123')).toBeNull()
  })
})

describe('validarNuevoUsuario', () => {
  it('exige nombre, correo y contraseña válidos', () => {
    expect(validarNuevoUsuario('a@b.co', ' ', 'clavelarga123')).toMatch(/nombre/)
    expect(validarNuevoUsuario('malo', 'Ana', 'clavelarga123')).toMatch(/válido/)
    expect(validarNuevoUsuario('a@b.co', 'Ana', 'corta')).toMatch(/10 caracteres/)
    expect(validarNuevoUsuario('a@b.co', 'Ana', 'clavelarga123')).toBeNull()
  })
})
