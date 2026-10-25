import * as React from 'react'
import { cn } from '@/lib/utils'

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number
}

export const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, ...props }, ref) => {
    const validValue = Math.min(100, Math.max(0, value || 0))
    return (
      <div
        ref={ref}
        className={cn('relative h-1.5 w-full overflow-hidden rounded-sm bg-slate-200 dark:bg-slate-800', className)}
        {...props}
      >
        <div
          className="h-full bg-indigo-600 transition-all duration-500 dark:bg-indigo-400"
          style={{ width: `${validValue}%` }}
        />
      </div>
    )
  }
)
Progress.displayName = 'Progress'
