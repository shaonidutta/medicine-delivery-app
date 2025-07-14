import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CheckCircleIcon, 
  ExclamationCircleIcon, 
  ExclamationTriangleIcon, 
  InformationCircleIcon,
  XMarkIcon 
} from '@heroicons/react/24/outline';
import { useUIStore } from '../../stores/uiStore';

const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useUIStore();

  const getToastIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircleIcon className="w-5 h-5 text-secondary-600" />;
      case 'error':
        return <ExclamationCircleIcon className="w-5 h-5 text-accent-600" />;
      case 'warning':
        return <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600" />;
      case 'info':
      default:
        return <InformationCircleIcon className="w-5 h-5 text-primary-600" />;
    }
  };

  const getToastStyles = (type: string) => {
    switch (type) {
      case 'success':
        return 'bg-secondary-50 border-secondary-200';
      case 'error':
        return 'bg-accent-50 border-accent-200';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200';
      case 'info':
      default:
        return 'bg-primary-50 border-primary-200';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2 max-w-sm w-full">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, x: 300, scale: 0.3 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 300, scale: 0.5 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className={`
              p-4 rounded-lg border shadow-soft-lg backdrop-blur-sm
              ${getToastStyles(toast.type)}
            `}
          >
            <div className="flex items-start">
              <div className="flex-shrink-0">
                {getToastIcon(toast.type)}
              </div>
              
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-neutral-900">
                  {toast.title}
                </p>
                {toast.message && (
                  <p className="mt-1 text-sm text-neutral-600">
                    {toast.message}
                  </p>
                )}
              </div>
              
              <div className="ml-4 flex-shrink-0">
                <button
                  onClick={() => removeToast(toast.id)}
                  className="inline-flex text-neutral-400 hover:text-neutral-600 transition-colors"
                >
                  <span className="sr-only">Close</span>
                  <XMarkIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default ToastContainer;
