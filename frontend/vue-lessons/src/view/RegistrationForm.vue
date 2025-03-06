<template>
  <div class="flex flex-col bg-white w-full m-8 p-8 rounded-3xl">
    <div class="mb-5">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">Registration</h1>
    </div>
    <form @submit.prevent="registerUser" class="flex flex-col space-y-8 items-evenly mt-8">
      <InputField v-model="user.firstName" type="text" placeholder="First Name" />
      <InputField v-model="user.lastName" type="text" placeholder="Last Name" />
      <InputField v-model="user.login" type="text" placeholder="Login" />
      <InputField v-model="user.email" type="text" placeholder="Email" />
      <InputField v-model="user.city" type="text" placeholder="City" />
      <InputField v-model="user.password" type="password" placeholder="Password" />
      <InputField v-model="user.confirmPassword" type="password" placeholder="Confirm Password" />
      <div class="flex justify-center">
        <Button type="submit" label="Register" />
      </div>
    </form>
  </div>
</template>

<script setup>
import Button from '../components/Button.vue'
import InputField from '../components/InputField.vue'
import { ref } from 'vue'
import axios from 'axios'

const user = ref({
  firstName: '',
  lastName: '',
  login: '',
  email: '',
  city: '',
  password: '',
  confirmPassword: ''
})

const registerUser = async () => {
  if (user.value.password !== user.value.confirmPassword) {
    alert('Passwords do not match')
    return
  }
  alert(user.value)
  try {
    const response = await axios.post('http://localhost:8000/users/', {
      login: user.value.login,
      password: user.value.password,
      email: user.value.email
    })
    alert('User registered successfully')
  } catch (error) {
    console.error(error)
    alert('Error registering user')
  }
}
</script>
