<template>
  <div class="relative group w-60 h-60">
    <img
      :src="avatarSrc"
      alt="User Avatar"
      class="rounded-full border-4 border-orange-200 w-full h-full object-cover cursor-pointer"
      @click="$emit('edit')"
    />
    <button
      class="absolute inset-0 bg-black bg-opacity-50 text-white text-xs rounded-full opacity-0 group-hover:opacity-100 flex items-center justify-center transition"
      @click="$emit('edit')"
    >
      Изменить
    </button>
  </div>
</template>

<script setup>
import { computed, defineEmits, defineProps } from 'vue'

const props = defineProps({
  avatarUrl: String
})

const avatarSrc = computed(() => {
  return props.avatarUrl ? `http://localhost:8000${props.avatarUrl}` : '/portrait.svg' // файл должен лежать в public/portrait.svg
})

defineEmits(['edit'])
</script>
