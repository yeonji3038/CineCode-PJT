import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = import.meta.env.VITE_APP_URL
  const router = useRouter()

  // 사용자 인증 상태 관리 토큰
  const token = ref(null)
  const username = ref('')
  const profileImage = ref('')
  const email = ref('')

  // 로그인 상태 확인
  const isLogin = computed(() => {
    return token.value !== null
  })

  // 사용자 정보 가져오기
  const fetchUserInfo = function () {
    axios({
      method: 'get',
      url: `${API_URL}accounts/profile/`,
      headers: { Authorization: `Token ${token.value}` }
    })
    .then((res) => {
      // 상태 업데이트
      username.value = res.data.username
      email.value = res.data.email
      profileImage.value = res.data.profile_image
      
      // localStorage에 저장
      localStorage.setItem('username', res.data.username)
      localStorage.setItem('email', res.data.email)
      if (userData.profile_image) {
        localStorage.setItem('profileImage', userData.profile_image)
      }
    })
    .catch((err) => {
      console.error('사용자 정보 가져오기 실패:', err)
      // 토큰이 유효하지 않은 경우 로그아웃 처리
      if (err.response?.status === 401) {
        logout()
      }
    })
  }

  // 로그인 함수
  const login = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}accounts/login/`,
      data: {
        username: payload.login_username,
        password: payload.login_password
      }
    })
    .then((res) => {
      token.value = res.data.key
      localStorage.setItem('token', res.data.key)
      
      // 사용자 정보 가져오기
      fetchUserInfo()
      router.push({ name: 'Home' })
    })
    .catch((err) => {
      console.error('로그인 실패:', err)
    })
  }

  // 로그아웃
  const logout = () => {
    token.value = null
    username.value = ''
    email.value = ''
    profileImage.value = ''
    
    // localStorage 클리어
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('email')
    localStorage.removeItem('profileImage')
    
    router.push({ name: 'Login' })
  }

  // 회원정보 업데이트 함수만 추가
  const updateUser = async (payload) => {
    try {
      const formData = new FormData()
      
      if (payload.email) formData.append('email', payload.email)
      if (payload.password1) formData.append('password', payload.password1)
      if (payload.profile_image) formData.append('profile_image', payload.profile_image)

      const response = await axios({
        method: 'put',
        url: `${API_URL}accounts/update/`,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Token ${token.value}`
        }
      })

      if (response.data.email) {
        email.value = response.data.email
      }

      return response.data
    } catch (error) {
      throw error.response?.data || '회원정보 업데이트에 실패했습니다.'
    }
  }

  return { API_URL, token, isLogin, username, profileImage, email, login, logout, fetchUserInfo, updateUser }
}, { persist: {key: 'auth', storage: localStorage, paths: ['token', 'username', 'email', 'profileImage']}
})  // Pinia의 persist 플러그인을 사용해 상태 저장
