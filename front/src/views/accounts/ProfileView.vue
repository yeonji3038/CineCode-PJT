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
      <div class="activity-item" @click="showUserReviews" :class="{ 'active': showingReviews }">
        <h5>내가 작성한 리뷰</h5>
        <p>{{ userReviews.length }}</p>
      </div>
      <div class="activity-item" @click="showLikedReviews" :class="{ 'active': showingLikes }">
        <h5>내가 좋아요한 리뷰</h5>
        <p>{{ likedReviews.length }}</p>
      </div>
    </div>

    <!-- 리뷰 목록 섹션 -->
    <div v-if="showingReviews" class="reviews-section">
      <div v-if="userReviews.length > 0" class="reviews-list">
        <ReviewUDCard
          v-for="review in userReviews"
          :key="review.id"
          :review="review"
          :movieTitle="review.movie_title"
          :moviePosterPath="review.movie_poster_path"
          @review-updated="refreshReviews"
          @review-deleted="refreshReviews"
        />
      </div>
      <p v-else class="no-reviews">작성한 리뷰가 없습니다.</p>
    </div>

    <!-- 좋아요한 리뷰 목록 섹션 -->
    <div v-if="showingLikes" class="reviews-section">
      <div v-if="likedReviews.length > 0" class="reviews-list">
        <ReviewReadCard
          v-for="review in likedReviews"
          :key="review.id"
          :review="review"
          :movieTitle="review.movie_title"
          :moviePosterPath="review.movie_poster_path"
        />
      </div>
      <p v-else class="no-reviews">좋아요한 리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import defaultProfileImage from '@/assets/profile.png'
import ReviewUDCard from '@/components/ReviewUDCard.vue'
import ReviewReadCard from '@/components/ReviewReadCard.vue'

const authStore = useAuthStore()
const showingReviews = ref(true) // 기본값을 true로 설정
const showingLikes = ref(false)
const userReviews = ref([])
const likedReviews = ref([])

const profileImageSrc = computed(() => {
  return authStore.profileImage || defaultProfileImage
})

// 사용자 리뷰 보기
const showUserReviews = () => {
  showingLikes.value = false
  showingReviews.value = true
  fetchUserReviews()
}

// 좋아요한 리뷰 보기
const showLikedReviews = () => {
  showingReviews.value = false
  showingLikes.value = true
  fetchLikedReviews()
}

// 사용자 리뷰 가져오기
const fetchUserReviews = () => {
  axios({
    method: 'get',
    url: `${authStore.API_URL}movies/user-reviews/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    }
  })
  .then(response => {
    userReviews.value = response.data
  })
  .catch(error => {
    console.error('리뷰 불러오기 실패:', error.response?.data?.error || error.message)
    userReviews.value = []
  })
}

// 좋아요한 리뷰 가져오기
const fetchLikedReviews = () => {
  axios({
    method: 'get',
    url: `${authStore.API_URL}movies/liked-reviews/`,
    headers: {
      'Authorization': `Token ${authStore.token}`
    }
  })
  .then(response => {
    likedReviews.value = response.data
  })
  .catch(error => {
    console.error('좋아요한 리뷰 불러오기 실패:', error)
    likedReviews.value = []
  })
}

// 리뷰 새로고침
const refreshReviews = () => {
  if (showingReviews.value) {
    fetchUserReviews()
  } else if (showingLikes.value) {
    fetchLikedReviews()
  }
}

onMounted(() => {
  if (authStore.isLogin) {
    fetchUserReviews()  // 초기 로드 시 사용자 리뷰 가져오기
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
