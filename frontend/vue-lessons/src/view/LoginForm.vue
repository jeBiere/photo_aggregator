<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl">
    <div class="mb-5">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">Login</h1>
    </div>
    <form @submit.prevent="loginUser" class="flex flex-col space-y-8 items-evenly mt-8">
      <InputField v-model="user.login" type="text" placeholder="Login" />
      <InputField v-model="user.password" type="password" placeholder="Password" />

      <div class="flex justify-center">
        <Button type="submit" label="Login" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRoute } from 'vue-router'
import axios from 'axios'
import InputField from '../components/InputField.vue'
import Button from '../components/Button.vue'

const authStore = useAuthStore()
const user = ref({
  username: '',
  password: ''
})

const loginUser = async () => {
  if (!validateForm()) {
    alert('Please fill in all fields correctly.')
    return
  }
  alert(user.value.login)
  try {
    const response = await axios.post('http://localhost:8000/users/login', {
      password: user.value.password,
      username: user.value.login
    })

    const token = response.data.access_token
    authStore.setToken(token)

    alert('User logged in successfully')
  } catch (error) {
    console.error(error)
    alert('Error logging in')
  }
}

const validateForm = () => {
  return user.value.login.trim() !== '' && user.value.password.trim() !== ''
}
</script>

<style scoped></style>
