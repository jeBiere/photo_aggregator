<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-card x-large">
      <!-- Кнопка закрытия -->
      <button class="close-button" @click="closeModal">
        <span class="close-icon">×</span>
      </button>

      <!-- Основной контент -->
      <div class="modal-content">
        <!-- Левая колонка - информация о фотографе -->
        <div class="photographer-info">
          <div class="header-section">
            <img :src="avatarUrl" alt="avatar" class="avatar" />
            <div class="name-section">
              <h2>{{ photographer.user?.first_name }} {{ photographer.user?.last_name }}</h2>
              <div class="rating-badge">{{ photographer.rating }}/5</div>
            </div>
          </div>

          <div class="details-section">
            <div class="detail-item">
              <span class="detail-label">Город:</span>
              <span class="detail-value">{{ photographer.city }}</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Опыт:</span>
              <span class="detail-value">{{ photographer.experience_years }} лет</span>
            </div>

            <div class="detail-item">
              <span class="detail-label">Цена:</span>
              <span class="detail-value">{{ photographer.price_per_hour }} ₽/час</span>
            </div>

            <div class="specializations-section">
              <h3>Специализации:</h3>
              <div class="tags">
                <span
                  v-for="(spec, index) in photographer.specializations"
                  :key="index"
                  class="tag"
                >
                  {{ spec }}
                </span>
              </div>
            </div>

            <div class="description-section">
              <h3>О фотографе:</h3>
              <p>{{ photographer.description }}</p>
            </div>
          </div>
        </div>

        <!-- Правая колонка - место для будущего календаря и работ -->
        <div class="right-section full-height">
          <PhotographerCalendar
            :photographerId="photographer.photographer_id"
            class="calendar-container"
            @dateSelected="updateSelectedDate"
            @timeSelected="updateSelectedTime"
          />
        </div>
      </div>

      <!-- Кнопка бронирования -->
      <div class="flex justify-center items-center">
        <button
          :disabled="!isBookingAvailable"
          :class="[
            'font-bold py-2 px-4 rounded-3xl mt-8 transition ease-in-out duration-300 uppercase',
            isBookingAvailable
              ? 'bg-orange-100 hover:bg-orange-200 text-slate-600 cursor-pointer'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          ]"
          @click="openModal"
        >
          Забронировать
        </button>
      </div>

      <!-- Модальное окно -->
      <CreateOrder
        v-if="isModalVisible"
        :isVisible="isModalVisible"
        :photographerId="photographer.photographer_id"
        :userId="userId"
        :selectedDate="selectedDate"
        :selectedTime="selectedTime"
        @update:isVisible="isModalVisible = $event"
        @confirm="handleBookingConfirm"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import PhotographerCalendar from './PhotographerCalendar.vue'
import CreateOrder from '../CreateOrder.vue'
import { useAuthStore } from '@/stores/authStore' // Assuming Pinia store for authentication
import axios from 'axios'
import { useRouter } from 'vue-router'

const emit = defineEmits(['close'])

const props = defineProps({
  photographer: Object, // Объект фотографа, передаваемый из родителя
  specializations: Array // Массив специализаций, передаваемый из родителя
})

const authStore = useAuthStore()
const router = useRouter()

const avatarUrl = computed(() => props.photographer.avatar_url || '/portrait.svg')
const userId = ref(null)
const selectedDate = ref(null) // Изначально null, будет обновляться при выборе
const selectedTime = ref(null) // Изначально null, будет обновляться при выборе
const isModalVisible = ref(false)

// Функция закрытия модалки
const closeModal = () => {
  emit('close')
}

// Функция открытия модалки
const openModal = () => {
  console.log('Open modal')
  isModalVisible.value = true
}

// Функция для подтверждения бронирования
const handleBookingConfirm = (orderData) => {
  // Обработка подтверждения бронирования
  console.log(orderData)
}

// Получаем информацию о пользователе и заказах
const fetchProfile = async () => {
  if (!authStore.isAuthenticated) {
    // Если токен отсутствует, перенаправляем на страницу логина
    router.push('/login')
    return
  }

  try {
    const token = authStore.token // Получаем токен из Pinia store
    const headers = { Authorization: `Bearer ${token}` }

    // Получаем данные пользователя
    const { data: userData } = await axios.get('http://localhost:8000/users/me', { headers })
    userId.value = userData.user_id
  } catch (error) {
    console.error('Ошибка при загрузке профиля:', error)
  }
}

// Обработчик для обновления выбранной даты
const updateSelectedDate = (date) => {
  selectedDate.value = date
}

// Обработчик для обновления выбранного времени
const updateSelectedTime = (time) => {
  selectedTime.value = time
}

const isBookingAvailable = computed(
  () =>
    props.photographer?.photographer_id && userId.value && selectedDate.value && selectedTime.value
)

fetchProfile()
</script>

<style scoped>
.right-section {
  width: 400px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.calendar-container {
  flex: 1; /* Позволяет календарю расти */
  width: 100%;
  min-height: 400px; /* Минимальная высота */
  background: white;
  border-radius: 12px;
  overflow: visible; /* Разрешаем элементам выходить за границы */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
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
  position: relative;
  background-color: white;
  border-radius: 20px;
  padding: 40px;
  width: 90%;
  max-width: 1000px;
  max-height: 95vh; /* Увеличил max-height */
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #ffedd5;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.close-icon {
  font-size: 24px;
  color: #333;
  line-height: 1;
  margin-top: -2px;
}

.modal-card.x-large {
  width: 95%;
  max-width: 1400px;
  padding: 30px;
  max-height: 95vh; /* Больше пространства для календаря */
}

.right-section.full-height {
  width: 65%;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  min-height: 500px; /* Гарантируем, что календарь влезет */
  max-height: calc(100% - 100px); /* Делаем высоту гибкой */
  overflow-y: auto; /* Если что-то не влезает, пусть прокручивается */
}

.close-button:hover {
  background-color: #fddfb0;
}

.modal-content {
  display: flex;
  gap: 40px;
  margin-bottom: 30px;
}

.photographer-info {
  flex: 1;
  min-width: 300px;
}

.header-section {
  display: flex;
  gap: 20px;
  margin-bottom: 25px;
  align-items: center;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 20px;
  object-fit: cover;
}

.name-section {
  flex: 1;
}

.name-section h2 {
  font-size: 28px;
  margin: 0 0 10px 0;
  color: #333;
}

.rating-badge {
  background-color: #ffedd5;
  border-radius: 9999px;
  padding: 8px 16px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  display: inline-block;
}

.details-section {
  margin-bottom: 25px;
}

.detail-item {
  margin-bottom: 12px;
  font-size: 16px;
}

.detail-label {
  font-weight: bold;
  color: #555;
  margin-right: 8px;
}

.detail-value {
  color: #333;
}

.specializations-section h3,
.description-section h3 {
  font-size: 18px;
  color: #333;
  margin: 20px 0 10px 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: #ffedd5;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 14px;
  color: #333;
}

.description-section p {
  font-size: 15px;
  line-height: 1.5;
  color: #444;
  margin: 0;
}

.placeholder-calendar,
.placeholder-portfolio {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 20px;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  font-size: 16px;
}

.placeholder-portfolio {
  height: 300px;
}

.book-button {
  display: block;
  width: 200px;
  margin: 0 auto;
  background-color: #ffedd5;
  border: none;
  padding: 14px 0;
  border-radius: 12px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}

.book-button:hover {
  background-color: #fddfb0;
}

.modal-card.large {
  width: 95%;
  max-width: 1200px;
  padding: 30px;
}

.right-section.expanded {
  width: 600px;
}
</style>
