<template>
  <div class="selectable-button" :class="{ active: isActive }" @click="toggleActive">
    {{ text }}
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

// props
const props = defineProps({
  text: {
    type: String,
    required: true
  },
  isActive: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:isActive'])

const toggleActive = () => {
  emit('update:isActive', !props.isActive)
}
</script>

<style scoped>
.selectable-button {
  display: inline-block;
  background-color: #dcdcdc;
  color: #333;
  padding: 8px 16px;
  border-radius: 20px; /* Закругляем только края */
  margin: 5px;
  cursor: pointer;
  text-align: center;
  font-size: 14px;
  transition: background-color 0.3s ease;
  border-top-left-radius: 20px; /* Закругление только левого верхнего угла */
  border-bottom-left-radius: 20px; /* Закругление только левого нижнего угла */
  border-top-right-radius: 20px; /* Прямой угол справа сверху */
  border-bottom-right-radius: 20px; /* Прямой угол справа снизу */
}

.selectable-button.active {
  background-color: #ffedd5; /* Бежевый цвет при активном состоянии */
}
</style>
