import { useCallback, useEffect, useId, useState } from 'react'
import type { FormEvent } from 'react'
import { toast } from 'sonner'
import { api } from '@/api/client'
import type { UsuarioAdmin } from '@/api/types'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { useSesion } from '@/hooks/useSesion'
import {
  LONGITUD_MINIMA_CONTRASENA,
  validarCambioContrasena,
  validarContrasenaNueva,
  validarNuevoUsuario,
} from '@/lib/auth'

function mensaje(err: unknown): string {
  return err instanceof Error ? err.message : String(err)
}

interface CampoProps {
  etiqueta: string
  type?: string
  value: string
  onChange: (v: string) => void
  autoComplete?: string
  ayuda?: string
}

function Campo({ etiqueta, type = 'text', value, onChange, autoComplete, ayuda }: CampoProps) {
  const id = useId()
  const idAyuda = `${id}-ayuda`
  return (
    <div className="space-y-1.5">
      <label htmlFor={id} className="text-sm font-medium text-slate-800 dark:text-slate-200">
        {etiqueta}
      </label>
      <Input
        id={id}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        autoComplete={autoComplete}
        aria-describedby={ayuda ? idAyuda : undefined}
        spellCheck={false}
      />
      {ayuda && (
        <p id={idAyuda} className="text-xs text-slate-600 dark:text-slate-400">
          {ayuda}
        </p>
      )}
    </div>
  )
}

function AvisoError({ texto }: { texto: string }) {
  return (
    <div role="alert">
      {texto && (
        <p className="rounded-md bg-rose-50 px-3 py-2 text-sm text-rose-800 dark:bg-rose-950/50 dark:text-rose-200">
          {texto}
        </p>
      )}
    </div>
  )
}

function CambiarContrasena() {
  const [actual, setActual] = useState('')
  const [nueva, setNueva] = useState('')
  const [confirmacion, setConfirmacion] = useState('')
  const [error, setError] = useState('')
  const [enviando, setEnviando] = useState(false)

  const enviar = async (e: FormEvent) => {
    e.preventDefault()
    const invalido = validarCambioContrasena(actual, nueva, confirmacion)
    if (invalido) {
      setError(invalido)
      return
    }
    setError('')
    setEnviando(true)
    try {
      await api.cambiarContrasena({ actual, nueva })
      setActual('')
      setNueva('')
      setConfirmacion('')
      toast.success('Contraseña actualizada')
    } catch (err) {
      setError(mensaje(err))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Cambiar contraseña</CardTitle>
        <CardDescription>Usa al menos {LONGITUD_MINIMA_CONTRASENA} caracteres.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={enviar} noValidate className="max-w-sm space-y-4">
          <Campo
            etiqueta="Contraseña actual"
            type="password"
            value={actual}
            onChange={setActual}
            autoComplete="current-password"
          />
          <Campo
            etiqueta="Nueva contraseña"
            type="password"
            value={nueva}
            onChange={setNueva}
            autoComplete="new-password"
          />
          <Campo
            etiqueta="Confirmar nueva contraseña"
            type="password"
            value={confirmacion}
            onChange={setConfirmacion}
            autoComplete="new-password"
          />
          <AvisoError texto={error} />
          <Button type="submit" disabled={enviando}>
            {enviando ? 'Guardando…' : 'Cambiar contraseña'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}

function FilaUsuario({
  usuario,
  esYo,
  alCambiar,
}: {
  usuario: UsuarioAdmin
  esYo: boolean
  alCambiar: (u: UsuarioAdmin) => void
}) {
  const [restableciendo, setRestableciendo] = useState(false)
  const [nueva, setNueva] = useState('')
  const [error, setError] = useState('')
  const [ocupado, setOcupado] = useState(false)

  const actualizar = async (datos: { activo?: boolean; contrasena?: string }) => {
    setOcupado(true)
    try {
      const { usuario: u } = await api.actualizarUsuario(usuario.id, datos)
      alCambiar(u)
      return true
    } catch (err) {
      setError(mensaje(err))
      return false
    } finally {
      setOcupado(false)
    }
  }

  const restablecer = async (e: FormEvent) => {
    e.preventDefault()
    const invalido = validarContrasenaNueva(nueva)
    if (invalido) {
      setError(invalido)
      return
    }
    setError('')
    if (await actualizar({ contrasena: nueva })) {
      setNueva('')
      setRestableciendo(false)
      toast.success(`Contraseña restablecida para ${usuario.correo}`)
    }
  }

  return (
    <li className="space-y-3 py-4">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-slate-900 dark:text-white">
            {usuario.nombre}
          </p>
          <p className="truncate text-sm text-slate-600 dark:text-slate-400">{usuario.correo}</p>
        </div>
        <div className="flex items-center gap-2">
          {usuario.es_admin && <Badge variant="secondary">Admin</Badge>}
          <Badge variant={usuario.activo ? 'success' : 'outline'}>
            {usuario.activo ? 'Activo' : 'Inactivo'}
          </Badge>
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          className="toque"
          disabled={ocupado || esYo}
          title={esYo ? 'No puedes desactivar tu propia cuenta' : undefined}
          onClick={() => {
            setError('')
            void actualizar({ activo: !usuario.activo })
          }}
        >
          {usuario.activo ? 'Desactivar' : 'Activar'}
          <span className="sr-only"> a {usuario.correo}</span>
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          className="toque"
          aria-expanded={restableciendo}
          onClick={() => {
            setError('')
            setRestableciendo((v) => !v)
          }}
        >
          Restablecer contraseña
          <span className="sr-only"> de {usuario.correo}</span>
        </Button>
      </div>
      {restableciendo && (
        <form onSubmit={restablecer} noValidate className="max-w-sm space-y-3">
          <Campo
            etiqueta={`Nueva contraseña para ${usuario.correo}`}
            type="password"
            value={nueva}
            onChange={setNueva}
            autoComplete="new-password"
          />
          <div className="flex gap-2">
            <Button type="submit" size="sm" className="toque" disabled={ocupado}>
              Guardar
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="toque"
              onClick={() => setRestableciendo(false)}
            >
              Cancelar
            </Button>
          </div>
        </form>
      )}
      <AvisoError texto={error} />
    </li>
  )
}

function Usuarios() {
  const { usuario: yo } = useSesion()
  const [usuarios, setUsuarios] = useState<UsuarioAdmin[] | null>(null)
  const [errorCarga, setErrorCarga] = useState('')
  const [correo, setCorreo] = useState('')
  const [nombre, setNombre] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [errorAlta, setErrorAlta] = useState('')
  const [creando, setCreando] = useState(false)

  const cargar = useCallback(() => {
    api
      .getUsuarios()
      .then((r) => setUsuarios(r.usuarios))
      .catch((err) => setErrorCarga(mensaje(err)))
  }, [])

  useEffect(() => {
    cargar()
  }, [cargar])

  const crear = async (e: FormEvent) => {
    e.preventDefault()
    const invalido = validarNuevoUsuario(correo, nombre, contrasena)
    if (invalido) {
      setErrorAlta(invalido)
      return
    }
    setErrorAlta('')
    setCreando(true)
    try {
      const { usuario } = await api.crearUsuario({
        correo: correo.trim(),
        nombre: nombre.trim(),
        contrasena,
      })
      setUsuarios((lista) => [...(lista ?? []), usuario])
      setCorreo('')
      setNombre('')
      setContrasena('')
      toast.success(`Usuario ${usuario.correo} creado`)
    } catch (err) {
      setErrorAlta(mensaje(err))
    } finally {
      setCreando(false)
    }
  }

  const reemplazar = (u: UsuarioAdmin) =>
    setUsuarios((lista) => (lista ?? []).map((x) => (x.id === u.id ? u : x)))

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Usuarios</CardTitle>
          <CardDescription>Cuentas con acceso a esta instalación.</CardDescription>
        </CardHeader>
        <CardContent>
          {errorCarga && <AvisoError texto={errorCarga} />}
          {!errorCarga && usuarios === null && (
            <p role="status" className="text-sm text-slate-600 dark:text-slate-400">
              Cargando usuarios…
            </p>
          )}
          {usuarios && (
            <ul className="divide-y divide-slate-200 dark:divide-slate-800">
              {usuarios.map((u) => (
                <FilaUsuario key={u.id} usuario={u} esYo={u.id === yo?.id} alCambiar={reemplazar} />
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Crear usuario</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={crear} noValidate className="max-w-sm space-y-4">
            <Campo etiqueta="Nombre" value={nombre} onChange={setNombre} autoComplete="off" />
            <Campo
              etiqueta="Correo"
              type="email"
              value={correo}
              onChange={setCorreo}
              autoComplete="off"
            />
            <Campo
              etiqueta="Contraseña inicial"
              type="password"
              value={contrasena}
              onChange={setContrasena}
              autoComplete="new-password"
              ayuda={`Al menos ${LONGITUD_MINIMA_CONTRASENA} caracteres.`}
            />
            <AvisoError texto={errorAlta} />
            <Button type="submit" disabled={creando}>
              {creando ? 'Creando…' : 'Crear usuario'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </>
  )
}

export function CuentaView() {
  const { usuario } = useSesion()
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-white">Cuenta</h1>
        {usuario && (
          <p className="mt-1 text-sm text-slate-600 dark:text-slate-400">
            {usuario.nombre} · {usuario.correo}
          </p>
        )}
      </header>
      <CambiarContrasena />
      {usuario?.es_admin && <Usuarios />}
    </div>
  )
}
