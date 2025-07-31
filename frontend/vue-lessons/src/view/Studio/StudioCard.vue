<template>
  <div class="bg-white rounded-2xl shadow-md p-6 mb-6 w-full">
    <!-- Верхняя часть: информация -->
    <div class="flex justify-between items-start w-full">
      <!-- Левая часть: текстовая информация -->
      <div class="flex-grow pr-6">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">
          {{ studio.studio_name }}
        </h2>

        <div class="text-gray-700 space-y-2 text-sm">
          <p><span class="font-medium">📍 Адрес:</span> {{ studio.address || 'Не указан' }}</p>
          <p><span class="font-medium">📞 Телефон:</span> {{ studio.phone || 'Не указан' }}</p>
          <p><span class="font-medium">📧 Email:</span> {{ studio.email || 'Не указан' }}</p>
          <p>
            <span class="font-medium">🌐 Сайт:</span>
            <a
              v-if="studio.website_url"
              :href="studio.website_url"
              target="_blank"
              class="text-blue-500 underline"
            >
              {{ studio.website_url }}
            </a>
            <span v-else>Не указан</span>
          </p>
        </div>
      </div>

      <!-- Правая часть: кнопка -->
      <div class="flex flex-col items-end">
        <button
          class="bg-orange-100 hover:bg-orange-200 transition-colors px-4 py-2 rounded-xl text-sm text-gray-800"
          @click="showDetails"
        >
          Подробнее
        </button>
      </div>
    </div>

    <!-- Нижняя часть: фотография и статус -->
    <div class="flex flex-col items-center mt-6">
      <img
        :src="logoUrl"
        alt="studio logo"
        class="w-40 h-40 object-cover rounded-2xl mb-2"
      />
      <div class="text-sm text-center text-gray-600">
        <p>💸 {{ studio.base_price_per_hour }} ₽/час</p>
        <p :class="studio.is_active ? 'text-green-500' : 'text-red-500'">
          {{ studio.is_active ? 'Активна' : 'Неактивна' }}
        </p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  studio: Object
})

const logoUrl = computed(() => props.studio.profile_picture_url || '/studio-default.png')

const showModal = ref(false)

const showDetails = () => {
  showModal.value = true
  // Можно подключить StudioCardFull.vue при необходимости
}
</script>
