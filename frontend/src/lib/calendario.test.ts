import { describe, expect, it } from 'vitest'
import { mesInicial, primerDiaDelMes, proximaClase } from './calendario'

const clase = (fecha: string, completada = false) => ({ fecha: new Date(`${fecha}T00:00:00`), completada })
const hoy = new Date('2026-11-11T00:00:00')

describe('proximaClase', () => {
  it('prefiere la pendiente más próxima por delante de hoy', () => {
    const c = [clase('2026-10-08'), clase('2026-12-02'), clase('2026-11-20'), clase('2026-11-15', true)]
    expect(proximaClase(c, hoy)).toBe(c[2])
  })

  it('cuenta la clase de hoy', () => {
    const c = [clase('2026-11-11'), clase('2026-11-18')]
    expect(proximaClase(c, hoy)).toBe(c[0])
  })

  it('sin pendientes por delante devuelve la pendiente más antigua (atraso)', () => {
    const c = [clase('2026-10-15'), clase('2026-10-08'), clase('2026-09-01', true)]
    expect(proximaClase(c, hoy)).toBe(c[1])
  })

  it('devuelve null si todo está completado o no hay clases', () => {
    expect(proximaClase([clase('2026-10-08', true)], hoy)).toBeNull()
    expect(proximaClase([], hoy)).toBeNull()
  })
})

describe('mesInicial', () => {
  it('abre el mes actual si tiene clases', () => {
    expect(mesInicial([clase('2026-11-25'), clase('2026-12-02')], hoy)).toEqual(new Date(2026, 10, 1))
  })

  it('abre el mes de la próxima clase si el actual no tiene clases', () => {
    expect(mesInicial([clase('2026-10-08'), clase('2026-12-02')], hoy)).toEqual(new Date(2026, 11, 1))
  })

  it('cae en el mes del atraso cuando no queda nada por delante', () => {
    expect(mesInicial([clase('2026-10-08'), clase('2026-10-15', true)], hoy)).toEqual(new Date(2026, 9, 1))
  })

  it('con todo completado o sin clases se queda en el mes actual', () => {
    expect(mesInicial([clase('2026-10-08', true)], hoy)).toEqual(primerDiaDelMes(hoy))
    expect(mesInicial([], hoy)).toEqual(primerDiaDelMes(hoy))
  })
})
