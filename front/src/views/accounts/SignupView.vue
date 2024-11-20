<template>
  <div id="Signup">
    <div class="signup">
      <h2>SIGNUP</h2>
      <div class="signup-info">
        <input
          placeholder="ID"
          type="text"
          v-model="credentials.username"
        />
        <input
          placeholder="Email"
          type="email"
          v-model="credentials.email"
          :class="{ 'input-error': emailErrorMessage }"
        />
        <!-- 이메일 형식 오류 메시지 -->
        <div v-if="emailErrorMessage" class="error-message">
          {{ emailErrorMessage }}
        </div>

        <input
          placeholder="Password"
          type="password"
          v-model="credentials.password1"
          :class="{ 'input-error': passwordErrorMessage }"
        />
        <div v-if="passwordErrorMessage" class="error-message">
          {{ passwordErrorMessage }}
        </div>

        <input
          placeholder="Confirm Password"
          type="password"
          v-model="credentials.password2"
          :class="{ 'input-error': confirmPasswordErrorMessage }"
        />
        <div v-if="confirmPasswordErrorMessage" class="error-message">
          {{ confirmPasswordErrorMessage }}
        </div>

        <input
          placeholder="Phone Number (ex : 010-1234-5678) "
          type="text"
          v-model="credentials.phone_number"
        />
      </div>
      <button @click="signup">SIGNUP</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const SERVER_URL = import.meta.env.VITE_APP_URL;  // 환경 변수로 서버 URL 가져오기

export default {
  name: 'Signup',
  setup() {
    const router = useRouter();
    const credentials = ref({
      username: '',
      email: '',
      password1: '',
      password2: '',
      phone_number: '',
    });

    const errorMessage = ref('');

    // 이메일 형식 유효성 검사
    const emailErrorMessage = computed(() => {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (credentials.value.email.length > 0 && !emailRegex.test(credentials.value.email)) {
        return '올바른 이메일 형식을 입력하세요.';
      }
      return '';
    });

    const passwordErrorMessage = computed(() => {
      if (credentials.value.password1.length > 0 && credentials.value.password1.length < 8) {
        return '8글자 이상 작성하십시오';
      }
      return '';
    });

    const confirmPasswordErrorMessage = computed(() => {
      if (credentials.value.password2.length > 0 && credentials.value.password1 !== credentials.value.password2) {
        return '비밀번호가 일치하지 않습니다.';
      }
      return '';
    });

    const signup = () => {
      console.log(SERVER_URL)
      if (passwordErrorMessage.value || confirmPasswordErrorMessage.value || emailErrorMessage.value) {
        errorMessage.value = 'Please fix the errors above before submitting.';
        return;
      }

      axios({
        method: 'post',
        url: `${SERVER_URL}accounts/signup/`,  // 환경 변수를 사용한 API 요청
        data: credentials.value,
      })
        .then((res) => {
          console.log(res);
          alert('Welcome to CineCode');
          router.push({ name: 'Login' });
        })
        .catch((err) => {
          console.error(err);
          if (err.response && err.response.data) {
            errorMessage.value = err.response.data.detail || 'Signup failed.';
          } else {
            errorMessage.value = 'An unexpected error occurred.';
          }
        });
    };

    return {
      credentials,
      signup,
      errorMessage,
      emailErrorMessage, // 이메일 오류 메시지
      passwordErrorMessage, // 비밀번호 조건 메시지
      confirmPasswordErrorMessage, // 비밀번호 확인 메시지
    };
  },
};
</script>

<style scoped src="./css/signup.css">
</style>
