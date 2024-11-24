<template>
    <div v-if="isLogin" class="review-create-card">
      <div class="header">
        <img :src="userProfileImage" alt="Profile" class="profile-image" />
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
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useReviewStore } from '@/stores/review'
  
  const authStore = useAuthStore()
  const reviewStore = useReviewStore()
  
  const isLogin = authStore.isLogin
  const username = authStore.username
  const userProfileImage = authStore.profile_image
  
  const props = defineProps({
    movieTitle: String,
    moviePosterPath: String,
    movieId: Number
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
      movie: props.movieId,
    }
    reviewStore.createReview(reviewData)
    .then(() => {
        // 성공 시 입력 필드 초기화
        reviewContent.value = ''
        isSpoiler.value = false
        // 성공 메시지 표시
        alert('리뷰가 성공적으로 작성되었습니다.')
    })
    .catch((error) => {
        console.error('리뷰 생성 실패:', error)
    })
  }
</script>
  
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
  }
  
  .profile-image {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    margin-right: 20px;
    margin-left: 10px;
  }

  .username {
    font-size: 1.2rem; /* 사용자 이름 크기 조정 */
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
    width: 95%;
    height: 100px;
    margin-bottom: 10px;
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
  }

  .label {
    align-items: center;
  }

  .checkbox {
    width: 18px; /* 체크박스 크기 조정 */
    height: 18px;
    margin-left: 5px;
  }

  .error-message {
    color: #ff4444;
    font-size: 0.9rem;
    padding-left: 5px;
  }
  
  button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 5px 10px;
    margin-right: 15px;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>