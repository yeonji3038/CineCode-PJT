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
  const likedReviewsCount = ref(0)

  // ReviewReadCard : 특정 영화의 리뷰 목록 가져오기
  const fetchReviews = (movieId) => {
    return axios.get(`${SERVER_URL}movies/reviews/`, {
      params: {
        movie_id: movieId
      }
    })
    .then((response) => {
      console.log('Fetched review data:', response.data)  // 받아온 데이터 확인
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
  
  // ReviewUDCard : 리뷰 수정하기 (인증 필요)
  const updateReview = (reviewId, updatedData) => {
    if (!authStore.isLogin) {
      router.push('/login')
      return Promise.reject('로그인이 필요합니다.')
    }
    return axios.put(`${SERVER_URL}movies/reviews/${reviewId}/`, updatedData, {
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then((response) => {
        // 로컬 상태 업데이트
        const index = reviews.value.findIndex(r => r.id === reviewId)
        if (index !== -1) {
          reviews.value[index] = {
            ...reviews.value[index],
            ...response.data
          }
        }
        return response.data
      })
      .catch((error) => {
      console.error('Failed to update review:', error)
      throw error
    })
  }

  // ReviewUDCard : 리뷰 삭제하기 (인증 필요)
  const deleteReview = (reviewId) => {
    if (!authStore.isLogin) {
    router.push('/login')
    return Promise.reject('로그인이 필요합니다.')
    }
    return axios.delete(`${SERVER_URL}movies/reviews/${reviewId}/`, {
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
      .then(() => {
        // 로컬 상태에서도 해당 리뷰 제거
        reviews.value = reviews.value.filter(review => review.id !== reviewId)
      })
      .catch((error) => {
        console.error('Failed to delete review:', error)
        throw error
      })
  }

  // ReviewCreateCard : 리뷰 좋아요 토글 (인증 필요)
  const toggleLike = (reviewId) => {
    if (!authStore.isLogin) {
      router.push('/accounts/login')
      return Promise.reject('로그인이 필요합니다.')
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
        // 좋아요 상태에 따라 카운트 업데이트
        updateLikedReviewsCount(response.data.is_liked)
        return response.data 
      })
      .catch((error) => {
        console.error('Failed to toggle like:', error)
        throw error
      })
    }

    const updateUserProfileImage = (username, newImage) => {
      return new Promise((resolve) => {
        reviews.value = reviews.value.map(review => {
          if (review.user.username === username) {
            return {
              ...review,
              user: {
                ...review.user,
                profile_image: newImage
              }
            }
          }
          return review
        })
        resolve()
      })
    }

    // 좋아요 토글 시 카운트 업데이트 수정
    const updateLikedReviewsCount = (isLiked) => {
      if (isLiked) {
        likedReviewsCount.value++
      } else {
        likedReviewsCount.value--
      }
    }

  return { reviews, fetchReviews, createReview, updateReview, deleteReview, toggleLike, updateUserProfileImage, likedReviewsCount, updateLikedReviewsCount }
})