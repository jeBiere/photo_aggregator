<template>
  <div class="filters-card w-full">
    <input v-model="city" placeholder="Город" class="input" />

    <div class="specializations-title">Специализации:</div>
    <div class="tags-container">
      <div
        v-for="spec in uniqueSpecializations"
        :key="spec"
        class="tag"
        :class="{ 'tag--active': selectedSpecs.includes(spec) }"
        @click="toggleSpec(spec)"
      >
        {{ spec }}
      </div>
    </div>

    <div class="price-filter">
      <div class="price-label">Макс. цена: {{ maxPrice }} ₽</div>
      <div class="slider-wrapper">
        <div class="slider-track">
          <div class="slider-progress" :style="{ width: sliderProgress + '%' }"></div>
        </div>
        <input
          type="range"
          min="1000"
          max="10000"
          step="500"
          v-model="maxPrice"
          class="slider-input"
          @input="updateSliderProgress"
        />
        <div class="slider-thumb" :style="{ left: sliderProgress + '%' }"></div>
      </div>
    </div>

    <button class="apply-button" @click="emitFilters">Применить фильтры</button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const emit = defineEmits(['apply-filters'])

const city = ref('')
const selectedSpecs = ref([])
const maxPrice = ref(10000)
const allSpecializations = ref([])
const sliderProgress = ref(100)

const uniqueSpecializations = computed(() => {
  const specs = allSpecializations.value.map((item) => item.specialization)
  return [...new Set(specs)]
})

const toggleSpec = (spec) => {
  const index = selectedSpecs.value.indexOf(spec)
  if (index === -1) {
    selectedSpecs.value.push(spec)
  } else {
    selectedSpecs.value.splice(index, 1)
  }
}

const updateSliderProgress = () => {
  const value = maxPrice.value
  const min = 1000
  const max = 10000
  sliderProgress.value = ((value - min) / (max - min)) * 100
}

onMounted(async () => {
  try {
    const res = await fetch('http://localhost:8000/specializations')
    if (res.ok) {
      allSpecializations.value = await res.json()
    }
    updateSliderProgress()
  } catch (error) {
    console.error('Ошибка при загрузке специализаций:', error)
  }
})

const emitFilters = () => {
  emit('apply-filters', {
    city: city.value,
    specializations: selectedSpecs.value,
    max_price: maxPrice.value
  })
}
</script>

<style scoped>
.filters-card {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 20px;
  margin: 20px auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.input {
  width: 100%;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #ddd;
  margin-bottom: 16px;
}

.specializations-title {
  margin-bottom: 12px;
  font-size: 15px;
  color: #555;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.tag {
  background-color: #f5f5f5;
  padding: 8px 16px;
  border-radius: 16px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tag--active {
  background-color: #ffedd5;
}

.price-filter {
  margin-bottom: 24px;
}

.price-label {
  margin-bottom: 8px;
  font-size: 15px;
  color: #555;
}

.slider-wrapper {
  position: relative;
  height: 24px;
  display: flex;
  align-items: center;
}

.slider-track {
  position: absolute;
  width: 100%;
  height: 6px;
  background: #ddd;
  border-radius: 3px;
}

.slider-progress {
  position: absolute;
  height: 100%;
  background: #ffedd5;
  border-radius: 3px;
}

.slider-input {
  position: absolute;
  width: 100%;
  height: 100%;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 3; 
}

.slider-thumb {
  position: absolute;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #ffedd5;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transform: translateX(-50%);
  z-index: 2;
  pointer-events: none;
}

.apply-button {
  display: block;
  margin: 0 auto;
  background-color: #ffedd5;
  border: none;
  padding: 12px 24px;
  border-radius: 14px;
  font-size: 16px;
  color: #333;
  cursor: pointer;
  transition: background-color 0.2s;
}

.apply-button:hover {
  background-color: #fddfb0;
}
</style>
