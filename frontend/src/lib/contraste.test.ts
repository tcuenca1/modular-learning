import { readFileSync } from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'

/** Lee un token CSS (`--nombre: #rrggbb;`) del bloque que empieza en `selector`. */
const css = readFileSync(path.resolve(import.meta.dirname, '../index.css'), 'utf-8')

function token(nombre: string, selector?: string): string {
  const zona = selector ? css.slice(css.indexOf(selector)) : css
  const m = zona.match(new RegExp(`${nombre}:\\s*(#[0-9a-fA-F]{6})`))
  if (!m) throw new Error(`No encuentro ${nombre}${selector ? ` en ${selector}` : ''}`)
  return m[1]
}

function luminancia(hex: string): number {
  const [r, g, b] = [1, 3, 5].map((i) => {
    const c = parseInt(hex.slice(i, i + 2), 16) / 255
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

function contraste(a: string, b: string): number {
  const [la, lb] = [luminancia(a), luminancia(b)].sort((x, y) => y - x)
  return (la + 0.05) / (lb + 0.05)
}

const claro = {
  fondos: ['--color-white', '--color-slate-50', '--color-slate-100'].map((t) => token(t)),
  slate400: token('--ml-slate-400', ':root {'),
  slate500: token('--ml-slate-500', ':root {'),
  rojo: token('--ml-rose-600', ':root {'),
}
const oscuro = {
  fondos: ['--color-slate-800', '--color-slate-900', '--color-slate-950'].map((t) => token(t)),
  slate400: token('--ml-slate-400', 'html.dark {'),
  slate500: token('--ml-slate-500', 'html.dark {'),
  rojo: token('--ml-rose-600', 'html.dark {'),
  verde: token('--color-indigo-400'),
}

describe('contraste AA (4,5:1) del texto secundario', () => {
  it.each(Object.entries({ slate400: claro.slate400, slate500: claro.slate500, rojo: claro.rojo }))(
    'tema claro: %s sobre el papel',
    (_nombre, color) => {
      for (const fondo of claro.fondos) expect(contraste(color, fondo)).toBeGreaterThanOrEqual(4.5)
    }
  )

  it.each(
    Object.entries({
      slate400: oscuro.slate400,
      slate500: oscuro.slate500,
      rojo: oscuro.rojo,
      verde: oscuro.verde,
    })
  )('tema oscuro: %s sobre el grafito', (_nombre, color) => {
    for (const fondo of oscuro.fondos) expect(contraste(color, fondo)).toBeGreaterThanOrEqual(4.5)
  })

  it('el texto oscuro sobre el verde de acento (botones en tema oscuro) también cumple', () => {
    expect(contraste(token('--color-slate-950'), oscuro.verde)).toBeGreaterThanOrEqual(4.5)
  })
})
