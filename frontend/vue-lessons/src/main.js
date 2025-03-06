import './assets/main.css'
import router from './router/router'

import { createApp } from 'vue'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)

app.use(autoAnimatePlugin)
app.use(router)
app.use(createPinia())

app.mount('#app')
