import { describe, expect, it } from 'vitest'
import { ultimoTramo } from './rutas'

describe('ultimoTramo', () => {
  it('toma el último tramo de rutas POSIX y de Windows', () => {
    expect(ultimoTramo('/home/yo/Universidad/Redes')).toBe('Redes')
    expect(ultimoTramo('C:\\Users\\yo\\Universidad\\Redes')).toBe('Redes')
    expect(ultimoTramo('C:/Users/yo/Obsidian/Redes/Proyectos/app.md')).toBe('app.md')
  })

  it('ignora separadores al final y repetidos', () => {
    expect(ultimoTramo('/home/yo/Redes/')).toBe('Redes')
    expect(ultimoTramo('C:\\\\Users\\\\yo\\\\Redes\\')).toBe('Redes')
  })

  it('no inventa nada con valores vacíos o sin separadores', () => {
    expect(ultimoTramo('')).toBe('')
    expect(ultimoTramo(undefined)).toBe('')
    expect(ultimoTramo(null)).toBe('')
    expect(ultimoTramo('Redes')).toBe('Redes')
    expect(ultimoTramo('/')).toBe('/')
  })
})
