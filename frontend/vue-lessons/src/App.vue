<template>
  <div id="app" class="flex flex-col">
    <Header> </Header>
    <router-view></router-view>
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

<style scoped>
#app {
  display: flex;
  align-items: center;
  height: 100vh;
  width: 100%;
}
</style>
