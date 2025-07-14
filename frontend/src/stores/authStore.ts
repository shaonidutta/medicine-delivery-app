import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User, AuthResponse, UserLogin, UserRegistration } from '../types';
import { authApi } from '../services/api';

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserRegistration) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<void>;
  clearError: () => void;
  updateUser: (userData: Partial<User>) => void;
  verifyPhone: (phone: string, otp: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (credentials: UserLogin) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.login(credentials);
          const { access_token, refresh_token, user } = response;
          
          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          
          // Set token in API client
          authApi.setAuthToken(access_token);
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.response?.data?.message || 'Login failed',
          });
          throw error;
        }
      },

      register: async (userData: UserRegistration) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.register(userData);
          const { access_token, refresh_token, user } = response;
          
          set({
            user,
            token: access_token,
            refreshToken: refresh_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
          
          // Set token in API client
          authApi.setAuthToken(access_token);
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.response?.data?.message || 'Registration failed',
          });
          throw error;
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          refreshToken: null,
          isAuthenticated: false,
          error: null,
        });
        
        // Clear token from API client
        authApi.setAuthToken(null);
        
        // Clear persisted state
        localStorage.removeItem('auth-storage');
      },

      refreshAccessToken: async () => {
        const { refreshToken } = get();
        if (!refreshToken) {
          get().logout();
          return;
        }

        try {
          const response = await authApi.refreshToken(refreshToken);
          const { access_token, refresh_token } = response;
          
          set({
            token: access_token,
            refreshToken: refresh_token,
          });
          
          // Set new token in API client
          authApi.setAuthToken(access_token);
        } catch (error) {
          // Refresh failed, logout user
          get().logout();
          throw error;
        }
      },

      clearError: () => {
        set({ error: null });
      },

      updateUser: (userData: Partial<User>) => {
        const { user } = get();
        if (user) {
          set({
            user: { ...user, ...userData },
          });
        }
      },

      verifyPhone: async (phone: string, otp: string) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.verifyPhone(phone, otp);
          const { user } = get();
          if (user) {
            set({
              user: { ...user, phone_verified: true },
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            isLoading: false,
            error: error.response?.data?.message || 'Phone verification failed',
          });
          throw error;
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        // Set token in API client when rehydrating
        if (state?.token) {
          authApi.setAuthToken(state.token);
        }
      },
    }
  )
);

// Auto-refresh token when it's about to expire
setInterval(() => {
  const { token, refreshAccessToken } = useAuthStore.getState();
  if (token) {
    // Check if token is about to expire (implement JWT decode logic)
    // For now, refresh every 50 minutes
    refreshAccessToken().catch(() => {
      // Handle refresh failure
    });
  }
}, 50 * 60 * 1000); // 50 minutes
