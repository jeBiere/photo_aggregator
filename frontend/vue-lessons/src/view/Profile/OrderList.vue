<template>
  <div class="bg-gray-100 p-6 rounded-xl shadow-md">
    <h3 class="text-xl text-slate-600 mb-4">Orders</h3>

    <!-- Активные заказы -->
    <ul class="space-y-4 mb-6">
      <template v-if="activeOrders.length > 0">
        <component
          :is="OrderComponent"
          v-for="order in activeOrders"
          :key="order.order_id"
          :order="order"
          :userType="userType"
          @update-order="handleOrderUpdate"
        />
      </template>
      <p v-else class="text-2xl text-slate-400 text-center py-12 w-full">Здесь будут ваши заказы</p>
    </ul>

    <!-- Заголовок для завершённых заказов -->
    <div class="mt-6">
      <div
        class="flex items-center justify-between cursor-pointer select-none mb-4"
        @click="toggleCompleted"
      >
        <h4 class="text-xl text-slate-600">Completed Orders</h4>
        <svg
          :class="[
            'w-5 h-5 transform transition-transform duration-300',
            { 'rotate-180': showCompleted }
          ]"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </div>

      <!-- Список завершённых заказов -->
      <transition name="fade">
        <ul v-if="showCompleted" class="space-y-4">
          <template v-if="completedOrders.length > 0">
            <component
              :is="OrderComponent"
              v-for="order in completedOrders"
              :key="order.order_id"
              :order="order"
              :userType="userType"
              @update-order="handleOrderUpdate"
            />
          </template>
          <template v-else>
            <li class="text-sm text-slate-400 text-center py-12 w-full">Завершённых заказов нет.</li>
          </template>
        </ul>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  orders: { type: Array, required: true },
  OrderComponent: { type: Object, required: true },
  userType: { type: String, required: true }
})

const emit = defineEmits(['update-order'])

const statusOrder = {
  pending: 0,
  in_progress: 1,
  completed: 2,
  cancelled: 3
}

const sortedOrders = computed(() =>
  [...props.orders].sort((a, b) => statusOrder[a.status] - statusOrder[b.status])
)

const activeOrders = computed(() =>
  sortedOrders.value.filter((order) => ['pending', 'in_progress'].includes(order.status))
)
const completedOrders = computed(() =>
  sortedOrders.value.filter((order) => ['completed', 'cancelled'].includes(order.status))
)

const showCompleted = ref(false)
const toggleCompleted = () => {
  showCompleted.value = !showCompleted.value
}

const handleOrderUpdate = (updatedOrder) => {
  const orderIndex = props.orders.findIndex((order) => order.order_id === updatedOrder.order_id)
  if (orderIndex !== -1) {
    props.orders[orderIndex] = updatedOrder
  }
  emit('update-order', updatedOrder)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
