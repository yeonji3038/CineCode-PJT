<template>
    <div class="home">
        <div class="content-container">
            <div class="main-container">
                <!-- 로그인된 사용자에게만 username 표시 -->
                <h1 v-if="authStore.isLogin" class="username-title">
                    {{ authStore.username }}님,
                </h1>
                
                <!--음성인식-->
                <div class="search-container">
                  <h2>오늘 하루의 기분이나 현재 감정을 알려주시면 영화를 추천해드릴게요!</h2>
                  <div class="search-box">
                    <div class="search-wrapper">
                      <input 
                        type="text" 
                        v-model="searchQuery" 
                        placeholder="ex. 오늘 힘든 하루를 보내서 조금 지쳐 있어"
                        class="search-input"
                      >
                      <img 
                        src="@/assets/mic-icon.svg" 
                        class="mic-icon" 
                        alt="voice"
                        @click="startVoiceRecognition"
                        :class="{ 'recording': isRecording }"
                      >
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
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const API_URL = import.meta.env.VITE_APP_URL
  const movieStore = useMovieStore()
  
  const { movies } = storeToRefs(movieStore)
  const authStore = useAuthStore()
  const { watchedMovies, likedMovies } = storeToRefs(movieStore)
  const searchQuery = ref('')
  const movieScroll = ref(null)
  const router = useRouter()
  const isRecording = ref(false)
  const mediaRecorder = ref(null)
  const audioChunks = ref([])

  const startVoiceRecognition = () => {
    if (isRecording.value) {
      alert('이미 녹음 중입니다.')
      return
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        isRecording.value = true
        mediaRecorder.value = new MediaRecorder(stream)
        audioChunks.value = []

        mediaRecorder.value.ondataavailable = (event) => {
          audioChunks.value.push(event.data)
        }

        mediaRecorder.value.onstop = () => {
          const audioBlob = new Blob(audioChunks.value)
          const formData = new FormData()
          formData.append('audio', audioBlob)

          axios.post(
            `${API_URL}movies/analyze-voice/`,
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
          )
          .then(response => {
            router.push({
              name: 'Search',
              params: {
                searchResults: response.data
              }
            })
          })
          .catch(error => {
            console.error('음성 분석 실패:', error)
            alert('음성 인식에 실패했습니다. 다시 시도해주세요.')
          })
          .finally(() => {
            isRecording.value = false
            if (mediaRecorder.value && mediaRecorder.value.stream) {
              mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
            }
          })
        }

        mediaRecorder.value.start()
        setTimeout(() => {
          if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
            stopRecording()
          }
        }, 5000)
      })
      .catch(error => {
        console.error('마이크 접근 실패:', error)
        alert('마이크 접근에 실패했습니다. 마이크 권한을 확인해주세요.')
        isRecording.value = false
      })
  }

  const stopRecording = () => {
    if (mediaRecorder.value && mediaRecorder.value.state !== 'inactive') {
      mediaRecorder.value.stop()
      isRecording.value = false
      mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
    }
  }

  onMounted(() => {
    movieStore.fetchMovies()
    if (authStore.isLogin) {
        movieStore.fetchWatchedMovies()
        movieStore.fetchLikedMovies()
    }
  })
  </script>
  
<style scoped src="./home.css">
.mic-icon {
  cursor: pointer;
}

.mic-icon.recording {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>