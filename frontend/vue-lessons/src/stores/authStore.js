// src/stores/authStore.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token) // Сохраняем в localStorage
    },
    logout() {
      this.token = null
      localStorage.removeItem('token') // Удаляем при выходе
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.token // Проверяем, залогинен ли пользователь
  }
})
