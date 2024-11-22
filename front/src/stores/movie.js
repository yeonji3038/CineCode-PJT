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

  // WatchButton : 영화 시청 상태 업데이트
  const toggleWatchStatus = (movie) => {
    if (!authStore.token) return

    axios.post(`${SERVER_URL}movies/${movie.id}/watch/`, null, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    .then((response) => {
      console.log(response.data.message)
      // 상태 업데이트 후 시청 목록 다시 불러오기
      fetchWatchedMovies()
    })
    .catch((error) => {
      console.error('시청 상태 변경 실패:', error)
    })
  }

  // LikeButton : 영화 찜 상태 업데이트
  // 찜하기 상태 토글
  const toggleLikeStatus = (movie) => {
    if (!authStore.token) return

    axios.post(`${SERVER_URL}movies/${movie.id}/like/`, null, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    .then((response) => {
      console.log(response.data.message)
      // 상태 업데이트 후 찜 목록 다시 불러오기
      fetchLikedMovies()
    })
    .catch((error) => {
      console.error('찜하기 상태 변경 실패:', error)
    })
  }

  return { movies, watchedMovies, likedMovies, fetchAllMovies, fetchWatchedMovies, fetchLikedMovies, toggleWatchStatus, toggleLikeStatus }
}, { persist: true })