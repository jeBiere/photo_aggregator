<template>
  <div class="modal-overlay">
    <div class="modal-card">
      <button class="close-button" @click="closeModal">×</button>

      <div class="modal-header">
        <h1 class="text-5xl text-slate-600 text-center uppercase mx-10 border-b-2 pb-4">
          Ваш заказ
        </h1>
      </div>

      <div class="order-info">
        <div class="order-detail">
          <span class="label">Фотограф:</span> <span>{{ photographerName }}</span>
        </div>
        <div class="order-detail">
          <span class="label">ID пользователя:</span> <span>{{ userId }}</span>
        </div>
        <div class="order-detail">
          <span class="label">Дата:</span> <span>{{ selectedDate }}</span>
        </div>
        <div class="order-detail">
          <span class="label">Время:</span> <span>{{ selectedTime }}</span>
        </div>
        <div class="order-detail">
          <span class="label">Цена за час:</span> <span>{{ photographerPrice }}₽</span>
        </div>

        <div class="order-detail">
          <span class="label">Длительность:</span>
          <div class="duration-control">
            <button class="circle-button" @click="decreaseDuration" :disabled="duration <= 1">
              -
            </button>

            <transition name="fade-scale" mode="out-in">
              <span :key="duration" class="duration-number">{{ duration }} ч</span>
            </transition>

            <button class="circle-button" @click="increaseDuration">+</button>
          </div>
        </div>

        <div class="order-detail total-price">
          <span class="label">Итого:</span> <span>{{ totalPrice }} ₽</span>
        </div>

        <div class="order-detail full-width">
          <label class="label">Адрес:</label>
          <InputField v-model="address" placeholder="Введите адрес" />
        </div>

        <div class="order-detail full-width">
          <label class="label">Доп. пожелания:</label>
          <InputField
            v-model="specialRequests"
            placeholder="Особые пожелания"
            :isTextarea="true"
            :rows="4"
          />
        </div>
      </div>

      <div class="flex justify-center items-center">
        <Button :label="'Подтвердить заказ'" @click="confirmBooking" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import InputField from '@/components/InputField.vue'
import Button from '@/components/Button.vue'
import axios from 'axios'

const emit = defineEmits()
const props = defineProps({
  isVisible: Boolean,
  photographerId: Number,
  userId: Number,
  selectedDate: String,
  selectedTime: String
})

const photographerName = ref('Загрузка...')
const photographerPrice = ref(0)
const duration = ref(1)
const address = ref('')
const specialRequests = ref('')

const totalPrice = computed(() => duration.value * photographerPrice.value)

const fetchPhotographerInfo = async () => {
  try {
    const { data: photographer } = await axios.get(
      `http://localhost:8000/photographers/${props.photographerId}`
    )
    photographerPrice.value = parseFloat(photographer.price_per_hour) || 0

    const userId = photographer.user_id
    const { data: user } = await axios.get(`http://localhost:8000/users/user_by_id/${userId}`)
    photographerName.value = `${user.first_name} ${user.last_name}`
  } catch (err) {
    console.error('Ошибка при получении информации о фотографе:', err)
    photographerName.value = 'Не удалось загрузить'
  }
}

onMounted(() => {
  if (props.photographerId) {
    fetchPhotographerInfo()
  }
})

watch(
  () => props.photographerId,
  () => {
    fetchPhotographerInfo()
  }
)

const increaseDuration = () => {
  duration.value += 1
}

const decreaseDuration = () => {
  if (duration.value > 1) {
    duration.value -= 1
  }
}

const closeModal = () => {
  emit('update:isVisible', false)
}

const confirmBooking = async () => {
  const orderPayload = {
    user_id: props.userId,
    photographer_id: props.photographerId,
    status: 'pending',
    shoot_date: props.selectedDate,
    start_time: props.selectedTime,
    duration: duration.value,
    price: totalPrice.value,
    address: address.value,
    special_requests: specialRequests.value
  }

  try {
    const response = await axios.post('http://localhost:8000/orders/', orderPayload)
    console.log('Заказ успешно создан:', response.data)
    emit('update:isVisible', false)
  } catch (error) {
    console.error('Ошибка при создании заказа:', error)
    alert('Не удалось создать заказ. Пожалуйста, попробуйте ещё раз.')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background-color: white;
  padding: 30px;
  border-radius: 15px;
  width: 600px;
  max-width: 90%;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.modal-header h1 {
  text-align: center;
  color: #334155;
  font-size: 2rem;
  margin-bottom: 20px;
}

.order-info {
  margin-top: 10px;
}

.order-detail {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  gap: 10px;
}

.order-detail.full-width {
  flex-direction: column;
}

.label {
  font-weight: bold;
  color: #475569;
}

.duration-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.duration-control {
  @apply flex items-center justify-center gap-4 mt-4;
}

.circle-button {
  @apply bg-orange-100 hover:bg-orange-200 
         text-slate-700 text-xl font-bold 
         w-10 h-10 rounded-full flex items-center justify-center 
         transition ease-in-out duration-300;
}

.duration-number {
  @apply text-xl font-semibold text-slate-700;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: all 0.3s ease;
}

.fade-scale-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.fade-scale-leave-to {
  opacity: 0;
  transform: scale(1.2);
}

.total-price span {
  font-size: 1.2em;
}

.text-input,
.textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  margin-top: 4px;
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 1.5em;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
}

.close-button:hover {
  color: #1e293b;
}
</style>
