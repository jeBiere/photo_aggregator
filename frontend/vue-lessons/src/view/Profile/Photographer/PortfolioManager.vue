<template>
  <div class="mt-10">
    <h2 class="text-2xl font-bold text-slate-700 mb-4">My Portfolio</h2>

    <div v-if="items.length === 0" class="text-slate-400 mb-4">No portfolio items found.</div>

    <div v-else class="flex flex-col gap-6 w-full">
      <div
        v-for="item in items"
        :key="item.item_id"
        class="bg-gray-50 w-full p-6 rounded-xl shadow"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-semibold text-slate-600 mb-2">{{ item.category }}</h3>
            <p class="text-slate-500 mb-4">{{ item.description }}</p>
          </div>
          <!-- Кнопка для открытия модалки загрузки фотографий -->
          <button
            class="bg-orange-100 hover:bg-orange-200 text-slate-600 transition ease-in-out duration-300 px-4 py-2 rounded-xl shadow"
            @click="openUploadModal(item.item_id)"
          >
            Загрузить фото
          </button>
        </div>

        <!-- Галерея с горизонтальной прокруткой -->
        <div class="flex gap-4 overflow-x-auto pb-2">
          <img
            v-for="photo in item.photos"
            :key="photo.photo_id"
            :src="`${API_BASE}/${photo.file_path}`"
            alt="Portfolio Photo"
            class="h-40 w-auto rounded-lg object-cover flex-shrink-0"
          />
        </div>
      </div>
    </div>

    <!-- Кнопка добавления нового портфолио айтема -->
    <div class="mt-8 flex justify-center">
      <button
        class="bg-orange-100 hover:bg-orange-200 text-slate-600 px-6 py-3 transition ease-in-out duration-300 rounded-2xl shadow"
        @click="isAddModalOpen = true"
      >
        Добавить портфолио-айтем
      </button>
    </div>

    <!-- Модалка для загрузки фотографий -->
    <PhotoUploader
      v-if="isUploadModalOpen"
      :open="isUploadModalOpen"
      :item-id="currentItemId"
      @update:open="isUploadModalOpen = $event"
      @photo-uploaded="onPhotoUploaded"
    />

    <PortfolioItemModal
      v-if="isAddModalOpen"
      :open="isAddModalOpen"
      @update:open="isAddModalOpen = $event"
      @item-created="onNewItemCreated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import PhotoUploader from './PhotoUploader.vue'
import PortfolioItemModal from './PortfolioItemModal.vue'

const API_BASE = 'http://localhost:8000'

const isAddModalOpen = ref(false)

const authStore = useAuthStore()
const items = ref([])
const isUploadModalOpen = ref(false)
const currentItemId = ref(null)

const onNewItemCreated = (item) => {
  items.value.push(item)
}

const loadPortfolio = async () => {
  try {
    const response = await axios.get(`${API_BASE}/portfolio_items/me`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    items.value = response.data
  } catch (error) {
    console.error('Failed to load portfolio items:', error)
  }
}

const openUploadModal = (itemId) => {
  currentItemId.value = itemId
  isUploadModalOpen.value = true
}

const onPhotoUploaded = async (newPhoto) => {
  await reloadItemPhotos(currentItemId.value)
  isUploadModalOpen.value = false
}

const reloadItemPhotos = async (itemId) => {
  try {
    const response = await axios.get(`${API_BASE}/portfolio_items/item_by_id/${itemId}`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    const updatedItem = items.value.find((item) => item.item_id === itemId)
    if (updatedItem) {
      updatedItem.photos = response.data.photos
    }
  } catch (error) {
    console.error('Ошибка при обновлении фото айтема:', error)
  }
}

onMounted(loadPortfolio)
</script>
