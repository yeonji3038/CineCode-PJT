<template>
    <div class="movie-card" @click="goToDetail">
      <img :src="movie.poster_path" :alt="movie.title">
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const props = defineProps({
    movie: {
        type: Object,
        required: true,
        validator(movie) {
        return movie.id && 
                movie.title && 
                movie.poster_path !== undefined
        }
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
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0 25px rgba(224, 224, 224, 0.3);
}

.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.3s ease;
  display: block;
}

.movie-card:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.movie-card:hover img {
  filter: brightness(0.7);
}

@media screen and (max-width: 1200px) {
  .movie-card {
    min-width: 250px;
    width: 250px;
    height: 375px;
  }
}

@media screen and (max-width: 768px) {
  .movie-card {
    min-width: 200px;
    width: 200px;
    height: 300px;
  }
}
  </style>