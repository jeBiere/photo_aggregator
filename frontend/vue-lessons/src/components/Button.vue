<template>
  <button class="standard-button bg-orange-100" :type="type">
    <slot>{{ label }}</slot>
  </button>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'button'
  }
})
</script>

<style>
.standard-button {
  @apply bg-orange-100 hover:bg-orange-200
        text-slate-600 font-bold 
        py-2 px-4 rounded-3xl mt-8 
        transition ease-in-out duration-300
        uppercase;
}
</style>
