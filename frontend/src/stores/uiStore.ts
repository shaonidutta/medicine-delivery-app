import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { FontScale, AccessibilitySettings, NotificationSettings } from '../types';

interface UIState {
  // Accessibility settings
  accessibilitySettings: AccessibilitySettings;
  
  // Notification settings
  notificationSettings: NotificationSettings;
  
  // UI state
  sidebarOpen: boolean;
  searchOpen: boolean;
  cartOpen: boolean;
  loading: boolean;
  
  // Search state
  searchQuery: string;
  searchHistory: string[];
  voiceSearchActive: boolean;
  
  // Modal state
  modalOpen: boolean;
  modalContent: React.ReactNode | null;
  
  // Toast notifications
  toasts: Array<{
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    title: string;
    message?: string;
    duration?: number;
  }>;
  
  // Actions
  setFontScale: (scale: FontScale['scale']) => void;
  toggleHighContrast: () => void;
  toggleReducedMotion: () => void;
  toggleScreenReader: () => void;
  updateNotificationSettings: (settings: Partial<NotificationSettings>) => void;
  
  // UI actions
  toggleSidebar: () => void;
  toggleSearch: () => void;
  toggleCart: () => void;
  setLoading: (loading: boolean) => void;
  
  // Search actions
  setSearchQuery: (query: string) => void;
  addToSearchHistory: (query: string) => void;
  clearSearchHistory: () => void;
  toggleVoiceSearch: () => void;
  
  // Modal actions
  openModal: (content: React.ReactNode) => void;
  closeModal: () => void;
  
  // Toast actions
  addToast: (toast: Omit<UIState['toasts'][0], 'id'>) => void;
  removeToast: (id: string) => void;
  clearToasts: () => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      // Initial state
      accessibilitySettings: {
        font_scale: 100,
        high_contrast: false,
        reduced_motion: false,
        screen_reader: false,
      },
      
      notificationSettings: {
        delivery_updates: true,
        medicine_reminders: true,
        order_status: true,
        prescription_expiry: true,
        marketing: false,
      },
      
      sidebarOpen: false,
      searchOpen: false,
      cartOpen: false,
      loading: false,
      
      searchQuery: '',
      searchHistory: [],
      voiceSearchActive: false,
      
      modalOpen: false,
      modalContent: null,
      
      toasts: [],

      // Accessibility actions
      setFontScale: (scale: FontScale['scale']) => {
        set((state) => ({
          accessibilitySettings: {
            ...state.accessibilitySettings,
            font_scale: scale,
          },
        }));
        
        // Apply font scale to document
        document.documentElement.style.fontSize = `${scale}%`;
      },

      toggleHighContrast: () => {
        set((state) => {
          const newHighContrast = !state.accessibilitySettings.high_contrast;
          
          // Apply high contrast to document
          if (newHighContrast) {
            document.documentElement.classList.add('high-contrast');
          } else {
            document.documentElement.classList.remove('high-contrast');
          }
          
          return {
            accessibilitySettings: {
              ...state.accessibilitySettings,
              high_contrast: newHighContrast,
            },
          };
        });
      },

      toggleReducedMotion: () => {
        set((state) => {
          const newReducedMotion = !state.accessibilitySettings.reduced_motion;
          
          // Apply reduced motion to document
          if (newReducedMotion) {
            document.documentElement.classList.add('reduce-motion');
          } else {
            document.documentElement.classList.remove('reduce-motion');
          }
          
          return {
            accessibilitySettings: {
              ...state.accessibilitySettings,
              reduced_motion: newReducedMotion,
            },
          };
        });
      },

      toggleScreenReader: () => {
        set((state) => ({
          accessibilitySettings: {
            ...state.accessibilitySettings,
            screen_reader: !state.accessibilitySettings.screen_reader,
          },
        }));
      },

      updateNotificationSettings: (settings: Partial<NotificationSettings>) => {
        set((state) => ({
          notificationSettings: {
            ...state.notificationSettings,
            ...settings,
          },
        }));
      },

      // UI actions
      toggleSidebar: () => {
        set((state) => ({ sidebarOpen: !state.sidebarOpen }));
      },

      toggleSearch: () => {
        set((state) => ({ searchOpen: !state.searchOpen }));
      },

      toggleCart: () => {
        set((state) => ({ cartOpen: !state.cartOpen }));
      },

      setLoading: (loading: boolean) => {
        set({ loading });
      },

      // Search actions
      setSearchQuery: (query: string) => {
        set({ searchQuery: query });
      },

      addToSearchHistory: (query: string) => {
        set((state) => {
          const newHistory = [query, ...state.searchHistory.filter(h => h !== query)].slice(0, 10);
          return { searchHistory: newHistory };
        });
      },

      clearSearchHistory: () => {
        set({ searchHistory: [] });
      },

      toggleVoiceSearch: () => {
        set((state) => ({ voiceSearchActive: !state.voiceSearchActive }));
      },

      // Modal actions
      openModal: (content: React.ReactNode) => {
        set({ modalOpen: true, modalContent: content });
      },

      closeModal: () => {
        set({ modalOpen: false, modalContent: null });
      },

      // Toast actions
      addToast: (toast: Omit<UIState['toasts'][0], 'id'>) => {
        const id = Math.random().toString(36).substr(2, 9);
        const newToast = { ...toast, id };
        
        set((state) => ({
          toasts: [...state.toasts, newToast],
        }));

        // Auto-remove toast after duration
        const duration = toast.duration || 5000;
        setTimeout(() => {
          get().removeToast(id);
        }, duration);
      },

      removeToast: (id: string) => {
        set((state) => ({
          toasts: state.toasts.filter(toast => toast.id !== id),
        }));
      },

      clearToasts: () => {
        set({ toasts: [] });
      },
    }),
    {
      name: 'ui-storage',
      partialize: (state) => ({
        accessibilitySettings: state.accessibilitySettings,
        notificationSettings: state.notificationSettings,
        searchHistory: state.searchHistory,
      }),
      onRehydrateStorage: () => (state) => {
        // Apply accessibility settings when rehydrating
        if (state?.accessibilitySettings) {
          const { font_scale, high_contrast, reduced_motion } = state.accessibilitySettings;
          
          document.documentElement.style.fontSize = `${font_scale}%`;
          
          if (high_contrast) {
            document.documentElement.classList.add('high-contrast');
          }
          
          if (reduced_motion) {
            document.documentElement.classList.add('reduce-motion');
          }
        }
      },
    }
  )
);
