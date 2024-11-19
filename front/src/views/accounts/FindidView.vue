<template>
  <div id="Find">
    <div class="find-id">
      <h2>FIND ID</h2>

      <div class="find-id-info">
        <input
          v-model="email"
          placeholder="Email"
          type="text"
        />
        <input
          v-model="phoneNumber"
          placeholder="Phone Number"
          type="text"
        />
      </div>

      <button @click="findId">FIND</button>

      <!-- 결과가 나오면 해당 아이디를 출력 -->
      <div v-if="foundId">
        <p>찾은 아이디: {{ foundId }}</p>
      </div>

      <!-- 에러 메시지가 있을 경우 출력 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div class="find">
        <button @click="goToLogin">아이디 찾기</button>
        <button @click="goToFindPassword">비밀번호 찾기</button>
      </div>

      <div class="signup">
        <router-link class="nav-item" to="/accounts/signup">SIGNUP</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// 이메일과 전화번호, 에러 메시지, 결과를 위한 상태 정의
const email = ref('');
const phoneNumber = ref('');
const foundId = ref('');
const errorMessage = ref('');

// Vue Router 사용을 위해 useRouter로 router 인스턴스 가져오기
const router = useRouter();

// 아이디 찾기 메소드
const findId = () => {
  // 서버에 요청하기 전에 이메일과 전화번호가 입력되었는지 확인
  if (!email.value || !phoneNumber.value) {
    errorMessage.value = '이메일과 전화번호를 입력해주세요.';
    return;
  }

  // 서버로 요청 (이 예시에서는 POST 방식으로 요청)
  axios.post('http://127.0.0.1:8000/accounts/find_id/', {
    email: email.value,
    phone_number: phoneNumber.value,
  })
    .then(response => {
      // 응답 데이터에서 아이디 받아오기
      if (response.data && response.data.id) {
        foundId.value = response.data.id;  // 아이디를 화면에 표시
        errorMessage.value = '';  // 에러 메시지 초기화
      } else {
        errorMessage.value = '해당하는 아이디를 찾을 수 없습니다.';
        foundId.value = '';
      }
    })
    .catch(error => {
      console.error(error);
      errorMessage.value = '아이디를 찾는 도중 오류가 발생했습니다.';
    });
};

// 로그인 페이지로 이동하는 함수
const goToLogin = () => {
  router.push('/accounts/login');
};

// 비밀번호 찾기 페이지로 이동하는 함수
const goToFindPassword = () => {
  router.push('/accounts/findpassword');
};
</script>



<style scoped src='./css/find.css'>
</style>

