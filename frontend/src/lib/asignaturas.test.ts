import { describe, expect, it } from 'vitest'
import {
  buscarMateriaPorClave,
  clave,
  clasesConFecha,
  describirFecha,
  enlaceTutoria,
  esCompletada,
  materiasConCronograma,
  parsearFecha,
} from './asignaturas'

describe('clave', () => {
  it('normaliza tildes, mayúsculas y caracteres especiales', () => {
    expect(clave('Ingeniería de Software II')).toBe('ingenieriadesoftwareii')
    expect(clave('INGENIERIA_DE_SOFTWARE_II')).toBe('ingenieriadesoftwareii')
    expect(clave('Seguridad de la Información!')).toBe('seguridaddelainformacion')
    expect(clave('Tecnologías de Conmutación I')).toBe('tecnologiasdeconmutacioni')
  })
})

describe('parsearFecha', () => {
  it('parsea fechas en formato dd/mm/aaaa', () => {
    const f = parsearFecha('15/10/2026')
    expect(f).toBeDefined()
    expect(f?.getDate()).toBe(15)
    expect(f?.getMonth()).toBe(9) // octubre es 9 en JS (0-indexed)
    expect(f?.getFullYear()).toBe(2026)
  })

  it('parsea fechas en formato ISO', () => {
    const f = parsearFecha('2026-10-15T08:00:00Z')
    expect(f).toBeDefined()
    expect(f?.getUTCFullYear()).toBe(2026)
  })

  it('retorna undefined para entradas no válidas', () => {
    expect(parsearFecha(null)).toBeUndefined()
    expect(parsearFecha(undefined)).toBeUndefined()
    expect(parsearFecha('fecha-invalida')).toBeUndefined()
  })
})

describe('describirFecha', () => {
  const hoy = new Date(2026, 9, 15) // 15 de octubre de 2026

  it('describe correctamente fechas relativas', () => {
    expect(describirFecha(undefined, hoy)).toBe('sin fecha en el cronograma')
    expect(describirFecha(new Date(2026, 9, 15), hoy)).toBe('es hoy')
    expect(describirFecha(new Date(2026, 9, 16), hoy)).toBe('es mañana')
    expect(describirFecha(new Date(2026, 9, 18), hoy)).toBe('en 3 días')
    expect(describirFecha(new Date(2026, 9, 14), hoy)).toBe('fue ayer')
    expect(describirFecha(new Date(2026, 9, 10), hoy)).toBe('fue hace 5 días')
  })
})

describe('esCompletada', () => {
  it('detecta clases completadas', () => {
    expect(esCompletada({ tema: 'T', estado: 'completado' })).toBe(true)
    expect(esCompletada({ tema: 'T', estado: 'Completada' })).toBe(true)
    expect(esCompletada({ tema: 'T', estado: 'pendiente' })).toBe(false)
    expect(esCompletada({ tema: 'T' })).toBe(false)
  })
})

describe('clasesConFecha y materiasConCronograma', () => {
  const cronogramas = {
    INGENIERIA_DE_SOFTWARE_II: [
      { fecha: '12/10/2026', tema: 'Arquitectura', estado: 'completado' },
      { fecha: '16/10/2026', tema: 'Testing', estado: 'pendiente' },
    ],
    PROGRAMACION_WEB: [
      { fecha: '10/10/2026', tema: 'HTML & CSS', estado: 'completado' },
    ],
  }
  const catalogo = ['Ingeniería de Software II', 'Programación Web']

  it('cruza cronogramas con catálogo y ordena por fecha', () => {
    const fechadas = clasesConFecha(cronogramas, catalogo)
    expect(fechadas).toHaveLength(3)
    expect(fechadas[0].materia).toBe('Programación Web')
    expect(fechadas[0].clase.tema).toBe('HTML & CSS')
    expect(fechadas[1].materia).toBe('Ingeniería de Software II')
    expect(fechadas[1].clase.tema).toBe('Arquitectura')
    expect(fechadas[2].clase.tema).toBe('Testing')
  })

  it('agrupa asignaturas con cronograma', () => {
    const mats = materiasConCronograma(cronogramas, catalogo)
    expect(mats).toHaveLength(2)
    expect(mats[0].materia).toBe('Ingeniería de Software II')
    expect(mats[1].materia).toBe('Programación Web')
  })

  it('cruza cronogramas cuyas claves son slugs con el catálogo', () => {
    const cronogramasSlug = {
      'ingenieria-de-software-ii': [
        { fecha: '12/10/2026', tema: 'Arquitectura', estado: 'completado' },
      ],
    }
    const fechadas = clasesConFecha(cronogramasSlug, catalogo)
    expect(fechadas[0].materia).toBe('Ingeniería de Software II')

    const mats = materiasConCronograma(cronogramasSlug, catalogo)
    expect(mats[0].materia).toBe('Ingeniería de Software II')
  })
})

describe('enlaceTutoria', () => {
  it('genera enlace solo con materia', () => {
    expect(enlaceTutoria('Redes')).toBe('/tutoria?materia=Redes')
  })

  it('genera enlace con tema y sin clase_id', () => {
    expect(enlaceTutoria('Redes', 'BGP')).toBe('/tutoria?materia=Redes&tema=BGP')
    expect(enlaceTutoria('Redes', 'BGP', 'duda')).toBe('/tutoria?materia=Redes&tema=BGP&enfoque=duda')
  })

  it('incluye clase_id en la query si viene', () => {
    expect(enlaceTutoria('Redes', 'BGP', undefined, 'clase-42')).toBe(
      '/tutoria?materia=Redes&tema=BGP&clase_id=clase-42'
    )
    expect(enlaceTutoria('Redes', 'BGP', 'duda', 'clase-42')).toBe(
      '/tutoria?materia=Redes&tema=BGP&enfoque=duda&clase_id=clase-42'
    )
  })
})

describe('buscarMateriaPorClave', () => {
  const catalogo = [
    { slug: 'ingenieria-de-software-ii', nombre: 'Ingeniería de Software II' },
    { slug: 'redes-de-computadores', nombre: 'Redes de Computadores' },
  ]

  it('encuentra por nombre exacto con tildes', () => {
    const m = buscarMateriaPorClave(catalogo, 'Ingeniería de Software II')
    expect(m?.slug).toBe('ingenieria-de-software-ii')
  })

  it('encuentra por slug normalizado sin tildes', () => {
    const m = buscarMateriaPorClave(catalogo, 'ingenieria-de-software-ii')
    expect(m?.nombre).toBe('Ingeniería de Software II')
  })

  it('encuentra aunque el texto buscado tenga tildes en el slug o este en mayusculas', () => {
    const m1 = buscarMateriaPorClave(catalogo, 'ingeniería-de-software-ii')
    expect(m1?.slug).toBe('ingenieria-de-software-ii')
    const m2 = buscarMateriaPorClave(catalogo, 'INGENIERIA DE SOFTWARE II')
    expect(m2?.slug).toBe('ingenieria-de-software-ii')
  })

  it('retorna undefined si no coincide', () => {
    expect(buscarMateriaPorClave(catalogo, 'Física')).toBeUndefined()
    expect(buscarMateriaPorClave(catalogo, '')).toBeUndefined()
  })
})

