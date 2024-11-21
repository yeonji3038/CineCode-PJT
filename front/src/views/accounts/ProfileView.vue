<template>
  <div class="profile-container dark-mode">
    <!-- 상단 프로필 영역 -->
    <div class="profile-header">
      <div class="profile-img-container">
        <img src="@/views/accounts/img/profile.png" alt="Profile Image" class="profile-img" />
      </div>
      <div class="profile-info">
        <h3>{{ authStore.username }}</h3>
        <p>{{ authStore.email }}</p>
        <router-link to="/accounts/update" class="contact-btn">회원정보 수정</router-link>
      </div>
    </div>

    <!-- Activity 영역 -->
    <div class="activity-section">
      <div class="activity-item" @click="toggleReviews" :class="{ 'active': showReviews }">
        <h5>Reviews Written</h5>
        <p>{{ userInfo.review_count || 0 }}</p>
      </div>
      <div class="activity-item">
        <h5>Likes</h5>
        <p>{{ userInfo.likes_count || 0 }}</p>
      </div>
      <div class="activity-item">
        <h5>Followers</h5>
        <p>{{ userInfo.followers_count || 0 }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const userInfo = ref({})
const showReviews = ref(false)
const reviews = ref([])

// const fetchUserInfo = () => {
//   axios({
//     method: 'get',
//     url: `${import.meta.env.VITE_APP_URL}accounts/profile/`,
//     headers: {
//        'Authorization': `Token ${authStore.token}`
//     }
//   })
//     .then((res) => {
//       console.log('사용자 정보:', res.data)
//       userInfo.value = res.data
//     })
//     .catch((err) => {
//       console.error('사용자 정보 가져오기 실패:', err)
//     })
// }

onMounted(() => {
  if (authStore.isLogin) {
    authStore.fetchUserInfo()
  }
})
</script>

<style scoped src="./css/profile.css"></style>
