export type Tema = 'light' | 'dark' | 'system'

const CLAVE_STORAGE = 'ml_theme'

export function obtenerTemaGuardado(): Tema {
  try {
    const valor = localStorage.getItem(CLAVE_STORAGE)
    if (valor === 'light' || valor === 'dark' || valor === 'system') {
      return valor
    }
  } catch {
    // localStorage no disponible
  }
  return 'system'
}

export function aplicarTema(tema: Tema): void {
  const root = document.documentElement
  const esOscuro =
    tema === 'dark' ||
    (tema === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)

  if (esOscuro) {
    root.classList.add('dark')
    root.classList.remove('light')
  } else {
    root.classList.remove('dark')
    root.classList.add('light')
  }

  try {
    localStorage.setItem(CLAVE_STORAGE, tema)
  } catch {
    // fallback
  }
}

// Inicializar inmediatamente al cargar el módulo
if (typeof window !== 'undefined') {
  aplicarTema(obtenerTemaGuardado())

  // Escuchar cambios en la preferencia del sistema operativo
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (obtenerTemaGuardado() === 'system') {
      aplicarTema('system')
    }
  })
}
