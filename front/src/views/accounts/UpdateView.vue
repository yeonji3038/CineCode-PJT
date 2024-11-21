<template>
  <div id="Signup">
    <div class="signup">
      <h2>Update Information</h2>
      
      <!-- 프로필 이미지 섹션 -->
      <div class="profile-img-container">
        <div class="profile-img-wrapper" @click="$refs.fileInput.click()">
          <img 
            src="@/views/accounts/img/profile.png"
            alt="Profile Image" 
            class="profile-img" 
          />
          <div class="profile-img-overlay">
            <span>이미지 변경</span>
          </div>
        </div>
        <input 
          type="file"
          ref="fileInput"
          @change="handleImageChange"
          accept="image/*"
          style="display: none"
        />
      </div>

      <div class="signup-info">
        <!-- username은 수정 불가능 -->
        <input
          placeholder="ID"
          type="text"
          v-model="credentials.username"
          readonly
        />
        <!-- 이메일 입력 필드 -->
        <input
          placeholder="Email"
          type="email"
          v-model="credentials.email"
          :class="{ 'input-error': emailErrorMessage }"
        />
        <div v-if="emailErrorMessage" class="error-message">
          {{ emailErrorMessage }}
        </div>

        <!-- 비밀번호 입력 필드 -->
        <input
          placeholder="New Password"
          type="password"
          v-model="credentials.password1"
          :class="{ 'input-error': passwordErrorMessage }"
        />
        <div v-if="passwordErrorMessage" class="error-message">
          {{ passwordErrorMessage }}
        </div>

        <input
          placeholder="Confirm New Password"
          type="password"
          v-model="credentials.password2"
          :class="{ 'input-error': confirmPasswordErrorMessage }"
        />
        <div v-if="confirmPasswordErrorMessage" class="error-message">
          {{ confirmPasswordErrorMessage }}
        </div>
      </div>
      <button @click="updateUserInfo" class="signup-button">UPDATE</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const errorMessage = ref('')
const emailErrorMessage = ref('')
const passwordErrorMessage = ref('')
const confirmPasswordErrorMessage = ref('')

const credentials = ref({
  username: authStore.username || '',
  email: authStore.email || '',
  password1: '',
  password2: '',
  profile_image: null
})

// updateUserInfo를 updateUser로 수정
const updateUserInfo = () => {
  if (credentials.value.password1 !== credentials.value.password2) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  const payload = {
    email: credentials.value.email,
    password1: credentials.value.password1 || null,
    password2: credentials.value.password2 || null,
    profile_image: credentials.value.profile_image || null
  }

  // updateUserInfo를 updateUser로 수정
  authStore.updateUser(payload)  // 여기를 수정
    .then(() => {
      alert('회원 정보가 성공적으로 업데이트되었습니다.')
      router.push({ name: 'Profile' })
    })
    .catch((error) => {
      errorMessage.value = error || '회원 정보 업데이트에 실패했습니다.'
      console.log(error)
    })
}

// 이미지 변경 처리
const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      event.target.previousElementSibling.querySelector('img').src = e.target.result
      credentials.value.profile_image = file
    }
    reader.readAsDataURL(file)
  }
}

onMounted(() => {
  credentials.value.username = authStore.username || ''
  credentials.value.email = authStore.email || ''
})
</script>

<style scoped src="./css/update.css">
</style>


