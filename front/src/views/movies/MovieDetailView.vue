<template>
  <div class="movie-detail" v-if="movie">
    <!-- 배경 이미지 -->
    <div class="backdrop-section">
      <div 
        class="background-image" 
        :style="{ backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.backdrop_path})` }"
      >
        <div class="overlay"></div>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="content">
        <!-- 영화 포스터 -->
        <div class="poster">
          <img :src="movie.poster_path" :alt="movie.title">
        </div>
  
        <!-- 영화 정보 -->
        <div class="info">
          <h1>{{ movie.title }}</h1>
          <div class="meta">
            <span>{{ movie.released_date }}</span>
            <span v-if="movie.runtime">{{ movie.runtime }}분</span>
            <span v-if="movie.genres">{{ movie.genres?.join(', ') }}</span>
          </div>
          <p class="overview">{{ movie.overview }}</p>
        </div>
      </div>
      
      <!-- 버튼 섹션 -->
    <div class="content-wrapper">
      <div class="button-section" v-if="movie">
        <WatchButton 
          :movie="movie" 
          class="action-button"
        />
        <LikeButton 
          :movie="movie" 
          class="action-button"
        />
      </div>
    </div>
    </div>


    <!-- 예고편 섹션 -->
    <div class="content-wrapper" v-if="movie.trailer_id">
      <div class="trailer-section">
        <h2>예고편</h2>
        <iframe
          :src="`https://www.youtube.com/embed/${movie.trailer_id}`"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import WatchButton from '@/components/WatchButton.vue'
import LikeButton from '@/components/LikeButton.vue'
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const movie = ref(null)
const SERVER_URL = import.meta.env.VITE_APP_URL;

onMounted(async () => {
  try {
    // 데이터 로딩 상태 확인을 위한 콘솔 로그
    console.log('영화 상세 정보 로딩 시작')
    
    const response = await axios.get(`${SERVER_URL}movies/${route.params.id}/detail/`)
    movie.value = response.data
    
    // 받아온 데이터 확인을 위한 콘솔 로그
    console.log('받아온 영화 데이터:', movie.value)
  } catch (error) {
    console.error('영화 상세 정보를 불러오는데 실패했습니다:', error)
  }
})
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
  padding-top: 100px;
}

.content {
  position: relative;
  padding: 120px 6rem 60px;  /* 상단 여백 늘림 (navbar 고려) */
  display: flex;
  gap: 3rem;
  z-index: 1;
}

/* content-wrapper 안의 content padding 조정 */
/* .content-wrapper .content {
  padding: 120px 0 60px;  /* 좌우 패딩 제거 */
/* } */

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
  width: 300px;
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
  justify-content: center;
  padding: 2rem 0;
  z-index: 2;
  position: relative;
}

.action-button {
  min-width: 120px;
}

.trailer-section {
  padding: 2rem 6rem;
  position: relative;
  z-index: 2;
}

.trailer-section h2 {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: white;
}

.trailer-section iframe {
  width: 100%;
  height: 600px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .content {
    flex-direction: column;
    align-items: center;
    padding: 100px 2rem 40px;
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

  .trailer-section {
    padding: 2rem 2rem 4rem;
  }

  .trailer-section iframe {
    height: 400px;
  }
}

@media (max-width: 768px) {
  .poster img {
    width: 250px;
  }

  .info h1 {
    font-size: 2.2rem;
  }

  .trailer-section iframe {
    height: 300px;
  }
}
</style>