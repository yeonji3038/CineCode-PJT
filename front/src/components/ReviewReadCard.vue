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
          <button @click="handleLikeClick" class="like-button"
          :disabled="!authStore.isLogin || review.user.username === authStore.username"
          :class="{ 'liked': review.is_liked }">
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
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'
  
  const props = defineProps({
    review: Object,
    movieTitle: String,
    moviePosterPath: String
  })
  
  const reviewStore = useReviewStore()
  const authStore = useAuthStore()
  const showContent = ref(false)
  const router = useRouter()
  
  const handleLikeClick = () => {
    if (!authStore.isLogin) {
      router.push('/login')
      return
    }

    if (props.review.user.username === authStore.username) {
      alert('자신의 리뷰는 좋아요할 수 없습니다.')
      return
    }

    reviewStore.toggleLike(props.review.id)
      .catch(error => {
        if (error.response?.status === 400) {
          alert(error.response.data.error)
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
    color: #000000;
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