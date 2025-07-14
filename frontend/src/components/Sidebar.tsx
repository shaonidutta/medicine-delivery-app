import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon,
  MagnifyingGlassIcon,
  DocumentTextIcon,
  ShoppingCartIcon,
  ClipboardDocumentListIcon,
  UserIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline';
import { useUIStore } from '../stores/uiStore';
import { cn } from '../utils/cn';

const Sidebar: React.FC = () => {
  const { sidebarOpen, toggleSidebar } = useUIStore();
  const location = useLocation();

  const navigation = [
    { name: 'Home', href: '/', icon: HomeIcon },
    { name: 'Browse Medicines', href: '/medicines', icon: MagnifyingGlassIcon },
    { name: 'Prescriptions', href: '/prescriptions', icon: DocumentTextIcon },
    { name: 'Cart', href: '/cart', icon: ShoppingCartIcon },
    { name: 'Orders', href: '/orders', icon: ClipboardDocumentListIcon },
    { name: 'Profile', href: '/profile', icon: UserIcon },
    { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
  ];

  const sidebarVariants = {
    open: {
      x: 0,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30,
      },
    },
    closed: {
      x: '-100%',
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30,
      },
    },
  };

  return (
    <AnimatePresence>
      {sidebarOpen && (
        <motion.aside
          className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-soft-lg border-r border-neutral-200 lg:relative lg:translate-x-0"
          variants={sidebarVariants}
          initial="closed"
          animate="open"
          exit="closed"
        >
          <div className="flex flex-col h-full">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-neutral-200">
              <h2 className="text-lg font-semibold text-neutral-900">Menu</h2>
              <button
                onClick={toggleSidebar}
                className="lg:hidden p-1 rounded-lg hover:bg-neutral-100 transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-2">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    onClick={() => {
                      // Close sidebar on mobile after navigation
                      if (window.innerWidth < 1024) {
                        toggleSidebar();
                      }
                    }}
                    className={cn(
                      'flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                      'hover:bg-neutral-100 hover:scale-105 transform',
                      isActive
                        ? 'bg-primary-100 text-primary-700 shadow-soft'
                        : 'text-neutral-600 hover:text-neutral-900'
                    )}
                  >
                    <item.icon
                      className={cn(
                        'mr-3 h-5 w-5',
                        isActive ? 'text-primary-600' : 'text-neutral-400'
                      )}
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-neutral-200">
              <div className="text-xs text-neutral-500 text-center">
                <p>MediQuick v1.0</p>
                <p>Quick Medicine Delivery</p>
              </div>
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
};

export default Sidebar;
