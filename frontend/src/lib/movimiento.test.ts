import { readFileSync } from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'

const css = readFileSync(path.resolve(import.meta.dirname, '../index.css'), 'utf-8')

/** Texto del bloque que empieza en `inicio` (hasta su llave de cierre) y el CSS sin ese bloque. */
function separarBloque(texto: string, inicio: string): { bloque: string; resto: string } {
  const desde = texto.indexOf(inicio)
  if (desde === -1) throw new Error(`No encuentro ${inicio}`)
  let profundidad = 0
  for (let i = texto.indexOf('{', desde); i < texto.length; i++) {
    if (texto[i] === '{') profundidad++
    if (texto[i] === '}' && --profundidad === 0) {
      return { bloque: texto.slice(desde, i + 1), resto: texto.slice(0, desde) + texto.slice(i + 1) }
    }
  }
  throw new Error('Llaves sin cerrar')
}

describe('movimiento respetuoso (prefers-reduced-motion)', () => {
  const { bloque, resto } = separarBloque(css, '@media (prefers-reduced-motion: no-preference)')

  it('el bloque contiene las animaciones y las transiciones de los botones', () => {
    expect(bloque).toContain('@keyframes entrada-vista')
    expect(bloque).toContain('.animar-cajon')
    expect(bloque).toContain('button:not(:disabled):active')
  })

  it('fuera de ese bloque no hay animaciones, keyframes ni transiciones escritas a mano', () => {
    expect(resto).not.toMatch(/@keyframes/)
    expect(resto).not.toMatch(/animation\s*:/)
    expect(resto).not.toMatch(/transition(-property|-duration)?\s*:/)
  })

  it('solo se animan propiedades baratas: transform y opacity', () => {
    const propiedades = [...bloque.matchAll(/^\s{4,}([a-z-]+)\s*:/gm)].map((m) => m[1])
    const permitidas = new Set([
      'opacity', 'transform', 'animation', 'transition-property', 'transition-duration', 'transition-timing-function',
    ])
    expect(propiedades.filter((p) => !permitidas.has(p))).toEqual([])
  })

  it('las duraciones no superan 200 ms', () => {
    const ms = [...bloque.matchAll(/(\d+)ms/g)].map((m) => Number(m[1]))
    expect(ms.length).toBeGreaterThan(0)
    expect(Math.max(...ms)).toBeLessThanOrEqual(200)
  })
})
