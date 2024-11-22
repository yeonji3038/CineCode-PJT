
<template>
  <div class="search">
    <h1>음성 감정 분석 결과</h1>

    <!-- transcript가 빈 문자열이 아닐 때만 표시,, -->
    <div v-if="transcript !== ''" class="result-section">
      <h2>말씀하신 내용:</h2>
      <p>{{ transcript }}</p>
    </div>

    <!-- sentiment가 null이 아닐 때만 표시 -->
    <div v-if="sentiment !== null" class="result-section">
      <h2>감정 분석 결과:</h2>
      <p>감정 점수: {{ sentiment }}</p>
    </div>

    <!-- movies 배열이 존재하고 길이가 0보다 클 때만 표시 -->
    <div v-if="movies && movies.length > 0" class="movies-section">
      <h2>추천 영화:</h2>
      <div class="movie-grid">
        <MovieCard 
          v-for="movie in movies" 
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MovieCard from '@/components/MovieCard.vue'

const route = useRoute()
const transcript = ref('')
const sentiment = ref(null)
const movies = ref([])

onMounted(() => {
  // 디버깅을 위한 로그
  console.log('Route query:', route.query)
  
  // query 파라미터 가져오기
  transcript.value = route.query.transcript || ''
  sentiment.value = route.query.sentiment || null
  
  try {
    // movies 문자열이 이미 JSON 형식인지 확인
    const moviesData = route.query.movies
    if (typeof moviesData === 'string') {
      // 문자열이 이스케이프된 JSON인 경우 처리
      const unescaped = moviesData.replace(/\\/g, '')
      movies.value = JSON.parse(unescaped.replace(/^"(.*)"$/, '$1'))
    } else {
      movies.value = []
    }
    console.log('Parsed movies:', movies.value)  // 파싱된 결과 확인
  } catch (error) {
    console.error('Movies parsing error:', error)
    movies.value = []
  }
})
</script>

<style scoped>
.search {
  padding: 20px;
}

.result-section {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.error {
  color: red;
  margin: 10px 0;
}
</style>