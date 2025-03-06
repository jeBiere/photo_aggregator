<template>
  <div>
    <CardList :items="services" :onClickAdd="onClickAdd">
      <template v-slot:default="{ item, onClickAdd }">
        <Card
          :key="item._id"
          :title="item.service_type"
          :price="item.price"
          :isAdded="false"
          :onClickAdd="onClickAdd"
        />
      </template>
    </CardList>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import CardList from '../components/CardList.vue'
import Card from '../components/Card.vue'

const services = ref([])

const fetchServices = async () => {
  try {
    const response = await axios.get('http://localhost:8000/services')
    services.value = response.data
  } catch (error) {
    console.error('Error fetching services:', error)
  }
}

const onClickAdd = () => {
  console.log('Added to cart')
}

onMounted(fetchServices)
</script>
