<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl">
    <div class="mb-5">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">Photographers</h1>
    </div>

    <CardList :items="photographers" :onClickAdd="onClickAdd">
      <template v-slot:default="{ item, onClickAdd }">
        <Card
          :key="item._id"
          :title="item.name"
          :price="item.expirience"
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

const photographers = ref([])

const fetchPhotographers = async () => {
  try {
    const response = await axios.get('http://localhost:8000/photographers')
    photographers.value = response.data
  } catch (error) {
    console.error('Error fetching photographers:', error)
  }
}

onMounted(() => {
  fetchPhotographers()
})

const onClickAdd = () => {
  console.log('Added to cart')
}
</script>

<style scoped></style>
