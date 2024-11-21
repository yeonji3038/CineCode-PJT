<template>
  <div class="search-results">
    <div class="analysis-result" v-if="recognizedText">
      <h2>인식된 텍스트:</h2>
      <p>{{ recognizedText }}</p>
      <h3>감정 분석 결과:</h3>
      <p>{{ getSentimentText(sentiment) }}</p>
    </div>

    <div class="recommended-movies" v-if="recommendedMovies.length">
      <h2>추천 영화</h2>
      <div class="movie-grid">
        <MovieCard 
          v-for="movie in recommendedMovies" 
          :key="movie.id"
          :movie="movie"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieCard from '@/components/MovieCard.vue'

const recognizedText = ref('')
const sentiment = ref(0)
const recommendedMovies = ref([])

const getSentimentText = (score) => {
  if (score > 0.3) return '긍정적인 감정이 느껴져요!'
  if (score < -0.3) return '부정적인 감정이 느껴져요.'
  return '중립적인 감정이네요.'
}

defineProps({
  searchResults: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
.search-results {
  padding: 20px;
}

.analysis-result {
  margin-bottom: 30px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
</style>