<template>
  <div class="search">
      <!-- 검색창 추가 -->
      <div class="search-container">

      <div class="search-box">
        <div class="search-wrapper">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="다른 감정으로도 영화를 추천받아보세요!"
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

    <!-- transcript가 빈 문자열이 아닐 때만 표시,, -->
    <!-- <div v-if="transcript !== ''" class="result-section">
      <h2>말씀하신 내용:</h2>
      <p>{{ transcript }}</p>
    </div> -->

    <!-- sentiment가 null이 아닐 때만 표시 -->
    <!-- <div v-if="sentiment !== null" class="result-section">
      <h2>감정 분석 결과:</h2>
      <p>감정 점수: {{ sentiment }}</p>
    </div> -->

    <!-- movies 배열이 존재하고 길이가 0보다 클 때만 표시 -->
    <div v-if="movies && movies.length > 0" class="movies-section">
      <h2>추천 영화:</h2>
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
      <p>음성 분석 중...</p>
    </div>
  </div>
</template>

<script setup>
// 필요한 모듈과 컴포넌트 import
import { ref, onMounted } from 'vue'
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
  // 이미 녹음 중이면 함수 종료
  if (isRecording.value) return;

  // 로딩 상태 시작
  isLoading.value = true;

  // 사용자의 마이크 접근 권한 요청 및 오디오 스트림 설정
  navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,      // 에코 제거
      noiseSuppression: true,      // 노이즈 제거
      autoGainControl: true,       // 자동 게인 제어
      sampleRate: 44100,           // 샘플링 레이트 설정
      channelCount: 1,             // 모노 채널 사용
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
      document.querySelector('.search-wrapper').appendChild(recordingIndicator);

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
        NotAllowedError: '마이크 사용 권한이 거부되었습니다.',
        NotFoundError: '마이크를 찾을 수 없습니다.',
        NotReadableError: '마이크에 접근할 수 없습니다.',
      };
      alert(errorMessages[error.name] || '오디오 입력 장치 오류가 발생했습니다.');
      isRecording.value = false;
      isLoading.value = false;
    });
};

// 컴포넌트 마운트 시 초기화
onMounted(() => {
  // URL의 query params에서 데이터 가져오기
  const queryTranscript = route.query.transcript;
  const querySentiment = route.query.sentiment;
  const queryMovies = route.query.movies;

  if (queryTranscript && querySentiment && queryMovies) {
    // 기본 데이터 설정
    transcript.value = queryTranscript;
    sentiment.value = Number(querySentiment);
    searchQuery.value = queryTranscript;
    
    // movies 데이터 파싱 및 설정
    try {
      let parsedMovies;
      
      // queryMovies가 이미 객체인 경우
      if (typeof queryMovies === 'object') {
        parsedMovies = queryMovies;
      } else {
        // 문자열인 경우 파싱 시도
        try {
          parsedMovies = JSON.parse(queryMovies);
        } catch (e) {
          // 첫 번째 파싱 시도가 실패하면 이스케이프된 문자열 처리 시도
          parsedMovies = JSON.parse(decodeURIComponent(queryMovies));
        }
      }

      if (Array.isArray(parsedMovies)) {
        movies.value = parsedMovies.map(movie => ({
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
      console.error('Movies parsing error:', error);
      console.log('Failed to parse movies data:', queryMovies);
      movies.value = [];
    }

    // 데이터 설정이 완료된 후 URL 정리
    router.replace({ path: '/search' });
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
</script>

<style scoped src="./css/search.css" ></style>

