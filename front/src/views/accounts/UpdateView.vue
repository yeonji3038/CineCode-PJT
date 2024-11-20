<template>
  <div id="Signup">
    <div class="signup">
      <h2>Update Information</h2>
      <div class="signup-info">
        <input
          placeholder="ID"
          type="text"
          v-model="credentials.username"
          :readonly="true"
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
          placeholder="Phone Number (ex : 010-1234-5678)"
          type="text"
          v-model="credentials.phone_number"
        />
      </div>
      <button @click="updateUserInfo" class="signup-button">UPDATE</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const SERVER_URL = import.meta.env.VITE_APP_URL;  // 환경 변수로 서버 URL 가져오기

export default {
  name: 'UpdateInfo',
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

    // 로그인한 사용자의 정보를 가져오기
    const fetchUserInfo = () => {
      axios({
        method: 'get',
        url: `${SERVER_URL}accounts/me/`,  // 로그인한 사용자의 정보 가져오기 API
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`, // 로그인 토큰을 Authorization 헤더에 추가
        },
      })
        .then((res) => {
          // 받아온 사용자 정보를 form에 미리 채우기
          credentials.value.username = res.data.username;
          credentials.value.email = res.data.email;
          credentials.value.phone_number = res.data.phone_number;
        })
        .catch((err) => {
          console.error(err);
          errorMessage.value = '사용자 정보를 불러오는데 실패했습니다.';
        });
    };

    // 사용자 정보 업데이트
    const updateUserInfo = () => {
      if (passwordErrorMessage.value || confirmPasswordErrorMessage.value || emailErrorMessage.value) {
        errorMessage.value = 'Please fix the errors above before submitting.';
        return;
      }

      axios({
        method: 'put',
        url: `${SERVER_URL}accounts/update/`,  // 사용자 정보 업데이트 API
        data: credentials.value,
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`, // 로그인 토큰을 Authorization 헤더에 추가
        },
      })
        .then((res) => {
          console.log(res);
          alert('정보가 업데이트 되었습니다.');
          router.push({ name: 'Profile' }); // 업데이트 후 프로필 페이지로 리다이렉트
        })
        .catch((err) => {
          console.error(err);
          if (err.response && err.response.data) {
            errorMessage.value = err.response.data.detail || '정보 수정에 실패했습니다.';
          } else {
            errorMessage.value = '예상치 못한 오류가 발생했습니다.';
          }
        });
    };

    // 컴포넌트가 마운트될 때 사용자 정보를 불러오기
    onMounted(() => {
      fetchUserInfo();
    });

    return {
      credentials,
      updateUserInfo,
      errorMessage,
      emailErrorMessage,
      passwordErrorMessage,
      confirmPasswordErrorMessage,
    };
  },
};
</script>

<style scoped src="./css/update.css">
</style>
