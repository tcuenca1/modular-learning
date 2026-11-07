import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Download, Printer } from 'lucide-react'
import { api } from '@/api/client'
import type { Guia } from '@/api/types'
import { Markdown } from '@/components/Markdown'
import { formatoCorto, parsearFecha } from '@/lib/asignaturas'
import { NOMBRE_EXTENSION } from '@/lib/guias'

const formatoLargo = new Intl.DateTimeFormat('es', { day: 'numeric', month: 'long', year: 'numeric' })

function fechaCorta(valor: string): string {
  const f = parsearFecha(valor)
  return f ? formatoCorto.format(f) : ''
}

/**
 * Guía lista para imprimir o guardar como PDF desde el navegador: A5 (cómodo en el móvil),
 * siempre en claro aunque el sistema esté en modo oscuro, una clase por página.
 */
export function GuiaImprimirView() {
  const { id = '' } = useParams()
  const [guia, setGuia] = useState<Guia | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    api
      .getGuia(id)
      .then(setGuia)
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
  }, [id])

  // El título es el nombre de archivo que propone el diálogo de "Guardar como PDF"
  useEffect(() => {
    if (!guia) return
    const anterior = document.title
    const fecha = new Date().toISOString().slice(0, 10)
    document.title = `Guia ${guia.materia} ${fecha}`
    return () => {
      document.title = anterior
    }
  }, [guia])

  if (error || (guia && !guia.completa)) {
    return (
      <div className="hoja-fondo flex min-h-screen items-center justify-center p-4">
        <div className="max-w-md space-y-3 rounded-lg bg-white p-6 text-slate-800">
          <p>{error ?? 'Esta guía todavía no está generada por completo.'}</p>
          <Link to="/guia" className="text-indigo-700 underline underline-offset-4">
            Volver a Guía offline
          </Link>
        </div>
      </div>
    )
  }

  if (!guia) {
    return <div className="hoja-fondo min-h-screen" />
  }

  const creada = parsearFecha(guia.creada)
  const conRespuestas = guia.clases.some((c) => c.respuestas)

  return (
    <div className="hoja-fondo min-h-screen">
      <div className="no-imprimir sticky top-0 z-10 border-b border-slate-300 bg-slate-100/95 backdrop-blur">
        <div className="mx-auto flex max-w-[148mm] flex-wrap items-center justify-between gap-3 px-4 py-3">
          <Link to="/guia" className="inline-flex items-center gap-1.5 text-sm text-slate-700 hover:text-slate-950">
            <ArrowLeft className="h-4 w-4" /> Guía offline
          </Link>
          <div className="flex items-center gap-2">
            <a
              href={`/api/guias/${guia.id}/pdf`}
              download
              className="inline-flex cursor-pointer items-center gap-2 rounded-md bg-indigo-700 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-800"
            >
              <Download className="h-4 w-4" /> Descargar PDF directo
            </a>
            <button
              type="button"
              onClick={() => window.print()}
              className="inline-flex cursor-pointer items-center gap-2 rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            >
              <Printer className="h-4 w-4" /> Imprimir
            </button>
          </div>
          <p className="w-full text-xs text-slate-600">
            Puedes descargar el PDF vectorial directamente o usar «Imprimir» para ajustar márgenes según tu dispositivo.
          </p>
        </div>
      </div>

      <article className="hoja mx-auto max-w-[148mm] px-4 py-6 sm:py-10">
        {/* Portada */}
        <section className="pagina">
          <p className="cifra text-xs text-slate-500">Modular Learning · guía offline</p>
          <h1 className="mt-6 text-[2rem] leading-tight text-slate-950">{guia.materia}</h1>
          <p className="mt-2 text-sm text-slate-600">
            {guia.clases.length === 1 ? '1 clase' : `${guia.clases.length} clases`} · versión{' '}
            {NOMBRE_EXTENSION[guia.extension]}
            {creada && ` · ${formatoLargo.format(creada)}`}
          </p>

          <ol className="mt-8 space-y-2 border-t border-slate-200 pt-6">
            {guia.clases.map((c, i) => (
              <li key={c.tema} className="grid grid-cols-[1.5rem_minmax(0,1fr)_auto] gap-2 text-sm">
                <span className="cifra text-slate-500">{i + 1}</span>
                <span className="text-slate-900">{c.tema}</span>
                <span className="cifra text-xs text-slate-500">{fechaCorta(c.fecha)}</span>
              </li>
            ))}
          </ol>

          <div className="mt-10 space-y-2 text-sm text-slate-700">
            <p className="font-display italic text-slate-500">Cómo usarla</p>
            <ol className="list-decimal space-y-1 pl-5">
              <li>Lee cada clase en orden y responde su autoevaluación sin mirar las respuestas.</li>
              <li>Apunta en el teléfono lo que no te quede claro.</li>
              <li>Comprueba tus respuestas al final del documento.</li>
              <li>Al volver, abre Modular Learning y confirma qué clases entendiste.</li>
            </ol>
          </div>
        </section>

        {guia.clases.map((c, i) => (
          <section key={c.tema} className="pagina salto">
            <p className="cifra text-xs text-slate-500">
              Clase {i + 1} de {guia.clases.length}
              {fechaCorta(c.fecha) && ` · ${fechaCorta(c.fecha)}`}
            </p>
            <h1 className="mt-2 mb-6 text-2xl leading-tight text-slate-950">{c.tema}</h1>
            <Markdown>{c.contenido}</Markdown>
          </section>
        ))}

        {conRespuestas && (
          <section className="pagina salto">
            <h1 className="mb-6 text-2xl text-slate-950">Respuestas</h1>
            <div className="space-y-8">
              {guia.clases.map(
                (c, i) =>
                  c.respuestas && (
                    <div key={c.tema}>
                      <h2 className="mb-2 text-lg text-slate-950">
                        {i + 1}. {c.tema}
                      </h2>
                      <Markdown>{c.respuestas}</Markdown>
                    </div>
                  )
              )}
            </div>
          </section>
        )}
      </article>
    </div>
  )
}
