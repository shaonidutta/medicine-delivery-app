import React from 'react';
import { motion } from 'framer-motion';
import Header from './Header';
import Sidebar from './Sidebar';
import Footer from './Footer';
import { useUIStore } from '../stores/uiStore';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { sidebarOpen } = useUIStore();

  return (
    <div className="min-h-screen bg-neutral-50 flex flex-col">
      {/* Header */}
      <Header />
      
      {/* Main content area */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Main content */}
        <motion.main
          className={`flex-1 transition-all duration-300 ease-smooth ${
            sidebarOpen ? 'lg:ml-64' : 'lg:ml-0'
          }`}
          layout
        >
          <div className="container mx-auto px-4 py-6 max-w-7xl">
            {children}
          </div>
        </motion.main>
      </div>
      
      {/* Footer */}
      <Footer />
      
      {/* Sidebar overlay for mobile */}
      {sidebarOpen && (
        <motion.div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => useUIStore.getState().toggleSidebar()}
        />
      )}
    </div>
  );
};

export default Layout;
