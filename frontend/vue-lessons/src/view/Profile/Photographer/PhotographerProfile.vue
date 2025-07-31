<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl shadow-lg mx-auto">
    <!-- Заголовок профиля -->
    <div class="mb-8">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">
        Photographer Profile
      </h1>
    </div>

    <!-- Блок с информацией о пользователе -->
    <div class="flex flex-col gap-6">

      <div class="flex items-start gap-6 flex-wrap">
        <!-- Аватар -->
        <AvatarDisplay :avatar-url="user.avatar_url" @edit="showUploader = true" />

        <!-- Правая часть: логин + инфо -->
        <div class="flex flex-col flex-1 gap-4">
          <!-- Логин, дата и рейтинг -->
          <div class="flex flex-wrap items-center gap-4">
            <div>
              <h2 class="text-2xl font-semibold text-slate-700 flex items-center gap-4">
                Photographer: <span class="text-slate-500">{{ user?.login }}</span>
                <span v-if="!isLoading && photographer?.rating" class="rating-badge">
                  {{ photographer.rating }}
                </span>
              </h2>
              <p class="text-slate-400 text-sm mt-1">
                Joined:
                <span class="text-slate-600">
                  {{ new Date(user?.created_at).toLocaleDateString() }}
                </span>
              </p>
            </div>
          </div>

          <!-- Блоки с заголовками -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
            <!-- Личная информация -->
            <div class="text-slate-700">
              <h3 class="text-slate-500 font-semibold mb-2">Личная информация</h3>
              <div class="space-y-1">
                <p><strong>Имя:</strong> {{ user.first_name }}</p>
                <p><strong>Фамилия:</strong> {{ user.last_name }}</p>
                <p><strong>Email:</strong> {{ user.email }}</p>
                <p><strong>Телефон:</strong> {{ user.phone }}</p>
                <p><strong>Город:</strong> {{ user.city }}</p>
              </div>
            </div>

            <!-- Профессиональная информация -->
            <div v-if="!isLoading" class="text-slate-700">
              <h3 class="text-slate-500 font-semibold mb-2">Профессиональная информация</h3>
              <div class="space-y-1">
                <p><strong>Описание:</strong> {{ photographer?.description || 'Не указано' }}</p>
                <p>
                  <strong>Стаж:</strong> {{ photographer?.experience_years || 'Не указан' }} лет
                </p>
                <p>
                  <strong>Цена за час:</strong> {{ photographer?.price_per_hour || 'Не указана' }} ₽
                </p>
              </div>
            </div>
          </div>

          <!-- Загрузка -->
          <div v-if="isLoading" class="text-slate-500">Загрузка данных фотографа...</div>
        </div>
      </div>

      <!-- Заказы -->
      <OrderList :orders="orders" :OrderComponent="Order" userType="photographer" />

      <!-- График -->
      <ScheduleManager />

      <!-- Отзывы -->
      <ReviewList :reviews="reviews" :ReviewComponent="Review" userType="photographer" />

      <!-- Портфолио -->
      <PortfolioManager />
    </div>

    <!-- Модалка -->
    <AvatarUploader
      :open="showUploader"
      @update:open="showUploader = $event"
      @avatar-updated="handleAvatarUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import OrderList from '../OrderList.vue'
import ReviewList from '../ReviewList.vue'
import ScheduleManager from './ScheduleManager.vue'
import AvatarDisplay from '../AvatarDisplay.vue'
import AvatarUploader from '../AvatarUploader.vue'
import Order from '../Order.vue'
import Review from '../Review.vue'
import PortfolioManager from './PortfolioManager.vue'

const props = defineProps({
  user: Object,
  orders: Array,
  reviews: Array
})

const showUploader = ref(false)
const photographer = ref(null)
const isLoading = ref(true) // Флаг загрузки

const handleAvatarUpdated = (newAvatarUrl) => {
  props.user.avatar_url = newAvatarUrl
}

onMounted(async () => {
  if (props.user?.user_id) {
    try {
      const res = await axios.get(`http://localhost:8000/photographers/user/${props.user.user_id}`)
      photographer.value = res.data
    } catch (error) {
      console.error('Ошибка при загрузке данных фотографа:', error)
    } finally {
      isLoading.value = false // Завершаем загрузку, даже если ошибка
    }
  }
})
</script>

<style scoped>
.rating-badge {
  background-color: #ffedd5;
  border-radius: 9999px;
  padding: 2px 14px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-left: 8px;
}
</style>
