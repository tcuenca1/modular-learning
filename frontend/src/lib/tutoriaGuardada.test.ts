import { beforeEach, describe, expect, it, vi } from 'vitest'
import type { SesionTutoriaResponse } from '@/api/types'
import {
  borrarTutoriaGuardada,
  guardarTutoria,
  leerTutoriaGuardada,
  type TutoriaGuardada,
} from './tutoriaGuardada'

const sesion = {
  sesion_id: 's1',
  materia: 'Redes',
  tema: 'ARP',
  pasos: [
    { titulo: 'A', descripcion: 'a' },
    { titulo: 'B', descripcion: 'b' },
  ],
} as unknown as SesionTutoriaResponse

const estado: TutoriaGuardada = {
  origen: '|ARP|',
  sesion,
  pasoActual: 1,
  explicaciones: { 0: 'Texto', 1: 'Par' },
  completados: [0],
  dudas: { 0: [{ duda: '¿Qué?', respuesta: 'Eso' }] },
}

describe('tutoriaGuardada', () => {
  let almacen: Record<string, string>

  beforeEach(() => {
    almacen = {}
    vi.stubGlobal('window', {
      sessionStorage: {
        getItem: (k: string) => almacen[k] ?? null,
        setItem: (k: string, v: string) => {
          almacen[k] = v
        },
        removeItem: (k: string) => {
          delete almacen[k]
        },
      },
    })
  })

  it('guarda y recupera la tutoría con el mismo destino', () => {
    guardarTutoria(estado)
    expect(leerTutoriaGuardada('|ARP|')).toEqual(estado)
  })

  it('no la devuelve si se abre con otro destino', () => {
    guardarTutoria(estado)
    expect(leerTutoriaGuardada('|OTRO|')).toBeNull()
  })

  it('borrar la elimina', () => {
    guardarTutoria(estado)
    borrarTutoriaGuardada()
    expect(leerTutoriaGuardada('|ARP|')).toBeNull()
  })

  it('ignora contenido corrupto o sin pasos', () => {
    almacen['ml.tutoria.v1'] = '{no es json'
    expect(leerTutoriaGuardada('|ARP|')).toBeNull()
    almacen['ml.tutoria.v1'] = JSON.stringify({
      origen: '|ARP|',
      sesion: { sesion_id: 's', pasos: [] },
    })
    expect(leerTutoriaGuardada('|ARP|')).toBeNull()
  })

  it('acota el paso actual a los pasos existentes', () => {
    guardarTutoria({ ...estado, pasoActual: 99 })
    expect(leerTutoriaGuardada('|ARP|')?.pasoActual).toBe(1)
  })
})
