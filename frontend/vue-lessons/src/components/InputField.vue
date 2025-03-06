<template>
  <input
    :type="type"
    class="standard-input"
    :placeholder="placeholder"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<style scoped>
.standard-input {
  @apply shadow-inner p-2 rounded-lg w-full 
  placeholder:text-center 
  border border-slate-100 
  focus:outline-none
  focus:border-orange-100
  font-sans
  text-center 
  transition ease-in-out duration-300;
}
</style>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  type: {
    type: String
  },
  placeholder: {
    type: String
  },
  modelValue: {
    type: String,
    default: ''
  }
})
</script>
