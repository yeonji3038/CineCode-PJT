<template>
  <nav class="sticky-nav">
    <div class="nav-container">
      <!-- cine_code 클릭 시 Home 경로로 이동하도록 설정 -->
      <router-link :to="{ name: 'Home' }" class="logo">cine_code</router-link>
      <div class="nav-links">
        <router-link :to="{ name: 'codeshare' }" class="nav-item">코드 쉐어</router-link>
        <span v-if="authStore.isLogin" class="nav-divider">|</span>
        <!-- <router-link v-if="authStore.isLogin" :to="{ name: 'mycode' }" class="nav-item">내 코드</router-link> -->
      </div>
      
      <!-- 로그인한 사용자 아이디가 있다면 표시 -->
      <!-- <span v-if="authStore.isLogin" class="user-id">{{ username }}</span> -->

      <!-- 로그인 및 로그아웃 버튼 -->
      <button v-if="!authStore.isLogin" @click="goToLogin" class="logout-btn">로그인</button>
      <button v-else @click="authStore.logout" class="logout-btn">로그아웃</button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

// 로그인 페이지로 이동하는 함수
const goToLogin = () => {
  router.push({ name: 'Login' })
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
