import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

import RegistrationForm from '../view/RegistrationForm.vue'
import LoginForm from '@/view/LoginForm.vue'
import About from '@/view/About.vue'
import Profile from '@/view/Profile/Profile.vue'
import Studios from '@/view/Studios.vue'
import Photographers from '@/view/Photographers.vue'

const routes = [
  {
    path: '/',
    redirect: '/about'
  },
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
    path: '/profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/studios',
    component: Studios,
    meta: { requiresAuth: true }
  },
  {
    path: '/photographers',
    component: Photographers,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  await authStore.validateToken()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/profile')
  }

  next()
})

export default router
