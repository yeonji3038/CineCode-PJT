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
import LikeIcon from '@/assets/like-icon.svg'
import LikeFillIcon from '@/assets/like-fill-icon.svg'

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
      icon: LikeFillIcon
    },
    default: {
      text: '찜하기',
      class: 'unliked',
      icon: LikeIcon
    }
  }
  
  if (!authStore.isLogin) {
    return styles.default
  }
  
  const isLiked = movieStore.likedMovies.some(m => m.id === props.movie.id)
  return isLiked ? styles.liked : styles.default
})

const handleLikeClick = () => {
  if (!authStore.isLogin) {
    router.push('/accounts/login')
    return
  }

  movieStore.toggleLikeStatus(props.movie)
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
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1.2rem;
  font-family: 'Noto Sans KR';
  background-color: #D9D9D9;
  color: #000000;
  transition: all 0.2s;
  min-width: 140px;
}

.button-icon {
  width: 17px;
  height: 17px;
}


.like-button.liked {
  background-color: #000000;
  color: #ffffff;
}

.like-button:hover {
  opacity: 0.8;
}
</style>