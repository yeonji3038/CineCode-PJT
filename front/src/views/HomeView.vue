<template>
    <div class="home">
        <div class="content-container">
            <div class="main-container">
                <!-- 로그인된 사용자에게만 username 표시 -->
                <h1 v-if="authStore.isLogin" class="username-title">
                    {{ authStore.username }}님,
                </h1>
    
                <div class="search-container">
                  <h2>오늘 하루의 기분이나 현재 감정을 알려주시면 영화를 추천해드릴게요!</h2>
                  <div class="search-box">
                    <div class="search-wrapper">
                      <img src="@/assets/search-icon.svg" class="search-icon" alt="search">
                      <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="ex. 오늘 힘든 하루를 보내서 조금 지쳐 있어"
                        class="search-input"
                      >
                      <img src="@/assets/mic-icon.svg" class="mic-icon" alt="voice">
                    </div>
                  </div>
                </div>
    
                <!-- 시청 중인 영화 섹션 -->
                <div v-if="authStore.isLogin" class="movie-section">
                    <h3 class="section-title">{{ authStore.username }}님이 시청중인 영화</h3>
                    <div v-if="watchedMovies.length" class="movie-scroll">
                    <MovieCard 
                        v-for="movie in watchedMovies" 
                        :key="movie.id"
                        :movie="movie"
                    />
                    </div>
                    <div v-else class="empty-message">
                    시청 중인 영화가 없습니다.
                    </div>
                </div>
    
                <!-- 찜한 영화 섹션 -->
                <div v-if="authStore.isLogin" class="movie-section">
                    <h3 class="section-title">{{ authStore.username }}님이 찜한 영화</h3>
                    <div v-if="likedMovies.length" class="movie-scroll">
                    <MovieCard 
                        v-for="movie in likedMovies" 
                        :key="movie.id"
                        :movie="movie"
                    />
                    </div>
                    <div v-else class="empty-message">
                    찜한 영화가 없습니다.
                    </div>
                </div>
                
                <h3 class="section-title">인기 있는 영화</h3>
                <div class="movie-grid">
                    <MovieCard 
                    v-for="movie in movies" 
                    :key="movie.id"
                    :movie="movie"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
  import { ref,onMounted } from 'vue'
  import { useMovieStore } from '@/stores/movie'
  import { useAuthStore } from '@/stores/auth'
  import { storeToRefs } from 'pinia'
  import MovieCard from '@/components/MovieCard.vue'
  
  const movieStore = useMovieStore()
  
  const { movies } = storeToRefs(movieStore)
  const authStore = useAuthStore()
  const { watchedMovies, likedMovies } = storeToRefs(movieStore)
  const searchQuery = ref('')
  const movieScroll = ref(null)
  
  onMounted(() => {
    movieStore.fetchMovies()
    if (authStore.isLogin) {
        movieStore.fetchWatchedMovies()
        movieStore.fetchLikedMovies()
    }
  })
  </script>
  
<style scoped>
.home {
  max-width: 1400px;
  margin: 0 auto;
  padding: 80px 6rem 2rem; /* 좌우 패딩만 유지 */
}


.search-container {
    text-align: center;
    margin: 0 auto; /* 상단 마진 제거 */
    margin-bottom: 6rem; /* 하단 마진만 유지 */
    max-width: 800px;
}

.username-title {
  font-size: 2rem;
  color: white;
  margin-bottom: 1rem;
  font-weight: lighter;
}

.search-container h2 {
  margin-bottom: 2rem;
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: lighter;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 30px;
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.search-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.mic-icon {
  width: 24px;
  height: 24px;
  margin-left: 10px;
  cursor: pointer;
}

.search-input {
  flex: 1;
  border: none;
  padding: 0.8rem;
  font-size: 1rem;
  background: transparent;
  outline: none;
}

.movie-section {
  margin: 2rem 0;
}

.movie-scroll {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding: 1rem 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.5) transparent;
}

.movie-scroll::-webkit-scrollbar {
  height: 8px;
}

.movie-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.movie-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 4px;
}

.empty-message {
  color: #666;
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.section-title {
  color: #ffffff;
  font-size: 1.5rem;
  margin: 0.5rem 0;
  font-weight: normal;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 6rem;  /* navbar와 동일한 좌우 패딩 적용 */
}
</style>