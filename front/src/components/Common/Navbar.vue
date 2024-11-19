<template>
  <nav class="sticky-nav">
    <!-- 로그인 했을 때 -->
    <div v-if="isLoggedIn" class="nav-container">
      <router-link to="/" class="logo">cine_code</router-link>
      <div class="nav-links">
        <router-link to="/code-share" class="nav-item">코드 쉐어</router-link>
        <router-link to="/my-code" class="nav-item">내 코드</router-link>
        <button @click="handleLogout" class="logout-btn">로그아웃</button>
      </div>
    </div>

    <!-- 로그인 하지 않았을 때 -->
    <div v-else class="nav-container">
      <router-link to="/" class="logo">cine_code</router-link>
      <div class="nav-links">
        <router-link to="/codeshare" class="nav-item">코드 쉐어</router-link>
        <router-link to="/accounts/login" class="nav-item">로그인</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isLoggedIn = ref(false) // 실제 구현시에는 상태 관리 도구(Pinia/Vuex)를 사용하세요
const router = useRouter()

const handleLogout = () => {
  isLoggedIn.value = false
  router.push('/login')
}
</script>

<style scoped>
.sticky-nav {
  position: sticky;
  top: 0;
  background-color: #000000;
  z-index: 1000;
  padding: 1rem 2rem;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-item {
  color: white;
  text-decoration: none;
  transition: font-weight 0.3s ease;
}

.nav-item:hover {
  font-weight: bold;
}

.logout-btn {
  background: transparent;
  border: 1px solid white;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: white;
  color: black;
  font-weight: bold;
}
</style>