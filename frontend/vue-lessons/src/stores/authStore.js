// src/stores/authStore.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },
    async validateToken() {
      if (!this.token) return

      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

      try {
        const { data } = await axios.get('http://localhost:8000/users/me') // или твоя ручка
        this.user = data
      } catch (err) {
        console.warn('Токен невалиден или истёк:', err)
        this.logout()
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  },
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user
  }
})
