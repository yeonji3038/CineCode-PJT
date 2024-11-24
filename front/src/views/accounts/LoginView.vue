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
          <div id="my-signin2"></div>
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
    script.src = 'https://apis.google.com/js/platform.js';
    script.onload = resolve;
    document.head.appendChild(script);
  });
};

// 구글 로그인 성공 핸들러
const handleGoogleLoginSuccess = async (googleUser) => {
  const googleEmail = googleUser.getBasicProfile().getEmail();
  if (googleEmail) {
    try {
      const response = await axios({
        method: 'post',
        url: `${authStore.API_URL}accounts/google/`,
        data: {
          id: googleEmail,
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
  window.gapi.load('auth2', () => {
    window.gapi.auth2.init({
      client_id: import.meta.env.VITE_APP_GOOGLE_CLIENT_ID,
      redirect_uri: '${authStore.FRONT_URL}accounts/login'  
    }).then(() => {
      window.gapi.signin2.render('my-signin2', {
        scope: 'profile email',
        width: 240,
        height: 50,
        longtitle: true,
        theme: 'dark',
        onsuccess: handleGoogleLoginSuccess,
        onfailure: handleGoogleLoginFailure,
      });
    });
  });
};

// 구글 로그인 버튼 클릭 핸들러
const handleGoogleLogin = () => {
  if (window.gapi && window.gapi.auth2) {
    const auth = window.gapi.auth2.getAuthInstance();
    if (auth) {
      auth.signIn();
    }
  }
};

onMounted(() => {
  initGoogleLogin();
});
</script>

<style scoped src="./css/login.css"></style>