<template>
  <div class="watch-button-group">
    <button class="watch-button" @click="handleWatchClick" :class="buttonStyle.class">
      <img :src="buttonStyle.icon" alt="icon" class="button-icon"/>
      {{ buttonStyle.text }}
    </button>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'
import PlayIcon from '@/assets/play-icon.svg'
import ContinueIcon from '@/assets/continue-icon.svg'
import ReplayIcon from '@/assets/replay-icon.svg'

const authStore = useAuthStore()
const movieStore = useMovieStore()
const router = useRouter()
const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

// 버튼 스타일과 텍스트를 한번에 관리
const buttonStyle = computed(() => {
  const styles = {
    '미시청': {
      text: '재생',
      class: 'play',
      icon: PlayIcon
    },
    '시청 중': {
      text: '이어서 보기',
      class: 'continue',
      icon: ContinueIcon
    },
    '시청 완료': {
      text: '다시 보기',
      class: 'replay',
      icon: ReplayIcon
    }
  }
  
  // 로그인 체크 추가
  if (!authStore.isLogin) {
    return styles['미시청']
  }
  
  // watchedMovies 배열에서 현재 영화 확인
  const isWatched = movieStore.watchedMovies.some(m => m.id === props.movie.id)
  return styles[isWatched ? '시청 중' : '미시청']
})

const handleWatchClick = () => {
  if (!authStore.isLogin) {
    router.push('/accounts/login')
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
.watch-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 0.8rem 2rem;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  font-size: 1.2rem;
  transition: all 0.2s;
  min-width: 140px;
}

.button-icon {
  width: 17px;
  height: 17px;
}

.watch-button.play {
  background-color: rgb(211, 47, 39);
  color: #ffffff;
}

.watch-button.continue,
.watch-button.replay {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.watch-button:hover {
  opacity: 0.8;
}
</style>