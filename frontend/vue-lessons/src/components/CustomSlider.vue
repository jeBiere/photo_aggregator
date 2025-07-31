<template>
  <div class="w-full py-6 flex flex-col items-center">
    <!-- Тонкая бежевая линия с делениями -->
    <div ref="trackRef" class="relative w-full max-w-md h-1 bg-slate-200 rounded-full">
      <!-- Деления -->
      <div
        v-for="n in 5"
        :key="n"
        class="absolute top-1/2 w-3 h-3 bg-slate-200 rounded-full"
        :style="{ left: `${(n - 1) * 25}%`, transform: 'translateX(-50%) translateY(-50%)' }"
      ></div>

      <!-- Кружок -->
      <div
        ref="thumbRef"
        class="relative z-10 w-8 h-8 text-white text-lg font-bold flex items-center justify-center rounded-full cursor-pointer transition-transform duration-200 select-none"
        :class="colorClass"
        :style="{ left: `${sliderPos}%`, top: '1px', transform: 'translate(-50%, -43%)' }"
        @mousedown="startDrag"
      >
        {{ rating }}
        <!-- Элемент для кольцевой анимации -->
        <div v-if="rating === 5 && !isDragging" class="circle-wave"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.circle-wave {
  position: absolute;
  width: 30%;
  height: 30%;
  border-radius: 50%;
  border: 1px solid rgb(0, 212, 146);
  z-index: 0;
  pointer-events: none;
  animation: waveEffect 1s ease-in-out forwards;
}

@keyframes waveEffect {
  0% {
    z-index: -1;
    widows: 30%;
    height: 30%;
    opacity: 0;
  }
  60% {
    z-index: -1;
    opacity: 1;
  }
  80% {
    z-index: -1;
    opacity: 0.6;
  }
  100% {
    z-index: -1;
    width: 250%;
    height: 250%;
    opacity: 0;
  }
}
</style>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'

const rating = defineModel('rating', { default: 0 }) // для v-model:rating
const sliderPos = ref(0)
const isDragging = ref(false)

const trackRef = ref(null)
const thumbRef = ref(null)

const colorClass = computed(() => {
  switch (rating.value) {
    case 1:
      return 'bg-red-200'
    case 2:
      return 'bg-orange-200'
    case 3:
      return 'bg-amber-200'
    case 4:
      return 'bg-lime-200'
    case 5:
      return 'bg-emerald-300'
    default:
      return 'bg-slate-400'
  }
})

const updateSliderPosition = (value) => {
  const clamped = Math.min(Math.max(value, 1), 5)
  rating.value = clamped
  targetPos.value = (clamped - 1) * 25
  if (!animationFrame) animateThumb()
}

const triggerAnimation = () => {
  const el = thumbRef.value
  el.animate(
    [
      { transform: 'translate(-50%, -43%) scale(1)' },
      { transform: 'translate(-50%, -43%) scale(1.1)' },
      { transform: 'translate(-50%, -43%) scale(1)' }
    ],
    {
      duration: 300,
      easing: 'ease-in-out'
    }
  )

  if (rating.value === 5) {
    // Запускаем волновую анимацию
    const waveEl = thumbRef.value.querySelector('.circle-wave')
    waveEl?.classList.add('active')
  }
}

const targetPos = ref(0)
let animationFrame = null

const animateThumb = () => {
  const diff = targetPos.value - sliderPos.value
  if (Math.abs(diff) > 0.1) {
    sliderPos.value += diff * 0.1 // коэффициент сопротивления
    animationFrame = requestAnimationFrame(animateThumb)
  } else {
    sliderPos.value = targetPos.value
    cancelAnimationFrame(animationFrame)
    animationFrame = null
  }
}

const startDrag = () => {
  isDragging.value = true
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', stopDrag)
}

const stopDrag = () => {
  isDragging.value = false
  snapToNearest()
  triggerAnimation()
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', stopDrag)
}

const onMouseMove = (e) => {
  if (!isDragging.value) return
  const track = trackRef.value
  const rect = track.getBoundingClientRect()
  const offsetX = Math.min(Math.max(e.clientX - rect.left, 0), rect.width)
  let percent = (offsetX / rect.width) * 100

  // Притягивание к ближайшему шагу
  const steps = [0, 25, 50, 75, 100]
  const snapThreshold = 15

  for (const step of steps) {
    if (Math.abs(percent - step) < snapThreshold) {
      percent = step
      break
    }
  }

  targetPos.value = percent

  const newRating = Math.round(percent / 25) + 1
  if (newRating !== rating.value) {
    rating.value = newRating
  }

  if (!animationFrame) animateThumb()
}
const snapToNearest = () => {
  const value = Math.round(sliderPos.value / 25) + 1
  if (value === 5) triggerAnimation()
  updateSliderPosition(value)
}

onMounted(() => updateSliderPosition(rating.value))
watch(rating, (val) => {
  updateSliderPosition(val)
})
</script>
