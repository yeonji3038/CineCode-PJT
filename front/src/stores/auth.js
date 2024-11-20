import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = import.meta.env.VITE_APP_URL
  const router = useRouter()

  // 사용자 인증 상태 관리 토큰
  const token = ref(localStorage.getItem('token') || null)

  // 로그인 상태 확인
  const isLogin = computed(() => {
    return token.value !== null
  })

  // 로그인
  const login = function (payload) {
    const { username, password } = payload
    axios({
      method: 'post',
      url: `${API_URL}accounts/login/`,
      data: {
        username,
        password
      }
    })
    .then((res) => {
      token.value = res.data.key
      console.log(res.data)
      localStorage.setItem('token', res.data.key) // 토큰을 로컬스토리지에 저장
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
      localStorage.removeItem('token') // 로컬스토리지에서 토큰 삭제
      router.push({ name: 'Home' })
    })
    .catch((err) => {
      console.log(err)
    })
  }

  return { API_URL, token, isLogin, login, logout }
}, { persist: true })  // Pinia의 persist 플러그인을 사용해 상태 저장
