<template>
    <div class="review-card">
      <div class="header">
        <div class="user-info">
          <img :src="profileImageSrc" :alt="review.username" class="profile-image">
          <span class="username">{{ review.username }}</span>
        </div>
        <div class="like-section">
          <button @click="handleLike" class="like-button">
            👍 {{ review.likes }}
          </button>
        </div>
      </div>
      <div class="content">
        <img :src="moviePosterPath" alt="Movie Poster" class="movie-poster" />
        <div class="review-content">
          <h3>{{ movieTitle }}</h3>
          <div v-if="isEditing">
            <textarea v-model="editedContent" class="edit-textarea"></textarea>
            <div class="controls">
              <label class="label">
                스포일러
                <input type="checkbox" v-model="editedSpoiler" class="checkbox"/>
              </label>
              <div class="button-group">
                <button @click="saveEdit" class="save-button">수정</button>
                <button @click="cancelEdit" class="cancel-button">취소</button>
              </div>
            </div>
          </div>
          <div v-else>
            <p :class="{ 'spoiler': review.is_spoiler }">{{ review.content }}</p>
            <div class="controls">
              <div class="spoiler-tag" v-if="review.is_spoiler">스포일러 있음</div>
              <div class="button-group" v-if="isOwner">
                <button @click="startEdit" class="edit-button">수정</button>
                <button @click="deleteReview" class="delete-button">삭제</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useReviewStore } from '@/stores/review'
  import defaultProfileImage from '@/assets/profile.png'
  
  const props = defineProps({
    review: Object,
    movieTitle: String,
    moviePosterPath: String
  })
  
  const emit = defineEmits(['review-updated', 'review-deleted'])
  const authStore = useAuthStore()
  const reviewStore = useReviewStore()
  
  const isEditing = ref(false)
  const editedContent = ref('')
  const editedSpoiler = ref(false)
  
  // 프로필 이미지 computed 속성
  const profileImageSrc = computed(() => {
    return props.review.profile_image || defaultProfileImage
  })
  
  // 현재 사용자가 리뷰 작성자인지 확인
  const isOwner = computed(() => {
    return authStore.username === props.review.username
  })
  
  const startEdit = () => {
    editedContent.value = props.review.content
    editedSpoiler.value = props.review.is_spoiler
    isEditing.value = true
  }
  
  const cancelEdit = () => {
    isEditing.value = false
  }
  
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
    background-color: #d9d9d9;
    padding: 20px;
    border-radius: 8px;
    margin: 20px auto;
    max-width: 800px;
    color: #000000;
    font-family: 'Inter', sans-serif;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 10px;
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .profile-image {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .username {
    font-size: 1rem;
    font-weight: bold;
  }
  
  .content {
    display: flex;
    margin-top: 20px;
  }
  
  .movie-poster {
    width: 114px;
    height: 171px;
    border-radius: 8px;
    margin-right: 20px;
  }
  
  .review-content {
    flex: 1;
  }
  
  .edit-textarea {
    width: 99%;
    height: 100px;
    border: none;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    font-family: 'Inter', sans-serif;
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
  
  button {
    background-color: #A7A7A7;
    color: white;
    border: none;
    padding: 5px 15px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  button:hover {
    background-color: rgb(211, 47, 39);
    color: black;
  }
  
  .spoiler {
    background-color: #eee;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .spoiler-tag {
    color: #ff4444;
    font-size: 0.9rem;
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
  
  .label {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .checkbox {
    width: 16px;
    height: 16px;
    margin: 0;
    cursor: pointer;
  }
  </style>