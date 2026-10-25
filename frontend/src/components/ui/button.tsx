import * as React from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    const baseStyles =
      'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 focus-visible:ring-offset-1 focus-visible:ring-offset-slate-50 dark:focus-visible:ring-offset-slate-950 disabled:pointer-events-none disabled:opacity-50 cursor-pointer'

    const variants = {
      default: 'bg-indigo-700 text-white hover:bg-indigo-800 dark:bg-indigo-400 dark:text-slate-950 dark:hover:bg-indigo-300',
      destructive: 'bg-red-600 text-white shadow-sm hover:bg-red-500',
      outline: 'border border-slate-300 bg-transparent hover:bg-slate-100 hover:text-slate-900 dark:border-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-50',
      secondary: 'bg-slate-100 text-slate-900 shadow-sm hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-50 dark:hover:bg-slate-700',
      ghost: 'hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-slate-50',
      link: 'text-indigo-700 underline decoration-indigo-300 underline-offset-4 hover:decoration-indigo-700 dark:text-indigo-300 dark:decoration-indigo-700',
    }

    const sizes = {
      default: 'h-9 px-4 py-2',
      sm: 'h-8 rounded-md px-3 text-xs',
      lg: 'h-10 rounded-md px-8',
      icon: 'h-9 w-9',
    }

    return (
      <button
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = 'Button'
