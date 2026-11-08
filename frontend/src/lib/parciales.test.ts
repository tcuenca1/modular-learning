import { describe, expect, it } from 'vitest'
import { describirCorte, resolverIndiceHasta, type ClaseParaCorte } from './parciales'

describe('resolverIndiceHasta', () => {
  const clases: ClaseParaCorte[] = [
    { id: 'clase-1', fecha: '01/10/2026', tema: 'Introducción' },
    { id: 'clase-2', fecha: '08/10/2026', tema: 'Criptografía simétrica' },
    { id: 'clase-3', fecha: '15/10/2026', tema: 'Criptografía asimétrica' },
    { id: 'clase-4', fecha: '22/10/2026', tema: 'Firmas digitales' },
  ]

  it('resuelve correctamente por id de clase', () => {
    expect(resolverIndiceHasta(clases, 'clase-1')).toBe(0)
    expect(resolverIndiceHasta(clases, 'clase-3')).toBe(2)
    expect(resolverIndiceHasta(clases, 'clase-4')).toBe(3)
  })

  it('resuelve correctamente por fecha antigua en formato dd/mm/aaaa', () => {
    // Coincidencia exacta de fecha
    expect(resolverIndiceHasta(clases, '15/10/2026')).toBe(2)
    // Fecha intermedia entre clase 2 (08/10) y clase 3 (15/10): devuelve clase 2
    expect(resolverIndiceHasta(clases, '10/10/2026')).toBe(1)
    // Fecha posterior a todas las clases: devuelve la última clase
    expect(resolverIndiceHasta(clases, '30/10/2026')).toBe(3)
  })

  it('resuelve correctamente por fecha antigua en formato ISO', () => {
    expect(resolverIndiceHasta(clases, '2026-10-08')).toBe(1)
  })

  it('devuelve -1 ante valores invalidos o no encontrados', () => {
    expect(resolverIndiceHasta(clases, null)).toBe(-1)
    expect(resolverIndiceHasta(clases, undefined)).toBe(-1)
    expect(resolverIndiceHasta(clases, '')).toBe(-1)
    expect(resolverIndiceHasta(clases, '   ')).toBe(-1)
    expect(resolverIndiceHasta(clases, 'id-inexistente')).toBe(-1)
    expect(resolverIndiceHasta(clases, 'texto-cualquiera')).toBe(-1)
    // Fecha anterior a la primera clase
    expect(resolverIndiceHasta(clases, '01/01/2020')).toBe(-1)
    // Lista de clases vacía
    expect(resolverIndiceHasta([], 'clase-1')).toBe(-1)
  })
})

describe('describirCorte', () => {
  const clases: ClaseParaCorte[] = [
    { id: 'clase-1', fecha: '01/10/2026', tema: 'Introducción' },
    { id: 'clase-2', fecha: '08/10/2026', tema: 'Criptografía simétrica' },
  ]

  it('muestra la fecha y el tema de la clase identificada por id', () => {
    expect(describirCorte(clases, 'clase-2')).toBe('08/10/2026 · Criptografía simétrica')
  })

  it('muestra la fecha y el tema cuando se consulta por fecha antigua', () => {
    expect(describirCorte(clases, '01/10/2026')).toBe('01/10/2026 · Introducción')
  })

  it('devuelve el valor original o fallback si no se puede resolver', () => {
    expect(describirCorte(clases, 'desconocido')).toBe('desconocido')
    expect(describirCorte(clases, '')).toBe('final')
    expect(describirCorte(clases, null)).toBe('final')
  })
})
