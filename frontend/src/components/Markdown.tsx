import ReactMarkdown from 'react-markdown'
import rehypeKatex from 'rehype-katex'
import remarkMath from 'remark-math'
import 'katex/dist/katex.min.css'
import { cn } from '@/lib/utils'

/**
 * Markdown de lectura (explicaciones del tutor, guías, respuestas) con fórmulas LaTeX:
 * `$...$` en línea y `$$...$$` en bloque, renderizadas con KaTeX.
 */
export function Markdown({ children, className }: { children: string; className?: string }) {
  return (
    <div className={cn('prose max-w-none', className)}>
      <ReactMarkdown
        remarkPlugins={[remarkMath]}
        rehypePlugins={[[rehypeKatex, { throwOnError: false, strict: false }]]}
        components={{
          pre({ children: contenido, ...props }) {
            return (
              <pre
                className="overflow-x-auto rounded-lg border border-slate-800 bg-slate-950 p-4 font-mono text-xs text-slate-100"
                {...props}
              >
                {contenido}
              </pre>
            )
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  )
}
