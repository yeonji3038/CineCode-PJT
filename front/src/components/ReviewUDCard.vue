<template>
    <div class="review-card">
    <div class="review-header">
      <div class="user-info-container">
        <div class="profile-image-container">
          <img :src="profileImageSrc" :alt="review.user.username" class="user-profile">
        </div>
        <div class="review-info">
          <div class="username">{{ review.user.username }}</div>
          <div class="created-at">{{ formattedDate }}</div>
        </div>
      </div>
      <div class="review-likes">
        <button @click="handleLike" class="like-button"
        :disabled="!authStore.isLogin || review.user.username === authStore.username">
          👍 {{ review.likes }}
        </button>
      </div>
    </div>
    <div class="review-content">
      <img :src="`https://image.tmdb.org/t/p/w500${review.movie.poster_path}`" alt="Movie Poster" class="movie-poster"
        @click="goToMovieDetail"
      />
      <div class="review-details">
        <h3>{{ review.movie.title }}</h3>
        <div v-if="isEditing">
          <textarea v-model="editedContent" class="edit-textarea" placeholder="리뷰를 작성해주세요"></textarea>
          <div class="controls">
            <label class="label">
              스포일러
              <input type="checkbox" v-model="editedSpoiler" class="checkbox"/>
            </label>
            <div class="button-group">
              <button @click="saveEdit" class="edit-button">수정</button>
              <button @click="cancelEdit" class="cancel-button">취소</button>
            </div>
          </div>
        </div>
        <div v-else class="review-text">
          <p v-if="!review.is_spoiler || showContent">{{ review.content }}</p>
          <button v-else @click="showContent = true" class="spoiler-button">
            스포일러가 포함된 리뷰입니다.
          </button>
          <div class="controls" v-if="isOwner">
            <button @click="startEdit" class="edit-button">수정</button>
            <button @click="deleteReview" class="delete-button">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useReviewStore } from '@/stores/review'
  import defaultProfileImage from '@/assets/profile.png'
  
  const props = defineProps({
    review: {
      type: Object,
      required: true
    },
    movieTitle: String,
    moviePosterPath: String
  })
  
  const authStore = useAuthStore()
  const reviewStore = useReviewStore()
  const router = useRouter()
  
  const emit = defineEmits(['review-updated', 'review-deleted'])
  const isEditing = ref(false)
  const editedContent = ref('')
  const editedSpoiler = ref(false)
  const showContent = ref(false)
  
  // 프로필 이미지 computed 속성
  const profileImageSrc = computed(() => {
    return props.review.user.profile_image || defaultProfileImage
  })
  
  // 현재 사용자가 리뷰 작성자인지 확인
  const isOwner = computed(() => {
    return authStore.username === props.review.user.username
  })

  const formattedDate = computed(() => {
    const createdAt = new Date(props.review.created_at)
    const now = new Date()
    const diff = now - createdAt

    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)
    const months = Math.floor(days / 30)
    const years = Math.floor(months / 12)

    if (minutes < 60) return `${minutes}분 전`
    if (hours < 24) return `${hours}시간 전`
    if (days < 30) return `${days}일 전`
    if (months < 12) return `${months}달 전`
    return `${years}년 전`
  })

  const goToMovieDetail = () => {
    router.push(`/movies/${props.review.movie.id}`)
  }
  
  // 수정 시작
  const startEdit = () => {
    editedContent.value = props.review.content
    editedSpoiler.value = props.review.is_spoiler
    isEditing.value = true
  }
  
  // 수정 취소
  const cancelEdit = () => {
    isEditing.value = false
    editedContent.value = props.review.content
    editedSpoiler.value = props.review.is_spoiler
  }
  
  // 수정 저장
const saveEdit = () => {
  if (!editedContent.value.trim()) {
    alert('리뷰 내용을 입력해주세요.')
    return
  }
  const updatedReview = {
    content: editedContent.value,
    is_spoiler: editedSpoiler.value
  }
  reviewStore.updateReview(props.review.id, updatedReview)
    .then(() => {
      // 리뷰 객체 직접 업데이트
      props.review.content = editedContent.value
      props.review.is_spoiler = editedSpoiler.value
      isEditing.value = false
      emit('review-updated')
    })
    .catch((error) => {
      console.error('리뷰 수정 실패:', error)
    })
  }
  
  const deleteReview = () => {
    if (confirm('정말로 이 리뷰를 삭제하시겠습니까?')) {
      reviewStore.deleteReview(props.review.id)
        .then(() => {
          emit('review-deleted')
        })
        .catch((error) => {
          console.error('리뷰 삭제 실패:', error)
        })
    }
  }
  
  const handleLike = () => {
    if (isOwner.value) {
      alert('자신의 리뷰는 좋아요할 수 없습니다.')
      return
    }
    
    reviewStore.toggleReviewLike(props.review.id)
      .catch((error) => {
        console.error('리뷰 좋아요 실패:', error)
      })
  }
</script>
  
<style scoped src="./css/reviewUd.css">

</style>