<script setup>
import Navbar from './components/Common/Navbar.vue'

import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import axios from 'axios'

const authStore = useAuthStore()

// axios 인터셉터 설정
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 401 에러 처리
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      authStore.logOut()
    }
    return Promise.reject(error)
  }
)
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