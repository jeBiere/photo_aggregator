<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'CardList',
  props: {
    items: {
      type: Array,
      required: true
    },
    onClickAdd: {
      type: Function,
      required: false
    }
  }
})
</script>

<template>
  <div class="flex flex-wrap gap-10 mt-10 justify-center rounded-3xl" v-auto-animate>
    <slot v-for="item in items" :item="item" :onClickAdd="onClickAdd"></slot>
  </div>
</template>
