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
  
<style scoped src="./css/reviewCreat.css">
  </style>