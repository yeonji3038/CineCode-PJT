<script setup>
import Navbar from './components/Common/Navbar.vue'
</script>

<template>
  <div class="app-container">
    <Navbar />
    <RouterView />
  </div>
</template>

<style>
/* 전역 스타일은 scoped 없이 작성 */
:root {
  background-color: #000000;
}

body, html {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-color: #000000;
}

.app-container {
  min-height: 100vh;
  background-color: #000000;
  color: white;
}
</style>