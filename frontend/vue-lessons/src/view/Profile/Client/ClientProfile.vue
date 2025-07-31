<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl shadow-lg mx-auto">
    <!-- Заголовок профиля -->
    <div class="mb-8">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">Client Profile</h1>
    </div>

    <!-- Блок с информацией о пользователе -->
    <div class="flex flex-col gap-6">
      <!-- Блок с информацией о пользователе -->
      <div class="flex items-center gap-4">
        <AvatarDisplay :avatar-url="user.avatar_url" @edit="showUploader = true" />
        <div>
          <h2 class="text-2xl font-semibold text-slate-700 mb-1">
            Username: <span class="text-slate-500">{{ user?.login }}</span>
          </h2>
          <p class="text-slate-400 text-sm mb-4">
            Registered on:
            <span class="text-slate-600">
              {{ new Date(user?.created_at).toLocaleDateString() }}
            </span>
          </p>
          <div class="text-slate-700 space-y-2">
            <p><strong>Name:</strong> {{ user.first_name }}</p>
            <p><strong>Surname:</strong> {{ user.last_name }}</p>
            <p><strong>Email:</strong> {{ user.email }}</p>
            <p><strong>Phone:</strong> {{ user.phone }}</p>
            <p><strong>City:</strong> {{ user.city }}</p>
          </div>
        </div>
      </div>

      <!-- Список заказов клиента -->
      <OrderList :orders="orders" :OrderComponent="Order" userType="client" />
      <!-- Отзывы клиента -->
      <ReviewList :reviews="reviews" :ReviewComponent="Review" userType="client" />
    </div>

    <!-- Модалка для аватара -->
    <AvatarUploader
      :open="showUploader"
      @update:open="showUploader = $event"
      @avatar-updated="handleAvatarUpdated"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import OrderList from '../OrderList.vue'
import ReviewList from '../ReviewList.vue'
import AvatarDisplay from '../AvatarDisplay.vue'
import AvatarUploader from '../AvatarUploader.vue'
import Order from '../Order.vue'
import Review from '../Review.vue'

const props = defineProps({
  user: Object,
  orders: Array,
  reviews: Array
})

const showUploader = ref(false)

const handleAvatarUpdated = (newAvatarUrl) => {
  // Обновляем аватар пользователя
  props.user.avatar_url = newAvatarUrl
  // Можно добавить здесь вызов API для обновления профиля, если нужно
}
</script>
