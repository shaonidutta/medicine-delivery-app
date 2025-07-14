import React from 'react';
import { motion } from 'framer-motion';

const MedicineCatalogPage: React.FC = () => {
  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <h1 className="text-3xl font-bold text-neutral-900">Medicine Catalog</h1>
      <div className="card p-8 text-center">
        <p className="text-neutral-600">Medicine catalog page coming soon...</p>
      </div>
    </motion.div>
  );
};

export default MedicineCatalogPage;
