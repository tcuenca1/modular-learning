import { cn } from '@/lib/utils'

/** Aviso breve dentro de un botón que llama a la IA (consume cuota y tarda unos segundos). */
export function AvisoIA({ className }: { className?: string }) {
  return <span className={cn('text-[11px] font-normal', className)}>· usa IA</span>
}
