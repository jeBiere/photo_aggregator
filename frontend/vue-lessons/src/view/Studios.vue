<template>
  <div class="studios-page w-full mx-auto">
    <div class="studios-list w-full">
      <StudioCard
        class="w-full"
        v-for="studio in studios"
        :key="studio.studio_id"
        :studio="studio"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import StudioCard from './Studio/StudioCard.vue'

export default {
  name: 'StudiosList',
  components: { StudioCard },
  setup() {
    const studios = ref([])

    const fetchStudios = async () => {
      const response = await axios.get('http://localhost:8000/studios/')
      studios.value = response.data
    }

    onMounted(() => {
      fetchStudios()
    })

    return {
      studios
    }
  }
}
</script>

<style scoped>
.studios-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.studios-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
