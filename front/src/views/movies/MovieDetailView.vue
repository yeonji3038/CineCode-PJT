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

<style scoped src="./css/detail.css">

</style>