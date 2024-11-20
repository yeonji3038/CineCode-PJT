<template>
    <div class="movie-card" @click="goToDetail">
      <div class="poster-container">
        <img :src="movie.poster_path" :alt="movie.title">
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const props = defineProps({
    movie: {
      type: Object,
      required: true
    }
  })
  
  const goToDetail = () => {
    router.push(`/movies/${props.movie.id}`)
  }
  </script>
  
  <style scoped>
  .movie-card {
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  
  .poster-container {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
  }
  
  .poster-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.3s ease;
  }
  
  .movie-card:hover {
    transform: scale(1.05);
  }
  
  .movie-card:hover img {
    filter: brightness(0.7);
  }
  </style>