<template>
    <div class="review-create-card">
      <div class="header">
        <img :src="profileImageSrc" :alt="authStore.username" class="user-profile">
        <span class="username">{{ username }}</span>
      </div>
      <div class="content">
        <img :src="moviePosterPath" alt="Movie Poster" class="movie-poster" />
        <div class="review-input">
          <h3>{{ movieTitle }}</h3>
          <textarea v-model="reviewContent" placeholder="감상평을 입력하세요"></textarea>
          <div class="controls">
            <label class="label">
              스포일러
              <input type="checkbox" v-model="isSpoiler" class="checkbox"/>
            </label>
            <div class="error-message" v-if="showError">
              <span v-if="showError">감상평을 입력해주세요</span>
            </div>
            <button @click="saveReview">저장</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, defineProps, defineEmits } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useReviewStore } from '@/stores/review'
  import defaultProfileImage from '@/assets/profile.png'

  const props = defineProps({
    movieTitle: String,
    moviePosterPath: String,
    movieId: Number
  })
  const emit = defineEmits(['review-created'])
  const authStore = useAuthStore()
  const reviewStore = useReviewStore()

  const username = authStore.username
  const userProfileImage = authStore.profile_image
  // 프로필 이미지 computed 속성 추가
  const profileImageSrc = computed(() => {
    return authStore.profileImage || defaultProfileImage
  })
  
  const reviewContent = ref('')
  const isSpoiler = ref(false)
  const showError = ref(false)

  const saveReview = () => {
    // 내용이 비어있는지 검사
    if (!reviewContent.value.trim()) {
      showError.value = true
      return
    }
    showError.value = false
    const reviewData = {
      content: reviewContent.value,
      is_spoiler: isSpoiler.value,
      movie_id: props.movieId,
    }
    console.log('전송할 데이터:', reviewData)  // 디버깅용 로그
    reviewStore.createReview(reviewData)
    .then(() => {
        // 성공 시 입력 필드 초기화
        reviewContent.value = ''
        isSpoiler.value = false
        // 성공 메시지 표시
        alert('리뷰가 성공적으로 작성되었습니다.')
        // 부모 컴포넌트에 리뷰 생성 이벤트 발생
        emit('review-created')
    })
    .catch((error) => {
        console.error('리뷰 생성 실패:', error)
    })
  }
</script>
  
<<<<<<< HEAD
<style scoped src="./css/reviewCreat.css">
=======
<style scoped>
  .review-create-card {
    background-color: #d9d9d9;
    padding: 20px;
    border-radius: 8px;
    margin: 20px auto;
    max-width: 800px; 
    color: #000000;
    font-family: 'Inter', sans-serif;
  }
  
  .header {
    display: flex;
    align-items: center;
    padding: 0 10px;
  }
  
  .user-profile {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
  }

  .username {
    font-size: 1rem;
    font-weight: bold;
  }
  
  .content {
    display: flex;
  }
  
  .movie-poster {
    width: 114px;
    height: 171px;
    border-radius: 8px;
    margin-right: 20px;
    margin-top: 15px; /* 포스터 위치 조정 */
  }
  
  h3 {
    font-size: 1.2rem;
    margin: 15px 0;
  }

  .review-input {
    flex: 1;
  }
  
  textarea {
    width: 99%;
    height: 100px;
    border: none; /* 박스 border 제거 */
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 10px;
    font-family: 'Inter', sans-serif; /* 폰트 변경 */
  }
  
  .controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 5px 0 0;  /* 오른쪽 패딩 추가 */
  }

  .label {
    display: flex;  /* 추가 */
    align-items: center;
    gap: 8px;  /* 체크박스와 텍스트 사이 간격 */
  }

  .checkbox {
    width: 16px;
    height: 16px;
    margin: 0;  /* 기존 마진 제거 */
    cursor: pointer;
  }

  .error-message {
    color: #ff4444;
    font-size: 0.9rem;
    padding-left: 2px;
  }
  
  button {
    background-color: #A7A7A7;
    color: white;
    border: none;
    padding: 5px 15px;
    margin-top: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s ease;  /* 호버 효과 추가 */
  }

  button:hover {
    background-color: rgb(211, 47, 39);  /* 호버 시 색상 */
    color: black;
  }
>>>>>>> 54bcfec37d7384b11f1c69f60b5e4337e2ff53aa
  </style>