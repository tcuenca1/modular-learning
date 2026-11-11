import path from 'path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig, type Plugin } from 'vite'

/**
 * KaTeX declara cada fuente en woff2, woff y ttf. Los navegadores actuales usan siempre woff2,
 * así que se quitan las otras dos para no copiar ~40 archivos inútiles al build.
 */
function katexSoloWoff2(): Plugin {
  return {
    name: 'katex-solo-woff2',
    enforce: 'pre',
    transform(codigo, id) {
      if (!id.includes('katex') || !id.split('?')[0].endsWith('.css')) return null
      return codigo.replace(/,\s*url\([^)]*\.(?:woff|ttf)\)\s*format\("[^"]*"\)/g, '')
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [katexSoloWoff2(), react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: path.resolve(import.meta.dirname, '../backend/src/modular_learning/apps/api/static'),
    emptyOutDir: true,
  },
})
