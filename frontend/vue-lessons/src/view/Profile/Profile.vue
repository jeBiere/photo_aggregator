<template>
  <div>
    <ClientProfile
      v-if="user?.role === 'client'"
      :user="user"
      :orders="orders"
      :reviews="reviews"
    />
    <PhotographerProfile
      v-else-if="user?.role === 'photographer'"
      :user="user"
      :orders="orders"
      :reviews="reviews"
    />
    <div v-else class="text-center text-slate-500 mt-8">Unknown role or loading...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import axios from 'axios'
import { useRouter } from 'vue-router'

import ClientProfile from './Client/ClientProfile.vue'
import PhotographerProfile from './Photographer/PhotographerProfile.vue'

const user = ref(null)
const orders = ref([])
const reviews = ref([])
const authStore = useAuthStore()
const router = useRouter()

const fetchProfile = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  try {
    const headers = { Authorization: `Bearer ${authStore.token}` }

    const { data: userData } = await axios.get('http://localhost:8000/users/me', { headers })
    user.value = userData

    const { data: ordersData } = await axios.get('http://localhost:8000/orders/me', { headers })
    orders.value = ordersData

    const { data: reviewsData } = await axios.get('http://localhost:8000/reviews/me', { headers })
    reviews.value = reviewsData
    
  } catch (error) {
    console.error('Ошибка при загрузке профиля:', error)
  }
}

onMounted(fetchProfile)
provide('reviews', reviews)
</script>
