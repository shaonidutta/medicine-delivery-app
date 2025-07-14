import React, { forwardRef } from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import { cn } from '../../utils/cn';

interface ButtonProps extends Omit<HTMLMotionProps<'button'>, 'size'> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  children: React.ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseClasses = [
      'inline-flex items-center justify-center font-medium rounded-lg',
      'transition-all duration-200 ease-smooth',
      'focus:outline-none focus:ring-2 focus:ring-offset-2',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      'transform hover:scale-105 active:scale-95',
    ];

    const variantClasses = {
      primary: [
        'bg-primary-600 text-white shadow-soft',
        'hover:bg-primary-700 hover:shadow-soft-lg hover:shadow-glow',
        'focus:ring-primary-500',
        'active:bg-primary-800',
      ],
      secondary: [
        'bg-secondary-600 text-white shadow-soft',
        'hover:bg-secondary-700 hover:shadow-soft-lg hover:shadow-glow-green',
        'focus:ring-secondary-500',
        'active:bg-secondary-800',
      ],
      outline: [
        'border border-neutral-300 bg-white text-neutral-700 shadow-soft',
        'hover:bg-neutral-50 hover:border-neutral-400 hover:shadow-soft-lg',
        'focus:ring-primary-500',
        'active:bg-neutral-100',
      ],
      ghost: [
        'text-neutral-600 bg-transparent',
        'hover:bg-neutral-100 hover:text-neutral-900',
        'focus:ring-primary-500',
        'active:bg-neutral-200',
      ],
      danger: [
        'bg-accent-600 text-white shadow-soft',
        'hover:bg-accent-700 hover:shadow-soft-lg hover:shadow-glow-red',
        'focus:ring-accent-500',
        'active:bg-accent-800',
      ],
    };

    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-sm',
      lg: 'px-6 py-3 text-base',
      xl: 'px-8 py-4 text-lg',
    };

    const iconSizeClasses = {
      sm: 'w-4 h-4',
      md: 'w-4 h-4',
      lg: 'w-5 h-5',
      xl: 'w-6 h-6',
    };

    const classes = cn(
      baseClasses,
      variantClasses[variant],
      sizeClasses[size],
      fullWidth && 'w-full',
      className
    );

    const iconSize = iconSizeClasses[size];

    return (
      <motion.button
        ref={ref}
        className={classes}
        disabled={disabled || loading}
        whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
        whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
        transition={{ type: 'spring', stiffness: 400, damping: 17 }}
        {...props}
      >
        {loading && (
          <svg
            className={cn('animate-spin mr-2', iconSize)}
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        
        {!loading && leftIcon && (
          <span className={cn('mr-2', iconSize)}>{leftIcon}</span>
        )}
        
        <span>{children}</span>
        
        {!loading && rightIcon && (
          <span className={cn('ml-2', iconSize)}>{rightIcon}</span>
        )}
      </motion.button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
