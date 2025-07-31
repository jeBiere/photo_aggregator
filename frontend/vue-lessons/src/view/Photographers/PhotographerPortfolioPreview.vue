<template>
  <div class="portfolio-preview mt-4 w-full mb-6">
    <h3 class="text-lg font-semibold text-slate-700 mb-2">Примеры работ</h3>

    <div v-if="photos.length === 0" class="text-slate-400 text-sm">
      Фотограф пока не добавил примеры работ.
    </div>

    <div v-else class="flex items-center relative">
      <!-- Кнопка влево -->
      <button
        @click="scrollLeft"
        class="z-10 bg-orange-100 hover:bg-orange-200 p-2 transition ease-in-out duration-300 rounded-full shadow mx-1"
      >
        ◀
      </button>

      <!-- Лента фото -->
      <div
        ref="scrollContainer"
        class="overflow-x-auto scroll-smooth py-2 rounded-lg whitespace-nowrap no-scrollbar flex-1"
      >
        <div
          v-for="(photo, index) in photos"
          :key="index"
          class="inline-block cursor-pointer px-2"
          :class="{
            'ml-4': index === 0,
            'mr-4': index === photos.length - 1
          }"
          ref="photoRefs"
          @click="openPreview(photo)"
        >
          <img
            :src="`${API_BASE}/${photo.file_path}`"
            alt="Пример работы"
            class="h-40 w-auto object-cover rounded-lg shadow hover:scale-105 transition-transform duration-200"
          />
        </div>
      </div>

      <!-- Кнопка вправо -->
      <button
        @click="scrollRight"
        class="z-10 bg-orange-100 hover:bg-orange-200 p-2 rounded-full shadow mx-1"
      >
        ▶
      </button>
    </div>

    <!-- Модалка для просмотра фото -->
    <div
      v-if="previewPhoto"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50"
      @click.self="closePreview"
    >
      <img
        :src="`${API_BASE}/${previewPhoto.file_path}`"
        alt="Просмотр фото"
        class="max-h-[90vh] max-w-[90vw] rounded shadow-lg"
      />
      <button @click="closePreview" class="absolute top-4 right-4 text-white text-3xl font-bold">
        ✕
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const props = defineProps({
  photographerId: {
    type: Number,
    required: true
  }
})

const API_BASE = 'http://localhost:8000'
const photos = ref([])
const scrollContainer = ref(null)
const photoRefs = ref([])
const previewPhoto = ref(null)

const fetchPortfolioPhotos = async () => {
  try {
    const res = await axios.get(
      `${API_BASE}/portfolio_items/item_by_photographer/${props.photographerId}`
    )
    photos.value = res.data.flatMap((item) => item.photos || [])
    await nextTick()
    photoRefs.value = photoRefs.value.slice(0, photos.value.length)
  } catch (error) {
    console.error('Ошибка при загрузке портфолио:', error)
  }
}

const scrollRight = () => {
  const container = scrollContainer.value
  if (!container || photoRefs.value.length === 0) return

  const containerLeft = container.scrollLeft

  for (const photo of photoRefs.value) {
    const photoLeft = photo.offsetLeft
    const photoStyle = getComputedStyle(photo)
    const marginLeft = parseFloat(photoStyle.marginLeft)
    const marginRight = parseFloat(photoStyle.marginRight)
    const totalOffset = photoLeft - marginLeft

    if (totalOffset > containerLeft + 5) {
      const scrollAmount = photo.offsetWidth + marginLeft + marginRight
      container.scrollTo({
        left: containerLeft + scrollAmount,
        behavior: 'smooth'
      })
      break
    }
  }
}

const scrollLeft = () => {
  const container = scrollContainer.value
  if (!container || photoRefs.value.length === 0) return

  const containerLeft = container.scrollLeft

  for (let i = photoRefs.value.length - 1; i >= 0; i--) {
    const photo = photoRefs.value[i]
    const photoLeft = photo.offsetLeft
    const photoStyle = getComputedStyle(photo)
    const marginLeft = parseFloat(photoStyle.marginLeft)
    const marginRight = parseFloat(photoStyle.marginRight)
    const totalOffset = photoLeft - marginLeft

    if (totalOffset + 5 < containerLeft) {
      const scrollAmount = photo.offsetWidth + marginLeft + marginRight
      container.scrollTo({
        left: containerLeft - scrollAmount,
        behavior: 'smooth'
      })
      break
    }
  }
}

const openPreview = (photo) => {
  previewPhoto.value = photo
}

const closePreview = () => {
  previewPhoto.value = null
}

onMounted(fetchPortfolioPhotos)
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
