import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = import.meta.env.VITE_APP_URL
  const router = useRouter()

  // 사용자 인증 상태 관리 토큰
  const token = ref(localStorage.getItem('token') || null)
  const username = ref(localStorage.getItem('username') || '')
  const profileImage = ref(localStorage.getItem('profileImage') || '')
  const email = ref(localStorage.getItem('email') || '')

  // 로그인 상태 확인
  const isLogin = computed(() => {
    return token.value !== null
  })

  // 사용자 정보를 localStorage에 저장하는 함수
  const saveUserToLocalStorage = (userData) => {
    localStorage.setItem('username', userData.username)
    localStorage.setItem('email', userData.email)
    if (userData.profile_image) {
      localStorage.setItem('profileImage', userData.profile_image)
    }
  }

  // 사용자 정보 가져오기
  const fetchUserInfo = async () => {
    if (!token.value) return

    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}accounts/profile/`,
        headers: {
          'Authorization': `Token ${token.value}`,
          'Content-Type': 'application/json',
        }
      })

      // 상태 업데이트
      username.value = response.data.username
      email.value = response.data.email
      profileImage.value = response.data.profile_image

      // localStorage에 저장
      saveUserToLocalStorage(response.data)
      
    } catch (err) {
      console.error('사용자 정보 가져오기 실패:', err.response || err)
      // 토큰이 유효하지 않은 경우 로그아웃 처리
      if (err.response?.status === 401) {
        logout()
      }
    }
  }

  // 로그인
  const login = async (payload) => {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}accounts/login/`,
        data: {
          username: payload.login_username,
          password: payload.login_password
        }
      })

      token.value = response.data.key
      localStorage.setItem('token', response.data.key)
      
      await fetchUserInfo()  // 로그인 후 사용자 정보 가져오기
      router.push({ name: 'Home' })
    } catch (err) {
      console.error('로그인 실패:', err.response || err)
      throw err
    }
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

  // 앱 초기화 시 자동으로 사용자 정보 가져오기
  const initialize = async () => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      token.value = storedToken
      // localStorage에서 기본 정보 복원
      username.value = localStorage.getItem('username') || ''
      email.value = localStorage.getItem('email') || ''
      profileImage.value = localStorage.getItem('profileImage') || ''
      
      // 서버에서 최신 정보 가져오기
      await fetchUserInfo()
    }
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

  return { API_URL, token, isLogin, username, profileImage, email, login, logout, fetchUserInfo, updateUser, initialize }
}, { persist: true })  // Pinia의 persist 플러그인을 사용해 상태 저장
