import { describe, expect, it } from 'vitest'
import { extensionPara, MAXIMO_CLASES_GUIA, NOMBRE_EXTENSION } from './guias'

describe('extensionPara', () => {
  it('aplica reglas según número de clases cuando no hay tiempo límite', () => {
    expect(extensionPara(0)).toBe('estandar')
    expect(extensionPara(1)).toBe('completa')
    expect(extensionPara(2)).toBe('completa')
    expect(extensionPara(3)).toBe('estandar')
    expect(extensionPara(5)).toBe('estandar')
    expect(extensionPara(6)).toBe('sintesis')
    expect(extensionPara(10)).toBe('sintesis')
  })

  it('adapta la extensión según el presupuesto de tiempo', () => {
    // 2 clases con 120 min = 60 min/clase (>= 45) -> completa
    expect(extensionPara(2, 120)).toBe('completa')

    // 4 clases con 120 min = 30 min/clase (>= 20) -> estandar
    expect(extensionPara(4, 120)).toBe('estandar')

    // 8 clases con 120 min = 15 min/clase (< 20) -> sintesis
    expect(extensionPara(8, 120)).toBe('sintesis')

    // 1 clase con 15 minutos -> sintesis
    expect(extensionPara(1, 15)).toBe('sintesis')
  })
})

describe('constantes de guías', () => {
  it('tiene configurados nombres legibles y límite', () => {
    expect(MAXIMO_CLASES_GUIA).toBe(16)
    expect(NOMBRE_EXTENSION.completa).toBe('completa')
    expect(NOMBRE_EXTENSION.estandar).toBe('estándar')
    expect(NOMBRE_EXTENSION.sintesis).toBe('síntesis')
  })
})
