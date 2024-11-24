<template>
  <button 
    @click="handleLikeClick" 
    class="like-button"
    :class="buttonStyle.class"
  >
    <i :class="buttonStyle.icon"></i>
    {{ buttonStyle.text }}
  </button>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const movieStore = useMovieStore()
const router = useRouter()
const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

const buttonStyle = computed(() => {
  const styles = {
    liked: {
      text: '찜 취소',
      class: 'liked',
      icon: 'bi bi-heart-fill'
    },
    default: {
      text: '찜',
      class: '',
      icon: 'bi bi-heart'
    }
  }
  
  // 로그인 체크
  if (!authStore.isLogin) {
    return styles.default
  }
  
  // likedMovies 배열에서 현재 영화 확인
  const isLiked = movieStore.likedMovies.some(m => m.id === props.movie.id)
  return isLiked ? styles.liked : styles.default
})

const handleWatchClick = () => {
  if (!authStore.isLogin) {
    router.push('/login')
    return
  }
  movieStore.toggleWatchStatus(props.movie)
    .then(() => {
      console.log('Watch status toggled successfully')
    })
    .catch((error) => {
      console.error('Failed to toggle watch status:', error)
    })
}

// 상태 변경 시 컴포넌트 리렌더링
watch(() => movieStore.watchedMovies, () => {
  console.log('Watched movies updated')
})
</script>

<style scoped>
.like-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 0.8rem 2rem;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  font-size: 1.2rem;
  background-color: #D9D9D9;
  color: #000000;
  transition: all 0.2s;
  min-width: 140px;
}

.like-button i {
  display: flex;
  align-items: center;
  font-size: 1.2rem;
}

.like-button.liked {
  background-color: #000000;
  color: #ffffff;
}

.like-button:hover {
  opacity: 0.8;
}
</style>