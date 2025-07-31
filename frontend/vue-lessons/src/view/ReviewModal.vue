<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white rounded-xl p-6 w-full max-w-md shadow-lg">
      <h2 class="text-xl font-bold mb-4">Оставить отзыв</h2>

      <!-- Информация о заказе -->
      <div class="bg-gray-100 p-4 rounded-lg mb-4 text-sm text-gray-800">
        <p><strong>ID заказа:</strong> {{ order.order_id }}</p>
        <p><strong>ID фотографа:</strong> {{ order.photographer_id ?? '—' }}</p>
        <p><strong>Дата съёмки:</strong> {{ formatDate(order.shoot_date) }}</p>
        <p><strong>Начало:</strong> {{ order.start_time }}</p>
        <p><strong>Длительность:</strong> {{ order.duration }} ч.</p>
        <p><strong>Цена:</strong> {{ formatPrice(order.price) }} ₽</p>
        <p><strong>Адрес:</strong> {{ order.address || 'Не указан' }}</p>
        <p><strong>Пожелания:</strong> {{ order.special_requests || '—' }}</p>
      </div>

      <!-- Поле оценки -->
      <label class="block mb-2 text-sm text-gray-700">Оценка (1-5):</label>
      <CustomSlider v-model:rating="rating" />
      <!-- Поле комментария -->
      <label class="block mb-2 text-sm text-gray-700">Комментарий:</label>
      <textarea
        v-model="comment"
        rows="4"
        class="w-full border border-gray-300 rounded-lg px-3 py-2"
      ></textarea>

      <!-- Кнопки -->
      <div class="flex justify-end gap-2 mt-6">
        <button
          @click="close"
          class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg transition duration-300"
        >
          Отмена
        </button>
        <button
          @click="submit"
          class="px-4 py-2 bg-orange-200 text-slate-600 rounded-lg hover:bg-orange-300 transition duration-300"
        >
          Отправить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import CustomSlider from '@/components/CustomSlider.vue'

const props = defineProps({
  order: { type: Object, required: true }
})

const emit = defineEmits(['close', 'submitted'])

const rating = ref(null)
const comment = ref('')
const userId = ref(null)

const authStore = useAuthStore()

// Получаем user_id один раз при монтировании
onMounted(async () => {
  const { data } = await axios.get('http://localhost:8000/users/me', {
    headers: {
      Authorization: `Bearer ${authStore.token}`
    }
  })
  userId.value = data.user_id
  console.log(userId.value)
})

const close = () => {
  emit('close')
}

const submit = async () => {
  try {
    await axios.post('http://localhost:8000/reviews/', {
      rating: rating.value,
      comment: comment.value,
      order_id: props.order.order_id,
      photographer_id: props.order.photographer_id,
      user_id: userId.value
    })

    close()
  } catch (error) {
    console.error('Ошибка при отправке отзыва:', error.response.data)
  }
}

// форматирование даты
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU')
}

// форматирование цены
const formatPrice = (value) => {
  return parseFloat(value).toFixed(2)
}
</script>
