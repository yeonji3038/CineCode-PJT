import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const SERVER_URL = import.meta.env.VITE_APP_URL;  // 환경 변수로 서버 URL 가져오기
  const movies = ref([])

  // 영화 데이터 가져오기
  const fetchMovies = () => {
    axios({
      method: 'get',
      url: `${SERVER_URL}movies/`
    })
      .then((response) => {
        movies.value = response.data.movies
      })
      .catch((error) => {
        console.error('영화 데이터 로딩 실패:', error)
      })
  }

  return { movies,fetchMovies}
}, { persist: true })