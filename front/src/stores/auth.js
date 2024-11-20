import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = import.meta.env.VITE_APP_URL
  const router = useRouter()

  // 사용자 인증 상태 관리 토큰
  const token = ref(localStorage.getItem('token') || null)
  const username = ref(null)
  const profileImage = ref(null)

  // 로그인 상태 확인
  const isLogin = computed(() => {
    return token.value !== null
  })

  // 사용자 정보 가져오기
  const fetchUserInfo = function () {
    if (!token.value) return

    axios({
      method: 'get',
      url: `${API_URL}accounts/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      username.value = response.data.username
      profileImage.value = response.data.profile_image
    })
    .catch((err) => {
      console.error('사용자 정보 가져오기 실패:', err)
    })
  }

  // 로그인
  const login = function (payload) {
    const { login_username, login_password } = payload

    axios({
      method: 'post',
      url: `${API_URL}accounts/login/`,
      data: {
        username: login_username,
        password: login_password
      }
    })
    .then((res) => {
      token.value = res.data.key
      console.log(res.data)
      localStorage.setItem('token', res.data.key) // 토큰을 로컬스토리지에 저장
      fetchUserInfo()
      router.push({ name: 'Home' })
    })
    .catch((err) => {
      console.log(err)
    })
  }

  // 로그아웃
  const logout = function () {
    axios({
      method: 'post',
      url: `${API_URL}accounts/logout/`,
    })
    .then((res) => {  
      token.value = null
      username.value = null
      profileImage.value = null
      localStorage.removeItem('token') // 로컬스토리지에서 토큰 삭제
      router.push({ name: 'Home' })
    })
    .catch((err) => {
      console.log(err)
    })
  }

  // 초기화 함수
  const initialize = function () {
    if (token.value) {
      fetchUserInfo()
    }
  }

  // 앱 시작시 사용자 정보 가져오기
  initialize()

  return { API_URL, token, isLogin, username, profileImage, login, logout, fetchUserInfo }
}, { persist: true })  // Pinia의 persist 플러그인을 사용해 상태 저장
