// src/frontend/frontend-app/src/store.js

import { create } from 'zustand';

export const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  isAuthenticated: false,
  token: null,
  setAuth: (isAuthenticated, token) => set({ isAuthenticated, token }),
  logout: () => set({ isAuthenticated: false, token: null }),
}));