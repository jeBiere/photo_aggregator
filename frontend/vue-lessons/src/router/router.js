import { createRouter, createWebHashHistory } from 'vue-router'

import App from '@/App.vue'
import RegistrationForm from '../view/RegistrationForm.vue'
import LoginForm from '@/view/LoginForm.vue'
import About from '@/view/About.vue'
import Services from '@/view/Services.vue'
import Profile from '@/view/Profile.vue'
import Studios from '@/view/Studios.vue'
import Photographers from '@/view/Photographers.vue'

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/about',
      component: About
    },
    {
      path: '/registration',
      component: RegistrationForm
    },
    {
      path: '/login',
      component: LoginForm
    },
    {
      path: '/services',
      component: Services
    },
    {
      path: '/profile',
      component: Profile
    },
    {
      path: '/studios',
      component: Studios
    },
    {
      path: '/photographers',
      component: Photographers
    },
  ]
})
