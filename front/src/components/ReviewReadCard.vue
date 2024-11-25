<template>
    <div class="review-card">
      <!-- 사용자 정보 섹션 -->
      <div class="review-header">
        <div class="user-info-container">
          <img :src="profileImageSrc" :alt="review.user.username" class="user-profile">
          <div class="review-info">
            <div class="username">{{ review.username }}</div>
            <div class="created-at">{{ formattedDate }}</div>
          </div>
        </div>
        <div class="review-likes">
          <button @click="handleLikeClick" class="like-button"
          :disabled="!authStore.isLogin || review.user.username === authStore.username"
          :class="{ 'liked': review.is_liked }" >
            <img src="@/assets/like-icon.svg" alt="Like" class="like-icon"/>
          </button>
          <span>{{ review.likes }}</span>
        </div>
      </div>
      <!-- 리뷰 내용 섹션 -->
      <div class="review-content">
        <img :src="moviePosterPath" alt="Movie Poster" class="movie-poster"
          @click="goToMovieDetail"
          style="cursor: pointer;"
        />
        <div class="review-details">
          <h3>{{ movieTitle }}</h3>
          <div class="review-text">
            <p v-if="!review.is_spoiler || showContent">{{ review.content }}</p>
            <button v-else @click="showContent = true" class="spoiler-button">스포일러가 포함된 리뷰입니다.</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useReviewStore } from '@/stores/review'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'
  import defaultProfileImage from '@/assets/profile.png'
  
  const props = defineProps({
    review: Object,
    movieTitle: String,
    moviePosterPath: String
  })
  
  const reviewStore = useReviewStore()
  const authStore = useAuthStore()
  const showContent = ref(false)
  const router = useRouter()
  const isSpoiler = computed(() => props.review.is_spoiler)
  
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

  const goToMovieDetail = () => {
    router.push(`/movies/${props.review.movie}`)
  }

  // 프로필 이미지 computed 속성 추가
  const profileImageSrc = computed(() => {
    return props.review.user.profile_image || defaultProfileImage 
  })
  </script>
  
  <style scoped>
  .review-card {
    width: 100%;  
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
    padding: 0 10px;
    width: 100%;
  }
  
  .user-info-container {
    display: flex;
    align-items: center;
  }
  
  .user-profile {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .review-info {
    margin-left: 10px;
  }
  
  .username {
    font-size: 1rem;
    font-weight: bold;
  }
  
  .created-at {
    color: #888;
    font-size: 0.9em;
  }
  
  .review-likes {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .like-button {
    background: none;
    border: none;
    cursor: pointer;
    padding: 5px;
  }
  
  .like-icon {
    width: 25px;
    height: 25px;
  }

  .like-button:disabled {
    opacity: 0.5; 
    cursor: not-allowed;
  }

  .review-likes span {
    margin-left: 10px;
    font-size: 1rem;
    font-weight: bold;
    font-family: 'Noto Sans KR', sans-serif;
  }

  .review-content {
    display: flex;
    margin-top: 16px;
  }
  
  .movie-poster {
  width: 100px;
  height: 150px;
  margin-right: 20px;
  border-radius: 4px;
  transition: transform 0.2s;
}

.movie-poster:hover {
  transform: scale(1.05);
}

.spoiler-button {
  width: 100%;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 12px;
  border-radius: 4px;
  cursor: pointer;
  color: #666;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.spoiler-button:hover {
  background-color: #e0e0e0;
}

.review-text {
  margin-top: 8px;
}
  </style>