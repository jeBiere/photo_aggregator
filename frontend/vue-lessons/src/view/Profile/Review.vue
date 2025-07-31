<template>
  <div class="min-w-45 max-w-45 bg-white p-6 rounded-lg shadow-lg flex flex-col mb-5">
    <div class="rating-badge mb-4 self-start inline-block">{{ review.rating }} / 5</div>
    <p class="text-slate-500 mb-2 italic">"{{ review.comment }}"</p>
    <p class="text-sm text-slate-400">Order ID: {{ review.order_id }}</p>
    <p class="text-sm text-slate-400">
      {{ userType === 'client' ? 'Photographer ID' : 'Client ID' }}:
      {{ userType === 'client' ? review.photographer_id : review.client_id }}
    </p>
    <p class="text-sm text-slate-400">
      Date: {{ new Date(review.created_at).toLocaleDateString() }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  review: Object,
  userType: { type: String, required: true }
})
</script>

<style scoped>
.min-w-45 {
  min-width: 45%;
}
.max-w-45 {
  max-width: 45%;
}

.rating-badge {
  background-color: #ffedd5;
  border-radius: 9999px;
  padding: 6px 14px;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  white-space: nowrap;
}
</style>
