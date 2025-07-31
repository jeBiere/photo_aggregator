<template>
  <div class="calendar-container">
    <div class="calendar-wrapper">
      <vue-cal
        date-picker
        view="month"
        :views="['month']"
        :views-bar="false"
        :today-button="false"
        :selected-date="selectedDate"
        @update:selected-date="handleDayClick"
        @view-change="handleMonthChange"
      />
    </div>

    <div class="slots-wrapper">
      <h2 class="text-2xl text-slate-600 text-center uppercase mx-10 border-b-2 pb-4">
        Интервалы для записи
      </h2>
      <div v-if="selectedSlots.length">
        <div class="slots-grid mt-10">
          <SelectableButton
            v-for="(slot, index) in selectedSlots"
            :key="index"
            :text="slot"
            :isActive="activeSlot === slot"
            @update:isActive="setActiveSlot(slot)"
            @view-change="handleMonthChange"
          />
        </div>
      </div>
      <div v-else>
        <p>Выберите дату, чтобы увидеть доступные интервалы</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'
import SelectableButton from '@/components/SelectableButton.vue'

const emit = defineEmits(['dateSelected', 'timeSelected'])

const props = defineProps({
  photographerId: {
    type: Number,
    required: true
  }
})

const selectedDate = ref(null)
const selectedSlots = ref([])
const availableDates = ref({})
const activeSlot = ref(null) // Храним активный интервал

// Получаем доступные даты
async function fetchAvailableDates(year, month) {
  const start = new Date(year, month, 1)
  const end = new Date(year, month + 1, 0)

  try {
    const response = await axios.get(
      `http://localhost:8000/schedules/availability/${props.photographerId}`,
      {
        params: {
          start: start.toISOString().split('T')[0],
          end: end.toISOString().split('T')[0]
        }
      }
    )

    const availabilityData = response.data
    availableDates.value = availabilityData
  } catch (error) {
    console.error('Ошибка при загрузке доступных дат:', error)
  }
}

// Обрабатываем клик по ячейке календаря
function handleDayClick(date) {
  const clickedDate = new Date(date)
  clickedDate.setDate(clickedDate.getDate() + 1)
  const dateStr = clickedDate.toISOString().split('T')[0] // Преобразуем дату в строку
  selectedDate.value = dateStr
  console.log(selectedDate.value)
  selectedSlots.value = availableDates.value[dateStr] || [] // Обновляем интервалы

  // Отправляем выбранную дату родительскому компоненту
  emit('dateSelected', selectedDate.value)
  emit('timeSelected', null)
}

// Обрабатываем смену месяца
function handleMonthChange(event) {
  console.log('Event received:', event)

  // Используем поле start (или extendedStart) для получения даты
  const startDate = event.start // Дата начала месяца
  console.log('startDate:', startDate)

  if (startDate) {
    const year = startDate.getFullYear()
    const month = startDate.getMonth()
    fetchAvailableDates(year, month)
    activeSlot.value = null
    emit('timeSelected', null)
  } else {
    console.error('startDate is undefined or null')
  }
}

// Устанавливаем активный интервал
function setActiveSlot(slot) {
  if (activeSlot.value === slot) {
    activeSlot.value = null // Если кликаем по уже активному, снимаем выделение
    emit('timeSelected', null)
  } else {
    activeSlot.value = slot // Если кликаем по новому, выделяем его
    // Отправляем выбранное время родительскому компоненту
    emit('timeSelected', activeSlot.value)
  }
}

// Получаем доступные даты при монтировании
onMounted(() => {
  const today = new Date()
  fetchAvailableDates(today.getFullYear(), today.getMonth())
})
</script>

<style>
.calendar-container {
  display: flex;
  justify-content: space-evenly;
  align-items: flex-start;
  gap: 40px;
  padding: 20px;
  flex-wrap: wrap; /* на всякий случай для адаптива */
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.calendar-wrapper {
  height: 500px;
  width: auto;
}
.slots-wrapper {
  min-width: 400px;
  max-width: 500px;
}

.slots-wrapper h2 {
  margin-bottom: 10px;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* можно увеличить до 3-4 */
  gap: 10px;
  margin-top: 10px;
}

.vuecal {
  --vuecal-primary-color: #c0996d !important;
  --vuecal-secondary-color: #ffedd5 !important;
  --vuecal-base-color: #000000 !important;
  --vuecal-contrast-color: #ffffff !important;
  --vuecal-border-radius: 16px !important;
  --vuecal-height: 500px !important;
  font-size: 1.5rem;
  height: 500px !important;
  width: 420px !important;
}
</style>
