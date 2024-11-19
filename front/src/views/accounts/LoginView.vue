<template>
  <Navbar />
  <div id="Login">
    <div class="login">
      <h2>LOGIN</h2>

      <div class="login-info">
        <input placeholder="Email" type="text" id="Email" />
        <input type="password" id="password" placeholder="Password" />
      </div>
      <button>LOGIN</button>

      
      <div class="social">
        <hr>
        <p>소셜로그인</p>
        <hr>
      </div>
      <div class="social_login">
        <div class="google">
          <img src="@/views/accounts/img/google.png" alt="구글 로그인" />
        </div>
        <div class="naver">
          <img src="@/views/accounts/img/naver.png" alt="네이버 로그인" />
        </div>
      </div>
      
      <div class="find">
        <button @click="goToFindId" id="id-button">아이디 찾기</button>
        <button id="password-button">비밀번호 찾기</button>
      </div>


      <div class="signup">
        <router-link class="nav-item" :to="'/accounts/signup'">SIGNUP</router-link>
      </div>
    </div>
  </div>
</template>



<!-- <script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // Vue Router 사용

const SERVER_URL = process.env.VUE_APP_SERVER_URL;
const PASSWORD = process.env.VUE_APP_PASSWORD;

const credentials = ref({
  username: "",
  password: "",
});

const errMsg = ref("");

const router = useRouter(); // Vue Router 사용

const login = () => {
  axios({
    method: "post",
    url: `${SERVER_URL}accounts/api/token/`,
    data: credentials.value,
  })
    .then((res) => {
      localStorage.setItem("JWT", res.data.access);
      store.dispatch("getUserName", credentials.value.username); // store로 로그인 정보 저장
      emit("login"); // 부모 컴포넌트에 로그인 이벤트 전달
      store.dispatch("setHeader"); // 헤더 설정
      router.push({ name: "Home" }); // Home 페이지로 이동
    })
    .catch((err) => {
      console.dir(err.response.data);
      errMsg.value = err.response.data.detail; // 에러 메시지 처리
    });
};

if (localStorage.getItem("JWT")) {
  router.push({ name: "Home" }); // 이미 JWT가 있으면 Home 페이지로 이동
}
</script> -->
<script setup>
import Navbar from '@/components/Common/Navbar.vue';
import { useRouter } from 'vue-router';

// Vue Router 사용을 위해 useRouter로 router 인스턴스를 가져옵니다.
const router = useRouter();

// 아이디 찾기 페이지로 이동하는 메소드
const goToFindId = () => {
  router.push('/accounts/findid');  // 아이디 찾기 경로로 이동
};

const login = () => {
  // 로그인 로직을 여기에 작성하세요.
};
</script>

<style scoped src='./css/login.css'>
</style>

