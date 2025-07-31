<template>
  <div class="bg-white p-6 rounded-3xl mt-4 w-full flex items-center justify-between">
    <div class="bg-orange-100 text-center p-2 rounded-xl">
      <p>@Photo_aggr</p>
    </div>

    <nav class="flex-1 flex justify-around items-center ml-6 px-2 gap-2 flex-wrap">
      <div class="header-element">
        <router-link to="/about">О нас</router-link>
      </div>

      <template v-if="isLoggedIn">
        <div class="header-element">
          <router-link to="/photographers">Фотографы</router-link>
        </div>
        <div class="header-element">
          <router-link to="/studios">Студии</router-link>
        </div>
        <div class="header-element">
          <router-link to="/services">Услуги</router-link>
        </div>
        <div class="header-element">
          <router-link to="/profile">Профиль</router-link>
        </div>
        <div class="header-element cursor-pointer" @click="handleLogout">Выйти</div>
      </template>

      <template v-else>
        <div class="header-element">
          <router-link to="/registration">Регистрация</router-link>
        </div>
        <div class="header-element">
          <router-link to="/login">Войти</router-link>
        </div>
      </template>
    </nav>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const isLoggedIn = computed(() => authStore.isAuthenticated)

const handleLogout = () => {
  authStore.logout()
  router.push('/login') 
}
</script>

<style>
.header-element {
  @apply hover:bg-orange-100 
         text-center px-4 py-2 rounded-xl 
         transition ease-in-out duration-300 
         whitespace-nowrap;
}
</style>
