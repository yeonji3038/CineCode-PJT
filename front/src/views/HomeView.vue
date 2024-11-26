<template>
  <div class="home">
    <div class="content-container">
      <div class="main-container">
        <!-- 로그인된 사용자에게만 username 표시  -->
        <h1 v-if="authStore.isLogin" class="username-title">
            {{ authStore.username }}님,
        </h1>
        
        <!--검색 및 음성인식-->
        <div class="search-container">
          <h2>영화를 검색하거나 현재 감정을 알려주시면 영화를 추천해드릴게요!</h2>
          <div class="search-box">
            <div class="input-wrapper">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="영화 제목을 입력하거나 감정을 표현해보세요!"
                class="search-input"
                @keyup.enter="handleSearch"
              >
              <img 
                src="@/assets/mic-icon.svg" 
                class="mic-icon" 
                alt="voice"
                @click="startVoiceRecognition"
                :class="{ 'recording': isRecording }"
              >
            </div>
            <button 
              class="search-button" 
              @click="handleSearch"
            >
              검색
            </button>
          </div>
        </div>

        <!-- 시청 중인 영화 섹션 -->
        <div v-if="authStore.isLogin" class="movie-section">
            <h3 class="section-title">{{ authStore.username }}님이 시청중인 영화</h3>
            <div v-if="watchedMovies.length" class="carousel-container">
                <button 
                    class="carousel-prev" 
                    @click="prevWatchedSlide" 
                    v-show="watchedStartIndex > 0"
                >
                    <span class="arrow">&#10094;</span>
                </button>

                <div class="movies-wrapper">
                    <div 
                        class="movies-track" 
                        :style="{ transform: `translateX(-${watchedStartIndex * (100/4)}%)` }"
                    >
                        <MovieCard 
                            v-for="watchedMovie in watchedMovies" 
                            :key="{...watchedMovie.movie.id}"
                            :movie="{
                                ...watchedMovie.movie,
                                status: '시청 중',
                                watched_at: watchedMovie.watched_at
                            }"
                            class="movie-item"
                        />
                    </div>
                </div>

                <button 
                    class="carousel-next" 
                    @click="nextWatchedSlide" 
                    v-show="watchedStartIndex < watchedMovies.length - 4"
                >
                    <span class="arrow">&#10095;</span>
                </button>
            </div>
            <div v-else class="empty-message">
                시청 중인 영화가 없습니다.
            </div>
        </div>

        <!-- 찜한 영화 섹션 -->
        <div v-if="authStore.isLogin" class="movie-section">
            <h3 class="section-title">{{ authStore.username }}님이 찜한 영화</h3>
            <div v-if="likedMovies.length" class="carousel-container">
                <button 
                    class="carousel-prev" 
                    @click="prevLikedSlide" 
                    v-show="likedStartIndex > 0"
                >
                    <span class="arrow">&#10094;</span>
                </button>

                <div class="movies-wrapper">
                    <div 
                        class="movies-track" 
                        :style="{ transform: `translateX(-${likedStartIndex * (100/4)}%)` }"
                    >
                        <MovieCard 
                            v-for="likedMovie in likedMovies" 
                            :key="{...likedMovie.movie.id}"
                            :movie="{
                                ...likedMovie.movie,
                                is_liked: true,
                                liked_at: likedMovie.liked_at
                            }"
                            class="movie-item"
                        />
                    </div>
                </div>

                <button 
                    class="carousel-next" 
                    @click="nextLikedSlide" 
                    v-show="likedStartIndex < likedMovies.length - 4"
                >
                    <span class="arrow">&#10095;</span>
                </button>
            </div>
            <div v-else class="empty-message">
                찜한 영화가 없습니다.
            </div>
        </div>
        
        <!-- 인기 있는 영화 섹션 -->
        <h3 class="section-title">인기 있는 영화</h3>
        <div class="movie-grid">
          <MovieCard 
              v-for="movie in popularMovies" 
              :key="movie.id"
              :movie="movie"
          />
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
  import { ref,onMounted, onUnmounted } from 'vue'
  import { useMovieStore } from '@/stores/movie'
  import { useAuthStore } from '@/stores/auth'
  import { storeToRefs } from 'pinia'
  import MovieCard from '@/components/MovieCard.vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const SERVER_URL = import.meta.env.VITE_APP_URL
  const CST_API_KEY = import.meta.env.VITE_CST_API_KEY
  const CNL_API_KEY = import.meta.env.VITE_CNL_API_KEY
  const movieStore = useMovieStore()
  const authStore = useAuthStore()
  const popularMovies = ref([])
  const loading = ref(true)
  const error = ref(null)
  const { watchedMovies, likedMovies } = storeToRefs(movieStore)
  const searchQuery = ref('')
  const router = useRouter()

  const watchedStartIndex = ref(0)
  const likedStartIndex = ref(0)

  // 음성 녹음 관련 상태 변수들
  const isRecording = ref(false)  // 현재 녹음 중인지 상태
  const mediaStream = ref(null)   // 오디오 스트림을 저장
  const mediaRecorder = ref(null) // 미디어 녹음기 인스턴스
  const audioChunks = ref([])     // 녹음된 오디오 데이터 청크를 저장하는 배열
  
  // Web Speech API 설정
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = 'ko-KR';
  recognition.interimResults = true;
  recognition.continuous = true;

  // 인기 영화 가져오기
  const fetchPopularMovies = () => {
    loading.value = true
    error.value = null
    
    axios.get(`${SERVER_URL}movies/popular/`)
      .then((response) => {
        popularMovies.value = response.data
      })
      .catch((err) => {
        console.error('인기 영화를 불러오는데 실패했습니다:', err)
        error.value = '인기 영화를 불러오는데 실패했습니다.'
      })
      .finally(() => {
        loading.value = false
      })
  }


  const nextWatchedSlide = () => {
    if (watchedStartIndex.value < watchedMovies.value.length - 4) {
        watchedStartIndex.value++
    }
}

const prevWatchedSlide = () => {
    if (watchedStartIndex.value > 0) {
        watchedStartIndex.value--
    }
}

const nextLikedSlide = () => {
    if (likedStartIndex.value < likedMovies.value.length - 4) {
        likedStartIndex.value++
    }
}

const prevLikedSlide = () => {
    if (likedStartIndex.value > 0) {
        likedStartIndex.value--
    }
}



  // 음성 녹음 시작 함수
  const startVoiceRecognition = () => {
    if (isRecording.value) return;
    isRecording.value = true;

    // Web Speech API를 통한 실시간 음성 인식 시작
    recognition.start();

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');
      
      // 실시간으로 인식된 텍스트를 검색창에 표시
      searchQuery.value = transcript;
    };

    recognition.onerror = (event) => {
      console.error('음성 인식 오류:', event.error);
      isRecording.value = false;
    };

    recognition.onend = () => {
      isRecording.value = false;
    };

    navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        sampleRate: 44100,
        channelCount: 1,
      }
    })
      .then((stream) => {
        mediaStream.value = stream;
        mediaRecorder.value = new MediaRecorder(stream);
        audioChunks.value = [];

        mediaRecorder.value.ondataavailable = (event) => {
          audioChunks.value.push(event.data);
        };

        mediaRecorder.value.onstop = () => {
          const audioBlob = new Blob(audioChunks.value);
          const formData = new FormData();
          formData.append('audio_file', audioBlob, 'voice.wav');

          // 서버로 전송
          fetch(`${SERVER_URL}movies/analyze_voice/`, {
            method: 'POST',
            body: formData,
            headers: {
              'Authorization': `Token ${authStore.token}`
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('서버 응답 오류');
              }
              return response.json();
            })
            .then(data => {
              console.log('분석 결과:', data);
              router.push({
                name: 'Search',
                query: {
                  transcript: data.transcript,
                  sentiment: data.sentiment_score,
                  movies: JSON.stringify(data.movies)
                }
              });
            })
            .catch(error => {
              console.error('음성 분석 오류:', error);
              alert('음성 분석 중 오류가 발생했습니다.');
            })
            .finally(() => {
              stream.getTracks().forEach(track => track.stop());
              isRecording.value = false;
            });
        };

        // 녹음 시작
        mediaRecorder.value.start();
        console.log('녹음 시작');

        // 녹음 상태 표시
        const recordingIndicator = document.createElement('div');
        recordingIndicator.textContent = '녹음 중...';
        recordingIndicator.style.color = 'red';
        document.querySelector('.input-wrapper').appendChild(recordingIndicator);

        // 5초 후 자동 종료
        setTimeout(() => {
          if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
            mediaRecorder.value.stop();
            recordingIndicator.remove();
          }
        }, 5000);
      })
      .catch(error => {
        console.error('오디오 입력 장치 오류:', error);
        let errorMessage = '';

        switch (error.name) {
          case 'NotAllowedError':
            errorMessage = '마이크 사용 권한이 거부되었습니다. 브라우저 설정에서 마이크 권한을 허용해주세요.';
            break;
          case 'NotFoundError':
            errorMessage = '마이크나 이어폰이 연결되어 있지 않습니다. 오디오 입력 장치를 연결해주세요.';
            break;
          case 'NotReadableError':
            errorMessage = '오디오 입력 장치에 접근할 수 없습니다. 다른 앱이 사용 중인지 확인해주세요.';
            break;
          default:
            errorMessage = '오디오 입력 장치 오류가 발생했습니다. 장치 연결을 확인해주세요.';
        }

        alert(errorMessage);
        isRecording.value = false;
      });
  }

  // 검색 함수 수정
  const handleSearch = async () => {
    if (!searchQuery.value.trim()) {
      alert('검색어를 입력해주세요.');
      return;
    }

    try {
      const response = await axios.get(`${SERVER_URL}movies/search/`, {
        params: { query: searchQuery.value },
        headers: {
          'Authorization': `Token ${authStore.token}`
        }
      });

      // 검색 결과가 있으면 검색 페이지로 이동
      router.push({
        name: 'Search',
        query: {
          searchQuery: searchQuery.value,
          movies: JSON.stringify(response.data)
        }
      });
    } catch (error) {
      console.error('검색 오류:', error);
      alert('검색 중 오류가 발생했습니다.');
    }
  };

  onMounted(() => {
    fetchPopularMovies()
    movieStore.fetchAllMovies()
    if (authStore.isLogin) {
        movieStore.fetchWatchedMovies()
        movieStore.fetchLikedMovies()
    }
  })

  onUnmounted(() => {
    if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
      mediaRecorder.value.stop();
    }
    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(track => track.stop());
    }
    // Web Speech API 정리
    recognition.stop();
  })
</script>


<style scoped src="./home.css">

</style>