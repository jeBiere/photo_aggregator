<style>
.header-element {
  @apply hover:bg-orange-100 w-full 
        text-center p-2 rounded-xl
        transition ease-in-out duration-300;
}
</style>

<template>
  <div class="flex bg-white p-6 gap-10 gap-x-32 rounded-3xl justify-evenly mt-4">
    <div class="bg-orange-100 text-center p-2 rounded-xl">
      <p>@Photo_aggr</p>
    </div>
    <div class="header-element">
      <router-link to="/about"> О нас </router-link>
    </div>
    <template v-if="authStore.isAuthenticated">
      <div class="header-element">
        <router-link to="/photographers"> Фотографы </router-link>
      </div>
      <div class="header-element">
        <router-link to="/studios"> Студии </router-link>
      </div>
      <div class="header-element">
        <router-link to="/services"> Услуги </router-link>
      </div>
      <div class="header-element">
        <router-link to="/profile"> Профиль </router-link>
      </div>
      <div class="header-element cursor-pointer" @click="authStore.logout">Выйти</div>
    </template>

    <template v-else>
      <div class="header-element">
        <router-link to="/registration"> Регистрация </router-link>
      </div>
      <div class="header-element">
        <router-link to="/login"> Войти </router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'


const authStore = useAuthStore()
</script>
