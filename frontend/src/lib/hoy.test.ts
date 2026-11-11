import { describe, expect, it } from 'vitest'
import { avanceGlobal, estadoHoy, pasosDeArranque, tieneCronograma } from './hoy'

const conClases = (total: number, completados: number, siguiente = completados < total) => ({
  stat: { total, completados },
  siguiente: siguiente ? { tema: 'x' } : undefined,
})
const sinCronograma = {}

describe('avanceGlobal', () => {
  it('suma solo las asignaturas con cronograma', () => {
    expect(avanceGlobal([conClases(2, 1), conClases(4, 4), sinCronograma])).toEqual({
      completados: 5,
      total: 6,
      porcentaje: 83,
    })
  })

  it('es null cuando ninguna asignatura tiene clases (no hay contador que mostrar)', () => {
    expect(avanceGlobal([])).toBeNull()
    expect(avanceGlobal([sinCronograma, sinCronograma])).toBeNull()
    expect(avanceGlobal([{ stat: { total: 0, completados: 0 } }])).toBeNull()
  })

  it('no cuenta un cronograma huérfano: el caso 1/2 con 5 asignaturas sin cronograma', () => {
    // El backend sumaba 1/2 de un cronograma ajeno al catálogo; aquí solo se mira lo listado
    const catalogo = Array.from({ length: 5 }, () => sinCronograma)
    expect(avanceGlobal(catalogo)).toBeNull()
    expect(estadoHoy(catalogo)).toBe('sin_cronogramas')
  })
})

describe('estadoHoy', () => {
  it('sin asignaturas', () => expect(estadoHoy([])).toBe('sin_asignaturas'))
  it('con asignaturas pero sin cronogramas', () =>
    expect(estadoHoy([sinCronograma, { stat: { total: 0, completados: 0 } }])).toBe(
      'sin_cronogramas'
    ))
  it('con una clase pendiente', () =>
    expect(estadoHoy([conClases(2, 1), sinCronograma])).toBe('pendiente'))
  it('con todo completado', () => expect(estadoHoy([conClases(2, 2), sinCronograma])).toBe('al_dia'))
})

describe('coherencia entre contador y titular', () => {
  it('"no hay pendientes" solo ocurre si hay clases y todas están completadas', () => {
    const casos = [[], [sinCronograma], [conClases(2, 1)], [conClases(2, 2)]]
    for (const c of casos) {
      const av = avanceGlobal(c)
      if (estadoHoy(c) === 'al_dia') expect(av?.completados).toBe(av?.total)
      if (estadoHoy(c) === 'pendiente') expect(av && av.completados < av.total).toBe(true)
      if (av === null) expect(['sin_asignaturas', 'sin_cronogramas']).toContain(estadoHoy(c))
    }
  })
})

describe('pasosDeArranque', () => {
  it('marca lo que ya está hecho', () => {
    expect(pasosDeArranque([]).map((p) => p.hecho)).toEqual([false, false, false])
    expect(pasosDeArranque([sinCronograma]).map((p) => p.hecho)).toEqual([true, false, false])
    expect(pasosDeArranque([conClases(2, 0)]).map((p) => p.hecho)).toEqual([true, true, false])
    expect(pasosDeArranque([conClases(2, 1)]).map((p) => p.hecho)).toEqual([true, true, true])
  })
})

describe('tieneCronograma', () => {
  it('exige al menos una clase', () => {
    expect(tieneCronograma(conClases(1, 0))).toBe(true)
    expect(tieneCronograma({ stat: { total: 0, completados: 0 } })).toBe(false)
    expect(tieneCronograma(sinCronograma)).toBe(false)
  })
})
