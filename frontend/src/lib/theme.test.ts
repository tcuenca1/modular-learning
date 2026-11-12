import fs from 'node:fs'
import path from 'node:path'
import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('Gestión de tema (theme.ts)', () => {
  let storage: Record<string, string>
  let classes: Set<string>

  beforeEach(() => {
    storage = {}
    classes = new Set<string>()

    vi.stubGlobal('localStorage', {
      getItem: (key: string) => storage[key] ?? null,
      setItem: (key: string, val: string) => {
        storage[key] = val
      },
      removeItem: (key: string) => {
        delete storage[key]
      },
      clear: () => {
        storage = {}
      },
    })

    vi.stubGlobal('document', {
      documentElement: {
        classList: {
          add: (cls: string) => classes.add(cls),
          remove: (cls: string) => classes.delete(cls),
          contains: (cls: string) => classes.has(cls),
        },
      },
    })
  })

  it('devuelve "system" por defecto si no hay nada guardado', async () => {
    const { obtenerTemaGuardado } = await import('./theme')
    expect(obtenerTemaGuardado()).toBe('system')
  })

  it('guarda y recupera temas válidos', async () => {
    const { obtenerTemaGuardado } = await import('./theme')
    storage.ml_theme = 'dark'
    expect(obtenerTemaGuardado()).toBe('dark')

    storage.ml_theme = 'light'
    expect(obtenerTemaGuardado()).toBe('light')

    storage.ml_theme = 'invalido'
    expect(obtenerTemaGuardado()).toBe('system')
  })

  it('aplica tema claro añadiendo clase light y quitando dark', async () => {
    const { aplicarTema } = await import('./theme')
    classes.add('dark')
    aplicarTema('light')
    expect(classes.has('light')).toBe(true)
    expect(classes.has('dark')).toBe(false)
    expect(storage.ml_theme).toBe('light')
  })

  it('aplica tema oscuro añadiendo clase dark y quitando light', async () => {
    const { aplicarTema } = await import('./theme')
    classes.add('light')
    aplicarTema('dark')
    expect(classes.has('dark')).toBe(true)
    expect(classes.has('light')).toBe(false)
    expect(storage.ml_theme).toBe('dark')
  })

  it('aplica tema del sistema consultando matchMedia', async () => {
    vi.stubGlobal('window', {
      matchMedia: (query: string) => ({
        matches: query.includes('dark'),
        addEventListener: vi.fn(),
      }),
    })

    const { aplicarTema } = await import('./theme')
    aplicarTema('system')
    expect(classes.has('dark')).toBe(true)
    expect(classes.has('light')).toBe(false)
  })

  it('index.css no contiene @media (prefers-color-scheme: dark) ni selectores html.light para contrarrestar', () => {
    const cssPath = path.resolve(__dirname, '../index.css')
    const css = fs.readFileSync(cssPath, 'utf-8')
    expect(css).not.toContain('@media (prefers-color-scheme: dark)')
    expect(css).not.toContain('html.light')
    expect(css).toContain('html.dark .prose')
    expect(css).toContain('html.dark .hoja .prose')
  })
})

describe('siguienteTema', () => {
  it('cicla claro → oscuro → sistema → claro', async () => {
    vi.stubGlobal('localStorage', { getItem: () => null, setItem: () => {} })
    vi.stubGlobal('window', {
      matchMedia: () => ({ matches: false, addEventListener: () => {} }),
    })
    vi.stubGlobal('document', { documentElement: { classList: { add: () => {}, remove: () => {} } } })
    const { siguienteTema } = await import('./theme')
    expect(siguienteTema('light')).toBe('dark')
    expect(siguienteTema('dark')).toBe('system')
    expect(siguienteTema('system')).toBe('light')
  })
})
