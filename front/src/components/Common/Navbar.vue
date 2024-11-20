<template>
  <nav class="sticky-nav">
    <div class="nav-container">
      <div class="nav-left">
        <router-link :to="{ name: 'Home' }" class="logo">cine_code</router-link>
        <router-link :to="{ name: 'CodeShare' }" class="nav-item">코드 쉐어</router-link>
        <span class="nav-divider">|</span>
        <router-link :to="{ name: 'MyCode' }" class="nav-item">내 코드</router-link>
      </div>
    
      <div class="nav-right">
          <!-- 로그인한 사용자 아이디가 있다면 표시 -->
        <span v-if="authStore.isLogin && authStore.username" class="user-id">
          {{ authStore.username }}
        </span>
        <!-- 로그인 및 로그아웃 버튼 -->
        <button v-if="!authStore.isLogin" @click="goToLogin" class="logout-btn">로그인</button>
        <button v-else @click="authStore.logout" class="logout-btn">로그아웃</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

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
  background-color: #000000;
  z-index: 1000;
  width: 100%;
  padding: 1.5rem 0;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  padding: 1rem 6rem;
  margin: 0 auto;
}

.logo {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 3rem; /* 로고와 nav-item 간의 간격 */
}

.nav-left {
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

.nav-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;  /* username과 login button 사이 간격 */
}

.user-id {
  display: flex;
  align-items: center;
  gap: 0.5rem;  /* 프로필 이미지와 username 사이 간격 */
  color: white;
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
