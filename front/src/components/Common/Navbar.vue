<template>
  <!-- 상단 네비게이션 바 -->
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="nav-container">
      <!-- 왼쪽 영역: 로고 -->
      <div class="nav-left">
        <router-link :to="{ name: 'Home' }" class="logo">CINECODE</router-link>
      </div>
      
      <!-- 오른쪽 영역: 사용자 정보 및 로그인/로그아웃 -->
      <div class="nav-right">
        <!-- 로그인 상태일 때 사용자 이름 표시 -->
        <router-link v-if="authStore.isLogin && authStore.username" :to="{ name: 'Profile' }" class="user-id">{{ authStore.username }}</router-link>
        <!-- 로그인/로그아웃 버튼 -->
        <button v-if="!authStore.isLogin" @click="goToLogin" class="logout-btn">로그인</button>
        <button v-else @click="authStore.logout" class="logout-btn">로그아웃</button>
      </div>

      <!-- 시간 표시 영역 -->
      <div class="time-container">
        <!-- 타임존 선택 드롭다운 -->
        <select v-model="selectedTimezone" class="timezone-select">
          <!-- 아시아 -->
          <optgroup label="아시아">
            <option value="Asia/Seoul">서울</option>
            <option value="Asia/Tokyo">도쿄</option>
            <option value="Asia/Shanghai">상하이</option>
            <option value="Asia/Singapore">싱가포르</option>
            <option value="Asia/Hong_Kong">홍콩</option>
            <option value="Asia/Bangkok">방콕</option>
            <option value="Asia/Dubai">두바이</option>
          </optgroup>

          <!-- 유럽 -->
          <optgroup label="유럽">
            <option value="Europe/London">런던</option>
            <option value="Europe/Paris">파리</option>
            <option value="Europe/Berlin">베를린</option>
            <option value="Europe/Rome">로마</option>
            <option value="Europe/Madrid">마드리드</option>
            <option value="Europe/Amsterdam">암스테르담</option>
            <option value="Europe/Moscow">모스크바</option>
          </optgroup>

          <!-- 북미 -->
          <optgroup label="북미">
            <option value="America/New_York">뉴욕</option>
            <option value="America/Los_Angeles">로스앤젤레스</option>
            <option value="America/Chicago">시카고</option>
            <option value="America/Toronto">토론토</option>
            <option value="America/Vancouver">밴쿠버</option>
          </optgroup>

          <!-- 오세아니아 -->
          <optgroup label="오세아니아">
            <option value="Australia/Sydney">시드니</option>
            <option value="Australia/Melbourne">멜버른</option>
            <option value="Pacific/Auckland">오클랜드</option>
          </optgroup>

          <!-- 남미 -->
          <optgroup label="남미">
            <option value="America/Sao_Paulo">상파울루</option>
            <option value="America/Buenos_Aires">부에노스아이레스</option>
            <option value="America/Santiago">산티아고</option>
          </optgroup>
        </select>
        <!-- 현재 시간 표시 -->
        <div class="time-info">{{ currentTime }}</div>
      </div>
    </div>
  </nav>
</template>

<script setup>
// 필요한 모듈 import
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted, onUnmounted, ref, watch } from 'vue'

// 스토어와 라우터 초기화
const authStore = useAuthStore()
const router = useRouter()
const isScrolled = ref(false)

// 시간 관련 상태 변수
const currentTime = ref('')
const selectedTimezone = ref('Asia/Seoul')  // 기본 타임존 설정

// 현재 시간 업데이트 함수
const updateTime = () => {
  const now = new Date()
  const options = {
    timeZone: selectedTimezone.value,
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }
  currentTime.value = now.toLocaleTimeString('ko-KR', options)
}

// 스크롤 이벤트 핸들러
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

// 컴포넌트 마운트 시 실행
onMounted(() => {
  // 스크롤 이벤트 리스너 등록
  window.addEventListener('scroll', handleScroll)
  // 초기 시간 설정 및 주기적 업데이트 시작
  updateTime()
  const timer = setInterval(updateTime, 60000)  // 1분마다 시간 업데이트

  // 컴포넌트 언마운트 시 정리
  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
    clearInterval(timer)  // 타이머 정리
  })
})

// 로그인 페이지로 이동
const goToLogin = () => {
  router.push({ name: 'Login' })
}

// 타임존 변경 감지 및 시간 업데이트
watch(selectedTimezone, () => {
  updateTime()
})
</script>

<style scoped>
/* 네비게이션 바 기본 스타일 */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  background-color: transparent;  /* 초기 상태는 완전 투명 */
  z-index: 1000;
  width: 100%;
  padding: 1.1rem 0;
  transition: all 0.3s ease; /* 부드러운 전환 효과 추가 */
}

/* 스크롤 시 네비게이션 바 스타일 */
.navbar.scrolled {
  background-color: rgba(0, 0, 0, 0.95); /* 거의 불투명한 검정색으로 변경 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); /* 선택사항: 그림자 효과 추가 */
}

/* 네비게이션 컨테이너 레이아웃 */
.nav-container {
  width: 100%;
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 로고 스타일 */
.logo {
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 3rem;
  color: #ffffff;
  font-family: 'Quicksand', sans-serif;
  text-shadow: 0 0 10px rgba(255,255,255,0.3),
               0 0 20px rgba(255,255,255,0.2);
  letter-spacing: 1px;
}

/* 로고 호버 효과 */
.logo:hover {
  transform: scale(1.03);
  transition: all 0.3s ease;
  text-shadow: 0 0 15px rgba(255,255,255,0.5),
               0 0 25px rgba(255,255,255,0.3);
}

/* 왼쪽 네비게이션 영역 */
.nav-left {
  display: flex;
  gap: 2rem;
  align-items: center;
  font-weight: lighter;
  gap: 1.5rem;  /* nav-item 간의 간격 */
  margin-right: auto; /* 로고 옆에 정렬 */
}

/* 네비게이션 아이템 스타일 */
.nav-item {
  color: white;
  text-decoration: none;
  transition: font-weight 0.3s ease;
}

.nav-item:hover {
  font-weight: bold;
}

/* 오른쪽 네비게이션 영역 */
.nav-right {
  display: flex;
  align-items: center;
  gap: 1.5rem; /* username과 login button 사이 간격 */
}

/* 사용자 ID 스타일 */
.user-id {
  display: flex;
  align-items: center;
  color: white;
  text-decoration: none;
  cursor: pointer; 
  transition: font-weight 0.3s ease;
}

.user-id:hover {
  font-weight: bold;
}

/* 로그인/로그아웃 버튼 스타일 */
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

/* 시간 표시 영역 스타일 */
.time-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 1rem;
}

/* 타임존 선택 드롭다운 스타일 */
.timezone-select {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 0.8rem;
  cursor: pointer;
  outline: none;
  -webkit-appearance: none;  /* 기본 스타일 제거 */
  -moz-appearance: none;     /* 기본 스타일 제거 */
  appearance: none;          /* 기본 스타일 제거 */
}

/* 옵션 그룹 스타일 */
.timezone-select optgroup {
  background: #1a1a1a;
  color: white;
  border: none;
}

/* 옵션 스타일 */
.timezone-select option {
  background: #1a1a1a;
  color: white;
  border: none;
  padding: 8px;
}

/* IE에서 화살표 제거 */
.timezone-select::-ms-expand {
  display: none;
}

/* 시간 정보 텍스트 스타일 */
.time-info {
  color: white;
  font-size: 0.9rem;
  letter-spacing: 1px;
}
</style>
