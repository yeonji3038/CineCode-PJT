<template>
  <button :class="likeButtonClass" @click="handleLikeClick"> {{ likeButtonText }} </button>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const movieStore = useMovieStore()
const router = useRouter()
const props = defineProps({
  movie: Object
})
// 찜 버튼 텍스트 
const likeButtonText = ref(props.movie?.is_liked ? '찜 취소' : '찜하기')
// 찜 버튼 스타일
const likeButtonClass = computed(() => {
  return props.movie?.is_liked ? 'like-button liked' : 'like-button'
})

const handleLikeClick = () => {
  if (!authStore.token) {
    router.push('/login')
    return;
  }
  movieStore.toggleLikeStatus(props.movie);
  likeButtonText.value = props.movie?.is_liked ? '찜 취소' : '찜하기'
}
</script>

<style scoped>
.like-button {
  padding: 10px 20px;
  border-radius: 15px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, color 0.3s;
  background-color: #fff;
  color: #000;
  border: 1px solid #ccc;
}

.liked {
  background-color: #f00;
  color: #fff;
}
</style>