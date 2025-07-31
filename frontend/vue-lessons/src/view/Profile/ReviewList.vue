<template>
  <div
    class="bg-gray-100 p-6 rounded-xl shadow-md mt-8 min-h-[200px] flex flex-col justify-center items-center"
  >
    <h3 class="text-xl text-slate-600 mb-4 self-start">Reviews</h3>

    <template v-if="reviews && reviews.length > 0">
      <div class="relative w-full">
        <!-- Кнопка влево -->
        <button
          class="absolute hover:bg-orange-200 transition ease-in-out duration-300 left-0 top-1/2 transform -translate-y-1/2 bg-[#ffedd5] rounded-full w-10 h-10 flex items-center justify-center shadow-md z-10"
          @click="scroll('left')"
        >
          ‹
        </button>

        <!-- Список отзывов -->
        <div ref="container" class="flex gap-6 overflow-x-auto scrollbar-hide px-12">
          <component
            :is="ReviewComponent"
            v-for="review in reviews"
            :key="review.review_id"
            :review="review"
            :userType="userType"
          />
        </div>

        <!-- Кнопка вправо -->
        <button
          class="absolute hover:bg-orange-200 transition ease-in-out duration-300 right-0 top-1/2 transform -translate-y-1/2 bg-[#ffedd5] rounded-full w-10 h-10 flex items-center justify-center shadow-md z-10"
          @click="scroll('right')"
        >
          ›
        </button>
      </div>
    </template>

    <template v-else>
      <div class="text-2xl text-slate-400 text-center py-12 w-full">Здесь будут ваши отзывы</div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  reviews: Array,
  ReviewComponent: {
    type: Object,
    required: true
  },
  userType: {
    type: String,
    required: true
  }
})

const container = ref(null)

const scroll = (direction) => {
  if (!container.value) return
  const scrollAmount = container.value.offsetWidth * 0.5
  container.value.scrollBy({
    left: direction === 'left' ? -scrollAmount : scrollAmount,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
