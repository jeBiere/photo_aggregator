<template>
  <div class="relative w-full m-8 p-8 rounded-3xl bg-white overflow-hidden mx-auto">
    <div class="mb-5">
      <h1 class="text-3xl text-slate-600 text-center uppercase mx-10 border-b-2">Registration</h1>
    </div>

    <div
      class="flex transition-transform duration-500 ease-in-out w-[205%]"
      :style="{ transform: `translateX(-${(step - 1) * 50}%)` }"
    >
      <!-- Шаг 1: Регистрация пользователя -->
      <form @submit.prevent="handleStepOne" class="w-1/2 flex flex-col space-y-8 mt-8 pr-4">
        <InputField v-model="user.firstName" type="text" placeholder="First Name" />
        <InputField v-model="user.lastName" type="text" placeholder="Last Name" />
        <InputField v-model="user.login" type="text" placeholder="Login" />
        <InputField v-model="user.email" type="text" placeholder="Email" />
        <InputField v-model="user.phone" type="text" placeholder="Phone" />
        <InputField v-model="user.city" type="text" placeholder="City" />
        <InputField v-model="user.password" type="password" placeholder="Password" />
        <InputField v-model="user.confirmPassword" type="password" placeholder="Confirm Password" />

        <label class="flex items-center space-x-3 cursor-pointer select-none mt-2">
          <div class="relative">
            <input type="checkbox" v-model="isPhotographer" class="sr-only peer" />
            <div
              class="w-11 h-6 bg-gray-300 rounded-full peer peer-checked:bg-orange-400 transition-colors duration-300"
            ></div>
            <div
              class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow-md transform transition-transform duration-300 peer-checked:translate-x-5"
            ></div>
          </div>
          <span class="text-slate-700 font-medium">Я фотограф</span>
        </label>

        <div class="flex justify-center">
          <Button type="submit">
            <transition name="fade-slide" mode="out-in">
              <span :key="isPhotographer">{{ isPhotographer ? 'Next →' : 'Register' }}</span>
            </transition>
          </Button>
        </div>
      </form>

      <!-- Шаг 2: Информация о фотографе -->
      <form @submit.prevent="registerPhotographer" class="w-1/2 flex flex-col space-y-8 mt-8 pl-4">
        <h2 class="text-xl text-slate-700 text-center font-semibold mb-4">
          Заполните данные о себе
        </h2>

        <InputField v-model="photographer.description" type="text" placeholder="Описание" />
        <InputField
          v-model="photographer.experience_years"
          type="number"
          placeholder="Стаж (лет)"
        />
        <InputField v-model="photographer.price_per_hour" type="number" placeholder="Цена за час" />

        <div class="text-slate-600 font-semibold mt-4">Выберите специализации:</div>
        <div class="flex flex-wrap">
          <SelectableButton
            v-for="(spec, index) in specializations"
            :key="spec"
            :text="spec"
            :is-active="selectedSpecializations[index]"
            @update:isActive="(val) => (selectedSpecializations[index] = val)"
          />
        </div>

        <div class="flex justify-between">
          <Button label="← Назад" @click="step = 1" />
          <Button label="Зарегистрироваться" type="submit" />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import InputField from '../components/InputField.vue'
import Button from '../components/Button.vue'
import SelectableButton from '@/components/SelectableButton.vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const step = ref(1)
const isPhotographer = ref(false)

const specializations = ['Свадебная', 'Детская', 'Студийная', 'Портретная', 'Фэшн', 'Семейная']
const selectedSpecializations = ref(Array(specializations.length).fill(false))

const user = ref({
  firstName: '',
  lastName: '',
  login: '',
  email: '',
  phone: '',
  city: '',
  password: '',
  confirmPassword: ''
})

const photographer = ref({
  description: '',
  experience_years: '',
  price_per_hour: ''
})

const registerPhotographer = async () => {
  if (user.value.password !== user.value.confirmPassword) {
    alert('Пароли не совпадают')
    return
  }

  const userPayload = {
    first_name: user.value.firstName,
    last_name: user.value.lastName,
    login: user.value.login,
    email: user.value.email,
    phone: user.value.phone,
    city: user.value.city,
    password: user.value.password,
    role: 'photographer'
  }

  try {
    // Сначала регистрируем пользователя
    const res = await axios.post('http://localhost:8000/users/register', userPayload)
    const userId = res.data.user_id

    // Потом фотографа
    await axios.post('http://localhost:8000/photographers/', {
      user_id: userId,
      description: photographer.value.description,
      experience_years: Number(photographer.value.experience_years),
      city: user.value.city,
      price_per_hour: Number(photographer.value.price_per_hour)
    })

    alert('Фотограф зарегистрирован!')
    router.push('/login')
  } catch (error) {
    alert('Ошибка при регистрации')
    console.error(error)
  }
}

const handleStepOne = () => {
  if (user.value.password !== user.value.confirmPassword) {
    alert('Пароли не совпадают')
    return
  }

  if (isPhotographer.value) {
    step.value = 2 
  } else {
    registerPhotographer()
  }
}
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 1s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-5px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(5px);
}
</style>
