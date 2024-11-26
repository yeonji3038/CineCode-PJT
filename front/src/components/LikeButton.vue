<template>
  <button 
    @click="handleLikeClick" 
    class="like-button"
    :class="buttonStyle.class"
  >
    <img :src="buttonStyle.icon" class="button-icon">
    {{ buttonStyle.text }}
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'
import LikeIcon from '@/assets/heart-icon.svg'
import LikeFillIcon from '@/assets/heart-fill-icon.svg'

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

  const isLiked = movieStore.likedMovies.some(m => m.movie?.id === props.movie.id)
  return isLiked ? styles.liked : styles.default
})

const handleLikeClick = async () => {
  if (!authStore.isLogin) {
    router.push('/accounts/login')
    return
  }

  try {
    await movieStore.toggleLikeStatus(props.movie)
  } catch (error) {
    console.error('Failed to toggle like status:', error)
  }
}
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
  background-color: #484848;
  color: #ffffff;
}

.like-button:hover {
  opacity: 0.8;
}
</style>