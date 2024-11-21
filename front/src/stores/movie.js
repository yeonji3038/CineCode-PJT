import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

export const useMovieStore = defineStore('movie', () => {
  const authStore = useAuthStore()
  const SERVER_URL = import.meta.env.VITE_APP_URL;  // 환경 변수로 서버 URL 가져오기
  const movies = ref([])
  const watchedMovies = ref([])
  const likedMovies = ref([])

  // 영화 데이터 가져오기
  const fetchMovies = () => {
    axios({
      method: 'get',
      url: `${SERVER_URL}movies/`
    })
      .then((response) => {
        movies.value = response.data
      })
      .catch((error) => {
        console.error('영화 데이터 로딩 실패:', error)
      })
  }

  // 시청 중인 영화 가져오기
  const fetchWatchedMovies = function() {
    if (!authStore.token) return

    axios({
      method: 'get',
      url: `${SERVER_URL}movies/watched/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then((res) => {
      watchedMovies.value = res.data
    })
    .catch((err) => {
      console.error('시청 중인 영화 가져오기 실패:', err)
      watchedMovies.value = []
    })
  }

  // 찜한 영화 가져오기
  const fetchLikedMovies = function() {
    if (!authStore.token) return

    axios({
      method: 'get',
      url: `${SERVER_URL}movies/liked/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
    .then((res) => {
      likedMovies.value = res.data
    })
    .catch((err) => {
      console.error('찜한 영화 가져오기 실패:', err)
      likedMovies.value = []
    })
  }

  // movie store에 추가
const getMovieDetail = (movieId) => {
  return axios({
    method: 'get',
    url: `${SERVER_URL}movies/${movieId}/detail/`,
    headers: authStore.token ? {
      Authorization: `Token ${authStore.token}`
    } : {}
  })
    .then((res) => {
      return res.data
    })
    .catch((err) => {
      console.error('영화 상세 정보 로딩 실패:', err)
      throw err
    })
}

  return { movies, watchedMovies, likedMovies, fetchMovies, fetchWatchedMovies, fetchLikedMovies, getMovieDetail }
}, { persist: true })