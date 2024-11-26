<template>
  <div class="search">
    <div class="search-container">
      <div class="search-box">
        <div class="input-wrapper">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="영화 제목을 입력하거나 음성으로 감정을 표현해보세요!"
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

    <!-- sentiment가 null이 아닐 때만 표시 -->
    <!-- <div v-if="sentiment !== null" class="result-section">
      <h2>감정 분석 결과:</h2>
      <p>감정 점수: {{ sentiment }}</p>
    </div> -->

    <!-- movies 배열이 존재하고 길이가 0보다 클 때만 표시 -->
    <div v-if="movies && movies.length > 0" class="movies-section">
      <h2>추천 영화</h2>
      <div class="carousel-container">
        <button 
          class="carousel-prev" 
          @click="prevSlide" 
          v-show="startIndex > 0"
        >
          <span class="arrow">&#10094;</span>
        </button>

        <div class="movies-wrapper">
          <div 
            class="movies-track" 
            :style="{ transform: `translateX(-${startIndex * (100/4)}%)` }"
          >
            <MovieCard 
              v-for="movie in movies" 
              :key="movie.id"
              :movie="movie"
              class="movie-item"
            />
          </div>
        </div>

        <button 
          class="carousel-next" 
          @click="nextSlide"
          v-show="startIndex < movies.length - 4"
        >
          <span class="arrow">&#10095;</span>
        </button>
      </div>
    </div>

    <!-- 로딩 인디케이터 추가 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>감정 분석중...</p>
    </div>
  </div>
</template>

<script setup>
// 필요한 모듈과 컴포넌트 import
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MovieCard from '@/components/MovieCard.vue'
import { useAuthStore } from '@/stores/auth'

// 환경 변수에서 서버 URL 가져오기
const SERVER_URL = import.meta.env.VITE_APP_URL
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 상태 관리를 위한 ref 변수들
const transcript = ref('')      // 음성 인식 텍스트
const sentiment = ref(null)     // 감정 분석 점수
const movies = ref([])          // 추천 영화 목록
const searchQuery = ref('')     // 검색어
const isRecording = ref(false)  // 녹음 상태
const mediaStream = ref(null)   // 오디오 스트림
const mediaRecorder = ref(null) // 미디어 레코더
const audioChunks = ref([])     // 오디오 데이터 청크

// 로딩 상태 추가
const isLoading = ref(false);

// 음성 인식 시작 함수
const startVoiceRecognition = () => {
  if (isRecording.value) return;
  isLoading.value = true;
  

  // Web Speech API의 SpeechRecognition 객체 생성
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  
  recognition.lang = 'ko-KR';
  recognition.interimResults = true;
  recognition.continuous = true;

  recognition.onresult = (event) => {
    const transcript = Array.from(event.results)
      .map(result => result[0])
      .map(result => result.transcript)
      .join('');
    
    // 실시간으로 인식된 텍스트를 검색창에 표시
    searchQuery.value = transcript;
  };

  recognition.start();

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
      isRecording.value = true;    // 녹음 상태 설정
      mediaStream.value = stream;  // 미디어 스트림 저장
      
      // MediaRecorder 설정 (오디오 포맷 지원 확인)
      try {
        const mimeType = MediaRecorder.isTypeSupported('audio/webm')
          ? 'audio/webm'
          : 'audio/mp4';

        mediaRecorder.value = new MediaRecorder(stream, {
          mimeType: mimeType,
          audioBitsPerSecond: 128000  // 오디오 비트레이트 설정
        });
      } catch (e) {
        // 기본 설정으로 폴백
        mediaRecorder.value = new MediaRecorder(stream);
      }
      
      // 오디오 데이터 저장을 위한 배열 초기화
      audioChunks.value = [];

      // 녹음 데이터가 사용 가능할 때마다 실행되는 이벤트 핸들러
      mediaRecorder.value.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.value.push(event.data);
        }
      };

      // 녹음이 멈출 때 실행되는 이벤트 핸들러
      mediaRecorder.value.onstop = async () => {
        recognition.stop(); // 음성 인식 중지
        // 녹음된 오디오 데이터를 Blob으로 변환
        const audioBlob = new Blob(audioChunks.value);
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'voice.wav');

        try {
          // 서버로 음성 데이터 전송
          const response = await fetch(`${SERVER_URL}movies/analyze_voice/`, {
            method: 'POST',
            body: formData,
            headers: {
              'Authorization': `Token ${authStore.token}`
            }
          });

          if (!response.ok) throw new Error('서버 응답 오류');
          
          // 서버 응답 처리
          const data = await response.json();
          transcript.value = data.transcript;        // 음성 텍스트 저장
          sentiment.value = data.sentiment_score;    // 감정 점수 저장
          searchQuery.value = data.transcript;       // 검색어 설정
          
          // 영화 데이터 처리
          if (data.movies && Array.isArray(data.movies)) {
            movies.value = data.movies.map(movie => ({
              id: movie.id,
              title: movie.title,
              overview: movie.overview,
              poster_path: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null,
              vote_average: movie.vote_avg,
              release_date: movie.released_date,
              popularity: movie.popularity
            }));
          }
        } catch (error) {
          console.error('음성 분석 오류:', error);
          alert('음성 분석 중 오류가 발생했습니다. 다시 시도해주세요.');
        } finally {
          // 스트림 정리 및 상태 초기화
          stream.getTracks().forEach(track => track.stop());
          isRecording.value = false;
          isLoading.value = false;
        }
      };

      // 녹음 중임을 표시하는 UI 요소 추가
      const recordingIndicator = document.createElement('div');
      recordingIndicator.textContent = '녹음 중...';
      recordingIndicator.style.color = 'red';
      document.querySelector('.input-wrapper').appendChild(recordingIndicator);

      // 녹음 시작
      mediaRecorder.value.start();
      
      // 5초 후 자동으로 녹음 중지
      setTimeout(() => {
        if (mediaRecorder.value?.state === 'recording') {
          mediaRecorder.value.stop();
          recordingIndicator.remove();
        }
      }, 5000);  // 5초 녹음
    })
    .catch(error => {
      // 오류 처리
      console.error('오디오 입력 장치 오류:', error);
      const errorMessages = {
        NotAllowedError: '마이크 사용 권한 거부되었습니다.',
        NotFoundError: '마이크를 찾을 수 없습니다.',
        NotReadableError: '마이크에 접근할 수 없습니다.',
      };
      alert(errorMessages[error.name] || '오디오 입력 장치 오류 발생했습니다.');
      isRecording.value = false;
      isLoading.value = false;
    });
};

// localStorage에서 데이터를 불러오는 함수
const loadFromLocalStorage = () => {
  const savedMovies = localStorage.getItem('searchMovies')
  const savedTranscript = localStorage.getItem('searchTranscript')
  const savedSentiment = localStorage.getItem('searchSentiment')
  const savedQuery = localStorage.getItem('searchQuery')

  if (savedMovies) {
    movies.value = JSON.parse(savedMovies)
    transcript.value = savedTranscript || ''
    sentiment.value = savedSentiment ? Number(savedSentiment) : null
    searchQuery.value = savedQuery || ''
  }
}

// movies가 변경될 때마다 localStorage에 저장
watch(movies, (newMovies) => {
  if (newMovies.length > 0) {
    localStorage.setItem('searchMovies', JSON.stringify(newMovies))
    localStorage.setItem('searchTranscript', transcript.value)
    localStorage.setItem('searchSentiment', sentiment.value)
    localStorage.setItem('searchQuery', searchQuery.value)
  }
}, { deep: true })

// 컴포넌트 마운트 시 초기화 수정
onMounted(() => {
  // URL의 query params에서 데이터 가져오기
  const querySearchQuery = route.query.searchQuery
  const queryMovies = route.query.movies
  const queryTranscript = route.query.transcript
  const querySentiment = route.query.sentiment

  // 검색어로 넘어온 경우
  if (querySearchQuery && queryMovies) {
    searchQuery.value = querySearchQuery;
    try {
      const parsedMovies = JSON.parse(queryMovies);
      movies.value = parsedMovies.map(movie => ({
        id: movie.id,
        title: movie.title,
        overview: movie.overview,
        poster_path: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null,
        vote_average: movie.vote_average,
        release_date: movie.release_date,
        popularity: movie.popularity
      }));

      // 쿼리 파라미터 처리 후 깨끗한 URL로 변경
      router.replace('/search');
    } catch (error) {
      console.error('Movies parsing error:', error);
      movies.value = [];
    }
  }
  // 음성 인식으로 넘어온 경우
  else if (queryTranscript && querySentiment && queryMovies) {
    transcript.value = queryTranscript;
    sentiment.value = Number(querySentiment);
    searchQuery.value = queryTranscript;
    
    try {
      const parsedMovies = JSON.parse(queryMovies);
      movies.value = parsedMovies.map(movie => ({
        id: movie.id,
        title: movie.title,
        overview: movie.overview,
        poster_path: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null,
        vote_average: movie.vote_avg,
        release_date: movie.released_date,
        popularity: movie.popularity
      }));

      // 쿼리 파라미터 처리 후 깨끗한 URL로 변경
      router.replace('/search');
    } catch (error) {
      console.error('Movies parsing error:', error);
      movies.value = [];
    }
  } else {
    // URL에 쿼리 파라미터가 없으면 localStorage에서 데이터 불러오기
    loadFromLocalStorage()
  }
});

const startIndex = ref(0)

const nextSlide = () => {
  if (startIndex.value < movies.value.length - 4) {
    startIndex.value += 4
  }
}

const prevSlide = () => {
  if (startIndex.value > 0) {
    startIndex.value -= 4
  }
}

// 검색 함수 추가
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    alert('검색어를 입력해주세요.');
    return;
  }

  isLoading.value = true;
  try {
    const response = await fetch(`${SERVER_URL}movies/search/?query=${encodeURIComponent(searchQuery.value)}`, {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    });

    if (!response.ok) throw new Error('검색 중 오류가 발생했습니다.');
    
    const data = await response.json();
    movies.value = data.map(movie => ({
      id: movie.id,
      title: movie.title,
      overview: movie.overview,
      poster_path: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null,
      vote_average: movie.vote_average,
      release_date: movie.release_date,
      popularity: movie.popularity
    }));

    // 검색 결과가 없는 경우
    if (movies.value.length === 0) {
      alert('검색 결과가 없습니다.');
    }
  } catch (error) {
    console.error('검색 오류:', error);
    alert('검색 중 오류가 발생했습니다.');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped src="./css/search.css" ></style>

