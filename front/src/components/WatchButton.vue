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

// 버튼 computed 속성
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

  if (!authStore.isLogin) {
    return styles['미시청']
  }

  // watchedMovies에 있는지 확인
  const isWatched = movieStore.watchedMovies.some(w => w.movie.id === props.movie.id)
  
  if (isWatched) {
    return styles['시청 중']
  }
  return styles[props.movie.lastStatus === '시청 완료' ? '시청 완료' : '미시청']
})

// 클릭 핸들러
const handleWatchClick = () => {
  if (!authStore.isLogin) {
    router.push('/accounts/login')
    return
  }

  const isWatched = movieStore.watchedMovies.some(w => w.movie.id === props.movie.id)
  
  if (isWatched) {
    // 시청 중 -> 시청 완료
    props.movie.lastStatus = '시청 완료'
  } else if (props.movie.lastStatus === '시청 완료') {
    // 시청 완료 -> 시청 중
    props.movie.lastStatus = '시청 중'
  } else {
    // 미시청 -> 시청 중
    props.movie.lastStatus = '시청 중'
  }

  movieStore.toggleWatchStatus(props.movie)
}
</script>

<style scoped>
.watch-button {
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
  background-color: white;
  color: black;
}

.watch-button:hover {
  opacity: 0.8;
}
</style>