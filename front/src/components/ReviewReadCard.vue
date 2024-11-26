<template>
    <div class="review-card">
      <!-- 사용자 정보 섹션 -->
      <div class="review-header">
        <div class="user-info-container">
          <div class="profile-image-container">
            <img :src="profileImageSrc" :alt="review.username" class="user-profile">
          </div>
          <div class="review-info">
            <div class="username">{{ review.user.username }}</div>
            <div class="created-at">{{ formattedDate }}</div>
          </div>
        </div>
        <div class="review-likes">
          <button @click="handleLikeClick" class="like-button"
          :disabled="!authStore.isLogin || review.username === authStore.username" >
            👍 {{ review.likes }}
          </button>
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
  
  // 프로필 이미지 computed 속성 추가
  const profileImageSrc = computed(() => {
    if (props.review.user?.profile_image) {
      return `${import.meta.env.VITE_BACKEND_URL}${props.review.user.profile_image}`
    }
    return defaultProfileImage
  })

  const handleLikeClick = () => {
    if (!authStore.isLogin) {
      router.push('/accounts/login')
      return
    }

    if (props.review.username === authStore.username) {
      alert('자신의 리뷰는 좋아요할 수 없습니다.')
      return
    }

    reviewStore.toggleLike(props.review.id)
      .then((response) => {
        // 서버에서 반환된 좋아요 수를 직접 사용
        props.review.likes = response.likes
        // store의 좋아요 카운트 업데이트
        reviewStore.updateLikedReviewsCount(response.is_liked)
      })
      .catch((error) => {
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
    router.push(`/movies/${props.review.movie.id}`)
  }

  </script>
  
  <style scoped src="./css/reviewRead.css">
  </style>