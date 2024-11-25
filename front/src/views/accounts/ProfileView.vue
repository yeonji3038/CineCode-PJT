<template>
  <div class="profile-container dark-mode">
    <!-- 상단 프로필 영역 -->
    <div class="profile-header">
      <div class="profile-img-container">
        <img :src="profileImageSrc" alt="Profile Image" class="profile-image">
      </div>
      <div class="profile-info">
        <h3>{{ authStore.username }}</h3>
        <p>{{ authStore.email }}</p>
        <router-link to="/accounts/update" class="contact-btn">회원정보 수정</router-link>
      </div>
    </div>

    <!-- Activity 영역 -->
    <div class="activity-section">
      <div class="activity-item" @click="toggleReviews" :class="{ 'active': showReviews }">
        <h5>Reviews Written</h5>
        <p>{{ userInfo.review_count || 0 }}</p>
      </div>
      <div class="activity-item">
        <h5>Likes</h5>
        <p>{{ userInfo.likes_count || 0 }}</p>
      </div>
    </div>

    <!-- 리뷰 목록 섹션 추가 -->
    <div v-if="showReviews" class="reviews-section">
      <div v-if="reviews.length > 0" class="reviews-list">
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <div class="review-header">
            <h4>{{ review.movie_title }}</h4>
            <span class="review-date">{{ formatDate(review.created_at) }}</span>
          </div>
          <p class="review-content">{{ review.content }}</p>
          <div class="review-rating">
            <span>평점: {{ review.rating }}/5</span>
          </div>
        </div>
      </div>
      <p v-else class="no-reviews">작성한 리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import defaultProfileImage from '@/assets/profile.png'

const authStore = useAuthStore()
const userInfo = ref({})
const showReviews = ref(false)
const reviews = ref([])

// 프로필 이미지 computed 속성 추가
const profileImageSrc = computed(() => {
  return authStore.profileImage || defaultProfileImage
})

// 리뷰 토글 및 불러오기 함수
const toggleReviews = async () => {
  showReviews.value = !showReviews.value
  
  // 리뷰가 보여질 때만 리뷰를 불러옴
  if (showReviews.value && reviews.value.length === 0) {
    try {
      const response = await axios({
        method: 'get',
        url: `${authStore.API_URL}movies/user-reviews/`,
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      })
      reviews.value = response.data
    } catch (error) {
      console.error('리뷰 불러오기 실패:', error)
    }
  }
}

// 날짜 포맷팅 함수
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  if (authStore.isLogin) {
    authStore.fetchUserInfo()
  }
})
</script>

<style scoped src="./css/profile.css"></style>

<style scoped>
/* 기존 CSS 파일에 추가 */
.reviews-section {
  margin-top: 2rem;
  padding: 0 1rem;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.review-header h4 {
  margin: 0;
  color: #fff;
}

.review-date {
  font-size: 0.9rem;
  color: #888;
}

.review-content {
  margin: 0.5rem 0;
  color: #ddd;
}

.review-rating {
  color: #ffd700;
  font-weight: bold;
}

.no-reviews {
  text-align: center;
  color: #888;
  padding: 2rem;
}

/* Activity 항목 호버 효과 */
.activity-item {
  cursor: pointer;
  transition: background-color 0.3s;
}

.activity-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.activity-item.active {
  background-color: rgba(255, 255, 255, 0.15);
}

.profile-image {
  width: 100px;  /* 프로필 페이지는 더 큰 크기 유지 */
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
}

.profile-img-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}
</style>
