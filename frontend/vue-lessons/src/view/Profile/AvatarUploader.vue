<template>
  <Teleport to="body">
    <div
      v-if="open"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
      @click.self="close"
    >
      <div class="bg-white p-6 rounded-xl shadow-xl w-full max-w-md relative">
        <button class="absolute top-2 right-2 text-slate-400 hover:text-slate-700" @click="close">
          ✕
        </button>
        <h2 class="text-lg mb-4 text-slate-700 font-bold">Загрузить аватар</h2>

        <!-- Шаг 1: Выбор файла -->
        <div v-if="!selectedFile" class="space-y-4">
          <input
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
          />
          <p class="text-sm text-slate-500">Выберите изображение для загрузки</p>
        </div>

        <!-- Шаг 2: Редактирование изображения -->
        <div v-else class="space-y-4">
          <div class="cropper-container">
            <img
              id="image-to-crop"
              class="max-w-full max-h-[400px]"
              :src="imagePreview"
              alt="Preview"
            />
          </div>

          <div class="flex flex-wrap gap-2 justify-between items-center">
            <button
              @click="resetCrop"
              class="px-3 py-1.5 text-sm bg-gray-100 rounded hover:bg-gray-200"
            >
              Сбросить
            </button>
            <button
              @click="rotateLeft"
              class="px-3 py-1.5 text-sm bg-gray-100 rounded hover:bg-gray-200"
            >
              ↺ Повернуть влево
            </button>
            <button
              @click="rotateRight"
              class="px-3 py-1.5 text-sm bg-gray-100 rounded hover:bg-gray-200"
            >
              ↻ Повернуть вправо
            </button>
            <button
              @click="cropAndUpload"
              class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onBeforeUnmount, nextTick } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'

const props = defineProps({
  open: Boolean
})

const emit = defineEmits(['update:open', 'avatar-updated'])

const authStore = useAuthStore()
const selectedFile = ref(null)
const imagePreview = ref('')
const cropperInstance = ref(null)

const close = () => {
  emit('update:open', false)
  resetCropper()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (!file) return

  resetCropper()
  selectedFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreview.value = e.target.result
    nextTick(() => initCropper())
  }
  reader.readAsDataURL(file)
}

const initCropper = () => {
  destroyCropper()

  const image = document.getElementById('image-to-crop')
  if (image) {
    cropperInstance.value = new Cropper(image, {
      aspectRatio: 1,
      viewMode: 1,
      autoCropArea: 0.8,
      movable: true,
      rotatable: true,
      scalable: true,
      zoomable: true,
      cropBoxMovable: true,
      cropBoxResizable: true,
      dragMode: 'move',
      ready() {
        cropperInstance.value.crop()
      }
    })
  }
}

const destroyCropper = () => {
  if (cropperInstance.value) {
    cropperInstance.value.destroy()
    cropperInstance.value = null
  }
}

const resetCropper = () => {
  destroyCropper()
  selectedFile.value = null
  imagePreview.value = ''
}

const rotateLeft = () => {
  if (cropperInstance.value) {
    cropperInstance.value.rotate(-90)
  }
}

const rotateRight = () => {
  if (cropperInstance.value) {
    cropperInstance.value.rotate(90)
  }
}

const cropAndUpload = async () => {
  if (!cropperInstance.value) return

  cropperInstance.value
    .getCroppedCanvas({
      width: 512,
      height: 512,
      fillColor: '#fff',
      imageSmoothingEnabled: true,
      imageSmoothingQuality: 'high'
    })
    .toBlob(
      async (blob) => {
        const formData = new FormData()
        formData.append('file', blob, 'avatar.png')

        try {
          const { data } = await axios.post('http://localhost:8000/users/avatar', formData, {
            headers: {
              Authorization: `Bearer ${authStore.token}`,
              'Content-Type': 'multipart/form-data'
            }
          })
          emit('avatar-updated', data.avatar_url)
          close()
        } catch (error) {
          console.error('Ошибка загрузки аватарки:', error)
          alert('Не удалось загрузить аватар.')
        }
      },
      'image/png',
      0.9
    )
}

onBeforeUnmount(() => {
  destroyCropper()
})
</script>

<style>
.cropper-container {
  width: 100%;
  height: 400px;
  margin-bottom: 1rem;
}

.cropper-view-box {
  outline: 1px solid #39f;
  outline-color: rgba(51, 153, 255, 0.75);
}

.cropper-face {
  background-color: inherit !important;
}

.cropper-line {
  background-color: #39f;
}

.cropper-point {
  background-color: #39f;
  width: 8px;
  height: 8px;
  opacity: 1;
}

.cropper-point.point-se {
  right: -4px;
  bottom: -4px;
}
</style>
