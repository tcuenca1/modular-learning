import { useCallback, useEffect, useRef, useState } from 'react'

export interface UseEventStreamOptions<T = unknown> {
  url: string
  method?: 'GET' | 'POST'
  body?: unknown
  headers?: Record<string, string>
  onMessage?: (data: T) => void
  onError?: (error: Error) => void
  onEnd?: () => void
}

export interface UseEventStreamReturn<T = unknown> {
  isStreaming: boolean
  events: T[]
  latestEvent: T | null
  error: Error | null
  startStream: (overrideBody?: unknown) => Promise<void>
  stopStream: () => void
  clearEvents: () => void
}

export function useEventStream<T = unknown>({
  url,
  method = 'GET',
  body,
  headers = {},
  onMessage,
  onError,
  onEnd,
}: UseEventStreamOptions<T>): UseEventStreamReturn<T> {
  const [isStreaming, setIsStreaming] = useState(false)
  const [events, setEvents] = useState<T[]>([])
  const [latestEvent, setLatestEvent] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)

  const abortControllerRef = useRef<AbortController | null>(null)
  const eventSourceRef = useRef<EventSource | null>(null)
  const isMountedRef = useRef(true)

  const stopStream = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
    if (isMountedRef.current) {
      setIsStreaming(false)
    }
  }, [])

  const clearEvents = useCallback(() => {
    setEvents([])
    setLatestEvent(null)
    setError(null)
  }, [])

  const startStream = useCallback(
    async (overrideBody?: unknown) => {
      stopStream()
      setIsStreaming(true)
      setError(null)

      if (method === 'GET') {
        try {
          const es = new EventSource(url)
          eventSourceRef.current = es

          es.onmessage = (event) => {
            if (!isMountedRef.current) return
            try {
              const parsed = JSON.parse(event.data) as T
              setEvents((prev) => [...prev, parsed])
              setLatestEvent(parsed)
              onMessage?.(parsed)
            } catch {
              // Si no es JSON puro
              const raw = event.data as unknown as T
              setEvents((prev) => [...prev, raw])
              setLatestEvent(raw)
              onMessage?.(raw)
            }
          }

          es.addEventListener('fin', () => {
            stopStream()
            onEnd?.()
          })

          es.addEventListener('error', (e) => {
            // El backend puede enviar event: error con JSON
            const customEvent = e as MessageEvent
            let err: Error
            if (customEvent.data) {
              try {
                const parsed = JSON.parse(customEvent.data)
                err = new Error(parsed.error || 'Error en el stream')
              } catch {
                err = new Error(customEvent.data)
              }
            } else {
              err = new Error('Conexión con el servidor interrumpida')
            }

            if (isMountedRef.current) {
              setError(err)
              onError?.(err)
            }
            stopStream()
          })
        } catch (err) {
          const streamErr = err instanceof Error ? err : new Error(String(err))
          if (isMountedRef.current) {
            setError(streamErr)
            onError?.(streamErr)
            setIsStreaming(false)
          }
        }
      } else {
        // Modo POST mediante fetch + ReadableStream
        const controller = new AbortController()
        abortControllerRef.current = controller

        try {
          const payload = overrideBody !== undefined ? overrideBody : body
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              ...headers,
            },
            body: payload ? JSON.stringify(payload) : undefined,
            signal: controller.signal,
          })

          if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`)
          }

          if (!response.body) {
            throw new Error('El servidor no devolvió un cuerpo legible (ReadableStream).')
          }

          const reader = response.body.getReader()
          const decoder = new TextDecoder('utf-8')
          let buffer = ''

          while (true) {
            const { done, value } = await reader.read()
            if (done) break

            buffer += decoder.decode(value, { stream: true })
            const lines = buffer.split('\n')
            // El último elemento puede ser una línea incompleta
            buffer = lines.pop() || ''

            for (let i = 0; i < lines.length; i++) {
              const line = lines[i].trim()
              if (!line) continue

              if (line.startsWith('event: fin')) {
                stopStream()
                onEnd?.()
                return
              }

              if (line.startsWith('data: ')) {
                const jsonStr = line.slice(6)
                if (jsonStr === '{}') continue
                try {
                  const parsed = JSON.parse(jsonStr) as T
                  if (isMountedRef.current) {
                    setEvents((prev) => [...prev, parsed])
                    setLatestEvent(parsed)
                    onMessage?.(parsed)
                  }
                } catch {
                  const raw = jsonStr as unknown as T
                  if (isMountedRef.current) {
                    setEvents((prev) => [...prev, raw])
                    setLatestEvent(raw)
                    onMessage?.(raw)
                  }
                }
              }
            }
          }

          if (isMountedRef.current) {
            setIsStreaming(false)
            onEnd?.()
          }
        } catch (err: unknown) {
          if ((err as Error)?.name === 'AbortError') {
            // Cancelación intencionada
            return
          }
          const streamErr = err instanceof Error ? err : new Error(String(err))
          if (isMountedRef.current) {
            setError(streamErr)
            onError?.(streamErr)
            setIsStreaming(false)
          }
        }
      }
    },
    [url, method, body, headers, onMessage, onError, onEnd, stopStream]
  )

  useEffect(() => {
    isMountedRef.current = true
    return () => {
      isMountedRef.current = false
      stopStream()
    }
  }, [stopStream])

  return {
    isStreaming,
    events,
    latestEvent,
    error,
    startStream,
    stopStream,
    clearEvents,
  }
}
