<template>
  <div class="card w-full">
    <!-- Левый блок: аватарка + город, опыт, цена -->
    <div class="card-left">
      <img :src="avatarUrl" alt="avatar" class="avatar" />
      <div class="info">
        <p>Город: {{ photographer.city }}</p>
        <p>Опыт: {{ photographer.experience_years }} лет</p>
        <p>Цена: {{ photographer.price_per_hour }} ₽/час</p>
      </div>
    </div>

    <!-- Центральный блок: имя, специализации, описание -->
    <div class="card-center">
      <h2 class="name">{{ photographer.user?.first_name }} {{ photographer.user?.last_name }}</h2>

      <div class="specializations">
        <span class="label">Профили съёмки:</span>
        <div class="tags">
          <span v-for="(spec, index) in specializations" :key="index" class="tag">
            {{ spec }}
          </span>
        </div>
      </div>

      <PhotographerPortfolioPreview :photographer-id="photographer.photographer_id" />

      <div class="description-block">
        {{ photographer.description }}
      </div>
    </div>

    <!-- Правый блок: рейтинг и кнопка -->
    <div class="card-right">
      <div class="rating-badge">{{ photographer.rating }}/5</div>
      <button class="details-button" @click="showDetails">Подробнее</button>
    </div>

    <!-- Модальное окно -->
    <PhotographerCardFull
      v-if="showModal"
      :photographer="photographer"
      :specializations="specializations"
      @close="hideDetails"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import PhotographerCardFull from './PhotographerCardFull.vue'
import PhotographerPortfolioPreview from './PhotographerPortfolioPreview.vue'

const props = defineProps({
  photographer: Object
})

const specializations = ref([])
const avatarUrl = computed(() => props.photographer.avatar_url || '/portrait.svg')
const showModal = ref(false)

const showDetails = () => {
  showModal.value = true
  document.body.style.overflow = 'hidden' // Блокируем скролл страницы
}

const hideDetails = () => {
  showModal.value = false
  document.body.style.overflow = '' // Восстанавливаем скролл
}

onMounted(async () => {
  const response = await fetch(
    `http://localhost:8000/photographers/${props.photographer.photographer_id}/specializations`
  )
  if (response.ok) {
    specializations.value = await response.json()
  }
})
</script>

<style scoped>
/* Оставляем существующие стили без изменений */
.card {
  display: flex;
  flex-direction: row;
  background-color: white;
  border-radius: 20px;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  position: relative;
}

.card-left {
  width: 250px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 30px;
}

.avatar {
  width: 220px;
  height: 220px;
  border-radius: 20px;
  object-fit: cover;
  margin-bottom: 12px;
}

.info {
  font-size: 15px;
  text-align: center;
  color: #555;
}

.card-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.name {
  font-size: 32px;
  color: #333;
  margin-bottom: 10px;
}

.specializations {
  margin-bottom: 12px;
  font-size: 15px;
}

.label {
  font-weight: bold;
  color: #333;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.tag {
  background-color: #ffedd5;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 14px;
  color: #333;
}

.description-block {
  background-color: #f5f5f5;
  padding: 12px;
  border-radius: 14px;
  min-height: 60px;
  flex-grow: 1;
  color: #444;
  font-size: 15px;
  margin-bottom: 12px;
}

.card-right {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
  margin-left: 30px;
  min-width: 120px;
}

.rating-badge {
  background-color: #ffedd5;
  border-radius: 9999px;
  padding: 10px 18px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: auto;
}

.details-button {
  margin-top: auto;
  background-color: #ffedd5;
  border: none;
  padding: 10px 18px;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  color: #333;
  transition: background-color 0.2s;
  align-self: flex-end;
  margin-right: 2px;
}

.details-button:hover {
  background-color: #fddfb0;
}
</style>
