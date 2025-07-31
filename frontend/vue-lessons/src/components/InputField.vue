<template>
  <component
    :is="isTextarea ? 'textarea' : 'input'"
    :type="isTextarea ? undefined : type"
    class="standard-input bg-white"
    :class="isTextarea ? 'text-left placeholder:text-left' : 'text-center placeholder:text-center'"
    :placeholder="placeholder"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    :rows="isTextarea ? rows : undefined"
  />
</template>

<style scoped>
.standard-input {
  @apply shadow-inner p-2 rounded-lg w-full 
  border border-slate-100
  bg-white
  focus:outline-none
  focus:border-orange-100
  font-sans
  transition ease-in-out duration-300;

  text-align: center;
  resize: none;
}
</style>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'text'
  },
  placeholder: {
    type: String,
    default: ''
  },
  modelValue: {
    type: String,
    default: ''
  },
  isTextarea: {
    type: Boolean,
    default: false
  },
  rows: {
    type: Number,
    default: 4 // можно изменить при необходимости
  }
})
</script>
