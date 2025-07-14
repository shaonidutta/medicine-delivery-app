import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { MagnifyingGlassIcon, MicrophoneIcon } from '@heroicons/react/24/outline';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import { useAuthStore } from '../stores/authStore';
import { useCartStore } from '../stores/cartStore';

const HomePage: React.FC = () => {
  const { user } = useAuthStore();
  const { getTotalItems } = useCartStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Navigate to search results
      window.location.href = `/medicines?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  const handleVoiceSearch = () => {
    setIsVoiceActive(true);
    // Implement voice search functionality
    setTimeout(() => setIsVoiceActive(false), 3000);
  };

  const cartItemCount = getTotalItems();

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <motion.section
        className="text-center py-12 px-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <motion.h1
          className="text-4xl md:text-6xl font-bold text-neutral-900 mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          Welcome back, {user?.first_name}!
        </motion.h1>
        
        <motion.p
          className="text-xl text-neutral-600 mb-8 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          Quick and reliable medicine delivery at your fingertips. 
          Search for medicines, upload prescriptions, and get them delivered in 30 minutes.
        </motion.p>

        {/* Search Bar */}
        <motion.div
          className="max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <form onSubmit={handleSearch} className="relative">
            <Input
              type="text"
              placeholder="Search for medicines, brands, or health conditions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              inputSize="lg"
              leftIcon={<MagnifyingGlassIcon className="w-5 h-5" />}
              rightIcon={
                <button
                  type="button"
                  onClick={handleVoiceSearch}
                  className={`p-1 rounded-full transition-colors ${
                    isVoiceActive 
                      ? 'text-accent-600 bg-accent-100' 
                      : 'text-neutral-400 hover:text-neutral-600'
                  }`}
                >
                  <MicrophoneIcon className="w-5 h-5" />
                </button>
              }
              className="pr-12"
            />
            <Button
              type="submit"
              className="absolute right-2 top-1/2 transform -translate-y-1/2"
              size="sm"
            >
              Search
            </Button>
          </form>
        </motion.div>
      </motion.section>

      {/* Quick Actions */}
      <motion.section
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <Link to="/medicines" className="card-interactive p-6 text-center">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">Browse Medicines</h3>
          <p className="text-neutral-600">Explore our comprehensive medicine catalog</p>
        </Link>

        <Link to="/prescriptions/upload" className="card-interactive p-6 text-center">
          <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">Upload Prescription</h3>
          <p className="text-neutral-600">Upload your prescription for quick ordering</p>
        </Link>

        <Link to="/cart" className="card-interactive p-6 text-center relative">
          <div className="w-12 h-12 bg-accent-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8" />
            </svg>
          </div>
          {cartItemCount > 0 && (
            <span className="absolute top-2 right-2 bg-accent-600 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center">
              {cartItemCount}
            </span>
          )}
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">My Cart</h3>
          <p className="text-neutral-600">
            {cartItemCount > 0 ? `${cartItemCount} items in cart` : 'Your cart is empty'}
          </p>
        </Link>

        <Link to="/orders" className="card-interactive p-6 text-center">
          <div className="w-12 h-12 bg-neutral-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-neutral-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">Order History</h3>
          <p className="text-neutral-600">Track your orders and reorder easily</p>
        </Link>
      </motion.section>

      {/* Featured Categories */}
      <motion.section
        className="space-y-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
      >
        <h2 className="text-2xl font-bold text-neutral-900">Popular Categories</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {[
            { name: 'Pain Relief', icon: '💊', color: 'bg-red-100 text-red-600' },
            { name: 'Vitamins', icon: '🌟', color: 'bg-yellow-100 text-yellow-600' },
            { name: 'First Aid', icon: '🩹', color: 'bg-green-100 text-green-600' },
            { name: 'Baby Care', icon: '👶', color: 'bg-pink-100 text-pink-600' },
            { name: 'Diabetes', icon: '🩺', color: 'bg-blue-100 text-blue-600' },
            { name: 'Heart Care', icon: '❤️', color: 'bg-purple-100 text-purple-600' },
          ].map((category, index) => (
            <motion.div
              key={category.name}
              className="card-interactive p-4 text-center"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: 0.6 + index * 0.1 }}
            >
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3 ${category.color}`}>
                <span className="text-2xl">{category.icon}</span>
              </div>
              <h3 className="text-sm font-medium text-neutral-900">{category.name}</h3>
            </motion.div>
          ))}
        </div>
      </motion.section>

      {/* Emergency Section */}
      <motion.section
        className="bg-gradient-to-r from-accent-600 to-accent-700 rounded-xl p-8 text-white text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.7 }}
      >
        <h2 className="text-2xl font-bold mb-4">Need Emergency Medicine?</h2>
        <p className="text-accent-100 mb-6">
          Get critical medicines delivered in 15 minutes with our emergency service
        </p>
        <Button variant="outline" className="bg-white text-accent-600 hover:bg-accent-50">
          Emergency Order
        </Button>
      </motion.section>
    </div>
  );
};

export default HomePage;
