import React, { forwardRef } from 'react';
import { motion } from 'framer-motion';
import { cn } from '../../utils/cn';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  variant?: 'default' | 'filled' | 'outlined';
  inputSize?: 'sm' | 'md' | 'lg';
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      variant = 'default',
      inputSize = 'md',
      className,
      id,
      ...props
    },
    ref
  ) => {
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;

    const baseClasses = [
      'block w-full rounded-lg transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-offset-1',
      'disabled:opacity-50 disabled:cursor-not-allowed',
    ];

    const variantClasses = {
      default: [
        'border border-neutral-300 bg-white',
        'focus:border-primary-500 focus:ring-primary-500',
        'hover:border-neutral-400',
      ],
      filled: [
        'border-0 bg-neutral-100',
        'focus:bg-white focus:ring-primary-500',
        'hover:bg-neutral-50',
      ],
      outlined: [
        'border-2 border-neutral-300 bg-transparent',
        'focus:border-primary-500 focus:ring-primary-500',
        'hover:border-neutral-400',
      ],
    };

    const sizeClasses = {
      sm: leftIcon || rightIcon ? 'py-2 pl-10 pr-4 text-sm' : 'py-2 px-3 text-sm',
      md: leftIcon || rightIcon ? 'py-2.5 pl-10 pr-4 text-base' : 'py-2.5 px-3 text-base',
      lg: leftIcon || rightIcon ? 'py-3 pl-12 pr-4 text-lg' : 'py-3 px-4 text-lg',
    };

    const iconSizeClasses = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-6 h-6',
    };

    const iconPositionClasses = {
      sm: 'left-3',
      md: 'left-3',
      lg: 'left-4',
    };

    const inputClasses = cn(
      baseClasses,
      variantClasses[variant],
      sizeClasses[inputSize],
      error && 'border-accent-500 focus:border-accent-500 focus:ring-accent-500',
      className
    );

    return (
      <div className="w-full">
        {label && (
          <motion.label
            htmlFor={inputId}
            className="block text-sm font-medium text-neutral-700 mb-2"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {label}
          </motion.label>
        )}
        
        <div className="relative">
          {leftIcon && (
            <div
              className={cn(
                'absolute inset-y-0 flex items-center pointer-events-none text-neutral-400',
                iconPositionClasses[inputSize]
              )}
            >
              <span className={iconSizeClasses[inputSize]}>{leftIcon}</span>
            </div>
          )}
          
          <motion.input
            ref={ref}
            id={inputId}
            className={inputClasses}
            whileFocus={{ scale: 1.01 }}
            transition={{ type: 'spring' as const, stiffness: 300, damping: 30 }}
            {...(props as any)}
          />
          
          {rightIcon && (
            <div
              className={cn(
                'absolute inset-y-0 right-0 flex items-center pr-3 text-neutral-400',
                props.onClick && 'cursor-pointer hover:text-neutral-600'
              )}
              onClick={props.onClick}
            >
              <span className={iconSizeClasses[inputSize]}>{rightIcon}</span>
            </div>
          )}
        </div>
        
        {(error || helperText) && (
          <motion.div
            className="mt-2"
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {error && (
              <p className="text-sm text-accent-600 flex items-center">
                <svg
                  className="w-4 h-4 mr-1"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                    clipRule="evenodd"
                  />
                </svg>
                {error}
              </p>
            )}
            
            {!error && helperText && (
              <p className="text-sm text-neutral-500">{helperText}</p>
            )}
          </motion.div>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
