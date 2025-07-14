import { create } from 'zustand';
import type { Cart, CartItem, AddToCartRequest } from '../types';
import { cartApi } from '../services/api';

interface CartState {
  cart: Cart | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchCart: () => Promise<void>;
  addToCart: (item: AddToCartRequest) => Promise<void>;
  updateCartItem: (itemId: string, quantity: number, notes?: string) => Promise<void>;
  removeFromCart: (itemId: string) => Promise<void>;
  clearCart: () => Promise<void>;
  validateCart: () => Promise<any>;
  getCartSummary: () => Promise<any>;
  clearError: () => void;
  
  // Computed values
  getTotalItems: () => number;
  getTotalAmount: () => number;
  getHasPrescriptionItems: () => boolean;
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  isLoading: false,
  error: null,

  fetchCart: async () => {
    set({ isLoading: true, error: null });
    try {
      const cart = await cartApi.getCart();
      set({ cart, isLoading: false });
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.response?.data?.message || 'Failed to fetch cart',
      });
    }
  },

  addToCart: async (item: AddToCartRequest) => {
    set({ isLoading: true, error: null });
    try {
      const cartItem = await cartApi.addToCart(item);
      
      // Refresh cart after adding item
      await get().fetchCart();
      
      set({ isLoading: false });
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.response?.data?.message || 'Failed to add item to cart',
      });
      throw error;
    }
  },

  updateCartItem: async (itemId: string, quantity: number, notes?: string) => {
    set({ isLoading: true, error: null });
    try {
      await cartApi.updateCartItem(itemId, { quantity, notes });
      
      // Update local cart state
      const { cart } = get();
      if (cart) {
        const updatedItems = cart.items.map(item => 
          item.id === itemId 
            ? { 
                ...item, 
                quantity, 
                notes: notes || item.notes,
                total_price: quantity * item.unit_price 
              }
            : item
        );
        
        const subtotal = updatedItems.reduce((sum, item) => sum + item.total_price, 0);
        const tax_amount = subtotal * 0.18;
        const delivery_fee = subtotal < 500 ? 50 : 0;
        const total_amount = subtotal + tax_amount + delivery_fee;
        
        set({
          cart: {
            ...cart,
            items: updatedItems,
            total_items: updatedItems.length,
            subtotal,
            tax_amount,
            delivery_fee,
            total_amount,
          },
          isLoading: false,
        });
      }
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.response?.data?.message || 'Failed to update cart item',
      });
      throw error;
    }
  },

  removeFromCart: async (itemId: string) => {
    set({ isLoading: true, error: null });
    try {
      await cartApi.removeFromCart(itemId);
      
      // Update local cart state
      const { cart } = get();
      if (cart) {
        const updatedItems = cart.items.filter(item => item.id !== itemId);
        
        const subtotal = updatedItems.reduce((sum, item) => sum + item.total_price, 0);
        const tax_amount = subtotal * 0.18;
        const delivery_fee = subtotal < 500 ? 50 : 0;
        const total_amount = subtotal + tax_amount + delivery_fee;
        
        set({
          cart: {
            ...cart,
            items: updatedItems,
            total_items: updatedItems.length,
            subtotal,
            tax_amount,
            delivery_fee,
            total_amount,
          },
          isLoading: false,
        });
      }
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.response?.data?.message || 'Failed to remove item from cart',
      });
      throw error;
    }
  },

  clearCart: async () => {
    set({ isLoading: true, error: null });
    try {
      await cartApi.clearCart();
      set({
        cart: null,
        isLoading: false,
      });
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.response?.data?.message || 'Failed to clear cart',
      });
      throw error;
    }
  },

  validateCart: async () => {
    set({ isLoading: true, error: null });
    try {
      const validation = await cartApi.validateCart();
      set({ isLoading: false });
      return validation;
    } catch (error: any) {
      set({
        isLoading: false,
        error: error.response?.data?.message || 'Failed to validate cart',
      });
      throw error;
    }
  },

  getCartSummary: async () => {
    try {
      const summary = await cartApi.getCartSummary();
      return summary;
    } catch (error: any) {
      set({
        error: error.response?.data?.message || 'Failed to get cart summary',
      });
      throw error;
    }
  },

  clearError: () => {
    set({ error: null });
  },

  // Computed values
  getTotalItems: () => {
    const { cart } = get();
    return cart?.total_items || 0;
  },

  getTotalAmount: () => {
    const { cart } = get();
    return cart?.total_amount || 0;
  },

  getHasPrescriptionItems: () => {
    const { cart } = get();
    return cart?.has_prescription_items || false;
  },
}));
