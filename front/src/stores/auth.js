import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()
  
  const token = ref(null)

  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  const setUser = function (payload) {
    user.value = payload
  }

  // 로그인
  const login = function (payload) {
    const { username, password } = payload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username,
        password
      }
    })
    .then((res) => {
      token.value = res.data.key
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
      url: `${API_URL}/accounts/logout/`,
    })
    .then((res) => {
      token.value = null
      router.push({ name: 'Home' })
    })
    .catch((err) => {
      console.log(err)
    })
  }

  return { API_URL, token, isLogin, login, logout }
}, {persist : true})
