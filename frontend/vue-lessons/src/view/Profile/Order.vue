<template>
  <div class="bg-white p-6 rounded-lg shadow-lg flex flex-col">
    <div class="flex justify-between items-center mb-4">
      <div class="flex flex-col">
        <p class="font-semibold text-slate-700">Order ID: {{ order.order_id }}</p>
        <p class="text-sm text-slate-500">
          {{ userType === 'client' ? 'Photographer' : 'Client' }}:
          {{ userType === 'client' ? order.photographer_id : order.user_id }}
        </p>
        <p class="text-sm text-slate-500">
          Date: {{ new Date(order.shoot_date).toLocaleDateString() }}
        </p>
        <p class="text-sm text-slate-500">Time: {{ order.start_time.slice(0, 5) }}</p>
        <p class="text-sm text-slate-400">Status: {{ order.status }}</p>
      </div>

      <!-- Кнопки управления заказом -->
      <div class="flex gap-2">
        <!-- Кнопки для фотографа -->
        <template v-if="userType === 'photographer'">
          <button
            v-if="order.status === 'pending'"
            @click="updateOrder('confirmed')"
            class="bg-blue-500 text-white px-4 py-2 rounded-lg"
          >
            Confirm
          </button>
          <button
            v-if="order.status === 'pending'"
            @click="updateOrder('cancelled')"
            class="bg-red-500 text-white px-4 py-2 rounded-lg"
          >
            Cancel
          </button>
          <button
            v-if="order.status === 'in_progress'"
            @click="updateOrder('completed')"
            class="bg-green-500 text-white px-4 py-2 rounded-lg"
          >
            Complete
          </button>
        </template>
        <template v-if="userType === 'client'">
          <!-- Проверка, есть ли отзыв для этого заказа -->
          <template v-if="authStore.isAuthenticated && order.status === 'completed'">
            <div v-if="hasReview">
              <!-- Отображаем рейтинг, если отзыв есть -->
              <div class="rating-badge">Оценка: {{ reviewForOrder }} / 5</div>
            </div>
            <button
              v-else
              @click="showReviewModal = true"
              class="bg-orange-200 hover:bg-orange-300 text-slate-600 px-4 py-2 rounded-lg transition-all duration-200"
            >
              Оставить отзыв
            </button>
            <Review v-if="showReviewModal" :order="order" @close="showReviewModal = false" />
          </template>
        </template>
      </div>
    </div>

    <p class="text-sm text-slate-500">Description: {{ order.comment }}</p>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { ref, inject, computed } from 'vue'
import Review from '../ReviewModal.vue'

const props = defineProps({
  order: { type: Object, required: true },
  userType: { type: String, required: true }
})

const emit = defineEmits(['update-order'])

const loading = ref(false)
const showReviewModal = ref(false)
const authStore = useAuthStore()
const reviews = inject('reviews')

const updateOrder = async (newStatus) => {
  if (!authStore.isAuthenticated) {
    alert('Вы не авторизованы')
    return
  }

  const headers = { Authorization: `Bearer ${authStore.token}` }
  const baseUrl = `http://localhost:8000/orders/${props.order.order_id}`

  let endpoint = ''
  if (newStatus === 'cancelled') endpoint = 'cancel'
  else if (newStatus === 'confirmed') endpoint = 'confirm'
  else if (newStatus === 'completed') endpoint = 'complete'

  try {
    loading.value = true
    const { data: updatedOrder } = await axios.post(`${baseUrl}/${endpoint}`, {}, { headers })
    emit('update-order', updatedOrder)
  } catch (error) {
    console.error('Ошибка при обновлении заказа:', error)
    alert('Не удалось обновить заказ')
  } finally {
    loading.value = false
  }
}

const hasReview = computed(() => {
  return reviews?.value?.some((review) => review.order_id === props.order.order_id)
})

const reviewForOrder = computed(() => {
  const r = reviews?.value?.find((review) => review.order_id === props.order.order_id)
  console.log(r.rating)
  return r.rating
})
</script>


<style>

.rating-badge {
  background-color: #ffedd5;
  border-radius: 9999px;
  padding: 6px 14px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  white-space: nowrap;
}

</style>