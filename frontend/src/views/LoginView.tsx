import { useId, useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Eye, EyeOff } from 'lucide-react'
import { api } from '@/api/client'
import type { Usuario } from '@/api/types'
import { ThemeToggle } from '@/components/ThemeToggle'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { validarLogin } from '@/lib/auth'

interface LoginViewProps {
  alAcceder: (usuario: Usuario) => void
}

export function LoginView({ alAcceder }: LoginViewProps) {
  const id = useId()
  const idCorreo = `${id}-correo`
  const idContrasena = `${id}-contrasena`
  const idError = `${id}-error`
  const [correo, setCorreo] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [verContrasena, setVerContrasena] = useState(false)
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)
  const refCorreo = useRef<HTMLInputElement>(null)
  const refContrasena = useRef<HTMLInputElement>(null)

  const enviar = async (e: FormEvent) => {
    e.preventDefault()
    if (enviando) return
    const invalido = validarLogin(correo, contrasena)
    if (invalido) {
      setError(invalido)
      ;(correo.trim() ? refContrasena : refCorreo).current?.focus()
      return
    }
    setError('')
    setEnviando(true)
    try {
      const { usuario } = await api.login({ correo: correo.trim(), contrasena })
      alAcceder(usuario)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No pude iniciar sesión. Inténtalo de nuevo.')
      setContrasena('')
      refContrasena.current?.focus()
      setEnviando(false)
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-slate-50 px-4 text-slate-900 antialiased dark:bg-slate-950 dark:text-slate-100">
      <div className="flex justify-end pt-3">
        <ThemeToggle compacto />
      </div>
      <main className="mx-auto flex w-full max-w-sm flex-1 flex-col justify-center pb-16">
        <div className="mb-8 flex items-center gap-3">
          <img src="/favicon.svg" alt="" className="h-10 w-10 shrink-0" />
          <div className="leading-tight">
            <h1 className="font-display text-2xl font-semibold text-slate-900 dark:text-slate-50">
              Modular Learning
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-400">Inicia sesión para continuar</p>
          </div>
        </div>

        <form
          onSubmit={enviar}
          noValidate
          aria-busy={enviando}
          className="space-y-4 rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"
        >
          <div className="space-y-1.5">
            <label htmlFor={idCorreo} className="text-sm font-medium text-slate-800 dark:text-slate-200">
              Correo o usuario
            </label>
            <Input
              ref={refCorreo}
              id={idCorreo}
              type="text"
              name="correo"
              autoComplete="username"
              inputMode="email"
              autoCapitalize="none"
              autoCorrect="off"
              spellCheck={false}
              autoFocus
              required
              value={correo}
              onChange={(e) => setCorreo(e.target.value)}
              aria-describedby={error ? idError : undefined}
              className="h-11 text-base"
            />
          </div>

          <div className="space-y-1.5">
            <label
              htmlFor={idContrasena}
              className="text-sm font-medium text-slate-800 dark:text-slate-200"
            >
              Contraseña
            </label>
            <div className="relative">
              <Input
                ref={refContrasena}
                id={idContrasena}
                type={verContrasena ? 'text' : 'password'}
                name="contrasena"
                autoComplete="current-password"
                required
                value={contrasena}
                onChange={(e) => setContrasena(e.target.value)}
                aria-describedby={error ? idError : undefined}
                className="h-11 pr-12 text-base"
              />
              <button
                type="button"
                onClick={() => setVerContrasena((v) => !v)}
                aria-pressed={verContrasena}
                aria-label="Mostrar contraseña"
                className="absolute inset-y-0 right-0 flex w-11 cursor-pointer items-center justify-center rounded-md text-slate-600 hover:text-slate-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 dark:text-slate-400 dark:hover:text-slate-100"
              >
                {verContrasena ? (
                  <EyeOff className="h-4 w-4" aria-hidden />
                ) : (
                  <Eye className="h-4 w-4" aria-hidden />
                )}
              </button>
            </div>
          </div>

          <div id={idError} role="alert" className="min-h-0">
            {error && (
              <p className="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-800 dark:bg-rose-950/50 dark:text-rose-200">
                {error}
              </p>
            )}
          </div>

          <Button type="submit" size="lg" className="h-11 w-full" disabled={enviando}>
            {enviando ? 'Entrando…' : 'Entrar'}
          </Button>
        </form>
      </main>
    </div>
  )
}
