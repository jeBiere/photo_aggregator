<template>
  <div class="relative inline-block w-full max-w-xs">
    <!-- Кнопка-селект -->
    <button
      @click="toggleDropdown"
      class="rounded-2xl bg-orange-50 text-slate-600 px-4 py-2 text-left shadow hover:bg-orange-100 transition-all duration-300 my-2 w-full"
    >
      {{ selectedLabel }}
    </button>

    <!-- Dropdown -->
    <transition name="fade-slide">
      <ul
        v-if="isOpen"
        class="absolute z-10 mt-2 w-full rounded-2xl bg-white shadow-lg ring-1 ring-orange-100 max-h-48 overflow-y-auto"
      >
        <li
          v-for="(option, index) in options"
          :key="index"
          @click="selectOption(option)"
          class="cursor-pointer px-4 py-2 rounded-2xl hover:bg-orange-100 transition-all duration-200"
          :class="{ 'bg-orange-100 font-semibold': option.value === modelValue }"
        >
          {{ option.label }}
        </li>
      </ul>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  options: {
    type: Array,
    required: true,
    default: () => []
  },
  modelValue: {
    type: [String, Number, Object],
    default: null
  },
  placeholder: {
    type: String,
    default: 'Выбрать...'
  }
})

const emit = defineEmits(['update:modelValue'])

const isOpen = ref(false)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  isOpen.value = false
}

const selectedLabel = computed(() => {
  const found = props.options.find((opt) => opt.value === props.modelValue)
  return found ? found.label : props.placeholder
})
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-5px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* Кастомный скроллбар (необязательно) */
ul::-webkit-scrollbar {
  width: 6px;
}

ul::-webkit-scrollbar-thumb {
  background-color: #f4e1d2;
  border-radius: 10px;
}
</style>
