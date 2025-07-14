import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

// Store imports
import { useAuthStore } from './stores/authStore';
import { useUIStore } from './stores/uiStore';

// Component imports
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LoadingSpinner from './components/ui/LoadingSpinner';
import ToastContainer from './components/ui/ToastContainer';
import Modal from './components/ui/Modal';

// Page imports
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MedicineCatalogPage from './pages/MedicineCatalogPage';
import MedicineDetailPage from './pages/MedicineDetailPage';
import CartPage from './pages/CartPage';
import CheckoutPage from './pages/CheckoutPage';
import OrdersPage from './pages/OrdersPage';
import OrderDetailPage from './pages/OrderDetailPage';
import OrderTrackingPage from './pages/OrderTrackingPage';
import PrescriptionsPage from './pages/PrescriptionsPage';
import PrescriptionUploadPage from './pages/PrescriptionUploadPage';
import ProfilePage from './pages/ProfilePage';
import NotFoundPage from './pages/NotFoundPage';

// Admin pages (basic)
import AdminDashboard from './pages/admin/AdminDashboard';

function App() {
  const { isAuthenticated, token, refreshAccessToken } = useAuthStore();
  const { loading, modalOpen, modalContent, accessibilitySettings } = useUIStore();

  // Initialize app
  useEffect(() => {
    // Apply accessibility settings on app load
    const { font_scale, high_contrast, reduced_motion } = accessibilitySettings;
    
    document.documentElement.style.fontSize = `${font_scale}%`;
    
    if (high_contrast) {
      document.documentElement.classList.add('high-contrast');
    }
    
    if (reduced_motion) {
      document.documentElement.classList.add('reduce-motion');
    }

    // Auto-refresh token if user is authenticated
    if (token) {
      refreshAccessToken().catch(() => {
        // Handle refresh failure silently
      });
    }
  }, [token, refreshAccessToken, accessibilitySettings]);

  // Page transition variants
  const pageVariants = {
    initial: {
      opacity: 0,
      y: 20,
    },
    in: {
      opacity: 1,
      y: 0,
    },
    out: {
      opacity: 0,
      y: -20,
    },
  };

  const pageTransition = {
    type: 'tween' as const,
    ease: 'anticipate' as const,
    duration: 0.3,
  };

  return (
    <Router>
      <div className="App min-h-screen bg-neutral-50">
        {/* Global loading overlay */}
        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm"
            >
              <LoadingSpinner size="lg" />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Main app content */}
        <AnimatePresence mode="wait">
          <Routes>
            {/* Public routes */}
            <Route
              path="/login"
              element={
                !isAuthenticated ? (
                  <motion.div
                    key="login"
                    initial="initial"
                    animate="in"
                    exit="out"
                    variants={pageVariants}
                    transition={pageTransition}
                  >
                    <LoginPage />
                  </motion.div>
                ) : (
                  <Navigate to="/" replace />
                )
              }
            />
            
            <Route
              path="/register"
              element={
                !isAuthenticated ? (
                  <motion.div
                    key="register"
                    initial="initial"
                    animate="in"
                    exit="out"
                    variants={pageVariants}
                    transition={pageTransition}
                  >
                    <RegisterPage />
                  </motion.div>
                ) : (
                  <Navigate to="/" replace />
                )
              }
            />

            {/* Protected routes with layout */}
            <Route
              path="/*"
              element={
                <ProtectedRoute>
                  <Layout>
                    <AnimatePresence mode="wait">
                      <Routes>
                        <Route
                          path="/"
                          element={
                            <motion.div
                              key="home"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <HomePage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/medicines"
                          element={
                            <motion.div
                              key="medicines"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <MedicineCatalogPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/medicines/:id"
                          element={
                            <motion.div
                              key="medicine-detail"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <MedicineDetailPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/cart"
                          element={
                            <motion.div
                              key="cart"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <CartPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/checkout"
                          element={
                            <motion.div
                              key="checkout"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <CheckoutPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/orders"
                          element={
                            <motion.div
                              key="orders"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <OrdersPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/orders/:id"
                          element={
                            <motion.div
                              key="order-detail"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <OrderDetailPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/orders/:id/tracking"
                          element={
                            <motion.div
                              key="order-tracking"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <OrderTrackingPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/prescriptions"
                          element={
                            <motion.div
                              key="prescriptions"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <PrescriptionsPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/prescriptions/upload"
                          element={
                            <motion.div
                              key="prescription-upload"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <PrescriptionUploadPage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/profile"
                          element={
                            <motion.div
                              key="profile"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <ProfilePage />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="/admin/*"
                          element={
                            <motion.div
                              key="admin"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <AdminDashboard />
                            </motion.div>
                          }
                        />
                        
                        <Route
                          path="*"
                          element={
                            <motion.div
                              key="not-found"
                              initial="initial"
                              animate="in"
                              exit="out"
                              variants={pageVariants}
                              transition={pageTransition}
                            >
                              <NotFoundPage />
                            </motion.div>
                          }
                        />
                      </Routes>
                    </AnimatePresence>
                  </Layout>
                </ProtectedRoute>
              }
            />
          </Routes>
        </AnimatePresence>

        {/* Global UI components */}
        <ToastContainer />
        
        {/* Global modal */}
        <AnimatePresence>
          {modalOpen && modalContent && (
            <Modal onClose={() => useUIStore.getState().closeModal()}>
              {modalContent}
            </Modal>
          )}
        </AnimatePresence>
      </div>
    </Router>
  );
}

export default App;
