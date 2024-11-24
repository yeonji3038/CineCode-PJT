<template>
  <div class="home">
    <div class="content-container">
      <div class="main-container">
        <!-- 로그인된 사용자에게만 username 표시  -->
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
            <div v-if="watchedMovies.length" class="movie-scroll"
              @mousedown="startDragging"
              @mousemove="drag"
              @mouseup="stopDragging"
              @mouseleave="stopDragging">
            <MovieCard 
                v-for="watchedMovie in watchedMovies" 
                :key="{...watchedMovie.movie.id}"
                :movie="{
                  ...watchedMovie.movie,
                  status: '시청 중',
                  watched_at: watchedMovie.watched_at
                }"
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
                v-for="likedMovie in likedMovies" 
                :key="{...likedMovie.movie.id}"
                :movie="{
                  ...likedMovie.movie,
                  is_liked: true,
                  liked_at: likedMovie.liked_at
                }"
            />
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

  // 드래그 스크롤 관련 상태 변수들
  const isDragging = ref(false)
  const startX = ref(0)
  const scrollLeft = ref(0)

  // 음성 녹음 관련 상태 변수들
  const isRecording = ref(false)  // 현재 녹음 중인지 상태
  const mediaStream = ref(null)   // 오디오 스트림을 저장
  const mediaRecorder = ref(null) // 미디어 녹음기 인스턴스
  const audioChunks = ref([])     // 녹음된 오디오 데이터 청크를 저장하는 배열
  
  // Web Speech API 설정 추가
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = 'ko-KR';
  recognition.interimResults = true;  // 중간 결과 반환
  recognition.continuous = true;      // 연속 인식 모드

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


  // 드래그 시작
  const startDragging = (e) => {
    isDragging.value = true
    const slider = e.currentTarget
    startX.value = e.pageX
    scrollLeft.value = slider.scrollLeft
  }

  // 드래그 중
  const drag = (e) => {
    if (!isDragging.value) return
    e.preventDefault()
    const slider = e.currentTarget
    const x = e.pageX - slider.offsetLeft
    const walk = (x - startX.value) * 2 // 스크롤 속도 조절
    slider.scrollLeft = scrollLeft.value - walk
  }

  // 드래그 종료
  const stopDragging = () => {
    isDragging.value = false
  }




  // 음성 녹음 시작 함수
  const startVoiceRecognition = () => {
    if (isRecording.value) {
      return;
    }

    const audioConstraints = {
      audio: {
        echoCancellation: { ideal: true },
        noiseSuppression: { ideal: true },
        autoGainControl: { ideal: true },
        deviceId: 'default'
      }
    };

    // 실시간 음성 인식 시작
    recognition.start();
    
    // 실시간 결과 처리
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join('');
      searchQuery.value = transcript;  // 실시간으로 검색창에 표시
    };

    // 기존 녹음 로직 유지
    navigator.mediaDevices.getUserMedia(audioConstraints)
      .then(stream => {
        console.log('오디오 스트림 획득 성공:', stream);
        isRecording.value = true;
        
        try {
          // 다양한 오디오 형식 지원
          const mimeType = MediaRecorder.isTypeSupported('audio/webm')
            ? 'audio/webm'
            : 'audio/mp4';

          mediaRecorder.value = new MediaRecorder(stream, {
            mimeType: mimeType,
            audioBitsPerSecond: 128000
          });
        } catch (e) {
          console.log('기본 설정으로 MediaRecorder 생성');
          mediaRecorder.value = new MediaRecorder(stream);
        }
        
        audioChunks.value = [];

        mediaRecorder.value.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunks.value.push(event.data);
          }
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
        document.querySelector('.search-wrapper').appendChild(recordingIndicator);

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

  // 음성 인식 에러 처리
  recognition.onerror = (event) => {
    console.error('음성 인식 오류:', event.error);
    isRecording.value = false;
  };

  // 음성 인식 종료 처리
  recognition.onend = () => {
    isRecording.value = false;
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
      mediaRecorder.value.stop()
    }
    if (isRecording.value) {
      recognition.stop();
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

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #ff4444;
  font-size: 1.1rem;
}
</style>