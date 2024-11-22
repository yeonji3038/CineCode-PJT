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

  // 전체 영화 가져오기
  const fetchAllMovies = () => {
    axios.get(`${SERVER_URL}movies/`)
      .then((response) => {
        movies.value = response.data
      })
      .catch((error) => {
        console.error('Failed to load movies:', error)
      })
  }

  // HomeView : 시청 중인 영화 가져오기
  const fetchWatchedMovies = function() {
    if (!authStore.token) return

    axios.get(`${SERVER_URL}movies/watched/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    .then((res) => {
      watchedMovies.value = res.data
    })
    .catch((err) => {
      console.error('Failed to load watched movies:', err)
      watchedMovies.value = []
    })
  }

  // HomeView : 찜한 영화 가져오기
  const fetchLikedMovies = function() {
    if (!authStore.token) return

    axios.get(`${SERVER_URL}movies/liked/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    .then((res) => {
      likedMovies.value = res.data
    })
    .catch((err) => {
      console.error('Failed to load liked movies:', err)
      likedMovies.value = []
    })
  }

  return { movies, watchedMovies, likedMovies, fetchAllMovies, fetchWatchedMovies, fetchLikedMovies }
}, { persist: true })