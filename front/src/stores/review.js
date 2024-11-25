import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useReviewStore = defineStore('review', () => {
  const SERVER_URL = import.meta.env.VITE_APP_URL
  const authStore = useAuthStore()
  const router = useRouter()
  const reviews = ref([])

  // ReviewReadCard : 특정 영화의 리뷰 목록 가져오기
  const fetchReviews = (movieId) => {
    return axios.get(`${SERVER_URL}movies/reviews/`, {
      params: {
        movie_id: movieId
      }
    })
    .then((response) => {
      reviews.value = response.data
      return response.data
    })
    .catch((error) => {
      console.error('Failed to fetch reviews:', error)
      throw error
    })
  }

  // ReviewCreateCard : 리뷰 생성하기 (인증 필요)
  const createReview = (reviewData) => {
    if (!authStore.isLogin) {
      router.push('/login')
      return
    }
    
    return axios.post(`${SERVER_URL}movies/reviews/`, reviewData, {
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((response) => {
        reviews.value.push(response.data)
        return response.data
      })
      .catch((error) => {
        console.error('Failed to create review:', error)
        throw error
      })
  }
  
  // ReviewCreateCard : 리뷰 좋아요 토글 (인증 필요)
  const toggleLike = (reviewId) => {
    if (!authStore.isLogin) {
      router.push('/login')
      return
    }

    return axios.post(`${SERVER_URL}movies/reviews/${reviewId}/like/`, {}, {
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((response) => {
        const review = reviews.value.find(r => r.id === reviewId)
        if (review) {
          review.likes = response.data.likes
          review.is_liked = response.data.is_liked
        }
        return response.data
      })
      .catch((error) => {
        console.error('Failed to toggle like:', error)
        throw error
      })
    }


  return { reviews, fetchReviews, createReview, toggleLike }
})