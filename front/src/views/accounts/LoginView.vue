<template>
  <div id="Login">
    <div class="login">
      <h2>LOGIN</h2>

      <div class="login-info">
        <input v-model="credentials.login_username" placeholder="ID" type="text" id="username" />
        <input v-model="credentials.login_password" type="password" id="password" placeholder="Password" />
      </div>
      <button @click="authStore.login(credentials)" class="login-button">LOGIN</button>
 
      <!-- 소셜 로그인 섹션 추가 -->
      <div class="social">
        <hr />
        <p>소셜로그인</p>
        <hr />
      </div>
      <div class="social_login">
        <div class="google">
          <button @click="handleGoogleLogin">
            <img src="@/views/accounts/img/google.png" alt="구글 로그인" />
          </button>
        </div>
        <div class="naver">
          <div id="naverIdLogin"></div>
          <img src="@/views/accounts/img/naver.png" alt="네이버 로그인" @click="handleNaverLogin" />
        </div>
      </div>

      <div class="signup">
        <router-link class="nav-item" :to="'/accounts/signup'">SIGNUP</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const authStore = useAuthStore()
const credentials = ref({
  login_username: '',
  login_password: '',
});

// 구글 API 스크립트 동적 로드
const loadGoogleAPI = () => {
  return new Promise((resolve) => {
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.onload = resolve;
    document.head.appendChild(script);
  });
};

// 구글 로그인 성공 핸들러
const handleGoogleLoginSuccess = async (response) => {
  if (response.credential) {  // 새로운 API는 credential을 반환
    try {
      const token = response.credential;
      const response = await axios({
        method: 'post',
        url: `${authStore.API_URL}accounts/google/`,
        data: {
          id_token: token,  // 백엔드로 id_token 전송
        }
      });
      
      credentials.value = {
        login_username: response.data.username,
        login_password: import.meta.env.VITE_APP_PASSWORD
      };
      
      authStore.login(credentials.value);
    } catch (error) {
      console.error('Google login error:', error);
    }
  }
};

// 구글 로그인 실패 핸들러
const handleGoogleLoginFailure = (error) => {
  console.error('Google login failed:', error);
};

// 구글 로그인 초기화
const initGoogleLogin = async () => {
  await loadGoogleAPI();
};

let lastLoginAttempt = 0;  // 마지막 로그인 시도 시간을 저장할 변수

// 구글 로그인 버튼 클릭 핸들러
const handleGoogleLogin = () => {
  const now = Date.now();
  const fiveMinutes = 5 * 60 * 1000;  // 5분을 밀리초로 변환
  
  if (now - lastLoginAttempt < fiveMinutes) {
    alert('잠시 후 다시 시도해주세요. (5분 간격 제한)');
    return;
  }
  
  lastLoginAttempt = now;
  
  google.accounts.id.initialize({
    client_id: import.meta.env.VITE_APP_GOOGLE_CLIENT_ID,
    callback: handleGoogleLoginSuccess
  });
  google.accounts.id.prompt();
};

onMounted(() => {
  initGoogleLogin();
});
</script>

<style scoped src="./css/login.css"></style>