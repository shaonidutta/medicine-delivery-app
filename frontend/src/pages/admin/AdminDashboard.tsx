import React from 'react';
import { motion } from 'framer-motion';

const AdminDashboard: React.FC = () => {
  return (
    <motion.div className="space-y-6" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
      <h1 className="text-3xl font-bold text-neutral-900">Admin Dashboard</h1>
      <div className="card p-8 text-center">
        <p className="text-neutral-600">Admin dashboard coming soon...</p>
      </div>
    </motion.div>
  );
};

export default AdminDashboard;
