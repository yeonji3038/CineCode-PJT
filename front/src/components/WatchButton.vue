<template>
  <button :class="watchButtonClass" @click="handleWatchClick"> {{ watchButtonText }} </button>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'
const authStore = useAuthStore()
const movieStore = useMovieStore()
const router = useRouter()
const props = defineProps({
  movie: Object
})

// 재생 버튼 텍스트
const watchButtonText = computed(() => {
  switch (props.movie?.status) {
    case '미시청':
      return '재생'
    case '시청 중':
      return '이어서 보기'
    case '시청 완료':
      return '다시 보기'
    default:
      return '재생'
  }
})

// 재생 버튼 스타일
const watchButtonClass = computed(() => {
  switch (props.movie?.status) {
    case '미시청':
      return 'watch-button play'
    case '시청 중':
      return 'watch-button continue'
    case '시청 완료':
      return 'watch-button replay'
    default:
      return 'watch-button play'
  }
})

const handleWatchClick = () => {
  if (!authStore.token) {
    router.push('/login');
    return;
  }
  movieStore.toggleWatchStatus(props.movie)
};
</script>

<style scoped>
.watch-button {
  padding: 10px 20px;
  border-radius: 15px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.play {
  background-color: #000;
  color: #fff;
}

.continue {
  background-color: #555;
  color: #fff;
}

.replay {
  background-color: #888;
  color: #fff;
}
</style>