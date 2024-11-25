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
      <img :src="review.movie.poster_path" alt="Movie Poster" class="movie-poster"
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
    }
  })
  
  const authStore = useAuthStore()
  const reviewStore = useReviewStore()
  const router = useRouter()
  
  const emit = defineEmits(['review-updated', 'review-deleted'])
  const isEditing = ref(false)
  const editedContent = ref('')
  const editedSpoiler = ref(false)
  
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
  
<style scoped>
  .review-card {
  width: 100%;  
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
  color: #000;
}

.review-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  width: 100%;
}

.user-info-container {
  display: flex;
  align-items: center;
}

.profile-image-container {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.user-profile {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-info {
  margin-left: 10px;
}

.username {
  font-size: 1rem;
  font-weight: bold;
}

.created-at {
  color: #888;
  font-size: 0.9em;
}

.review-likes {
  margin-left: auto;
  display: flex;
  align-items: center;
}

.like-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 5px 10px;
}

.like-button:hover {
  background-color: #eee;
}

.like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.review-content {
  display: flex;
  margin-top: 16px;
}

.movie-poster {
  width: 100px;
  height: 150px;
  margin-right: 20px;
  border-radius: 4px;
  transition: transform 0.2s;
  cursor: pointer;
}

.movie-poster:hover {
  transform: scale(1.05);
}

.review-details {
  flex: 1;
}

.review-text {
  margin-top: 8px;
}

.edit-textarea {
  width: 100%;
  min-height: 100px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin: 10px 0;
  font-family: inherit;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.button-group {
  display: flex;
  gap: 10px;
}

.edit-button, .delete-button, .cancel-button {
  padding: 5px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  color: white;
}

.edit-button {
  background-color: #A7A7A7;
}

.delete-button {
  background-color: #dc3545;
}

.cancel-button {
  background-color: #6c757d;
}

.spoiler-button {
  width: 100%;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 12px;
  border-radius: 4px;
  cursor: pointer;
  color: #666;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.spoiler-button:hover {
  background-color: #e0e0e0;
}
</style>