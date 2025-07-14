import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  User,
  AuthResponse,
  UserLogin,
  UserRegistration,
  Medicine,
  MedicineSearchParams,
  MedicineSearchResponse,
  Category,
  Cart,
  CartItem,
  AddToCartRequest,
  Prescription,
  Order,
  CreateOrderFromCart,
} from '../types';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 errors (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh token
        const refreshToken = localStorage.getItem('refresh-token');
        if (refreshToken) {
          const response = await api.post('/auth/refresh', {
            refresh_token: refreshToken,
          });
          
          const { access_token } = response.data;
          localStorage.setItem('auth-token', access_token);
          
          // Retry original request
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('auth-token');
        localStorage.removeItem('refresh-token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (credentials: UserLogin): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  register: async (userData: UserRegistration): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  refreshToken: async (refreshToken: string): Promise<{ access_token: string; refresh_token: string }> => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  verifyPhone: async (phone: string, otp: string): Promise<void> => {
    await api.post('/auth/verify-phone', { phone, otp });
  },

  setAuthToken: (token: string | null) => {
    if (token) {
      localStorage.setItem('auth-token', token);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      localStorage.removeItem('auth-token');
      delete api.defaults.headers.common['Authorization'];
    }
  },
};

// Medicine API
export const medicineApi = {
  search: async (params: MedicineSearchParams): Promise<MedicineSearchResponse> => {
    const response = await api.get('/medicines/search', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Medicine> => {
    const response = await api.get(`/medicines/${id}`);
    return response.data;
  },

  getAlternatives: async (id: string): Promise<Medicine[]> => {
    const response = await api.get(`/medicines/${id}/alternatives`);
    return response.data;
  },

  getSuggestions: async (query: string): Promise<Medicine[]> => {
    const response = await api.get('/medicines/suggestions', { params: { q: query } });
    return response.data;
  },
};

// Category API
export const categoryApi = {
  getAll: async (): Promise<Category[]> => {
    const response = await api.get('/categories/');
    return response.data;
  },

  getWithCounts: async (): Promise<Category[]> => {
    const response = await api.get('/categories/with-counts');
    return response.data;
  },

  getById: async (id: string): Promise<Category> => {
    const response = await api.get(`/categories/${id}`);
    return response.data;
  },
};

// Cart API
export const cartApi = {
  getCart: async (): Promise<Cart> => {
    const response = await api.get('/cart/');
    return response.data;
  },

  addToCart: async (item: AddToCartRequest): Promise<CartItem> => {
    const response = await api.post('/cart/items', item);
    return response.data;
  },

  updateCartItem: async (itemId: string, data: { quantity: number; notes?: string }): Promise<CartItem> => {
    const response = await api.put(`/cart/items/${itemId}`, data);
    return response.data;
  },

  removeFromCart: async (itemId: string): Promise<void> => {
    await api.delete(`/cart/items/${itemId}`);
  },

  clearCart: async (): Promise<void> => {
    await api.delete('/cart/clear');
  },

  getCartSummary: async (): Promise<any> => {
    const response = await api.get('/cart/summary');
    return response.data;
  },

  validateCart: async (): Promise<any> => {
    const response = await api.post('/cart/validate');
    return response.data;
  },
};

// Prescription API
export const prescriptionApi = {
  upload: async (file: File, metadata?: any): Promise<Prescription> => {
    const formData = new FormData();
    formData.append('file', file);
    if (metadata) {
      formData.append('metadata', JSON.stringify(metadata));
    }

    const response = await api.post('/prescriptions/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getAll: async (params?: any): Promise<Prescription[]> => {
    const response = await api.get('/prescriptions/', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Prescription> => {
    const response = await api.get(`/prescriptions/${id}`);
    return response.data;
  },

  search: async (params: any): Promise<any> => {
    const response = await api.get('/prescriptions/search', { params });
    return response.data;
  },

  getStats: async (): Promise<any> => {
    const response = await api.get('/prescriptions/stats/overview');
    return response.data;
  },
};

// Order API
export const orderApi = {
  createFromCart: async (orderData: CreateOrderFromCart): Promise<Order> => {
    const response = await api.post('/orders/from-cart', orderData);
    return response.data;
  },

  getAll: async (params?: any): Promise<Order[]> => {
    const response = await api.get('/orders/', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Order> => {
    const response = await api.get(`/orders/${id}`);
    return response.data;
  },

  getTracking: async (id: string): Promise<any> => {
    const response = await api.get(`/orders/${id}/tracking`);
    return response.data;
  },

  cancelOrder: async (id: string, reason: string): Promise<Order> => {
    const response = await api.post(`/orders/${id}/cancel`, { reason });
    return response.data;
  },

  search: async (params: any): Promise<any> => {
    const response = await api.get('/orders/search', { params });
    return response.data;
  },

  getStats: async (): Promise<any> => {
    const response = await api.get('/orders/stats/overview');
    return response.data;
  },
};

// Health check
export const healthApi = {
  check: async (): Promise<{ status: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
