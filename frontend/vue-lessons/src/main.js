import './assets/main.css'

import { createApp } from 'vue'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { createPinia } from 'pinia'
import router from './router/router'
import { VueCal } from 'vue-cal'

import 'vue-cal/style'
import App from './App.vue'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

app.use(autoAnimatePlugin)
app.use(router)
app.component('VueCal', VueCal)

import { useAuthStore } from './stores/authStore'
const authStore = useAuthStore()
authStore.validateToken() 

app.mount('#app')
