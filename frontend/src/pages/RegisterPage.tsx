import React from 'react';
import { motion } from 'framer-motion';

const RegisterPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-soft flex items-center justify-center py-12 px-4">
      <motion.div
        className="max-w-md w-full card p-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="text-2xl font-bold text-center mb-6">Register</h1>
        <p className="text-center text-neutral-600">
          Registration page coming soon...
        </p>
      </motion.div>
    </div>
  );
};

export default RegisterPage;
