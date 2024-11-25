<template>
  <div class="movie-detail" v-if="movieStore.movieDetail">
    <!-- 배경 이미지 -->
    <div class="backdrop-section">
      <div class="background-image" :style="{ backgroundImage: `url(https://image.tmdb.org/t/p/original${movieStore.movieDetail.backdrop_path})` }">
        <div class="overlay"></div>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="content">
        <!-- 영화 포스터 -->
        <div class="poster">
          <img :src="movieStore.movieDetail.poster_path" :alt="movieStore.movieDetail.title">
        </div>
        <!-- 영화 정보 -->
        <div class="info">
          <h1>{{ movieStore.movieDetail.title }}</h1>
          <div class="meta">
            <span>{{ movieStore.movieDetail.released_date }}</span>
            <span v-if="movieStore.movieDetail.runtime">{{ movieStore.movieDetail.runtime }}분</span>
            <span v-if="movieStore.movieDetail.genres">{{ movieStore.movieDetail.genres?.join(', ') }}</span>
          </div>
          <p class="overview">{{ movieStore.movieDetail.overview }}</p>
          <!-- 버튼 섹션 -->
          <div class="button-section" v-if="movieStore.movieDetail">
            <WatchButton :movie="movieStore.movieDetail" class="action-button"/>
            <LikeButton :movie="movieStore.movieDetail" class="action-button"/>
          </div>
        </div>
      </div>
    </div>
      
    <!-- 예고편 섹션 -->
    <div class="content-wrapper1">
      <div class="trailer-section">
        <h2 class="section-title">예고편</h2>
        <iframe
          :src="`https://www.youtube.com/embed/${movieStore.movieDetail.trailer_id}`"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>

    <!-- 리뷰 작성 섹션 -->
    <div class="content-wrapper1">
      <div class="review-section">
        <div class="review-header">
          <h2 class="section-title">내 리뷰</h2>
        </div>
        <!-- 로그인한 사용자에게만 리뷰 작성 카드 표시 -->
        <ReviewCreateCard
          v-if="authStore.isLogin"
          :movieTitle="movieStore.movieDetail.title"
          :moviePosterPath="movieStore.movieDetail.poster_path"
          :movieId="movieStore.movieDetail.id"
          @review-created="refreshReviews"
        />
         <!-- 로그인하지 않은 사용자에게는 안내 메시지 표시 -->
        <div v-else class="login-prompt">
          <p>리뷰를 작성하려면 <router-link to="/accounts/login" class="login-link">로그인</router-link>이 필요합니다.</p>
        </div>
      </div>
    </div>

    <!-- 리뷰 조회 섹션 -->
    <div class="reviews-section">
      <div class="review-header">
        <h2 class="section-title">리뷰</h2>
        <select v-model="sortOption" class="sort-select" @change="sortReviews">
          <option value="latest">최신순</option>
          <option value="likes">좋아요순</option>
        </select>
        </div>
      <div v-if="reviews.length === 0" class="no-reviews">
        아직 작성된 리뷰가 없습니다.
      </div>
      <ReviewReadCard
        v-for="review in reviews"
        :key="review.id"
        :review="review"
        :movieTitle="movieStore.movieDetail.title"
        :moviePosterPath="movieStore.movieDetail.poster_path"
      />
    </div>
  </div>
</template>

<script setup>
import WatchButton from '@/components/WatchButton.vue'
import LikeButton from '@/components/LikeButton.vue'
import { ref, onMounted, watch } from 'vue'
import ReviewCreateCard from '@/components/ReviewCreateCard.vue'
import ReviewReadCard from '@/components/ReviewReadCard.vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMovieStore } from '@/stores/movie'
import { useReviewStore } from '@/stores/review'

const route = useRoute()
const authStore = useAuthStore()
const movieStore = useMovieStore()
const reviewStore = useReviewStore() 
const reviews = ref([])
const sortOption = ref('latest')

// 리뷰 생성 후 리뷰 목록을 새로고침하는 함수
const refreshReviews = () => {
  reviewStore.fetchReviews(route.params.id)
    .then((data) => {
      reviews.value = data
      sortReviews()
    })
    .catch((error) => {
      console.error('Failed to refresh reviews:', error)
    })
}

// 리뷰 정렬 함수
const sortReviews = () => {
  if (sortOption.value === 'latest') {
    reviews.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } else {
    reviews.value.sort((a, b) => b.likes - a.likes)
  }
}

// 영화와 리뷰 정보 불러오기
onMounted(() => {
  movieStore.fetchMovieDetail(route.params.id)
  reviewStore.fetchReviews(route.params.id)
    .then((data) => {
      reviews.value = data
      sortReviews()
    })
    .catch((error) => {
      console.error('Failed to load reviews:', error)
    })
})

// 영화 상태가 변경될 때마다 상세 정보 다시 불러오기
watch(
  [() => movieStore.watchedMovies, () => movieStore.likedMovies],
  () => {
    movieStore.fetchMovieDetail(route.params.id)
  },
  { deep: true }
)
</script>

<style scoped>
.movie-detail {
  position: relative;
  min-height: 100vh;
  width: 100%;
  color: white;
  background-color: #000;  /* 배경 이미지 로드 전 검정 배경 */
}

.backdrop-section {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 80vh;  /* 화면 높이만큼만 배경 이미지 표시 */
  overflow: hidden;
}

.background-image {
  position: absolute;  /* fixed로 변경하여 스크롤해도 배경이 고정되도록 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center top;
  background-repeat: no-repeat;
  z-index: 0;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.3) 0%,
    rgba(0, 0, 0, 0.7) 70%,
    #000 100%  /* 완전한 검정으로 페이드 아웃 */
    );
  }
  
.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 100px 12rem 0;  /* 좌우 패딩 6rem 추가 */
}

.content-wrapper1 {
  max-width: 1000px;  /* HomeView와 동일한 최대 폭 */
  margin: 0 auto;
  width: 100%;
  padding-bottom: 30px;
}

.content {
  position: relative;
  padding: 150px 0 60px;  /* 좌우 패딩 제거, 상하 패딩만 유지 */
  display: flex;
  gap: 3rem;
  z-index: 1;
  width: 100%;
}

.meta {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  color: #e0e0e0;
  font-size: 1.1rem;
}

.meta span {
  position: relative;
}

/* 구분자 스타일 수정 */
.meta span:not(:last-child) {
  &::after {
    content: '';  /* 기본적으로 비어있음 */
  }
}

/* 다음 요소가 있는 경우에만 구분자 표시 */
.meta span:not(:last-child):has(+ span[style*="display: inline"]) {
  &::after {
    content: '|';
    position: absolute;
    right: -1rem;
  }
}

.poster {
  flex-shrink: 0;  /* 포스터 크기 고정 */
}

.poster img {
  width: 350px;
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}

.info {
  flex: 1;
  padding-top: 2rem;  /* 상단 여백 추가 */
}

.info h1 {
  font-size: 2.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.meta {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  color: #e0e0e0;
  font-size: 1.1rem;
}

.meta span {
  position: relative;
}

.meta span:not(:last-child)::after {
  content: '|';
  position: absolute;
  right: -1rem;
}

.overview {
  font-size: 1.1rem;
  line-height: 1.8;
  max-width: 800px;
  color: #e0e0e0;
  margin-bottom: 2rem;
}

.button-section {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;  /* overview와의 간격 */
}

.action-button {
  min-width: 120px;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  margin-left: 2rem;
}

.trailer-section {
  padding: 2rem 0;
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}

.trailer-section iframe {
  width: 100%;
  height: 507px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.review-section {
  padding: 2rem 6rem;
  margin: 0 auto;
  width: 100%;
  max-width: 1000px;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-select {
  background-color: transparent;
  color: #fff;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.sort-select:focus {
  outline: none;
  border-color:rgb(211, 47, 39);
}

.sort-select option {
  background-color: #000;
  color: #fff;
}

.login-prompt {
  background-color: #d9d9d9;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  color: #333;
  margin: 0 6rem;  /* review-section의 padding과 동일하게 맞춤 */
}

.login-link {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}

.reviews-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
  padding: 0 6rem;
  margin: 0 auto 150px;
  max-width: 1000px;
}

.no-reviews {
  text-align: center;
  color: #888;
  font-size: 1.2rem;
  margin-bottom: 100px;
}

.section-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  margin: 0;  /* margin-left 제거 */
  padding-bottom: 1rem;
}
.review-card {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .trailer-section iframe {
    height: calc((100vw - 12rem) * 0.507);
  }
}

@media (max-width: 1024px) {
  .trailer-section,
  .review-section,
  .reviews-section {
    padding: 2rem;
  }

  .content-wrapper,
  .content-wrapper1 {
    padding: 0 2rem;
  }

  .content {
    flex-direction: column;
    align-items: center;
    padding: 0 2rem 40px;
  }

  .info {
    text-align: center;
  }

  .meta {
    justify-content: center;
  }

  .overview {
    margin: 0 auto 2rem;
  }

  .button-section {
    justify-content: center;  /* 버튼 중앙 정렬 */
  }
  
  .trailer-section iframe {
    height: calc((100vw - 4rem) * 0.507);
  }
}

@media (max-width: 768px) {
  .content {
    flex-direction: column;
    align-items: center;
    padding: 100px 1rem 40px;
  }

  .content-wrapper,
  .content-wrapper1 {
    padding: 0 1rem;
  }

  .trailer-section,
  .review-section,
  .reviews-section {
    padding: 2rem 1rem;
  }

  .poster img {
    width: 250px;
  }

  .info h1 {
    font-size: 2.2rem;
  }

  .meta {
    justify-content: center;
  }

  .overview {
    margin: 0 auto 2rem;
  }

  .button-section {
    justify-content: center;
  }
  
  .trailer-section iframe {
    height: calc((100vw - 2rem) * 0.507);
  }
}

</style>