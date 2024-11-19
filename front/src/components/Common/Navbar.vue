<template>
  <nav class="sticky-nav">
    <div class="nav-container">
      <router-link to="/" class="logo">cine_code</router-link>
      <div class="nav-links">
        <router-link to="/codeshare" class="nav-item">코드 쉐어</router-link>
        <span v-if="isLogin" class="nav-divider">|</span>
        <router-link v-if="isLogin" :to="'/mycode/' + username" class="nav-item">내 코드</router-link>
      </div>
      <button v-if="!isLogin" @click="login" class="logout-btn">로그인</button>
      <button v-else @click="logout" class="logout-btn">로그아웃</button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const isLogin = ref(false) // 실제 구현시에는 상태 관리 도구(Pinia/Vuex)를 사용하세요
const username = ref('')   // 실제 구현시에는 서버 응답에서 받아야 함
const router = useRouter()

const logout = () => {
  isLogin.value = false
  router.push('/')
}
const login = () => {
  isLogin.value = true
  router.push('/accounts/login')
}
</script>

<style scoped>
.sticky-nav {
  position: sticky;
  top: 0;
  background-color: #000000;
  z-index: 1000;
  padding: 1.5rem 2rem;
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
  margin-right: 3rem; /* 로고와 nav-item 간의 간격 */
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
  font-weight: lighter;
  gap: 1.5rem; /* nav-item 간의 간격 */
  margin-right: auto; /* 로고 옆에 정렬 */
}

.nav-divider {
  color: white;
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
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: white;
  color: black;
  font-weight: bold;
}
</style>