<template>
  <div id="Login">
    <div class="login">
      <h2>LOGIN</h2>

      <div class="login-info">
        <input v-model="credentials.login_username" placeholder="ID" type="text" id="username" />
        <input v-model="credentials.login_password" type="password" id="password" placeholder="Password" />
      </div>
      <button @click="authStore.login(credentials)" class="login-button">LOGIN</button>
 
      <div class="social">
        <hr />
        <p>소셜로그인</p>
        <hr />
      </div>
      <div class="social_login">
        <div class="google">
          <button @click="GoogleLoginBtn">
            <img src="@/views/accounts/img/google.png" alt="구글 로그인" />
          </button>
        </div>
        <div class="naver">
          <img src="@/views/accounts/img/naver.png" alt="네이버 로그인" />
        </div>
      </div>

      <div class="signup">
        <router-link class="nav-item" :to="'/accounts/signup'">SIGNUP</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore()
// 로그인 입력값을 관리하는 상태 변수
const credentials = ref({
  login_username: '',
  login_password: '',
});


</script>

<style scoped src="./css/login.css"></style>