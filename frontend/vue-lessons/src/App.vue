<template>
  <div id="app" class="flex flex-col w-[70%] min-w-[600px] max-w-[1600px] mx-auto">
    <Header />
    <transition name="page-fade" mode="out-in">
      <router-view :key="$route.fullPath"></router-view>
    </transition>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style src="./assets/main.css"></style>

<style scoped></style>

<style>
.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}
</style>
