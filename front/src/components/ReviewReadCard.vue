<template>
    <div class="review-card">
      <!-- 사용자 정보 섹션 -->
      <div class="review-header">
        <img :src="review.user.profile_image" alt="Profile" class="profile-image" />
        <div class="review-info">
          <span class="username">{{ review.user.username }}</span>
          <span class="created-at">{{ formattedDate }}</span>
        </div>
        <!-- 좋아요 버튼 섹션 -->
        <div class="review-likes">
          <button @click="toggleLike" class="like-button">
            <img src="@/assets/like-icon.svg" alt="Like" />
          </button>
          <span>{{ review.likes }}</span>
        </div>
      </div>
      <!-- 리뷰 내용 섹션 -->
      <div class="review-content">
        <img :src="moviePosterPath" alt="Movie Poster" class="movie-poster" />
        <div>
          <h3>{{ movieTitle }}</h3>
          <p v-if="!isSpoiler || showContent">{{ review.content }}</p>
          <button v-else @click="showContent = true">스포일러가 포함된 리뷰입니다.</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useReviewStore } from '@/stores/review'
  
  const props = defineProps({
    review: Object,
    movieTitle: String,
    moviePosterPath: String
  })
  
  const reviewStore = useReviewStore()
  const showContent = ref(false)
  
  const toggleLike = () => {
    reviewStore.toggleLike(props.review.id)
    .catch((error) => {
      if (error.response?.status === 401) {
        // 401 에러 시 로그인 페이지로 이동
        router.push('/login')
      }
    })
  }
  const formattedDate = computed(() => {
    const createdAt = new Date(props.review.created_at)
    const now = new Date()
    const diff = now - createdAt
  
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)
    const months = Math.floor(days / 30)
    const years = Math.floor(months / 12)
  
    if (minutes < 60) return `${minutes}분 전`
    if (hours < 24) return `${hours}시간 전`
    if (days < 30) return `${days}일 전`
    if (months < 12) return `${months}달 전`
    return `${years}년 전`
  })
  </script>
  
  <style scoped>
  .review-card {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    background-color: #f9f9f9;
  }
  
  .review-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .profile-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  
  .review-info {
    flex-grow: 1;
    margin-left: 16px;
  }
  
  .username {
    font-weight: bold;
  }
  
  .created-at {
    color: #888;
    font-size: 0.9em;
  }
  
  .review-likes {
    display: flex;
    align-items: center;
  }
  
  .like-button {
    background: none;
    border: none;
    cursor: pointer;
  }
  
  .review-content {
    display: flex;
    margin-top: 16px;
  }
  
  .movie-poster {
    width: 100px;
    height: 150px;
    margin-right: 20px;
  }
  </style>