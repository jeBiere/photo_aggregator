<template>
  <div class="photographers-page w-full mx-auto">
    <FiltersCard @apply-filters="handleFiltersChange" />

    <!-- Блок с карточками -->
    <div v-if="isLoading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="photographers-list w-full">
      <PhotographerCard
        class="w-full"
        v-for="photographer in photographers"
        :key="photographer.photographer_id"
        :photographer="photographer"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import PhotographerCard from './Photographers/PhotographerCard.vue'
import FiltersCard from './Photographers/Filters.vue'

export default {
  name: 'PhotographersList',
  components: { PhotographerCard, FiltersCard },
  setup() {
    const photographers = ref([])
    const isLoading = ref(true)
    const error = ref(null)

    const handleFiltersChange = async (filters) => {
      await fetchPhotographers(filters)
    }

    const fetchPhotographers = async (filters = {}) => {
      isLoading.value = true
      error.value = null

      try {
        const response = await axios.post('http://localhost:8000/photographers/recommendations/', {
          city: filters.city || '',
          specializations: filters.specializations || [],
          max_price: filters.max_price || 15000
        })

        photographers.value = await Promise.all(
          response.data.map(async (photographer) => {
            const userResponse = await axios.get(
              `http://localhost:8000/users/user_by_id/${photographer.user_id}`
            )
            const specsResponse = await axios.get(
              `http://localhost:8000/photographers/${photographer.photographer_id}/specializations`
            )

            return {
              ...photographer,
              user: userResponse.data,
              specializations: specsResponse.data
            }
          })
        )
      } catch (e) {
        error.value = 'Ошибка при загрузке данных.'
        console.error(e)
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      fetchPhotographers()
    })

    return {
      photographers,
      isLoading,
      error,
      handleFiltersChange
    }
  }
}
</script>

<style scoped>
.photographers-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.loading,
.error {
  font-size: 18px;
  color: #666;
  margin-top: 20px;
}

.photographers-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
