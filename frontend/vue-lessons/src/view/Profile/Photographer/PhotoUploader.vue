<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50"
  >
    <div class="bg-white p-8 rounded-xl shadow-lg w-96">
      <h2 class="text-2xl font-semibold mb-4">Загрузить фотографии в портфолио</h2>

      <!-- Превью выбранных файлов -->
      <div v-if="imagePreviews.length > 0" class="mb-4">
        <div v-for="(preview, index) in imagePreviews" :key="index" class="mb-2">
          <img :src="preview" alt="Selected Image" class="w-full h-auto rounded-lg" />
        </div>
      </div>

      <!-- Форма для выбора файлов -->
      <input type="file" accept="image/*" multiple @change="handleFileSelect" class="mb-4" />

      <div class="flex justify-between">
        <!-- Кнопка закрытия модалки -->
        <button
          @click="close"
          class="bg-gray-300 text-gray-700 px-4 py-2 rounded-xl hover:bg-gray-400"
        >
          Отменить
        </button>

        <!-- Кнопка загрузки -->
        <button
          @click="uploadPhotos"
          :disabled="!selectedFiles.length"
          class="bg-orange-100 text-slate-600 px-4 py-2 rounded-xl hover:bg-orange-200 disabled:bg-gray-300"
        >
          Загрузить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const props = defineProps({
  open: Boolean,
  itemId: Number
})

const emit = defineEmits(['update:open', 'photos-uploaded'])

const authStore = useAuthStore()
const selectedFiles = ref([])
const imagePreviews = ref([])

const close = () => {
  emit('update:open', false)
}

const handleFileSelect = (event) => {
  const files = event.target.files
  if (files.length === 0) return

  selectedFiles.value = Array.from(files)
  imagePreviews.value = []

  Array.from(files).forEach((file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreviews.value.push(e.target.result)
    }
    reader.readAsDataURL(file)
  })
}

const uploadPhotos = async () => {
  if (selectedFiles.value.length === 0) return

  const formData = new FormData()
  selectedFiles.value.forEach((file) => {
    formData.append('files', file)
  })

  try {
    const response = await axios.post(
      `http://localhost:8000/portfolio_photos/${props.itemId}/photos`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    emit('photo-uploaded', response.data)
    close()
  } catch (error) {
    console.error('Ошибка загрузки фотографий:', error)
    alert('Не удалось загрузить фотографии.')
  }
}
</script>

<style scoped>
.fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
.bg-opacity-50 {
  background-color: rgba(0, 0, 0, 0.5);
}
.bg-white {
  background-color: white;
}
.p-8 {
  padding: 2rem;
}
.rounded-xl {
  border-radius: 1rem;
}
.shadow-lg {
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}
.w-96 {
  width: 24rem;
}
</style>
