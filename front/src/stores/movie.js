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
  const movieDetail = ref(null)

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
  const fetchWatchedMovies = () => {
    if (!authStore.token) {
      watchedMovies.value = []
      return Promise.resolve()
    }
  
    return axios.get(`${SERVER_URL}movies/watched/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    .then((res) => {
      watchedMovies.value = res.data
      return res.data
    })
    .catch((err) => {
      console.error('Failed to load watched movies:', err)
      watchedMovies.value = []
      throw err
    })
  }


  // HomeView : 찜한 영화 가져오기
  const fetchLikedMovies = () => {
    if (!authStore.token) return Promise.resolve()
  
    return axios.get(`${SERVER_URL}movies/liked/`, {
      headers: { Authorization: `Token ${authStore.token}` }
    })
    .then((res) => {
      likedMovies.value = res.data
      console.log('Fetched likedMovies:', res.data)  // 디버깅
      return res.data
    })
    .catch((err) => {
      console.error('Failed to load liked movies:', err)
      likedMovies.value = []
      throw err
    })
  }


  // MovieDetailView : 영화 상세 정보 가져오기
  const fetchMovieDetail = (movieId) => {
    return axios.get(`${SERVER_URL}movies/${movieId}/detail/`)
      .then((response) => {
        movieDetail.value = response.data
        return response.data
      })
      .catch((error) => {
      console.error('영화 상세 정보를 불러오는데 실패했습니다:', error)
      throw error
    })
  }


  // WatchButton : 영화 시청 상태 업데이트
  const toggleWatchStatus = (movie) => {
    if (!authStore.token) return Promise.resolve()

      return axios.post(`${SERVER_URL}movies/${movie.id}/watch/`, null, {
        headers: { Authorization: `Token ${authStore.token}` }
      })
      .then((response) => {
        const isWatched = watchedMovies.value.some(w => w.movie.id === movie.id)
        
        if (!isWatched && movie.lastStatus === '시청 중') {
          // 미시청/시청완료 -> 시청 중으로 변경할 때
          watchedMovies.value.push({
            movie: { ...movie },
            watched_at: new Date().toISOString()
          })
        } else if (isWatched && movie.lastStatus === '시청 완료') {
          // 시청 중 -> 시청 완료로 변경할 때
          watchedMovies.value = watchedMovies.value.filter(w => w.movie.id !== movie.id)
        }
        
        return response.data
      })
      .catch((error) => {
        console.error('시청 상태 변경 실패:', error)
        throw error
      })
  }


// LikeButton : 영화 찜 상태 업데이트
const toggleLikeStatus = (movie) => {
  if (!authStore.token) return Promise.resolve()

  return axios.post(`${SERVER_URL}movies/${movie.id}/like/`, null, {
    headers: { Authorization: `Token ${authStore.token}` }
  })
  .then((response) => {
    // 서버 응답에서 상태를 가져옴
    const isLiked = response.data.is_liked
    
    if (!isLiked) {
      // 찜 취소: likedMovies에서 제거
      likedMovies.value = likedMovies.value.filter(m => m.id !== movie.id)
    } else {
      // 찜하기: likedMovies에 추가
      if (!likedMovies.value.some(m => m.id === movie.id)) {
        likedMovies.value.push(movie)
      }
    }

    // movies 배열에서도 해당 영화의 상태 업데이트
    const movieInList = movies.value.find(m => m.id === movie.id)
    if (movieInList) {
      movieInList.is_liked = isLiked
    }

    // movieDetail도 업데이트
    if (movieDetail.value?.id === movie.id) {
      movieDetail.value.is_liked = isLiked
    }

    return response.data
  })
  .catch((error) => {
    console.error('찜하기 상태 변경 실패:', error)
    throw error
  })
}

  return { movies, watchedMovies, likedMovies, movieDetail, fetchAllMovies, fetchWatchedMovies, fetchLikedMovies, fetchMovieDetail, toggleWatchStatus, toggleLikeStatus }
}, { persist: true })