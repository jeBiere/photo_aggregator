<!-- components/AddPortfolioItemModal.vue -->
<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    @click.self="$emit('update:open', false)"
  >
    <div class="bg-white rounded-xl shadow-xl p-6 w-[90%] max-w-xl">
      <h3 class="text-xl font-bold text-slate-700 mb-4">Добавить портфолио-айтем</h3>

      <label class="block mb-2 text-slate-600">Тип съёмки</label>
      <Select v-model="category" :options="categoryOptions" placeholder="Выберите тип съёмки" />

      <label class="block mb-2 text-slate-600">Описание</label>
      <InputField
        v-model="description"
        placeholder="Особые пожелания"
        :isTextarea="true"
        :rows="4"
      />

      <div class="mt-4 flex justify-end gap-2">
        <button
          class="px-4 py-2 rounded-lg bg-slate-300 hover:bg-slate-400 text-white"
          @click="$emit('update:open', false)"
        >
          Отмена
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-orange-100 hover:bg-orange-200 text-slate-700"
          :disabled="!category"
          @click="createItem"
        >
          Добавить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import Select from '@/components/Select.vue'
import InputField from '@/components/InputField.vue'

const props = defineProps({
  open: Boolean
})
const emit = defineEmits(['update:open', 'item-created'])

const category = ref('')
const description = ref('')

const API_BASE = 'http://localhost:8000'
const authStore = useAuthStore()

const categoryOptions = [
  { value: 'portrait', label: 'Портретная' },
  { value: 'wedding', label: 'Свадебная' },
  { value: 'family', label: 'Семейная' },
  { value: 'children', label: 'Детская' },
  { value: 'event', label: 'Мероприятия' },
  { value: 'fashion', label: 'Фэшн' },
  { value: 'boudoir', label: 'Будуарная' },
  { value: 'sports', label: 'Спортивная' },
  { value: 'studio', label: 'В студии' },
  { value: 'on_location', label: 'На выезде' },
  { value: 'product', label: 'Предметная' },
  { value: 'love_story', label: 'Love Story' }
]

const createItem = async () => {
  try {
    const res = await axios.post(
      `${API_BASE}/portfolio_items/`,
      {
        category: category.value,
        description: description.value
      },
      {
        headers: { Authorization: `Bearer ${authStore.token}` }
      }
    )

    emit('item-created', {
      item_id: res.data.item_id,
      category: res.data.category,
      description: res.data.description,
      photos: []
    })

    emit('update:open', false)
  } catch (err) {
    console.error('Ошибка при создании айтема:', err)
  }
}

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      category.value = ''
      description.value = ''
    }
  }
)
</script>
