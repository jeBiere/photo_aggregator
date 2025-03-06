<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl shadow-lg">
    <!-- Заголовок профиля -->
    <div class="mb-8">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">Profile</h1>
    </div>

    <!-- Блок с информацией о пользователе -->
    <div class="flex flex-col gap-6">
      <div class="flex items-center gap-4">
        <!-- Картинка профиля -->
        <img
          src="https://via.placeholder.com/100"
          alt="User Avatar"
          class="rounded-full border-4 border-blue-500 w-24 h-24"
        />
        <div>
          <h2 class="text-2xl font-semibold text-slate-700">
            Username: <span class="text-slate-500">JohnDoe</span>
          </h2>
          <p class="text-slate-400">
            Registered on: <span class="text-slate-600">Jan 10, 2022</span>
          </p>
        </div>
      </div>

      <!-- Информация о заказах -->
      <div class="bg-gray-100 p-6 rounded-xl shadow-md">
        <h3 class="text-xl text-slate-600 mb-4">Orders</h3>
        <ul class="space-y-4">
          <li class="flex justify-between p-4 bg-white rounded-lg shadow-sm">
            <span class="font-medium">Order #12345</span>
            <span class="text-green-600">Completed</span>
          </li>
          <li class="flex justify-between p-4 bg-white rounded-lg shadow-sm">
            <span class="font-medium">Order #12346</span>
            <span class="text-orange-500">Pending</span>
          </li>
          <li class="flex justify-between p-4 bg-white rounded-lg shadow-sm">
            <span class="font-medium">Order #12347</span>
            <span class="text-red-500">Canceled</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const user = ref({
  username: 'JohnDoe',
  registrationDate: '2022-01-10',
  orders: [
    { id: 12345, status: 'Completed' },
    { id: 12346, status: 'Pending' },
    { id: 12347, status: 'Canceled' }
  ]
})
</script>

<style scoped>
/* Параметры для картинки профиля */
img {
  object-fit: cover;
  border-radius: 50%;
}

/* Тени для контейнеров */
.bg-gray-100 {
  background-color: #f7fafc;
}

.shadow-lg {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Дополнительные стили для карточек заказов */
ul {
  list-style: none;
  padding: 0;
}
</style>
